
# src/platforms/input/joystick_input.py
from .base_input import BaseInput

class JoystickInput(BaseInput):
    def __init__(self, joystick):
        self.joystick = joystick
        
    def get_input(self):
        return {
            'up': not self.joystick.button_U.value,
            'down': not self.joystick.button_D.value,
            'left': not self.joystick.button_L.value,
            'right': not self.joystick.button_R.value,
            'A': not self.joystick.button_A.value,
            'B': not self.joystick.button_B.value
        }
        
    def wait_for_any_key(self):
        while True:
            if any(value for value in self.get_input().values()):
                return True