from typing import List, Set

from source.config import CANTILEVER_LIMIT
from source.domain import Panel



class CantileverValidatorError(ValueError):
    pass

class CantileverValidator:
    def __init__(
            self,
            cantilevers_limit: float = CANTILEVER_LIMIT,
    ):
        self.cantilevers_limit = cantilevers_limit

    def validate(self, segment: List[Panel], mounts: List[float]) -> None:
        if not segment:
            return

        start_of_segment = segment[0].left
        end_of_segment = segment[-1].right

        if not mounts:
            if (end_of_segment - start_of_segment) > CANTILEVER_LIMIT:
                raise CantileverValidatorError(
                    f"Cantilever exceeded: Segment {start_of_segment} to {end_of_segment}"
                    f" has no mounts, and full length is > {CANTILEVER_LIMIT}"
                )
            return

        first_mount = mounts[0]
        last_mount = mounts[-1]

        if first_mount - start_of_segment > CANTILEVER_LIMIT:
            raise CantileverValidatorError(
                f"Cantilever exceeded on the left side of segment: "
                f"{first_mount} - {start_of_segment} > {CANTILEVER_LIMIT}"
            )

        if end_of_segment - last_mount > CANTILEVER_LIMIT:
            raise CantileverValidatorError(
                f"Cantilever exceeded on the right side of segment: "
                f"{end_of_segment} - {last_mount} > {CANTILEVER_LIMIT}"
            )
