# Android Utility Box

Android Utility Box is a versatile tool for managing Android devices. It allows you to perform various actions like installing APKs, sideloading ZIPs, and flashing images. It also supports rebooting devices into different modes (fastboot, recovery, bootloader) and exiting fastboot mode.

## Features

- **Device Detection**: Automatically detects connected Android devices and their states.
- **Reboot Options**: Reboot devices into fastboot, recovery, or bootloader modes.
- **File Operations**:
  - Install APK files when in normal mode.
  - Sideload ZIP files when in sideload mode.
  - Flash image files when in fastboot mode.
- **User-Friendly Interface**: Simple and intuitive GUI built with Tkinter.

## Installation

1. **Download Android Utility Box**
   - Download the latest release of Android Utility Box from the [releases page](https://github.com/yourusername/android-utility-box/releases) on GitHub.
   - Extract the contents of the downloaded ZIP file to a directory of your choice.

2. **Download and Install Android Platform Tools**
   - Download the platform tools from the [official Android developer website](https://developer.android.com/studio/releases/platform-tools).
   - Extract the contents to a directory and add the directory to your system's PATH.

## Usage

1. **Connect Your Device**
   - Connect your Android device to your computer using a USB cable. Ensure USB debugging is enabled on your device.

2. **Launch Android Utility Box**
   - Navigate to the directory where you extracted Ninja Droid and run the executable:
     ```sh
     android_utility_box.exe
     ```

3. **Perform Actions**
   - The application will detect your device and display its state. Depending on the state, you can perform various actions:
     - **Normal Mode**: Install APK files.
     - **Sideload Mode**: Sideload ZIP files.
     - **Fastboot Mode**: Flash image files.

4. **Reboot Options**
   - Use the "Device" menu to reboot your device into different modes:
     - Reboot to Fastboot
     - Reboot to Recovery
     - Reboot to Bootloader
     - Reboot to Normal
     - Exit Fastboot

## Troubleshooting

- **adb or fastboot not found**: Ensure that Android platform-tools are installed and the directory containing `adb` and `fastboot` is added to your system's PATH.
- **Device not detected**: Make sure USB debugging is enabled on your device and it is properly connected to your computer.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
