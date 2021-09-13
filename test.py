import praw
from selenium import webdriver
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class MainProcess():
    def __init__(self, college_name):
        self.college_name = college_name

    def get_subreddit_name(self):
        PATH = 'C:\Program Files (x86)\chromedriver.exe'
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

        hot_posts = reddit.subreddit(self.get_subreddit_name()).hot(limit=20)
        titles = []
        for post in hot_posts:
            if post.selftext == "":
                continue
            titles.append(post.title)
            if len(titles) == 10:
                break
        return titles

    academic_word_list = ["learn", "study", "learning", "elearning", 
                        "class", "classes", "coding", "major", "minor",
                        "CS", "PHYS", "MATH", "Internships", "lecture",
                        "books", "Computer Science"]

    def get_number(self):
        academic_posts = 0
        non_academic_posts = 0
        subreddit_titles = self.get_subreddit_data()
        for title in subreddit_titles:
            for word in MainProcess.academic_word_list:
                is_academic = False
                if word in title:
                    academic_posts +=1
                    is_academic = True
                    break
            if not is_academic:
                non_academic_posts += 1
        return [academic_posts, non_academic_posts]

    def get_posts(self):
        reddit = praw.Reddit(client_id='gOvMlso5eSn1FOScDhBYxg', client_secret='0agQ0Sf7X0_x-_84lvOHApYem5gOZw', user_agent='UTD_data')

        posts = reddit.subreddit(self.get_subreddit_name()).hot(limit=20)
        acaPosts = []
        nonAcaPosts = []
        acaTitles = []
        nonAcaTitles = []
        for post in posts:
            if post.selftext == "":
                continue
            for word in MainProcess.academic_word_list:
                is_academic = False
                if word in post.title:
                    acaTitles.append(post.title)
                    acaPosts.append(post.selftext)
                    is_academic = True
                    break
            if not is_academic:
                nonAcaTitles.append(post.title)
                nonAcaPosts.append(post.selftext)
            if len(acaPosts) + len(nonAcaPosts) == 10:
                break
        return acaTitles, acaPosts, nonAcaTitles, nonAcaPosts



a = MainProcess("UTD")
l1, l2, l3, l4 = a.get_posts()
print(l4)