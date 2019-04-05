FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN pip3 install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5002
CMD python3 __init__.py
