import socket
import json
from pymongo import MongoClient
from datetime import datetime
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Starting socket server...")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/")
logging.debug(f"MongoDB URI: {MONGO_URI}")
try:
    client = MongoClient(MONGO_URI)
    db = client["chat"]
    collection = db["messages"]
    logging.info("Connected to MongoDB successfully")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise

# Socket server settings
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def start_socket_server():
    logging.info(f"Starting socket server on {SERVER_HOST}:{SERVER_PORT}")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        logging.info("Socket server is now listening for connections...")
    except Exception as e:
        logging.error(f"Error starting socket server: {e}")
        raise

    while True:
        try:
            logging.debug("Waiting for a new connection...")
            client_socket, client_address = server_socket.accept()
            logging.info(f"Connection established with {client_address}")

            data = client_socket.recv(BUFFER_SIZE)
            if data:
                logging.debug(f"Raw data received: {data}")
                try:
                    message_data = json.loads(data.decode("utf-8"))
                    message_data["timestamp"] = datetime.utcnow().isoformat()
                    logging.debug(f"Decoded message: {message_data}")

                    # Save to MongoDB
                    collection.insert_one(message_data)
                    logging.info(f"Message saved to MongoDB: {message_data}")

                    # Send confirmation back to client
                    client_socket.sendall(b"Message received and saved")
                    logging.debug("Confirmation sent to client")
                except json.JSONDecodeError as json_error:
                    logging.error(f"Failed to decode JSON: {json_error}")
                except Exception as db_error:
                    logging.error(f"Failed to save to MongoDB: {db_error}")
            else:
                logging.warning("No data received from client")
        except Exception as e:
            logging.error(f"Error during client communication: {e}")
        finally:
            client_socket.close()
            logging.info("Connection closed")

if __name__ == "__main__":
    logging.info("Executing main.py...")
    start_socket_server()