import abc
import asyncio

from contextsingleton import ContextSingleton


class Prosumer(abc.ABC):
    """A Consumer and Producer pair"""
    tasks = set()

    def __init__(self, data, context: ContextSingleton.Context, name=''):
        self.data = data
        self.context = context
        self.logger = context.logger
        self.context.prosumers.add(self)
        self.name = name or f'prosumer{len(context.prosumers)}'

    async def produce(self):
        await self._produce()
        await asyncio.gather(*self.tasks)
        self.logger.debug('[%s] finished', self.name)
        self.context.prosumers.remove(self)

    @abc.abstractmethod
    async def consumer(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def _produce(self):
        """Implement producer logic here"""
        pass

    def add_task(self, args=None):
        t = self.context.loop.create_task(self.consumer(args))
        self.tasks.add(t)
