import pika
import json
import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
QUEUE_NAME = 'text_generation'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

class ModelService:
    def run(self, prompt_id: int, user_id: int, prompt: str):
        task = {
            prompt_id: prompt_id,
            user_id: user_id,
            prompt: prompt
        }
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(task)
        )
        print(f"[x] Sent {task}")
