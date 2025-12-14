import pytest

from source.domain import Panel, Point
from source.services.rafter_service import RafterGrid

@pytest.fixture
def rafter_generator():
    return RafterGrid()

def test_generate_grid_basic(rafter_generator):
    panels = [
        Panel(top_left=Point(0.0, 0.0)),
        Panel(top_left=Point(45.05, 0.0)),
    ]
    expected_rafters = [0.0, 16.0, 32.0, 48.0, 64.0, 80.0]
    actual_rafters = rafter_generator.generate_grid(panels)

    assert expected_rafters == actual_rafters

def test_generate_grid_offset(rafter_generator):
    panels = [Panel(top_left=Point(5.0, 0.0))]
    expected_rafters = [0.0, 16.0, 32.0, 48.0]
    actual_rafters = rafter_generator.generate_grid(panels)

    assert expected_rafters == actual_rafters

def test_generate_grid_empty_input(rafter_generator):
    panels = []
    expected_rafters = []
    actual_rafters = rafter_generator.generate_grid(panels)

    assert expected_rafters == actual_rafters
