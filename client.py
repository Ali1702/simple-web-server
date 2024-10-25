import socket

def send_request(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8080))
        s.sendall(data.encode('utf-8'))
        response = s.recv(4096)
        print('Received:', response.decode('utf-8'))

# valid request
send_request("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")

# valid request with body
send_request("POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 5\r\n\r\nHello")

# partial request
send_request("GET / HTTP/1.1\r\nHost: localhost")

# misspelled method
send_request("GOT / HTTP/1.1\r\nHost: localhost\r\n\r\n")

# Sinvalid request
("INVALID REQUEST")

# large header
large_header = "GET / HTTP/1.1\r\n" + "X-Header: " + "A" * (20 * 1024 * 1024) + "\r\n\r\n"
send_request(large_header)

# large body
large_body = "POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 20\r\n\r\n" + "A" * (20 * 1024 * 1024)