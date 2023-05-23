import pika
import json
import os
# Initialize connection to RabbitMQ server
credentials = pika.PlainCredentials('admin1', 'admin123')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.1.24', credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='planet_simulation')

# Define a callback function to process the incoming messages


def callback(ch, method, properties, body):
    forces = json.loads(body)
    print(forces)
    with open('testing.json', 'a+') as f:
        f.seek(0)
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
        data.append(forces)
        f.seek(0)
        json.dump(data, f)


# Consume messages from the queue and pass them to the callback function
channel.basic_consume(queue='planet_simulation',
                      on_message_callback=callback, auto_ack=True)

if not os.path.isfile('testing.json'):
    with open('testing.json', 'w') as f:
        json.dump([], f)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
