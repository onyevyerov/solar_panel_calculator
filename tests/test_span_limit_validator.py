import pytest
from source.validators.span_limit_validator import SpanLimitValidator
from source.validators.span_limit_validator import SpanLimitValidatorError



@pytest.fixture
def span_validator():
    return SpanLimitValidator()

def test_maximum_allowed_span_is_valid(span_validator):
    mount_positions = [10.0, 58.0]

    span_validator.validate(mount_positions)


def test_smaller_than_max_span_is_valid(span_validator):
    mount_positions = [0.0, 16.0, 32.0]

    span_validator.validate(mount_positions)


def test_single_mount_in_segment_is_valid(span_validator):
    mount_positions = [20.0]

    span_validator.validate(mount_positions)

def test_span_just_exceeding_limit_raises_error(span_validator):
    mount_positions = [10.0, 58.01]

    with pytest.raises(SpanLimitValidatorError) as excinfo:
        span_validator.validate(mount_positions)

    assert "span limit" in str(excinfo.value). lower()
    assert "48.0" in str(excinfo.value)
