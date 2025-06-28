# Import Airflow's DAG and PythonOperator classes
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import time-related utilities
from datetime import datetime, timedelta
from pendulum import timezone  # For setting the timezone

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',  # DAG owner
    'start_date': datetime(2024, 1, 1, tzinfo=timezone("Africa/Nairobi")),  # DAG start date with timezone
    'retries': 1,  # Number of retries if a task fails
    'retry_delay': timedelta(minutes=5),  # Wait time between retries
}

# ------------------------------------------
# 🧪 Task 1: Extract raw data from JSON files and load into MongoDB, MySQL, and PostgreSQL
# ------------------------------------------
def run_extract():
    from extract_all_data import load_all_data  # Import the extract function
    load_all_data()  # Run the extraction process

# ------------------------------------------
# 🧹 Task 2: Transform raw data into cleaned and structured format
# ------------------------------------------
def run_transform():
    # Import transformation functions for each dataset
    from transform_all_data import (
        transform_users,
        transform_posts,
        transform_comments,
        transform_post_likes
    )
    import pandas as pd
    
    # Transform and save the users dataset
    print("🔄 Transforming Users...")
    df_users = transform_users("dags/data/User.json")
    df_users.to_json("dags/data/User_transformed.json", orient="records", indent=2)

    # Transform and save the posts dataset
    print("🔄 Transforming Posts...")
    df_posts = transform_posts("dags/data/posts.json")
    df_posts.to_json("dags/data/posts_transformed.json", orient="records", indent=2)

    # Transform and save the comments dataset
    print("🔄 Transforming Post Comments...")
    df_comments = transform_comments("dags/data/postComments.json")
    df_comments.to_json("dags/data/postComments_transformed.json", orient="records", indent=2)

    # Transform and save the likes dataset
    print("🔄 Transforming Post Likes...")
    df_likes = transform_post_likes("dags/data/postLikes.json")
    df_likes.to_json("dags/data/postLikes_transformed.json", orient="records", indent=2)

    print("✅ Transformation complete.")

# ------------------------------------------
# 🗃️ Task 3: Load transformed data into PostgreSQL
# ------------------------------------------
def run_load():
    from load_to_postgres import run_load  # Import the load function
    run_load()  # Load cleaned data into PostgreSQL

# Define the DAG (workflow)
with DAG(
    dag_id='Extract_transform_load',  # Unique ID for the DAG
    default_args=default_args,        # Default arguments defined earlier
    description='Extract, Transform, and Load social media data',  # Description for the UI
    schedule_interval="0 12 * * 3",   # Cron schedule: every Wednesday at 12:00 PM
    # timezone=timezone("Africa/Nairobi"),  # Optional: already covered in start_date
    catchup=False                     # Do not run past missed DAG runs
) as dag:

    # Task: Extract raw data    
    extract_task = PythonOperator(
        task_id='extract_all_data',      # Task name
        python_callable=run_extract      # Function to run
    )

    # ------------------------------------------
    # 🔁 Task: Transform the extracted data
    # ------------------------------------------
    transform_task = PythonOperator(
        task_id='transform_all_data',
        python_callable=run_transform
    )

    # ------------------------------------------
    # 📤 Task: Load the transformed data into PostgreSQL
    # ------------------------------------------
    load_task = PythonOperator(
        task_id='load_transformed_to_postgres',
        python_callable=run_load
    )

    # ------------------------------------------
    # 🔗 Set task dependencies: extract >> transform >> load
    # ------------------------------------------
    extract_task >> transform_task >> load_task
