from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pendulum import timezone

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1, tzinfo=timezone("Africa/Nairobi")),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Task 1: Extract
def run_extract():
    from extract_all_data import load_all_data
    load_all_data()

# Task 2: Transform
def run_transform():
    from transform_all_data import (
        transform_users,
        transform_posts,
        transform_comments,
        transform_post_likes
    )
    import pandas as pd

    print("🔄 Transforming Users...")
    df_users = transform_users("dags/data/User.json")
    df_users.to_json("dags/data/User_transformed.json", orient="records", indent=2)

    print("🔄 Transforming Posts...")
    df_posts = transform_posts("dags/data/posts.json")
    df_posts.to_json("dags/data/posts_transformed.json", orient="records", indent=2)

    print("🔄 Transforming Post Comments...")
    df_comments = transform_comments("dags/data/postComments.json")
    df_comments.to_json("dags/data/postComments_transformed.json", orient="records", indent=2)

    print("🔄 Transforming Post Likes...")
    df_likes = transform_post_likes("dags/data/postLikes.json")
    df_likes.to_json("dags/data/postLikes_transformed.json", orient="records", indent=2)

    print("✅ Transformation complete.")

# Task 3: Load
def run_load():
    from load_to_postgres import run_load
    run_load()

# Define DAG
with DAG(
    dag_id='Extract_transform_load',
    default_args=default_args,
    description='Extract, Transform, and Load social media data',
    schedule_interval="0 12 * * 3",
    # timezone=timezone("Africa/Nairobi"),
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_all_data',
        python_callable=run_extract
    )

    transform_task = PythonOperator(
        task_id='transform_all_data',
        python_callable=run_transform
    )

    load_task = PythonOperator(
        task_id='load_transformed_to_postgres',
        python_callable=run_load
    )

    extract_task >> transform_task >> load_task
