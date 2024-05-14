FROM python:3.11.9-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg curl \
        git \
        wget \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash  \
    && apt-get install git-lfs -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /models && chmod -R 777 /models


RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

EXPOSE 5001

WORKDIR /funAsr
#RUN pip install flask requests funasr modelscope
COPY . .

RUN pip install -r requirements.txt


CMD ["python" , "app.py"]