from PIL import Image
import os
import math
import pygame

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.velocity = 0
        self.direction = 0
        self.image_path = os.path.join('src', 'assets', 'images', 'objects', 'ball.png')
        self.image = self._load_image(self.image_path)
        self.in_hole = False
    
    def _load_image(self, image_path):
        image = Image.open(image_path)
        return image.resize((self.width, self.height), Image.Resampling.LANCZOS)
    
    def update(self):
        if self.velocity > 0 and not self.in_hole:
            self.x += math.cos(self.direction) * self.velocity
            self.y -= math.sin(self.direction) * self.velocity  # y축은 아래가 양수
            self.velocity = max(0, self.velocity - 0.5)  # 마찰 적용

class HoleCup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50  # 크기 증가
        self.height = 80
        self.hole_radius = 15  # 실제 홀의 반지름
        self.image_path = os.path.join('src', 'assets', 'images', 'objects', 'holecup_flag.png')
        self.image = self._load_image(self.image_path)
    
    def _load_image(self, image_path):
        image = Image.open(image_path)
        return image.resize((self.width, self.height), Image.Resampling.LANCZOS)
    
    def check_ball_in_hole(self, ball):
        # 홀컵의 실제 구멍 위치 (깃발 아래쪽)
        hole_x = self.x
        hole_y = self.y + self.height/4  # 깃발 이미지의 아래쪽 부분
        
        # 공과 홀 중심점 사이의 거리 계산
        distance = math.sqrt((ball.x - hole_x)**2 + (ball.y - hole_y)**2)
        return distance < self.hole_radius

class Golfer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100  # 크기 증가
        self.height = 150
        self.power = 0
        self.max_power = 20
        self.is_charging = False
        self.image_path = os.path.join('src', 'assets', 'images', 'player', 'golfer.png')
        self.image = self._load_image(self.image_path)
    
    def _load_image(self, image_path):
        image = Image.open(image_path)
        return image.resize((self.width, self.height), Image.Resampling.LANCZOS)
    
    def update_power(self):
        if self.is_charging:
            self.power = min(self.power + 0.5, self.max_power)
    
    def move_to_ball(self, ball):
        # 공 뒤쪽으로 이동 (약간의 간격을 두고)
        self.x = ball.x - 20
        self.y = ball.y - 20  # 공보다 약간 아래에 위치

class GameScreen:
    def __init__(self, display, input_handler):
        self.display = display
        self.input_handler = input_handler
        self.width = 240
        self.height = 240
        
        # 게임 오브젝트 초기화
        self.background = self._load_background()
        self.golfer = Golfer(100, 180)
        # 골퍼 바로 앞에 공 위치시키기
        self.ball = Ball(self.golfer.x + 20, self.golfer.y + 20)
        self.holecup = HoleCup(120, 40)
        
        self.game_state = 'AIMING'  # AIMING, CHARGING, SHOOTING, MOVING_GOLFER
        self.shot_count = 0
        
        # 스코어 관련 변수 추가
        self.score_image = None
        self.score_display_time = 0
        self.SCORE_DISPLAY_DURATION = 180  # 3초 (60 FPS 기준)
        
        # 스코어 이미지 미리 로드
        self.score_images = self._load_score_images()
    
    def _load_background(self):
        bg_path = os.path.join('src', 'assets', 'images', 'course', 'background.png')
        bg = Image.open(bg_path)
        return bg.resize((self.width, self.height), Image.Resampling.LANCZOS)

    def _load_score_images(self):
        """스코어 이미지들을 미리 로드합니다."""
        scores = {
            1: 'hole_in_one.png',
            2: 'birdie.png',
            3: 'par.png',
            4: 'bogey.png',
            5: 'double_bogey.png',
            6: 'double_par.png'
        }
        
        loaded_images = {}
        for shots, filename in scores.items():
            path = os.path.join('src', 'assets', 'images', 'scores', filename)
            try:
                image = Image.open(path)
                # 화면 너비의 2/3 크기로 스코어 이미지 조정
                target_width = int(self.width * 0.66)
                ratio = target_width / image.width
                target_height = int(image.height * ratio)
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                loaded_images[shots] = image
            except Exception as e:
                print(f"Error loading score image {filename}: {e}")
                loaded_images[shots] = None
        
        return loaded_images

    def _show_score(self):
        """샷 수에 따른 스코어 이미지를 설정합니다."""
        if self.shot_count in self.score_images:
            self.score_image = self.score_images[self.shot_count]
            self.score_display_time = self.SCORE_DISPLAY_DURATION
    
    def update(self):
        inputs = self.input_handler.get_input()
        if inputs is None:
            return False

        if self.game_state == 'AIMING':
            if inputs['A']:  # A 버튼으로 파워 충전 시작
                self.game_state = 'CHARGING'
                self.golfer.is_charging = True
        
        elif self.game_state == 'CHARGING':
            self.golfer.update_power()
            if not inputs['A']:  # A 버튼을 떼면 샷
                self.ball.velocity = self.golfer.power
                self.ball.direction = math.pi / 2  # 위쪽으로 발사
                self.golfer.power = 0
                self.golfer.is_charging = False
                self.game_state = 'SHOOTING'
                self.shot_count += 1
        
        elif self.game_state == 'SHOOTING':
            self.ball.update()
            
            # 홀컵 충돌 체크
            if self.holecup.check_ball_in_hole(self.ball):
                self.ball.in_hole = True
                print(f"홀인! {self.shot_count}번 만에 성공!")
                self._show_score()
                return True
            
            # 공이 멈추면 골퍼 이동
            if self.ball.velocity == 0 and not self.ball.in_hole:
                self.game_state = 'MOVING_GOLFER'
        
        elif self.game_state == 'MOVING_GOLFER':
            self.golfer.move_to_ball(self.ball)
            self.game_state = 'AIMING'
        
        # 스코어 표시 타이머 업데이트
        if self.score_display_time > 0:
            self.score_display_time -= 1
        
        return True
    
    def draw(self):
        # 배경 이미지 복사
        game_image = self.background.copy()
        
        # 깃발과 홀컵 그리기
        game_image.paste(self.holecup.image, 
                        (int(self.holecup.x - self.holecup.width//2), 
                         int(self.holecup.y - self.holecup.height//2)), 
                        self.holecup.image)
        
        # 골프공 그리기
        if not self.ball.in_hole:
            game_image.paste(self.ball.image, 
                            (int(self.ball.x - self.ball.width//2), 
                             int(self.ball.y - self.ball.height//2)), 
                            self.ball.image)
        
        # 골퍼 그리기 (공이 홀인되지 않았을 때만)
        if not self.ball.in_hole:
            game_image.paste(self.golfer.image, 
                            (int(self.golfer.x - self.golfer.width//2), 
                             int(self.golfer.y - self.golfer.height//2)), 
                            self.golfer.image)
        
        # 파워 게이지 그리기
        if self.game_state == 'CHARGING':
            power_height = int((self.golfer.power / self.golfer.max_power) * 50)
            for y in range(power_height):
                for x in range(5):
                    game_image.putpixel((20, 200 - y), (255, 0, 0))

        # 스코어 이미지 그리기
        if self.score_image and self.score_display_time > 0:
            # 스코어 이미지를 화면 중앙에 배치
            score_x = (self.width - self.score_image.width) // 2
            score_y = (self.height - self.score_image.height) // 2
            game_image.paste(self.score_image, (score_x, score_y), self.score_image)
        
        return game_image
    
    def run(self):
        """게임 화면 메인 루프"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # 업데이트 및 그리기
            if not self.update():
                running = False
            
            game_image = self.draw()
            self.display.show_image(game_image)
            
            # 종료 체크
            if self.display.check_quit():
                running = False
                break
                
            # FPS 제어
            clock.tick(60)