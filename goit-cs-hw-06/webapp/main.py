from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import logging
import socket  # Import the socket module
import json  # Import the json module

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Set the base directory and static files directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

class ChatAppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Log the requested path
        logging.info(f"Requested path: {self.path}")

        # Default path is the index.html
        if self.path == "/":
            self.path = "index.html"
        else:
            # Remove the leading slash to normalize the path
            self.path = self.path.lstrip("/")

        # Construct the full path to the file
        file_path = os.path.join(STATIC_DIR, self.path)
        logging.debug(f"Resolved file path: {file_path}")

        # Check if the file exists
        if os.path.isfile(file_path):
            logging.info(f"Serving file: {file_path}")
            try:
                with open(file_path, "rb") as f:
                    self.send_response(200)
                    if self.path.endswith(".html"):
                        self.send_header("Content-type", "text/html")
                    elif self.path.endswith(".css"):
                        self.send_header("Content-type", "text/css")
                    elif self.path.endswith(".png"):
                        self.send_header("Content-type", "image/png")
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                # Handle unexpected errors
                logging.error(f"Error serving file {file_path}: {e}")
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Internal Server Error: {e}".encode("utf-8"))
        else:
            # Log file not found
            logging.warning(f"File not found: {file_path}")
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            error_file_path = os.path.join(STATIC_DIR, "error.html")
            logging.debug(f"Serving 404 error page: {error_file_path}")
            if os.path.isfile(error_file_path):
                with open(error_file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>404 Not Found</h1>")


    def do_POST(self):
        if self.path == "/message":
            logging.info("Received POST request to /message")
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")

            # Parse the form data
            data = {key: value for key, value in [item.split("=") for item in post_data.split("&")]}
            logging.info(f"Received form data: {data}")

            # Send data to Socket server
            try:
                logging.info("Attempting to connect to the Socket server...")
                with socket.create_connection(("socket", 5000)) as sock:
                    logging.info("Connected to the Socket server")
                    sock.sendall(json.dumps(data).encode("utf-8"))
                    logging.info("Data sent to the Socket server")
                    response = sock.recv(1024).decode("utf-8")
                    logging.info(f"Response from Socket server: {response}")
            except Exception as e:
                logging.error(f"Error connecting to Socket server: {e}")

            # Respond to the client
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Message sent to Socket server")


# Start the server
def run(server_class=HTTPServer, handler_class=ChatAppHandler):
    server_address = ("", 3000)  # Server listens on port 3000
    logging.info("Starting HTTP server on port 3000...")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()