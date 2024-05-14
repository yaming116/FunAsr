FROM yaming116/touch-base:latest


RUN mkdir -p /models && chmod -R 777 /models

EXPOSE 5001

WORKDIR /funAsr
#RUN pip install flask requests funasr modelscope
COPY . .

RUN pip install -r requirements.txt

CMD ["python" , "app.py"]