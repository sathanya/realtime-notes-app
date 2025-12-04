📒 Real-Time Collaborative Notes App

A lightweight Flask + Socket.IO web application that allows multiple users to create, edit, and sync notes in real time.
Users can type simultaneously, and updates are instantly reflected across all connected clients.

🚀 Features

📝 Real-time note editing using Flask-SocketIO

👥 Multiple users can collaborate at once

🔄 Instant synchronization across all browsers

💾 Notes saved automatically to a file

🌐 Simple, clean UI with HTML/CSS/JS

⚡ Lightweight backend designed for beginners

🛠️ Tech Stack

Backend:

Python

Flask

Flask-SocketIO

Frontend:

HTML

CSS

JavaScript

📦 Installation & Setup
1️⃣ Clone this repository
git clone https://github.com/sathanya/realtime-notes.git
cd realtime-notes

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python app.py

4️⃣ Open in browser
http://localhost:5000

📁 Project Structure
realtime-notes/
│── app.py
│── requirements.txt
│── templates/
│     └── index.html
│── static/
      ├── style.css
      └── script.js

🧠 How It Works

Flask serves the web interface

Socket.IO establishes a persistent connection with all clients

When any user edits the note:

JavaScript detects the change

Sends update to server over WebSocket

Server broadcasts change to all connected clients

Notes are periodically saved to a text file

🎯 Future Improvements

User authentication

Multiple notes / note folders

Typing indicators

Dark mode UI

Export notes as PDF or Markdown

🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

📜 License

This project is open-source and free to use.
