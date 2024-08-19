
import json
import logging
import datetime
import logging.handlers
import transform

import _env


def init_logger(path_log):
    global logger
    logger = config_log(path_log, _env.NAME_LOGGER_MODUL_UTILS, _env.LEVEL_LOG_MODUL_UTILS)

def config_log(path_log, name_logger, lever_logger):
    '''
    cấu hình root logger này bị cấu hình của airflow ghi đè nên không thể ghi log ra file riêng _env.PATH_LOG_FILE được
    '''
    # logging.basicConfig(level=logging.INFO, 
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    #                     handlers=[logging.FileHandler(_env.PATH_LOG_FILE)]
    #                     )


    '''
    cấu hình tạo logger riêng để tự ghi log ra file riêng
    '''
    logger = logging.getLogger(name_logger)
    logger.setLevel(lever_logger)

    # Tạo formatter để định dạng log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Tạo file handler để ghi log vào file theo ngày
    file_handler = logging.handlers.TimedRotatingFileHandler(path_log, when="midnight", interval=1, encoding="utf-8")
    file_handler.setFormatter(formatter)
    # tên sẽ kèm thêm thời gian
    file_handler.suffix = "%Y-%m-%d.log"

    # Loại bỏ tất cả các handler ghi ra console
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            logger.removeHandler(handler)
    
    # Thêm file handler vào logger
    logger.addHandler(file_handler)
    return logger

def read_config(path_config):
    name_config = path_config.split("/")[-1]
    logger.info(f"Read config {name_config}")
    return json.load(open(path_config, "r", encoding="utf-8"))

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

def check_all_thread_done(futures):
    for future in futures:
        if future.done() == False:
            return False
    return True

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

def list_element_to_output(logger, thread_name, config, list_element):
    if config["type_output"] == 1:
        pass
    elif config["type_output"] == 2:
        pass
    elif config["type_output"] == 3:
        return transform.list_element_to_string(thread_name, list_element)
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
        return transform.list_element_to_list_attribute(thread_name, config, list_element)

def json_to_output(logger, thread_name, config, json_data):
    pass

def list_json_to_output(logger, thread_name, config, list_json):
    pass