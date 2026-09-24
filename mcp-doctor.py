#!/usr/bin/env python3
"""mcp-doctor.py — tes handshake MCP beneran (bukan cuma nama bagus).
Kandidat dicoba dalam bentuk npx/uvx (auto-download) atau binary lokal.
Hasil: ALIVE (bisa initialize+tools/list) / DEAD / BUTuh-KEY.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

H = os.path.expanduser("~")
SPECS = {
  # --- yang sudah terbukti lokal (codex) ---
  "skill-catalog":        ["python3", H+"/.agents/skill-mcp.py"],
  "skill-graph":          ["/opt/homebrew/bin/skill-graph"],
  "tokz-compress":        ["tokz-compress"],
  "fetch":                ["uvx", "mcp-server-fetch"],
  "git":                  ["uvx", "mcp-server-git"],
  "time":                 ["uvx", "mcp-server-time"],
  "sqlite":               ["uvx", "mcp-server-sqlite", "--db-path", H+"/.agents/skills-index.db"],
  # --- kandidat via npx (auto-download, gratis, tanpa API key) ---
  "filesystem":           ["npx", "-y", "@modelcontextprotocol/server-filesystem", H+"/receptor"],
  "memory":               ["npx", "-y", "@modelcontextprotocol/server-memory"],
  "sequential-thinking":  ["npx", "-y", "@modelcontextprotocol/server-sequential-thinking"],
  "everything":           ["npx", "-y", "@modelcontextprotocol/server-everything"],
  "playwright":           ["npx", "-y", "@playwright/mcp@latest"],
  "context7":             ["npx", "-y", "@upstash/context7-mcp"],
  "puppeteer":            ["npx", "-y", "@modelcontextprotocol/server-puppeteer"],
  # --- butuh API key (cuma dites kalau env-nya ada) ---
  "firecrawl":            ["npx", "-y", "firecrawl-mcp"],
  "tavily":               ["npx", "-y", "tavily-mcp"],
  "brave-search":         ["npx", "-y", "@modelcontextprotocol/server-brave-search"],
  "github":               ["npx", "-y", "@modelcontextprotocol/server-github"],
  # --- kandidat berguna (memory/analitik/file-ops), tanpa API key ---
  "desktop-commander":    ["npx", "-y", "@wonderwhy-er/desktop-commander@latest"],
  "duckdb":               ["uvx", "mcp-server-duckdb", "--db-path", H+"/.agents/skills-index.db"],
  "memory-bank":          ["npx", "-y", "@allpepper/memory-bank-mcp"],
  "sqlite":               ["uvx", "mcp-server-sqlite", "--db-path", H+"/.agents/skills-index.db"],
  "framelink-figma-mcp":   ["npx", "-y", "figma-developer-mcp"],
  "ddg-search":            ["uvx", "duckduckgo-mcp-server"],
}
ENV_KEYS = {"firecrawl": ["FIRECRAWL_API_KEY"], "tavily": ["TAVILY_API_KEY"],
            "brave-search": ["BRAVE_API_KEY"], "github": ["GITHUB_PERSONAL_ACCESS_TOKEN", "GITHUB_TOKEN"]}

def probe(name, cmd):
    keys = ENV_KEYS.get(name, [])
    if keys and not any(os.environ.get(k) for k in keys):
        return name, "BUTUH-KEY", f"set {keys[0]} dulu"
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, text=True, env={**os.environ})
        req = [{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"doctor","version":"0"}}},
               {"jsonrpc":"2.0","method":"notifications/initialized"},
               {"jsonrpc":"2.0","id":2,"method":"tools/list"}]
        p.stdin.write("\n".join(json.dumps(r) for r in req) + "\n"); p.stdin.flush()
        tools = -1
        import time
        t0 = time.time()
        limit = 60 if (cmd[0] in ("npx", "uvx", "bunx")) else 30  # npx/uvx butuh download
        import select
        while time.time() - t0 < limit:
            rdy, _, _ = select.select([p.stdout], [], [], 1.0)  # tick 1 dtk: deadline benar2 dievaluasi
            if not rdy:
                continue
            line = p.stdout.readline()
            if not line: break
            try: d = json.loads(line)
            except Exception: continue
            if d.get("id") == 1 and "result" not in d:
                p.kill(); return name, "DEAD", str(d.get("error", {}))[:60]
            if d.get("id") == 2:
                tools = len((d.get("result") or {}).get("tools", [])) if "result" in d else -2
                break
        p.kill()
        return (name, "ALIVE", f"{tools} tools") if tools >= 0 else (name, "DEAD", "tidak jawab tools/list")
    except FileNotFoundError as e:
        return name, "DEAD", f"runtime hilang: {e.filename}"
    except Exception as e:
        return name, "DEAD", str(e)[:60]

if __name__ == "__main__":
    only = {x.strip() for x in sys.argv[sys.argv.index("--only")+1].split(",")} if "--only" in sys.argv else None
    specs = {k: v for k, v in SPECS.items() if not only or k in only}
    res = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(probe, n, c): n for n, c in specs.items()}
        for f in as_completed(futs):
            n, st, info = f.result(); res[n] = (st, info)
    # retry sekali (serial, tanpa badai) utk DEAD "tidak jawab tools/list"
    for n in list(specs):
        s, i = res.get(n, ("", ""))
        if s == "DEAD" and i == "tidak jawab tools/list":
            n2, s2, i2 = probe(n, specs[n]); res[n] = (s2, i2)
    alive = sorted(n for n, (s, _) in res.items() if s == "ALIVE")
    print('%-20s %-10s %s' % ('server','status','catatan'))
    for n in specs:
        s, i = res[n]
        print('%-20s %-10s %s' % (n, s, i))
    print()
    print('ALIVE  :', ', '.join(alive))
    rpath = os.path.expanduser('~/.agents/mcp-doctor-result.json')
    if only:
        try: prev = json.load(open(rpath))
        except Exception: prev = {}
        prev.update(res); res = prev
    json.dump(res, open(rpath, 'w'), indent=2)
