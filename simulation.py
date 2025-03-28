import numpy as np

from asset import Asset
from threat import Threat


class Simulation:
    """
    TODO: document
    """
    def __init__(self, asset: Asset, threats: list[Threat], dt: int = 10 ):
        self.dt = dt
        self.asset = asset
        self.threats = threats
    
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
        :return (int, bool): the value of the asset if the asset was destroyed and zero otherwise
        """
        while self.asset.is_alive:
            
            # if all threats are destroyed, return zero 
            if all([not t.is_alive for t in self.threats]):
                return 0
            
            for threat in self.threats:
                
                if not threat.is_alive:
                    continue
                
                # try to spot the threats
                for observer in self.asset.observers:
                    observer.spot(threat)
                    
                # if spotted - try to destroy the threats
                for effector in self.asset.effectors:
                    effector.effect(threat)
                    
                # try to destroy the asset
                if threat.attack_asset():
                    self.asset.is_alive = False
            
                # advance threats
                threat.update_position(self.asset, self.dt)
        
        return self.asset.value
            
    
    def simulate_n_attacks(self, n: int = 1_000_000) -> tuple[float, float]:
        """
        :return (float, float, float): return the average cost of assets destroyed in one attack,
            standard deviation of costs and frequency/probability of asset getting destroyed 
        """
        costs = []
        number_assets_destroyed = 0
        
        for _ in range(n):
            cost = self.simulate_one_attack()
            costs.append(cost)
            
            if cost > 0:
                number_assets_destroyed += 1
        
        return np.sum(costs) / n, np.std(costs), number_assets_destroyed / n 
    