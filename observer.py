from threat import Threat


class Observe:
    def __init__(self, dist: list[float]):
        self.dist = dist
        
    def spot(self, threat: Threat) -> None:
        """
        Tries to spot the threat by sampling from the dist attribute, which represents
        the discrete probability distribution of the threat getting spotted as a function of
        distance to the asset.
        :return (None): returns None, in case the threat is spotted the is_spotted attribute of the threat is
                        changed to true
        """
        ...