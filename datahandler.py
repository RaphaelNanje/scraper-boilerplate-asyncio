import asyncio
import os
import time
from threading import Thread

from contextsingleton import ContextSingleton

context = ContextSingleton.get()
logger = context.logger


class DataHandler:
    queue = asyncio.Queue()
    data = set()

    def __init__(self):
        save_t = Thread(target=auto_save_thread, name='SaveThread')
        stat_t = Thread(target=stats_thread, name='StatsThread')
        save_t.start()
        stat_t.start()

    def initialize(self):
        logger.info('initializing...')

        if os.path.exists(context.settings.DATA_FILE):
            logger.info('loading existing data...')
            with open(context.settings.DATA_FILE) as f:
                self.data.update([f.strip() for f in f.readlines()])
                context.stats.initial_numbers = len(self.data)

    def save(self):
        with open(context.settings.DATA_FILE, 'w') as f:
            logger.debug('saving data -> %s', context.settings.DATA_FILE)
            f.write('\n'.join(self.data))


def auto_save_thread():
    logger.debug('save thread starting.')
    while context.running:
        time.sleep(context.settings.auto_save_interval)
        if not context.running:
            break
        logger.debug('autosaving...')
        context.data.save()


def stats_thread():
    while context.running:
        time.sleep(context.settings.debug_stats_interval)
        if not context.running:
            break
        logger.debug(context.stats.get_stats_string())
