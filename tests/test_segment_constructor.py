import pytest
from source.constructors.segment_constructor import SegmentConstructor
from source.domain import Panel, Point
from typing import List



def create_panel(x: float, y: float) -> Panel:
    return Panel(top_left=Point(x, y))

def test_single_row_single_segment_required():
    panels = [
        create_panel(0.0, 0.0),
        create_panel(45.05, 0.0),
        create_panel(90.1, 0.0),
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 1
    assert len(actual_segments[0]) == 3
    assert actual_segments[0][0].top_left.x == 0.0
    assert actual_segments[0][2].top_left.x == 90.1


def test_single_row_multiple_segments():
    panels = [
        create_panel(0.0, 0.0),  # Segment 1
        create_panel(46.0, 0.0)  # Segment 2
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 2
    assert len(actual_segments[0]) == 1
    assert actual_segments[0][0].top_left.x == 0.0
    assert actual_segments[1][0].top_left.x == 46.0


def test_mixed_segmentation():
    panels = [
        create_panel(0.0, 0.0),  # Segment 1: panel 1
        create_panel(45.05, 0.0),  # Segment 1: panel 2
        create_panel(91.0, 0.0),  # Segment 2: panel 1
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 2
    assert len(actual_segments[0]) == 2
    assert len(actual_segments[1]) == 1
    assert actual_segments[0][0].top_left.x == 0.0
    assert actual_segments[1][0].top_left.x == 91.0


def test_multiple_rows_separate_segments():
    panels = [
        create_panel(0.0, 0.0),  # Segment 1 (Row 1)
        create_panel(0.0, 71.6)  # Segment 2 (Row 2)
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 2

    assert actual_segments[0][0].top_left.y == 0.0
    assert actual_segments[1][0].top_left.y == 71.6


def test_empty_input():
    panels = []

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert actual_segments == []


def test_single_panel_input():
    panels = [create_panel(10.0, 10.0)]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 1
    assert len(actual_segments[0]) == 1
    assert actual_segments[0][0].top_left.x == 10.0
