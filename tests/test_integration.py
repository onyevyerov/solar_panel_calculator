import pytest

from source.calculators.solar_panel_calculator import SolarPanelCalculator
from source.domain import Panel, Point

MINIMAL_PANELS_INPUT = [
    {"x": 0, "y": 0},  # P1 (Row 1)
    {"x": 45.05, "y": 0},  # P2 (Row 1)
    {"x": 0, "y": 71.6},  # P3 (Row 2)
    {"x": 45.05, "y": 71.6},  # P4 (Row 2)
]


@pytest.fixture
def minimal_panels():
    """Returns a list of Panel objects from the minimal input configuration."""
    return [Panel(top_left=Point(p["x"], p["y"])) for p in MINIMAL_PANELS_INPUT]


def test_full_calculation_with_minimal_data(minimal_panels):
    """Tests the full end-to-end calculation flow for a minimal, valid two-row configuration.

    Verifies:
    -No critical exceptions are raised during calculation.
    -Correct Mount positions are found and included (respecting Edge Clearance).
    -Correct Horizontal Joints are found (where gap < 1.0).
    -Correct Shared Joints are found (vertical alignment).
    -Incorrect joints (where gap > 1.0) are correctly excluded."""
    calculator = SolarPanelCalculator(minimal_panels)

    try:
        result = calculator.calculate()
    except Exception as e:
        pytest.fail(f"Calculation failed with a critical business logic error: {e}")

    mounts = result["mounts"]
    joints = result["joints"]

    # Panel_1
    expected_mount_1 = {"x": 16.0, "y": 0.0}  # Top
    expected_mount_2 = {"x": 16.0, "y": 71.1}  # Bottom
    expected_mount_3 = {"x": 32.0, "y": 0.0}  # Top
    expected_mount_4 = {"x": 32.0, "y": 71.1}  # Bottom

    # Panel_2
    expected_mount_5 = {"x": 64.0, "y": 71.1}  # Bottom
    expected_mount_6 = {"x": 64.0, "y": 0.0}  # Top
    expected_mount_7 = {"x": 80.0, "y": 71.1}  # Bottom
    expected_mount_8 = {"x": 80.0, "y": 0.0}  # Top

    assert expected_mount_1 in mounts, "Missing Mount at X=16.0 Y=0.0 on P1 (Top)"
    assert expected_mount_2 in mounts, "Missing Mount at X=16.0 Y=71.1 on P1 (Bottom)"
    assert expected_mount_3 in mounts, "Missing Mount at X=32.0 Y=0.0 on P1 (Top)"
    assert expected_mount_4 in mounts, "Missing Mount at X=32.0 Y=71.1 on P1 (Bottom)"
    assert expected_mount_5 in mounts, "Missing Mount at X=64.0 Y=0.0 on P2 (Top)"
    assert expected_mount_6 in mounts, "Missing Mount at X=64.0 Y=71.1 on P2 (Bottom)"
    assert expected_mount_7 in mounts, "Missing Mount at X=80.0 Y=0.0 on P2 (Top)"
    assert expected_mount_8 in mounts, "Missing Mount at X=80.0 Y=71.1 on P2 (Bottom)"

    # Panel_2 (X=45.05): Rafters 48.0, 64.0, 80.0. Checking Edge Clearance.
    expected_mount_3 = {"x": 80.0, "y": 71.1}
    expected_mount_4 = {"x": 48.0, "y": 0.0}
    expected_mount_5 = {"x": 80.0, "y": 0.0}

    assert expected_mount_3 in mounts, "Missing Mount at X=80.0 on P2"
    assert expected_mount_4 in mounts, "Missing Mount at X=80.0 on P2"
    assert expected_mount_5 in mounts, "Missing Mount at X=80.0 on P2"

    expected_joint_horiz_top = {"x": 44.88, "y": 0.0}
    expected_joint_horiz_bottom = {"x": 44.88, "y": 71.1}

    assert expected_joint_horiz_top in joints, "Missing Horizontal Joint (P1-P2, Top)"
    assert (
        expected_joint_horiz_bottom in joints
    ), "Missing Horizontal Joint (P1-P2, Bottom)"

    # Missing Horizontal Joint (between P2 and P3): Gap 1.25.
    # Checks that the Joint point (X=90.38) is missing (or excluded).
    joint_not_expected = {"x": 90.38, "y": 0.0}
    assert joint_not_expected not in joints, "Joint found where gap > 1.0 (P2-P3)"

    # Shared joint(P2 and P4): X=44.88. Vert Gap 0.5. Y=71.35
    expected_joint_shared = {"x": 44.88, "y": 71.35}
    assert expected_joint_shared in joints, "Missing Shared Joint (P2-P4)"

    # Checking length
    assert len(joints) >= 5, "Incorrect number of unique joints found"
