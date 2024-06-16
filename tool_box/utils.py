import threading
import subprocess
import tkinter as tk

def log(app, message):
    app.log_viewer.config(state=tk.NORMAL)
    app.log_viewer.insert(tk.END, message + '\n')
    app.log_viewer.config(state=tk.DISABLED)
    app.log_viewer.see(tk.END)

def check_device_periodically(app):
    check_device(app)
    app.root.after(5000, lambda: check_device_periodically(app))

def check_device(app):
    def run():
        device, state = get_connected_device(app)
        update_labels(app, device, state)
        update_file_menu(app, state)
        update_device_menu(app, state)

    threading.Thread(target=run).start()

def get_connected_device(app):
    device = None
    state = "N/A"
    try:
        # Check for adb devices
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            for line in lines[1:]:
                if "device" in line:
                    device = line.split()[0]
                    state = "adb"
                    break
                elif "sideload" in line:
                    device = line.split()[0]
                    state = "sideload"
                    break
                elif "recovery" in line:
                    device = line.split()[0]
                    state = "recovery"
                    break
        if not device:
            # If no adb device found, check for fastboot devices
            result = subprocess.run(["fastboot", "devices"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            if lines and lines[0]:
                device = lines[0].split()[0]
                state = "fastboot"
    except FileNotFoundError:
        log(app, "Error: adb or fastboot not found. Please ensure that Android platform-tools are installed and added to the PATH.")
    except Exception as e:
        log(app, f"Error: Failed to check connected devices: {e}")
    return device, state

def update_labels(app, device, state):
    app.device_label.config(text=f"Device: {device}" if device else "No device connected")
    app.state_label.config(text=f"Device State: {state}")

def update_file_menu(app, state):
    if state == "adb":
        app.actions_menu.entryconfig("Install APK", state=tk.NORMAL)
        app.actions_menu.entryconfig("Install ZIP", state=tk.DISABLED)
        app.actions_menu.entryconfig("Flash Image", state=tk.DISABLED)
    elif state == "sideload":
        app.actions_menu.entryconfig("Install APK", state=tk.DISABLED)
        app.actions_menu.entryconfig("Install ZIP", state=tk.NORMAL)
        app.actions_menu.entryconfig("Flash Image", state=tk.DISABLED)
    elif state == "fastboot":
        app.actions_menu.entryconfig("Install APK", state=tk.DISABLED)
        app.actions_menu.entryconfig("Install ZIP", state=tk.DISABLED)
        app.actions_menu.entryconfig("Flash Image", state=tk.NORMAL)
    else:
        app.actions_menu.entryconfig("Install APK", state=tk.DISABLED)
        app.actions_menu.entryconfig("Install ZIP", state=tk.DISABLED)
        app.actions_menu.entryconfig("Flash Image", state=tk.DISABLED)

def update_device_menu(app, state):
    if state == "adb":
        app.device_menu.entryconfig("Fastboot", state=tk.DISABLED)
        app.device_menu.entryconfig("ADB", state=tk.NORMAL)
    elif state == "fastboot":
        app.device_menu.entryconfig("Fastboot", state=tk.NORMAL)
        app.device_menu.entryconfig("ADB", state=tk.DISABLED)
    
def execute_command(app, command, message):
    def run():
        try:
            log(app, f"Executing: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                log(app, f"Success: {message}")
            else:
                log(app, f"Error: {result.stderr}")
        except subprocess.CalledProcessError as e:
            log(app, f"Error: Command failed: {e}")
        except FileNotFoundError:
            log(app, "Error: adb or fastboot not found. Please ensure that Android platform-tools are installed and added to the PATH.")
        except Exception as e:
            log(app, f"Error: An error occurred: {e}")

    threading.Thread(target=run).start()

def get_device_state(app):
    _, state = get_connected_device(app)
    return state

def update_progress(progress, progress_value):
    progress['value'] = progress_value

def update_hash_result(hash_label, hash_result, hash_name):
    hash_label.config(text=f"{hash_name}: {hash_result}")
