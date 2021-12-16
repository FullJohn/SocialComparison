from datetime import datetime

from SocialComp.serializers import PostSerializer
from ...models import PostModel


class TiktokPost:
    ###############################################################
    # TikTokPost - Class                                          #
    #                                                             #
    # Description:                                                #
    #   TikTok post data and methods                              #
    #   Used for parsing the data from a specific TikTok post     #
    #                                                             #
    # Inputs:                                                     #
    #   video_item - a video object ready for parsing             #
    #   brand_name - account brand name                           #
    #                                                             #
    # Web Kimoni                                                  #
    ###############################################################

    def __init__(self, brand_name):
        # Class initialization function
        self.postId = ''
        self.brand = brand_name
        self.playCount = 0
        self.likeCount = 0
        self.shareCount = 0
        self.dateCreated = ''
        self.commentCount = 0
        self.description = ''
        self.playUrl = ''
        self.downloadUrl = ''
        self.thumbnail = ''

    def parse_post(self, vid_item):
        # Parse video item
        self.postId = vid_item['id']
        self.description = vid_item['desc']
        self.dateCreated = datetime.fromtimestamp(int(vid_item['createTime'])).date()
        self.playCount = vid_item['stats']['playCount']
        self.likeCount = vid_item['stats']['diggCount']
        self.shareCount = vid_item['stats']['shareCount']
        self.commentCount = vid_item['stats']['commentCount']
        self.playUrl = 'https://www.tiktok.com/@' + self.brand + '/video/' + self.postId
        self.downloadUrl = vid_item['video']['downloadAddr']
        self.thumbnail = vid_item['video']['dynamicCover']

    def print(self):
        # Prints the data from the post
        print("Brand:\t\t", self.brand)
        print("Post ID:\t", self.postId)
        print("Description:\t", self.description)
        print("Date:\t\t", self.dateCreated)
        print("Likes:\t\t", self.likeCount)
        print("Shares:\t", self.shareCount)
        print("Comments:\t", self.commentCount)
        print("Video Views:\t", self.playCount)
        print("Play URL:\t", self.playUrl)
        print("Download URL:\t", self.downloadUrl)
        print("Thumbnail:\t\t", self.thumbnail)
        print("\n\n")

    def save_post(self, query_id):
        post_data = {'QueryId': str(query_id),
                     'url': str(self.playUrl),
                     'title': str(self.description),
                     'description': str(self.description),
                     'thumbnail': str(self.thumbnail),
                     'channel': str(self.brand),
                     'date': str(self.dateCreated),
                     'views': str(self.playCount),
                     'comments': str(self.commentCount),
                     'likes': str(self.likeCount)}

        # post_data = {'brand': str(self.brand),
        #              'playUrl': str(self.playUrl),
        #              'description': str(self.description),
        #              'date': str(self.dateCreated),
        #              'likes': str(self.likeCount),
        #              'views': str(self.playCount),
        #              'comments': str(self.commentCount),
        #              'shares': str(self.shareCount)}

        post_serializer = PostSerializer(data=post_data)

        if post_serializer.is_valid():
            post_serializer.save()

        else:
            print(post_serializer.errors)
