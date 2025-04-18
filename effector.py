import numpy as np


class Effector:
    def __init__(self, visibility_coeff: float, type: str, value: int, parameters: dict, night_mode: bool):
        self.type = type
        self.value = value
        self.parameters = parameters
        self.night_mode = night_mode
        
        assert (visibility_coeff > 0 and visibility_coeff <= 1), "visibility coefficent has to be between 0 and 1"
        self.visibility_coeff = visibility_coeff
        
    def get_p(self, threat) -> float:
        """
        Returns the probability of succesfully effecting on the threat
        as a function of distance to the asset/effector
        """
        a, b, c, xmin, xmax = self.parameters[threat.type.value].values()
        x = threat.distance_to_asset / 1_000
        
        if x <= xmin:
            p = 0.9
        elif x >= xmax:
            p = 0
        else:
            p = self.visibility_coeff * (a * x ** 2 + b * x + c)
            
            # this should not be used
            if p > 1:
                p = 0.9
            elif p < 0:
                p = 0
        
        return p
        
    def effect(self, threat, is_night_mode):
        """
        Tries to destroy the threat by sampling from the binomial attribute, which represents
        the probability of the threat getting destroyed as a function of distance to the asset.
        :return (bool): returns True, in case the threat is destroyed and the is_alive attribute of the threat is
                        changed to False. Returns False otherwise
        """
        # cant effect during night time
        if is_night_mode and not self.night_mode:
            return False
        
        if threat.is_spotted:
            p = self.get_p(threat)
            if bool(np.random.binomial(1, p)):
                threat.is_alive = False
                
                return True
            
        return False