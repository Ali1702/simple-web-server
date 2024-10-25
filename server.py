import socket
import select
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s - %(levelname)s')

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_RECV_SIZE = 100 * 1024 * 1024  # 100 MB

def parse_request(request):
    lines = request.split('\r\n')
    if len(lines) < 1:
        return None, None, None
    
    for line in lines:
        if len(line) > MAX_SIZE:
            logging.warning("Line too large, closing connection")
            return None, None, None

    request_line = lines[0].split()
    if len(request_line) < 3:
        return None, None, None
    method = request_line[0]
    
    if method not in ['GET', 'POST']:
        logging.warning("Invalid method, closing connection")
        return None, None, None

    headers = {}
    body = ''
    for line in lines[1:]:
        if line == '':
            break  
        key_value = line.split(': ', 1)
        if len(key_value) == 2:
            headers[key_value[0]] = key_value[1]

    body = '\r\n'.join(lines[len(headers) + 2:])

    return method, headers, body

def handle_client(client_socket):
    client_socket.settimeout(20)  
    request_data = b''
    headers_received = False
    try:
        while True:
            chunk = client_socket.recv(MAX_RECV_SIZE)
            if not chunk:
                logging.info("Client disconnected")
                return
            
            request_data += chunk
            
            if not headers_received and len(request_data) > MAX_SIZE:
                logging.warning("Headers too large, closing connection")
                return
            
            if b'\r\n\r\n' in request_data:
                headers_received = True
                header_end_index = request_data.index(b'\r\n\r\n') + 4
                #headers_data = request_data[:header_end_index]
                body_data = request_data[header_end_index:]
                
                if len(body_data) > MAX_SIZE:
                    logging.warning("Body too large, closing connection")
                    return
                
                break
        
        decoded_request = request_data.decode('utf-8', errors='ignore')
        method, headers, body = parse_request(decoded_request)
        
        if method is None:
            logging.warning("Received invalid request")
            response = "400 Bad Request\r\n"
        else:
            logging.info(f"Received method: {method}")
            logging.info("Received headers:")
            for header, value in headers.items():
                logging.info(f"    {header}: {value}")
            logging.info(f"Body: {body}") if body else None
            
            response = f"Echo: {decoded_request}\r\n"

        client_socket.sendall(response.encode('utf-8'))
        #logging.info(f"Sent response: {response.strip()}")

    except socket.timeout:
        logging.warning("Read operation timed out, closing connection")
    except socket.error as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address_port = ("127.0.0.1", 8080)
    listener_socket.bind(address_port)
    listener_socket.listen(5)
    logging.info(f"Listening on {address_port}")

    while True:
        read_ready_sockets, _, _ = select.select([listener_socket], [], [], 0)
        if read_ready_sockets:
            for ready_socket in read_ready_sockets:
                client_socket, client_address = ready_socket.accept()
                logging.info(f"Accepted connection from {client_address}")
                handle_client(client_socket)
