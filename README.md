# PyRemoteShellLab
A lightweight multi-session remote access lab framework built in Python to teach ethical hacking, socket communication, and client-server architecture.
# PyRemoteShellLab

**PyRemoteShellLab** is a lightweight, Python-based Command and Control (C2) educational framework that demonstrates how multi-session remote access systems work. It enables students and ethical hackers to understand the core building blocks of remote shell management, socket communication, file transfer, and session control.

> 🚨 **Disclaimer:**
> This project is for **educational and lab use only.** Do not use it on unauthorized systems or networks. The author does not condone or take responsibility for any misuse.

---

## 🧠 What It Does

PyRemoteShellLab consists of two components:

### 1. **Server (C2 Controller)**
- Listens for incoming client connections
- Maintains multiple concurrent sessions using threading
- Offers an interactive shell to interact with any connected client
- Allows upload/download of files to/from clients
- Can background sessions, kill sessions, or re-establish them

### 2. **Client (Agent)**
- Connects back to the server (supports dynamic IP config in custom setups)
- Accepts shell commands and executes them on the host system
- Sends command output back to the server
- Supports file upload/download using base64
- Can take screenshots using `mss`
- Contains optional persistence feature using Windows registry

---

## 📦 Features Summary

| Feature                | Server Side        | Client Side        | Notes                                  |
|------------------------|--------------------|--------------------|----------------------------------------|
| Multi-session handling | ✅ Yes             | -                  | Threaded, each client gets a session ID|
| Remote shell           | ✅ Yes             | ✅ Yes             | Full command execution support         |
| File upload            | ✅ Yes             | ✅ Yes             | base64 encoded, works cross-platform   |
| File download          | ✅ Yes             | ✅ Yes             | base64 encoded                         |
| Screenshot             | -                  | ✅ Yes             | Saved temporarily then sent            |
| Persistence (optional) | -                  | ✅ Yes             | via `HKCU\...\Run` registry key        |
| Session management     | ✅ Yes             | -                  | Connect, kill, list, background        |

---

## 🛠 Lab Setup

You’ll need:
- Python 3.8+
- One Windows VM for running the client
- One Linux or Windows machine for running the server
- `mss`, `pyautogui`, and `requests` modules for full client capabilities

### Install Dependencies (client only):
```bash
pip install mss pyautogui requests
```

> Tip: Test in **VirtualBox or VMware** with Host-only or NAT networking.

---

## 🚀 How to Run

### Server:
```bash
python server.py
```
You’ll be dropped into the `Manager>` interactive prompt.

### Client:
```bash
python client.py
```
Client attempts to connect to the server IP defined in the script.

---

## 🕹 Server Commands

| Command                     | Description                                                  |
|-----------------------------|--------------------------------------------------------------|
| `sessions list`            | Lists all active client sessions                             |
| `connect <session_id>`     | Connects to a specific session for remote shell access       |
| `sessions kill <session_id>` | Closes and removes the specified session                    |
| `help`                     | Displays help menu                                           |

Inside a session shell (`Shell #<id>`):

| Command            | Description                                     |
|--------------------|-------------------------------------------------|
| `cd <path>`        | Change directory on the remote machine          |
| `download <file>`  | Download a file from the remote machine         |
| `upload <file>`    | Upload a file to the remote machine             |
| `screenshot`       | Capture and send a screenshot                   |
| `persist_enable`   | Enable registry-based persistence (lab only)    |
| `persist_disable`  | Remove persistence                              |
| `background`       | Return to session manager without disconnecting |
| `exit`             | Fully disconnect and kill the session           |
| `<any command>`    | Executes any OS command                         |

---

## 📁 Project Structure
```
PyRemoteShellLab/
├── client.py          # Python agent that connects back to server
├── server.py          # C2 server to manage multiple sessions
├── README.md          # Documentation
└── requirements.txt   # Optional dependency file for pip
```

---

## 🚧 Future Ideas (for learners)

- 🔐 Add AES encryption layer to secure comms
- 🕵️ Add sandbox detection / VM evasion for practice
- 📊 Log session activity and output
- 🌐 Add dynamic C2 discovery using hosted pages
- 🐍 Port to compiled formats with PyInstaller/Nuitka

---

## 👨‍💻 Author

Built by a 16-year-old student passionate about ethical hacking, offensive security, and Python development. This tool exists to help others learn the same skills — safely and responsibly.

If this helped you learn something, feel free to ⭐ the repo or fork it!

---

## 🔒 Note on Advanced Features

This public version of PyRemoteShellLab has been intentionally limited to preserve ethical boundaries and ensure compliance with open-source platform guidelines. 

Advanced modules such as:
- Privilege escalation techniques
- AV/EDR evasion logic
- Process injection and hollowing
- Browser credential extraction

have been **removed or redacted** from this repository.

> If you're an educator, student, researcher, or security professional with a legitimate reason to review the full version, feel free to reach out.

📧 **Request access:**  
Please contact me at pyremoteshelllab@proton.me with:
- Your name and organization  
- Your role (e.g. instructor, lab designer, infosec researcher)  
- A brief reason for the request

All requests will be considered on a case-by-case basis.

---

> ⚠️ Unauthorized use of advanced versions of this project for real-world exploitation is strictly prohibited. All full-featured variants are for academic and lab environments only.



## 📄 License

MIT License — Free to use for educational and ethical purposes.
Unauthorized or malicious use is strictly prohibited.

