# src/core/game_engine.py

from enum import Enum
from ..objects.ball import Ball
from ..objects.golfer import Golfer
from ..objects.holecup import HoleCup
import math  # math 모듈 추가

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
        # 게임 오브젝트 초기화
        self.golfer = Golfer(100, 180)
        self.ball = Ball(self.golfer.x + 20, self.golfer.y + 20)
        self.holecup = HoleCup(120, 40)
        
        # 게임 상태 관리
        self.state = GameState.AIMING
        self.previous_state = None
        self.shot_count = 0
        self.current_course = 1
        self.par = 3
        
        # 점수 표시 관련
        self.score_display_time = 0
        self.SCORE_DISPLAY_DURATION = 120
        
        # 방향 변경 속도
        self.direction_change_speed = math.pi / 180
        
        # 입력 쿨다운
        self.input_cooldown = 0
        self.COOLDOWN_DURATION = 20

    def update(self, inputs):
        """게임 상태를 업데이트합니다."""
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
        """일시정지 처리"""
        if self.state != GameState.PAUSED:
            self.previous_state = self.state
            self.state = GameState.PAUSED
        else:
            self.state = self.previous_state
            self.input_cooldown = self.COOLDOWN_DURATION
        return True

    def _handle_score_display(self):
        """점수 표시 처리"""
        if self.score_display_time > 0:
            self.score_display_time -= 1
        else:
            self.state = GameState.COURSE_TRANSITION
        return True

    def _handle_course_transition(self, inputs):
        """코스 전환 처리"""
        if inputs['A']:
            self._move_to_next_course()
        elif inputs['B']:
            self._retry_current_course()
        return True

    def _handle_aiming(self, inputs):
        """조준 상태 처리"""
        if inputs['left']:
            self.ball.direction += self.direction_change_speed
        if inputs['right']:
            self.ball.direction -= self.direction_change_speed
        
        if inputs['A']:
            self.state = GameState.CHARGING
            self.golfer.start_charging()
        return True

    def _handle_charging(self, inputs):
        """파워 충전 상태 처리"""
        self.golfer.update_power()
        if not inputs['A']:
            power = self.golfer.stop_charging()
            self.ball.set_velocity(power)
            self.state = GameState.SHOOTING
            self.shot_count += 1
        return True

    def _handle_shooting(self):
        """샷 진행 상태 처리"""
        self.ball.update()
        
        if self.holecup.check_ball_in_hole(self.ball):
            self.ball.in_hole = True
            self._show_score()
            return True
        
        if not self.ball.is_moving() and not self.ball.in_hole:
            self.state = GameState.MOVING_GOLFER
        return True

    def _handle_moving_golfer(self):
        """골퍼 이동 상태 처리"""
        self.golfer.move_to_ball(self.ball)
        self.state = GameState.AIMING
        return True

    def _move_to_next_course(self):
        """다음 코스로 이동"""
        self.current_course += 1
        self._restart_game()

    def _retry_current_course(self):
        """현재 코스 재시도"""
        self._restart_game()

    def _restart_game(self):
        """게임 상태 초기화"""
        self.golfer = Golfer(100, 180)
        self.ball = Ball(self.golfer.x + 20, self.golfer.y + 20)
        self.shot_count = 0
        self.score_display_time = 0
        self.state = GameState.AIMING
        self.input_cooldown = self.COOLDOWN_DURATION

    def _show_score(self):
        """점수 표시 시작"""
        self.score_display_time = self.SCORE_DISPLAY_DURATION
        self.state = GameState.SHOWING_SCORE

    def get_game_objects(self):
        """현재 게임 오브젝트들의 상태를 반환"""
        return {
            'golfer': self.golfer,
            'ball': self.ball,
            'holecup': self.holecup,
            'state': self.state,
            'shot_count': self.shot_count,
            'current_course': self.current_course,
            'score_display_time': self.score_display_time
        }