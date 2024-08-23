import sys
sys.path.append("./src")

from extract import _env, crawl_function
from utils import utils, thread


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_CRAWL_DETAIL, _env.LEVEL_LOG_MODUL_CRAWL_DETAIL)

def handler_crawl_detail(obj_url, config):
    # lay thread name
    thread_name = thread.get_thread_name()

    # chon loai crawl
    # 1: requests
    if config["type_crawl"] == 1:
        # gui request toi url
        response = crawl_function.request_to_url(thread_name, obj_url["url"])

        # lap qua cac obj can crawl
        detail_news = crawl_function.crawl_obj_requests(thread_name, obj_url["url"], config, response)

    # 2: api
    elif config["type_crawl"] == 2:
        # gui request toi api
        response = crawl_function.request_to_api(config["url_crawl"])
        response = response.json()

        # loc lay data can thiet
        data = crawl_function.get_data_from_keys(config)

        # chua xu ly tiep

    # 3: selenium
    elif config["type_crawl"] == 3:
        pass

    return detail_news