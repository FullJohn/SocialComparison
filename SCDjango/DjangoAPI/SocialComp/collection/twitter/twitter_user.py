import random
import time
import datetime
import re

import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
from . import twitter_post


class TwitterUser:
    #################################################################
    # TwitterUser - Class                                           #
    #                                                               #
    # Description:                                                  #
    #   Class for an TwitterUser user                               #
    #   Used for collecting data from Twitter                       #
    #   posts from a specific class.                                #
    #                                                               #
    # Inputs:                                                       #
    #   brand_name - the name of the Twitter account, ie 'oreo'     #
    #   date_range - the range of dates to collect posts from       #
    #                                                               #
    # Pierce Hopkins                                                #
    #################################################################

    def __init__(self, brand_name, date_range, query_id):
        # Class initializing function

        # Webdriver Options
        mobile_emulation = {"deviceName": "Nexus 5"}
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--incognito')
        options.add_experimental_option('mobileEmulation', mobile_emulation)

        # Class variables
        self.followers = '' #@TODO(P): Need to validate brand name to ensure followers are read
        
        self.driver = webdriver.Chrome(options=options)
        self.brand_name = brand_name
        self.brand_img = ''
        self.firstDate = date_range[0]
        self.lastDate = date_range[1]
        #self.date_range = firstDate - lastDate
        self.divs = []
        self.posts = []
        
        self.query_id = query_id

        self.retrieve_posts()
        self.parse_divs()

    def retrieve_posts(self):
        account_url = "https://twitter.com/" + self.brand_name + "/"

        self.driver.get(account_url)
        print("Gathering all posts between: " + self.firstDate.strftime("%b %d") + " and " + self.lastDate.strftime("%b %d"))

        scroll_pause_time = 1
        screen_height = self.driver.execute_script("return window.screen.height;")
        i = 1
        scrolling = True
        
        #@TODO(P): Make sure this doesn't enter an infinite loop if the date entered goes back further than the oldest post
        while scrolling:
            #@NOTE(P): Scroll one screens worth of height at a time
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            #@NOTE(P): Update scroll height each time after the page is scrolled, as the scroll height can change after doing so
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            temp_divs = soup.find_all("div", class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1t982j2")
            
            if(len(temp_divs) < 4):
                #<span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">969.3K</span> css-901oao css-16my406 r-1fmj7o5 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0
                temp_followers = soup.find(href = "/" + self.brand_name + "/followers" )
                #temp_followers = soup.select("css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
            
            #@NOTE(P): Add div of post only if we haven't already done so
            for temp in temp_divs:
                if temp not in self.divs:
                    self.divs.append(temp)
            
            print("Number of posts gathered:\t" + str(len(self.divs)))
            
            #@NOTE(P): Scrape dates on page, breaking out of the loop if we find a date before the beginning of our date range
            for d in range(len(self.divs)):
                time_posted = self.divs[d].find("time")
                #@NOTE(P): Twitter datetime example: 2021-09-27T18:26:32.000Z 
                temp_datetime = datetime.datetime.strptime(time_posted.attrs['datetime'], "%Y-%m-%dT%H:%M:%S.000Z")
                
                #@NOTE(P): Break the loop when we find a post before our date range
                if temp_datetime.date() < self.firstDate:
                    scrolling = False
        self.followers = temp_followers.get_text() if temp_followers else "{Error Retrieving Followers}"
        self.driver.quit()

    def parse_divs(self):
        #@NOTE(P): Parse the posts and add them to a list
        print(self.followers + "\n")
        for div in self.divs:
            post = twitter_post.TwitterPost(div, self.brand_name)
            post.followers = self.followers
            post.scrape_post()
            self.posts.append(post)
        
        for post in self.posts:
            if post.date.date() < self.firstDate or post.date.date() > self.lastDate:
                self.posts.remove(post)
            else:
                post.print()
                post.save_post(self.query_id)
