from PIL import Image
import os

class StartScreen:
    def __init__(self, display, input_handler):
        self.display = display
        self.input_handler = input_handler
        self.width = 240
        self.height = 240
        
    def draw(self):
        # 에셋 경로 설정
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(current_dir, 'assets', 'images', 'start_screen.png')
        
        # 이미지 로드 및 리사이즈
        try:
            image = Image.open(image_path)
            # 디스플레이 크기에 맞게 리사이즈
            image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error loading start screen image: {e}")
            # 이미지 로드 실패시 단색 배경으로 대체
            image = Image.new("RGB", (self.width, self.height), (135, 206, 235))
        
        return image

    def run(self):
        """시작 화면을 실행하고 사용자 입력을 기다립니다."""
        start_image = self.draw()
        self.display.show_image(start_image)
        return self.input_handler.wait_for_any_key()