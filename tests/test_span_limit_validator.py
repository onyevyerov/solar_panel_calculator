import pytest
from source.validators.span_limit_validator import SpanLimitValidator
from source.validators.span_limit_validator import SpanLimitValidatorError



@pytest.fixture
def span_validator():
    """Fixture for the SpanLimitValidator instance."""
    return SpanLimitValidator()

def test_maximum_allowed_span_is_valid(span_validator):
    """Tests success when the span is EXACTLY equal to the maximum limit (48.0)."""
    mount_positions = [10.0, 58.0] # 58.0 - 10.0 = 48.0

    span_validator.validate(mount_positions)


def test_smaller_than_max_span_is_valid(span_validator):
    """Tests success when spans are significantly smaller than the limit (16.0)."""
    mount_positions = [0.0, 16.0, 32.0]

    span_validator.validate(mount_positions)


def test_single_mount_in_segment_is_valid(span_validator):
    """Tests success when the segment has only one mount (no span to measure)."""
    mount_positions = [20.0]

    span_validator.validate(mount_positions)

def test_span_just_exceeding_limit_raises_error(span_validator):
    """Verifies that a span just over the limit (48.01) raises a SpanLimitValidatorError."""
    mount_positions = [10.0, 58.01] # 58.01 - 10.0 = 48.1 > 48.0

    with pytest.raises(SpanLimitValidatorError) as excinfo:
        span_validator.validate(mount_positions)

    assert "span limit" in str(excinfo.value). lower()
    assert "48.0" in str(excinfo.value)
