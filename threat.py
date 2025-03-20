from enum import Enum

import numpy as np


class Threat(Enum):
    FPV = "FPV"
    CMC = "CMC"
    MMC = "MMC"

class Threat:
    """
    TODO: document
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
        position = np.random.randint(5_000, 10_000, 2)
        while np.sqrt(sum([cord**2 for cord in position])) < 5_000:
            position = np.random.randint(5_000, 10_000, 2)
        
        return position
        
    def attack_asset(self) -> bool:
        """
        Draws a sample from a binomial distribution which results in the asset getting destroyed if result is True
        or a failed attack if result is False 
        :return (bool): True if asset was destroyed or False if attack was failed (drone miss/asset not destroyed)
        """
        if self.dist <= 0:
            return bool(np.random.binomial(1, self.prob))

if __name__ == "__main__":
    print(np.random.randint(5_000, 10_000, 2))