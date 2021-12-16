import sys
# import insta_page
# import insta_post
from . import insta_page
from . import insta_post
import datetime

def run_instagram_collect(brands, date_range, query_id):
    date_range = pre_collect(date_range)

    if date_range[0] > date_range[1]:
        date_range.reverse()

    for brand in brands:
        insta_page.Insta_Page(brand, date_range, query_id)

def pre_collect(date_range):
    date1 = [date_range[0].split('T')[0]][0]
    date2 = [date_range[1].split('T')[0]][0]
    date1 = date1.split('-')
    date2 = date2.split('-')
    date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
    date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
    return [date1, date2]

"""
Driver to test locally
brands = ["oreo", "ritzcrackers", "pringles"]
date_range = ["2021-12-1", "2021-12-30"]
run_instagram_collect(brands, date_range, query_id=1)
"""
