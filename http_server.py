import socket
from urllib.parse import urlparse

HOST = '127.0.0.1'
PORT = 8080


def parse_http_request(data):
    request, *headers_tmp, blank_line, body = data.split('\r\n')
    method, path, protocol = request.split(' ')
    headers = {}
    for header in headers_tmp:
        header_name, header_value = header.split(':', 1)
        headers[header_name] = header_value
    return method, path, protocol, headers, body


def generate_http_response(method, path, protocol, headers, body):
    response = "temporary response"
    parsed_path = urlparse(path)
    tmp_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\nContent-Type: text/html\r\n\r\n{response}\r\n"
    return tmp_response


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    while True:
        conn, addr = server_socket.accept()
        with conn:
            data = conn.recv(1024).decode('utf-8')
            method, path, protocol, headers, body = parse_http_request(data)
            http_response = generate_http_response(
                method, path, protocol, headers, body)
            conn.sendall(http_response.encode('utf-8'))
