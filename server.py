#!/usr/bin/env python3
"""QualCode local server.

Run:  python server.py   (or double-click start.bat / start.command)
Every document is saved as a subfolder next to this file:
    <document name>/document.txt, codes.csv, coded_segments.csv, project.json
Uses only the Python standard library.
"""
import json
import os
import re
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("QUALCODE_PORT", "8765"))
SKIP = {"__pycache__"}


def safe_name(name):
    name = re.sub(r'[\\/:*?"<>|]+', "-", str(name or "")).strip().strip(".")
    name = re.sub(r"\s+", " ", name)[:80]
    if not name or name.startswith("."):
        raise ValueError("Invalid document name")
    return name


def doc_dir(name):
    path = os.path.join(ROOT, safe_name(name))
    if os.path.dirname(os.path.abspath(path)) != ROOT:
        raise ValueError("Invalid document name")
    return path


def read(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


def write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)  # atomic: a crash never leaves a half-written file


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass  # keep the console quiet

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_err(self, code, msg):
        body = msg.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        try:
            if url.path == "/api/info":
                return self.send_json({"folder": os.path.basename(ROOT), "path": ROOT})
            if url.path == "/api/projects":
                names = []
                for n in os.listdir(ROOT):
                    p = os.path.join(ROOT, n)
                    if n in SKIP or n.startswith(".") or not os.path.isdir(p):
                        continue
                    if os.path.exists(os.path.join(p, "project.json")) or os.path.exists(os.path.join(p, "document.txt")):
                        names.append(n)
                return self.send_json({"projects": sorted(names, key=str.lower)})
            if url.path == "/api/project":
                d = doc_dir(parse_qs(url.query).get("name", [""])[0])
                if not os.path.isdir(d):
                    return self.send_err(404, "Document not found")
                pj = os.path.join(d, "project.json")
                if os.path.exists(pj):
                    try:
                        return self.send_json({"project": json.loads(read(pj))})
                    except ValueError:
                        pass  # damaged json -> rebuild from txt + csv
                out = {}
                if os.path.exists(os.path.join(d, "document.txt")):
                    out["text"] = read(os.path.join(d, "document.txt"))
                if os.path.exists(os.path.join(d, "coded_segments.csv")):
                    out["segments_csv"] = read(os.path.join(d, "coded_segments.csv"))
                return self.send_json(out)
        except ValueError as e:
            return self.send_err(400, str(e))
        if url.path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/save":
            return self.send_err(404, "Not found")
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
            d = doc_dir(data["name"])
            os.makedirs(d, exist_ok=True)
            project = data["project"]
            write(os.path.join(d, "document.txt"), project.get("text", ""))
            write(os.path.join(d, "project.json"), json.dumps(project, ensure_ascii=False, indent=2))
            write(os.path.join(d, "codes.csv"), data.get("codes_csv", ""))
            write(os.path.join(d, "coded_segments.csv"), data.get("segments_csv", ""))
            return self.send_json({"ok": True})
        except (ValueError, KeyError) as e:
            return self.send_err(400, str(e))
        except OSError as e:
            return self.send_err(500, "Could not write files: " + str(e))


def main():
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"Port {PORT} is busy - QualCode may already be running. Opening it in your browser.")
        webbrowser.open(f"http://127.0.0.1:{PORT}/")
        return
    url = f"http://127.0.0.1:{PORT}/"
    print("QualCode is running at", url)
    print("Saving documents into:", ROOT)
    print("Keep this window open while you work. Press Ctrl+C (or close it) to stop.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
