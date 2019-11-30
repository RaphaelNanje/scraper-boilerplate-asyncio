import asyncio


def my_handler(_, _2):
    print('Cancelling all tasks, this may take a moment...')
    global go
    go = False
    for task in asyncio.all_tasks():
        task.cancel()
