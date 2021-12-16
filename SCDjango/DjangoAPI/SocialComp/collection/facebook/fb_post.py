import datetime

#from SocialComp.serializers import PostSerializer
#from ...models import PostModel


class FB_Post:
    ###############################################################
    # FB_Post - Class                                             #
    # Implemented by Ryan Cheng                                   #
    # Description:                                                #
    #   Facebook post data and methods                            #
    #   Used for collecting data from a specific facebook post    #
    #                                                             #
    # Inputs:                                                     #
    #   post_url - the url of the post to collect data from       #
    #   driver   - webdriver from fb_user class                   #
    ###############################################################

    def __init__(self, div, brand_name):

        # Class initialization function
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

    def scrape_post(self):

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
