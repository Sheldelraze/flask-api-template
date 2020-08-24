FROM python:3.6

COPY requirements.txt .
RUN pip3 install --quiet -r requirements.txt

COPY . /

CMD gunicorn -w 5 -b 0.0.0.0:3412 server:app --threads=2 --worker-class=gthread --access-logfile - --max-requests 200 --max-requests-jitter 10 --timeout 180
