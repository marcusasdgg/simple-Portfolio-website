import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import emailApp.sendEmail as sE
import badApple.badapple as bA
import ssl
import socket



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/shutdown':
            # If the path is '/shutdown', shut down the server
            print("Server is shutting down...")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Shutting down server...')
            # Trigger the server shutdown
            server.shutdown()
        elif '.ico' in self.path:
            try:
        # Open the requested file
                path = os.path.join(os.getcwd(), self.path[1:])
                with open(path, 'rb') as file:
                    content = file.read()
        # Send the response
                self.send_response(200)
                self.send_header('Content-type', 'image/x-icon')
                # Set caching headers to cache for 1 day (86400 seconds)
                self.send_header('Cache-Control', 'max-age=86400')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
        # If the file is not found, send a 204 No Content response
                self.send_response(204)
                self.end_headers()
        elif ".html" in self.path:
            # Serve HTML files
            try:
                print(self.path)
                # Open the requested file
                path = os.path.join(os.getcwd(), self.path[1:])
                print("path is (" + path + ")")
                with open(path, 'rb') as file:
                    content = file.read()
                # Send the response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
            # If the file is not found, send a 204 No Content response
                self.send_response(204)
                self.end_headers()
        elif ".css" in self.path:
            # Serve HTML files
            try:
                # Open the requested file
                
                path = os.path.join(os.getcwd(), self.path[1:])
                print("finding path = " + path)
                with open(path, 'rb') as file:
                    content = file.read()
                # Send the response
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                # If the file is not found, send a 404 error
                    self.send_response(302)
                    self.send_header('Location', '/secret.html')
                    self.end_headers()
        elif ".mp3" in self.path:
            try:
                # Open the MP3 file
                path = os.path.join(os.getcwd(), self.path[1:])
                with open(path, 'rb') as file:
                    content = file.read()

                # Send the response
                self.send_response(200)
                self.send_header('Content-type', 'audio/mpeg')  # Set the content type
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                # If the file is not found, send a 404 error
                self.send_response(204) 
        elif ".png" in self.path:
            try:
                with open(self.path[1:], 'rb') as file:
                    content = file.read()
                # Send the response with content type 'image/png'
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(204)
    def do_POST(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])
        print("type = "+content_type)
        # Check if the request contains a file upload
        if 'multipart/form-data' in content_type:
            # Extract the boundary string from the Content-Type header
            boundary = content_type.split("=")[1].encode()

            # Read the raw request body
            raw_data = self.rfile.read(content_length)

            # Split the request body into individual parts using the boundary
            parts = raw_data.split(boundary)

            # Iterate over the parts to find the file data
            for part in parts:
                if b'filename="' in part:
                    print("file chunk found")
                    # Extract the filename from the Content-Disposition header
                    filename = part.split(b'filename="')[1].split(b'"')[0]
                    # Extract the file data
                    file_data = part.split(b'\r\n\r\n')[1].strip(b'\r\n')
                    # Save the file data to a file
                    with open(filename, 'wb') as f:
                        f.write(file_data)

            # Send a response back to the client
                self.send_response(302)
                self.send_header('Location', '/about.html')
                self.end_headers()
        else:
            # Handle other types of POST requests
            pass

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('192.168.0.200', 443)
    httpd = server_class(server_address, handler_class)
    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Load the key and certificate files
    ssl_context.load_cert_chain(keyfile="server.key", certfile="server.crt")
    # Wrap the socket with SSL
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    print(f'Server running at https://192.168.0.200:{port}/')
    httpd.serve_forever()

if __name__ == '__main__':
    image = False
    icon = False
    if not (os.path.exists("badApple/imageStorage")):
        os.mkdir("badApple/imageStorage")
        print("Created badApple/imageStorage")
    else:
        image = True
    if not (os.path.exists("badApple/icoStorage")):
        os.mkdir("badApple/icoStorage")
        print("created badApple/icoStorag")
    else:
        icon = True

    if (image == False or icon == False):
        bA.split_video("badApple/ba.mp4","badApple/imageStorage","badApple/icoStorage")
    run()