import board
import digitalio
import storage
import usb_cdc

bypass_button = digitalio.DigitalInOut(board.GP5)
bypass_button.direction = digitalio.Direction.INPUT
bypass_button.pull = digitalio.Pull.UP

if bypass_button.value:
    storage.disable_usb_drive()
    # usb_cdc.disable()          # Uncomment this to also hide the Serial COM port

bypass_button.deinit()