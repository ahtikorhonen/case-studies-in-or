import numpy as np

from asset import Asset
from threat import Threat


class Simulation:
    """
    TODO: document
    """
    def __init__(self, asset: Asset, threats: list[Threat]):
        self.asset = asset
        self.threats = threats
        
    def __initialisize_simulation(self):
        ...
    
    def num_of_drones(self, drone_type: str) -> int:
        """
        Samples the number of a specific drone type in a single attack on the asset
        :drone_type (str): name of the drone type
        :return (int): the sampled number of drones
        """
        try:
            dist = self.threats[drone_type]["dist"]
            range = self.threats[drone_type]["range"]
            
            return np.random.choice(range, p=dist)
        
        except Exception as ex:
            raise (f"Failed to sample number of drones - {str(ex)}")
        
    def simulate_one_attack(self) -> tuple[int, bool]:
        """
        :return (int, bool): the value of the asset and True if the asset was destroyed, zero and False otherwise
        """
        pass
    
    def simulate_n_attacks(self, n: int = 1_000_000) -> tuple[float, float]:
        """
        :return (float, float, float): return the average cost of assets destroyed in one attack,
            standard deviation of costs and frequency/probability of asset getting destroyed 
        """
        pass
    