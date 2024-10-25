# Simple HTTP Server for Request Logging

This project implements a basic HTTP server for logging client requests. The server listens on the standard HTTP port and reads data from client connections byte-by-byte. It logs the request details, including headers, method, and body, and gracefully handles potential anomalies in incoming data.

## Requirements

The server should:

1. **Listen on the standard HTTP port** and accept at least one client connection.
2. **Log request details**, specifically:
   - Request **method** (supports `GET` and `POST`).
   - Request **headers** and their values.
   - Request **body**.
3. **Handle the following anomalous cases**:
   - Invalid requests containing random bytes, including non-printable characters.
   - Header lines or the initial line exceeding 10MB.
   - Bodies exceeding 10MB.

**Note**: The server only needs to log received data and is not required to send responses.

## Key Requirements

- **Byte-by-byte Parsing**: The server reads incoming data without relying on pre-built parsers, ensuring direct handling of data as it arrives.
- **Stability Against Large Inputs**: The server should not crash when encountering very large headers or bodies. 

## Simulating Input

To test various input cases, there is a simple client scrypt.
## Usage and Testing

1. Clone this repository and run the server.
2. Run the client script to simulate requests.
3. Verify logs to ensure headers, method, and body content are captured as expected.
