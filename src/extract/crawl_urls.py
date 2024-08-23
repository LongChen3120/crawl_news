import sys
sys.path.append("./src")

from extract import _env, crawl_function
from utils import utils, thread

def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_CRAWL_URLS, _env.LEVEL_LOG_MODUL_CRAWL_URLS)

def handler_crawl_url(config):
    # lay thread name
    thread_name = thread.get_thread_name()

    # chon loai crawl
    # 1: requests
    if config["type_crawl"] == 1:
        # gui request toi url
        response = crawl_function.request_to_url(thread_name, config["url_crawl"])
        # trich xuat element chua url hop le
        list_element = crawl_function.find_by_xpath(thread_name, config["url_crawl"], response, config)
        # trich xuat url tu list element
        list_url = crawl_function.extract_url_from_element(thread_name, config["url_crawl"], list_element)

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

    # format du lieu truoc khi tra lai main
    list_doc = utils.format_list_url(list_url, config)
    if not list_doc:
        logger.warning(f"{thread_name}: Url crawl {config['url_crawl']} return []")
        return []
    else:
        logger.warning(f"{thread_name}: Url crawl {config['url_crawl']} return {len(list_doc)} docs")
        return list_doc