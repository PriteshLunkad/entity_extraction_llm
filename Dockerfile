FROM python:3.10-slim-buster
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 
EXPOSE 8000
ENTRYPOINT [ "uvicorn", "server:app", "--host","0.0.0.0", "--port","8000" ]
