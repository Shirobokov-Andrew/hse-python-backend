FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip

WORKDIR /src

COPY . ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
