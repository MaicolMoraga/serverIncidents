FROM alpine:3.10

RUN apk add --no-cache python2-dev
RUN apk add --update py-pip

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

CMD ["python2","app.py"]