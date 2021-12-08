from .youtube.youtube_collect import run_youtube_collect

def run_collection(platform, brands, date_range, query_id):
    if platform =='YouTube':
        run_youtube_collect(brands, date_range, query_id)
    #elif platform =='Twitter':
    #    run_twitter_collect(brands, date_range, query_id)
    #elif platform =='Pinterest':
    #    run_pinterest_collect(brands, date_range, query_id)
    #elif platform =='Facebook':
    #    run_facebook_collect(brands, date_range, query_id)
    #elif platform =='Instagram':
    #    run_instagram_collect(brands, date_range, query_id)


