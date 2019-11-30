import time
from collections import Counter


class Stats(Counter):
    """keep track of various stats"""
    start_time: float
    _end_time = None
    data_found = 0
    initial_data_count = 0

    def __init__(self, context) -> None:
        from contextsingleton import ContextSingleton
        self.context: ContextSingleton.Context = context
        super().__init__()

    @property
    def end_time(self):
        return self._end_time or time.time()

    def get_count_strings(self):
        string = str()
        for k, v in self.items():
            string += f'\t\t\t    {k} count: {v}\n'
            string += f'\t\t\t    {k} per second: {v / self.elapsed_time}\n'
        return string.rstrip()

    def get_stats_string(self):
        task_string = '\n' + '\n'.join(
            [f'\t\t\t    [{p.name}] tasks left: {len(p.tasks)}' for p in self.context.prosumers]
        )
        return ('\n\t\t\t    elapsed time: {time:.6f} secs'
                '\n\t\t\t    queue size: {queue}').format(
            time=self.elapsed_time,
            queue=self.context.data.queue.qsize()
        ) + task_string + self.get_count_strings()

    @property
    def elapsed_time(self):
        return self.end_time - self.start_time
