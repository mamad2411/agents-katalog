#!/usr/bin/env python3
"""pow — satu pintu ke semua aset lokal, output sengaja dipangkas (hemat context).

Prinsip: AI tidak perlu tahu 300k skill / 100k repo / 894 tool. Cukup 1 baris
perintah, dan semua detail diambil saat benar-benar dipakai (0 token idle).

  pow find <kata>     # cari skill + repo + tool + agent sekaligus (maks 8 baris)
  pow tool            # tool yang sudah terpasang (PATH semua AI)
  pow tool install <owner/name>
  pow agent           # subagent opencode yang tersedia
  pow cost            # audit biaya context: prompt statis vs katalog
  pow scan <path>     # scan keamanan sebelum memakai kode asing
"""
import json
import os
import re
import sqlite3
import subprocess
import sys

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
SKDB = os.path.join(AG, "skills-index.db")
REDB = os.path.join(AG, "repos.db")
READY = os.path.join(AG, "skills-readiness.json")
TOOLS_JSON = os.path.join(AG, "tools-installed.json")
AGENTS = os.path.join(HOME, ".config", "opencode", "agents")
OPENCODE_JSON = os.path.join(HOME, ".config", "opencode", "opencode.json")


def tok(s):
    return max(1, len(s) // 4)


def ready_map():
    try:
        return json.load(open(READY))
    except Exception:
        return {}


def find(q, n=3):
    q = q.strip()
    if not q:
        sys.exit("pakai: pow find <kata>")
    rm = ready_map()
    out = []
    # 1. skill — pakai mesin pencari yang sama dengan `sk` (IDF + sinonim) supaya konsisten
    try:
        r = subprocess.run([sys.executable, os.path.join(AG, "skillq.py"), q, "-n", str(n)],
                           capture_output=True, text=True, timeout=60)
        for line in (r.stdout or "").strip().splitlines():
            if line.startswith("- "):
                out.append("skill  " + line[2:].replace(" — ", " — ")[:110])
    except Exception:
        pass
    # 2. repo
    try:
        c = sqlite3.connect(REDB, timeout=20)
        rows = c.execute(
            "SELECT slug, stars FROM repos WHERE slug LIKE ? OR desc LIKE ? "
            "ORDER BY stars DESC LIMIT ?", (pat, pat, n)).fetchall()
        for slug, st in rows:
            out.append(f"repo   {slug} ⭐{st}")
    except Exception:
        pass
    # 3. tool terpasang
    try:
        reg = json.load(open(TOOLS_JSON))
        hit = [(s, v) for s, v in reg.items() if q.lower() in s.lower() and v.get("status") == "installed"]
        for s, v in hit[:2]:
            out.append(f"tool   {v.get('cmd') or s} ← {s}")
    except Exception:
        pass
    # 3b. MCP terdaftar (semua disabled, nyalakan seperlunya)
    try:
        cfg = json.load(open(OPENCODE_JSON))
        for k, v in (cfg.get("mcp") or {}).items():
            if q.lower() in k.lower():
                out.append(f"mcp    {k} {'ON' if v.get('enabled') else 'off'} → pow mcp on {k}")
    except Exception:
        pass
    # 4. agent
    try:
        for f in sorted(os.listdir(AGENTS)):
            if f.endswith(".md") and q.lower() in f.lower():
                out.append(f"agent  {f[:-3]} (~/.config/opencode/agents/{f})")
    except Exception:
        pass
    # 5. dataset (indeks 957rb+: HF/OpenML/Zenodo) — metadata saja
    try:
        ddb = os.path.join(AG, "datasets-index.db")
        if os.path.exists(ddb):
            dc = sqlite3.connect(ddb, timeout=10)
            terms = " ".join(dict.fromkeys(re.findall(r"[a-zA-Z]{3,}", q.lower())))
            if terms:
                match = '"' + '" OR "'.join(terms.split()) + '"'
                rows = dc.execute(
                    "SELECT d.source,d.slug,d.name,d.downloads FROM ds d "
                    "JOIN ds_fts f ON d.rowid=f.rowid WHERE ds_fts MATCH ? "
                    "ORDER BY d.downloads DESC LIMIT ?", (match, 3)).fetchall()
                for src, slug, name, dl in rows:
                    how = {"hf": f"hf:{slug}", "openml": f"openml:{slug}",
                           "zenodo": f"zenodo:{slug}"}.get(src, slug)
                    out.append(f"data   {how} ⬇{dl} {name[:50]} → data-hub peek {how}")
    except Exception:
        pass
    if not out:
        print("tidak ada hasil")
        return
    print("\n".join(out[:8]))


def tools(args):
    reg = {}
    try:
        reg = json.load(open(TOOLS_JSON))
    except Exception:
        pass
    if args and args[0] == "install":
        if len(args) < 2:
            sys.exit("pakai: pow tool install <owner/name>")
        os.execv(sys.executable, [sys.executable, os.path.join(AG, "tool-install.py"), args[1]])
    ok = [(s, v) for s, v in reg.items() if v.get("status") == "installed"]
    print(f"tool terpasang: {len(ok)} (di PATH: ~/.agents/bin)")
    for s, v in sorted(ok):
        print(f"- {v.get('cmd') or s} ← {s} [{v.get('kind')}]")


def agents():
    try:
        names = [f[:-3] for f in sorted(os.listdir(AGENTS)) if f.endswith(".md")]
    except Exception:
        names = []
    print(f"subagent opencode: {len(names)}")
    print(", ".join(names))


def cost():
    rows = []
    for f, label in ((os.path.join(HOME, ".config", "opencode", "AGENTS.md"), "AGENTS.md"),
                     (os.path.join(AG, "RULES.md"), "RULES.md")):
        try:
            rows.append((label, tok(open(f, encoding="utf-8", errors="ignore").read())))
        except Exception:
            pass
    # katalog skill yang terekspos ke prompt
    exposed = 0
    descs = 0
    try:
        c = sqlite3.connect(SKDB, timeout=20)
        for d in os.listdir(os.path.join(HOME, ".opencode", "skills")):
            r = c.execute("SELECT COALESCE(description,'') FROM skills WHERE name=? LIMIT 1",
                          (d,)).fetchone()
            exposed += 1
            descs += tok((r[0] if r else "") + d)
    except Exception:
        pass
    rows.append((f"{exposed} skill terekspos", descs))
    mcp_on = []
    try:
        cfg = json.load(open(OPENCODE_JSON))
        for k, v in (cfg.get("mcp") or {}).items():
            if v.get("enabled"):
                mcp_on.append(k)
    except Exception:
        pass
    total = sum(r[1] for r in rows)
    print("audit context (perkiraan token, statis tiap request):")
    for label, t in rows:
        print(f"  {label:26} {t:>6}")
    print(f"  {'MCP aktif':26} {len(mcp_on):>6}  ({', '.join(mcp_on) or '-'})")
    print(f"  {'TOTAL (tanpa MCP)':26} {total:>6}  ≈ {total / 128000 * 100:.1f}% dari 128k")
    print("katalog besar TIDAK masuk context: sk / pow find / repo-hub = 0 token saat idle")


MCP_VERIFIED = os.path.join(AG, "mcp-verified.json")
MCP_HUB = os.path.join(AG, "mcp-hub.py")


def mcp(args):
    """Kelola MCP: semua terdaftar DISABLED, nyalakan hanya saat butuh."""
    try:
        cfg = json.load(open(OPENCODE_JSON))
    except Exception:
        cfg = {}
    reg = cfg.get("mcp") or {}
    ver = {}
    try:
        ver = json.load(open(MCP_VERIFIED))
    except Exception:
        pass
    cats = {}
    for k in reg:
        cats.setdefault((ver.get(k) or {}).get("cat", "lain"), []).append(k)

    def item(k):
        v = reg[k]
        st = "ON " if v.get("enabled") else "off"
        vd = (ver.get(k) or {}).get("verdict", "-")
        cmd = " ".join(v.get("command") or [v.get("url", "")])[:52]
        return f"  {st} {k:<20} {vd:<14} {cmd}"

    if not args:
        on = [k for k, v in reg.items() if v.get("enabled")]
        print(f"MCP terdaftar: {len(reg)} · aktif: {len(on)} ({', '.join(on) or '-'})")
        for c in sorted(cats):
            print(f"\n[{c}] {len(cats[c])}")
            for k in sorted(cats[c]):
                print(item(k))
        print("\nnyalakan: pow mcp on <nama> · matikan: pow mcp off <nama>")
        print("filter  : pow mcp cat design|coding|deploy|test|data|search|comms|docs|memory|security|util")
        print("tambah  : pow mcp search <kata> lalu pow mcp add <nama> (unduh + SCAN + daftar mati)")
        return
    if args[0] == "cat" and len(args) > 1:
        q = args[1].lower()
        hit = [k for k in cats.get(q, [])] or [k for k in reg if q in k.lower()]
        if not hit:
            sys.exit(f"tidak ada MCP kategori '{q}' (ada: {', '.join(sorted(cats))})")
        print(f"[{q}] {len(hit)} MCP")
        for k in sorted(hit):
            print(item(k))
        return
    sub = args[0]
    if sub in ("on", "off") and len(args) > 1:
        name = args[1]
        if name not in reg:
            sys.exit(f"tidak terdaftar: {name} (lihat: pow mcp)")
        reg[name]["enabled"] = sub == "on"
        cfg["mcp"] = reg
        json.dump(cfg, open(OPENCODE_JSON, "w"), indent=2, ensure_ascii=False)
        print(f"{name} -> enabled={sub == 'on'}")
        if sub == "on":
            on = [k for k, v in reg.items() if v.get("enabled")]
            print(f"aktif sekarang: {', '.join(on)}")
            print("catatan: MCP menambah schema tool ke SETIAP request — matikan lagi setelah selesai.")
        return
    os.execv(sys.executable, [sys.executable, MCP_HUB] + args)


def scan(path):
    if not path:
        sys.exit("pakai: pow scan <path>")
    r = subprocess.run([sys.executable, os.path.join(AG, "repo-hub.py"), "scan", path, "-n", "5"],
                       capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[:900])


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd, rest = a[0], a[1:]
    if cmd == "find":
        find(" ".join(rest))
    elif cmd == "tool":
        tools(rest)
    elif cmd == "mcp":
        mcp(rest)
    elif cmd == "agent":
        agents()
    elif cmd == "cost":
        cost()
    elif cmd == "scan":
        scan(" ".join(rest))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
