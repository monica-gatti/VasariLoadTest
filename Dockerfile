FROM locust:latest
RUN apk add --no-cache python3-dev
RUN apk add py3-pip

WORKDIR /app

COPY . /app

RUN apk --no-cache add curl

EXPOSE 8089

ENTRYPOINT python3 locust -f locustfile.py --host=http://localhost:5000