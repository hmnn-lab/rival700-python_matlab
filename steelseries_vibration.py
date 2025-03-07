# steelseries_vibration.py
import usb.core
import usb.util
import time

def trigger_vibration(vibration_type, delay_ms):
    # Vibration types mapping (from C++ vibrations map)
    vibrations = {
        "Strong": 0b000001,
        "Soft": 0b000010,
        "Sharp": 0b000100,
        "Ping": 0b001000,
        "Bump": 0b000111,
        "Double": 0b001010,
        "QuickDouble": 0b011011,
        "QuickDoubleSoft": 0b100000,
        "QuickTriple": 0b001100,
        "Buzz": 0b101111,
        "LongBuzz": 0b001111,
        "Ring": 0b010000,
        "LongButLight": 0b111111,
        "LightBuzz": 0b110011,
        "Tick": 0b011000,
        "Pulse": 0b110101,
        "StrongPulse": 0b110100
    }

    # Convert vibration_type to byte, use integer if not in map
    try:
        if vibration_type in vibrations:
            vibration_value = vibrations[vibration_type]
        else:
            vibration_value = int(vibration_type) & 0x7F  # 7-bit integer (0-127)
    except ValueError:
        print(f"Invalid vibration type: {vibration_type}")
        return False

    # Convert delay from milliseconds to seconds
    delay_seconds = delay_ms / 1000.0

    # Find the SteelSeries Rival 700 (VID: 0x1038, PID: 0x1700)
    dev = usb.core.find(idVendor=0x1038, idProduct=0x1700)
    if dev is None:
        print("Could not find SteelSeries Rival 700")
        return False

    # Detach kernel driver if active
    if dev.is_kernel_driver_active(0):
        try:
            dev.detach_kernel_driver(0)
        except usb.core.USBError as e:
            print(f"Could not detach kernel driver: {e}")
            return False

    # Claim the interface
    try:
        usb.util.claim_interface(dev, 0)
    except usb.core.USBError as e:
        print(f"Could not claim interface: {e}")
        return False

    # Data packet for haptic feedback (from C++: {0x59, 0x01, 0x00, buzzType})
    data = [0x59, 0x01, 0x00, vibration_value]

    # Delay before sending the vibration
    time.sleep(delay_seconds)

    # Send control transfer (matches C++ libusb_control_transfer)
    try:
        dev.ctrl_transfer(
            bmRequestType=0x21,  # LIBUSB_REQUEST_TYPE_CLASS | LIBUSB_RECIPIENT_INTERFACE | LIBUSB_ENDPOINT_OUT
            bRequest=9,          # HID Set_Report
            wValue=0x0200,       # From C++ wValue
            wIndex=0,            # Interface 0
            data_or_wLength=data,
            timeout=60
        )
    except usb.core.USBError as e:
        print(f"Control transfer failed: {e}")
        return False

    # Release interface and reattach kernel driver
    usb.util.release_interface(dev, 0)
    if dev.is_kernel_driver_active(0) == False:
        try:
            dev.attach_kernel_driver(0)
        except usb.core.USBError as e:
            print(f"Could not reattach kernel driver: {e}")

    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python steelseries_vibration.py <vibration_type> <delay_ms>")
    else:
        success = trigger_vibration(sys.argv[1], int(sys.argv[2]))
        if success:
            print(f"Vibration type '{sys.argv[1]}' triggered successfully after {sys.argv[2]}ms")
