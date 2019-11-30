import logging
from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING

import logzero

from settings import Settings
from stats import Stats

if TYPE_CHECKING:
    from datahandler import DataHandler


class ContextSingleton:
    """A singleton for easy-access to all important objects"""

    class _Context:
        stats = Stats()
        settings = Settings()
        logger: logging.Logger = logzero.logger
        running = True
        data: 'DataHandler'
        loop: AbstractEventLoop
        prosumers = set()

    _context = _Context()

    Context = _Context

    @classmethod
    def get(cls):
        return cls._context
