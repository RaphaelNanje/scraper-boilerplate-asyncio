import abc
from abc import abstractmethod

from contextsingleton import ContextSingleton


class Prosumer(metaclass=abc.ABCMeta):
    tasks = set()
    max_concurrent = 10

    def __init__(self, data, context: ContextSingleton.Context):
        self.data = data
        self.context = context
        self.logger = context.logger

    async def do(self):
        """start the produce or consume process"""
        if isinstance(self, Producer):
            await self.produce()
        if isinstance(self, Consumer):
            await self.consume()

    @property
    @abstractmethod
    def name(self):
        pass

    def append(self, n=1):
        """increment the count of whatever this prosumer is processing"""
        self.context.stats[self] += n

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Producer(Prosumer, metaclass=abc.ABCMeta):
    """A Consumer and Producer pair"""

    @abc.abstractmethod
    async def produce(self):
        pass

    @abc.abstractmethod
    async def _produce(self, *args):
        """Implement producer logic here"""
        pass

    def add_task(self, args=None):
        t = self.context.loop.create_task(self._produce(args))
        self.tasks.add(t)


class Consumer(Prosumer, metaclass=abc.ABCMeta):
    """A Consumer and Producer pair"""

    @abc.abstractmethod
    async def consume(self):
        pass

    @abc.abstractmethod
    async def _consume(self, *args):
        """Implement producer logic here"""
        pass

    def add_task(self, args=None):
        t = self.context.loop.create_task(self._consume(args))
        self.tasks.add(t)
