# visualize_data.py
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Load transformed data ----------------
df_users = pd.read_json("airflow/dags/data/User_transformed.json")
df_posts = pd.read_json("airflow/dags/data/posts_transformed.json")
df_comments = pd.read_json("airflow/dags/data/postComments_transformed.json")
df_likes = pd.read_json("airflow/dags/data/postLikes_transformed.json")

# ---------------- USERS ----------------
# 1. Follower vs Following (Scatter)
plt.figure(figsize=(8, 6))
print(df_users.columns)
sns.scatterplot(data=df_users, x='followingCount', y='followersCount', hue='isAccountPrivate')
plt.title('Followers vs Following')
plt.grid(True)
plt.show()
time.sleep(5)

# 2. Account privacy distribution
privacy_counts = df_users['isAccountPrivate'].value_counts()
privacy_counts.plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Private vs Public Accounts')
plt.ylabel('')
plt.show()
time.sleep(5)

# 3. Top 10 Posts by Likes
top_posts = df_posts.nlargest(10, 'likesCount')[['_id', 'likesCount']]
top_posts.plot.bar(x='_id', y='likesCount', title='Top 10 Posts by Likes')
plt.xticks(rotation=45)
plt.ylabel('Likes Count')
plt.show()
time.sleep(5)

# ---------------- COMMENTS ----------------
# 4. Comments per post (Distribution)
comment_dist = df_comments['postId'].value_counts()
comment_dist.plot.hist(bins=20)
plt.title("Number of Comments per Post")
plt.xlabel("Number of Comments")
plt.ylabel("Number of Posts")
plt.grid(True)
plt.show()
time.sleep(5)

# ---------------- LIKES ----------------
# 5. Likes over time (Time Series)
df_likes['createdAt'] = pd.to_datetime(df_likes['createdAt'], unit='ms', errors='coerce')
df_likes = df_likes.dropna(subset=['createdAt'])  # Remove invalid timestamps
likes_time = df_likes['createdAt'].dt.date.value_counts().sort_index()
likes_time.plot(kind='line', title='Number of Likes Over Time')
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.ylabel("Likes")
plt.grid(True)
plt.show()
time.sleep(5)
