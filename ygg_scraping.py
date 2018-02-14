import logging
import time
import requests
from services import scraping_service
import config
import constants
from db import dao

logging.basicConfig(filename=config.log_file, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')

if __name__ == '__main__':
    logging.info('=== start scraping ===')
    for category in constants.CATEGORIES_LIST:
        logging.info('category {} scanning...'.format(category.name))
        page = 0
        page_results_number = None
        new_torrents_list = True
        torrent_updated_counter = 0
        all_torrents_in_category = []
        while new_torrents_list:
            time.sleep(config.wait_time)
            url = "{}{}?{}={}&{}={}".format(constants.YGG_TORRENTS_ROOT_URL, category.id_url,
                                            constants.PER_PAGE_PARAM_URL,
                                            config.results_number_by_page, constants.PAGE_PARAM_URL, page)
            r = requests.get(url)

            # Get Torrents List to update
            new_torrents_list = scraping_service.get_torrents(r.text, category)
            if new_torrents_list:
                dao.insert_new_torrents_lines(new_torrents_list)
                torrent_updated_counter += len(new_torrents_list)
                all_torrents_in_category += new_torrents_list
            page += config.results_number_by_page
        logging.info('{} torrents updated'.format(torrent_updated_counter))
        logging.info('finding dead torrents...')
        dead_torrents_number = dao.set_dead_torrents_in_category(all_torrents_in_category, category)
        logging.info('{} dead torrents updated'.format(dead_torrents_number))
    logging.info('=== end scraping ===')
