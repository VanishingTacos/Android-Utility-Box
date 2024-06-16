import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, messagebox, Canvas, Frame, Scrollbar, Checkbutton, IntVar, Button
from tool_box.utils import execute_command, log
import subprocess

class FileOperations:
    @staticmethod
    def add_file_operations_menu(menu, app):
        menu.add_command(label="Install APK", command=lambda: FileOperations.install_apk(app))
        menu.add_command(label="Uninstall APK", command=lambda: FileOperations.uninstall_apk(app))
        menu.add_command(label="Install ZIP", command=lambda: FileOperations.install_zip(app))
        menu.add_command(label="Flash Image", command=lambda: FileOperations.flash_image(app))

    @staticmethod
    def install_apk(app):
        file_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if file_path:
            execute_command(app, ["adb", "install", file_path], f"Installing APK from {file_path}...")
    
    @staticmethod
    def uninstall_apk(app):
        packages = FileOperations.get_installed_packages(app)
        if not packages:
            messagebox.showinfo("No Apps Found", "No user-installed apps found.")
            return
        
        uninstall_window = Toplevel(app.root)
        uninstall_window.title("Uninstall APK")
        uninstall_window.geometry("800x600")

        canvas = Canvas(uninstall_window)
        frame = Frame(canvas)
        scrollbar = Scrollbar(uninstall_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        checkboxes = []
        for pkg in packages:
            var = IntVar()
            chk = Checkbutton(frame, text=pkg, variable=var)
            chk.var = var
            chk.pack(anchor='w')
            checkboxes.append((pkg, var))

        def on_uninstall():
            selected_packages = [pkg for pkg, var in checkboxes if var.get() == 1]
            if selected_packages:
                confirm = messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall the selected packages?")
                if confirm:
                    for pkg_name in selected_packages:
                        execute_command(app, ["adb", "uninstall", pkg_name], f"Uninstalling {pkg_name}...")
            else:
                messagebox.showinfo("No Selection", "No packages selected for uninstallation.")

        # Add the uninstall button outside the canvas
        button_frame = Frame(uninstall_window)
        button_frame.pack(fill='x')
        uninstall_button = Button(button_frame, text="Uninstall", command=on_uninstall)
        uninstall_button.pack(pady=10)

        # Bind the mousewheel event to the canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    @staticmethod
    def get_installed_packages(app):
        try:
            result = subprocess.run(["adb", "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True)
            if result.returncode == 0:
                packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]
                return packages
            else:
                log(app, f"Error: {result.stderr}")
                return []
        except subprocess.CalledProcessError as e:
            log(app, f"Error: Command failed: {e}")
            return []
        except FileNotFoundError:
            log(app, "Error: adb not found. Please ensure that Android platform-tools are installed and added to the PATH.")
            return []
        except Exception as e:
            log(app, f"Error: An error occurred: {e}")
            return []


    @staticmethod
    def install_zip(app):
        file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if file_path:
            execute_command(app, ["adb", "sideload", file_path], f"Sideloading ZIP from {file_path}...")

    @staticmethod
    def flash_image(app):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.img")])
        if file_path:
            partition = simpledialog.askstring("Partition", "Enter the partition to flash (e.g., boot, recovery):")
            if partition:
                execute_command(app, ["fastboot", "flash", partition, file_path], f"Flashing {file_path} to {partition}...")
