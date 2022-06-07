"""Implements the representation of directional light"""

from light.light import Light

class DirectionalLight(Light):
    """Directional light"""
    def __init__(self, color=[1, 1, 1], direction=[0, -1, 0]):
        super().__init__(Light.DIRECTIONAL)
        self.color = color
        self.set_direction(direction)
