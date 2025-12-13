from typing import Iterable, List

from source.domain import Mount, Joint


class OutputFormatter:
    """Convert domain objects(Mount, Joint) to primitive JSON-friendly structures."""

    @staticmethod
    def mount_to_dict(mount: Mount) -> dict:
        """
        Converts a Mount object to a dictionary with rounded 'x' and 'y' coordinates.
        """
        return {"x": round(mount.position.x, 2), "y": round(mount.position.y, 2)}

    @staticmethod
    def joint_to_dict(joint: Joint) -> dict:
        """
        Converts a Joint object to a dictionary with rounded 'x' and 'y' coordinates.
        """
        return {"x": round(joint.position.x, 2), "y": round(joint.position.y, 2)}

    @staticmethod
    def mounts_to_list(mounts: Iterable[Mount]) -> List[dict]:
        """
        Converts an iterable of Mount objects into a list of dictionaries.
        """
        return [OutputFormatter.mount_to_dict(m) for m in mounts]

    @staticmethod
    def joints_to_list(joints: Iterable[Joint]) -> List[dict]:
        """
        Converts an iterable of Joint objects into a list of dictionaries.
        """
        return [OutputFormatter.joint_to_dict(j) for j in joints]