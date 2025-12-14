from typing import List

from source.config import RAFTER_SPACING
from source.domain import Panel


class RafterGrid:
    def __init__(self, first_rafter: float = 0.0, spacing: float = RAFTER_SPACING):
        self.first_rafter = first_rafter
        self.spacing = spacing

    def generate_grid(self, panels: List[Panel]) -> list[float]:
        """
        Generate and returns X-coordinates of all rafters in the grid.
        Returns empty list if there are no Panels.

        Args:
            panels: List of Panels.

        Returns:
            List[float]: List of X-coordinates.
        """
        if not panels:
            return []

        min_x = panels[0].left
        max_x = panels[0].right

        for panel in panels:
            if panel.left < min_x:
                min_x = panel.left
            if panel.right > max_x:
                max_x = panel.right

        rafters_x_coordinates = []

        x = self.first_rafter

        while x + self.spacing < min_x:
            x += self.spacing

        while x <= max_x:
            rafters_x_coordinates.append(x)
            x += self.spacing

        return sorted(rafters_x_coordinates)
