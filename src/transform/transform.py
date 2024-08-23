
import sys
import datetime
sys.path.append("./src")

from lxml import html

from transform import _env
from utils import utils


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_TRANSFORM, _env.LEVEL_LOG_MODUL_TRANSFORM)

def format_task(time_run, config):
    # 1 task sẽ có thời gian thực hiện và config
    task_format = {
        "time_run":time_run,
        "config":config
    }
    return task_format

def format_list_url(list_url, config):
    if not list_url:
        return False
    else:
        list_url= list(set(list_url))
        list_doc = []
        time_now = datetime.datetime.now()
        for url in list_url:
            list_doc.append({
            "website": config["website"],
            "url_crawl": config["url_crawl"],
            "data": url,
            "time_crawl": time_now
        })
        return list_doc

def format_detail_news(data, config, detail_new):
    if config["type"] == 1: # title
        detail_new["title"] = data
        return detail_new
    elif config["type"] == 2: # sapo
        detail_new["sapo"] = data
        return detail_new
    elif config["type"] == 3: # content
        detail_new["content"] = data
        return detail_new
    elif config["type"] == 4: # img
        detail_new["img"] = data
        return detail_new
    elif config["type"] == 5: # time post
        detail_new["time_post"] = data
        return detail_new
    elif config["type"] == 6: # source
        detail_new["source"] = data
        return detail_new
    elif config["type"] == 7: # author
        detail_new["author"] = data
        return detail_new

def format_list_detail_news(list_detail_news, config):
    if not list_detail_news:
        return False
    else:
        list_doc = []
        time_now = datetime.datetime.now()
        for detail_news in list_detail_news:
            list_doc.append({
            "website": config["website"],
            "url_crawl": config["url_crawl"],
            "data": detail_news,
            "time_crawl": time_now
        })
        return list_doc

def detect_result(logger, thread_name, config, result):
    if not result:
        logger.error(f"{thread_name}: Detect result false")
    else:
        if config["type_result"] == 1:
            logger.info(f"{thread_name}: Type result: Int")
            int_to_output(config, result)
        elif config["type_result"] == 2:
            logger.info(f"{thread_name}: Type result: List int")
            list_int_to_output(config, result)
        elif config["type_result"] == 3:
            logger.info(f"{thread_name}: Type result: String")
            string_to_output(config, result)
        elif config["type_result"] == 4:
            logger.info(f"{thread_name}: Type result: List string")
            list_string_to_output(config, result)
        elif config["type_result"] == 5:
            logger.info(f"{thread_name}: Type result: Datetime")
            datetime_to_output(config, result)
        elif config["type_result"] == 6:
            logger.info(f"{thread_name}: Type result: Element html")
            element_to_output(config, result)
        elif config["type_result"] == 7:
            logger.info(f"{thread_name}: Type result: List element html")
            return list_element_to_output(logger, thread_name, config, result)
        elif config["type_result"] == 8:
            logger.info(f"{thread_name}: Type result: Json")
            json_to_output(config, result)
        elif config["type_result"] == 9:
            logger.info(f"{thread_name}: Type result: List json")
            list_json_to_output(config, result)
        elif config["type_result"] == 10:
            pass
        elif config["type_result"] == 11:
            pass

def list_element_to_output(logger, thread_name, config, list_element):
    if config["type_output"] == 1:
        pass
    elif config["type_output"] == 2:
        pass
    elif config["type_output"] == 3:
        return list_element_to_string(thread_name, list_element)
    elif config["type_output"] == 4:
        pass
    elif config["type_output"] == 5:
        pass
    elif config["type_output"] == 6:
        pass
    elif config["type_output"] == 7:
        pass
    elif config["type_output"] == 8:
        pass
    elif config["type_output"] == 9:
        pass
    elif config["type_output"] == 10:
        pass
    elif config["type_output"] == 11:
        return list_element_to_list_attribute(thread_name, config, list_element)

def list_element_to_string(thread_name, list_element):
    try:
        result = ""
        for element in list_element: # duyet qua cac phan tu
            temp = ' '.join(element.itertext()) # trich xuat text cua phan tu
            result += temp + "\n"
        result = result.strip() # loai bo khoang trang thua
        if not result:
            logger.error(f"{thread_name}: String is None")
            return None
        else:
            logger.info(f"{thread_name}: Transfrom list element to string complete")
            return result
        
    except Exception as e:
        logger.warning(f"{thread_name}: Transfrom list element to string Exception:\n{e}")

def list_element_to_list_attribute(thread_name, config, list_element):
    
    list_result = []
    for element in list_element:
        logger.info(html.tostring(element))
        try:
            list_result.append(element.attrib[config["name_attribute"]])
        except:
            continue

    if not list_result:
        logger.error(f"{thread_name}: List attribute is None")
        return None
    else:
        logger.info(f"{thread_name}: Transfrom list element to list attribute complete")
        return list_result
    
def int_to_output(logger, thread_name, config, int_data):
    pass

def list_int_to_output(logger, thread_name, config, list_int):
    pass

def string_to_output(logger, thread_name, config, string_data):
    pass

def list_string_to_output(clogger, thread_name, onfig, list_string):
    pass

def datetime_to_output(logger, thread_name, config, datetime):
    pass

def element_to_output(logger, thread_name, config, element):
    pass

def json_to_output(logger, thread_name, config, json_data):
    pass

def list_json_to_output(logger, thread_name, config, list_json):
    pass