import sys
import json
import logging
sys.path.append("./src")

from utils import _env


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

def check_all_thread_done(futures):
    for future in futures:
        if future.done() == False:
            return False
    return True
