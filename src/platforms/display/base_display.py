# src/platforms/display/base_display.py
from abc import ABC, abstractmethod

class BaseDisplay(ABC):
    @abstractmethod
    def init_display(self):
        pass
    
    @abstractmethod
    def show_image(self, image):
        pass
    
    @abstractmethod
    def clear(self):
        pass

