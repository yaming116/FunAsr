FROM yaming116/fun-asr:latest

EXPOSE 5001

WORKDIR /funAsr
#RUN pip install flask requests funasr modelscope
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["tail", "-f", "/dev/null"]