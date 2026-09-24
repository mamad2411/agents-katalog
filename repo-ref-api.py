#!/usr/bin/env python3
"""
Repo Reference API (standalone server, port 27126)
==================================================
Melayani index repo-refs (STUB.md + meta.json + TREE.txt) untuk LLM.
Endpoint: /health /stats /repos /repos/search?q= /repos/readme?name=
          /repos/meta?name= /repos/tree?name=
Response cap 2000 chars.
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

REFS_DIR = os.path.expanduser("~/.agents/repo-refs")
INDEX_FILE = os.path.join(REFS_DIR, "repo-master-index.json")
PORT = 27126
CAP = 2000


def truncate(s):
    s = s or ""
    return s[:CAP] + "\n... [truncated]" if len(s) > CAP else s


def load_index():
    try:
        with open(INDEX_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"repos": [], "count": 0}


def read_file(*parts):
    try:
        with open(os.path.join(REFS_DIR, *parts), errors="ignore") as f:
            return f.read()
    except OSError:
        return None


def stub(name):
    for fn in ("STUB.md", "README.md", "PATTERNS.md"):
        c = read_file(name, fn)
        if c:
            return c
    return None


def search(q):
    kw = (q or "").lower()
    if not kw:
        return []
    hits = []
    for r in load_index().get("repos", []):
        if kw in r.get("name", "").lower() or kw in r.get("stub_preview", "").lower():
            hits.append(r["name"])
        if len(hits) >= 25:
            break
    return hits


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        p, qs = u.path, parse_qs(u.query)
        idx = load_index()
        if p in ("/health", "/"):
            self._json({"status": "ok", "port": PORT, "repos": idx.get("count", 0)})
        elif p == "/stats":
            self._json({"repos_indexed": idx.get("count", 0),
                        "updated": idx.get("updated"), "refs_dir": REFS_DIR})
        elif p == "/repos":
            names = [r["name"] for r in idx.get("repos", [])]
            self._json({"count": len(names), "repos": names[:200]})
        elif p == "/repos/search":
            q = qs.get("q", [""])[0]
            self._json({"query": q, "results": search(q)})
        elif p == "/repos/readme":
            n = qs.get("name", [""])[0]
            c = stub(n)
            self._json({"name": n, "found": bool(c), "content": truncate(c)})
        elif p == "/repos/meta":
            n = qs.get("name", [""])[0]
            self._json({"name": n, "meta": truncate(read_file(n, "meta.json"))})
        elif p == "/repos/tree":
            n = qs.get("name", [""])[0]
            self._json({"name": n, "tree": truncate(read_file(n, "TREE.txt"))})
        else:
            self._json({"error": "unknown endpoint",
                        "endpoints": ["/health", "/stats", "/repos",
                                      "/repos/search?q=", "/repos/readme?name=",
                                      "/repos/meta?name=", "/repos/tree?name="]}, 404)


def main():
    srv = HTTPServer(("127.0.0.1", PORT), H)
    print(f"Repo Reference API on http://127.0.0.1:{PORT} "
          f"({load_index().get('count', 0)} repos)")
    srv.serve_forever()


if __name__ == "__main__":
    main()