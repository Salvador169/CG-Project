"""Implements the representation of ambient light"""

from light.light import Light

class AmbientLight(Light):
    """Ambient light"""
    def __init__(self, color = [1, 1, 1]):
        super().__init__(Light.AMBIENT)
        self.color = color
