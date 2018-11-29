FROM ubuntu
RUN apt-get update && \
    apt-get install -y \
    libgdiplus \
    python-dev \
    python \
    python-pip \
    build-essential \
    cmake \
    pkg-config \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-python-dev \
    python3-dev \
    gcc

COPY requirements.txt /
RUN pip install -r /requirements.txt
