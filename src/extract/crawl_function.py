import sys
import requests
sys.path.append("./src")

from lxml import html

from extract import _env
from utils import utils


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_CRAWL_FUNCTION, _env.LEVEL_LOG_MODUL_CRAWL_FUNCTION)

def crawl_obj_requests(thread_name, url_detail, config, response):
    '''
    Hàm crawl từng đối tượng của bài báo (trong obj_crawl ở trong config)
    '''
    if response is None:
        logger.error(f"{thread_name}: Crawl obj fail")
        return False
    else:
        detail_new = {
            "url_detail": url_detail
        }
        # lap qua cac obj can crawl
        for obj in config["obj_crawl"]:
            result = find_by_xpath(thread_name, url_detail, response, obj)
            result = utils.detect_result(logger, thread_name, obj, result)
            detail_new = utils.format_detail_news(result, obj, detail_new)
        
        return detail_new

def request_to_url(thread_name, url):
    # try:
    response = requests.get(url)
    if response.status_code == 200:
        logger.info(f"{thread_name}: Request {url} status code 200")
        response.encoding = "utf-8"
        return html.fromstring(response.content)
    else:
        logger.error(f"{thread_name}: Request {url} fail, status code: {response.status_code}")
        return False
    # except:
    #     logger.error(f"{thread_name}: Request {url} fail")
    #     return False
    
def init_browser():
    pass

def request_to_api(api):
    response = requests.get(api)
    return response.json()

def find_by_xpath(thread_name, url, response, config):
    if response is None:
        logger.error(f"{thread_name}: {url} Find element by xpath fail")
        return False
    else:
        try:
            list_element = response.xpath(config["xpath"])
        except Exception as e:
            logger.warning(f"{thread_name}: {url} Exception find element by xpath:\n{e}")
        
        if not list_element:
            logger.warning(f"{thread_name}: {url} Find element by xpath: List element empty")
            return False
        else:
            logger.info(f"{thread_name}: {url} Find element by xpath complete")
            return list_element

def extract_url_from_element(thread_name, url, list_element):
    if not list_element:
        logger.warning(f"{thread_name}: Extract url from {url} fail")
        return False
    else:
        try:
            list_url = [element.attrib["href"] for element in list_element]
        except Exception as e:
            logger.warning(f"{thread_name}: Exception extract url from {url} :\n{e}")

        if not list_url:
            logger.warning(f"{thread_name}: Extract url from {url}: List url empty")
            return False
        else:
            logger.info(f"{thread_name}: Extract url from {url} complete")
            return list_url

def get_data_from_keys(config, data):
    for key in config["keys"]:
        data = data[key]
    return data