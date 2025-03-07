# SteelSeries Rival 700 Haptic Control

This repository contains a Python script (steelseries_vibration.py) to control the haptic feedback (vibration) of the SteelSeries Rival 700 mouse via USB. It allows you to trigger various vibration patterns with a customizable delay, replicating functionality originally implemented in a C++ project. It also contains a Matlab code, which can be used with the Python code.

## Features
- Supports all tactile patterns from the original SteelSeriesControl project (e.g., "Buzz", "Strong", "Pulse").
- Accepts numeric vibration values (0–127) for custom effects.
- Configurable delay before triggering the vibration (in milliseconds).
- Pure Python implementation using pyusb for USB communication.

## Prerequisites
- Operating System: Tested on Linux (Fedora), should work on other platforms with libusb support.
- Hardware: SteelSeries Rival 700 mouse (VID: 0x1038, PID: 0x1700). [change wherever in the codes your model changes]
- Python: Version 3.x (e.g., Python 3.11 on Fedora).
- Dependencies:
  - pyusb: Python USB library.
  - libusb: Backend for pyusb.

## Installation

1. Install Python Dependencies:

  Install pyusb:
  ```
  pip install pyusb
  ```
  
  Install libusb (required by pyusb):
  ```
  sudo dnf install libusb libusb-devel #as per your distro
  ```

2. Set Up USB Permissions
  To access the mouse without root privileges, add a udev rule:
  ```
  sudo nano /etc/udev/rules.d/99-steelseries.rules
  ```
  Add the following line:
  ```
  SUBSYSTEM=="usb", ATTR{idVendor}=="1038", ATTR{idProduct}=="1700", MODE="0666"
  ```
  Save and exit, then apply:
  ```
  sudo udevadm control --reload-rules
  sudo udevadm trigger
  ```
  Unplug and replug the mouse.

4. Clone the Repository
  ```
  git clone https://github.com/<your-username>/steelseries-rival700-haptic.git
  cd steelseries-rival700-haptic
  ```

## Usage
- Python
    Command-Line
    Run the script directly:
    ```
    python3 steelseries_vibration.py <vibration_type> <delay_ms>
    ```
    - <vibration_type>: A named vibration (e.g., Buzz, Strong) or a number (0–127).
    - <delay_ms>: Delay in milliseconds before the vibration (e.g., 250).
  
    Examples:
    ```
    python3 steelseries_vibration.py Buzz 250    # Buzz with 250ms delay
    python3 steelseries_vibration.py Strong 500  # Strong with 500ms delay
    ```
  
    As a Python Module
    Import and use the trigger_vibration function:
    ```
    from steelseries_vibration import trigger_vibration
  
    success = trigger_vibration("Buzz", 250)
    if success:
        print("Vibration triggered!")
    else:
        print("Failed to trigger vibration.")
    ```
- MATLAB
    This script can be called from MATLAB using the Python integration:
    See the accompanying MATLAB function triggerVibration.m for a complete example
    Run the script directly from MATLAB (navigate or add the folder to MATLAB path):
    ```
    triggerVibration('Buzz',250)    # Buzz with 250ms delay
    triggerVibration('Strong',500)  # Strong with 500ms delay

## Vibration Types
  The script supports the following named vibration patterns (matching the original C++ implementation):
  - Strong (0b000001)
  - Soft (0b000010)
  - Sharp (0b000100)
  - Ping (0b001000)
  - Bump (0b000111)
  - Double (0b001010)
  - QuickDouble (0b011011)
  - QuickDoubleSoft (0b100000)
  - QuickTriple (0b001100)
  - Buzz (0b101111)
  - LongBuzz (0b001111)
  - Ring (0b010000)
  - LongButLight (0b111111)
  - LightBuzz (0b110011)
  - Tick (0b011000)
  - Pulse (0b110101)
  - StrongPulse (0b110100)

  You can also use any integer from 0 to 127 for custom effects. (Each number has a different pattern)

## Troubleshooting
- "Could not find SteelSeries Rival 700": Ensure the mouse is connected (running lsusb should show ID 1038:1700). Adjust idVendor/idProduct in the script if your device differs.
- "Could not claim interface": Verify the udev rule is active and you have permissions.
- Python Errors: Ensure pyusb and libusb are installed correctly.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Based on the original C++ project SteelSeriesControl (https://github.com/HughPH/SteelSeriesControl) by HughPH.
- Built with pyusb for USB communication.

Happy buzzing!
