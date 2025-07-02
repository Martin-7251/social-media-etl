# Import libraries
import pandas as pd
import numpy as np
import json

# ----------------- USERS ------------------
def transform_users(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    df = pd.DataFrame(users)

    df['followersCount'] = pd.to_numeric(df['followersCount'], errors='coerce')
    df['followingCount'] = pd.to_numeric(df['followingCount'], errors='coerce')

    df['follower_following_ratio'] = np.where(
        df['followingCount'] > 0,
        df['followersCount'] / df['followingCount'],
        np.nan
    )

    df['follower_following_ratio'].fillna(0, inplace=True)
    df['follower_following_ratio'] = df['follower_following_ratio'].round(0).astype(int)

    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df

# ----------------- POSTS ------------------
def transform_posts(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    df = pd.DataFrame(posts)

    # Drop rows where 'text' is null or missing
    df.dropna(subset=['text'], inplace=True)

    # Convert numeric fields
    df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce')
    df['repostsCount'] = pd.to_numeric(df['repostsCount'], errors='coerce')
    df['viewsCount'] = pd.to_numeric(df['viewsCount'], errors='coerce')
    df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce')

    def parse_attachments(x):
        try:
            return json.loads(x) if isinstance(x, str) else x
        except Exception:
            return []

    df['attachments'] = df['attachments'].apply(parse_attachments)

    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df

# ----------------- POST COMMENTS ------------------
def transform_comments(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        comments = json.load(f)

    df = pd.DataFrame(comments)

    df['likesCount'] = pd.to_numeric(df.get('likesCount', 0), errors='coerce')
    df['childCommentsCount'] = pd.to_numeric(df.get('childCommentsCount', 0), errors='coerce')

    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df

# ----------------- POST LIKES ------------------
def transform_post_likes(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        likes = json.load(f)

    df = pd.DataFrame(likes)

    df.drop(columns=['_class'], inplace=True, errors='ignore')

    # Extract post_id from post dict
    df['post_id'] = df['post'].apply(
        lambda post: post.get('_id') if isinstance(post, dict) else None
    )

    # Extract liker_id from liker dict
    df['liker_id'] = df['liker'].apply(
        lambda liker: liker.get('_id') if isinstance(liker, dict) else None
    )

    # Rename _id to id
    df['id'] = df['_id']

    # Return final DataFrame
    return df[['id', 'liker_id', 'post_id', 'createdAt']]
