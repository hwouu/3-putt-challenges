from time import time
from src.platforms.input.base_input import BaseInput

class JoystickInput(BaseInput):
    def __init__(self, joystick):
        self.joystick = joystick
        self.last_press_time = {}  # 디바운싱을 위한 시간 저장
        self.button_states = {}    # 버튼 상태 저장
        self.DEBOUNCE_TIME = 0.05  # 50ms
        self.debug_mode = True     # 디버그 모드 활성화

    def _is_debounced(self, button_name):
        """
        버튼 디바운싱 처리
        Returns:
            bool: 디바운스 시간이 지났으면 True, 아니면 False
        """
        current_time = time()
        if button_name not in self.last_press_time:
            self.last_press_time[button_name] = current_time
            return True
        
        if current_time - self.last_press_time[button_name] >= self.DEBOUNCE_TIME:
            self.last_press_time[button_name] = current_time
            return True
        return False

    def get_input(self):
        """
        조이스틱의 현재 입력 상태를 반환합니다.
        풀업 저항이 적용되어 있으므로, 버튼이 눌리면 False가 반환됩니다.
        이를 반전시켜서 눌렸을 때 True가 되도록 합니다.
        
        Returns:
            dict: 각 버튼의 상태를 담은 딕셔너리
            None: 에러 발생 시
        """
        try:
            input_state = {
                'up': False, 'down': False,
                'left': False, 'right': False,
                'A': False, 'B': False
            }

            # 모든 버튼의 현재 상태 가져오기
            button_values = self.joystick.get_button_states()
            
            # 각 버튼에 대해 처리
            for button_name, value in button_values.items():
                # 버튼이 눌렸을 때 (풀업 저항으로 인해 False)
                if not value and self._is_debounced(button_name):
                    input_state[button_name] = True
                    if self.debug_mode:
                        print(f"Button pressed: {button_name}")

            return input_state

        except Exception as e:
            if self.debug_mode:
                print(f"조이스틱 입력 처리 중 오류: {e}")
            return None
        
    def wait_for_any_key(self):
        """
        아무 버튼이나 눌릴 때까지 대기합니다.
        
        Returns:
            bool: 입력이 감지되면 True, 오류 발생 시 False
        """
        try:
            while True:
                current_input = self.get_input()
                if current_input and any(current_input.values()):
                    return True
                
        except Exception as e:
            if self.debug_mode:
                print(f"키 대기 중 오류: {e}")
            return False