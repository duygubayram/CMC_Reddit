import praw
import pandas as pd

#public posts don't need username and password
reddit = praw.Reddit(
    client_id = "",
    client_secret = "",
    user_agent="LGBTQSentComm",
    #username="USERNAME",
    #password=password
)

# ordered by comment count
posts = ["zqh1e2", "qbxdux", "xe60d8", "sk86oc", "yt6p9y"]
comments_list = []

# https://praw.readthedocs.io/en/latest/tutorials/comments.html
# https://stackoverflow.com/questions/49151084/how-to-implement-a-dfs-to-the-reddit-praw
for post in posts:
    submission = reddit.submission(post)
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    while comment_queue:
        comment = comment_queue.pop(0)
        comments_list.append(comment.body)
        #print(comment.body+"\n---")
        comment_queue[0:0] = comment.replies
    comments_list.append("next post")
    #print("\n***\n")

df = pd.DataFrame(comments_list, columns=["comments"])

print(df)
df.to_excel("Comments.xlsx")