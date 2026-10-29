FROM jupyter/pyspark-notebook:spark-3.5.0

LABEL maintainer="Namith Kumar C (PES1UG24AM171), Jayanth K (PES1UG24AM123)"
LABEL description="Big Data Systems & Responsible AI Engineering - Spatial Fairness Pipeline"

USER root

# Install system dependencies for spatial processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# Install python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/jovyan/work

CMD ["start-notebook.sh", "--NotebookApp.token=''"]
