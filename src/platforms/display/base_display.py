# src/platforms/display/base_display.py
from abc import ABC, abstractmethod

class BaseDisplay(ABC):
    @abstractmethod
    def init_display(self):
        """디스플레이를 초기화합니다."""
        pass
    
    @abstractmethod
    def show_image(self, image):
        """이미지를 화면에 표시합니다."""
        pass
    
    @abstractmethod
    def clear(self):
        """화면을 지웁니다."""
        pass
    
    @abstractmethod
    def check_quit(self):
        """종료 이벤트를 확인합니다."""
        pass