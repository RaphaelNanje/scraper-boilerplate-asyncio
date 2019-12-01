import asyncio
import random

from prosumer import Prosumer


class ConcurrencyMaxProducer(Prosumer):
    """print numbers asynchronously"""

    def __init__(self, data=None, context=None):
        super().__init__(data, context)

    async def produce(self):
        self.logger.debug('%s starting...', self.name)
        while self.context.running:
            if len(self.tasks) >= self.max_concurrent:
                self.logger.debug('pausing %s tasks until current %s tasks complete', self.name, self.name)
                # Wait for some tasks to finish before adding a new one
                _done, self.tasks = await asyncio.wait(
                    self.tasks, return_when=asyncio.FIRST_COMPLETED)

            item = await self.context.data.queue.get()
            if item is None:
                break
            self.add_task(item)

        await asyncio.gather(*self.tasks)
        self.logger.debug('[%s] finished', self.name)
        self.context.prosumers.remove(self)

    async def fill_queue(self):
        for i in range(1, self.data):
            await self.queue.put(i)

    async def work(self, number):
        sleep_time = random.randint(1, 10)
        await asyncio.sleep(sleep_time)
        self.logger.info(number)
        self.append()

    @property
    def name(self):
        return 'concurrent_prints'
