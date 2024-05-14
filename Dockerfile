FROM python:3.11.9-slim-bullseye

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg curl \
        git \
        wget \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash  \
    && apt-get install git-lfs -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5001

WORKDIR /funAsr

RUN mkdir -p /funAsr/hub \
    && cd /funAsr/hub \
    && git lfs install \
    && git clone https://www.modelscope.cn/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch.git \
    && git clone https://www.modelscope.cn/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch.git \
    && git clone https://www.modelscope.cn/iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch.git \
    && git clone https://www.modelscope.cn/iic/speech_campplus_sv_zh-cn_16k-common.git \

#COPY requirements.txt requirements.txt
RUN pip install flask requests funasr modelscope

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY . .

CMD ["python" , "app.py"]