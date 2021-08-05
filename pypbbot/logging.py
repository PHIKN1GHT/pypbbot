import sys
import logging
from loguru import logger
from typing import cast
from types import FrameType

__all__ = ['LOG_CONFIG', 'logger']


def _init_loggers() -> None:
    logger.remove()
    logger.add(sys.stdout, colorize=True, diagnose=False,
               format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u><{name}></u></c>: {message}")


_init_loggers()

# Copied From https://github.com/nsidnev/fastapi-realworld-example-app


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "pypbbot.logging.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO"
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
        },
    },
}
