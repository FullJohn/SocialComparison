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

    def parse_post(self, vid_item):
        # Parse video item
        self.postId = vid_item['id']
        self.description = vid_item['desc']
        self.dateCreated = datetime.fromtimestamp(int(vid_item['createTime']))
        self.playCount = vid_item['stats']['playCount']
        self.likeCount = vid_item['stats']['diggCount']
        self.shareCount = vid_item['stats']['shareCount']
        self.commentCount = vid_item['stats']['commentCount']
        self.playUrl = vid_item['video']['playAddr']
        self.downloadUrl = vid_item['video']['downloadAddr']

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
        print("\n\n")

    def save_post(self):
        post_data = {'brand': str(self.brand),
                     'playUrl': str(self.playUrl),
                     'description': str(self.description),
                     'date': str(self.dateCreated),
                     'likes': str(self.likeCount),
                     'views': str(self.playCount),
                     'comments': str(self.commentCount),
                     'shares': str(self.shareCount)}

        post_serializer = PostSerializer(data=post_data)

        if post_serializer.is_valid():
            post_serializer.save()

        else:
            print(post_serializer.errors)
