import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8000))
server_socket.listen(1)
print("Server listening on http://localhost:8000")

PAGE_STYLE = """
<style>
    * { box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        background: #0d0d14;
        color: #d8d8e0;
        margin: 0;
        padding: 50px 20px;
    }
    .container { max-width: 760px; margin: 0 auto; }
    nav { margin-bottom: 45px; }
    nav a {
        color: #7d8590;
        text-decoration: none;
        margin-right: 24px;
        font-size: 0.95em;
        border-bottom: 2px solid transparent;
    }
    nav a:hover { color: #eaeaea; border-bottom: 2px solid #e85d75; }
    h1 {
        font-size: 2.1em;
        margin-bottom: 6px;
        color: #f0f0f0;
    }
    .subtitle { color: #7d8590; margin-bottom: 40px; font-size: 1.05em; }
    p { line-height: 1.7; }
    .terminal {
        background: #060608;
        border: 1px solid #262633;
        border-radius: 10px;
        padding: 0;
        margin: 30px 0;
        overflow: hidden;
    }
    .terminal-bar {
        background: #16161f;
        padding: 10px 14px;
        display: flex;
        gap: 6px;
    }
    .dot { width: 11px; height: 11px; border-radius: 50%; }
    .dot.red { background: #ff5f56; }
    .dot.yellow { background: #ffbd2e; }
    .dot.green { background: #27c93f; }
    .terminal-body {
        padding: 18px 20px;
        font-family: 'Consolas', monospace;
        font-size: 0.9em;
        color: #9cdb8a;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    .terminal-body .prompt { color: #7d8590; }
    .note {
        border-left: 3px solid #e85d75;
        padding-left: 16px;
        margin: 30px 0;
        color: #b8b8c8;
        font-style: italic;
    }
    h2 { color: #eaeaea; font-size: 1.25em; margin-top: 40px; }
    .log-entry { margin-bottom: 18px; }
    .log-entry .status { font-family: monospace; margin-right: 8px; }
    .done { color: #6ecb63; }
    .pending { color: #7d8590; }
    a.inline { color: #e85d75; }
    footer { margin-top: 60px; color: #55555f; font-size: 0.85em; border-top: 1px solid #1c1c26; padding-top: 20px; }
</style>
"""

def layout(title, content):
    return f"""
    <html>
    <head><title>{title}</title>{PAGE_STYLE}</head>
    <body>
        <div class="container">
            <nav><a href="/">home</a><a href="/about">about</a></nav>
            {content}
            <footer>this page is served by the same server you're reading about right now.</footer>
        </div>
    </body>
    </html>
    """

def home_page(ip):
    content = f"""
    <h1>I built a web server from nothing</h1>
    <p class="subtitle">No Flask. No Django. Just Python's socket module and a lot of trial and error.</p>

    <p>Every time you load a website, your browser and a server have a conversation —
    it sends a request, the server figures out what you want, and sends something back.
    Usually a framework handles that conversation for you. I wanted to see what it actually
    looks like underneath, so I wrote both sides by hand.</p>

    <p>Right now, this exact page you're looking at was generated the moment you opened this tab.
    Your browser sent a raw HTTP request over a TCP socket, my code read it byte by byte, and built
    this HTML on the spot.</p>

    <div class="terminal">
        <div class="terminal-bar">
            <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
        </div>
        <div class="terminal-body"><span class="prompt">$</span> python server.py
Server listening on http://localhost:8000
Connected by ('{ip}', ...)
Method: GET, Path: /, Version: HTTP/1.1</div>
    </div>

    <p class="note">That's your actual IP as seen by this server — <strong>{ip}</strong>.
    Not a placeholder, not hardcoded. It's pulled straight from the live connection.</p>

    <p>If you're curious how far this has come and what's still missing,
    check the <a class="inline" href="/about">build log</a>.</p>
    """
    return layout("home", content)

def about_page():
    content = """
    <h1>What's actually going on here</h1>
    <p class="subtitle">A running log of what's built, in the order it got built.</p>

    <p>This started as a way to actually understand HTTP instead of just importing something
    that handles it for me. Turns out sockets are simpler than I expected, and HTTP is just
    plain text with strict formatting rules.</p>

    <h2>Working so far</h2>
    <div class="log-entry"><span class="status done">[done]</span> opened a raw TCP socket and bound it to a port</div>
    <div class="log-entry"><span class="status done">[done]</span> accepted real connections from an actual browser</div>
    <div class="log-entry"><span class="status done">[done]</span> parsed the request line to pull out method, path, version</div>
    <div class="log-entry"><span class="status done">[done]</span> wrote valid HTTP responses by hand — status line, headers, body</div>
    <div class="log-entry"><span class="status done">[done]</span> basic routing, so different paths show different pages</div>
    <div class="log-entry"><span class="status done">[done]</span> a proper 404 for anything unmatched</div>

    <h2>Not built yet</h2>
    <div class="log-entry"><span class="status pending">[ ]</span> handling more than one visitor at a time — right now it's one at a time, in order</div>
    <div class="log-entry"><span class="status pending">[ ]</span> reading data sent from forms (POST requests)</div>
    <div class="log-entry"><span class="status pending">[ ]</span> serving actual files instead of generating HTML in Python strings</div>

    <p class="note">Everything here is one file. No dependencies outside the Python standard library.
    That's intentional — the point was understanding the protocol, not building something production-ready.</p>
    """
    return layout("about", content)

def not_found_page(path):
    content = f"""
    <h1>Nothing here</h1>
    <p class="subtitle">You asked for <code>{path}</code> and this server has no idea what that is.</p>
    <p>There's no file system being checked, no database lookup — just a simple check
    against a couple of known paths, and this one didn't match any of them.</p>
    """
    return layout("404", content)

while True:
    connection, address = server_socket.accept()
    print("Connected by", address)

    request_data = connection.recv(1024).decode()

    if not request_data:
        connection.close()
        continue

    request_line = request_data.split("\r\n")[0]
    parts = request_line.split(" ")

    if len(parts) != 3:
        connection.close()
        continue

    method, path, version = parts
    print(f"Method: {method}, Path: {path}, Version: {version}")

    if path == "/":
        status_line = "HTTP/1.1 200 OK"
        body = home_page(address[0])
    elif path == "/about":
        status_line = "HTTP/1.1 200 OK"
        body = about_page()
    else:
        status_line = "HTTP/1.1 404 Not Found"
        body = not_found_page(path)

    response = status_line + "\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"
    response += body

    connection.sendall(response.encode("utf-8"))
    connection.close()