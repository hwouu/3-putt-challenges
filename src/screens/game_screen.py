from PIL import Image, ImageDraw, ImageFont
import math
import pygame
from src.core.game_engine import GameEngine, GameState
from src.utils.asset_loader import get_asset_path, load_and_resize_image
from src.objects.obstacles.bomb import Bomb
from src.screens.score_card_screen import ScoreCardScreen

class GameScreen:
    def __init__(self, display, input_handler):
        self.display = display
        self.input_handler = input_handler
        self.width = 240
        self.height = 240
        self.game_engine = GameEngine()
        self._load_assets()

    def _load_assets(self):
        self.background = self._load_background()
        self.pause_image = self._load_pause_screen()
        self.next_course_image = self._load_next_course_screen()
        self.score_images = self._load_score_images()
        self.score_image = None
        self.bomb_effect = load_and_resize_image(get_asset_path('objects', 'bomb.png'), 40, 40)  # 폭탄 이펙트 추가
        try:
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except IOError:
            self.font = ImageFont.load_default()

    def _load_background(self):
        """배경 이미지를 로드합니다."""
        return load_and_resize_image(
            get_asset_path('course', 'background.png'),
            self.width,
            self.height
        )

    def _load_pause_screen(self):
        """일시정지 화면 이미지를 로드합니다."""
        try:
            return load_and_resize_image(
                get_asset_path('ui', 'pause_screen.png'),
                self.width,
                self.height
            )
        except Exception as e:
            print(f"Error loading pause screen: {e}")
            image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.text((self.width // 2 - 30, self.height // 2), "PAUSE", fill=(255, 255, 255))
            return image

    def _load_next_course_screen(self):
        """다음 코스 화면 이미지를 로드합니다."""
        try:
            return load_and_resize_image(
                get_asset_path('ui', 'next_course.png'),
                self.width,
                self.height
            )
        except Exception as e:
            print(f"Error loading next course screen: {e}")
            image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.text((self.width // 2 - 50, self.height // 2), "NEXT COURSE", fill=(255, 255, 255))
            return image

    def _load_score_images(self):
        """점수 관련 이미지들을 로드합니다."""
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
            try:
                image = Image.open(get_asset_path('scores', filename))
                target_width = int(self.width * 0.66)
                ratio = target_width / image.width
                target_height = int(image.height * ratio)
                loaded_images[shots] = image.resize(
                    (target_width, target_height),
                    Image.Resampling.LANCZOS
                )
            except Exception as e:
                print(f"Error loading score image {filename}: {e}")
                loaded_images[shots] = None

        return loaded_images

    def _draw_game_info(self, draw):
        """게임 정보(PAR, SHOT 등)를 화면에 그립니다."""
        text_color = (255, 255, 255)
        shadow_color = (0, 0, 0)
        game_objects = self.game_engine.get_game_objects()

        par_text = f"PAR {self.game_engine.par}"
        draw.text((self.width - 80 + 1, 10 + 1), par_text, font=self.font, fill=shadow_color)
        draw.text((self.width - 80, 10), par_text, font=self.font, fill=text_color)

        shot_text = f"SHOT {game_objects['shot_count']}"
        draw.text((self.width - 80 + 1, 35 + 1), shot_text, font=self.font, fill=shadow_color)
        draw.text((self.width - 80, 35), shot_text, font=self.font, fill=text_color)

    def update(self):
        """게임 상태를 업데이트합니다."""
        inputs = self.input_handler.get_input()
        if inputs is None:
            return False

        return self.game_engine.update(inputs)

    def draw(self):
        """현재 게임 상태를 화면에 그립니다."""
        game_objects = self.game_engine.get_game_objects()
        current_state = game_objects['state']

        if current_state == GameState.PAUSED:
            return self.pause_image

        if current_state == GameState.COURSE_TRANSITION:
            return self.next_course_image

        game_image = self.background.copy()
        draw = ImageDraw.Draw(game_image)

        self._draw_game_info(draw)

        # 장애물 그리기
        for obstacle in game_objects['obstacles']:
            if isinstance(obstacle, Bomb):
                if obstacle.is_visible:  # 트리거된 폭탄만 표시
                    game_image.paste(
                        self.bomb_effect,
                        (
                            int(obstacle.x - obstacle.width // 2),
                            int(obstacle.y - obstacle.height // 2)
                        ),
                        self.bomb_effect
                    )
            else:  # 일반 장애물
                game_image.paste(
                    obstacle.image,
                    (
                        int(obstacle.x - obstacle.width // 2),
                        int(obstacle.y - obstacle.height // 2)
                    ),
                    obstacle.image
                )

        # HoleCup 그리기
        holecup = game_objects['holecup']
        game_image.paste(
            holecup.image,
            (
                int(holecup.x - holecup.width // 2),
                int(holecup.y - holecup.height // 2)
            ),
            holecup.image
        )

        ball = game_objects['ball']
        golfer = game_objects['golfer']

        if current_state == GameState.AIMING and not ball.in_hole:
            aim_line, line_width, line_height = ball.get_rotated_aim_line()
            line_x = int(ball.x - line_width // 2)
            line_y = int(ball.y - line_height // 2)
            offset = ball.height // 2
            line_y += offset
            game_image.paste(aim_line, (line_x, line_y), aim_line)

        if not ball.in_hole:
            game_image.paste(
                ball.image,
                (
                    int(ball.x - ball.width // 2),
                    int(ball.y - ball.height // 2)
                ),
                ball.image
            )

            game_image.paste(
                golfer.image,
                (
                    int(golfer.x - golfer.width // 2),
                    int(golfer.y - golfer.height // 2)
                ),
                golfer.image
            )

        if current_state == GameState.CHARGING:
            power_height = int((golfer.power / golfer.max_power) * 50)
            for y in range(power_height):
                for x in range(5):
                    game_image.putpixel((20, 200 - y), (255, 0, 0))

        if (current_state == GameState.SHOWING_SCORE and
            game_objects['score_display_time'] > 0 and
            game_objects['shot_count'] in self.score_images):

            score_image = self.score_images[game_objects['shot_count']]
            if score_image:
                score_x = (self.width - score_image.width) // 2
                score_y = (self.height - score_image.height) // 2
                game_image.paste(score_image, (score_x, score_y), score_image)

        return game_image

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            if not self.update():
                if self.game_engine.state == GameState.SHOW_SCORECARD:
                    score_card_screen = ScoreCardScreen(self.display, self.input_handler, self.game_engine.score_card)
                    score_card_screen.run()
                running = False

            game_image = self.draw()
            self.display.show_image(game_image)

            if self.display.check_quit():
                running = False
                break

            clock.tick(60)