# src/platforms/input/base_input.py
from abc import ABC, abstractmethod

class BaseInput(ABC):
    @abstractmethod
    def get_input(self):
        """Returns a dictionary of current input states"""
        pass
    
    @abstractmethod
    def wait_for_any_key(self):
        """Waits for any input and returns True when received"""
        pass


