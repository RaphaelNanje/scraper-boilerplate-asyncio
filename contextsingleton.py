import logging
from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING, Set

import logzero

from settings import Settings
from stats import Stats

if TYPE_CHECKING:
    from datahandler import DataHandler
    from prosumer import Prosumer


class ContextSingleton:
    """A singleton for easy-access to all important objects"""

    class _Context:
        settings = Settings()
        logger: logging.Logger = logzero.logger
        running = True
        data: 'DataHandler'
        loop: AbstractEventLoop
        prosumers: 'Set[Prosumer]' = set()

        def __init__(self) -> None:
            self.stats = Stats(self)

    _context: _Context = None

    Context = _Context

    @classmethod
    def get(cls) -> _Context:
        if cls._context:
            return cls._context
        cls._context = cls._Context()
        return cls._context
