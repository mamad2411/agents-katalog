#!/usr/bin/env python3
"""mcp-router.py — MCP meta-server (stdio, stdlib only).

Prinsip: MCP TIDAK nyala mulu. AI liat katalog via tool, pas butuh →
router spawn MCP-nya on-demand, teruskan panggilan, idle auto-mati.

Tools:
  mcp_list(query?)      — daftar/cari MCP di katalog+parkiran (AI jadi tau apa aja)
  mcp_search(query)     — cari MCP by kata kunci (FTS ringan atas mcp-catalog.json)
  mcp_use(name, tool, arguments)
                        — spawn MCP `name` (kalau belum idup), panggil `tool`,
                          kembalikan hasil. Proses dipool, idle >300s auto-mati.
  mcp_status()          — MCP mana yg lagi idup sekarang

Daftarkan ke provider:
  claude mcp add --scope user mcp-router -- python3 ~/.agents/mcp-router.py
"""
import json, os, sys, time, subprocess, threading, re
from pathlib import Path

AG = Path.home() / ".agents"
CATALOG_F = AG / "mcp-catalog.json"
PARKED_F  = AG / "mcp-parked.json"
USAGE_F   = AG / "mcp-usage.json"
IDLE_TTL  = 300   # detik idle sebelum proses MCP dibunuh otomatis
REAP_EVERY = 60   # interval reaper

# --- pool proses MCP idup: {name: {"proc":Popen, "last":ts, "next_id":int}} ---
POOL = {}
POOL_LOCK = threading.Lock()


def _load(path, default):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default


def _save_usage(name):
    try:
        u = _load(USAGE_F, {})
        e = u.get(name, {"count": 0, "first_used": time.time(), "last_used": 0, "days_active": []})
        e["count"] += 1; e["last_used"] = time.time()
        today = time.strftime("%Y-%m-%d")
        days = e.setdefault("days_active", [])
        if today not in days: days.append(today)
        e["days_active"] = days[-90:]
        u[name] = e
        Path(USAGE_F).write_text(json.dumps(u, indent=2))
    except Exception:
        pass


def _find_cfg(name):
    """Ambil run-config MCP: parked.json dulu (config asli), fallback run_hint katalog."""
    parked = _load(PARKED_F, {})
    if name in parked:
        return parked[name], True
    cat = _load(CATALOG_F, [])
    for it in cat:
        if it.get("name") == name:
            hint = it.get("run_hint")
            if not hint:
                return None, False
            parts = hint.split()
            return {"command": parts[0], "args": parts[1:]}, False
    return None, False


def _spawn(name, cfg):
    """Spawn MCP `name` sebagai subprocess stdio. Return proc atau None."""
    cmd = cfg.get("command")
    args = [os.path.expandvars(a) for a in cfg.get("args", [])]
    env = dict(os.environ)
    env.update({k: os.path.expandvars(v) for k, v in cfg.get("env", {}).items()})
    if not cmd:
        return None
    try:
        proc = subprocess.Popen(
            [cmd] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, text=True, bufsize=1,
        )
    except FileNotFoundError:
        return None
    except Exception:
        return None
    # initialize handshake
    try:
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18",
                               "clientInfo": {"name": "mcp-router", "version": "1.0.0"},
                               "capabilities": {}}}
        proc.stdin.write(json.dumps(init_req) + "\n"); proc.stdin.flush()
        resp = proc.stdout.readline()
        if not resp:
            proc.kill(); return None
        r = json.loads(resp)
        # beberapa server balas error di init tapi tetap jalan -> teruskan
        if "error" in r and "result" not in r:
            proc.kill(); return None
        # notifications/initialized
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        proc.stdin.flush()
    except Exception:
        proc.kill(); return None
    return proc


def _rpc(proc, method, params=None, timeout=30):
    """Kirim JSON-RPC ke subprocess MCP, baca 1 baris balasan."""
    with POOL_LOCK:
        nid = 0
        # id unik per proc: cari slot
    # pakai counter global sederhana
    nid = int(time.time() * 1000) % 100000
    req = {"jsonrpc": "2.0", "id": nid, "method": method}
    if params is not None:
        req["params"] = params
    try:
        proc.stdin.write(json.dumps(req) + "\n"); proc.stdin.flush()
        # baca sampai ketemu id matching (skip notifications)
        deadline = time.time() + timeout
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                return None
            try:
                msg = json.loads(line)
            except Exception:
                continue
            if msg.get("id") == nid:
                return msg
            # notification? ignore, keep reading
        return None
    except Exception:
        return None


def _get_proc(name):
    """Ambil proc dari pool, atau spawn bila perlu. Return (proc, spawned_new)."""
    with POOL_LOCK:
        if name in POOL:
            POOL[name]["last"] = time.time()
            return POOL[name]["proc"], False
    cfg, ok = _find_cfg(name)
    if not cfg:
        return None, False
    proc = _spawn(name, cfg)
    if proc is None:
        return None, False
    with POOL_LOCK:
        POOL[name] = {"proc": proc, "last": time.time()}
    return proc, True


def _kill(name):
    with POOL_LOCK:
        entry = POOL.pop(name, None)
    if entry:
        try:
            entry["proc"].kill()
            entry["proc"].wait(timeout=5)
        except Exception:
            pass


def _reaper():
    """Background: bunuh proses MCP idle > IDLE_TTL."""
    while True:
        time.sleep(REAP_EVERY)
        now = time.time()
        victims = []
        with POOL_LOCK:
            for name, e in POOL.items():
                if now - e["last"] > IDLE_TTL:
                    victims.append(name)
        for n in victims:
            _kill(n)


threading.Thread(target=_reaper, daemon=True).start()


# ============================== TOOLS ==============================

def tool_mcp_list(args):
    q = (args.get("query") or "").lower().strip()
    cat = _load(CATALOG_F, [])
    parked = _load(PARKED_F, {})
    # parked (real, siap pakai) tampil di atas
    rows = []
    for name in sorted(parked.keys()):
        rows.append(("PARKED", name, "(official/real config — siap mcp_use)"))
    for it in cat:
        nm = it.get("name", "")
        desc = it.get("description", "")
        lang = it.get("lang") or "?"
        hint = it.get("run_hint") or ""
        if q and q not in nm.lower() and q not in desc.lower() and q not in (lang or ""):
            continue
        rows.append((lang, nm, desc[:90] + (" | hint: " + hint if hint else "")))
        if len(rows) >= 200:
            break
    if not rows:
        return "Tidak ada MCP cocok."
    out = ["**%d MCP** (parked=%d, katalog=%d). Pakai `mcp_use(name, tool, arguments)` untuk nyain." % (
        len(rows), len(parked), len(cat)), "",
        "| tipe | name | info |", "|---|---|---|"]
    for t, n, d in rows[:60]:
        out.append("| %s | `%s` | %s |" % (t, n, d.replace("|", "/")[:90]))
    if len(rows) > 60:
        out.append("\n...dan %d lagi.persempit dengan query." % (len(rows) - 60))
    return "\n".join(out)


def tool_mcp_search(args):
    q = (args.get("query") or "").lower().strip()
    if not q:
        return "Berikan kata kunci, mis. {\"query\":\"postgres\"}"
    cat = _load(CATALOG_F, [])
    scored = []
    for it in cat:
        hay = (it.get("name", "") + " " + it.get("description", "")).lower()
        score = 0
        for tok in q.split():
            if tok in it.get("name", "").lower():
                score += 5
            if tok in hay:
                score += 2
        if score > 0:
            scored.append((score, it))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        return "Tidak ketemu MCP untuk `%s`." % q
    out = ["Hasil `%s` (top %d):" % (q, min(10, len(scored)))]
    for score, it in scored[:10]:
        out.append("- `%s` [%s] %s%s" % (
            it.get("name"), it.get("lang") or "?",
            it.get("description", "")[:80],
            " | " + it.get("run_hint") if it.get("run_hint") else ""))
    out.append("\n> Pakai `mcp_use` untuk nyain. Kalau belum punya config asli, router coba run_hint.")
    return "\n".join(out)


def tool_mcp_use(args):
    name = args.get("name")
    tool = args.get("tool")
    arguments = args.get("arguments") or {}
    if not name or not tool:
        return "Butuh `name` (MCP) dan `tool` (nama tool di MCP itu). arg: {\"name\":\"server-fetch\",\"tool\":\"fetch\",\"arguments\":{...}}"
    proc, spawned = _get_proc(name)
    if proc is None:
        cfg, ok = _find_cfg(name)
        if cfg is None:
            cat = _load(CATALOG_F, [])
            repo = next((i.get("url") for i in cat if i.get("name") == name), "?")
            return "MCP `%s` tidak punya run-config. Repo: %s — pasang dulu config-nya di mcp-parked.json (mcp-lifecycle.py --on)." % (name, repo)
        return "Gagal spawn `%s` (command: %s). Cek: %s terinstall?" % (
            name, cfg.get("command"), cfg.get("command"))
    _save_usage(name)
    # kalau tool = "list_tools", panggil tools/list
    if tool == "list_tools":
        resp = _rpc(proc, "tools/list")
    else:
        resp = _rpc(proc, "tools/call", {"name": tool, "arguments": arguments})
    if resp is None:
        _kill(name)
        return "MCP `%s` tidak merespon (dibunuh). Coba lagi." % name
    if "error" in resp:
        return "ERROR dari `%s`: %s" % (name, resp["error"])
    result = resp.get("result", {})
    # format MCP: {content: [{type:text, text:...}], isError}
    if isinstance(result, dict) and "content" in result:
        texts = [c.get("text", "") for c in result["content"] if c.get("type") == "text"]
        return "\n".join(texts) if texts else json.dumps(result)
    return json.dumps(result, ensure_ascii=False)[:4000]


def tool_mcp_status(args):
    with POOL_LOCK:
        if not POOL:
            return "Semua MCP mati (0 proses). 0 CPU/0 RAM. Saat AI butuh, otomatis spawn."
        out = ["**%d MCP lagi idup** (auto-mati setelah %ds idle):" % (len(POOL), IDLE_TTL)]
        now = time.time()
        for name, e in POOL.items():
            idle = int(now - e["last"])
            out.append("- `%s` — idle %ds%s" % (name, idle, " ← bunuh soon" if idle > IDLE_TTL * 0.8 else ""))
        return "\n".join(out)


TOOLS = [
    ("mcp_list", "Daftar/cari MCP di katalog+parkiran. AI liat apa aja MCP yg ada (tanpa nyalain).",
     {"type": "object", "properties": {"query": {"type": "string"}}, "required": []}),
    ("mcp_search", "Cari MCP by kata kunci (FTS ringan).",
     {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
    ("mcp_use", "Spawn MCP on-demand & panggil tool-nya. MCP nyala CUMA saat ini, idle auto-mati. name=MCP, tool=nama tool di MCP (atau 'list_tools' untuk liat tools MCP itu), arguments=arg tool.",
     {"type": "object",
      "properties": {"name": {"type": "string"}, "tool": {"type": "string"},
                    "arguments": {"type": "object"}},
      "required": ["name", "tool"]}),
    ("mcp_status", "Lihat MCP mana yg lagi idup sekarang + idle-nya.",
     {"type": "object", "properties": {}}),
]
HANDLERS = {
    "mcp_list": tool_mcp_list, "mcp_search": tool_mcp_search,
    "mcp_use": tool_mcp_use, "mcp_status": tool_mcp_status,
}


def reply(obj):
    sys.stdout.write(json.dumps(obj) + "\n"); sys.stdout.flush()


def handle(msg):
    mid = msg.get("id"); method = msg.get("method", "")
    if method == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion") or ""
        reply({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": want if isinstance(want, str) and want else "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "mcp-router", "version": "1.0.0"}}})
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
            result = fn(p.get("arguments") or {})
            reply({"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": str(result)}], "isError": False}})
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
