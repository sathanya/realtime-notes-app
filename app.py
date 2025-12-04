# app.py
import os
from threading import Lock, Timer
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_PATH = os.path.join(BASE_DIR, "note.txt")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret'

# Use threading async mode (works reliably on Windows for dev)
socketio = SocketIO(app, async_mode='threading')

# Thread-safe shared state
note_content = ""
note_lock = Lock()
save_timer = None
SAVE_DELAY = 1.0  # seconds

def ensure_note_file():
    global note_content
    if not os.path.exists(NOTE_PATH):
        with open(NOTE_PATH, "w", encoding="utf-8") as f:
            f.write("")
        note_content = ""
    else:
        with open(NOTE_PATH, "r", encoding="utf-8") as f:
            note_content = f.read()

def _do_save():
    global save_timer
    with note_lock:
        try:
            with open(NOTE_PATH, "w", encoding="utf-8") as f:
                f.write(note_content)
            app.logger.info("Note saved to disk.")
        except Exception as e:
            app.logger.error("Error saving note: %s", e)
    save_timer = None

def schedule_save():
    """Debounced save using threading.Timer."""
    global save_timer
    # Cancel existing scheduled save
    if save_timer is not None:
        save_timer.cancel()
    # Schedule new save
    save_timer = Timer(SAVE_DELAY, _do_save)
    save_timer.daemon = True
    save_timer.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/healthz")
def healthz():
    return "OK", 200

@socketio.on("connect")
def handle_connect():
    app.logger.info("Client connected")
    with note_lock:
        emit("load-note", note_content)

@socketio.on("update-note")
def handle_update_note(data):
    global note_content
    # data is expected to be the full note text
    with note_lock:
        note_content = data or ""
    # broadcast update to all other clients (exclude sender)
    emit("update-note", data, broadcast=True, include_self=False)
    schedule_save()

if __name__ == "__main__":
    ensure_note_file()
    # Use socketio.run to run the server; threading mode is default here
    socketio.run(app, host="0.0.0.0", port=5000)
