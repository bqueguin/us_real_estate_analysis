FROM python:3.11

RUN apt-get clean && apt-get -y update && apt-get install -y curl
RUN apt-get install -y default-jre

VOLUME /logs

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Necessary so that the application avoids asking for the email address
RUN mkdir -p ~/.streamlit/ \
    && echo "[general]"  > ~/.streamlit/credentials.toml \
    && echo "email = \"\""  >> ~/.streamlit/credentials.toml

COPY . /
WORKDIR /app
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--logger.level=info", "2>>", "../logs/snowflake_summit.log"]