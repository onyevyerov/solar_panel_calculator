from typing import List

from source.config import JOINT_GAP_THRESHOLD
from source.domain import Panel, Joint, Point


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

    def _horizontal_joints_in_row(self, row: List[Panel]) -> List[Joint]:
        if not row:
            return []

        joints: List[Joint] = []

        for a, b in zip(row, row[1:]):
            gap = b.left - a.right
            if abs(gap) < JOINT_GAP_THRESHOLD:
                joint_x = round((a.right + b.left) / 2, 2)
                joints.append(Joint(position=Point(joint_x, round(a.top, 2))))
                joints.append(Joint(position=Point(joint_x, round(a.bottom, 2))))

        return joints

    @staticmethod
    def rounded_coord(joint: Joint, digits=2):
        """
        Method to round Joint coordinates to 2 digits after coma
        """
        return (
            round(joint.position.x, digits),
            round(joint.position.y, digits)
        )

    def _shared_joints_between_rows(self, top_row: List[Panel], bottom_row: List[Panel]) -> List[Joint]:
        if not top_row or not bottom_row:
            return []

        if abs(top_row[0].bottom - bottom_row[0].top) >= JOINT_GAP_THRESHOLD:
            return []

        top_row_joints = self._horizontal_joints_in_row(top_row)
        bottom_row_joints = self._horizontal_joints_in_row(bottom_row)

        top_row_bottom_joints = [
            joint for joint in top_row_joints
            if abs(joint.position.y - top_row[0].bottom) < JOINT_GAP_THRESHOLD
        ]

        bottom_row_top_joints = [
            joint for joint in bottom_row_joints
            if abs(joint.position.y - bottom_row[0].top) < JOINT_GAP_THRESHOLD
        ]

        shared_joints: List[Joint] = []
        result = set()

        for joint_t in top_row_bottom_joints:
            for joint_b in bottom_row_top_joints:
                if round(joint_t.position.x, 2) == round(joint_b.position.x, 2):
                    shared_x = round((joint_t.position.x + joint_b.position.x) / 2, 2)
                    shared_y = round((joint_t.position.y + joint_b.position.y) / 2, 2)
                    shared_joint = (shared_x, shared_y)
                    if shared_joint not in result:
                        result.add(shared_joint)
                        shared_joints.append(Joint(position=Point(shared_x, shared_y)))

        return shared_joints
