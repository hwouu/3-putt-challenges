from digitalio import DigitalInOut, Direction, Pull
from adafruit_rgb_display import st7789
import board

class Joystick:
    def __init__(self):
        # 디스플레이 핀 설정
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        # 디스플레이 초기화
        self.spi = board.SPI()
        self.disp = st7789.ST7789(
            self.spi,
            height=240,
            y_offset=80,
            rotation=180,
            cs=self.cs_pin,
            dc=self.dc_pin,
            rst=self.reset_pin,
            baudrate=self.BAUDRATE,
        )

        # 조이스틱 버튼 설정 - 풀업 저항 추가
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT
        self.button_A.pull = Pull.UP

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT
        self.button_B.pull = Pull.UP

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT
        self.button_L.pull = Pull.UP

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT
        self.button_R.pull = Pull.UP

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT
        self.button_U.pull = Pull.UP

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT
        self.button_D.pull = Pull.UP

        # 백라이트 설정
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # 버튼 상태 저장용 딕셔너리
        self.button_states = {
            'A': False, 'B': False,
            'up': False, 'down': False,
            'left': False, 'right': False
        }

    def init_display(self):
        """디스플레이 초기화"""
        self.disp.fill(0)

    def get_button_states(self):
        """
        모든 버튼의 현재 상태를 반환합니다.
        풀업 저항이 적용되어 있으므로, 버튼이 눌리면 False를 반환합니다.
        """
        return {
            'A': self.button_A.value,
            'B': self.button_B.value,
            'up': self.button_U.value,
            'down': self.button_D.value,
            'left': self.button_L.value,
            'right': self.button_R.value
        }