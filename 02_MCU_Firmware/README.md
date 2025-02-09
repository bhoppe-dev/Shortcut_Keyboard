# Shortcut Keyboard Firmware

CircuitPython firmware for the Shortcut Keyboard project, implementing an 8-key programmable macro keyboard with volume control functionality.

## Overview

This firmware powers the Shortcut Keyboard using CircuitPython and the RP2040 microcontroller. It provides a implementation of programmable shortcut keys and volume control through a rotary encoder.

## Features

- 8 programmable macro keys using SHIFT+ALT+CTRL + letter combinations
- Volume control via rotary encoder with mute functionality
- Built-in debouncing for reliable key detection
- Error indication via onboard LED
- Comprehensive error logging
- USB HID compliance for wide compatibility

## Technical Specifications

- **MCU**: RP2040
- **Version**: V1.1.1-beta
- **Language**: CircuitPython
- **Encoder Step**: 2 steps per click

## Pin Configuration

### Macro Keys
- GP0-GP7: Programmable shortcut buttons

### Rotary Encoder
- GP19: Encoder Pin A
- GP18: Encoder Pin B
- GP20: Encoder Push Button (Mute)

### Status Indication
- GP25: Onboard LED for error indication

## Default Key Mappings

Each button is configured to send a combination of SHIFT+ALT+CTRL + letter:

| Pin  | Key Combination              |
|------|----------------------------|
| GP0  | SHIFT + ALT + CTRL + A    |
| GP1  | SHIFT + ALT + CTRL + B    |
| GP2  | SHIFT + ALT + CTRL + C    |
| GP3  | SHIFT + ALT + CTRL + D    |
| GP4  | SHIFT + ALT + CTRL + E    |
| GP5  | SHIFT + ALT + CTRL + F    |
| GP6  | SHIFT + ALT + CTRL + G    |
| GP7  | SHIFT + ALT + CTRL + H    |

## Dependencies

- `board`
- `digitalio`
- `rotaryio`
- `usb_hid`
- `adafruit_hid.keyboard`
- `adafruit_hid.keycode`
- `adafruit_hid.consumer_control`
- `adafruit_hid.consumer_control_code`

## Installation

1. Install CircuitPython on your RP2040 board
2. Copy the firmware file to the CircuitPython drive
3. Ensure all required libraries are in the `lib` folder

## Error Handling

The firmware includes comprehensive error handling with visual feedback:
- Errors are indicated via the onboard LED (GP25)
- Error messages are printed to serial console
- LED duration for errors: 2 seconds

## Functions

### Core Functions
- `setup_error_led()`: Initializes the onboard LED for error indication
- `setup_buttons()`: Configures the 8 programmable buttons with pull-up resistors
- `setup_rotary_encoder()`: Initializes the volume control encoder
- `setup_usb_devices()`: Sets up USB HID interfaces

### Polling Functions
- `poll_buttons()`: Monitors button states and sends key combinations
- `poll_rotary_encoder()`: Handles volume control and mute functionality

### Utility Functions
- `log_error()`: Logs errors with LED indication
- `log_info()`: Logs informational messages

## License

This firmware is part of the Shortcut Keyboard project and is licensed under the BSD 2-Clause License.

## Author

Benjamin Hoppe

---

For more information about the complete Shortcut Keyboard project, please refer to the main project README.
