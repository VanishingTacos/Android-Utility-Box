from tkinter import filedialog, simpledialog
from utils import execute_command

class FileOperations:
    @staticmethod
    def add_file_operations_menu(menu, app):
        menu.add_command(label="Install APK", command=lambda: FileOperations.install_apk(app))
        menu.add_command(label="Install ZIP", command=lambda: FileOperations.install_zip(app))
        menu.add_command(label="Flash Image", command=lambda: FileOperations.flash_image(app))

    @staticmethod
    def install_apk(app):
        file_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if file_path:
            execute_command(app, ["adb", "install", file_path], f"Installing APK from {file_path}...")

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
