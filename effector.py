import numpy as np

from threat import Threat


class Effector:
    def __init__(self, dist: list[float]):
        self.dist = dist # [[5000, 0], [3000, 0.1], [2000, 0.2], ...]
        
    def get_prob(self, threat_dist) -> float:
        for dist, prob in self.dist:
            if dist >= threat_dist:
                return prob
        
        return 0
        
    def effect(self, threat: Threat):
        """
        Tries to destroy the threat by sampling from the dist attribute, which represents
        the discrete probability distribution of the threat getting destroyed as a function of
        distance to the asset.
        :return (None): returns None, in case the threat is destroyed the is_alive attribute of the threat is
                        changed to False
        """
        if threat.is_spotted:
            destruction_prob = self.get_prob(threat.dist)
            if np.random.rand() < destruction_prob:
                threat.is_alive = False