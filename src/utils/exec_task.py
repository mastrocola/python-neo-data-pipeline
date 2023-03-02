from time import time
from src.services.logger import Log


def exec_task(task_function):
    start_time = time()

    try:
        task_function()
    except BaseException as error:  # pylint: disable=broad-except
        Log().error(f'{task_function.__name__.upper()}_ETL_TASK_ERROR', f'Error on generate {task_function.__module__}', error)
    else:
        Log().info(f'{task_function.__name__.upper()}_ETL_TASK_FINISH', f'Finished {task_function.__module__} table generation. Elapsed time: {time() - start_time}')
