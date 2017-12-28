# -*- coding: utf-8 -*-

"""
fut.extras
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's additional methods.

"""

import requests

def futheadPrice(item_id, year=18, platform=None):
    params = {'year': year,
              'id': item_id}
    rc = requests.get('http://www.futhead.com/prices/api/', params=params)
    if rc.status_code == 524:  # connection timeout
        return 0
    try:
        rc = rc.json()
    except JSONDecodeError:
        print('futhead response is not valid')
        print(rc.status_code)
        print(rc.url)
        print(rc.content)
        rc = {}
    if not rc:
        return 0
    rc = rc[str(item_id)]
    xbox = rc['xbLowFive'][0]
    ps = rc['psLowFive'][0]

    if platform == 'xbox':
        price = xbox
    elif platform == 'ps':
        price = ps
    else:
        price = max([xbox, ps])

    return price


def futbinPrice(item_id, platform=None):
    rc = requests.get('https://www.futbin.com/18/playerPrices', params={'player': str(item_id)})
    try:
        rc = rc.json()
    except ValueError:
        return -1, "N/A"
    if not rc:
        return 0
    rc = rc[str(item_id)]['prices']
    rc['xbox']['LCPrice'] = str(rc['xbox']['LCPrice']).replace(',', '')
    rc['ps']['LCPrice'] = str(rc['ps']['LCPrice']).replace(',', '')
    rc['pc']['LCPrice'] = str(rc['pc']['LCPrice']).replace(',', '')
    xbox = int(rc['xbox']['LCPrice'])
    ps = int(rc['ps']['LCPrice'])
    pc = int(rc['pc']['LCPrice'])

    if platform == 'pc':
        price = pc
    elif platform == 'xbox':
        price = xbox
    elif platform == 'ps':
        price = ps
    else:
        price = max([xbox, ps, pc])

    return price, rc['ps']['updated']


# def futwizPrice(item_id, platform=None):  # item_id is different on this page
#     if not platform or platform == 'xbox':
#         rc = requests.get('https://www.futwiz.com/en/app/price_history_player', params={'p': item_id, 'h': '', 'c': 'xb'}).json()
#         print(rc)
#         if rc:
#             xbox = rc[0][1]
#         else:
#             xbox = 0
#     if not platform or platform == 'ps':
#         rc = requests.get('https://www.futwiz.com/en/app/price_history_player', params={'p': item_id, 'h': '', 'c': 'ps'}).json()
#         print(rc)
#         if rc:
#             ps = rc[0][1]
#         else:
#             ps = 0
#
#     if not platform:
#         price = max([xbox, ps])
#     elif platform == 'ps':
#         price = ps
#     elif platform == 'xbox':
#         price = xbox
#
#     return price
