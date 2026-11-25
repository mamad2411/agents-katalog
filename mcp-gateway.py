#!/usr/bin/env python3
"""mcp-gateway — 1 tool MCP untuk skill + repo. Skema minimal (~150 token), bukan 263k tool.

Kenapa 1 tool: setiap tool MCP yang hidup menambah schema ke SETIAP request.
Satu tool = biaya tetap paling kecil. Jalur paling murah tetap shell (`sk`), 0 token.

Daftar tool: skill_gateway(action=…)
  search   cari skill            (query, limit)
  load     cetak SKILL.md        (query = nama skill)
  repo     cari repo             (query, limit)
  repo_get shallow clone repo    (query = owner/name)
  scan     scan keamanan         (path)
  agents   daftar agent opencode (query opsional)
  hits     repo populer/tren     (limit)
  stats    ringkasan indeks

Jalankan: python3 ~/.agents/mcp-gateway.py   (stdio JSON-RPC, tanpa dependency)
"""
import json
import os
import re
import sqlite3
import subprocess
import sys

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
SKILL_DB = os.path.join(AG, "skills-index.db")
REPO_DB = os.path.join(AG, "repos.db")
AGENT_DIR = os.path.join(HOME, ".config", "opencode", "agents")

TOOL = {
    "name": "skill_gateway",
    "description": "Skills & repos lokal (grep/load/scan) tanpa MCP berat.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {"type": "string",
                       "enum": ["search", "load", "repo", "repo_get", "scan",
                                "agents", "hits", "stats"]},
            "query": {"type": "string", "description": "kata kunci / nama skill / owner/name"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 50},
            "path": {"type": "string", "description": "khusus scan"},
        },
        "required": ["action"],
    },
}

MAX_CHARS = 20000


def _skill_search(q, limit):
    if not q:
        return "query kosong"
    toks = [t for t in re.findall(r"[\w./+-]+", q.lower()) if len(t) > 1][:8]
    c = sqlite3.connect(SKILL_DB, timeout=10)
    rows = []
    try:
        rows = c.execute(
            "SELECT name, COALESCE(category,''), COALESCE(description,''), path FROM skills "
            "WHERE skills MATCH ? AND tier <> 'junk' ORDER BY bm25(skills, 8.0, 1.0, 0, 0, 0, 0) "
            "LIMIT ?", (" OR ".join(toks), limit)).fetchall()
    except Exception:
        rows = []
    if not rows:
        like = f"%{q}%"
        rows = c.execute("SELECT name, COALESCE(category,''), COALESCE(description,''), path "
                         "FROM skills WHERE name LIKE ? OR description LIKE ? LIMIT ?",
                         (like, like, limit)).fetchall()
    if not rows:
        return f"tidak ada skill cocok: {q}"
    return "\n".join(f"- {n} [{c or '-'}] {(d or '').strip()[:70]} — "
                     f"{p.replace(HOME, '~')}" for n, c, d, p in rows)


def _skill_load(name):
    if not name:
        return "query kosong"
    c = sqlite3.connect(SKILL_DB, timeout=10)
    r = c.execute("SELECT path FROM skills WHERE name=? LIMIT 1", (name,)).fetchone()
    if not r:
        r = c.execute("SELECT path FROM skills WHERE name LIKE ? LIMIT 1",
                      (f"%{name}%",)).fetchone()
    if not r:
        return f"tidak ada skill '{name}'"
    try:
        with open(r[0], encoding="utf-8", errors="ignore") as f:
            return f.read()[:MAX_CHARS]
    except Exception as e:
        return f"gagal baca {r[0]}: {e}"


def _repo_search(q, limit):
    if not q:
        return "query kosong"
    c = sqlite3.connect(REPO_DB, timeout=10)
    try:
        rows = c.execute(
            "SELECT r.slug, r.stars, r.state, r.has_skill, substr(COALESCE(r.desc,''),1,70) "
            "FROM repos r WHERE r.slug IN (SELECT slug FROM repos_fts WHERE repos_fts MATCH ?) "
            "ORDER BY r.stars DESC LIMIT ?", (q, limit)).fetchall()
    except Exception:
        like = f"%{q}%"
        rows = c.execute("SELECT slug, stars, state, has_skill, substr(COALESCE(desc,''),1,70) "
                         "FROM repos WHERE slug LIKE ? OR desc LIKE ? ORDER BY stars DESC LIMIT ?",
                         (like, like, limit)).fetchall()
    total = c.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
    if not rows:
        return f"tidak ada repo cocok ({total} terindeks)"
    out = [f"- {s} ⭐{st} [{state}{'+skill' if hs else ''}] {d}"
           for s, st, state, hs, d in rows]
    out.append(f"({total} repo; kode asli: repo_get)")
    return "\n".join(out)


def _repo_get(slug):
    if not slug or "/" not in slug:
        return "butuh owner/name"
    p = subprocess.run([sys.executable, os.path.join(AG, "repo-hub.py"), "get", slug],
                       capture_output=True, text=True, timeout=300)
    return (p.stdout or p.stderr or "").strip()[:2000]


def _scan(path):
    p = subprocess.run([sys.executable, os.path.join(AG, "repo-hub.py"), "scan", path or
                        os.path.join(AG, "skills-store"), "-n", "15"],
                       capture_output=True, text=True, timeout=900)
    return (p.stdout or p.stderr or "").strip()[-4000:]


def _agents(q):
    try:
        names = sorted(f[:-3] for f in os.listdir(AGENT_DIR) if f.endswith(".md"))
    except Exception:
        return "tidak ada folder agent"
    if q:
        names = [n for n in names if q.lower() in n.lower()]
    return "\n".join("- " + n for n in names) or "tidak ada yang cocok"


def _hits(limit):
    p = subprocess.run([sys.executable, os.path.join(AG, "repo-hub.py"), "hits", "-n", str(limit)],
                       capture_output=True, text=True, timeout=120)
    return (p.stdout or p.stderr or "").strip()[:3000]


def _stats():
    s = sqlite3.connect(SKILL_DB, timeout=10).execute("SELECT COUNT(*) FROM skills").fetchone()[0]
    r = sqlite3.connect(REPO_DB, timeout=10).execute("SELECT COUNT(*) FROM repos").fetchone()[0]
    return f"skill terindeks: {s}\nrepo terindeks: {r}\nagent opencode: {_agents('')}"


HANDLERS = {
    "search": lambda a: _skill_search(a.get("query"), int(a.get("limit") or 8)),
    "load": lambda a: _skill_load(a.get("query")),
    "repo": lambda a: _repo_search(a.get("query"), int(a.get("limit") or 8)),
    "repo_get": lambda a: _repo_get(a.get("query")),
    "scan": lambda a: _scan(a.get("path")),
    "agents": lambda a: _agents(a.get("query")),
    "hits": lambda a: _hits(int(a.get("limit") or 10)),
    "stats": lambda a: _stats(),
}

RESOURCES = [
    ("repo-catalog", "Katalog repo lokal (~/.agents/repo-catalog.md)", os.path.join(AG, "repo-catalog.md")),
    ("repo-hits", "Repo populer + tren (~/.agents/repo-hits.md)", os.path.join(AG, "repo-hits.md")),
    ("security-scan", "Hasil scan keamanan terakhir", os.path.join(AG, "security-scan-report.md")),
    ("rules", "Aturan global semua AI (~/.agents/RULES.md)", os.path.join(AG, "RULES.md")),
    ("design-playbook", "Panduan desain", os.path.join(AG, "DESIGN-PLAYBOOK.md")),
]


def reply(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def handle(msg):
    mid = msg.get("id")
    m = msg.get("method", "")
    if m == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion") or ""
        reply({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": want if isinstance(want, str) and want else "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}, "resources": {"listChanged": False}},
            "serverInfo": {"name": "skill-gateway", "version": "1.0.0"}}})
    elif m.startswith("notifications/"):
        return
    elif m == "ping":
        reply({"jsonrpc": "2.0", "id": mid, "result": {}})
    elif m == "tools/list":
        reply({"jsonrpc": "2.0", "id": mid, "result": {"tools": [TOOL]}})
    elif m == "resources/list":
        reply({"jsonrpc": "2.0", "id": mid, "result": {"resources": [
            {"uri": f"skill://{k}", "name": k, "description": d, "mimeType": "text/markdown"}
            for k, d, _ in RESOURCES]}})
    elif m == "resources/read":
        uri = (msg.get("params") or {}).get("uri", "")
        key = uri.rsplit("/", 1)[-1]
        for k, _, path in RESOURCES:
            if k == key and os.path.exists(path):
                with open(path, encoding="utf-8", errors="ignore") as f:
                    reply({"jsonrpc": "2.0", "id": mid,
                           "result": {"contents": [{"uri": uri, "mimeType": "text/markdown",
                                                    "text": f.read()[:MAX_CHARS]}]}})
                return
        reply({"jsonrpc": "2.0", "id": mid,
               "error": {"code": -32602, "message": f"resource tidak ada: {uri}"}})
    elif m == "tools/call":
        p = msg.get("params") or {}
        if p.get("name") != TOOL["name"]:
            reply({"jsonrpc": "2.0", "id": mid,
                   "error": {"code": -32602, "message": "tool tidak dikenal"}})
            return
        a = p.get("arguments") or {}
        fn = HANDLERS.get(a.get("action", ""))
        try:
            text = fn(a) if fn else "action tidak valid"
            reply({"jsonrpc": "2.0", "id": mid,
                   "result": {"content": [{"type": "text", "text": text}], "isError": False}})
        except Exception as e:
            reply({"jsonrpc": "2.0", "id": mid,
                   "result": {"content": [{"type": "text", "text": f"ERROR: {e}"}], "isError": True}})
    elif mid is not None:
        reply({"jsonrpc": "2.0", "id": mid,
               "error": {"code": -32601, "message": f"method tidak didukung: {m}"}})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        for x in (msg if isinstance(msg, list) else [msg]):
            handle(x)


if __name__ == "__main__":
    main()
