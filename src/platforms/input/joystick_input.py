from time import time
from src.platforms.input.base_input import BaseInput

class JoystickInput(BaseInput):
    def __init__(self, joystick):
        self.joystick = joystick
        self.last_press_time = {}
        self.button_states = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'A': False,
            'B': False
        }
        self.DEBOUNCE_TIME = 0.01  # 디바운스 시간을 줄임
        self.debug = True

    def _debug_log(self, message):
        if self.debug:
            print(f"[JoystickInput] {message}")

    def get_input(self):
        """
        조이스틱의 현재 입력 상태를 반환합니다.
        버튼이 눌린 상태를 유지합니다.
        """
        try:
            current_time = time()
            raw_states = {
                'up': not self.joystick.button_U.value,
                'down': not self.joystick.button_D.value,
                'left': not self.joystick.button_L.value,
                'right': not self.joystick.button_R.value,
                'A': not self.joystick.button_A.value,
                'B': not self.joystick.button_B.value
            }

            # 각 버튼의 상태 업데이트
            for button, is_pressed in raw_states.items():
                if is_pressed:  # 버튼이 눌려있으면
                    if not self.button_states[button]:  # 이전에 눌려있지 않았다면
                        if button not in self.last_press_time or \
                           current_time - self.last_press_time[button] >= self.DEBOUNCE_TIME:
                            self.button_states[button] = True
                            self.last_press_time[button] = current_time
                            if self.debug:
                                self._debug_log(f"Button {button} pressed")
                else:  # 버튼이 눌려있지 않으면
                    if self.button_states[button]:  # 이전에 눌려있었다면
                        self.button_states[button] = False
                        if self.debug:
                            self._debug_log(f"Button {button} released")

            return self.button_states.copy()

        except Exception as e:
            self._debug_log(f"Error in get_input: {e}")
            return None

    def wait_for_any_key(self):
        """아무 버튼이나 눌릴 때까지 대기합니다."""
        try:
            while True:
                current_input = self.get_input()
                if current_input and any(current_input.values()):
                    return True
                
        except Exception as e:
            self._debug_log(f"Error in wait_for_any_key: {e}")
            return False