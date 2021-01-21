FROM python:3.7

ENV APP_HOME /arknights-farmer

COPY . $APP_HOME
WORKDIR $APP_HOME

RUN apt update && apt install -y android-tools-adb
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash", "-c", "adb start-server ; python server.py"]
