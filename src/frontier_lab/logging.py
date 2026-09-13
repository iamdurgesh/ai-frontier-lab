"""Opt-in logging. Callers must never include credentials or submitted payloads."""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure console metadata without replacing application-owned handlers."""
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
