from typing import List, Set

from source.config import EDGE_CLEARANCE
from source.domain import Panel


class MountService:
    def __init__(self, mounts_x_coordinates: List[float]):
        self.mounts_x_coordinates = sorted(float(x) for x in mounts_x_coordinates)

    def get_mounts_for_panel(self, panel: Panel):
        min_allowed_x = panel.left + EDGE_CLEARANCE
        max_allowed_x = panel.right - EDGE_CLEARANCE

        mounts = [
            x for x in self.mounts_x_coordinates
            # checking if the rafter not closer than 2 units(EDGE_CLEARANCE) to the edge of panel
            if min_allowed_x <= x <= max_allowed_x
        ]

        return sorted(mounts)

    def get_mounts_for_segment(self, segment: List[Panel]) -> List[float]:
        mounts: Set[float]= set()

        for panel in segment:
            panel_mounts_x = self.get_mounts_for_panel(panel)
            mounts.update(panel_mounts_x)

        return sorted(mounts)
