from src.objects.obstacles.base_obstacle import BaseObstacle
from src.utils.asset_loader import get_asset_path
import math

class MovingFence(BaseObstacle):
    def __init__(self, x, y, movement_type="horizontal", speed=2.0):
        super().__init__(
            x=x, 
            y=y, 
            width=40,
            height=80,
            image_path=get_asset_path('objects', 'fence.png')
        )
        
        self.movement_type = movement_type
        self.speed = speed
        self.initial_position = (x, y)
        self.movement_distance = 160  # 기존 100에서 160으로 확장
        self.angle = 0  # 원형 이동을 위한 각도
        
        # 이동 타입에 따른 초기 설정
        if movement_type == "horizontal":
            self.set_movement_bounds(
                x - self.movement_distance/2,
                x + self.movement_distance/2,
                y, y
            )
        elif movement_type == "vertical":
            self.set_movement_bounds(
                x, x,
                y - self.movement_distance/2,
                y + self.movement_distance/2
            )
    
    def update(self):
        if self.movement_type == "horizontal":
            self._update_horizontal()
        elif self.movement_type == "vertical":
            self._update_vertical()
        elif self.movement_type == "circular":
            self._update_circular()
    
    def _update_horizontal(self):
        self.x += self.speed
        if self.x > self.movement_bounds['max_x']:
            self.x = self.movement_bounds['max_x']
            self.speed = -abs(self.speed)
        elif self.x < self.movement_bounds['min_x']:
            self.x = self.movement_bounds['min_x']
            self.speed = abs(self.speed)
    
    def _update_vertical(self):
        self.y += self.speed
        if self.y > self.movement_bounds['max_y']:
            self.y = self.movement_bounds['max_y']
            self.speed = -abs(self.speed)
        elif self.y < self.movement_bounds['min_y']:
            self.y = self.movement_bounds['min_y']
            self.speed = abs(self.speed)
    
    def _update_circular(self):
        self.angle += self.speed * 0.02
        self.x = self.initial_position[0] + math.cos(self.angle) * self.movement_distance/2
        self.y = self.initial_position[1] + math.sin(self.angle) * self.movement_distance/2
    
    def handle_collision(self, ball):
        """공과 울타리의 충돌을 처리합니다."""
        ball.direction = math.pi - ball.direction
        ball.velocity *= ball.bounce_damping
        
        # 울타리와 충돌 시 약간의 반동 추가
        if self.movement_type in ["horizontal", "circular"]:
            ball.velocity += abs(self.speed) * 0.5
