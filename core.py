import asyncio
# regex here
import signal
import time

import click as click

from contextsingleton import ContextSingleton
from datahandler import DataHandler
from example import PrintNumbersProducer
from example2 import ConcurrencyMaxProducer
from utilities import my_handler, gather_prosumer

context = ContextSingleton.get()
context.data = DataHandler()
logger = context.logger


# scraper settings here


async def start():
    """all tasks here will run until completion"""

    for i in range(1000):
        await context.data.queue.put(i)
    await context.data.queue.put(None)
    await gather_prosumer(
        PrintNumbersProducer(10, context),
        ConcurrencyMaxProducer(context=context)
    )


@click.command()
@click.option('-s', '--save-interval', default=context.settings.auto_save_interval,
              help='How often in seconds to save DEFAULT=10', type=float)
def core(save_interval):
    try:
        if save_interval:
            context.settings.auto_save_interval = save_interval
    except Exception as e:
        exit('Please check your parameters.')
        logger.exception(e)
    context.data.initialize()
    logger.info('Starting {}...'.format(context.settings.TITLE))
    context.stats.start_time = time.time()

    try:
        context.loop.run_until_complete(start())
        context.stats._end_time = time.time()
        logger.info('All tasks have completed!')
    except asyncio.CancelledError:
        print('All tasks have been canceled')
    except Exception as e:
        logger.exception(e)
    finally:
        context.running = False
        context.data.save()
        logger.info(context.stats.get_stats_string())
        context.loop.close()
        logger.info('Closing...')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    context.loop = loop
    signal.signal(signal.SIGINT, my_handler)
    signal.signal(signal.SIGTERM, my_handler)
    core()
