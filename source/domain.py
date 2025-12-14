from dataclasses import dataclass

from source.config import PANEL_WIDTH, PANEL_HEIGHT


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Mount:
    position: Point

    def __repr__(self) -> str:
        return f"Mount({self.position.x}, {self.position.y})"


@dataclass(frozen=True)
class Joint:
    position: Point

    def __repr__(self) -> str:
        return f"Joint({self.position.x, self.position.y})"


@dataclass(frozen=True)
class Panel:
    top_left: Point
    width: float = PANEL_WIDTH
    height: float = PANEL_HEIGHT

    @property
    def left(self):
        return self.top_left.x

    @property
    def right(self) -> float:
        return self.top_left.x + self.width

    @property
    def bottom(self) -> float:
        return self.top_left.y + self.height

    @property
    def top(self) -> float:
        return self.top_left.y
