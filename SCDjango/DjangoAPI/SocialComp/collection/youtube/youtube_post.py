import time

from bs4 import BeautifulSoup
from spacy_langdetect import LanguageDetector
from spacy.language import Language
import spacy
import requests
import datetime

from SocialComp.serializers import PostSerializer
from ...models import PostModel


def get_lang_detector(nlp, name):
    return LanguageDetector()


class YouTubePost:
    ###############################################################
    # YouTubePost - Class                                         #
    #                                                             #
    # Description:                                                #
    #   Youtube post data and methods                             #
    #   Used for collecting data from a specific youtube post     #
    #                                                             #
    # Inputs:                                                     #
    #   url        - the url of the post to collect data from     #
    #   date_range - the date range to collect posts in           #
    #   driver     - webdriver from insta_user class              #
    ###############################################################

    def __init__(self, url, date_range, driver):

        # Class initialization function

        self.webdriver = driver
        self.date_range = date_range
        self.url = url
        self.title = ''
        self.description = ''
        self.thumbnail = ''
        self.channel = ''
        self.date = ''
        self.views = 0
        self.comments = 0
        self.likes = 0
        self.include_post = False

    def collect_post(self):
        # Collects information from the post
        # Returns true or false if the post is within our date range

        nlp = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        nlp.add_pipe('language_detector', last=True)
        content = requests.get("https://www.youtube.com" + self.url).text
        soup = BeautifulSoup(content, 'lxml')
        meta_data = soup.findAll("div")[0]
        title_and_channel = meta_data.findAll(itemprop="name")
        likes_pre_parse = content[:content.rfind(' likes"')]
        
        self.title = title_and_channel[0].get('content')
        self.channel = title_and_channel[1].get('content')
        self.description = meta_data.find(itemprop="description").get('content')
        self.views = meta_data.find(itemprop="interactionCount").get('content')
        self.url = meta_data.find(itemprop="url").get('href')
        self.thumbnail = meta_data.find(itemprop="thumbnailUrl").get('href')
        self.date = meta_data.find(itemprop="datePublished").get('content')
        self.likes = likes_pre_parse[likes_pre_parse.rfind('"') + 1:].replace(',', "")
        
        self.webdriver.get(self.url)
        self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        comments = self.webdriver.find_elements_by_tag_name('h2')

        if len(comments) == 2:
            comments = comments[1].text

            if comments != "Comments":
                comments = comments[comments.rfind(' '):]
                comments = comments.replace(' ', "")
                comments = comments.replace(',', "")
                self.comments = int(comments)

            else:
                self.comments = 0
        else:
            self.comments = 0

        year = int(self.date[:4])
        month = int(self.date[5:7])
        day = int(self.date[8:])

        post_datetime = datetime.date(year, month, day)
        lang = nlp(self.title)
        out_of_date_range = False
        
        if self.date_range[0] >= post_datetime and self.date_range[1] <= post_datetime:
            out_of_date_range = True

       
        if lang._.language['language'] != 'en' or out_of_date_range:
            
            self.include_post = False

        if out_of_date_range:
            self.include_post = False
        
        else:
            self.include_post = True

        #self.webdriver.close()

        if self.date_range[0] > post_datetime:
            return False
        else:
            return True

    def save_post(self, query_id):

        post_data = {}
        post_data['QueryId'] = str(query_id)
        post_data['url'] = str(self.url)
        post_data['title'] = str(self.title)[0:99]
        post_data['description'] = str(self.description)
        post_data['thumbnail'] = str(self.thumbnail)
        post_data['channel'] = str(self.channel)
        post_data['date'] = str(self.date)
        post_data['views'] = str(self.views)
        post_data['comments'] = str(self.comments)
        post_data['likes'] = str(self.likes)

        post_serializer = PostSerializer(data = post_data)

        if post_serializer.is_valid():
            post_serializer.save()

        else:
            print(post_serializer.errors)
            