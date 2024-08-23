import queue
import datetime

import _env
from extract import crawl_urls, crawl_function
from load import database
from transform import transform
from utils import utils, scheduler, thread


def init_logger(path_log):
    crawl_urls.init_logger(path_log)
    crawl_function.init_logger()
    database.init_logger(path_log)
    transform.init_logger(path_log)
    utils.init_logger(path_log)
    scheduler.init_logger(path_log)
    thread.init_logger(path_log)

def main():
    # khoi tao logger cho cac modul
    init_logger(_env.PATH_LOG_FILE_CRAWL_URL_RAW)

    # tao logger cho main
    logger = utils.config_log(_env.PATH_LOG_FILE_CRAWL_URL_RAW, _env.NAME_LOGGER_MODUL_MAIN, _env.LEVEL_LOG_MODUL_MAIN)
    logger.info("__________________________________Run Crawl URL raw")

    # tao queue luu task
    task_queue = queue.Queue()

    # read config crawl url
    crawl_urls_config = utils.read_config(_env.PATH_CONFIG_CRAWL_URLS)

    # ket noi database
    db = database.connect_db_mongodb(_env.DB_NAME)
    # ket noi collection
    col_urls = database.connect_col(db, _env.COL_URLS_RAW)

    # đẩy config vào trong queue
    for config in crawl_urls_config:
        task_queue.put(config)
    
    # sinh luồng
    executor = thread.init_threadpool(_env.NUMB_THREAD_FOR_CRAWL_URL)

    futures = []
    list_doc = []
    while not task_queue.empty():
        config = task_queue.get()
        # thread.task_handler(task, col_urls, task_queue)
        futures.append(executor.submit(crawl_urls.handler_crawl_url, config))

    # doi cac worker hoan thanh, xu ly ket qua cua tung worker
    for future in futures:
        try:
            # thu thap du lieu tu cac luong
            list_doc.extend(future.result())
        except Exception as e:
            logger.error(f"Task failed with exception: \n{e}")

    # tat executor, doi cac worker hoan thanh
    executor.shutdown(wait=True)

    # luu data vao db
    database.insert_many_col(col_urls, list_doc)

    logger.info("Task queue empty, task done")
