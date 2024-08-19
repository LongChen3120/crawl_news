
import queue
import datetime
import logging

import _env, utils, thread, crawl, database, scheduler, transform


def init_logger(path_log):
    crawl.init_logger(path_log)
    database.init_logger(path_log)
    scheduler.init_logger(path_log)
    thread.init_logger(path_log)
    transform.init_logger(path_log)
    utils.init_logger(path_log)

def crawl_url_raw():
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
    db = database.connect_db_mongodb(_env.MONGODB_SERVER, _env.DB_NAME)
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
        futures.append(executor.submit(crawl.crawl_url_raw, config))

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

def crawl_detail_news():
    # khoi tao logger cho cac module
    init_logger(_env.PATH_LOG_FILE_CRAWL_DETAIL_NEWS)

    # tao logger cho main
    logger = utils.config_log(_env.PATH_LOG_FILE_CRAWL_DETAIL_NEWS, _env.NAME_LOGGER_MODUL_MAIN, _env.LEVEL_LOG_MODUL_MAIN)
    logger.info("__________________________________Run Crawl detail news")

    # read config crawl url
    crawl_detail_config = utils.read_config(_env.PATH_CONFIG_CRAWL_DETAIL)

    # ket noi database
    db = database.connect_db_mongodb(_env.MONGODB_SERVER, _env.DB_NAME)
    # ket noi collection
    col_urls = database.connect_col(db, _env.COL_URLS_CLEAN)
    col_detail = database.connect_col(db, _env.COL_DETAIL)
    for config in crawl_detail_config:
        # lay cac url can crawl(numb_crawl_detail == 0)
        query = _env.QUERY_FIND_URL_CRAWL_NUMB_CRAWL_0
        query["url_crawl"] = config["url_crawl"]

        list_obj_url = database.find(col_urls, query)

        if not list_obj_url:
            logger.info(f"Config url crawl: {config['url_crawl']} find 0 docs")
        else:
            logger.info(f"Config url crawl: {config['url_crawl']} find {len(list_obj_url)} docs")
            # tao queue luu task
            url_queue = queue.Queue()
            # đẩy doi tuong can crawl detail vào trong queue
            for obj_url in list_obj_url:
                url_queue.put(obj_url)

            # sinh luồng
            executor = thread.init_threadpool(_env.NUMB_THREAD_FOR_CRAWL_DETAIL)

            futures = []
            list_detail_news = []
            while not url_queue.empty():
                obj_url = url_queue.get()
                futures.append(executor.submit(crawl.crawl_detail, obj_url, config))

                # update ban ghi da duoc crawl detail
                query_find = _env.QUERY_FIND_URL_NUMB_CRAWL_0
                query_find["url"] = obj_url["url"]
                query_update = _env.QUERY_UPDATE_NUMB_CRAWL_DETAIL
                query_update["$set"]["time_crawl_detail"] = datetime.datetime.now()
                database.update_many(col_urls, query_find, query_update)

            # doi cac worker hoan thanh, xu ly ket qua cua tung worker
            for future in futures:
                try:
                    result = future.result()
                    list_detail_news.append(result)
                except Exception as e:
                    logger.error(f"Task failed with exception: \n{e}")

            # tat executor, doi cac worker hoan thanh
            executor.shutdown(wait=True)

            # format du lieu truoc khi insert
            list_doc = utils.format_list_detail_news(list_detail_news, config)
            # insert du lieu vao collection
            database.insert_many_col(col_detail, list_doc)

        logger.info("Task queue empty, task done")
