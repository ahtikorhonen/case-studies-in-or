from enum import Enum

import numpy as np

from asset import Asset


class ThreatE(Enum):
    FW = "FW"
    MC = "MC"

class Threat:
    """
    A base class for all threats/drones

    :type (Threat): type of drone
    :p (float): probability of destroying the asset on attack
    :speed (int): velocity of the drone in m/s
    :position (tuple[int, int]): position of the drone on the x, y plane
    :distance_to_asset (int): distance to the closest/target asset in meters
    :is_alive (bool): indicates whether the drone is functional
    :is_spotted (bool): indicates wheter the drone has been spotted by the asset
    """
    def __init__(self, type: ThreatE, p: float, speed: int, asset: Asset):
        self.type = type
        self.p = p
        self.speed = speed
        self.position = self.randomize_initial_position(asset)
        self.distance_to_asset = self.calculate_distance_to_asset(asset)
        self.is_alive = True
        self.is_spotted = False
        
    def randomize_initial_position(self, asset, min_distance = 3_000, max_distance = 10_000) -> tuple[int, int]:
        """
        Randomly generates x- and y-coordinates such that the initial position is at least
        5 km from the asset and no more than 20 km
        """
        theta = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(min_distance**2, max_distance**2))
        x_1, y_1 = asset.position
        x = x_1 + r * np.cos(theta)
        y = y_1 + r * np.sin(theta)
        
        return x, y
    
    def update_position(self, asset: Asset, dt: int) -> None:
        """
        Advances the threats position in the direction of the closest asset
        :asset (Asset): the closest asset to the threat
        :dt (int): time interval that passes in a single loop of the simulation
        """
        if self.distance_to_asset == 0:
            return
        
        traveled_distance = self.speed * dt
        distance = self.distance_to_asset
        
        if traveled_distance >= self.distance_to_asset:
            self.position = asset.position
        
        x_1, y_1 = asset.position
        x_2, y_2 = self.position
        dx = x_1 - x_2
        dy = y_1 - y_2
        unit_dx = dx / distance
        unit_dy = dy / distance
        
        new_x = x_2 + unit_dx * traveled_distance
        new_y = y_2 + unit_dy * traveled_distance
        
        self.position = (new_x, new_y)
        self.distance_to_asset = self.calculate_distance_to_asset(asset)
        #print(f"Threat: {self.type}, new pos: {new_x, new_y}, new dist: {self.distance_to_asset}")
    
    def calculate_distance_to_asset(self, asset: Asset) -> None:
        """
        TODO: document
        """
        x_1, y_1 = asset.position
        x_2, y_2 = self.position
        distance_to_asset = np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)
        
        return distance_to_asset
        
    def attack_asset(self) -> bool:
        """
        Draws a sample from a binomial distribution which results in the asset getting destroyed if result is True
        or a failed attack if result is False 
        :return (bool): True if asset was destroyed or False if attack was failed (drone miss/asset not destroyed)
        """
        if self.distance_to_asset <= 0 and self.is_alive:
            self.is_alive = False
            attack_result = bool(np.random.binomial(1, self.p))
            #print(f"type: {self.type}, result: {attack_result}")
            
            return attack_result
        
        return False
    