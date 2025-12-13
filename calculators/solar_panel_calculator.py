from typing import List

from source.constructors.segment_constructor import SegmentConstructor
from source.domain import Panel
from source.formatter import OutputFormatter
from calculators.joint_calculator import JointCalculator
from calculators.mount_calculator import MountCalculator
from source.services.rafter_service import RafterGrid
from source.validators.cantilever_validator import CantileverValidator
from source.validators.span_limit_validator import SpanLimitValidator


class SolarPanelCalculator:
    def __init__(self, panels: List[Panel]):
        self.panels = panels

    def calculate(self) -> dict:
        """
        Compute mounts and joints for the current panel layout.

        Returns:
            dict: JSON-ready structure with unique mount points and joint points
            (each rounded to two decimals).
        """
        rafters = RafterGrid().generate_grid(self.panels)

        segments = SegmentConstructor(self.panels).group_rows_into_segments()

        mount_calculator = MountCalculator(rafters)

        for segment in segments:
            mounts_x = mount_calculator.mount_service.get_mounts_for_segment(segment)

            CantileverValidator().validate(segment, mounts_x)
            for panel in segment:
                panel_mounts_x = mount_calculator.mount_service.get_mounts_for_panel(panel)
                SpanLimitValidator().validate(panel_mounts_x)

        all_mounts = mount_calculator.collect_mounts_for_all_panels(self.panels)

        joint_calculator = JointCalculator(self.panels)
        all_joints = joint_calculator.calculate_joints()

        return {
            "mounts": OutputFormatter.mounts_to_list(all_mounts),
            "joints": OutputFormatter.joints_to_list(all_joints),
        }
