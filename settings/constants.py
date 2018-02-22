from db.entities import Category

YYG_TORRENT_SITE = 'https://yggtorrent.com/'
YGG_TORRENT_PAGE_ROOT_URL = YYG_TORRENT_SITE + 'torrent/'
YGG_TORRENTS_ROOT_URL = YYG_TORRENT_SITE + 'torrents/'
YGG_TORRENTS_ROOT_DOWNLOAD_URL = YYG_TORRENT_SITE + 'engine/download_torrent'
YGG_SUB_CATEGORY_TORRENT_PAGE_INDEX = 5
FILM_CATEGORY = '2145-filmvidéo'
AUDIO_CATEGORY = '2139-audio'
APPLICATION_CATEGORY = '2144-application'
JEU_VIDEO_CATEGORY = '2142-jeu+vidéo'
E_BOOK_CATEGORY = '2140-ebook'
EMULATION_CATEGORY = '2141-emulation'
GPS_CATEGORY = '2143-gps'
PER_PAGE_PARAM_URL = 'per_page'
PAGE_PARAM_URL = 'page'
ID_PARAM_URL = 'id'

MB_KEY_WORD = 'MB'
GB_KEY_WORD = 'GB'
KB_KEY_WORD = 'kB'
B_KEY_WORD = 'B'


CATEGORIES_LIST = [Category('GPS', GPS_CATEGORY),
                   Category('AUDIO', AUDIO_CATEGORY),
                   Category('APPLICATION', APPLICATION_CATEGORY),
                   Category('JEU_VIDEO', JEU_VIDEO_CATEGORY),
                   Category('E_BOOK', E_BOOK_CATEGORY),
                   Category('EMULATION', EMULATION_CATEGORY),
                   Category('FILM_VIDEO', FILM_CATEGORY)]

# REST API
VALID_ORDER_VALUE = {'SIZE', 'NAME', 'CATEGORY'}
