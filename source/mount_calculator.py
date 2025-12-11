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

    @staticmethod
    def deduplicate_mounts(mounts: List[Mount]) -> List[Mount]:
        """
        Delete duplicates from a list of mounts. Returns list with unique mounts.
        """
        if not mounts:
            return []

        unique_mounts = {}

        for mount in mounts:
            key = (round(mount.position.x, 2), round(mount.position.y, 2))
            if key not in unique_mounts:
                unique_mounts[key] = Mount(position=Point(key[0], key[1]))

        unique_sorted = sorted(unique_mounts.values(), key=lambda mt: (mt.position.x, mt.position.y))
        return unique_sorted