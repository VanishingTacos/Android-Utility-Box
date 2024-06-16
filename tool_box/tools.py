import tkinter as tk
import hashlib
import os
import threading
import subprocess
from tkinter import filedialog, Toplevel, ttk, messagebox
from tool_box.utils import log, update_progress, update_hash_result, execute_command
from queue import Queue, Empty

class Tools:
    @staticmethod
    def add_tools_menu(menu, app):
        menu.add_command(label="MD5 Checker", command=lambda: Tools.open_md5_checker(app))
        menu.add_command(label="SHA-256 Checker", command=lambda: Tools.open_sha256_checker(app))
        menu.add_command(label="View Logcat", command=lambda: Tools.view_logcat(app))
        menu.add_command(label="View dmesg", command=lambda: Tools.view_dmesg(app))

    @staticmethod
    def open_md5_checker(app):
        file_path = filedialog.askopenfilename()
        if file_path:
            hash_checker_window = tk.Toplevel(app.root)
            hash_checker_window.title("MD5 Checker")

            hash_label = tk.Label(hash_checker_window, text="Calculating MD5...")
            hash_label.pack(pady=10)

            progress = ttk.Progressbar(hash_checker_window, length=400, mode='determinate')
            progress.pack(pady=10)

            threading.Thread(target=Tools.calculate_md5, args=(app, file_path, hash_label, progress)).start()

    @staticmethod
    def open_sha256_checker(app):
        file_path = filedialog.askopenfilename()
        if file_path:
            hash_checker_window = tk.Toplevel(app.root)
            hash_checker_window.title("SHA-256 Checker")

            hash_label = tk.Label(hash_checker_window, text="Calculating SHA-256...")
            hash_label.pack(pady=10)

            progress = ttk.Progressbar(hash_checker_window, length=400, mode='determinate')
            progress.pack(pady=10)

            threading.Thread(target=Tools.calculate_sha256, args=(app, file_path, hash_label, progress)).start()

    @staticmethod
    def calculate_md5(app, file_path, hash_label, progress):
        Tools.calculate_hash(app, file_path, hashlib.md5(), "MD5", hash_label, progress)

    @staticmethod
    def calculate_sha256(app, file_path, hash_label, progress):
        Tools.calculate_hash(app, file_path, hashlib.sha256(), "SHA-256", hash_label, progress)

    @staticmethod
    @staticmethod
    def calculate_hash(app, file_path, hash_algorithm, hash_name, hash_label, progress):
        log(app, f"Calculating {hash_name} for: {file_path}")
        total_size = os.path.getsize(file_path)
        read_size = 0
        buffer_size = 8192  # read in chunks of 8KB

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(buffer_size), b""):
                hash_algorithm.update(chunk)
                read_size += len(chunk)
                progress_value  = (read_size / total_size) * 100
                update_progress(progress, progress_value)

        hash_result = hash_algorithm.hexdigest()
        update_hash_result(hash_label, hash_result, hash_name)
        log(app, f"{hash_name} Result: {hash_result}")
    
    @staticmethod
    def view_logcat(app):
        Tools.log_window(app, "Logcat Viewer", ["adb", "logcat"], continuous=True)

    @staticmethod
    def view_dmesg(app):
        execute_command(app, ["adb", "root"], "Requesting root access...")
        Tools.log_window(app, "dmesg Viewer", ["adb", "shell", "dmesg"])

    @staticmethod
    def log_window(app, title, *commands, continuous=False):
        window = Toplevel(app.root)
        window.title(title)

        text_area = tk.Text(window, height=30, state=tk.NORMAL)
        text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        pause_button = ttk.Button(window, text="Pause", command=lambda: toggle_pause())
        pause_button.pack(pady=10)

        stop_event = threading.Event()
        stop_event.clear()

        log_queue = Queue()

        def toggle_pause():
            if stop_event.is_set():
                stop_event.clear()
                pause_button.config(text="Pause")
                threading.Thread(target=run).start()
            else:
                stop_event.set()
                pause_button.config(text="Resume")

        def read_process_output(process):
            buffer = []
            while not stop_event.is_set():
                try:
                    line = process.stdout.readline().decode('utf-8', errors='replace')
                    if not line:
                        break
                    buffer.append(line)
                    if len(buffer) >= 20:  # update the queue every 20 lines
                        log_queue.put(''.join(buffer))
                        buffer.clear()
                except Exception as e:
                    log_queue.put(f"Error reading line: {e}\n")
            if buffer:  # put the remaining lines in the queue
                log_queue.put(''.join(buffer))
        
        def update_text_area():
            while not stop_event.is_set():
                try:
                    text = log_queue.get_nowait()
                    text_area.insert(tk.END, text)
                    text_area.see(tk.END)
                except Empty:
                    break
            if not stop_event.is_set():
                window.after(100, update_text_area)

        def run():
            for command in commands:
                try:
                    log(app, f"Executing: {' '.join(command)}")
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
                    
                    if continuous:
                        threading.Thread(target=read_process_output, args=(process,), daemon=True).start()
                        threading.Thread(target=update_text_area, daemon=True).start()
                    else:
                        stdout, stderr = process.communicate()
                        stdout = stdout.decode('utf-8', errors='replace')
                        stderr = stderr.decode('utf-8', errors='replace')
                        if process.returncode == 0:
                            text_area.insert(tk.END, stdout)
                        else:
                            if 'adb' in command and 'root' in command:
                                messagebox.showerror("Error", "Root access required to view dmesg. Please ensure the device is rooted and adb root is enabled.")
                                return
                            text_area.insert(tk.END, stderr)
                except subprocess.CalledProcessError as e:
                    text_area.insert(tk.END, f"Error: Command failed: {e}")
                except FileNotFoundError:
                    text_area.insert(tk.END, "Error: adb not found. Please ensure that Android platform-tools are installed and added to the PATH.")
                except Exception as e:
                    text_area.insert(tk.END, f"Error: An error occurred: {e}")

        threading.Thread(target=run).start()