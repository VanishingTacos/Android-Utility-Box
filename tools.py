import tkinter as tk
import hashlib
import os
import threading
import subprocess
from tkinter import filedialog, ttk
from utils import log, update_progress, update_hash_result

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
    def calculate_hash(app, file_path, hash_algorithm, hash_name, hash_label, progress):
        log(app, f"Calculating {hash_name} for: {file_path}")
        total_size = os.path.getsize(file_path)
        read_size = 0

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_algorithm.update(chunk)
                read_size += len(chunk)
                progress_value = (read_size / total_size) * 100
                update_progress(progress, progress_value)

        hash_result = hash_algorithm.hexdigest()
        update_hash_result(hash_label, hash_result, hash_name)
        log(app, f"{hash_name} Result: {hash_result}")
    
    @staticmethod
    def view_logcat(app):
        Tools.log_window(app, "Logcat Viewer", "adb logcat")

    @staticmethod
    def view_dmesg(app):
        Tools.log_window(app, "dmesg Viewer", "adb shell dmesg")

    @staticmethod
    def log_window(app, title, command):
        window = tk.Toplevel(app.root)
        window.title(title)

        # add scrollbars
        scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(window, height=30, state=tk.NORMAL, yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)
        text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)


        def run():
            try:
                log(app, f"Executing: {command}")
                result = subprocess.run(command.split(), capture_output=True, text=True)
                if result.returncode == 0:
                    text_area.insert(tk.END, result.stdout)
                else:
                    text_area.insert(tk.END, f"Error: {result.stderr}")
            except subprocess.CalledProcessError as e:
                text_area.insert(tk.END, f"Error: Command failed: {e}")
            except FileNotFoundError:
                text_area.insert(tk.END, "Error: adb not found. Please ensure that Android platform-tools are installed and added to the PATH.")
            except Exception as e:
                text_area.insert(tk.END, f"Error: An error occurred: {e}")

        threading.Thread(target=run).start()
