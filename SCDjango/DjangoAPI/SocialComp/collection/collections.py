from .youtube.youtube_collect import run_youtube_collect

def run_collection(platform, brands, date_range):
    if platform =='YouTube':
        run_youtube_collect(brands, date_range)
    else if platform =='Twitter':
        run_twitter_collect(brands, date_range)
    else if platform =='Pinterest':
        run_pinterest_collect(brands, date_range)
    else if platform =='Facebook':
        run_facebook_collect(brands, date_range)
    else if platform =='Instagram':
        run_instagram_collect(brands, date_range)
