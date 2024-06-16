import tkinter as tk
from tool_box.device_actions import DeviceActions
from tool_box.file_operations import FileOperations
from tool_box.tools import Tools
from tool_box.utils import check_device_periodically

class AndroidUtilityBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Android Utility Box")
        self.root.geometry("600x500")

        # Create the menu bar
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)

        # Create a Device menu
        self.device_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Device", menu=self.device_menu)
        DeviceActions.add_device_menu(self.device_menu, self)

        # Create an Actions menu
        self.actions_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Actions", menu=self.actions_menu)
        FileOperations.add_file_operations_menu(self.actions_menu, self)

        # Create a Tools menu
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=self.tools_menu)
        Tools.add_tools_menu(self.tools_menu, self)

        self.device_label = tk.Label(root, text="No device connected")
        self.device_label.pack(pady=10)

        self.state_label = tk.Label(root, text="Device State: N/A")
        self.state_label.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh", command=lambda: check_device_periodically(self))
        self.refresh_button.pack(pady=10)

        self.log_viewer = tk.Text(root, height=10, state=tk.DISABLED)
        self.log_viewer.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        check_device_periodically(self)

if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidUtilityBox(root)
    root.mainloop()
