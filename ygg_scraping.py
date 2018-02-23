import getopt
import logging
import sys

from services import rest_service, scraping_service
from settings import config

logging.basicConfig(filename=config.log_file, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def usage():
    return 'TODO'


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "rs", ["run_scraping", "start_rest_api"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-r", "--run_scraping"):
            scraping_service.run_scraping()
        elif o in ("-s", "--start_rest_api"):
            rest_service.start_api()
        else:
            assert False, "unhandled option"
