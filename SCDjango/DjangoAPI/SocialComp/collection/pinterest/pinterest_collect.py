import pinterest_user
import time
import datetime


firstDate =  datetime.datetime.now() - datetime.timedelta(30)
lastDate  =  datetime.datetime.now()


print('Beginning data retrieval...')
oreo = pinterest_user.PinterestUser('oreo', firstDate, lastDate)

oreo.retrieve_posts()
oreo.parse_divs()

import sys
from . import pinterest_user
from . import pinterest_post
import datetime


def run_pinterest_collect(brands, date_range):

    date_range = pre_collect(date_range)

    if date_range[0] > date_range[1]:
        date_range.reverse()

    for brand_name in brands:
        pinterest_user.PinterestUser(brand_name, date_range)


def pre_collect(date_range):
    
    date1 = [date_range[0].split('T')[0]][0]
    date2 = [date_range[1].split('T')[0]][0]
    date1 = date1.split('-')
    date2 = date2.split('-')
    date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
    date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
    return [date1, date2]