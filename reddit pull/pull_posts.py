'''
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

~~To run this code for yourself:
Get your Reddit API token: https://www.reddit.com/prefs/apps
Enter your "personal use script" on CLIENT_ID
Enter your "secret" on SECRET_KEY
Enter your Reddit username on "username"
Write your Reddit password in a text file, add path to the "with open" function

~~Pulled posts restrictions:
  subreddit: askgaybros
  keywords: qatar, fifa, world cup
  post pull limit: 100 per keyword
  post type: thread (t3)
  sort: controversial
  dropped if "Not a question" flair
  posts with 10+ comments only
'''

import requests
import pandas as pd

#sets df print limits
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 12)

#set your CLIENT_ID and SECRET_KEY tokens
CLIENT_ID = ''
SECRET_KEY = ''

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

#reads password file, replace password.txt with your path
with open('password.txt', 'r') as f:
    password = f.read()

# here we pass our login method (password), username, and password
#replace your_username with your username
data = {'grant_type': 'password',
        'username': 'your_username',
        'password': password}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'LGBTQSent/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

#set search keywords
keywords = ['qatar', 'fifa', 'world_cup']

#create empty dataframe
df = pd.DataFrame()

#pull posts
#if you want to pull from multiple specific subreddits, you can use a similar method as keywords
#if you don't want to specify any subreddits, you can delete /r/{subreddit} and &restrict_sr=on
for key in keywords:
    res = requests.get(f"https://oauth.reddit.com/r/AskGayBros/search.json?q={key}&restrict_sr=on&sort=controversial",
                 headers=headers, params= {'limit':'100',
                                          'kind':'t3'})
    for post in res.json()['data']['children']:
        df = df.append({
            'id': post['kind'] + '_' + post['data']['id'],
            'subreddit': post['data']['subreddit'],
            # 'time' : post['data']['created_utc'],
            'title': post['data']['title'],
            'body': post['data']['selftext'],
            'comments': post['data']['num_comments'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'upvotes': post['data']['ups'],
            'downvotes': post['data']['downs'],
            'score': post['data']['score'],
            'flair': post['data']['link_flair_text'],
            'url': post['data']['url']
            # 'content_categories' : post['data']['content_categories'],
            # 'link_flair_type' : post['data']['link_flair_type'],
            # 'discussion_type' : post['data']['discussion_type']
            # 'comments' : post['data']['comments']
        },
            ignore_index=True)


#to see which keys are available
#print(res.json()['data'].keys())
#print(post['data'].keys())

#restrict comment count, drop duplicates, drop posts with "not a question" flair
df = df[df.comments >= 10]
#df = df[df.comments <= 100]
df.drop_duplicates()
df = df[df.flair != 'Not a question']
print(df)
print(df.shape)

#write to csv file
df.to_csv('CollectedPosts', sep=',', encoding='utf-8')
