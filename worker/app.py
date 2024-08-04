import pika
import json
import os
from llama_cpp import Llama

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
QUEUE_NAME = 'text_generation'

MODEL_PATH = '/app/Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf'

llama = Llama(model_path=MODEL_PATH)

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

def callback(ch, method, properties, body):
    message = json.loads(body)
    prompt = message['prompt']

    response = llama.generate(prompt=prompt)
    generated_text = response['choices'][0]['text']

    with open(f"/results/results_{message['prompt_id']}.txt", "w") as result_file:
        result_file.write(result)

    response_message = {
        'id': message['prompt_id'],
        'text': generated_text
    }
    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps(response_message)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

print('[*] Waiting for messages')
channel.start_consuming()
