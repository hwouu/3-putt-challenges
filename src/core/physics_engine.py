from typing import List
from src.objects.ball import Ball
from src.objects.obstacles.base_obstacle import BaseObstacle

class PhysicsEngine:
    def __init__(self):
        self.gravity = 0.5
        self.friction = 0.98
        self.obstacles: List[BaseObstacle] = []
        self.last_collision = None

    def add_obstacle(self, obstacle: BaseObstacle):
        self.obstacles.append(obstacle)

    def get_last_collision(self):
        return self.last_collision

    def update(self, ball: Ball) -> bool:
        collision_occurred = False
        self.last_collision = None
        
        for obstacle in self.obstacles:
            obstacle.update()
            
        if ball.velocity > 0 and not ball.in_hole:
            for obstacle in self.obstacles:
                if obstacle.check_collision(ball):
                    obstacle.handle_collision(ball)
                    self.last_collision = obstacle
                    collision_occurred = True
                    break
            
            ball.velocity *= self.friction
            ball.velocity = max(0, ball.velocity - self.gravity)

        return collision_occurred

    def clear_obstacles(self):
        self.obstacles.clear()
        self.last_collision = None