from .youtube.youtube_collect import run_youtube_collect
from .tiktok.tiktok_collect import run_tiktok_collect
from .pinterest.pinterest_collect import run_pinterest_collect
from .twitter.twitter_collect import run_twitter_collect
from .facebook.fb_collect import run_facebook_collect
from .instagram.insta_collect import run_instagram_collect

def run_collection(platform, brands, date_range, query_id):
    platform = platform.lower()
    if platform =='youtube':
        run_youtube_collect(brands, date_range, query_id)
    elif platform =='twitter':
        run_twitter_collect(brands, date_range, query_id)
    elif platform =='pinterest':
        run_pinterest_collect(brands, date_range, query_id)
    elif platform =='tiktok':
       run_tiktok_collect(brands, date_range, query_id)
    elif platform =='facebook':
       run_facebook_collect(brands, date_range, query_id)
    elif platform =='instagram':
       run_instagram_collect(brands, date_range, query_id)
