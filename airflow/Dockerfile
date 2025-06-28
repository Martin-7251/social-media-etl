# Use the official Apache Airflow image version 2.7.2 as the base image
FROM apache/airflow:2.7.2

# Switch to root user to allow system-level installations 
USER root

# Switch back to airflow user (default user in airflow image) for application-level commands
USER airflow

# Upgrade pip and install required Python packages for the project
RUN pip install --no-cache-dir --upgrade pip && \  # Upgrade pip to latest version without caching
    pip install --no-cache-dir \                   # Install the following Python libraries:
        pandas \                   # For data manipulation and analysis
        numpy \                    # For numerical computations
        pymongo \                  # For connecting to and working with MongoDB
        mysql-connector-python \   # For connecting to MySQL databases
        psycopg2-binary            # For connecting to PostgreSQL databases
