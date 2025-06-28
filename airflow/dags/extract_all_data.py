# extract_all_data.py

# Import required libraries
import json               # To read JSON files
import os                 # For file path operations
import psycopg2           # PostgreSQL database connector
import mysql.connector    # MySQL database connector
from pymongo import MongoClient  # MongoDB client

def load_all_data():
    # Define the path to the directory containing JSON data files
    DATA_DIR = "/opt/airflow/dags/data"

    # Utility function to load JSON data from a file
    def load_json(filename):
        path = os.path.join(DATA_DIR, filename)  # Construct full file path
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            # Raise an error if the file is missing or empty
            raise FileNotFoundError(f"❌ File not found or empty: {filename}")
        with open(path, "r") as f:
            return json.load(f)  # Load and return JSON data

    # -----------------------------------------------
    # 📦 Step 1: Load Users into MongoDB
    # -----------------------------------------------
    mongo_client = MongoClient("mongodb://admin:admin@mongodb:27017/")  # Connect to MongoDB
    mongo_db = mongo_client["social_media"]  # Use the 'social_media' database
    mongo_users = mongo_db["users"]          # Use the 'users' collection
    users = load_json("User.json")           # Load user data from JSON file
    mongo_users.delete_many({})              # Clear existing documents
    mongo_users.insert_many(users if isinstance(users, list) else [users])  # Insert new data
    print(f"✅ Inserted {len(users)} users into MongoDB")

    # -----------------------------------------------
    # 📝 Step 2: Load Posts into PostgreSQL
    # -----------------------------------------------
    pg_conn = psycopg2.connect(
        host="postgres",
        dbname="social_data",
        user="airflow",
        password="airflow"
    )  # Connect to PostgreSQL
    pg_cur = pg_conn.cursor()
    pg_cur.execute("DROP TABLE IF EXISTS posts")  # Drop table if exists (clean slate)
    pg_cur.execute("""
        CREATE TABLE posts (
            _id TEXT PRIMARY KEY,
            text TEXT,
            postOwner_id TEXT,
            createdAt TEXT
        )
    """)  # Create new table for posts
    posts = load_json("posts.json")  # Load post data
    for post in posts:
        pg_cur.execute("""
            INSERT INTO posts (_id, text, postOwner_id, createdAt)
            VALUES (%s, %s, %s, %s)
        """, (
            post.get('_id'),
            post.get('text'),
            post.get('postOwner', {}).get('_id'),  # Nested structure
            post.get('createdAt')
        ))  # Insert each post into the table
    pg_conn.commit()       # Save changes
    pg_cur.close()
    pg_conn.close()
    print(f"✅ Inserted {len(posts)} posts into PostgreSQL")

    # -----------------------------------------------
    # 💬 Step 3: Load Comments into MySQL
    # -----------------------------------------------
    my_conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="social_data"
    )  # Connect to MySQL
    my_cur = my_conn.cursor()
    my_cur.execute("DROP TABLE IF EXISTS post_comments")  # Drop existing table
    my_cur.execute("""
        CREATE TABLE post_comments (
            _id VARCHAR(255) PRIMARY KEY,
            comment TEXT,
            commentor_id TEXT,
            post_id TEXT,
            createdAt TEXT
        )
    """)  # Create table for post comments
    comments = load_json("postComments.json")  # Load comments data
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
        ))  # Insert each comment
    my_conn.commit()  # Save changes
    print(f"✅ Inserted {len(comments)} comments into MySQL")

    # -----------------------------------------------
    # ❤️ Step 4: Load Likes into MySQL
    # -----------------------------------------------
    my_cur.execute("DROP TABLE IF EXISTS post_likes")  # Drop existing likes table
    my_cur.execute("""
        CREATE TABLE post_likes (
            _id VARCHAR(255) PRIMARY KEY,
            liker_id TEXT,
            post_id TEXT,
            createdAt TEXT
        )
    """)  # Create table for likes
    likes = load_json("postLikes.json")  # Load likes data
    for l in likes:
        my_cur.execute("""
            INSERT INTO post_likes (_id, liker_id, post_id, createdAt)
            VALUES (%s, %s, %s, %s)
        """, (
            l.get('_id'),
            l.get('liker', {}).get('_id'),
            l.get('post', {}).get('_id'),
            l.get('createdAt')
        ))  # Insert each like
    my_conn.commit()  # Save changes
    my_cur.close()
    my_conn.close()
    print(f"✅ Inserted {len(likes)} likes into MySQL")
