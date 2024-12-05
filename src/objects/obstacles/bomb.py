# src/objects/obstacles/bomb.py
from src.objects.obstacles.base_obstacle import BaseObstacle
from src.utils.asset_loader import get_asset_path

class Bomb(BaseObstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, get_asset_path('objects', 'bomb.png'))
        self.is_visible = False
        self.triggered = False

    def update(self):
        pass

    def handle_collision(self, ball):
        if not self.triggered:
            self.triggered = True
            self.is_visible = True
            ball.velocity = 0
            return True
        return False

    def reset(self):
        self.triggered = False
        self.is_visible = False