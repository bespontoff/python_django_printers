FROM python:3.10
LABEL authors="m.denisov@agrohold.ru"

RUN apt-get update && apt-get install -y python3-dev libldap2-dev libsasl2-dev libssl-dev

RUN apt-get install -y libsnmp-dev

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED=1

COPY ./monitoring_printers .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]