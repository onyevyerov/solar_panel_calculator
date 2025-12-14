import pytest
from source.domain import Panel, Point
from source.services.rafter_service import RafterGrid
from source.services.mount_service import MountService



@pytest.fixture
def global_rafter_grid():
    panels_for_grid = [Panel(top_left=Point(0.0, 0.0)), Panel(top_left=Point(100.0, 0.0))]
    return RafterGrid().generate_grid(panels_for_grid)

@pytest.fixture
def mount_service(global_rafter_grid):
    return MountService(global_rafter_grid)

def test_panel_mounts_filtering(mount_service):
    panel = Panel(top_left=Point(0.0, 0.0))
    expected_mounts_x = [16.0, 32.0]
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert actual_mounts_x == expected_mounts_x

def test_panel_mounts_filtering_offset(mount_service):
    panel = Panel(top_left=Point(5.0, 0.0))
    expected_mounts_x = [16.0, 32.0]
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert actual_mounts_x == expected_mounts_x

def test_rafter_position_satisfies_edge_clearance(mount_service):
    panel = Panel(top_left=Point(0.0, 0.0))
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert 0.0 not in actual_mounts_x
    assert 16.0 in actual_mounts_x

def test_no_mounts_possible(mount_service):
    small_panel = Panel(top_left=Point(10.0, 0.0), width=3.0, height=10.0)
    actual_mounts_x = mount_service.get_mounts_for_panel(small_panel)

    assert actual_mounts_x == []

def test_rafter_outside_panel_is_excluded(mount_service):
    panel = Panel(top_left=Point(0.0, 0.0))
    actual_mounts_x = mount_service.get_mounts_for_panel(panel)

    assert 48.0 not in actual_mounts_x

def test_segment_mount_aggregation(mount_service):
    segment = [
        Panel(top_left=Point(0.0, 0.0)),  # Mounts: 16.0, 32.0
        Panel(top_left=Point(45.05, 0.0))  # Mounts: 48.0, 64.0, 80.0
    ]

    expected_mounts_x = [16.0, 32.0, 48.0, 64.0, 80.0]
    actual_mounts_x = mount_service.get_mounts_for_segment(segment)

    assert actual_mounts_x == expected_mounts_x
