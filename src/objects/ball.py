# src/objects/ball.py

from PIL import Image  # Image 모듈 임포트 추가
import math
from ..utils.asset_loader import get_asset_path, load_and_resize_image

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.velocity = 0
        self.direction = math.pi / 2
        self.bounce_damping = 0.7
        self.in_hole = False
        
        # 공 이미지 로드
        self.image = load_and_resize_image(
            get_asset_path('objects', 'ball.png'),
            self.width,
            self.height
        )
        
        # 조준선 관련 설정
        self.aim_line_width = 15
        self.aim_line_height = 100
        self.aim_line = load_and_resize_image(
            get_asset_path('objects', 'aim_line.png'),
            self.aim_line_width,
            self.aim_line_height
        )
    
    def get_rotated_aim_line(self):
        """조준선을 현재 방향에 맞게 회전시킵니다."""
        angle = math.degrees(self.direction) - 90
        rotated = self.aim_line.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
        new_width, new_height = rotated.size
        return rotated, new_width, new_height
    
    def update(self):
        """공의 위치와 속도를 업데이트합니다."""
        if self.velocity > 0 and not self.in_hole:
            next_x = self.x + math.cos(self.direction) * self.velocity
            next_y = self.y - math.sin(self.direction) * self.velocity

            # 벽과의 충돌 처리
            if next_x < 10 or next_x > 230:
                self.direction = math.pi - self.direction
                self.velocity *= self.bounce_damping
                next_x = max(10, min(230, next_x))
            
            if next_y < 10 or next_y > 230:
                self.direction = -self.direction
                self.velocity *= self.bounce_damping
                next_y = max(10, min(230, next_y))

            self.x = next_x
            self.y = next_y
            self.velocity = max(0, self.velocity - 0.5)

    def get_position(self):
        """공의 현재 위치를 반환합니다."""
        return self.x, self.y

    def set_velocity(self, power):
        """공의 초기 속도를 설정합니다."""
        self.velocity = power

    def is_moving(self):
        """공이 움직이고 있는지 확인합니다."""
        return self.velocity > 0