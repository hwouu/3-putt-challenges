# main.py

from src.platforms.display.mac_display import MacDisplay
from src.platforms.display.rpi_display import RPiDisplay
from src.platforms.input.keyboard_input import KeyboardInput
from src.platforms.input.joystick_input import JoystickInput
from src.screens.start_screen import StartScreen
from src.screens.game_screen import GameScreen
import pygame
import os

def get_platform_handlers():
    """현재 플랫폼에 맞는 디스플레이와 입력 핸들러를 반환합니다."""
    if os.environ.get('PLATFORM') == 'rpi':
        try:
            # joystick 임포트를 try-except 블록으로 감싸서 처리
            try:
                from src.platforms.input.joystick import Joystick
            except ImportError:
                print("라즈베리파이 전용 joystick 모듈을 찾을 수 없습니다.")
                return MacDisplay(), KeyboardInput()
                
            joystick = Joystick()
            return RPiDisplay(joystick), JoystickInput(joystick)
        except Exception as e:
            print(f"라즈베리파이 환경 설정 실패: {e}")
            return MacDisplay(), KeyboardInput()
    else:
        return MacDisplay(), KeyboardInput()
def main():
   try:
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
   except Exception as e:
       print(f"게임 실행 중 오류 발생: {e}")
   finally:
       # 게임 종료 시 정리 작업
       pygame.quit()

if __name__ == '__main__':
   main()