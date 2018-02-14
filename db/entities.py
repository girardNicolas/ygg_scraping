import datetime
from enum import Enum


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


class Category:
    def __init__(self, name, id_url):
        self.name = name
        self.id_url = id_url


class SearchParameters:
    def __init__(self, name=None, category=None, order=None, skip=None, limit=None):
        self.name = name
        self.category = category
        self.order = order
        self.skip = skip
        self.limit = limit

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