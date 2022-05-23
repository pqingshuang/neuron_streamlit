FROM python:3.9.12-bullseye

WORKDIR /opt/python/streamLit

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8501
COPY . .

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]