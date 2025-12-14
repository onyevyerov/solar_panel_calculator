import pytest
from source.validators.cantilever_validator import CantileverValidator
from source.validators.cantilever_validator import CantileverValidatorError
from source.domain import Panel, Point
from typing import List


@pytest.fixture
def cantilever_validator():
    return CantileverValidator()


def create_segment(start_x: float, end_x: float) -> List[Panel]:
    return [Panel(top_left=Point(start_x, 0.0), width=end_x - start_x, height=10.0)]


def test_cantilever_at_max_limit_is_valid(cantilever_validator):
    """Tests success when the left and right cantilevers are EXACTLY at the limit (16.0)."""
    segment = create_segment(start_x=10.0, end_x=60.0)
    mount_positions = [26.0, 44.0]  # 26.0 - 10.0 = 16.0 / 60.0 - 44.0 = 16.0

    cantilever_validator.validate(segment, mount_positions)


def test_small_cantilever_is_valid(cantilever_validator):
    """Tests success when the left and right edge clearance are EXACTLY at the limit (2.0)."""
    segment = create_segment(start_x=0.0, end_x=50.0)
    mount_positions = [2.0, 48.0]

    cantilever_validator.validate(segment, mount_positions)


def test_left_cantilever_just_over_limit_fails(cantilever_validator):
    """Verifies that a left cantilever JUST exceeding the limit (16.01) raises an error."""
    segment = create_segment(start_x=0.0, end_x=50.0)
    mount_positions = [16.01, 33.0]

    with pytest.raises(CantileverValidatorError) as excinfo:
        cantilever_validator.validate(segment, mount_positions)

    assert "Cantilever exceeded on the left side of segment" in str(excinfo.value)
    assert "16.01" in str(excinfo.value)


def test_right_cantilever_just_over_limit_fails(cantilever_validator):
    """Verifies that a right cantilever JUST exceeding the limit (33.99) raises an error."""
    segment = create_segment(start_x=0.0, end_x=50.0)
    mount_positions = [16.0, 33.99]

    with pytest.raises(CantileverValidatorError) as excinfo:
        cantilever_validator.validate(segment, mount_positions)

    assert "Cantilever exceeded on the right side of segment" in str(excinfo.value)
    assert "50.0 - 33.99" in str(excinfo.value)


def test_no_mounts_in_large_segment_fails(cantilever_validator):
    """Verifies that no mounts in a large segment (Cantilever 100.0 > 16.0) raises an error."""
    segment = create_segment(start_x=0.0, end_x=100.0)
    mount_positions = []

    with pytest.raises(CantileverValidatorError):
        cantilever_validator.validate(segment, mount_positions)
