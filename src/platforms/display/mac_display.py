
# src/platforms/display/mac_display.py
import pygame
from .base_display import BaseDisplay

class MacDisplay:
    def __init__(self, width=240, height=240):
        self.width = width
        self.height = height
        self.screen = None
        
    def init_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("3-Putt Challenge")
        
    def show_image(self, pil_image):
        # PIL Image를 pygame surface로 변환
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        
        pygame_image = pygame.image.fromstring(data, size, mode)
        self.screen.blit(pygame_image, (0, 0))
        pygame.display.flip()
        
    def clear(self):
        self.screen.fill((255, 255, 255))
        pygame.display.flip()

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False