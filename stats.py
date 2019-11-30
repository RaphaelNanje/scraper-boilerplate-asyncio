import time


class Stats:
    """keep track of various stats"""
    start_time: float
    data_found = 0
    initial_data_count = 0

    def get_stats_string(self):
        from contextsingleton import ContextSingleton

        context = ContextSingleton.get()
        elapsed_time = time.time() - self.start_time
        task_string = '\n' + '\n'.join(
            [f'\t\t\t    [{p.name}] tasks left: {len(p.tasks)}' for p in context.prosumers]
        )
        return ('\n\t\t\t    elapsed time: {time:.6f} secs'
                '\n\t\t\t    speed: {speed:.2f} listings scraped per second'
                '\n\t\t\t    queue size: {queue}').format(
            speed=self.data_found / elapsed_time,
            time=elapsed_time,
            queue=context.data.queue.qsize()
        ) + task_string
