import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from kmk.modules.mouse_keys import MouseKeys

# === PIN MAPPINGS ===
BUTTON_0 = board.GP27
BUTTON_1 = board.GP9
BUTTON_2 = board.GP13
BUTTON_3 = board.GP17
BUTTON_4 = board.GP21

keyboard = KMKKeyboard()

# === Modules & Extensions ===
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())
keyboard.modules.append(MouseKeys())

# === Hardware Setup ===
keyboard.matrix = KeysScanner(
    pins=[BUTTON_0, BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4],
    value_when_pressed=False,
    pull=True
)

# Encoder setup: GP2(A), GP3(B), GP5(Switch)
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP2, board.GP3, board.GP5, False),)
keyboard.modules.append(encoder_handler)

encoder_handler.map = [
    ((KC.MW_UP, KC.MW_DN, KC.MB_LMB),),  # Layer 0: Scroll Up, Scroll Down, Left Click
    ((KC.VOLD, KC.VOLU, KC.MUTE),),      # Layer 1: Vol Down, Vol Up, Mute
    ((KC.MW_UP, KC.MW_DN, KC.MB_LMB),),  # Layer 2: Defaults to Scroll
    ((KC.MW_UP, KC.MW_DN, KC.MB_LMB),),  # Layer 3: Defaults to Scroll
    ((KC.TRNS, KC.TRNS, KC.TRNS),)       # Layer 4: Transparent (Inactive)
]

# === Keymap ===
keyboard.keymap = [
    # ---------------------------------------------------------
    # LAYER 0
    [
        KC.MO(4),                  # Btn 0: HOLD for Switcher Layer
        KC.LGUI(KC.LSFT(KC.S)),    # Btn 1: Snipping Tool
        KC.LCTRL(KC.C),            # Btn 2: Copy
        KC.LCTRL(KC.V),            # Btn 3: Paste
        KC.LCTRL(KC.LSFT(KC.ESC))  # Btn 4: Task Manager
    ],

    # ---------------------------------------------------------
    # LAYER 1
    [
        KC.MO(4),                  # Btn 0: HOLD for Switcher Layer
        KC.MPLY,                   # Btn 1: Play/Pause
        KC.VOLD,                   # Btn 2: Volume Down 
        KC.VOLU,                   # Btn 3: Volume Up 
        KC.MUTE                    # Btn 4: System Mute
    ],

    # ---------------------------------------------------------
    # LAYER 2
    [
        KC.MO(4),                  # Btn 0: HOLD for Switcher Layer
        KC.LCTRL(KC.LSFT(KC.T)),   # Btn 1: Reopen Closed Tab
        KC.LCTRL(KC.LSFT(KC.TAB)), # Btn 2: Tab Left
        KC.LCTRL(KC.TAB),          # Btn 3: Tab Right
        KC.LCTRL(KC.W)             # Btn 4: Close Tab
    ],

    # ---------------------------------------------------------
    # LAYER 3
    [
        KC.MO(4),                  # Btn 0: HOLD for Switcher Layer
        KC.F13,                    # Btn 1: F13
        KC.F14,                    # Btn 2: F14
        KC.F15,                    # Btn 3: F15
        KC.F16                     # Btn 4: F16
    ],
    
    # ---------------------------------------------------------
    # LAYER 4; Must always be the highest layer
    [
        KC.TRNS,                   # Btn 0: (Holding)
        KC.DF(0),                  # Btn 1: Sets Default to Layer 0
        KC.DF(1),                  # Btn 2: Sets Default to Layer 1
        KC.DF(2),                  # Btn 3: Sets Default to Layer 2
        KC.DF(3)                   # Btn 4: Sets Default to Layer 3
    ]
]

if __name__ == '__main__':
    keyboard.go()