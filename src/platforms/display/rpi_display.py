# src/platforms/display/rpi_display.py
from src.platforms.display.base_display import BaseDisplay

class RPiDisplay(BaseDisplay):
    def __init__(self, joystick):
        self.joystick = joystick
        
    def init_display(self):
        # 라즈베리파이의 디스플레이 초기화
        if hasattr(self.joystick, 'init_display'):
            self.joystick.init_display()
        
    def show_image(self, image):
        if hasattr(self.joystick, 'disp'):
            self.joystick.disp.image(image)
        
    def clear(self):
        if hasattr(self.joystick, 'disp'):
            self.joystick.disp.clear()
            self.joystick.disp.display()
            
    def check_quit(self):
        # 라즈베리파이에서는 별도의 종료 체크가 필요 없을 수 있음
        return False