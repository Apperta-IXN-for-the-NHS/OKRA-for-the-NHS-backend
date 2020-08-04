FROM python:3.6
WORKDIR /emis-backend

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "emisbackend:app", "-c", "./gunicorn.conf.py"]