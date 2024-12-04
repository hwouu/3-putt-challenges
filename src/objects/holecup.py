# src/objects/holecup.py

import math
from ..utils.asset_loader import get_asset_path, load_and_resize_image

class HoleCup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.hole_radius = 15
        
        # 홀컵 이미지 로드
        self.image = load_and_resize_image(
            get_asset_path('objects', 'holecup_flag.png'),
            self.width,
            self.height
        )
    
    def check_ball_in_hole(self, ball):
        """
        공이 홀컵 안에 들어갔는지 확인합니다.
        
        Args:
            ball: Ball 객체
            
        Returns:
            bool: 공이 홀컵 안에 있으면 True, 그렇지 않으면 False
        """
        hole_x = self.x
        hole_y = self.y + self.height/4  # 깃발 위치 조정
        ball_x, ball_y = ball.get_position()
        
        distance = math.sqrt((ball_x - hole_x)**2 + (ball_y - hole_y)**2)
        return distance < self.hole_radius
    
    def get_position(self):
        """홀컵의 현재 위치를 반환합니다."""
        return self.x, self.y
    
    def get_hole_position(self):
        """실제 홀의 중심 위치를 반환합니다."""
        return self.x, self.y + self.height/4
    
    def get_dimensions(self):
        """홀컵의 크기 정보를 반환합니다."""
        return {
            'width': self.width,
            'height': self.height,
            'hole_radius': self.hole_radius
        }