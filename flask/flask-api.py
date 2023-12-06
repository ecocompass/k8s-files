import pika
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# RabbitMQ connection parameters
connection_params = pika.ConnectionParameters(
    host='rabbitmq.default.svc.cluster.local',
    port=5672,
    credentials=pika.PlainCredentials(username='user', password='M99hwSzjBIhK2WC7')
)
url = "insert server URL here"
url_out = "Insert Java's URL"
# Simulate a core server API endpoint
@app.route('/input', methods=['GET'])
def get_test():
    param1 = str(request.args.get('param'))
    try:
        response = requests.get(url, timeout=5, verify=False)
        response.raise_for_status()
        # print(response.text)
    except:
        print("Server Down")
        return jsonify({'message': 'Server Down'}), 404

    # Establish a new connection and channel for each request
    with pika.BlockingConnection(connection_params) as connection:
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='test_queue')

        # Publish a message
        channel.basic_publish(exchange='', routing_key='test_queue', body=param1)
        print("Message published")

    response_from_core = {"message": param1}
    return jsonify(response_from_core)

@app.route('/output', methods=['GET'])
def push_test():
    try:
        response = requests.get(url_out, timeout=5, verify=False)
        response.raise_for_status()
        # print(response.text)
    except:
        print("Server Down")
        return jsonify({'message': 'Server Down'}), 404
    # Establish a new connection and channel for each request
    with pika.BlockingConnection(connection_params) as connection:
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='test_queue')

        # Consume a message
        method_frame, header_frame, body = channel.basic_get(queue='test_queue')
        if method_frame:
            msg = str(body.decode('utf-8'))
            print(f"Received message: {msg}")

            # Acknowledge the message (confirming it has been processed)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            print("No messages in the queue")

    return jsonify({"message": msg})

@app.route('/test', methods=['PUT'])
def put_test():
    # Enqueue a task for test_put
    # enqueue_task.delay('test_put')
    return jsonify({"message": "Task 'test_put' enqueued successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')