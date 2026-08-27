import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8000))
server_socket.listen(1)
print("Server listening on http://localhost:8000")

while True:
    connection, address = server_socket.accept()
    print("Connected by", address)

    request_data = connection.recv(1024).decode()

    # Parse just the first line, e.g. "GET / HTTP/1.1"
    request_line = request_data.split("\r\n")[0]
    method, path, version = request_line.split(" ")

    print(f"Method: {method}, Path: {path}, Version: {version}")

    response_body = f"""
    <html>
    <head>
        <title>My Python Server</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1e1e2f, #3a3a5c);
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }}
            h1 {{
                font-size: 3em;
                margin-bottom: 0.2em;
            }}
            p {{
                font-size: 1.2em;
                color: #ccc;
            }}
            .box {{
                background: rgba(255,255,255,0.1);
                padding: 30px 50px;
                border-radius: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🚀 Hello, {address[0]}!</h1>
            <p>You requested: <strong>{method} {path}</strong></p>
            <p>Built from scratch using raw Python sockets.</p>
        </div>
    </body>
    </html>
    """

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(response_body)}\r\n"
    response += "\r\n"
    response += response_body

    connection.sendall(response.encode())
    connection.close()


