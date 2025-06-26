from transform_all_data_copy import (
    transform_users,
    transform_posts,
    transform_comments,
    transform_post_likes
)

def preview(title, df):
    print(f"\n🟢 {title}")
    print("-" * len(title))
    print(df.head(), "\n")
    print(f"Columns: {list(df.columns)}")
    print(f"Total records: {len(df)}\n")

def main():
    # File paths
    user_path = "airflow/dags/data/User.json"
    posts_path = "airflow/dags/data/posts.json"
    comments_path = "airflow/dags/data/postComments.json"
    likes_path = "airflow/dags/data/postLikes.json"

    # Transform each dataset
    df_users = transform_users(user_path)
    df_posts = transform_posts(posts_path)
    df_comments = transform_comments(comments_path)
    df_likes = transform_post_likes(likes_path)

    # Save transformed outputs
    df_users.to_json("airflow/dags/data/User_transformed.json", orient="records", indent=2)
    df_posts.to_json("airflow/dags/data/posts_transformed.json", orient="records", indent=2)
    df_comments.to_json("airflow/dags/data/postComments_transformed.json", orient="records", indent=2)
    df_likes.to_json("airflow/dags/data/postLikes_transformed.json", orient="records", indent=2)

    # Preview each
    preview("Transformed Users", df_users)
    preview("Transformed Posts", df_posts)
    preview("Transformed Post Comments", df_comments)
    preview("Transformed Post Likes", df_likes)

if __name__ == "__main__":
    main()
