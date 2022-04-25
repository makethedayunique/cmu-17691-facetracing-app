FROM python:3.8

WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# COPY requirements-wo-gui.txt requirements-wo-gui.txt
# RUN pip3 install -r requirements-wo-gui.txt

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py" , "runserver"]