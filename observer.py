import numpy as np

class Observer:
    def __init__(self, type: str, value: int, parameters: dict):
        self.type = type
        self.value = value
        self.parameters = parameters
            
    def get_p(self, threat) -> float:
        """
        Returns the probability of succesfully spotting the threat
        as a function of distance to the asset/observer
        """
        a, b, c, xmin, xmax = self.parameters[threat.type].values()
        x = threat.distance_to_asset / 1_000
        
        if x <= xmin:
            p = 0.9
        elif x >= xmax:
            p = 0
        else:
            p = a * x ** 2 + b * x + c
            
            if p > 1:
                p = 0.9
            elif p < 0:
                p = 0
        
        return p
        
    def spot(self, threat):
        """
        Tries to spot the threat by sampling from the dist attribute, which represents
        the discrete probability distribution of the threat getting spotted as a function of
        distance to the asset.
        :return (None): returns None, in case the threat is spotted the is_spotted attribute of the threat is
                        changed to true
        """
        p = self.get_p(threat)
        if bool(np.random.binomial(1, p)):
            threat.is_spotted = True