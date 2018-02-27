import logging
import re
import time

import requests
from bs4 import BeautifulSoup

from db import dao
from db.entities import TorrentLine
from settings import constants, config


def get_result_number(html):
    html = BeautifulSoup(html, "html.parser")
    content = html.find('div', attrs={'class': 'panel-title'}).text
    m = re.search(' [0-9]{1,6} ', content)
    return int(m.group(0).strip())


def convert_size_in_byte(size_str):
    """

    :type size_str: str
    """
    if size_str.find(constants.TB_KEY_WORD) != -1:
        return float(size_str.strip(constants.TB_KEY_WORD)) * 1099511627776
    elif size_str.find(constants.GB_KEY_WORD) != -1:
        return float(size_str.strip(constants.GB_KEY_WORD)) * 1073741824
    elif size_str.find(constants.MB_KEY_WORD) != -1:
        return float(size_str.strip(constants.MB_KEY_WORD)) * 1024
    elif size_str.find(constants.KB_KEY_WORD) != -1:
        return float(size_str.strip(constants.KB_KEY_WORD))
    elif size_str.find(constants.B_KEY_WORD) != -1:
        return float(size_str.strip(constants.B_KEY_WORD)) / 1024
    else:
        return None


def get_id_from_torrent_page(torrent_page):
    return int(re.search('\/[0-9]{1,8}-', torrent_page).group(0).strip('/').strip('-'))


def get_sub_category_from_torrent_page(torrent_page):
    """

    :rtype: str
    """
    return torrent_page.split('/')[constants.YGG_SUB_CATEGORY_TORRENT_PAGE_INDEX]


def sanitize_torrent_name(name):
    return re.sub('^\s*|\s*$', '', name)


def get_torrent(tr, category):
    index = 0
    name, size, nb_seeders, ygg_id, nb_leechers, torrent_page, sub_category = None, None, None, None, None, None, None
    for td in tr.findAll('td'):
        if index == 0:
            a = td.find('a')
            name = sanitize_torrent_name(a.text)
            torrent_page = a.attrs['href']
            ygg_id = get_id_from_torrent_page(torrent_page)
            sub_category = get_sub_category_from_torrent_page(torrent_page)

        elif index == 3:
            size = convert_size_in_byte(td.text)
            if size is None:
                logging.error("Size unrecognized")
        elif index == 4:
            nb_seeders = int(td.text)
        elif index == 5:
            nb_leechers = int(td.text)
        index += 1
    return TorrentLine(ygg_id, name, size, nb_seeders, nb_leechers, category, sub_category.upper())


def get_torrents(html, category=None):
    """
    :rtype: list
    """
    html = BeautifulSoup(html, "html.parser")
    t_body_torrents = html.find('tbody')
    tr_to_parse_list = t_body_torrents.findAll('tr')
    torrents_list = []
    for tr in tr_to_parse_list:
        torrent = get_torrent(tr, category)
        torrent.category = category.name
        torrents_list.append(torrent)
    return torrents_list


def run_scraping():
    logging.info('=== start scraping ===')
    for category in constants.CATEGORIES_LIST:
        logging.info('category {} scanning...'.format(category.name))
        page = 0
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
            new_torrents_list = get_torrents(r.text, category)
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
