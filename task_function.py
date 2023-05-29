import hashlib
import json
import logging
import multiprocessing as mp
from functools import partial
from time import time
from tqdm import tqdm
from matplotlib import pyplot as plt


def check_hash(settings: dict, first_digits: int, other_digits: int) -> int:
    """The function performs a comparison between the found hash of the map and the hash that we have.

    Args:
        first_digits: 6 first digits
        other_digits: 4 last digits

    Returns:
        int: card number if hash matched or False 
    """
    full_number = f'{first_digits}{other_digits}{settings["last_digits"]}'
    if hashlib.md5(f'{full_number}'.encode()).hexdigest() == settings["hash"]:
        logging.info(f'Hash matched! Card number: {full_number}')
        return int(full_number)
    else:
        return False


def find_number(settings: dict, streams: int) -> None:
    """The function locates a card number that has the same hash

    Args:
        
        streams: number of used threads
    """
    completion = False
    with mp.Pool(streams) as pl:
        for num in settings["first_digits"]:
            logging.info(f'Starting card number selection: {num}******{settings["last_digits"]}')
            for number in pl.map(partial(check_hash, settings, int(num)), tqdm(range(100000, 1000000),
                                                                               colour="green")):
                if number:
                    pl.terminate()
                    completion = True
                    data = {}
                    data["card_number"] = f'{number}'
                    data["validation_check"] = "Unknown"
                    logging.info(f'Card number found! Saving into {settings["save_path"]}')
                    try:
                        with open(settings["save_path"], "w") as f:
                            json.dump(data, f)
                    except OSError as err:
                        logging.warning(f'{err} during writing to {settings["save_path"]}')
                    break
            if completion:
                break
    if completion is not True:
        logging.info("Card number not found")


def luhn_algorithm(settings: dict) -> bool:
    """The function performs a card number validation check.

    Args:
        settings: settings

    Returns:
        bool: validation status
    """
    try:
        with open(settings["save_path"], "r") as f:
            data = json.load(f)
    except OSError as err:
        logging.warning(f'{err} during reading from {settings["save_path"]}')
    num = data["card_number"]
    length = len(num)
    if length != 16:
        logging.info("Invalid card number")
        if data["validation_check"] != "Unknown" or data["validation_check"] != "Invalid":
            data["validation_check"] = "Invalid"
            try:
                with open(settings["save_path"], "w") as f:
                    json.dump(data, f)
            except OSError as err:
                logging.warning(f'{err} during writing into {settings["save_path"]}')
        return False
    else:
        sum = 0
        for i in range(0, length - 1):
            if(length - i) % 2 == 0:
                if (int(num[i]) * 2) // 10 != 0:
                    sum = sum + (int(num[i]) * 2) // 10 + (int(num[i]) * 2) % 10
                else:
                    sum += (int(num[i]) * 2) // 10
            else:
                sum += int(num[i])
        sum %= 10
        sum %= 10
        sum = 10 - sum
        if sum == int(num[15]):
            logging.info("Card number is valid")
            if data["validation_check"] != "Unknown" or data["validation_check"] != "Valid":
                data["validation_check"] = "Valid"
                try:
                    with open(settings["save_path"], "w") as f:
                        json.dump(data, f)
                except OSError as err:
                    logging.warning(f'{err} during writing into {settings["save_path"]}')
            return True
        else:
            logging.info("Invalid card number")
            if data["validation_check"] != "Unknown" or data["validation_check"] != "Invalid":
                data["validation_check"] = "Invalid"
                try:
                    with open(settings["save_path"], "w") as f:
                        json.dump(data, f)
                except OSError as err:
                    logging.warning(f'{err} during writing into {settings["save_path"]}')
            return False
        
    
def make_statistic(settings: dict) -> None:
    """The function measures the time taken and generates a graph
     showing the relationship between the time and the number of used threads.

    Args:
        settings: settings
    """
    logging.info("Measuring statistic")
    times = []
    for i in range(int(settings["thread_number"])):
        start = time()
        logging.info(f'Thread number: {i+1}')
        find_number(settings, i+1)
        times.append(time() - start)
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Time')
    plt.xlabel('Threads')
    plt.title('Dependence of time on number of threads')
    plt.plot(list(x + 1 for x in range(int(settings["thread_number"]))), times, color='#004158')
    plt.savefig(f'{settings["pic_path"]}')
    logging.info(f'Picture has been saved into {settings["pic_path"]}')
