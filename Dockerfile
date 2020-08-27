FROM python:3.6
WORKDIR /emis-backend

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN wget https://github.com/eyaler/word2vec-slim/raw/master/GoogleNews-vectors-negative300-SLIM.bin.gz
RUN gunzip GoogleNews-vectors-negative300-SLIM.bin.gz
COPY . .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
