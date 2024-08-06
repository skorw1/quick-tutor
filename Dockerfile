FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# Запуск сервера разработки Django
CMD ["python3", "./src/manage.py", "runserver", "0.0.0.0:8000"]
