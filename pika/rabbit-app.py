import pika
import requests
from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# RabbitMQ connection parameters
connection_params = pika.ConnectionParameters(
    host='rabbitmq.default.svc.cluster.local',
    port=5672,
    credentials=pika.PlainCredentials(username='user', password='M99hwSzjBIhK2WC7')
)
url = "insert server URL here"
url_out = "Insert Java's URL"

# Define the MongoDB service address within the Minikube cluster
mongodb_service_host = "mongodb"

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
        # return jsonify({'message': 'Server Down'}), 404
    try:
        # Create a connection to MongoDB
        client = MongoClient(mongodb_service_host, 27017)

        # Access or create the desired database
        database_name = "mydatabase"
        db = client[database_name]

        # Access or create a collection within the database
        collection_name = "mycollection"
        collection = db[collection_name]

        # Define the data to be stored
        data_to_store = {
            "param": param1
        }

        # Insert data into the collection
        result = collection.insert_one(data_to_store)

        # Print the inserted document's ID
        print(f"Inserted document ID: {result.inserted_id}")

        # Close the MongoDB connection
        client.close()
    except Exception as e:
        print(e)
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
        # return jsonify({'message': 'Server Down'}), 404
    # Establish a new connection and channel for each request
    with pika.BlockingConnection(connection_params) as connection:
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='test_queue')

        # Consume a message
        method_frame, header_frame, body = channel.basic_get(queue='test_queue')
        if method_frame:
            msg = str(body.decode('utf-8'))
            print(f"Received message: msg")

            # Acknowledge the message (confirming it has been processed)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            print("No messages in the queue")
    return True

@app.route('/get_documents', methods=['GET'])
def get_documents():
    # Get the value of the 'param' query parameter from the request
    param_value = str(request.args.get('param'))
    # Create a connection to MongoDB
    client = MongoClient(mongodb_service_host, 27017)

    # Access or create the desired database
    database_name = "mydatabase"
    db = client[database_name]

    # Access or create a collection within the database
    collection_name = "mycollection"
    collection = db[collection_name]

    # Query MongoDB for documents that match the specified parameter
    query = {"param": param_value}
    cursor = collection.find(query)

    # Convert the cursor to a list of dictionaries
    documents = list(cursor)

    # Close the MongoDB connection
    client.close()
    print(documents)

    # Return a JSON response using Flask's jsonify
    return jsonify({"documents": documents})

@app.route('/test', methods=['PUT'])
def put_test():
    # Enqueue a task for test_put
    # enqueue_task.delay('test_put')
    return jsonify({"message": "Task 'test_put' enqueued successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')