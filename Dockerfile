FROM python:3.7

ENV APP_HOME /arknights-farmer

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP_HOME
WORKDIR $APP_HOME

RUN apt update && apt install -y android-tools-adb
CMD ["bash", "-c", "adb start-server ; python server.py"]
