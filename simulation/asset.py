from simulation.effector import Effector
from simulation.observer import Observer


class Asset:
    """
    TODO: document
    """
    def __init__(self, value: int, effectors: list, observers: list, visibility_coeff: float, position: tuple = (0,0)):
        self.value = value
        self.effectors = [Effector(visibility_coeff, **effector) for effector in effectors]
        self.observers = [Observer(visibility_coeff, **observer) for observer in observers]
        self.position = position
        self.is_alive = True
    
    @property    
    def total_value(self):
        effectors_value = sum([eff.value for eff in self.effectors])
        observers_value = sum([obs.value for obs in self.observers])
        
        return effectors_value + observers_value + self.value