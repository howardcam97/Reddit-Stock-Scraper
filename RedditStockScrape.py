import praw

#Reddit PRAW Config 
reddit = praw.Reddit(client_id = 'jnUjpAgZlu37mQ', client_secret = 'tjOmUVA_F96Hz-WWgqSUwMtT6DnXLg', username = 'deepfriedhotdobpraw', password = 'prawpassword1', user_agent = 'stock_praw')
subreddit = reddit.subreddit('wallstreetbets')
hot_votes = subreddit.hot()

for posts in hot_votes:
    if not posts.stickied: 
        print('Title : {}'.format(posts.title))
        print('Score : {} , Ratio : {}' .format(posts.score, posts.upvote_ratio))

