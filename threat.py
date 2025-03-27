from enum import Enum

import numpy as np

from asset import Asset


class Threat(Enum):
    FPV = "FPV"
    CMC = "CMC"
    MMC = "MMC"

class Threat:
    """
    A base class for all threats i.e
    """
    def __init__(self, type: Threat, prob: list[tuple], dist: list[float], range: int, speed: int):
        self.type = type
        self.prob = prob
        self.dist = dist
        self.range = range
        self.speed = speed
        self.position = self.randomize_initial_position()
        self.is_alive = True
        self.is_spotted = False
        
    def randomize_initial_position(self) -> tuple[int, int]:
        """
        Randomly generates x- and y-coordinates such that the initial position is at least
        5 km from the asset
        """
        position = np.random.randint(-10_000, 10_000, 2)
        while np.sqrt(sum([coord**2 for coord in position])) < 5_000:
            position = np.random.randint(5_000, 10_000, 2)
        
        return position
    
    def update_position(self, asset: Asset, dt: int) -> None:
        """
        Advances the threats position in the direction of the closest asset
        :asset (Asset): the closest asset to the threat
        :dt (int): time interval that passes in a single loop of the simulation
        """
        pass
    
    def calculate_distance_to_asset(self, asset: Asset) -> None:
        pass
        
    def attack_asset(self) -> bool:
        """
        Draws a sample from a binomial distribution which results in the asset getting destroyed if result is True
        or a failed attack if result is False 
        :return (bool): True if asset was destroyed or False if attack was failed (drone miss/asset not destroyed)
        """
        if self.dist and self.is_alive <= 0:
            self.is_alive = False
            
            return bool(np.random.binomial(1, self.prob))
        
        return False
    