# src/platforms/input/base_input.py
from abc import ABC, abstractmethod

class BaseInput(ABC):
    @abstractmethod
    def get_input(self):
        """
        현재 입력 상태를 딕셔너리로 반환합니다.
        
        Returns:
            dict: 각 입력에 대한 상태 값을 가진 딕셔너리
            None: 종료 요청 시
        """
        pass
    
    @abstractmethod
    def wait_for_any_key(self):
        """
        아무 키 입력을 기다립니다.
        
        Returns:
            bool: 입력 성공 시 True, 종료 요청 시 False
        """
        pass