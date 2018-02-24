import sqlite3

from settings import config, constants
from db.entities import SearchParameters, Torrent, Metric


def insert_new_torrent_line(torrent, connection):
    """

    :type torrent: db.entities.TorrentLine
    :type connection:
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM TORRENTS WHERE ID=?', (torrent.ygg_id,))

    if not cursor.fetchone():
        if torrent.alive:
            alive = 1
        else:
            alive = 0
        cursor.execute(
            'INSERT INTO TORRENTS (NAME, SIZE, ALIVE, CATEGORY, SUB_CATEGORY, ID) VALUES(?, ?, ?, ?, ?, ?)',
            (torrent.name, torrent.size, alive, torrent.category, torrent.sub_category, torrent.ygg_id))
        ygg_id = cursor.lastrowid
    else:
        ygg_id = torrent.ygg_id
    if torrent.seeders_number != 0:
        ratio = torrent.leechers_number / torrent.seeders_number
    else:
        ratio = 0
    cursor.execute(
        'INSERT INTO METRICS (SCRAPING_DATE, SEEDERS_NUMBER, LEECHERS_NUMBER, RATIO, TORRENT_ID) VALUES(?, ?, ?, ?, ?)',
        (torrent.scrap_date, torrent.seeders_number, torrent.leechers_number, ratio, ygg_id))
    connection.commit()


def insert_new_torrents_lines(torrents):
    connection = sqlite3.connect(config.database_path)
    for torrent in torrents:
        insert_new_torrent_line(torrent, connection)
    connection.close()


def set_dead_torrents_in_category(all_torrents_in_category, category):
    connection = sqlite3.connect(config.database_path)
    ygg_id_list = [str(torrent.ygg_id) for torrent in all_torrents_in_category]
    request = 'UPDATE TORRENTS SET ALIVE = 0 WHERE CATEGORY = ? AND ALIVE = 1 AND ID NOT IN ({})'.format(
        ','.join(ygg_id_list))
    cursor = connection.cursor()
    cursor.execute(request, (category.name,))
    connection.commit()
    new_dead_torrents_count = cursor.rowcount
    connection.close()
    return new_dead_torrents_count


def search(search_parameters):
    """

    :rtype: [Torrent]
    :type search_parameters: SearchParameters
    """
    connection = sqlite3.connect(config.database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Build request
    request = 'SELECT t.ID AS YGG_ID, m.id AS METRIC_ID, * FROM ({}) t, METRICS m WHERE t.ID = m.TORRENT_ID '
    sub_request = 'SELECT * FROM TORRENTS '
    need_where_clause_in_sub_request = search_parameters.name or search_parameters.category
    if need_where_clause_in_sub_request:
        sub_request += 'WHERE '
    request_params = ()

    # NAME
    if search_parameters.name:
        sub_request += 'NAME=? '
        request_params += (search_parameters.name,)

    # CATEGORY
    if search_parameters.category:
        if search_parameters.name:
            sub_request += 'AND '
        sub_request += 'CATEGORY=? '
        request_params += (search_parameters.category,)

    # ORDER
    if search_parameters.order and is_tolerate_order_value(search_parameters.order):
        order_by_criteria = 'ORDER BY {} '
        sub_request += order_by_criteria.format(search_parameters.order)
        request += order_by_criteria.format(search_parameters.order)

        # SORT
        if search_parameters.sort_mode and is_tolerate_sort_value(search_parameters.sort_mode):
            sub_request += search_parameters.sort_mode + " "
            request += search_parameters.sort_mode + " "

    # LIMIT
    if search_parameters.limit:
        limit = search_parameters.limit
    else:
        limit = config.default_limit_result
    sub_request += 'LIMIT ? '
    request_params += (limit,)

    # SKIP
    if search_parameters.skip:
        skip = search_parameters.skip
    else:
        skip = config.default_skip_result
    sub_request += 'OFFSET ?'
    request_params += (skip,)

    request = request.format(sub_request)
    cursor.execute(request, request_params)
    torrents = convert_rows_result_to_torrents_list(cursor)
    connection.close()
    return torrents


def is_tolerate_order_value(order_value):
    return order_value in constants.VALID_ORDER_VALUE


def is_tolerate_sort_value(sort_value):
    return sort_value in constants.VALID_SORT_ORDER_VALUE


def convert_rows_result_to_torrents_list(cursor):
    torrents = []
    torrents_dictionary = {}
    for row in cursor:
        ygg_id = row['YGG_ID']
        if ygg_id not in torrents_dictionary:
            name = row['NAME']
            size = row['SIZE']
            alive = True if row['ALIVE'] == 1 else False
            category = row['CATEGORY']
            sub_category = row['SUB_CATEGORY']
            torrent = Torrent(ygg_id, name, size, alive, category, sub_category, [])
            torrents.append(torrent)
            torrents_dictionary[ygg_id] = torrent
        else:
            torrent = torrents_dictionary[ygg_id]
        metric_id = row['METRIC_ID']
        scraping_date = row['SCRAPING_DATE']
        seeders_number = row['SEEDERS_NUMBER']
        leechers_number = row['LEECHERS_NUMBER']
        ratio = row['RATIO']
        metric = Metric(metric_id, scraping_date, seeders_number, leechers_number, ratio, ygg_id)
        torrent.metrics_list.append(metric)
    return torrents
