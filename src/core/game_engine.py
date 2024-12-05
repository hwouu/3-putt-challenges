from enum import Enum
from src.objects.ball import Ball
from src.objects.golfer import Golfer
from src.objects.holecup import HoleCup
from src.objects.obstacles.fence import MovingFence
from src.core.physics_engine import PhysicsEngine
from src.objects.obstacles.bomb import Bomb
from src.models.score_card import ScoreCard
import math

class GameState(Enum):
    AIMING = "AIMING"
    CHARGING = "CHARGING"
    SHOOTING = "SHOOTING"
    MOVING_GOLFER = "MOVING_GOLFER"
    SHOWING_SCORE = "SHOWING_SCORE"
    COURSE_TRANSITION = "COURSE_TRANSITION"
    PAUSED = "PAUSED"
    SHOW_SCORECARD = "SHOW_SCORECARD"

class GameEngine:
    def __init__(self):
        self.physics_engine = PhysicsEngine()
        self.score_card = ScoreCard()
        self._initialize_game_state()
        self._initialize_game_objects()
        self._setup_current_course()

    def _initialize_game_objects(self):
        if self.current_course == 2:
            self.golfer = Golfer(60, 200)
            self.holecup = HoleCup(180, 40)
        elif self.current_course == 3:
            self.golfer = Golfer(180, 200)
            self.holecup = HoleCup(60, 40)
        else:
            self.golfer = Golfer(100, 180)
            self.holecup = HoleCup(120, 40)
        
        self.ball = Ball(self.golfer.x + 20, self.golfer.y + 20)

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
        self.golfer_move_delay = 0
        self.GOLFER_MOVE_DELAY = 90

    def _setup_current_course(self):
        self.physics_engine.clear_obstacles()
        if self.current_course == 2:
            fence = MovingFence(120, 120, "horizontal", 2.0)
            self.physics_engine.add_obstacle(fence)
            self.par = 3
        elif self.current_course == 3:
            bomb1 = Bomb(120, 120)
            bomb2 = Bomb(90, 80)
            bomb3 = Bomb(150, 80)
            self.physics_engine.add_obstacle(bomb1)
            self.physics_engine.add_obstacle(bomb2)
            self.physics_engine.add_obstacle(bomb3)
            self.par = 3

    def update(self, inputs):
        self.physics_engine.update(self.ball)
        if self.input_cooldown > 0:
            self.input_cooldown -= 1
            inputs['A'] = False

        if self.state == GameState.SHOW_SCORECARD:
            return False

        if inputs['B'] and self.state not in [GameState.SHOWING_SCORE, GameState.COURSE_TRANSITION]:
            if self.state != GameState.PAUSED:
                self.previous_state = self.state
                self.state = GameState.PAUSED
            return True

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

    def _handle_pause_state(self, inputs):
        if inputs['B']:
            if self.previous_state:
                self.state = self.previous_state
                self.previous_state = None
                return True
        elif inputs['A']:
            self._restart_current_course()
            self.state = GameState.AIMING
        return True

    def _handle_score_display(self):
        if self.score_display_time > 0:
            self.score_display_time -= 1
        else:
            if self.current_course == 3:
                self.state = GameState.SHOW_SCORECARD 
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
        previous_velocity = self.ball.velocity
        initial_ball_position = (self.ball.x, self.ball.y)
        initial_golfer_position = (self.golfer.x, self.golfer.y)
        
        self.ball.update()
        collision = self.physics_engine.update(self.ball)

        if collision:
            if isinstance(self.physics_engine.get_last_collision(), Bomb):
                self.shot_count += 2
            elif isinstance(self.physics_engine.get_last_collision(), MovingFence):
                self.shot_count += 1
                
            self.ball.x, self.ball.y = initial_ball_position
            self.golfer.x, self.golfer.y = initial_golfer_position
            self.ball.velocity = 0
            
            if self.shot_count >= self.par * 2:
                self._show_score()
                return True
            
            self.state = GameState.MOVING_GOLFER
            return True

        if self.holecup.check_ball_in_hole(self.ball):
            self.ball.in_hole = True
            self._show_score()
            return True
        
        if not self.ball.is_moving() and not self.ball.in_hole:
            if self.shot_count >= self.par * 2:
                self._show_score()
                return True
                
            if self.golfer_move_delay < self.GOLFER_MOVE_DELAY:
                self.golfer_move_delay += 1
                return True
            self.golfer_move_delay = 0
            self.state = GameState.MOVING_GOLFER
        return True

    def _handle_moving_golfer(self):
        self.golfer.move_to_ball(self.ball)
        self.state = GameState.AIMING
        return True

    def _move_to_next_course(self):
        if self.current_course == 3:
            self.state = GameState.SHOW_SCORECARD
            return
        
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
        self.golfer_move_delay = 0
        self._setup_current_course()

    def _restart_current_course(self):
        self._initialize_game_objects()
        self.shot_count = 0
        self.score_display_time = 0
        self.input_cooldown = self.COOLDOWN_DURATION
        self.golfer_move_delay = 0
        self._setup_current_course()

    def _show_score(self):
        self.score_display_time = self.SCORE_DISPLAY_DURATION
        self.state = GameState.SHOWING_SCORE
        self.score_card.add_score(self.current_course, self.shot_count)

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