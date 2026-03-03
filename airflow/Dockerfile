FROM apache/airflow:2.9.3-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# deps python (cache stable)
COPY --chown=airflow:0 requirements.airflow.txt /tmp/requirements.airflow.txt

USER airflow
RUN pip install --no-cache-dir -r /tmp/requirements.airflow.txt

# code projet
COPY --chown=airflow:0 . /opt/project
WORKDIR /opt/project

# installe ton package (évite egg-info dans le repo, et évite upgrade deps)
RUN pip install --no-cache-dir --no-deps .