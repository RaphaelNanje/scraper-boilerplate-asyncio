import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from prosumer import Prosumer


def my_handler(_, _2):
    print('Cancelling all tasks, this may take a moment...')
    for task in asyncio.all_tasks():
        task.cancel()


async def gather_prosumer(*objects: 'Prosumer'):
    tasks = set()
    from prosumer import Prosumer
    for obj in objects:
        assert isinstance(obj, Prosumer)
        t = asyncio.create_task(obj.run())
        tasks.add(t)
    await asyncio.gather(*tasks)
