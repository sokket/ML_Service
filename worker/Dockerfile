FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN wget -O /app/Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf?download=true

RUN pip install --no-cache-dir pika llama-cpp-python

COPY . /app/

CMD ["python", "app.py"]
