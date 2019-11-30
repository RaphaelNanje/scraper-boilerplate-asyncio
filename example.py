import asyncio
import random

from prosumer import Producer


class PrintNumbersProducer(Producer):
    """print numbers asynchronously"""

    def __init__(self, data: int, context):
        super().__init__(data, context)

    async def produce(self):
        self.logger.debug('%s producer starting...', self.name)
        for i in range(self.data):
            self.add_task(i)
        await asyncio.gather(*self.tasks)
        self.logger.debug('[%s] finished', self.name)
        self.context.prosumers.remove(self)

    async def _produce(self, number):
        sleep_time = random.randint(1, 3)
        await asyncio.sleep(sleep_time)
        self.logger.info(number)
        self.append()

    @property
    def name(self):
        return 'print_number'
