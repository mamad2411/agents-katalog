#!/usr/bin/env python3
"""opencode-tools-mcp.py — MCP server (stdio, stdlib only) untuk audit token opencode.

Tools:
  tok_stats(days, mode)   -> ringkasan / kapasitas model / json
  lim_check(mode, days)   -> status 429 / analisis RPM
  skill_find(query, k)    -> cari skill lokal (~/.agents)

Daftarkan di ~/.config/opencode/opencode.json:
  "mcp": { "opencode-tools": { "type": "local",
           "command": ["python3", "/Users/<user>/.agents/opencode-tools-mcp.py"],
           "enabled": true } }
"""
import json
import os
import subprocess
import sys
from pathlib import Path

AG = Path.home() / ".agents"
TOKEN = AG / "opencode-token-research.py"
LIMIT = AG / "opencode-limit-guard.py"
SKILL = AG / "skill-search.sh"


def _run(cmd, timeout=25, max_lines=0):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return "SKIP: perintah tidak ada: %s" % cmd[0]
    except subprocess.TimeoutExpired:
        return "ERROR: timeout %ss" % timeout
    if p.returncode != 0:
        return "ERROR: %s" % (p.stderr or p.stdout or "exit %s" % p.returncode)[:300].strip()
    out = (p.stdout or "").strip()
    if max_lines and len(out.splitlines()) > max_lines:
        lines = out.splitlines()
        out = "\n".join(lines[:max_lines]) + "\n… (%d baris dipotong)" % (len(lines) - max_lines)
    return out or "(kosong)"


def tool_tok_stats(args):
    days = str(args.get("days") or 7)
    mode = args.get("mode") or "summary"
    if not TOKEN.exists():
        return "SKIP: %s tidak ada" % TOKEN
    if mode == "limits":
        return _run(["python3", str(TOKEN), "--limits", "--days", days], max_lines=60)
    if mode == "json":
        return _run(["python3", str(TOKEN), "--days", days, "--json"], max_lines=80)
    return _run(["python3", str(TOKEN), "--days", days], max_lines=60)


def tool_lim_check(args):
    days = str(args.get("days") or 7)
    if not LIMIT.exists():
        return "SKIP: %s tidak ada" % LIMIT
    base = ["python3", str(LIMIT), "--days", days]
    if args.get("mode") == "rpm":
        base.insert(2, "--rpm")
    return _run(base, max_lines=40)


def tool_skill_find(args):
    q = (args.get("query") or "").strip()
    if not q:
        return "ERROR: query kosong"
    if not SKILL.exists():
        return "SKIP: %s tidak ada" % SKILL
    k = int(args.get("k") or 5)
    out = _run(["bash", str(SKILL), q])
    lines = [l for l in out.splitlines() if l.strip()]
    return "\n".join(lines[:k]) if lines else "Tidak ada skill cocok: %s" % q


TOOLS = [
    ("tok_stats",
     "Statistik token opencode dari DB lokal. mode=summary (ringkasan+tren+model), "
     "mode=limits (kapasitas context model vs pemakaian nyata), mode=json (data mentah).",
     {"type": "object", "properties": {
         "days": {"type": "number", "description": "rentang hari, default 7"},
         "mode": {"type": "string", "enum": ["summary", "limits", "json"], "description": "jenis laporan"}},
      "required": []}),
    ("lim_check",
     "Cek rate limit opencode: jumlah 429 dari log, model/provider kena, dan apakah penyebabnya RPM atau kuota.",
     {"type": "object", "properties": {
         "mode": {"type": "string", "enum": ["status", "rpm"], "description": "status=ringkasan 429; rpm=analisis request/menit"},
         "days": {"type": "number", "description": "rentang hari, default 7"}},
      "required": []}),
    ("skill_find",
     "Cari skill/workflow terpasang di katalog lokal (~/.agents, 3000+ skill) sebelum menulis workflow baru.",
     {"type": "object", "properties": {
         "query": {"type": "string", "description": "kata kunci, mis. 'pdf extract'"},
         "k": {"type": "number", "description": "jumlah hasil, default 5"}},
      "required": ["query"]}),
]

HANDLERS = {"tok_stats": tool_tok_stats, "lim_check": tool_lim_check, "skill_find": tool_skill_find}


def reply(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def handle(msg):
    mid = msg.get("id")
    method = msg.get("method", "")
    if method == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion") or ""
        reply({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": want if isinstance(want, str) and want else "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "opencode-tools", "version": "1.0.0"}}})
    elif method in ("notifications/initialized", "notifications/cancelled"):
        return
    elif method == "ping":
        reply({"jsonrpc": "2.0", "id": mid, "result": {}})
    elif method == "tools/list":
        reply({"jsonrpc": "2.0", "id": mid, "result": {"tools": [
            {"name": n, "description": d, "inputSchema": s} for n, d, s in TOOLS]}})
    elif method == "tools/call":
        p = msg.get("params") or {}
        fn = HANDLERS.get(p.get("name", ""))
        if not fn:
            reply({"jsonrpc": "2.0", "id": mid,
                   "error": {"code": -32602, "message": "tool tidak dikenal: %s" % p.get("name")}})
            return
        try:
            text = fn(p.get("arguments") or {})
            reply({"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": text}], "isError": False}})
        except Exception as e:
            reply({"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": "ERROR: %s" % e}], "isError": True}})
    elif mid is not None:
        reply({"jsonrpc": "2.0", "id": mid,
               "error": {"code": -32601, "message": "method tidak didukung: %s" % method}})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        for m in (msg if isinstance(msg, list) else [msg]):
            handle(m)


if __name__ == "__main__":
    main()
