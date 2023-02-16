from subprocess import Popen
import requests

from config import Config
from logging import Logger, getLogger
from json import dump, loads
from backend.worker.worker import txt_to_json
from enum import Enum
from typing import List

class QueryType(Enum):
    DOMAIN = 'domain'
    LOGIN = 'email'
    PASS = 'password'

class QueryParams:
    def __init__(self, type: QueryType, keyword: str, pagination: bool = True, page: int = 1) -> None:
        self.type = type
        self.keyword = keyword
        self.pagination = pagination
        self.page = page

def send_file(file: str or bytes, config: Config):
    logger = getLogger("Add.send")
    from_bytes = False
    if type(file) is bytes:
        from_bytes = True
        with open("from_archive.txt", 'wb') as out:
            out.write(file)
        filename = "from_archive.txt"
    else:
        filename = file
    logger.info("Passing file to worker...")
    txt_to_json(filename, config.add_address, config.add_batch_size)
    

def print_query(leaks: List[object]):
    mail_padding = 0
    for leak in leaks:
        full_address = f"{leak[QueryType.LOGIN.value]}@{leak[QueryType.DOMAIN.value]}"
        new_padding = len(full_address)
        if new_padding > mail_padding:
            mail_padding = new_padding
    print(f"\n{'Email'.ljust(mail_padding)} | Password")
    for leak in leaks:
        full_address = f"{leak[QueryType.LOGIN.value]}@{leak[QueryType.DOMAIN.value]}"
        print(f"{full_address.ljust(mail_padding)} | {leak[QueryType.PASS.value]}")
    print("")

def query_storage(address, payload, logger: Logger):
    try:
        response = requests.post(address, json=payload).json()
        return response
    except (requests.ConnectionError, requests.ConnectTimeout, requests.TooManyRedirects, requests.HTTPError) as e:
        logger.error(f"Couldn't receive response from storage module: {str(e)}")
        return {"is_final": True, "leaks": []}

def send_query(query: QueryParams, config: Config):
    logger = getLogger("Query.send")
    payload = {
        "key": query.type.value,
        "value": query.keyword
    }
    current_page = 1
    response = query_storage(config.query_address, payload, logger)
    if query.pagination:
        while current_page != query.page:
            if response["is_final"]:
                logger.warning(f"This search query ended after only {current_page} pages.")
                return
            payload["token"] = response["end_cursor"]
            response = query_storage(config.query_address, payload, logger)
            current_page += 1
        print_query(response["leaks"])
        if response["end_cursor"] != "":
            logger.info(f"This is not the last page for this search. To get the next page, use --page {current_page + 1} parameter")
    else:
        overall_leaks = response["leaks"]
        while not response["is_final"]:
            payload["token"] = response["end_cursor"]
            response = query_storage(config.query_address, payload, logger)
            overall_leaks += response["leaks"]
        print_query(overall_leaks)
            
    