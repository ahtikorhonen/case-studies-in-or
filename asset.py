from effector import Effector
from observer import Observer


class Asset:
    """
    TODO: document
    """
    def __init__(self, value: int, effectors: list, observers: list):
        self.value = value
        self.effectors = [Effector(**effector) for effector in effectors]
        self.observers = [Observer(**observer) for observer in observers]
        self.position = (0,0)
        self.is_alive = True
    
    @property    
    def total_value(self):
        effectors_value = sum([eff.value for eff in self.effectors])
        observers_value = sum([obs.value for obs in self.observers])
        
        return effectors_value + observers_value + self.value