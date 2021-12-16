import time
import datetime
import re

from bs4 import BeautifulSoup

from SocialComp.serializers import PostSerializer
from ...models import PostModel

class TwitterPost:
    ###############################################################
    # TwitterPost - Class                                         #
    #                                                             #
    # Description:                                                #
    #   Twitter post data and methods                             #
    #   Used for parsing the data from a specific Twitter post    #
    #                                                             #
    # Inputs:                                                     #
    #   div - div scraped from the twitter users page             #
    #   brand_name - account brand name                           #
    #                                                             #
    # Pierce Hopkins                                              #
    ###############################################################

    def __init__(self, div, brand_name):
        # Class initialization function
        self.post_html = div
        
        self.post_url = ''
        self.brand = brand_name
        self.description = ''
        self.likes = -1
        self.retweets = -1
        self.date = ''
        self.comments = -1
        self.image_url = ''
        self.vid_views = ''
        self.followers = ''
        
        
    def scrape_post(self):
        #@NOTE(P): Parse Post URL
        #a
        #css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-1qd0xha r-1b43r93 r-16dba41 r-hjklzo r-bcqeeo r-3s2u2q r-qvutc0
        post_url = self.post_html.find("a", class_="css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-1qd0xha r-1b43r93 r-16dba41 r-hjklzo r-bcqeeo r-3s2u2q r-qvutc0")
        if post_url != None:
            self.post_url = "www.twitter.com" + post_url['href']
        else:
            self.post_url = "www.twitter.com" + "/error"

        #@NOTE(P): Parse post text if it exists
        #span
        #css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0
        post_text_element = self.post_html.find("div", { "lang" : "en" })
        self.description = post_text_element.get_text() if post_text_element else "{No Post Text}"
        
            
        #@NOTE(P): Parse likes
        #div
        #css-18t94o4 css-1dbjc4n r-1777fci r-3vrnjh r-1ny4l3l r-bztko3 r-lrvibr
        likes = self.post_html.find("div", { "data-testid" : "like" }).attrs['aria-label']
        if likes != None:
            p = re.search(r"(\d+) Likes. Like", likes)
            self.likes = int(p.group(1))
        else:
            self.likes = 0
        
        #@NOTE(P): Parse retweets
        #div
        #css-18t94o4 css-1dbjc4n r-1777fci r-3vrnjh r-1ny4l3l r-bztko3 r-lrvibr
        retweets = self.post_html.find("div", { "data-testid" : "retweet" }).attrs['aria-label']
        if retweets != None:
            p = re.search(r"(\d+) Retweets. Retweet", retweets)
            self.retweets = int(p.group(1))
        else:
            self.retweets = 0
        
        #@NOTE(P):Scrape the date
        #time
        time_posted = self.post_html.find("time")
        #@NOTE(P): Twitter datetime example: 2021-09-27T18:26:32.000Z 
        self.date = datetime.datetime.strptime(time_posted.attrs['datetime'], "%Y-%m-%dT%H:%M:%S.000Z")
        
        #@NOTE(P): Parse comments
        #div
        #css-18t94o4 css-1dbjc4n r-1777fci r-3vrnjh r-1ny4l3l r-bztko3 r-lrvibr
        comments = self.post_html.find("div", { "data-testid" : "reply" }).attrs['aria-label']
        if comments != None:
            p = re.search(r"(\d+) Replies. Reply", comments)
            self.comments = int(p.group(1))
        else:
            self.comments = 0
        
        #NOTE(P): Parse the image if it exists
        #div(?)
        #css-1dbjc4n r-1p0dtai r-1mlwlqe r-1d2f490 r-11wrixw r-1mnahxq r-1udh08x r-u8s1d r-zchlnj r-ipm5af r-417010
        post_img_element = self.post_html.find("div", { "data-testid" : "tweetPhoto" })
        if post_img_element == None:
            self.image_url = "{No Post Image}"
        else:
            self.image_url = post_img_element.find("img", { "class" : "css-9pa8cd" }).attrs['src']
        
        #NOTE(P): Parse the video views if the post contains a video
        post_vid_element = self.post_html.find("div", { "class" : "css-1dbjc4n r-1awozwy r-k200y r-loe9s5 r-pm2fo r-1dpl46z r-z2wwpe r-ou6ah9 r-notknq r-1yevf0r r-1777fci r-s1qlax r-633pao" })
        self.vid_views = post_vid_element.get_text() if post_vid_element else "{No Post Video}"
          

    def print(self):
        # Prints the data from the post
        print("Brand:\t\t", self.brand)
        print("Post URL:\t", self.post_url)
        print("Description:\t", self.description)
        print("Date:\t\t", self.date)
        print("Likes:\t\t", self.likes)
        print("Retweets:\t", self.retweets)
        print("Comments:\t", self.comments)
        print("Image URL:\t", self.image_url)
        print("Video Views:\t", self.vid_views)
        print("Acount Followers:\t", self.followers)
        print("\n\n")
        
    def save_post(self, query_id):
        post_data = {}
        """
        post_data['QueryId'] = str(query_id)
        post_data['brand'] = str(self.brand)
        post_data['url'] = str(self.post_url)
        post_data['description'] = str(self.description)
        post_data['date'] = str(self.date)
        post_data['likes'] = str(self.likes)
        post_data['retweets'] = str(self.retweets)
        post_data['comments'] = str(self.comments)
        post_data['image_url'] = str(self.image_url)
        post_data['views'] = str(self.vid_views)
        post_data['followers'] = str(self.followers)
        """
        post_data['QueryId'] = str(query_id)
        post_data['url'] = str(self.post_url)
        post_data['title'] = str(self.retweets)
        post_data['description'] = str(self.description)
        post_data['thumbnail'] = str(self.image_url)
        post_data['channel'] = str(self.brand)
        post_data['date'] = str(self.date)
        post_data['views'] = str(self.vid_views)
        post_data['comments'] = str(self.comments)
        post_data['likes'] = str(self.likes)
        
        post_serializer = PostSerializer(data = post_data)

        if post_serializer.is_valid():
            post_serializer.save()

        else:
            print(post_serializer.errors)
