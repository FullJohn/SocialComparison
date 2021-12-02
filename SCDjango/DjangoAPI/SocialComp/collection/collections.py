from .youtube.youtube_collect import run_youtube_collect

def run_collection(platform, brands, date_range):
    if platform =='YouTube':
        run_youtube_collect(brands, date_range)

