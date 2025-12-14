import json
from typing import List

from source.calculators.solar_panel_calculator import SolarPanelCalculator
from source.domain import Panel, Point


def load_panels_from_file(path: str) -> List[Panel]:
    """
    Load Panel data from a JSON file and return Panel objects.

    Args:
        path (str): Path to a JSON file containing a list of Panel data.

    Returns:
        list[Panel]: List of panels -> [Panel(x, y)].
    """
    with open(path, "r") as f:
        data = json.load(f)

    return [Panel(top_left=Point(p["x"], p["y"])) for p in data["panels"]]


def main() -> None:
    """
    Loads panels from file, runs the solar panel calculator, and prints results.

    Returns:
        JSON: {
            'mounts': [],
            'joints': []
        }
    """
    panels = load_panels_from_file("examples/sample_input.json")
    result = SolarPanelCalculator(panels).calculate()

    print(result)


if __name__ == "__main__":
    main()
