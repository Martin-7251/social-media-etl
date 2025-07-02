# Import essential libraries
import json
import psycopg2
import pandas as pd
import numpy as np

# Configuration dictionary for connecting to PostgreSQL
PG_CONFIG = {
    "host": "postgres",
    "dbname": "social_data",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}

# General-purpose function to insert a pandas DataFrame into a PostgreSQL table
def insert_dataframe(df, table_name, schema, columns):
    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()

    try:
        print(f"📦 Creating table {table_name}...")
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cur.execute(f"CREATE TABLE {table_name} ({schema})")

        for _, row in df.iterrows():
            try:
                clean_row = []
                for val in row[columns]:
                    if isinstance(val, (list, dict)):
                        clean_row.append(json.dumps(val))
                    elif pd.isna(val):
                        clean_row.append(None)
                    else:
                        clean_row.append(val)

                placeholders = ', '.join(['%s'] * len(clean_row))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cur.execute(insert_sql, tuple(clean_row))

            except Exception as e:
                print(f"❌ Failed to insert row into {table_name}: {row[columns].tolist()}")
                print(f"Error: {e}")
                conn.rollback()

        conn.commit()
        print(f"✅ Loaded {len(df)} rows into {table_name}")

    finally:
        cur.close()
        conn.close()


# Main function to orchestrate loading all datasets into PostgreSQL
def run_load():
    # ---------------------- USERS ----------------------
    df_users = pd.read_json("dags/data/User_transformed.json")
    df_users.columns = [col.lower() for col in df_users.columns]
    df_users['follower_following_ratio'] = df_users['follower_following_ratio'].astype(np.int64)

    user_schema = """
        _id TEXT PRIMARY KEY,
        createdat TEXT,
        handle TEXT,
        bio TEXT,
        fixedusername TEXT,
        profileurl TEXT,
        followerscount BIGINT,
        followingcount BIGINT,
        isaccountprivate BOOLEAN,
        usertype INTEGER,
        emailisphonenumber INTEGER,
        follower_following_ratio BIGINT
    """
    user_columns = [
        "_id", "createdat", "handle", "bio", "fixedusername", "profileurl",
        "followerscount", "followingcount", "isaccountprivate", "usertype",
        "emailisphonenumber", "follower_following_ratio"
    ]
    insert_dataframe(df_users, "users_cleaned", user_schema, user_columns)

    # ---------------------- POSTS ----------------------
    df_posts = pd.read_json("dags/data/posts_transformed.json")
    df_posts.columns = [col.lower() for col in df_posts.columns]

    post_schema = """
        _id TEXT PRIMARY KEY,
        text TEXT,
        datecreated BIGINT,
        likescount BIGINT,
        repostscount BIGINT,
        childcount BIGINT,
        sharescount BIGINT,
        viewscount BIGINT,
        isliked BOOLEAN,
        isreposted BOOLEAN,
        isrepost BOOLEAN,
        totalattachmentcount BIGINT,
        postiscompletelyuploaded BOOLEAN,
        attachments JSONB
    """
    post_columns = [
        "_id", "text", "datecreated", "likescount", "repostscount", "childcount",
        "sharescount", "viewscount", "isliked", "isreposted", "isrepost",
        "totalattachmentcount", "postiscompletelyuploaded", "attachments"
    ]
    insert_dataframe(df_posts, "posts_cleaned", post_schema, post_columns)

    # ---------------------- COMMENTS ----------------------
    df_comments = pd.read_json("dags/data/postComments_transformed.json")
    df_comments.columns = [col.lower() for col in df_comments.columns]

    if "commentliked" in df_comments.columns:
        df_comments["commentliked"] = df_comments["commentliked"].astype(bool)

    comment_schema = """
        _id TEXT PRIMARY KEY,
        postid TEXT,
        text TEXT,
        createdat BIGINT,
        likescount BIGINT,
        childcommentscount BIGINT,
        commentliked BOOLEAN
    """
    comment_columns = [
        "_id", "postid", "text", "createdat",
        "likescount", "childcommentscount", "commentliked"
    ]
    insert_dataframe(df_comments, "comments_cleaned", comment_schema, comment_columns)

    # ---------------------- LIKES ----------------------
    df_likes = pd.read_json("dags/data/postLikes_transformed.json")
    df_likes.columns = [col.lower() for col in df_likes.columns]

    likes_schema = """
        id TEXT PRIMARY KEY,
        liker_id TEXT,
        post_id TEXT,
        createdat BIGINT
    """
    likes_columns = ["id", "liker_id", "post_id", "createdat"]

    insert_dataframe(df_likes, "likes_cleaned", likes_schema, likes_columns)


# Entry point
if __name__ == "__main__":
    run_load()
