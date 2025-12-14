from source.constructors.segment_constructor import SegmentConstructor
from source.domain import Panel, Point
from typing import List


def create_panel(x: float, y: float) -> Panel:
    """Helper to create a Panel instance with default size."""
    return Panel(top_left=Point(x, y))


def test_single_row_single_segment_required():
    """Tests that a single row with small gaps (0.35 and 0.05) is grouped into one segment.
    P1 (0.0) -> P2 (45.05): Gap 0.35 (<= 1.0) -> Grouped.
    P2 (45.05) -> P3 (90.1): Gap 0.35 (<= 1.0) -> Grouped."""
    panels = [
        create_panel(0.0, 0.0),
        create_panel(45.05, 0.0),  # gap 0.35
        create_panel(90.1, 0.0),  # gap 0,35
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 1
    assert len(actual_segments[0]) == 3
    assert actual_segments[0][0].top_left.x == 0.0
    assert actual_segments[0][2].top_left.x == 90.1


def test_single_row_multiple_segments():
    """Tests that a row with a large gap is split into two separate segments.
    P1 (0.0) -> P2 (46.0): Gap 1.3 (> 1.0) -> SPLIT."""
    panels = [create_panel(0.0, 0.0), create_panel(46.0, 0.0)]  # gap 1.3  # segment 2

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 2
    assert len(actual_segments[0]) == 1
    assert actual_segments[0][0].top_left.x == 0.0
    assert actual_segments[1][0].top_left.x == 46.0


def test_mixed_segmentation():
    """Tests a row where the first gap is small (grouped) and the second gap is large (split).
    P1 (0.0) -> P2 (45.05): Gap 0.35 (Grouped).
    P2 (45.05) -> P3 (91.0): Gap 1.25 (Split)."""
    panels = [
        create_panel(0.0, 0.0),  # Segment 1: panel 1
        create_panel(45.05, 0.0),  # Segment 1: panel 2
        create_panel(91.0, 0.0),  # gap 1.25 -> Segment 2: panel 1
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 2
    assert len(actual_segments[0]) == 2
    assert len(actual_segments[1]) == 1
    assert actual_segments[0][0].top_left.x == 0.0
    assert actual_segments[1][0].top_left.x == 91.0


def test_multiple_rows_separate_segments():
    """Tests that panels in different vertical rows are correctly treated as separate segments."""
    panels = [
        create_panel(0.0, 0.0),  # Segment 1 (Row 1)
        create_panel(0.0, 71.6),  # Segment 2 (Row 2)
    ]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 2

    assert actual_segments[0][0].top_left.y == 0.0
    assert actual_segments[1][0].top_left.y == 71.6


def test_empty_input():
    """Tests that an empty input list returns an empty list of segments."""
    panels = []

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert actual_segments == []


def test_single_panel_input():
    """Tests that a single input panel results in exactly one segment containing that panel."""
    panels = [create_panel(10.0, 10.0)]

    constructor = SegmentConstructor(panels)
    actual_segments: List[List[Panel]] = constructor.divide_rows_into_segments()

    assert len(actual_segments) == 1
    assert len(actual_segments[0]) == 1
    assert actual_segments[0][0].top_left.x == 10.0
