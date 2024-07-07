"""
A basic logger for the project.
"""

import logging
import sys

logger = logging.getLogger("simple_english_project")
logger.setLevel(logging.DEBUG if "DEBUG" in sys.argv else logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if "DEBUG" in sys.argv else logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] (%(levelname)s) %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
