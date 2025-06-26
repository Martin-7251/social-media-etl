FROM apache/airflow:2.7.2

USER root

# Install system dependencies if needed (optional)
# RUN apt-get update && apt-get install -y build-essential libpq-dev

# Switch to airflow user before pip install
USER airflow

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        pandas \
        numpy \
        pymongo \
        mysql-connector-python \
        psycopg2-binary
