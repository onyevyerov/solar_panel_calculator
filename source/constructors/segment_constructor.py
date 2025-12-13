from typing import List

from source.config import CONTINUOUS_GAP
from source.constructors.row_constructor import RowConstructor
from source.domain import Panel


class SegmentConstructor:
    def __init__(self, panels: List[Panel]):
        self.panels = panels


    def divide_rows_into_segments(self) -> List[List[Panel]]:
        """
        Divide rows into segments.
        A segment consists of panels whose distance between adjacent panels does not exceed CONTINUOUS_GAP.

        Returns:
            List[List[Panel]]: List of segments with Panels -> [Segment[Panel]]
        """
        if not self.panels:
            return []

        row_constructor = RowConstructor(self.panels)
        rows = row_constructor.group_panels_into_row()

        segments: List[List[Panel]] = []

        for row in rows:
            current_segment = [row[0]]

            for panel_a, panel_b in zip(row, row[1:]):
                gap = panel_b.left - panel_a.right

                if abs(gap) < CONTINUOUS_GAP:
                    current_segment.append(panel_b)
                else:
                    segments.append(current_segment)
                    current_segment = [panel_b]

            segments.append(current_segment)

        return segments
