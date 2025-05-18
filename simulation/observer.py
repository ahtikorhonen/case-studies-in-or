import numpy as np

class Observer:
    def __init__(self, visibility_coeff: float, type: str, value: int, parameters: dict, night_mode: bool):
        self.type = type
        self.value = value * 10**3
        self.parameters = parameters
        self.night_mode = night_mode
        
        assert (visibility_coeff > 0 and visibility_coeff <= 1), "visibility coefficent has to be between 0 and 1"
        self.visibility_coeff = visibility_coeff
            
    def get_p(self, threat) -> float:
        """
        Returns the probability of succesfully spotting the threat
        as a function of distance to the asset/observer
        """
        a, b, c, xmin, xmax = self.parameters[threat.type.value].values()
        x = threat.distance_to_asset / 1_000
        
        if x <= xmin:
            p = 0.9
        elif x >= xmax:
            p = 0
        else:
            p = self.visibility_coeff * (a * x ** 2 + b * x + c)
            
            if p > 0.9:
                p = 0.9
            elif p < 0:
                p = 0
        
        return p
        
    def spot(self, threat, is_night_mode):
        """
        Tries to spot the threat by sampling from the dist attribute, which represents
        the discrete probability distribution of the threat getting spotted as a function of
        distance to the asset.
        :return (bool): returns True, in case the threat is spotted and the is_spotted attribute of the threat is
                        changed to true
        """
        # cant spot during night time
        if is_night_mode and not self.night_mode:
            return False
        
        p = self.get_p(threat)
        #print(f"observer type: {self.type}, sampled p-value: {p}, distance to asset: {threat.distance_to_asset}")
        if bool(np.random.binomial(1, p)):
            threat.is_spotted = True
            
            return True
        
        return False