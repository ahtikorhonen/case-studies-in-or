import numpy as np

from threat import Threat


class Observer:
    def __init__(self, dist: list[float]):
        self.dist = dist
        
    def get_prob(self, threat_dist) -> float:
        for dist, prob in self.dist:
            if dist >= threat_dist:
                return prob
        
        return 0
        
    def spot(self, threat: Threat) -> None:
        """
        Tries to spot the threat by sampling from the dist attribute, which represents
        the discrete probability distribution of the threat getting spotted as a function of
        distance to the asset.
        :return (None): returns None, in case the threat is spotted the is_spotted attribute of the threat is
                        changed to true
        """
        spotting_prob = self.get_prob(threat.dist)
        if np.random.rand() < spotting_prob:
            threat.is_spotted = True