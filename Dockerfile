FROM python:3.13.3

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./ ./

RUN rm -rf requirements.txt

CMD ["python3", "main.py"]
