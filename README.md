# 🧪 Social Media ETL Pipeline

This project is an end-to-end **ETL (Extract, Transform, Load)** pipeline for social media data, built using **Docker, Airflow, MongoDB, MySQL, PostgreSQL, and Python**.

It automates data ingestion from JSON files, transformation using Pandas and NumPy, and loads the cleaned data into structured databases for further analysis and visualization.

---

## 📁 Project Structure

SOCIAL_MEDIA_ETL/
│
├── airflow/
│ └── dags/
│ ├── data/ # Raw and transformed JSON data
│ ├── extract_all_data.py # Extract data from files and load into DBs
│ ├── transform_all_data.py # Transform raw data with pandas/NumPy
│ ├── load_to_postgres.py # Load transformed data into PostgreSQL
│ └── etl_dag.py # Airflow DAG defining ETL pipeline
│
├── Dockerfile # Custom Airflow image with Python packages
├── docker-compose.yml # Define all services (Airflow, DBs, etc.)
├── ETL_Data_Visualizations.py # Standalone script for visualizing ETL data
├── .gitignore
└── README.md

## 🛠️ Technologies Used

- **Airflow** – Workflow orchestration
- **Docker & Docker Compose** – Containerized setup
- **PostgreSQL, MySQL, MongoDB** – Target databases
- **Pandas, NumPy** – Data transformation
- **Matplotlib, Seaborn, Plotly** – Visual analytics
- **VS Code / Python Scripts** – Development and testing

---

## 🔁 ETL Pipeline Overview

1. **Extract**  
   - Load raw `.json` data files from `dags/data/`
   - Insert into MongoDB (users), PostgreSQL (posts), MySQL (comments/likes)

2. **Transform**  
   - Clean, normalize, and derive new fields (e.g., follower/following ratio)
   - Save transformed data as new `.json` files

3. **Load**  
   - Insert transformed data into PostgreSQL

4. **Visualize**  
   - Analyze trends and patterns using `ETL_Data_Visualizations.py`

---

## 🚀 How to Run the Project

### 1. Clone the Repository
``bash
git clone https://github.com/Martin-7251/social_media_etl.git
cd social_media_etl

🐳 How to Run (Local)
Ensure you have Docker + Docker Compose installed.

2. Start Docker Containers
bash
Copy
Edit
docker-compose up --build
3. Access Airflow UI
Navigate to http://localhost:8081 and trigger the Extract_transform_load DAG.

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

4. Run Visualizations (Optional)
bash
Copy
Edit
python ETL_Data_Visualizations.py
📊 Sample Visualizations
Followers vs Following (scatter)

Account privacy distribution (pie chart)

Post likes over time (line chart)

Comments per post (histogram)

Top 10 most liked posts (bar chart)

📌 Future Improvements
Integrate with social media APIs for real-time data

Add unit tests and logging

Build interactive dashboards using Plotly Dash


Runs every Wednesday at 12:00 PM (Africa/Nairobi timezone)

Can also be triggered manually

## 👨‍💻 Author

- **Martin Kamau**  
  Data Analyst | Data Engineer | [LinkedIn](https://www.linkedin.com/in/martinkamau29/)


  




