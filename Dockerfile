FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y libzbar0

COPY . .

CMD ["python3", "__cli__.py"]
