# src/objects/golfer.py

from ..utils.asset_loader import get_asset_path, load_and_resize_image

class Golfer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 150
        self.power = 0
        self.max_power = 20
        self.is_charging = False
        
        # 골퍼 이미지 로드
        self.image = load_and_resize_image(
            get_asset_path('player', 'golfer.png'),
            self.width,
            self.height
        )
    
    def update_power(self):
        """스윙 파워를 업데이트합니다."""
        if self.is_charging:
            self.power = min(self.power + 0.5, self.max_power)
    
    def move_to_ball(self, ball):
        """골퍼를 공의 위치로 이동시킵니다."""
        self.x = ball.x - 20
        self.y = ball.y - 20
    
    def start_charging(self):
        """스윙 충전을 시작합니다."""
        self.is_charging = True
        self.power = 0
    
    def stop_charging(self):
        """스윙 충전을 종료하고 최종 파워를 반환합니다."""
        final_power = self.power
        self.power = 0
        self.is_charging = False
        return final_power
    
    def get_position(self):
        """골퍼의 현재 위치를 반환합니다."""
        return self.x, self.y
    
    def get_power_percentage(self):
        """현재 파워를 퍼센트로 반환합니다."""
        return (self.power / self.max_power) * 100