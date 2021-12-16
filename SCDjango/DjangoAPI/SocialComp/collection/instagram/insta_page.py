import time
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
import datetime
# import insta_post
import random
from . import insta_post
# from selenium.webdriver.common.action_chains import ActionChains


class Insta_Page:
    ###############################################################
    # FB_Page - Class                                             #
    # Implemented by Ryan Cheng                                   #
    # Description:                                                #
    #   Class for an Instagram page                               #
    #   Used for collecting data from Instagram                   #
    #   posts from a specific brand.                              #
    #                                                             #
    # Inputs:                                                     #
    #   brand_name - the name of the instagram account, ie 'oreo' #
    #   date_range - the range of dates to collect posts from     #
    ###############################################################

    def __init__(self, brand_name, date_range, query_id):
        # Class initializing function

        # Webdriver Options
        mobile_emulation = {"deviceName": "Nexus 5"}
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--incognito')
        options.add_experimental_option('mobileEmulation', mobile_emulation)


        # Class variables
        self.driver = webdriver.Chrome(options=options)
        self.brand_name = brand_name
        self.startDate = date_range[0]
        self.endDate = date_range[1]
        self.divs = []
        self.posts = []
        self.url_list = []

        # self.driver.quit()
        # self.login()
        # self.retrieve_urls()
        self.retrieve_posts()
        self.parse_divs()

    # Login function is currently not necessary, however running too many post requests will occasionally ask for login. Once logged
    # in, date published is no longer visible and is instead dynamic -- will find workaround later
    def login(self):
        # email = input("Enter email: ")
        # password = input("Enter password: ")
        username = "socialcompfb190"
        password = "SCFacebook123"
        self.driver.get('https://www.instagram.com/accounts/login/')
        username_box = self.driver.find_element_by_name('username')
        # username_box = self.driver.find_element_by_name('username')
        username_box.send_keys(username)
        time.sleep(1)

        password_box = self.driver.find_element_by_name('password')
        # password_box = self.driver.find_element_by_name('password')
        password_box.send_keys(password)
        time.sleep(1)

        login_box = self.driver.find_element_by_class_name('sqdOP  L3NKy   y3zKF     ')
        login_box.click()
        time.sleep(5)

        self.driver.quit()

    def retrieve_urls(self):
        # Retrieve the URLs of posts that we will collect data for

        account_url = "https://www.instagram.com/" + self.brand_name + "/"

        self.driver.get(account_url)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        divs = soup.findAll('div', {"class": "v1Nh3 kIKUG  _bz0w"})

        for item in divs:
            self.url_list.append(item.find('a').get('href'))
            print(item)

    def retrieve_posts(self):
        # Retrieve the posts that we will collect data for
        print("Beginning data retrieval for ", self.brand_name)
        print("Collecting posts since ", self.startDate)
        print("Collecting posts until ", self.endDate)

        """
        for url in self.url_list:
            post = insta_post.Insta_Post(url, self.driver)
            post.create_soup()
            post.scrape_post()
            post.print()
            delay = random.randrange(30, 60)
            time.sleep(delay)


        """
        # -- Currently working on updating this --
        account_url = "https://www.instagram.com/" + self.brand_name + "/"
        self.driver.get(account_url)

        scroll_pause = 1
        screen_height = self.driver.execute_script("return window.screen.height;")
        scroll_count = 0
        i = 1
        scrolling = True

        # Scroll while posts are within date range
        while scrolling:
            # Scroll one screens worth of height at a time
            self.driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause)
            # Update scroll height each time after the page is scrolled, as the scroll height can change after doing so
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")

            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            temp_divs = soup.find_all('div', {"class": "_3drp"})

            # Add div of post only if we haven't already done so
            for temp in temp_divs:
                if temp not in self.divs:
                    self.divs.append(temp)

            print("Number of posts gathered:\t" + str(len(self.divs)))
            scroll_count += 1
            if scroll_count > 20:
                scrolling = False

            # Scrape dates on page, breaking out of the loop if we find a date before the beginning of our date range
            for div in self.divs:
                # get the Unix time (lot of string splicing required)
                timeString = div.find('article').get('data-store')
                idx = timeString.find('publish_time')
                timeString = timeString[idx:]
                idx = timeString.find("story_name")
                timeString = timeString[:idx]
                timeString = timeString.split(":", 1)[1]
                timeString = timeString.split(",", 1)[0]

                # convert Unix time string to datetime object
                date = datetime.date.fromtimestamp(int(timeString))

                # Break loop when we find a post before our date range
                if date < self.startDate:
                    scrolling = False

        self.driver.quit()


    def store_posts(self, item):
        url = item.find('a').get('href')
        print(url)


        likes = item.find('span', {"class": "like_def _28wy"})
        likes = str(likes)
        likes = likes.split(">", 1)[1]
        self.likes = likes.split(" Likes", 1)[0]
        print(self.likes)


    def parse_divs(self):
        # Parse the posts and add them to a list
        for div in self.divs:
            post = insta_post.FB_Post(div, self.brand_name)
            post.scrape_post()
            self.posts.append(post)

        for post in self.posts:
            if post.date < self.startDate or post.date > self.endDate:
                self.posts.remove(post)
            else:
                post.print()
                post.save_post(self.query_id)