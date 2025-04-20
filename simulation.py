from collections import defaultdict

import numpy as np

from sim_utils import euclidean_distance


class Simulation:
    """
    TODO: document
    """
    def __init__(self, assets: list, threats: list, generate_threats, dt: int = 10, night_mode = False):
        self.dt = dt
        self.assets = assets
        self.threats = threats
        self.night_mode = night_mode
        self.generate_threats = generate_threats
        
    def simulate_one_attack(self) -> tuple[int, bool]:
        """
        :return (int, bool): the value of the asset if the asset was destroyed and zero otherwise
        """
        asset_value_destroyed = 0
        while all([asset.is_alive for asset in self.assets]):
            
            # if all threats are destroyed, return value of destroyed assets 
            if all([not threat.is_alive for threat in self.threats]):
                return asset_value_destroyed
            
            asset_value_destroyed += self.attack_loop()
                        
        return asset_value_destroyed
    
    def attack_loop(self) -> float:
        asset_value_destroyed = 0
        alive_assets = [asset for asset in self.assets if asset.is_alive]
        alive_threats = [threat for threat in self.threats if threat.is_alive]
        mapping = self.group_by_closest(alive_assets, alive_threats)
        
        for asset, threats in mapping.items():
            for threat in threats:
                for observer in asset.observers:
                    observer.spot(threat, self.night_mode)
                    
                for effector in asset.effectors:
                    if effector.effect(threat, self.night_mode):
                        break
                    
                if threat.attack_asset():
                    asset.is_alive = False
                    asset_value_destroyed += asset.total_value
            
                threat.update_position(asset, self.dt)
        
        return asset_value_destroyed

    def reset_simulation(self):
        for asset in self.assets:
            asset.is_alive = True
        
        self.threats = self.generate_threats()
    
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

    def group_by_closest(
        self,
        assets: list,
        threats: list
    ) -> dict:
        """
        For each asset in assets, build a dict containing:
        - the asset itself as key
        - all threats for which the asset is the nearest neighbor among all assets.
        
        """
        mapping = defaultdict(list)
        
        # For each threat, find its nearest asset and assign it:
        for threat in threats:
            closest_asset = min(
                assets,
                key=lambda asset: euclidean_distance(asset.position, threat.position)
            )
            mapping[closest_asset].append(threat)
            threat.closest_asset = closest_asset
        
        return mapping
