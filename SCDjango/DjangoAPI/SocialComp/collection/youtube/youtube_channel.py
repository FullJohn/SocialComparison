import selenium.webdriver as webdriver
from bs4 import BeautifulSoup

from . import youtube_post
import time
import csv
import requests

def total_sub_count(content):
    subscribers = content[:content.rfind(" subscribers")]
    subscribers = subscribers[subscribers.rfind('"')+1:]
    if 'K' in subscribers:
        subscribers = subscribers.split('K')
        subscribers = float(subscribers[0]) * 1000
    
    return subscribers

class YouTubeChannel:
    ###############################################################
    # YouTubeChannel - Class                                      #
    #                                                             #
    # Description:                                                #
    #   Class for a YouTube channel                               #
    #   Used for collection videos from a specific                #
    #   YouTube channel.                                          #
    #                                                             #
    # Inputs:                                                     #
    #   channel_name - the name of the YouTube channel to collect #
    #                  from.                                      #
    #   Date         - Date range to collect posts within         #
    ###############################################################

    def __init__(self, channel_name, date_range, query_id):

        # Class Initialization function

        options = webdriver.ChromeOptions()

        # Default browser options
        options.add_argument('--incognito')
        options.add_argument('--headless')

        # Mobile Emulation Setup
        mobile_emulation = {"deviceName": "Nexus 5"}
        options.add_experimental_option('mobileEmulation', mobile_emulation)

        self.webdriver = webdriver.Chrome(options=options)

        self.channel_name = channel_name
        self.date_range = date_range
        self.url_list = []

        post = youtube_post.YouTubePost
        self.posts = []

        self.query_id = query_id
        self.retrieve_post_urls()
        self.create_posts()
        self.collect_posts()

    def retrieve_post_urls(self):

        # Retrieves the URLs from every video on the channel

        print("Beginning data retrieval for", self.channel_name)
        print("Collecting videos since", self.date_range)
        slash_c = False
        slash_user = False
        subs_c = 0
        subs_user = 0

        self.webdriver.get('https://www.youtube.com/c/' + self.channel_name + '/videos')

        if(self.webdriver.title != '404 Not Found'):
            # Meaning the channel exists at that url but we need to verify that it's the correct one
            slash_c = True

        if slash_c:
            content = requests.get("https://www.youtube.com/c/" + self.channel_name + '/videos').text
            subs_c = int(total_sub_count(content))
            
        self.webdriver.get('https://www.youtube.com/user/' + self.channel_name + '/videos')

        if(self.webdriver.title != '404 Not Found'):
            slash_user = True

        if slash_user:
            content = requests.get("https://www.youtube.com/user/" + self.channel_name + '/videos').text
            subs_user = int(total_sub_count(content))
        
        
        if subs_c > subs_user:
            self.webdriver.get('https://www.youtube.com/c/' + self.channel_name + '/videos')

        else:
            self.webdriver.get('https://www.youtube.com/user/' + self.channel_name + '/videos')

        last_height = self.webdriver.execute_script("return document.body.scrollHeight")
        scroll_pause = 0.5
        while True:
            self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = self.webdriver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(self.webdriver.page_source, 'lxml')

        time.sleep(3)
        videos = soup.find("lazy-list").find("ytm-item-section-renderer").find("lazy-list")

        for video in videos:
            url = video.find('a').get('href')
            if url == "/user/" + self.channel_name:
                pass
            else:
                self.url_list.append(url)

    def create_posts(self):

        # Creates a YouTubePost class for each video from the channel
        for url in self.url_list:
            post = youtube_post.YouTubePost(url, self.date_range, self.webdriver)
            self.posts.append(post)

    def collect_posts(self):
        # Calls the collect_post() method from YouTubePost to collect
        # data from each video
        for post in self.posts:
            keep_collecting = post.collect_post()
            if post.include_post:
                post.save_post(self.query_id)
            if not keep_collecting:
                break
                    
        self.webdriver.quit()
