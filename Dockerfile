FROM python:3.11

WORKDIR /main

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY AI.py ./
COPY song_analize.py ./
COPY new_parameters.py ./
COPY genres.txt ./
COPY neural_network.h5 ./
COPY conn.py ./
COPY results.json ./
COPY results2.json ./
COPY static ./static
COPY templates ./templates

EXPOSE 8000

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
