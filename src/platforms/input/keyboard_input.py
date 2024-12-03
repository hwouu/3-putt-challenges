import pygame

class KeyboardInput:
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
        input_state = {
            'up': False, 'down': False,
            'left': False, 'right': False,
            'A': False, 'B': False
        }
        
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
    
    def wait_for_any_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    return True
            pygame.time.delay(10)