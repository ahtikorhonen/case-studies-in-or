class Asset:
    """
    TODO: document
    """
    def __init__(self, value: int, effectors: list, observers: list, position: list[int]):
        self.value = value
        self.effectors = effectors
        self.observers = observers
        self.position = position
        self.is_alive = True