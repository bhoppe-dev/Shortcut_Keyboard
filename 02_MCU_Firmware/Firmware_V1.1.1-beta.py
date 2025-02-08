"""
Project_Name: Shortcut_Keyboard
Author: Benjamin Hoppe
Date: 24.11.2024
Version: V1.1.1-beta

Description:
============
This Python script is designed to create a shortcut keyboard using a RP2040 microcontroller.
It uses the Adafruit HID library to send media control commands over USB.

Key Features:
- 8 programmable shortcut buttons (GP0-GP7)
- Volume control via rotary encoder
- Error indication via onboard LED
- Debouncing for reliable button presses
"""

import time
import board
import digitalio
import rotaryio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Software version
SOFTWARE_VERSION = "1.1.1-beta"

# Constants
BUTTON_DELAY = 0.2
POLLING_INTERVAL = 0.05  # Time between each main loop iteration
ENCODER_STEP = 2  # How many volume steps per encoder click
ERROR_LED_DURATION = 2
DEBOUNCE_DELAY = 0.3  # Minimum time between button presses in seconds

# Button configuration
# Each button sends SHIFT+ALT+CTRL + Letter combination
BUTTONS = [
    {"pin": board.GP0, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.A]},
    {"pin": board.GP1, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.B]},
    {"pin": board.GP2, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.C]},
    {"pin": board.GP3, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.D]},
    {"pin": board.GP4, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.E]},
    {"pin": board.GP5, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.F]},
    {"pin": board.GP6, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.G]},
    {"pin": board.GP7, "combo": [Keycode.LEFT_SHIFT, Keycode.LEFT_ALT, Keycode.LEFT_CONTROL, Keycode.H]},
]

# Rotary Encoder configuration - Used for volume control
ROTARY_PIN_A = board.GP19
ROTARY_PIN_B = board.GP18
ROTARY_BUTTON_PIN = board.GP20  # Press to mute

# LED configuration - Uses onboard LED for error indication
ERROR_LED_PIN = board.GP25  # Onboard LED of the Raspberry Pi Pico

# Global variables
error_led = None
button_last_press_times = {}  # Stores the last press time for each button
button_states = {}  # Stores the current state of each button

def setup_error_led():
    global error_led
    error_led = digitalio.DigitalInOut(ERROR_LED_PIN)
    error_led.direction = digitalio.Direction.OUTPUT

def log_error(message):
    print(f"ERROR: {message}")
    if error_led:
        error_led.value = True
        time.sleep(ERROR_LED_DURATION)
        error_led.value = False

def log_info(message):
    print(f"INFO: {message}")

def setup_buttons():
    """Initialize all shortcut buttons with pull-up resistors enabled"""
    try:
        buttons = []
        for i, button_config in enumerate(BUTTONS):
            btn = digitalio.DigitalInOut(button_config["pin"])
            btn.direction = digitalio.Direction.INPUT
            btn.pull = digitalio.Pull.UP  # Button pressed = LOW, not pressed = HIGH
            buttons.append({
                "button": btn,
                "combo": button_config["combo"],
                "id": i  # Use an index as unique identifier
            })
            # Initialize the button states and last press times
            button_states[i] = True  # True = not pressed
            button_last_press_times[i] = 0
        return buttons
    except Exception as e:
        log_error(f"Error setting up buttons: {e}")
        return None

def setup_rotary_encoder():
    """Initialize the rotary encoder for volume control"""
    try:
        encoder = rotaryio.IncrementalEncoder(ROTARY_PIN_A, ROTARY_PIN_B)
        button = digitalio.DigitalInOut(ROTARY_BUTTON_PIN)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        return encoder, button
    except Exception as e:
        log_error(f"Error setting up rotary encoder: {e}")
        return None, None

def setup_usb_devices():
    """Initialize USB HID devices for keyboard and media control"""
    try:
        keyboard = Keyboard(usb_hid.devices)
        consumer_control = ConsumerControl(usb_hid.devices)
        return keyboard, consumer_control
    except Exception as e:
        log_error(f"Error setting up USB devices: {e}")
        return None, None

def poll_buttons(buttons, keyboard):
    """Check button states and send key combinations if pressed"""
    try:
        current_time = time.monotonic()

        for button in buttons:
            button_id = button["id"]
            current_state = button["button"].value

            # Check if the button state has changed
            if current_state != button_states[button_id]:
                # If button is pressed (remember, pulled up, so 0 = pressed)
                if current_state == 0:
                    # Check if enough time has passed since last press (debouncing)
                    if current_time - button_last_press_times[button_id] >= DEBOUNCE_DELAY:
                        # Send the keypress combination (e.g., SHIFT+ALT+CTRL+A)
                        keyboard.press(*button["combo"])
                        keyboard.release_all()
                        # Update the last press time
                        button_last_press_times[button_id] = current_time

                # Update the stored state
                button_states[button_id] = current_state

    except Exception as e:
        log_error(f"Error polling buttons: {e}")

def poll_rotary_encoder(encoder, button, consumer_control, last_position, last_button_state):
    """Handle volume control via rotary encoder"""
    try:
        current_position = encoder.position
        if current_position != last_position:
            # Rotate right = volume up, rotate left = volume down
            if current_position > last_position:
                for _ in range(ENCODER_STEP):
                    consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
            else:
                for _ in range(ENCODER_STEP):
                    consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)
            time.sleep(0.01)

        # Check for encoder button press (mute function)
        current_button_state = button.value
        if current_button_state == 0 and last_button_state == 1:
            consumer_control.send(ConsumerControlCode.MUTE)
            time.sleep(BUTTON_DELAY)

        return current_position, current_button_state
    except Exception as e:
        log_error(f"Error polling rotary encoder: {e}")
        return last_position, last_button_state

def main():
    log_info(f'Shortcut-Keyboard by Benjamin Hoppe - Version: {SOFTWARE_VERSION}')
    setup_error_led()
    buttons = setup_buttons()
    encoder, encoder_button = setup_rotary_encoder()
    keyboard, consumer_control = setup_usb_devices()

    if buttons is None or encoder is None or encoder_button is None or keyboard is None or consumer_control is None:
        log_error("Error setting up devices. Terminating program.")
        return

    last_encoder_position = encoder.position
    last_button_state = encoder_button.value

    # Main program loop
    while True:
        poll_buttons(buttons, keyboard)
        last_encoder_position, last_button_state = poll_rotary_encoder(
            encoder, encoder_button, consumer_control, last_encoder_position, last_button_state
        )
        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_info("Keyboard interrupt. Terminating program.")
    except Exception as e:
        log_error(f"Error: {e}")
