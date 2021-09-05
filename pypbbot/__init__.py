import os
from pathlib import Path

from .logging import logger
from .server import app, run_server
__version__ = open(os.path.join(
    Path(__file__).parent, 'VERSION')).read().strip()
__all__ = ["app", "logger", "run_server"]
