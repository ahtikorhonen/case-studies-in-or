from threat import Threat


class Effector:
    def __init__(self, dist: list[float]):
        self.dist = dist
        
    def effect(self, threat: Threat):
        """
        Tries to destroy the threat by sampling from the dist attribute, which represents
        the discrete probability distribution of the threat getting destroyed as a function of
        distance to the asset.
        :return (None): returns None, in case the threat is destroyed the is_alive attribute of the threat is
                        changed to False
        """
        ...