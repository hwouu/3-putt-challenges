# src/platforms/display/rpi_display.py
from .base_display import BaseDisplay

class RPiDisplay(BaseDisplay):
    def __init__(self, joystick):
        self.joystick = joystick
        
    def init_display(self):
        # 기존 Joystick 클래스의 디스플레이 초기화 코드 사용
        pass
        
    def show_image(self, image):
        self.joystick.disp.image(image)
        
    def clear(self):
        # 화면 클리어 구현
        pass