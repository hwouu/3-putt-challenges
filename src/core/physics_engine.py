from typing import List
from src.objects.ball import Ball
from src.objects.obstacles.base_obstacle import BaseObstacle

class PhysicsEngine:
    def __init__(self):
        self.gravity = 0.5
        self.friction = 0.98
        self.obstacles: List[BaseObstacle] = []

    def add_obstacle(self, obstacle: BaseObstacle):
        self.obstacles.append(obstacle)

    def update(self, ball: Ball):
        # 장애물 업데이트 - ball이 움직이지 않아도 실행
        for obstacle in self.obstacles:
            obstacle.update()
            
        if ball.velocity > 0 and not ball.in_hole:
            # 충돌 감지 및 처리
            for obstacle in self.obstacles:
                if obstacle.check_collision(ball):
                    obstacle.handle_collision(ball)
            
            # 공 물리 업데이트
            ball.velocity *= self.friction
            ball.velocity = max(0, ball.velocity - self.gravity)

    def clear_obstacles(self):
        self.obstacles.clear()