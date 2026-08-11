from pathlib import Path

from .load_config import assign_environmental_to_variables
from .load_config import global_constants

__all__ = [
    "assign_environmental_to_variables",
    "global_constants",
]

BASE_DIR = Path(__file__).resolve().parent.parent