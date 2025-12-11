from typing import List

from source.config import EDGE_CLEARANCE, CANTILEVER_LIMIT, SPAN_LIMIT
from source.domain import Panel, Mount, Point


class MountCalculator:
    def __init__(self, rafters_x_coordinates: List[float]):
        self.rafters_x_coordinates = rafters_x_coordinates

    def mounts_for_panel(self, panel: Panel) -> list[Mount]:
        """
        Return list of mounts coordinates for one panel
        """
        allowed_min_x = panel.left + EDGE_CLEARANCE
        allowed_max_x = panel.right - EDGE_CLEARANCE

        possible_rafters = [
            x for x in self.rafters_x_coordinates
            if allowed_min_x <= x <= allowed_max_x
        ]

        if not possible_rafters:
            raise ValueError("No rafters available for the panel")

        first_x = possible_rafters[0]
        last_x = possible_rafters[-1]

        if first_x - panel.left > CANTILEVER_LIMIT:
            raise ValueError("Cantilever limit exceeded on left side of panel")

        if panel.right - last_x > CANTILEVER_LIMIT:
            raise ValueError("Cantilever limit exceeded on right side of panel")

        for a, b in zip(possible_rafters, possible_rafters[1:]):
            if b - a > SPAN_LIMIT:
                raise ValueError("Span limit exceeded between mounts")

        mounts: List[Mount] = []

        for x in possible_rafters:
            mounts.append(Mount(position=Point(x, panel.top)))
            mounts.append(Mount(position=Point(x, panel.bottom)))

        return mounts