import pandas as pd
import psycopg2
import numpy as np
import json

# PostgreSQL connection config
PG_CONFIG = {
    "host": "postgres",
    "dbname": "social_data",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}


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
                conn.rollback()  # Critical to reset transaction state

        conn.commit()
        print(f"✅ Loaded {len(df)} rows into {table_name}")

    finally:
        cur.close()
        conn.close()


def run_load():
    # Load users
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

    # Load posts
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

    # Load comments
    df_comments = pd.read_json("dags/data/postComments_transformed.json")

    # Ensure all column names are lowercase
    df_comments.columns = [col.lower() for col in df_comments.columns]

    # Cast float values to boolean where needed
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

    # Load likes
    df_likes = pd.read_json("dags/data/postLikes_transformed.json")
    df_likes.columns = [col.lower() for col in df_likes.columns]

    likes_schema = """
        _id TEXT PRIMARY KEY,
        createdat BIGINT,
        liker JSONB,
        post JSONB
    """
    likes_columns = ["_id", "createdat", "liker", "post"]
    insert_dataframe(df_likes, "likes_cleaned", likes_schema, likes_columns)


# Run it
if __name__ == "__main__":
    run_load()
