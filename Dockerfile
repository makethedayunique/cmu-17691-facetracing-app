FROM python:3.8

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=facetracing.settings \
	PORT=8000

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --clear

RUN export DJANGO_SETTINGS_MODULE=facetracing.settings

#CMD [ "python3", "manage.py" , "runserver", "0.0.0.0:8000"]
CMD gunicorn facetracing.wsgi:application