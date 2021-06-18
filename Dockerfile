FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["python3", "__cli__.py"]
