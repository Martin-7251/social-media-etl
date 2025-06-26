# extract_all_data.py
import json
import os
import psycopg2
import mysql.connector
from pymongo import MongoClient

def load_all_data():
    DATA_DIR = "/opt/airflow/dags/data"

    def load_json(filename):
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            raise FileNotFoundError(f"❌ File not found or empty: {filename}")
        with open(path, "r") as f:
            return json.load(f)

    # MongoDB - Users
    mongo_client = MongoClient("mongodb://admin:admin@mongodb:27017/")
    mongo_db = mongo_client["social_media"]
    mongo_users = mongo_db["users"]
    users = load_json("User.json")
    mongo_users.delete_many({})
    mongo_users.insert_many(users if isinstance(users, list) else [users])
    print(f"✅ Inserted {len(users)} users into MongoDB")

    # PostgreSQL - Posts
    pg_conn = psycopg2.connect(
        host="postgres",
        dbname="social_data",
        user="airflow",
        password="airflow"
    )
    pg_cur = pg_conn.cursor()
    pg_cur.execute("DROP TABLE IF EXISTS posts")
    pg_cur.execute("""
        CREATE TABLE posts (
            _id TEXT PRIMARY KEY,
            text TEXT,
            postOwner_id TEXT,
            createdAt TEXT
        )
    """)
    posts = load_json("posts.json")
    for post in posts:
        pg_cur.execute("""
            INSERT INTO posts (_id, text, postOwner_id, createdAt)
            VALUES (%s, %s, %s, %s)
        """, (
            post.get('_id'),
            post.get('text'),
            post.get('postOwner', {}).get('_id'),
            post.get('createdAt')
        ))
    pg_conn.commit()
    pg_cur.close()
    pg_conn.close()
    print(f"✅ Inserted {len(posts)} posts into PostgreSQL")

    # MySQL - Comments
    my_conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="social_data"
    )
    my_cur = my_conn.cursor()
    my_cur.execute("DROP TABLE IF EXISTS post_comments")
    my_cur.execute("""
        CREATE TABLE post_comments (
            _id VARCHAR(255) PRIMARY KEY,
            comment TEXT,
            commentor_id TEXT,
            post_id TEXT,
            createdAt TEXT
        )
    """)
    comments = load_json("postComments.json")
    for c in comments:
        my_cur.execute("""
            INSERT INTO post_comments (_id, comment, commentor_id, post_id, createdAt)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            c.get('_id'),
            c.get('comment'),
            c.get('commentor', {}).get('_id'),
            c.get('postId'),
            c.get('createdAt')
        ))
    my_conn.commit()
    print(f"✅ Inserted {len(comments)} comments into MySQL")

    # MySQL - Likes
    my_cur.execute("DROP TABLE IF EXISTS post_likes")
    my_cur.execute("""
        CREATE TABLE post_likes (
            _id VARCHAR(255) PRIMARY KEY,
            liker_id TEXT,
            post_id TEXT,
            createdAt TEXT
        )
    """)
    likes = load_json("postLikes.json")
    for l in likes:
        my_cur.execute("""
            INSERT INTO post_likes (_id, liker_id, post_id, createdAt)
            VALUES (%s, %s, %s, %s)
        """, (
            l.get('_id'),
            l.get('liker', {}).get('_id'),
            l.get('post', {}).get('_id'),
            l.get('createdAt')
        ))
    my_conn.commit()
    my_cur.close()
    my_conn.close()
    print(f"✅ Inserted {len(likes)} likes into MySQL")
