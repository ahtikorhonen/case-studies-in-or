from collections import defaultdict
from math import hypot

import numpy as np


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
        while any([asset.is_alive for asset in self.assets]):
            
            # if all threats are destroyed, return value of destroyed assets 
            if all([not threat.is_alive for threat in self.threats]):
                return asset_value_destroyed, len([asset for asset in self.assets if not asset.is_alive])
            
            asset_value_destroyed += self.attack_loop()
                        
        return asset_value_destroyed, len([asset for asset in self.assets if not asset.is_alive])
    
    def attack_loop(self) -> float:
        asset_value_destroyed = 0
        alive_assets = [asset for asset in self.assets if asset.is_alive]
        alive_threats = [threat for threat in self.threats if threat.is_alive]
        self.map_to_closest(alive_assets, alive_threats)
            
        for asset in alive_assets:
            for threat in alive_threats:
                
                for effector in asset.effectors:
                    if threat is asset.closest_threat:
                        if effector.effect(threat, self.night_mode):
                            break
                
                for observer in asset.observers:
                    if observer.spot(threat, self.night_mode):
                        break
                
                if asset is threat.closest_asset:
                    if threat.attack_asset():
                        asset.is_alive = False
                        asset_value_destroyed += asset.total_value
                    
                    threat.update_position(self.dt)
                
        return asset_value_destroyed

    def reset_simulation(self):
        for asset in self.assets:
            asset.is_alive = True
        
        self.threats = self.generate_threats()
    
    def simulate_n_attacks(self, n: int = 1_000_000) -> tuple[float, float]:
        """
        :return (float, float, float): return the average cost of assets destroyed in one attack,
            standard deviation of costs and the average number of destroyed assets in a single attack
        """
        costs = []
        sum_of_assets_destroyed = 0
        
        for _ in range(n):
            cost, num_of_destroyed_assets = self.simulate_one_attack()
            costs.append(cost)
            
            sum_of_assets_destroyed += num_of_destroyed_assets
            
            self.reset_simulation()
                        
        return np.mean(costs), np.std(costs), sum_of_assets_destroyed / n

    def map_to_closest(
        self,
        assets: list,
        threats: list
    ):
        """
        Assigns the closest spotted and alive threat as the closest_threat attribute of the asset and
        assigns the closest alive asset as the closest_asset attribute of the threat.
        """
        # For each threat, find its nearest asset and assign it:
        for threat in threats:
            closest_asset = min(
                assets,
                key=lambda asset: self.euclidean_distance(asset.position, threat.position)
            )
            threat.closest_asset = closest_asset
        
        # for each asset, find its nearest spotted threat
        for asset in assets:
            spotted_threats = [threat for threat in threats if threat.is_spotted]
            if spotted_threats:
                closest_spotted_threat = min(
                    [threat for threat in threats if threat.is_spotted],
                    key=lambda threat: self.euclidean_distance(threat.position, asset.position)
                )
                asset.closest_threat = closest_spotted_threat
    
    def euclidean_distance(self, p1: tuple[float, float], p2: tuple[float, float]) -> float:
        """
        :return (float): the Euclidean distance between two (x, y) positions
        """
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        
        return hypot(dx, dy)
