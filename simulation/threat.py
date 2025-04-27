from enum import Enum
from math import hypot

import numpy as np

from simulation.asset import Asset


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
    def __init__(self, type: ThreatE, p: float, speed: int, assets: Asset):
        self.type = type
        self.p = p
        self.speed = speed
        self.position = self.randomize_initial_position()
        self.closest_asset = self.get_closest_asset(assets)
        self.distance_to_asset = self.euclidean_distance(self.closest_asset.position, self.position)
        self.is_alive = True
        self.is_spotted = False
        
    def randomize_initial_position(self, min_distance = 3_000, max_distance = 10_000) -> tuple[int, int]:
        """
        Randomly generates x- and y-coordinates such that the initial position is at least
        5 km from the closest asset and no more than 15 km. Assume that all assets are within close
        proximity to the point (0,0).
        :return (tuple[int,int]): initial position of the threat
        """
        theta = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(min_distance**2, max_distance**2))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y
    
    def get_closest_asset(self, assets):
        closest_asset = min(
                assets,
                key=lambda asset: self.euclidean_distance(asset.position, self.position)
            )
        
        return closest_asset
    
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
        self.distance_to_asset = self.euclidean_distance(asset.position, self.position)
        
    def attack_asset(self) -> bool:
        """
        Draws a sample from a binomial distribution which results in the asset getting destroyed if result is True
        or a failed attack if result is False 
        :return (bool): True if asset was destroyed or False if attack was failed (drone miss/asset not destroyed)
        """
        if self.distance_to_asset <= 0 and self.is_alive:
            self.is_alive = False
            attack_result = bool(np.random.binomial(1, self.p))
            
            return attack_result
        
        return False
    
    def euclidean_distance(self, p1: tuple[float, float], p2: tuple[float, float]) -> float:
        """
        :return (float): the Euclidean distance between two (x, y) positions
        """
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        
        return hypot(dx, dy)
    