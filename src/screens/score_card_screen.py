from PIL import Image, ImageDraw, ImageFont

class ScoreCardScreen:
    def __init__(self, display, input_handler, score_card):
        self.display = display
        self.input_handler = input_handler
        self.score_card = score_card
        self.width = 240
        self.height = 240
        self._load_assets()
        
    def _load_assets(self):
        try:
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            self.small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except IOError:
            self.font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()

    def draw(self):
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 타이틀
        draw.rectangle([0, 0, self.width, 40], fill=(0, 100, 0))
        draw.text((20, 10), "SCORECARD", font=self.font, fill=(255, 255, 255))
        
        # 헤더
        y = 50
        headers = ["Hole", "Par", "Score", "+/-"]
        x_positions = [20, 80, 140, 190]
        for header, x in zip(headers, x_positions):
            draw.text((x, y), header, font=self.small_font, fill=(0, 0, 0))
        
        # 각 홀 스코어
        y = 80
        for hole in range(1, 4):
            result = self.score_card.get_course_result(hole)
            if result is not None:
                draw.text((20, y), f"{hole}", font=self.font, fill=(0, 0, 0))
                draw.text((80, y), f"{self.score_card.pars[hole]}", font=self.font, fill=(0, 0, 0))
                draw.text((140, y), f"{self.score_card.scores[hole]}", font=self.font, fill=(0, 0, 0))
                
                # 스코어 차이를 색상으로 표시
                color = (0, 150, 0) if result < 0 else (150, 0, 0) if result > 0 else (0, 0, 0)
                draw.text((190, y), f"{result:+d}", font=self.font, fill=color)
            y += 40
        
        # 총점
        draw.line([10, y, 230, y], fill=(0, 0, 0), width=2)
        y += 20
        total = self.score_card.get_total_score()
        par_total = self.score_card.get_total_par()
        total_diff = total - par_total
        
        draw.text((20, y), "Total", font=self.font, fill=(0, 0, 0))
        draw.text((80, y), f"{par_total}", font=self.font, fill=(0, 0, 0))
        draw.text((140, y), f"{total}", font=self.font, fill=(0, 0, 0))
        color = (0, 150, 0) if total_diff < 0 else (150, 0, 0) if total_diff > 0 else (0, 0, 0)
        draw.text((190, y), f"{total_diff:+d}", font=self.font, fill=color)
        
        return image
      
    def run(self):
      while True:
          inputs = self.input_handler.get_input()
          if inputs is None or inputs['A'] or inputs['B']:
              return True
              
          score_card_image = self.draw()
          self.display.show_image(score_card_image)