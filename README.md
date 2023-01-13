# CMC_Reddit

This is a simple project to pull posts from Reddit according to the listed filters, and to pull comments from selected posts with a depth-first approach using PRAW.

filters:
  subreddit: askgaybros
  keywords: qatar, fifa, world cup
  post pull limit: 100 per keyword
  post type: thread (t3)
  sort: controversial
  dropped if "Not a question" flair
  posts with 10+ comments only
  
  You can find our codebook (annotation guidelines) and annotated data in the "annotation and data" folder.
