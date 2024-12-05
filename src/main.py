from src.platforms.display.mac_display import MacDisplay
from src.platforms.display.rpi_display import RPiDisplay
from src.platforms.input.keyboard_input import KeyboardInput
from src.platforms.input.joystick_input import JoystickInput
from src.screens.start_screen import StartScreen
from src.screens.game_screen import GameScreen
import pygame
import os

def get_platform_handlers():
    if os.environ.get('PLATFORM') == 'rpi':
        try:
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
        display, input_handler = get_platform_handlers()
        display.init_display()
        
        while True:
            start_screen = StartScreen(display, input_handler)
            if not start_screen.run():
                break
            
            game_screen = GameScreen(display, input_handler)
            if not game_screen.run():
                continue
            break
            
    except Exception as e:
        print(f"게임 실행 중 오류 발생: {e}")
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()