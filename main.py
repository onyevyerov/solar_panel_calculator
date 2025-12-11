from typing import List

from source.domain import Panel
from source.formatter import OutputFormatter
from source.joint_calculator import JointCalculator
from source.mount_calculator import MountCalculator
from source.rafter import RafterGrid


class SolarPanelCalculator:
    def __init__(self, panels: List[Panel]):
        self.panels = panels


    def calculate(self) -> dict:
        rafter = RafterGrid()
        all_rafters = rafter.generate_grid(self.panels)

        mount_calculator = MountCalculator(all_rafters)
        all_mounts = mount_calculator.collect_mounts_for_all_panels(self.panels)

        joint_calculator = JointCalculator(self.panels)
        all_joints = joint_calculator.calculate_joints()

        return {
            "mounts": OutputFormatter.mounts_to_list(all_mounts),
            "joints": OutputFormatter.joints_to_list(all_joints),
        }