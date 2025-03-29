import numpy as np


class Effector:
    def __init__(self, type: str, value: int, parameters: dict):
        self.type = type
        self.value = value
        self.parameters = parameters
        
    def get_p(self, threat) -> float:
        """
        Returns the probability of succesfully effecting on the threat
        as a function of distance to the asset/effector
        """
        a, b, c, xmin, xmax = self.parameters[threat.type].values()
        x = threat.distance_to_asset / 1_000
        
        if x <= xmin:
            p = 0.9
        elif x >= xmax:
            p = 0
        else:
            p = a * x ** 2 + b * x + c
        
        return p
        
    def effect(self, threat):
        """
        Tries to destroy the threat by sampling from the binomial attribute, which represents
        the probability of the threat getting destroyed as a function of distance to the asset.
        :return (None): returns None, in case the threat is destroyed the is_alive attribute of the threat is
                        changed to False
        """
        if threat.is_spotted:
            p = self.get_p(threat)
            if bool(np.random.binomial(1, p)):
                threat.is_alive = False