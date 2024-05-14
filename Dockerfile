#FROM yaming116/touch-base:latest
FROM registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-cpu-0.4.4

RUN mkdir -p /models && chmod -R 777 /models

EXPOSE 5001

WORKDIR /funAsr
#RUN pip install flask requests funasr modelscope
COPY . .

RUN pip install -r requirements.txt

CMD ["python" , "app.py"]