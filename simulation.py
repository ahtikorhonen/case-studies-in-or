import numpy as np

from asset import Asset
from sim_utils import sample_poisson_threats


class Simulation:
    """
    TODO: document
    """
    def __init__(self, asset: Asset, threats: list, generate_threats, dt: int = 10, night_mode = False):
        self.dt = dt
        self.asset = asset
        self.threats = threats
        self.night_mode = night_mode
        self.generate_threats = generate_threats
        
    def simulate_one_attack(self) -> tuple[int, bool]:
        """
        :return (int, bool): the value of the asset if the asset was destroyed and zero otherwise
        """
        while self.asset.is_alive:
            
            # if all threats are destroyed, return zero 
            if all([not threat.is_alive for threat in self.threats]):
                return 0
            
            for threat in self.threats:
                
                if not threat.is_alive:
                    continue
                
                for observer in self.asset.observers:
                    observer.spot(threat, self.night_mode)
                    
                for effector in self.asset.effectors:
                    if effector.effect(threat, self.night_mode):
                        break
                    
                if threat.attack_asset():
                    self.asset.is_alive = False
            
                threat.update_position(self.asset, self.dt)
                        
        return self.asset.total_value
    
    def reset_simulation(self):
        self.asset.is_alive = True
        
        if self.generate_threats:
            self.threats = self.generate_threats()
            
        for threat in self.threats:
            threat.is_alive = True
            threat.is_spotted = False
            threat.position = threat.randomize_initial_position(self.asset)
            threat.distance_to_asset = threat.calculate_distance_to_asset(self.asset)
    
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
            
            self.reset_simulation()
                        
        return np.sum(costs) / n, np.std(costs), number_assets_destroyed / n 