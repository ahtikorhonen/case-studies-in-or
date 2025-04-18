import itertools

import numpy as np

from threat import Threat, ThreatE


def get_combinations(data: dict):
    """
    Gives all the possible combinations of effectors and observers
    :data (dict): contains the possible objects in the combinations
    :return (list): two lists containing all non-empty combinations (subsets) of the observers and effectors.
    """
    effectors = data.get("effectors", [])
    observers = data.get("observers", [])
    
    return list(itertools.product(observers, effectors))

def sample_poisson_threats(asset, drone_specs: dict, lambdas: dict):
    threats = []
    
    for drone_type, lam in lambdas.items():
        count = np.random.poisson(lam)
        spec = next(filter(lambda d: d["type"] == drone_type, drone_specs))
        
        for _ in range(count):
            threats.append(Threat(ThreatE[drone_type], spec["p"], spec["speed"], asset))
            
    return threats

def num_of_drones(drone_type: str, threats) -> int:
    """
    Samples the number of a specific drone type in a single attack on the asset
    :drone_type (str): name of the drone type
    :return (int): the sampled number of drones
    """
    try:
        dist = threats[drone_type]["dist"]
        range = threats[drone_type]["range"]
        
        return np.random.choice(range, p=dist)

    except Exception as ex:
        raise (f"Failed to sample number of drones - {str(ex)}")