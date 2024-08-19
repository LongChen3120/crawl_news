import logging
import pymongo
import pymongo.mongo_client

import _env, utils


def init_logger(path_log):
    global logger
    logger = utils.config_log(path_log, _env.NAME_LOGGER_MODUL_DATABASE, _env.LEVEL_LOG_MODUL_DATABASE)

def connect_db_mongodb(connection_string, db_name):
    try:
        client = pymongo.MongoClient(connection_string)
        db = client[db_name]
        logger.info(f"Connected database {db_name}")
        return db
    except Exception as e:
        logger.error(f"Connect database {db_name} fail:\n{e}")

def connect_col(db, col_name):
    try:
        col = db[col_name]
        logger.info(f"Connected collection {col_name}")
        return col
    except Exception as e:
        logger.error(f"Connect collection {col_name} fail:\n{e}")

def find(col, query):
    try:
        result = col.find(query)
        result = list(result)
        if not result:
            logger.warning("Find: Empry")
        else:
            return result
    except Exception as e:
        logger.warning(f"Find raise exception:\n{e}")

def find_sort(col, query, sort):
    pass

def find_limit(col, query, limit):
    try:
        result = col.find(query).limit(limit)
        result = list(result)
        if not result:
            logger.warning("Find limit: Empry")
        else:
            return result
    except Exception as e:
        logger.warning(f"Find limit raise exception:\n{e}")

def find_sort_limit(col, query, sort, limit):
    pass

def insert_one_col(col, doc):
    pass

def insert_many_col(col, list_doc):
    # list docs là list dicts
    try:
        result = col.insert_many(list_doc)
        logger.info(f"Inserted {len(result.inserted_ids)} docs")
    except:
        logger.warning("Insert many fail")

def update_one(col, query_find, query_update):
    pass

def update_many(col, query_find, query_update):
    try:
        result = col.update_many(query_find, query_update)
        # logger.info(f"Update many find: {result.matched_count} docs, update:{result.modified_count} docs")
    except Exception as e:
        logger.warning(f"Update many raise exception:\n{e}")
