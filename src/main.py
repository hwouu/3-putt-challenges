from platforms.display.mac_display import MacDisplay
from platforms.display.rpi_display import RPiDisplay
from platforms.input.keyboard_input import KeyboardInput
from platforms.input.joystick_input import JoystickInput
from screens.start_screen import StartScreen
from screens.game_screen import GameScreen
import os

def get_platform_handlers():
    """현재 플랫폼에 맞는 디스플레이와 입력 핸들러를 반환합니다."""
    if os.environ.get('PLATFORM') == 'rpi':
        from joystick import Joystick
        joystick = Joystick()
        return RPiDisplay(joystick), JoystickInput(joystick)
    else:
        return MacDisplay(), KeyboardInput()

def main():
    # 플랫폼에 맞는 핸들러 가져오기
    display, input_handler = get_platform_handlers()
    
    # 디스플레이 초기화
    display.init_display()
    
    # 시작 화면 실행
    start_screen = StartScreen(display, input_handler)
    if start_screen.run():
        # 게임 화면으로 전환
        game_screen = GameScreen(display, input_handler)
        game_screen.run()

if __name__ == '__main__':
    main()