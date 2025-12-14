import pytest

from source.domain import Panel, Point
from source.services.rafter_service import RafterGrid


@pytest.fixture
def rafter_generator():
    """Fixture for the RafterGrid instance."""
    return RafterGrid()


def test_generate_grid_basic(rafter_generator):
    """Tests basic rafter generation starting from X=0.0.
    Verifies that rafters are generated in 16.0 unit increments up to the maximum panel extent.
    """
    panels = [
        Panel(top_left=Point(0.0, 0.0)),
        Panel(top_left=Point(45.05, 0.0)),
    ]
    expected_rafters = [0.0, 16.0, 32.0, 48.0, 64.0, 80.0]
    actual_rafters = rafter_generator.generate_grid(panels)

    assert expected_rafters == actual_rafters


def test_generate_grid_offset(rafter_generator):
    """Tests rafter generation when the panel input is offset from X=0.0.
    Verifies that the grid starts from 0.0 and covers the panel extent.
    Panel [5.0, 0.0] -> Grid should cover up to 49.7(5.0 + 44.7). Rafters: 0, 16, 32, 48.
    """
    panels = [Panel(top_left=Point(5.0, 0.0))]
    expected_rafters = [0.0, 16.0, 32.0, 48.0]
    actual_rafters = rafter_generator.generate_grid(panels)

    assert expected_rafters == actual_rafters


def test_generate_grid_empty_input(rafter_generator):
    """Tests that an empty list of panels returns an empty rafter grid."""
    panels = []
    expected_rafters = []
    actual_rafters = rafter_generator.generate_grid(panels)

    assert expected_rafters == actual_rafters
