# src/platforms/input/joystick_input.py
from src.platforms.input.base_input import BaseInput

class JoystickInput(BaseInput):
    def __init__(self, joystick):
        self.joystick = joystick
        
    def get_input(self):
        """
        조이스틱의 현재 입력 상태를 반환합니다.
        
        Returns:
            dict: 각 버튼의 상태를 담은 딕셔너리
        """
        try:
            return {
                'up': not self.joystick.button_U.value,
                'down': not self.joystick.button_D.value,
                'left': not self.joystick.button_L.value,
                'right': not self.joystick.button_R.value,
                'A': not self.joystick.button_A.value,
                'B': not self.joystick.button_B.value
            }
        except AttributeError as e:
            print(f"조이스틱 입력 오류: {e}")
            return None
        
    def wait_for_any_key(self):
        """
        아무 버튼이나 눌릴 때까지 대기합니다.
        
        Returns:
            bool: 입력이 감지되면 True
        """
        try:
            while True:
                if any(value for value in self.get_input().values()):
                    return True
        except Exception as e:
            print(f"조이스틱 대기 중 오류: {e}")
            return False