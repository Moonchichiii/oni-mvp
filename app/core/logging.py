from __future__ import annotations

import logging

log = logging.getLogger("oni")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s - %(message)s",
    )
