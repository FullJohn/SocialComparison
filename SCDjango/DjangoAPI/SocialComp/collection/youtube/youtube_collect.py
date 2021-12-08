import sys
from . import youtube_channel
from . import youtube_post
import datetime


def run_youtube_collect(brands, date_range, query_id):

    date_range = pre_collect(date_range)

    if date_range[0] > date_range[1]:
        date_range.reverse()

    for brand in brands:
        youtube_channel.YouTubeChannel(brand, date_range, query_id)


def pre_collect(date_range):
    
    date1 = [date_range[0].split('T')[0]][0]
    date2 = [date_range[1].split('T')[0]][0]
    date1 = date1.split('-')
    date2 = date2.split('-')
    date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
    date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
    return [date1, date2]
