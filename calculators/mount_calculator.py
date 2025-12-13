from typing import List

from source.domain import Panel, Mount, Point
from source.services.mount_service import MountService


class MountCalculator:
    def __init__(self, rafters_x_coordinates: List[float]):
        self.mount_service = MountService(rafters_x_coordinates)

    def mounts_for_panel(self, panel: Panel) -> list[Mount]:
        """
        Return list of mounts coordinates for one panel
        """
        possible_mounts = self.mount_service.get_mounts_for_panel(panel)

        if not possible_mounts:
            raise ValueError("No rafters available for the panel")

        mounts: List[Mount] = []

        for x in possible_mounts:
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

    def collect_mounts_for_all_panels(self, panels: List[Panel], ignore_error: bool = True) -> List[Mount]:
        """
        Collect Mounts for all panels and return list of deduplicated, sorted by (x, y) and rounded by 2 decimals Mounts.
        if ignore_error is True, panels that cannot be mounted will be skipped and warning will be printed.
        If ignore_error is False, the ValueError will be raised in case of error.
        """
        if not panels:
            return []

        all_mounts: List[Mount] = []

        for panel in panels:
            try:
                panel_mounts = self.mounts_for_panel(panel)
            except ValueError as e:
                if not ignore_error:
                    raise
                print(f"Warning: skipping panel with coordinates {panel.top_left} due to: {e}")
                continue
            all_mounts.extend(panel_mounts)

        unique_mounts = self.deduplicate_mounts(all_mounts)

        return unique_mounts