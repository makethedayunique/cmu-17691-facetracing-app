FROM python:3.8

WORKDIR /app

COPY requirements-wo-gui.txt requirements-wo-gui.txt
RUN pip3 install -r requirements-wo-gui.txt

COPY . .

CMD [ "python3", "manage.py" , "runserver"]