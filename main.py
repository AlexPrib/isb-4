from task_function import *
from read import *
import argparse
import logging
logger = logging.getLogger()
logger.setLevel('INFO')
SETTINGS_FILE = "data/settings.json"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-set", "--settings", type=str, default=SETTINGS_FILE,
                        help="Allows to use your own json file ")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-fnd", "--find",
                       help="Find card number", action="store_true")
    group.add_argument("-ch", "--check",
                       help="Check validation of card number", action="store_true")
    group.add_argument("-st", "--statistic",
                       help="Measures dependence of time on threads", action="store_true")
    args = parser.parse_args()
    settings = read_settings(args.settings)
    if args.find:
        find_number(settings, int(settings["thread_number"]))
    elif args.check:
        logging.info(f'Validation status: {luhn_algorithm(settings)}')
    elif args.statistic:
        make_statistic(settings)