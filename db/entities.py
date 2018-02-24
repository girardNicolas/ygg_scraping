import datetime
from enum import Enum

from settings import constants


class TorrentLine:
    def __init__(self, ygg_id, name, size, seeders_number, leechers_number, category, sub_category,
                 scrap_date=None, alive=True):
        if not scrap_date:
            self.scrap_date = datetime.datetime.now()
        else:
            self.scrap_date = scrap_date
        self.name = name
        self.size = size
        self.seeders_number = seeders_number
        self.leechers_number = leechers_number
        self.category = category
        self.sub_category = sub_category
        self.alive = alive
        self.ygg_id = ygg_id


class SearchParameters:
    def __init__(self, name=None, category=None, order=None, skip=None, limit=None, sort_mode=None):
        self.name = name
        self.category = category
        self.order = order
        self.skip = skip
        self.limit = limit
        self.sort_mode = sort_mode

    def all_none(self):
        for attr_value in self.__dict__.values():
            if attr_value:
                return False
        return True


class Torrent:
    def __init__(self, ygg_id, name, size, alive, category, sub_category, metrics_list):
        self.ygg_id = ygg_id
        self.name = name
        self.size = size
        self.category = category
        self.sub_category = sub_category
        self.alive = alive
        self.metrics_list = metrics_list

    def get_torrent_page_link(self):
        def convert_category_part_for_url(cat):
            return cat.strip('_').lower()
        category = convert_category_part_for_url(self.category)
        sub_category = convert_category_part_for_url(self.sub_category)
        name = self.name.replace(' ', '+').lower()
        return '{}{}/{}/{}-{}'.format(constants.YGG_TORRENT_PAGE_ROOT_URL, category, sub_category, self.ygg_id, name)

    def get_direct_link_download(self):
        return '{}?{}={}'.format(constants.YGG_TORRENTS_ROOT_DOWNLOAD_URL, constants.ID_PARAM_URL, self.ygg_id)


class Metric:
    def __init__(self, metric_id, scraping_date, seeders_number, leechers_number, ratio, torrent_id):
        self.metric_id = metric_id
        self.scraping_date = scraping_date
        self.seeders_number = seeders_number
        self.leechers_number = leechers_number
        self.ratio = ratio
        self.torrent_id = torrent_id


class SearchOrder(Enum):
    CATEGORY = 'CATEGORY'
    NAME = 'NAME'
    SIZE = 'SIZE'
