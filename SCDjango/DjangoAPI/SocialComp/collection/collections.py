from .youtube.youtube_collect import run_youtube_collect
from .tiktok.tiktok_collect import run_tiktok_collect
from .pinterest.pinterest_collect import run_pinterest_collect
from .twitter.twitter_collect import run_twitter_collect

def run_collection(platform, brands, date_range, query_id):
    if platform =='YouTube':
        run_youtube_collect(brands, date_range, query_id)
    elif platform =='Twitter':
        run_twitter_collect(brands, date_range, query_id)
    elif platform =='Pinterest':
        run_pinterest_collect(brands, date_range, query_id)
    elif platform =='TikTok':
        run_tiktok_collect(brands, date_range, query_id)
    #elif platform =='Facebook':
    #    run_facebook_collect(brands, date_range, query_id)
    #elif platform =='Instagram':
    #    run_instagram_collect(brands, date_range, query_id)
