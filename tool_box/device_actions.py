import tkinter as tk
from tool_box.utils import execute_command

class DeviceActions:
    @staticmethod
    def add_device_menu(menu, app):
        # add sub-menu for adb
        adb_sub_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="ADB", menu=adb_sub_menu)
        adb_sub_menu.add_command(label="Reboot to Fastboot", command=lambda: DeviceActions.reboot_to_fastboot(app))
        adb_sub_menu.add_command(label="Reboot to Recovery", command=lambda: DeviceActions.reboot_to_recovery(app))
        adb_sub_menu.add_command(label="Reboot to Bootloader", command=lambda: DeviceActions.reboot_to_bootloader(app))
        adb_sub_menu.add_command(label="Reboot", command=lambda: DeviceActions.reboot(app))
        # add sub-menu for fastboot
        fastboot_sub_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Fastboot", menu=fastboot_sub_menu)
        fastboot_sub_menu.add_command(label="Reboot to Recovery", command=lambda: DeviceActions.fastboot_reboot_to_recovery(app))
        fastboot_sub_menu.add_command(label="Lock Bootloader", command=lambda: DeviceActions.fastboot_lock_bootloader(app))
        fastboot_sub_menu.add_command(label="Unlock Bootloader", command=lambda: DeviceActions.fastboot_unlock_bootloader(app))
        fastboot_sub_menu.add_command(label="Exit Fastboot", command=lambda: DeviceActions.fastboot_exit(app))
        fastboot_sub_menu.add_command(label="Reboot", command=lambda: DeviceActions.fastboot_exit(app))

    @staticmethod
    def reboot_to_fastboot(app):
        execute_command(app, ["adb", "reboot", "bootloader"], "Rebooting to Fastboot...")
    
    @staticmethod
    def reboot_to_recovery(app):
        execute_command(app, ["adb", "reboot", "recovery"], "Rebooting to Recovery...")
    
    @staticmethod
    def reboot_to_bootloader(app):
        execute_command(app, ["adb", "reboot", "bootloader"], "Rebooting to Bootloader...")
    
    @staticmethod
    def reboot(app):
        execute_command(app, ["adb", "reboot"], "Rebooting...")
    
    @staticmethod
    def fastboot_reboot_to_recovery(app):
        execute_command(app, ["fastboot", "reboot", "recovery"], "Rebooting to Recovery...")
    
    @staticmethod
    def fastboot_lock_bootloader(app):
        execute_command(app, ["fastboot", "flashing", "lock"], "Locking bootloader...")
    
    @staticmethod
    def fastboot_unlock_bootloader(app):
        execute_command(app, ["fastboot", "flashing", "unlock"], "Unlocking bootloader...")
    
    @staticmethod
    def fastboot_exit(app):
        execute_command(app, ["fastboot", "reboot"], "Exiting Fastboot...")
