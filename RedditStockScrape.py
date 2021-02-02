import praw
import requests
import string
import pandas as pd
import re
from bs4 import BeautifulSoup

#Reddit PRAW Config 
reddit = praw.Reddit(client_id = 'jnUjpAgZlu37mQ', client_secret = 'tjOmUVA_F96Hz-WWgqSUwMtT6DnXLg', username = 'deepfriedhotdobpraw', password = 'prawpassword1', user_agent = 'stock_praw')
subreddit = reddit.subreddit('wallstreetbets')
hot_votes = subreddit.hot()

#Stock ticker Config
company_name = []
company_ticker = []
reddit_tickers = []
NYSE_URL = 'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies='
NASDAQ_URL = 'https://www.advfn.com/nasdaq/nasdaq.asp?companies='

#Scrape all NASDAQ/NYSE tickers and company names
def scrape_stock_symbols(Letter, URL):
    
    Letter =  Letter.upper()
    URL =  URL + Letter
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    odd_rows = soup.find_all('tr', attrs= {'class':'ts0'})
    even_rows = soup.find_all('tr', attrs= {'class':'ts1'})
    
    for i in odd_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())
    
    for i in even_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())
    
    return (company_name, company_ticker)

for char in string.ascii_uppercase:
    (temp_name,temp_ticker) = scrape_stock_symbols(char, NYSE_URL)

for char in string.ascii_uppercase:
    (temp_name,temp_ticker) = scrape_stock_symbols(char, NASDAQ_URL)

#Store all stock tickers in a dataframe
data = pd.DataFrame(columns = ['company_name',  'company_ticker']) 
data['company_name'] = company_name
data['company_ticker'] = company_ticker
data = data[data['company_name'] != '']

#Scrape Reddit posts/comments 
for posts in hot_votes:
    if not posts.stickied: 
        try:
            
            print('Title : {}'.format(posts.title.encode("utf-8" , errors="ignore")))
            print('Score : {} , Ratio : {}' .format(posts.score, posts.upvote_ratio))
            posts.comments.replace_more(limit=0) #Takes all comments and lists them out 
            
            print("REGEX !!!!!!!!!!")
            print(re.findall(r'[$]\S*',(posts.title)))
            reddit_tickers.append(re.findall(r'[$]\S*',(posts.title)))
            
            for comment in posts.comments.list():
                print(20 * '-')
                print(comment.body.encode("utf-8", errors='ignore'))
                print('Comment Score : {} ' .format(comment.score)) 
            
        except praw.exceptions.PRAWException as e:
            pass

#Regular expression stock ticker extraction
