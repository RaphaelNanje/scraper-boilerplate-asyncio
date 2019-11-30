import asyncio
import random

from prosumer import Prosumer


class PrintNumbersProsumer(Prosumer):
    """print numbers asynchronously"""

    def __init__(self, data: int, context):
        super().__init__(data, context)

    async def _produce(self):
        self.logger.debug('PrintNumbersProsumer starting...')
        for i in range(self.data):
            self.add_task(i)

    async def consumer(self, number):
        sleep_time = random.randint(1, 3)
        await asyncio.sleep(sleep_time)
        self.logger.info(number)
