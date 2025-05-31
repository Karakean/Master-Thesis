FROM python:3.13-slim

WORKDIR /app

ADD router.py ./router.py
ADD utils.py ./utils.py
ADD requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "router.py"]
