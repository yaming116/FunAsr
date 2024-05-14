FROM python:3.11.9-slim-bullseye

EXPOSE 5001

WORKDIR /funAsr
#RUN pip install flask requests funasr modelscope
COPY . .

RUN pip install -r requirements.txt

CMD ["python" , "app.py"]