# Import libraries
import pandas as pd        # For manipulating data
import numpy as np         # For numerical operations
import json                # For reading and parsing JSON files

# ----------------- USERS ------------------
def transform_users(json_path):
    # Load the raw JSON data from the file
    with open(json_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    # Convert the list of users (dicts) into a pandas DataFrame
    df = pd.DataFrame(users)

    # Ensure follower/following counts are numeric (convert strings or NaNs to numbers)
    df['followersCount'] = pd.to_numeric(df['followersCount'], errors='coerce')
    df['followingCount'] = pd.to_numeric(df['followingCount'], errors='coerce')

    # Compute the follower-to-following ratio
    df['follower_following_ratio'] = np.where(
        df['followingCount'] > 0,                      # Avoid division by zero
        df['followersCount'] / df['followingCount'],   # Calculate ratio
        np.nan                                          # Assign NaN if followingCount is zero or missing
    )

    # Fill missing values with 0 to avoid nulls in downstream processing
    df['follower_following_ratio'].fillna(0, inplace=True)

    # Round the ratio to the nearest whole number and convert to integer
    df['follower_following_ratio'] = df['follower_following_ratio'].round(0).astype(int)

    # Drop any unnecessary fields like '_class' that might come from MongoDB export
    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df  # Return the cleaned and enriched users DataFrame

# ----------------- POSTS ------------------
def transform_posts(json_path):
    # Load raw post data
    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Convert numeric fields to appropriate format (coerce invalid values to NaN)
    df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce')
    df['repostsCount'] = pd.to_numeric(df['repostsCount'], errors='coerce')
    df['viewsCount'] = pd.to_numeric(df['viewsCount'], errors='coerce')
    df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce')

    # Define a helper function to safely parse the 'attachments' field (which may be stringified JSON)
    def parse_attachments(x):
        try:
            return json.loads(x) if isinstance(x, str) else x  # If string, parse it
        except Exception:
            return []  # If parsing fails, return empty list

    # Apply the function to each row in the 'attachments' column
    df['attachments'] = df['attachments'].apply(parse_attachments)

    # Drop unwanted fields like '_class'
    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df  # Return the cleaned and enriched posts DataFrame

# ----------------- POST COMMENTS ------------------
def transform_comments(json_path):
    # Load raw comment data
    with open(json_path, "r", encoding="utf-8") as f:
        comments = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(comments)

    # Convert numeric fields to appropriate types
    df['likesCount'] = pd.to_numeric(df.get('likesCount', 0), errors='coerce')
    df['childCommentsCount'] = pd.to_numeric(df.get('childCommentsCount', 0), errors='coerce')

    # Drop unnecessary fields
    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df  # Return the cleaned comments DataFrame

# ----------------- POST LIKES ------------------
def transform_post_likes(json_path):
    # Load raw like data
    with open(json_path, "r", encoding="utf-8") as f:
        likes = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(likes)

    # Drop any extra fields not needed for analysis
    df.drop(columns=['_class'], inplace=True, errors='ignore')

    return df  # Return the cleaned likes DataFrame
