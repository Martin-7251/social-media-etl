📊Social Media ETL Pipeline with Airflow, Docker & PostgreSQL
This project implements a complete ETL (Extract, Transform, Load) pipeline for social media data using Apache Airflow for orchestration and Docker to manage services like MongoDB, PostgreSQL, and MySQL.

🚀 Features
✅ Extracts raw JSON data from local files

🔁 Transforms user, post, comment, and like data using Pandas and NumPy

📥 Loads:

Users into MongoDB

Posts into PostgreSQL

Comments and likes into MySQL

📅 Scheduled with Apache Airflow (LocalExecutor)

🐳 Fully containerized with Docker Compose

🧩 Optional web UIs: pgAdmin, mongo-express

📂 Project Structure
bash
Copy
Edit
├── airflow/
│   ├── dags/
│   │   ├── etl_dag.py
│   │   ├── extract_all_data.py
│   │   ├── transform_all_data.py
│   │   └── load_to_postgres.py
│   └── Dockerfile
├── data/
│   ├── User.json
│   ├── posts.json
│   ├── postComments.json
│   └── postLikes.json
├── postgres/
├── mysql/
├── mongodb/
├── docker-compose.yml
└── README.md

⚙️ Technologies Used
Tool                                                	Purpose
Apache Airflow                                       	Workflow orchestration
Docker	                                              Containerization of services
PostgreSQL	                                          Stores transformed post data
MongoDB	                                              Stores transformed user data
MySQL	                                                Stores comments and likes data
pgAdmin                                             	PostgreSQL web UI
Mongo Express                                       	MongoDB web UI
Pandas/NumPy	                                        Data cleaning and transformation

🧠 ETL Workflow Overview
🔸 1. Extract
Raw JSON files (User.json, posts.json, postComments.json, postLikes.json)

Extracted and inserted into MongoDB, MySQL, PostgreSQL

🔸 2. Transform
Cleaned using Pandas & NumPy

Fixes formatting, data types, and missing values

🔸 3. Load
Transformed data loaded into:

users_cleaned (MongoDB)

posts_cleaned (PostgreSQL)

comments_cleaned, likes_cleaned (MySQL)

🐳 How to Run (Local)
Ensure you have Docker + Docker Compose installed.

Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/social-media-etl.git
cd social-media-etl
Start all containers

bash
Copy
Edit
docker-compose up --build
Access Airflow

🌐 http://localhost:8081

Username: admin, Password: admin

Trigger the DAG

Open Airflow UI

Turn on and trigger the DAG: Extract_transform_load

🛠 Optional Admin Interfaces
pgAdmin: http://localhost:5050

Email: admin@admin.com, Password: admin

mongo-express: http://localhost:8083

Username: admin, Password: pass

admirer: http://localhost:8082

Username: airflow, Password: airflow

📅 DAG Schedule
DAG ID: Extract_transform_load

Runs every Wednesday at 12:00 PM (Africa/Nairobi timezone)

Can also be triggered manually


