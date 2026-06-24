"""Centralized logging setup for the simulation."""

import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with a console handler."""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.handlers = [handler]
