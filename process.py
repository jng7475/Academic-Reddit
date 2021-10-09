import praw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class MainProcess():
    def __init__(self, college_name):
        self.college_name = college_name

    def get_subreddit_name(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(PATH, options=options)
        #search the school's subreddit on google
        driver.get("https://www.google.com/")
        driver.implicitly_wait(5)
        search_bar = driver.find_element_by_name('q')
        search_bar.send_keys(self.college_name+" subreddit")
        search_bar.send_keys(Keys.RETURN)
        #Choose the first result
        results = driver.find_elements_by_xpath('//div[@class="yuRUbf"]/a/h3')  # finds webresults
        results[0].click() # clicks the first one
        #get the exact subreddit's name without /r
        subreddit_name = driver.find_element_by_class_name('_33aRtz9JtW0dIrBNKFAl0y').text
        subreddit_name_variable = subreddit_name[2:]
        return subreddit_name_variable

    def get_subreddit_data(self):
            #get data from the chosen subreddit
        reddit = praw.Reddit(client_id='gOvMlso5eSn1FOScDhBYxg', client_secret='0agQ0Sf7X0_x-_84lvOHApYem5gOZw', user_agent='UTD_data')
        #top 20 posts
        hot_posts = reddit.subreddit(self.get_subreddit_name()).hot(limit=20)
        tags = []
        titles = []
        content = []
        #get title for each post
        for post in hot_posts:
            if post.selftext == "":
                continue
            titles.append(post.title)
            tags.append(post.link_flair_text)
            content.append(post.selftext)
            if len(titles) == 10:
                break
        return [titles, tags, content]
 
    def get_posts(self):
        acaPosts = []
        nonAcaPosts = []
        acaTitles = []
        nonAcaTitles = []
        academic_posts = 0
        non_academic_posts = 0
        subreddit_titles = self.get_subreddit_data()[0]
        subreddit_tags = self.get_subreddit_data()[1]
        subreddit_contents = self.get_subreddit_data()[2]
        for i in range(len(subreddit_tags)):
            is_academic = False
            if subreddit_tags[i] == 'Question: Academics':
                academic_posts +=1
                is_academic = True
                acaTitles.append(subreddit_titles[i])
                acaPosts.append(subreddit_contents[i])
            if not is_academic:
                non_academic_posts += 1
                nonAcaTitles.append(subreddit_titles[i])
                nonAcaPosts.append(subreddit_contents[i])
        return [academic_posts, non_academic_posts, acaTitles, acaPosts, nonAcaTitles, nonAcaPosts]

       
