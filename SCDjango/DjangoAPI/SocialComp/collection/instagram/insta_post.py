import datetime
from bs4 import BeautifulSoup

from SocialComp.serializers import PostSerializer
from ...models import PostModel


class Insta_Post:
    ###############################################################
    # Insta_Post - Class                                          #
    # Implemented by Ryan Cheng                                   #
    # Description:                                                #
    #   Facebook post data and methods                            #
    #   Used for collecting data from a specific instagram post   #
    #                                                             #
    # Inputs:                                                     #
    #   post_url - the url of the post to collect data from       #
    #   driver   - webdriver from insta_page class                #
    ###############################################################

    def __init__(self, div, brand_name):

        # Class initialization function
        # self.driver = driver
        # self.soup_list = []
        # self.soup = ''

        self.div = div
        self.brand = brand_name
        self.url = ''
        self.title = 'N/A'
        self.description = ''
        self.thumbnail = ''
        self.channel = ''
        self.date = ''
        self.views = ''
        self.comments = ''
        self.likes = ''

    def create_soup(self):
        # Creates a BeautifulSoup object for parsing the HTML page
        self.driver.get("https://www.instagram.com" + self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')

    # --- Currently fixing this ---
    def scrape_post(self):
        # Parses the soup object and page_source for data
        likes = self.soup.find('a', {"class": "zV_Nj"})
        if likes is None:
            likes = self.soup.find('span', {"class": "vcOH2"})

        self.likes = likes.find('span').text.replace(',', '')
        """
        self.brand = self.soup.find('a', {"class": "sqdOP yWX7d _8A5w5 ZIAjV"}).get('href').replace('/', '')
        date = self.soup.find('a', {"class": "c-Yi7"}).find('time').get('datetime')
        self.date = date[0:date.rfind('T')]
        self.comments = self.soup.find('a', {"class": "r8ZrO"}).find('span').text
        self.description = self.soup.find('div', {"class": "QzzMF Igw0E IwRSH eGOV_ vwCYk"}).find('span').find(
            'span').text
        image_pre_parse = self.soup.findAll('img')
        self.image_url = image_pre_parse[1].get('src')
        """

        """

        # Parse url
        url = self.div.find('a', {"data-sigil": "feed-ufi-trigger"}).get('href')
        self.url = "www.facebook.com" + url

        # Parse date
        timeString = self.div.find('article').get('data-store')
        idx = timeString.find('publish_time')
        timeString = timeString[idx:]
        idx = timeString.find("story_name")
        timeString = timeString[:idx]
        timeString = timeString.split(":", 1)[1]
        timeString = timeString.split(",", 1)[0]
        # convert Unix time string to datetime object
        self.date = datetime.date.fromtimestamp(int(timeString))

        # Parse description
        desString = str(self.div.find_all('p'))
        desString = desString.split(">", 1)[1]
        desString = desString.split("<", 1)[0]
        self.description = desString

        # Parse thumbnail (for FB, image link is same as url)
        self.thumbnail = "www.facebook.com" + url

        # Parse comments
        comments = self.div.find('span', {"class": "cmt_def _28wy"})
        comments = str(comments)

        if comments:
            comments = comments.split(">", 1)[1]
            comments = comments.split(" ", 1)[0]
            comments = comments.replace(',', '')
            self.comments = comments
        else:
            self.comments = '0'

        # Parse likes
        likes = self.div.find('span', {"class": "like_def _28wy"})
        likes = str(likes)

        if likes:
            likes = likes.split(">", 1)[1]
            likes = likes.split(" ", 1)[0]
            likes = likes.replace(',', '')
            self.likes = likes
        else:
            self.likes = '0'

        # Parse views (currently just likes + comments, to find exact count need to use 3rd party API)
        views = int(self.likes) + int(self.comments)
        self.views = str(views)
        
        """



    def print(self):

        # Prints the data collected from the facebook post
        print("Post URL: ", self.url)
        print("Title: ", self.title)
        print("Description: ", self.description)
        print("Thumbnail: ", self.thumbnail)
        print("Brand: ", self.brand)
        print("Date: ", self.date)
        print("Views: ", self.views)
        print("Comments: ", self.comments)
        print("Likes: ", self.likes)
        print("\n\n")

    def save_post(self, query_id):
        # Sends post data to serializer
        post_data = {}
        post_data['QueryId'] = str(query_id)
        post_data['url'] = self.url
        post_data['title'] = self.title
        post_data['description'] = self.description
        post_data['thumbnail'] = self.thumbnail
        post_data['channel'] = self.channel
        post_data['date'] = self.date
        post_data['views'] = self.views
        post_data['comments'] = self.comments
        post_data['likes'] = self.likes


        post_serializer = PostSerializer(data = post_data)

        if post_serializer.is_valid():
            post_serializer.save()
        else:
            print(post_serializer.errors)