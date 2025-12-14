from typing import List

from source.config import SPAN_LIMIT


class SpanLimitValidatorError(Exception):
    pass


class SpanLimitValidator:
    def __init__(self, span_limit: float = SPAN_LIMIT):
        self.span_limit = span_limit

    def validate(self, mounts: List[float]) -> None:
        for mount_a, mount_b in zip(mounts, mounts[1:]):
            if mount_b - mount_a > self.span_limit:
                raise SpanLimitValidatorError(
                    f"Span limit exceeded: {mount_b} - {mount_a} > {self.span_limit}"
                )
