import pytest
from source.domain import Panel, Point
from source.services.rafter_service import RafterGrid
from source.services.mount_service import MountService


@pytest.fixture
def global_rafter_grid():
    """Generates a common Rafter Grid for the tests."""
    panels_for_grid = [
        Panel(top_left=Point(0.0, 0.0)),
        Panel(top_left=Point(100.0, 0.0)),
    ]
    return RafterGrid().generate_grid(panels_for_grid)


@pytest.fixture
def mount_service(global_rafter_grid):
    """Fixture for the MountService instance, initialized with the global grid."""
    return MountService(global_rafter_grid)


def test_panel_mounts_filtering(mount_service):
    """Verifies that mounts are correctly filtered by Edge Clearance (2.0) and panel width (44.7)."""
    panel = Panel(top_left=Point(0.0, 0.0))
    expected_mounts_x = [16.0, 32.0]
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert actual_mounts_x == expected_mounts_x


def test_panel_mounts_filtering_offset(mount_service):
    """Verifies filtering works when the panel is offset."""
    panel = Panel(top_left=Point(5.0, 0.0))
    expected_mounts_x = [16.0, 32.0]
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert actual_mounts_x == expected_mounts_x


def test_rafter_position_satisfies_edge_clearance(mount_service):
    """Verifies that mounts at the panel edges (0.0 and 44.7) are excluded due to Edge Clearance (2.0).
    Rafter 0.0 should be excluded, 16.0 should be included."""
    panel = Panel(top_left=Point(0.0, 0.0))
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert 0.0 not in actual_mounts_x
    assert 16.0 in actual_mounts_x


def test_no_mounts_possible(mount_service):
    """Verifies that an empty list is returned for a panel too small (3.0 units wide) to satisfy Edge Clearance."""
    small_panel = Panel(top_left=Point(10.0, 0.0), width=3.0, height=10.0)
    actual_mounts_x = mount_service.get_mounts_for_panel(small_panel)

    assert actual_mounts_x == []


def test_rafter_outside_panel_is_excluded(mount_service):
    """Verifies that rafters falling outside the panel boundaries are correctly excluded."""
    panel = Panel(top_left=Point(0.0, 0.0))
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert 48.0 not in actual_mounts_x


def test_segment_mount_aggregation(mount_service):
    """Verifies that the MountService correctly aggregates and deduplicates mounts for all panels within a segment."""
    segment = [
        Panel(top_left=Point(0.0, 0.0)),  # Mounts: 16.0, 32.0
        Panel(top_left=Point(45.05, 0.0)),  # Mounts: 48.0, 64.0, 80.0
    ]

    expected_mounts_x = [16.0, 32.0, 48.0, 64.0, 80.0]
    actual_mounts_x = mount_service.get_mounts_for_segment(segment)

    assert actual_mounts_x == expected_mounts_x
