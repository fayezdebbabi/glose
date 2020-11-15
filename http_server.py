import socket
from pathlib import Path

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
    if (method == "GET"):
        requested_file = Path("." + path)
        if requested_file.exists():
            if requested_file.is_file():
                response_body_content = requested_file.read_text()
                generated_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body_content)}\r\nContent-Type: text/html\r\n\r\n{response_body_content}\r\n"
                return generated_response
            if requested_file.is_dir():
                directory_result_list = ""
                for entry in requested_file.iterdir():
                    if entry.is_dir():
                        tmp_file_reference = str(entry).split("/")[-1]
                        if path == "/":
                            directory_result_list = directory_result_list + \
                                f"""<a href="{path + str(entry)}">{str(entry)}</a><br>"""
                        else:
                            directory_result_list = directory_result_list + \
                                f"""<a href="{path + "/" + tmp_file_reference}">{str(tmp_file_reference)}</a><br>"""
                for entry in requested_file.iterdir():
                    if entry.is_file():
                        tmp_file_reference = str(entry).split("/")[-1]
                        if path == "/":
                            directory_result_list = directory_result_list + \
                                f"""<a href="{path + str(entry)}">{str(entry)}</a><br>"""
                        else:
                            directory_result_list = directory_result_list + \
                                f"""<a href="{path + "/" + tmp_file_reference}">{str(tmp_file_reference)}</a><br>"""
                response_body_content = directory_result_list
                generated_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body_content)}\r\nContent-Type: text/html\r\n\r\n{response_body_content}\r\n"
                return generated_response
        else:
            response_body_content = "Resource not found"
            generated_response = f"HTTP/1.1 404 Bad Request\r\nContent-Length: {len(response_body_content)}\r\nContent-Type: text/html\r\n\r\n{response_body_content}\r\n"
            return generated_response
    else:
        response_body_content = "Method not supported"
        generated_response = f"HTTP/1.1 400 Bad Request\r\nContent-Length: {len(response_body_content)}\r\nContent-Type: text/html\r\n\r\n{response_body_content}\r\n"
        return generated_response


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
