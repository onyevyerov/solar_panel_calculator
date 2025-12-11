from typing import List

from source.config import JOINT_GAP_THRESHOLD
from source.domain import Panel


class JointCalculator:
    def __init__(self, panels: List[Panel]):
        self.panels = panels

    def _group_panels_into_row(self) -> List[List[Panel]]:
        if not self.panels:
            return []

        sorted_panels = sorted(self.panels, key=lambda p: p.top) # sorting panels by Y

        rows: List[List[Panel]] = []
        current_row: List[Panel] = [sorted_panels[0]]

        for panel in sorted_panels[1::]:
            if abs(panel.top - current_row[0].top) <= JOINT_GAP_THRESHOLD:
                current_row.append(panel)
            else:
                current_row.sort(key=lambda p: p.left) # sorting panels by X before adding them to row
                rows.append(current_row)
                current_row = [panel]

        current_row.sort(key=lambda p: p.left) # sorting panels by X in last row
        rows.append(current_row)

        return rows