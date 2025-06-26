import pandas as pd
import numpy as np
import json

# ----------------- USERS ------------------
def transform_users(json_path):
    # Load the JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(users)

    # Ensure numeric conversion
    df['followersCount'] = pd.to_numeric(df['followersCount'], errors='coerce')
    df['followingCount'] = pd.to_numeric(df['followingCount'], errors='coerce')

    # Calculate follower/following ratio
    df['follower_following_ratio'] = np.where(
        df['followingCount'] > 0,
        df['followersCount'] / df['followingCount'],
        np.nan
    )
    # Replacing all null values with zeros
    df['follower_following_ratio'].fillna(0, inplace=True)

    # Round to whole number (integer)
    df['follower_following_ratio'] = df['follower_following_ratio'].round(0).astype(int)

    # Drop unwanted fields
    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df

# ----------------- POSTS ------------------
def transform_posts(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Ensure numeric conversion
    df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce')
    df['repostsCount'] = pd.to_numeric(df['repostsCount'], errors='coerce')
    df['viewsCount'] = pd.to_numeric(df['viewsCount'], errors='coerce')
    df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce')

    # Clean attachments (stringified JSON)
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

    return df

