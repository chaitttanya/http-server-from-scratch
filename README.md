# Raw HTTP Server (Python, from scratch)

A web server built using nothing but Python's built-in `socket` module — no Flask, no Django, no external dependencies. The goal wasn't to build something production-ready, it was to actually understand what a framework normally hides: how a browser and a server talk to each other over raw bytes.

## Why

Most developers use HTTP constantly without seeing what's underneath — sockets, request parsing, headers, response formatting. This project rebuilds that from the ground up, one piece at a time.

## What it does

- Opens a raw TCP socket and listens for connections
- Accepts real browser requests
- Parses the HTTP request line (method, path, version) and headers
- Handles both GET and POST requests
- Parses POST body data from a submitted form
- Routes different paths to different pages (`/`, `/about`, `/contact`)
- Returns a proper 404 for unmatched routes
- Handles multiple visitors at once using threads
- Shuts down cleanly on `Ctrl+C`

## Running it

Requires Python 3 (no other dependencies).

```bash
python server.py
```

Then open `http://localhost:8000` in a browser.

## Routes

| Route      | Method | Description                          |
|------------|--------|---------------------------------------|
| `/`        | GET    | Home page, explains the project       |
| `/about`   | GET    | Build log — what's done, what's not   |
| `/contact` | GET    | A simple contact form                 |
| `/contact` | POST   | Parses and displays submitted form data |

## What's not implemented

This is intentionally minimal — no file serving, no persistent storage, no HTTPS. The point was learning the protocol, not building something production-ready.

## Structure

Everything lives in a single file, `server.py`, so the whole flow — socket setup, parsing, routing, response building — is easy to read top to bottom.