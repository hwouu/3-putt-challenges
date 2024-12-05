from enum import Enum
from src.objects.ball import Ball
from src.objects.golfer import Golfer
from src.objects.holecup import HoleCup
from src.objects.obstacles.fence import MovingFence
from src.core.physics_engine import PhysicsEngine
import math

class GameState(Enum):
    AIMING = "AIMING"
    CHARGING = "CHARGING"
    SHOOTING = "SHOOTING"
    MOVING_GOLFER = "MOVING_GOLFER"
    SHOWING_SCORE = "SHOWING_SCORE"
    COURSE_TRANSITION = "COURSE_TRANSITION"
    PAUSED = "PAUSED"

class GameEngine:
    def __init__(self):
        self.physics_engine = PhysicsEngine()
        self._initialize_game_objects()
        self._initialize_game_state()
        self._setup_current_course()

    def _initialize_game_objects(self):
        self.golfer = Golfer(100, 180)
        self.ball = Ball(self.golfer.x + 20, self.golfer.y + 20)
        self.holecup = HoleCup(120, 40)

    def _initialize_game_state(self):
        self.state = GameState.AIMING
        self.previous_state = None
        self.shot_count = 0
        self.current_course = 1
        self.par = 3
        self.score_display_time = 0
        self.SCORE_DISPLAY_DURATION = 120
        self.direction_change_speed = math.pi / 180
        self.input_cooldown = 0
        self.COOLDOWN_DURATION = 20

    def _setup_current_course(self):
        self.physics_engine.clear_obstacles()

        if self.current_course == 2:
            # 코스 2의 장애물 설정
            fence = MovingFence(120, 120, "horizontal", 2.0)
            self.physics_engine.add_obstacle(fence)
            self.holecup = HoleCup(120, 40)
            self.par = 4

    def update(self, inputs):
        # 장애물 지속적 업데이트 추가
        self.physics_engine.update(self.ball)

        if self.input_cooldown > 0:
            self.input_cooldown -= 1
            inputs['A'] = False

        if inputs['B'] and self.state not in [GameState.SHOWING_SCORE, GameState.COURSE_TRANSITION]:
            return self._handle_pause()

        if self.state == GameState.SHOWING_SCORE:
            return self._handle_score_display()
        
        if self.state == GameState.COURSE_TRANSITION:
            return self._handle_course_transition(inputs)

        if self.state == GameState.PAUSED:
            return self._handle_pause_state(inputs)

        if self.state == GameState.AIMING:
            return self._handle_aiming(inputs)
        
        if self.state == GameState.CHARGING:
            return self._handle_charging(inputs)
        
        if self.state == GameState.SHOOTING:
            return self._handle_shooting()
        
        if self.state == GameState.MOVING_GOLFER:
            return self._handle_moving_golfer()

        return True

    def _handle_pause(self):
        if self.state != GameState.PAUSED:
            self.previous_state = self.state
            self.state = GameState.PAUSED
        else:
            self.state = self.previous_state
            self.input_cooldown = self.COOLDOWN_DURATION
        return True

    def _handle_score_display(self):
        if self.score_display_time > 0:
            self.score_display_time -= 1
        else:
            self.state = GameState.COURSE_TRANSITION
        return True

    def _handle_course_transition(self, inputs):
        if inputs['A']:
            self._move_to_next_course()
        elif inputs['B']:
            self._retry_current_course()
        return True

    def _handle_aiming(self, inputs):
        if inputs['left']:
            self.ball.direction += self.direction_change_speed
        if inputs['right']:
            self.ball.direction -= self.direction_change_speed
        
        if inputs['A']:
            self.state = GameState.CHARGING
            self.golfer.start_charging()
        return True

    def _handle_charging(self, inputs):
        self.golfer.update_power()
        if not inputs['A']:
            power = self.golfer.stop_charging()
            self.ball.set_velocity(power)
            self.state = GameState.SHOOTING
            self.shot_count += 1
        return True

    def _handle_shooting(self):
        self.ball.update()
        self.physics_engine.update(self.ball)

        if self.holecup.check_ball_in_hole(self.ball):
            self.ball.in_hole = True
            self._show_score()
            return True
        
        if not self.ball.is_moving() and not self.ball.in_hole:
            self.state = GameState.MOVING_GOLFER
        return True

    def _handle_moving_golfer(self):
        self.golfer.move_to_ball(self.ball)
        self.state = GameState.AIMING
        return True

    def _move_to_next_course(self):
        self.current_course += 1
        self._restart_game()

    def _retry_current_course(self):
        self._restart_game()

    def _restart_game(self):
        self._initialize_game_objects()
        self.shot_count = 0
        self.score_display_time = 0
        self.state = GameState.AIMING
        self.input_cooldown = self.COOLDOWN_DURATION
        self._setup_current_course()

    def _show_score(self):
        self.score_display_time = self.SCORE_DISPLAY_DURATION
        self.state = GameState.SHOWING_SCORE

    def get_game_objects(self):
        return {
            'golfer': self.golfer,
            'ball': self.ball,
            'holecup': self.holecup,
            'state': self.state,
            'shot_count': self.shot_count,
            'current_course': self.current_course,
            'score_display_time': self.score_display_time,
            'obstacles': self.physics_engine.obstacles
        }
