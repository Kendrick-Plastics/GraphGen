FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install openpyxl flask-socketio flask numpy pandas seaborn

EXPOSE 5000

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0"]