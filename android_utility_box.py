import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import threading


class AndroidToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Android Unility Box")
        self.root.geometry("400x400")

        # Create the menu bar
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)

        # Create a Device menu
        self.device_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Device", menu=self.device_menu)
        self.device_menu.add_command(label="Reboot to Fastboot", command=self.reboot_to_fastboot)
        self.device_menu.add_command(label="Reboot to Recovery", command=self.reboot_to_recovery)
        self.device_menu.add_command(label="Reboot to Bootloader", command=self.reboot_to_bootloader)
        self.device_menu.add_command(label="Reboot to Normal", command=self.reboot_to_normal)
        self.device_menu.add_command(label="Exit Fastboot", command=self.exit_fastboot)

        # Create an Actions menu
        self.actions_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Actions", menu=self.actions_menu)
        self.actions_menu.add_command(label="Install APK", command=self.install_apk)
        self.actions_menu.add_command(label="Install ZIP", command=self.install_zip)
        self.actions_menu.add_command(label="Flash Image", command=self.flash_image)

        self.device_label = tk.Label(root, text="No device connected")
        self.device_label.pack(pady=10)

        self.state_label = tk.Label(root, text="Device State: N/A")
        self.state_label.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.check_device)
        self.refresh_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)

        self.check_device_periodically()

    def check_device_periodically(self):
        self.check_device()
        self.root.after(5000, self.check_device_periodically)  # Check every 5 seconds

    def check_device(self):
        def run():
            device, state = self.get_connected_device()
            self.update_labels(device, state)
            self.update_menu(state)

        threading.Thread(target=run).start()

    def get_connected_device(self):
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
            messagebox.showerror("Error", "adb or fastboot not found. Please ensure that Android platform-tools are installed and added to the PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check connected devices: {e}")
        return device, state

    def update_labels(self, device, state):
        self.device_label.config(text=f"Device: {device}" if device else "No device connected")
        self.state_label.config(text=f"Device State: {state}")

    def update_menu(self, state):
        if state == "adb":
            self.actions_menu.entryconfig("Install APK", state=tk.NORMAL)
            self.actions_menu.entryconfig("Install ZIP", state=tk.DISABLED)
            self.actions_menu.entryconfig("Flash Image", state=tk.DISABLED)
        elif state == "sideload":
            self.actions_menu.entryconfig("Install APK", state=tk.DISABLED)
            self.actions_menu.entryconfig("Install ZIP", state=tk.NORMAL)
            self.actions_menu.entryconfig("Flash Image", state=tk.DISABLED)
        elif state == "fastboot":
            self.actions_menu.entryconfig("Install APK", state=tk.DISABLED)
            self.actions_menu.entryconfig("Install ZIP", state=tk.DISABLED)
            self.actions_menu.entryconfig("Flash Image", state=tk.NORMAL)
        else:
            self.actions_menu.entryconfig("Install APK", state=tk.DISABLED)
            self.actions_menu.entryconfig("Install ZIP", state=tk.DISABLED)
            self.actions_menu.entryconfig("Flash Image", state=tk.DISABLED)

    def reboot_to_fastboot(self):
        self.execute_command(["adb", "reboot", "bootloader"], "Rebooting to fastboot...")

    def reboot_to_recovery(self):
        self.execute_command(["adb", "reboot", "recovery"], "Rebooting to recovery...")

    def reboot_to_bootloader(self):
        self.execute_command(["adb", "reboot", "bootloader"], "Rebooting to bootloader...")

    def reboot_to_normal(self):
        self.execute_command(["adb", "reboot"], "Rebooting to normal...")

    def exit_fastboot(self):
        self.execute_command(["fastboot", "reboot"], "Exiting fastboot...")

    def install_apk(self):
        file_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if file_path:
            self.execute_command(["adb", "install", file_path], f"Installing APK from {file_path}...")

    def install_zip(self):
        file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if file_path:
            self.execute_command(["adb", "sideload", file_path], f"Sideloading ZIP from {file_path}...")

    def flash_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.img")])
        if file_path:
            partition = simpledialog.askstring("Partition", "Enter the partition to flash (e.g., boot, recovery):")
            if partition:
                self.execute_command(["fastboot", "flash", partition, file_path], f"Flashing {file_path} to {partition}...")

    def execute_command(self, command, message):
        def run():
            try:
                subprocess.run(command, check=True)
                messagebox.showinfo("Success", message)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Command failed: {e}")
            except FileNotFoundError:
                messagebox.showerror("Error", "adb or fastboot not found. Please ensure that Android platform-tools are installed and added to the PATH.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        threading.Thread(target=run).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidToolApp(root)
    root.mainloop()
