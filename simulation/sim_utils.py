import itertools

import numpy as np

from simulation.threat import Threat, ThreatE


def get_combinations(data: dict):
    """
    Gives all the possible combinations of effectors and observers
    :data (dict): contains the possible objects in the combinations
    :return (list): two lists containing all non-empty combinations (subsets) of the observers and effectors.
    """
    effectors = data.get("effectors", [])
    observers = data.get("observers", [])
    
    return list(itertools.product(observers, effectors))

def sample_poisson_threats(drone_specs: dict, lambdas: dict):
    threats = []
    
    for drone_type, lam in lambdas.items():
        count = np.random.poisson(lam)
        spec = next(filter(lambda d: d["type"] == drone_type, drone_specs))
        
        for _ in range(count):
            threats.append(Threat(ThreatE[drone_type], spec["p"], spec["speed"]))
            
    return threats