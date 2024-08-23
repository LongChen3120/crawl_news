
import sys
import time
import datetime
sys.path.append("./src")

from utils import _env, utils


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_SCHEDULER, _env.LEVEL_LOG_MODUL_SCHEDULER)

def wait_before_task(thread_name, task):
    '''
    task = {
        'time_run': datetime.datetime(year, month, day, hour, minute, second, minisecond), 
        'config': {...}
    '''
    # hàm đợi 1 khoảng thời gian nếu chưa tới lịch chạy task, nếu tới rồi thì chạy luôn
    time_run = task["time_run"]
    now = datetime.datetime.now()

    if time_run < now:
        logger.info(f"{thread_name} None sleep")
    else:
        time_wait = (time_run - now).total_seconds()
        logger.info(f"{thread_name} Wait: {time_wait} seconds before run task crawl url {task['config']['url_crawl']}" )
        time.sleep(time_wait)