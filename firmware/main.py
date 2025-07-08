import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.rgb import RGB, AnimationModes 
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306 
from kmk.modules.macros import Press, Release, Tap, Macros

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP26, board.GP27, board.GP28, board.GP29)
keyboard.row_pins = (board.GP0, board.GP1, board.GP2, board.GP4)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

macros = Macros()
keyboard.modules.append(macros)

rgb = RGB(
    pixel_pin=board.GP3,
    num_pixels=16,
    rgb_order=(1, 0, 2), 
    animation_mode=AnimationModes.RAINBOW,
    val_limit=100,      
    val_default=50       
)
keyboard.extensions.append(rgb)

i2c_bus = busio.I2C(board.GP7, board.GP6) 
oled_driver = SSD1306(i2c=i2c_bus, device_address=0x3C) 
oled = Display(
    display=oled_driver,
    entries=[
        TextEntry(text='GBCartPad', x=0, y=0),       
        TextEntry(text='Yahoo!', x=0, y=12) 
    ],
    width=128,
    height=32, 
    brightness=0.8 
)
keyboard.extensions.append(oled)

keyboard.keymap = [
    [
        KC.N1,    KC.N2,    KC.N3,    KC.N4,
        KC.N5,    KC.N6,    KC.N7,    KC.N8,
        KC.N9,    KC.N0,    KC.UP,    
        KC.Macro(
            Press(KC.LCTL, KC.LCMD), 
            Tap(KC.SPC), 
            Release(KC.LCTL, KC.LCMD)
        ),
        KC.Macro(
            Press(KC.LCMD, KC.LSFT),  
            Tap(KC.C),                
            Release(KC.LCMD, KC.LSFT),
            WaitMs(100),
            Press(KC.LCMD),           
            Tap(KC.N2),               
            Release(KC.LCMD)          
        ),   KC.LEFT,   KC.DOWN,   KC.RIGHT 
    ]
]

if __name__ == '__main__':
    keyboard.go()