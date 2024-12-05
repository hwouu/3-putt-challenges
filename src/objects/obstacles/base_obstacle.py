from abc import ABC, abstractmethod
from PIL import Image
from src.utils.asset_loader import load_and_resize_image  # 절대 경로로 변경

class BaseObstacle(ABC):
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0
        self.is_moving = False
        self.movement_bounds = None
        self.collision_enabled = True
        
        # 이미지 로드
        self.image = load_and_resize_image(image_path, width, height)
    
    def get_position(self):
        """장애물의 현재 위치를 반환합니다."""
        return self.x, self.y
    
    def get_bounds(self):
        """충돌 감지를 위한 장애물의 경계를 반환합니다."""
        return {
            'left': self.x - self.width/2,
            'right': self.x + self.width/2,
            'top': self.y - self.height/2,
            'bottom': self.y + self.height/2
        }
    
    def set_movement_bounds(self, min_x, max_x, min_y, max_y):
        """장애물의 이동 범위를 설정합니다."""
        self.movement_bounds = {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y
        }
    
    def check_collision(self, ball):
        """공과의 충돌을 감지합니다."""
        if not self.collision_enabled:
            return False
            
        bounds = self.get_bounds()
        ball_x, ball_y = ball.get_position()
        
        return (bounds['left'] < ball_x < bounds['right'] and 
                bounds['top'] < ball_y < bounds['bottom'])
    
    @abstractmethod
    def update(self):
        """장애물의 상태를 업데이트합니다. 하위 클래스에서 구현해야 합니다."""
        pass
    
    @abstractmethod
    def handle_collision(self, ball):
        """공과의 충돌을 처리합니다. 하위 클래스에서 구현해야 합니다."""
        pass