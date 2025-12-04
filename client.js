// static/client.js
const socket = io(); // auto-connects to same host/port
const noteEl = document.getElementById('note');
const statusEl = document.getElementById('status');
const saveBtn = document.getElementById('saveBtn');

let isTyping = false;
let timeoutId = null;

// Connection status
socket.on('connect', () => {
  statusEl.textContent = 'Connected';
  statusEl.style.color = '#2a7f62';
});

socket.on('disconnect', () => {
  statusEl.textContent = 'Disconnected';
  statusEl.style.color = '#d9534f';
});

// Load initial note
socket.on('load-note', (data) => {
  noteEl.value = data || '';
});

// When others update, update the textarea carefully
socket.on('update-note', (data) => {
  if (isTyping) {
    // If user is typing, avoid immediate overwrite; small heuristic:
    if (Math.abs(data.length - noteEl.value.length) > 50) {
      noteEl.value = data;
    }
  } else {
    const pos = noteEl.selectionStart;
    noteEl.value = data;
    noteEl.selectionStart = noteEl.selectionEnd = Math.min(pos, noteEl.value.length);
  }
});

// Emit updates (debounced)
noteEl.addEventListener('input', () => {
  isTyping = true;
  const text = noteEl.value;
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    socket.emit('update-note', text);
    isTyping = false;
  }, 250);
});

// Manual save
saveBtn.addEventListener('click', () => {
  socket.emit('update-note', noteEl.value);
  statusEl.textContent = 'Saved';
  setTimeout(() => { statusEl.textContent = 'Connected'; }, 700);
});
