from typing import List

from source.config import JOINT_GAP_THRESHOLD
from source.constructors.row_constructor import RowConstructor
from source.domain import Panel, Joint, Point


class JointCalculator:
    def __init__(self, panels: List[Panel]):
        self.panels = panels

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
        Method to round Joint coordinates to N digits after coma
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
            if abs(joint.position.y - top_row[0].bottom) < JOINT_GAP_THRESHOLD # checking is it lower joints of top row panels
        ]

        bottom_row_top_joints = [
            joint for joint in bottom_row_joints
            if abs(joint.position.y - bottom_row[0].top) < JOINT_GAP_THRESHOLD # checking is it upper joins of bottom row panels
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


    def _deduplicate_joints(self, joints: List[Joint], digits: int = 2) -> List[Joint]:
        """
        Remove duplicated Joint objects by rounding coordinates to N decimal places.
        Returns a list of unique Joint instances.
        """
        unique = {}

        for joint in joints:
            key = self.rounded_coord(joint, digits)
            if key not in unique:
                unique[key] = Joint(
                    position=Point(key[0], key[1])
                )

        return list(unique.values())

    def calculate_joints(self) -> List[Joint]:
        """
        Collect all joint in one collection without duplicates. Returns list of Joint or empty list.
        """
        row_constructor = RowConstructor(self.panels)
        rows = row_constructor.group_panels_into_row()
        if not rows:
            return []

        all_joints: List[Joint] = []

        for row in rows:
            horizontal_joints = self._horizontal_joints_in_row(row)
            if horizontal_joints:
                all_joints.extend(horizontal_joints)

        for upper_row, lower_row in zip(rows, rows[1:]):
            shared_joints = self._shared_joints_between_rows(upper_row, lower_row)
            if shared_joints:
                all_joints.extend(shared_joints)

        return self._deduplicate_joints(all_joints)
