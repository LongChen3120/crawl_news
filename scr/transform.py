
import utils
from lxml import html

import _env


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_TRANSFORM, _env.LEVEL_LOG_MODUL_TRANSFORM)

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