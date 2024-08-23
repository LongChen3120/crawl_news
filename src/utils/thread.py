import sys
sys.path.append("./src")

import threading
from concurrent.futures import ThreadPoolExecutor

from utils import _env, utils


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_THREAD, _env.LEVEL_LOG_MODUL_THREAD)

def init_threadpool(numb_thread):
    logger.info(f"Create thread pool {numb_thread} workers")
    return ThreadPoolExecutor(max_workers=numb_thread)

def get_thread_name():
    return threading.current_thread().getName()
