import asyncio
# regex here
import signal
import time

import click as click

from contextsingleton import ContextSingleton
from datahandler import DataHandler
from example import PrintNumbersProsumer
from utilities import my_handler

context = ContextSingleton.get()
context.data = DataHandler()
logger = context.logger


# scraper settings here


async def start():
    p = PrintNumbersProsumer(10, context)
    # async with aiohttp.ClientSession() as session:
    await asyncio.gather(
        context.loop.create_task(p.produce())
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
