# src/platforms/input/keyboard_input.py
import pygame
from src.platforms.input.base_input import BaseInput

class KeyboardInput(BaseInput):
    def __init__(self):
        self.key_mapping = {
            pygame.K_w: 'up',
            pygame.K_s: 'down',
            pygame.K_a: 'left',
            pygame.K_d: 'right',
            pygame.K_SPACE: 'A',
            pygame.K_RETURN: 'B'
        }
        
    def get_input(self):
        """
        키보드의 현재 입력 상태를 반환합니다.
        
        Returns:
            dict: 각 키의 상태를 담은 딕셔너리
            None: 종료 요청 시
        """
        input_state = {
            'up': False, 'down': False,
            'left': False, 'right': False,
            'A': False, 'B': False
        }
        
        try:
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
            
            # 키 상태 확인
            keys = pygame.key.get_pressed()
            for key, action in self.key_mapping.items():
                if keys[key]:
                    input_state[action] = True
                    
            return input_state
            
        except pygame.error as e:
            print(f"키보드 입력 처리 중 오류: {e}")
            return None
    
    def wait_for_any_key(self):
        """
        아무 키나 눌릴 때까지 대기합니다.
        
        Returns:
            bool: 입력 성공 시 True, 종료 요청 시 False
        """
        try:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                        return True
                pygame.time.delay(10)
        except pygame.error as e:
            print(f"키 대기 중 오류: {e}")
            return False