import json
import requests
# import datetime
from . import tiktok_post


class TiktokUser:
    #################################################################
    # TiktokUser - Class                                            #
    #                                                               #
    # Description:                                                  #
    #   Class for an TiktokUser user                                #
    #   Used for collecting data from TikTok                        #
    #   posts from a specific class.                                #
    #                                                               #
    # Inputs:                                                       #
    #   brand_handle - the name of the TikTok account,              #
    #   i.e 'theoreoofficial' instead of 'oreos'                    #
    #   date_range - the range of dates to collect posts from       #
    #                                                               #
    # Web Kimoni                                                    #
    #################################################################

    def __init__(self, brand_handle, date_range, query_id):
        # Class initializing function
        # Class variables
        self.id = 0
        self.query_id = query_id
        self.brandName = ''
        self.brandHandle = brand_handle
        self.brandDesc = ''
        self.brandImage = ''
        self.dateRange = date_range
        self.brandLikes = 0
        self.brandFollowers = 0
        self.brandFollowing = 0
        self.vidCount = 0
        self.data = []
        self.posts = []

        self.retrieve_posts()
        self.parse_data()

    def retrieve_posts(self):
        account_url = "https://tiktok33.p.rapidapi.com/user/feed/" + self.brandHandle
        headers = {
            'x-rapidapi-host': "tiktok33.p.rapidapi.com",
            'x-rapidapi-key': "44d7dc18b7msha7cecb65b430470p110f63jsn9c77f57b3583"
        }

        response = requests.request("GET", account_url, headers=headers)
        self.data = json.loads(response.text)
        authorInfo = self.data[0]['author']
        brandInfo = self.data[0]['authorStats']
        self.id = authorInfo['id']
        self.brandName = authorInfo['nickname']
        self.brandImage = authorInfo['avatarThumb']
        self.brandDesc = authorInfo['signature']
        self.vidCount = brandInfo['videoCount']
        self.brandLikes = brandInfo['heartCount']
        self.brandFollowing = brandInfo['followingCount']
        self.brandFollowers = brandInfo['followerCount']

    def parse_data(self):
        # @NOTE(P): Parse the posts and add them to a list
        for vid in self.data:
            p = tiktok_post.TiktokPost(self.brandName)
            p.parse_post(vid)
            self.posts.append(p)

        for post in self.posts:
            if post.dateCreated < self.dateRange[0] or post.dateCreated > self.dateRange[1]:
                self.posts.remove(post)
            else:
                # post.print()
                post.save_post(self.query_id)
