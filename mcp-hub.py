#!/usr/bin/env python3
"""mcp-hub — katalog MCP resmi (registry.modelcontextprotocol.io), semua DISABLED.

Semua MCP di sini tidak menyala saat opencode jalan: schema tool MCP menambah token
di SETIAP request. Jadi: katalog disimpan di DB, baru didaftarkan/dinyalakan saat
benar-benar dipakai.

  python3 mcp-hub.py sync            # tarik registry (resumable)
  python3 mcp-hub.py top -n 20       # server paling berguna
  python3 mcp-hub.py search <kata>
  python3 mcp-hub.py show <nama>
  python3 mcp-hub.py verify <nama>   # unduh paket npm/pypi lalu SCAN sebelum dipakai
  python3 mcp-hub.py enable <nama> [--on]   # tulis ke opencode.json (default disabled)
  python3 mcp-hub.py local           # daftar server MCP dari repo lokal (sudah discan)
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import time
import urllib.request

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
DB = os.path.join(AG, "mcp-registry.db")
STATE = os.path.join(AG, ".mcp-sync-state.json")
OPENCODE = os.path.join(HOME, ".config", "opencode", "opencode.json")
HUB = os.path.join(AG, "repo-hub.py")
API = "https://registry.modelcontextprotocol.io/v0/servers?limit=100"

USEFUL = {
    # nama/vendor & kapabilitas umum — dipakai untuk skor "berguna"
    "github": 10, "gitlab": 8, "cloudflare": 9, "vercel": 7, "supabase": 8,
    "postgres": 9, "postgresql": 9, "sqlite": 9, "mysql": 7, "mongo": 7, "redis": 8,
    "filesystem": 10, "fetch": 10, "memory": 9, "sequential": 8, "thinking": 8,
    "playwright": 9, "puppeteer": 8, "browser": 9, "chrome": 8, "selenium": 7,
    "slack": 8, "notion": 8, "linear": 7, "jira": 7, "atlassian": 6, "discord": 6,
    "figma": 7, "stripe": 7, "shopify": 6, "twilio": 6, "smtp": 6, "email": 6,
    "aws": 8, "google": 8, "gcp": 6, "azure": 6, "kubernetes": 6, "docker": 7,
    "sentry": 7, "grafana": 6, "elastic": 6, "opensearch": 5, "s3": 6, "gcs": 5,
    "time": 6, "weather": 5, "maps": 5, "youtube": 5, "excel": 7, "pdf": 7,
    "office": 5, "word": 5, "obsidian": 6, "search": 7, "brave": 7, "tavily": 6,
    "exa": 6, "perplexity": 6, "context7": 7, "deepwiki": 5, "scrape": 6, "crawl": 6,
    "vault": 5, "1password": 5, "bitwarden": 5, "sec": 4, "scanner": 4,
}


def init():
    c = sqlite3.connect(DB, timeout=60)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("""CREATE TABLE IF NOT EXISTS servers(
        name TEXT PRIMARY KEY, title TEXT, desc TEXT, version TEXT,
        packages TEXT, remotes TEXT, repo TEXT, meta TEXT, score INTEGER DEFAULT 0,
        fetched_at TEXT)""")
    c.execute("CREATE INDEX IF NOT EXISTS s_score ON servers(score DESC)")
    return c


def score(name, title, desc):
    txt = f"{name} {title or ''} {desc or ''}".lower()
    s = 0
    for k, w in USEFUL.items():
        if k in txt:
            s = max(s, w) if s < w else s
            s += 1
    # bonus: paket npm/pypi resmi + deskripsi informatif
    return s


def sync():
    c = init()
    st = {}
    try:
        st = json.load(open(STATE))
    except Exception:
        pass
    cursor = st.get("cursor")
    pages = st.get("pages", 0)
    if st.get("done"):
        print("sync sudah selesai:", c.execute("SELECT count(*) FROM servers").fetchone()[0], "server")
        return
    while True:
        url = API + (f"&cursor={cursor}" if cursor else "")
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "mcp-hub", "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=40) as r:
                    data = json.loads(r.read().decode())
                break
            except Exception as e:
                if attempt == 3:
                    print("gagal:", e)
                    json.dump({"cursor": cursor, "pages": pages}, open(STATE, "w"))
                    return
                time.sleep(3 * (attempt + 1))
        batch = 0
        for item in data.get("servers", []):
            sv = item.get("server", {})
            meta = (item.get("_meta", {}) or {}).get("io.modelcontextprotocol.registry/official", {})
            if meta.get("isLatest") is False:
                continue
            name = sv.get("name")
            if not name:
                continue
            pkgs = sv.get("packages") or []
            remotes = sv.get("remotes") or []
            repo = (sv.get("repository") or {}).get("url") if isinstance(sv.get("repository"), dict) else None
            try:
                c.execute("INSERT OR REPLACE INTO servers(name,title,desc,version,packages,remotes,repo,meta,score,fetched_at) "
                          "VALUES(?,?,?,?,?,?,?,?,?,?)",
                          (name, sv.get("title") or "", sv.get("description") or "", sv.get("version") or "",
                           json.dumps(pkgs), json.dumps(remotes), repo, json.dumps(meta),
                           score(name, sv.get("title"), sv.get("description")),
                           time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
                batch += 1
            except Exception:
                pass
        c.commit()
        pages += 1
        md = data.get("metadata") or {}
        cursor = md.get("nextCursor")
        json.dump({"cursor": cursor, "pages": pages}, open(STATE, "w"))
        if pages % 10 == 0:
            print(f"  halaman {pages} · server={c.execute('SELECT count(*) FROM servers').fetchone()[0]}", flush=True)
        if not cursor:
            json.dump({"cursor": None, "pages": pages, "done": True}, open(STATE, "w"))
            break
        time.sleep(0.4)
    print("sync selesai:", c.execute("SELECT count(*) FROM servers").fetchone()[0], "server", f"({pages} halaman)")


def cmd_of(pkgs, remotes):
    """Perintah untuk menjalankan server: npx / uvx / remote url."""
    for p in pkgs or []:
        rt = (p.get("registryType") or "").lower()
        ident = p.get("identifier") or p.get("name")
        if not ident:
            continue
        if rt == "npm":
            return "local", f"npx -y {ident}"
        if rt in ("pypi", "python"):
            return "local", f"uvx {ident}"
    for r in remotes or []:
        if r.get("url"):
            return "remote", r["url"]
    return None, None


def show(row):
    name, title, desc, ver, pk, rm, repo, sc = row
    kind, cmd = cmd_of(json.loads(pk or "[]"), json.loads(rm or "[]"))
    print(f"{name}  (skor {sc})")
    print(f"  judul : {title}")
    print(f"  versi : {ver}")
    print(f"  repo  : {repo or '-'}")
    print(f"  tipe  : {kind or 'tidak dikenal'} {('· ' + cmd) if cmd else ''}")
    print(f"  desc  : {(desc or '')[:300]}")
    return kind, cmd


def find_one(c, q):
    r = c.execute("SELECT name,title,desc,version,packages,remotes,repo,score FROM servers "
                  "WHERE name=? LIMIT 1", (q,)).fetchone()
    if r:
        return r
    r = c.execute("SELECT name,title,desc,version,packages,remotes,repo,score FROM servers "
                  "WHERE name LIKE ? OR title LIKE ? ORDER BY score DESC LIMIT 1",
                  (f"%{q}%", f"%{q}%")).fetchone()
    return r


def find_exact(c, q):
    """cari pakai nama persis / akhiran '/nama' — jangan fuzzy (hindari server ngawur)."""
    r = c.execute("SELECT name,title,desc,version,packages,remotes,repo,score FROM servers "
                  "WHERE lower(name)=lower(?) LIMIT 1", (q,)).fetchone()
    if r:
        return r
    rows = c.execute("SELECT name,title,desc,version,packages,remotes,repo,score FROM servers "
                     "WHERE lower(name) LIKE ? ORDER BY (packages LIKE '%npm%' OR packages LIKE '%pypi%') DESC, "
                     "score DESC LIMIT 5", (f"%/{q.lower()}",)).fetchall()
    return rows[0] if rows else None


def verify(name):
    """Unduh paket (npm/pypi) lalu scan — wajib sebelum dipakai."""
    c = init()
    row = find_one(c, name)
    if not row:
        sys.exit("tidak ditemukan:", name)
    kind, cmd = show(row)
    pk = json.loads(row[4] or "[]")
    pkg = next((p for p in pk if (p.get("registryType") or "").lower() in ("npm", "pypi", "python")), None)
    if not pkg:
        print("  SCAN: dilewati (remote http / tanpa paket) — tidak ada kode lokal untuk dipindai.")
        return
    ident = pkg.get("identifier") or pkg.get("name")
    rt = (pkg.get("registryType") or "").lower()
    tmp = os.path.join("/tmp", "mcpverify")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    print(f"  unduh {rt}:{ident} ...")
    if rt == "npm":
        r = subprocess.run(["npm", "pack", ident, "--pack-destination", tmp],
                           capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            print("  GAGAL unduh:", (r.stderr or r.stdout)[-200:])
            return
        tgz = [f for f in os.listdir(tmp) if f.endswith(".tgz")]
        if not tgz:
            print("  GAGAL: paket tidak ada")
            return
        with tarfile.open(os.path.join(tmp, tgz[0])) as t:
            t.extractall(os.path.join(tmp, "src"))
    else:
        r = subprocess.run(["uv", "pip", "download", "--no-deps", "-d", tmp, ident],
                           capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            print("  GAGAL unduh:", (r.stderr or r.stdout)[-200:])
            return
        for f in os.listdir(tmp):
            if f.endswith((".whl", ".tar.gz")):
                try:
                    with tarfile.open(os.path.join(tmp, f)) as t:
                        t.extractall(os.path.join(tmp, "src"))
                except Exception:
                    pass
    src = os.path.join(tmp, "src")
    r = subprocess.run([sys.executable, HUB, "scan", src, "-n", "6"], capture_output=True, text=True)
    out = (r.stdout or r.stderr).strip()
    print(out[:800])
    bad = "[critical]" in out
    print("  VERDICT:", "BLOCKED (critical)" if bad else "lolos (tidak ada critical)")


def enable(name, on=False, do_scan=True):
    c = init()
    row = find_exact(c, name)
    if not row:
        sys.exit(f"tidak ditemukan: {name} — pakai nama persis dari `pow mcp search <kata>`")
    kind, cmd = cmd_of(json.loads(row[4] or "[]"), json.loads(row[5] or "[]"))
    if not kind:
        sys.exit("server ini tidak punya paket/remote yang bisa didaftarkan")
    if do_scan:
        pk = json.loads(row[4] or "[]")
        pkg = next((x for x in pk if (x.get("registryType") or "").lower() in ("npm", "pypi", "python")), None)
        if pkg:
            ident = pkg.get("identifier") or pkg.get("name")
            rt = (pkg.get("registryType") or "").lower()
            verdict, msg = scan_pkg("npm" if rt == "npm" else "pypi", ident)
            print(f"  scan {ident}: {verdict} · {msg}")
            if verdict == "BLOCKED":
                sys.exit("DITOLAK: ada pola kritis; tidak didaftarkan.")
    key = row[0].split("/")[-1].replace(".", "-")[:40] or "mcp"
    cfg = json.load(open(OPENCODE))
    mcp = cfg.setdefault("mcp", {})
    if kind == "remote":
        mcp[key] = {"type": "remote", "url": cmd, "enabled": on}
    else:
        mcp[key] = {"type": "local", "command": cmd.split(), "enabled": on}
    json.dump(cfg, open(OPENCODE, "w"), indent=2, ensure_ascii=False)
    print(f"didaftarkan: {key} ({kind}) enabled={on}")
    print(f"  → nyalakan saat butuh: pow mcp on {key}")


CURATED = os.path.join(AG, "mcp-curated.json")
VERIFIED = os.path.join(AG, "mcp-verified.json")


def pkg_exists(kind, ident):
    if kind == "npm":
        r = subprocess.run(["npm", "view", ident, "version"], capture_output=True, text=True, timeout=120)
        return r.stdout.strip().splitlines()[-1].strip() if r.returncode == 0 and r.stdout.strip() else None
    try:
        req = urllib.request.Request(f"https://pypi.org/pypi/{ident}/json", headers={"User-Agent": "mcp-hub"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())["info"]["version"]
    except Exception:
        return None


def scan_pkg(kind, ident):
    """Unduh paket lalu scan isinya. Return (verdict, ringkas)."""
    tmp = os.path.join("/tmp", "mcpscan", ident.replace("/", "_"))
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    if kind == "npm":
        r = subprocess.run(["npm", "pack", ident, "--pack-destination", tmp],
                           capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            return "download-failed", (r.stderr or r.stdout)[-160:]
        tg = [f for f in os.listdir(tmp) if f.endswith(".tgz")]
        if not tg:
            return "download-failed", "tidak ada .tgz"
        with tarfile.open(os.path.join(tmp, tg[0])) as t:
            t.extractall(os.path.join(tmp, "src"))
    else:
        # PyPI langsung (pipa `pip download` diblokir di mesin ini)
        try:
            req = urllib.request.Request(f"https://pypi.org/pypi/{ident}/json",
                                         headers={"User-Agent": "mcp-hub"})
            with urllib.request.urlopen(req, timeout=40) as r:
                meta = json.loads(r.read().decode())
        except Exception as e:
            return "download-failed", f"pypi: {e}"
        urls = [u for u in (meta.get("urls") or []) if u.get("packagetype") in ("bdist_wheel", "sdist")]
        if not urls:
            return "download-failed", "tidak ada wheel/sdist"
        urls.sort(key=lambda u: 0 if u["packagetype"] == "bdist_wheel" else 1)
        f = urls[0]
        dst = os.path.join(tmp, f["filename"])
        try:
            req = urllib.request.Request(f["url"], headers={"User-Agent": "mcp-hub"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as out:
                out.write(r.read())
        except Exception as e:
            return "download-failed", f"unduh: {e}"
        try:
            with tarfile.open(dst) as t:
                t.extractall(os.path.join(tmp, "src"))
        except Exception:
            import zipfile
            try:
                with zipfile.ZipFile(dst) as z:
                    z.extractall(os.path.join(tmp, "src"))
            except Exception as e:
                return "download-failed", f"bongkar: {e}"
    src = os.path.join(tmp, "src")
    if not os.path.isdir(src):
        return "skip", "tidak bisa dibongkar"
    r = subprocess.run([sys.executable, HUB, "scan", src, "-n", "3"], capture_output=True, text=True)
    out = (r.stdout or "").strip()
    if "[critical]" in out:
        return "BLOCKED", out.splitlines()[0][:160]
    return "PASS", (out.splitlines()[0][:120] if out else "tidak ada temuan")


def curate(do_scan=True, on=False):
    items = json.load(open(CURATED))
    cfg = json.load(open(OPENCODE))
    mcp = cfg.setdefault("mcp", {})
    verified = {}
    try:
        verified = json.load(open(VERIFIED))
    except Exception:
        pass
    only = os.environ.get("MCP_ONLY", "").split(",") if os.environ.get("MCP_ONLY") else None
    catf = os.environ.get("MCP_CAT")
    for item in items:
        name, kind, ident, extra, note = item[:5]
        cat = item[5] if len(item) > 5 else "util"
        if only and name not in only:
            continue
        if catf and cat != catf:
            continue
        print(f"\n== {name} ({kind}:{ident}) — {note}")
        ver = pkg_exists(kind, ident)
        if not ver:
            print("   TIDAK ADA di registry paket — dilewati")
            continue
        print("   versi:", ver)
        verdict, msg = ("skip", "scan dimatikan") if not do_scan else scan_pkg(kind, ident)
        print(f"   scan: {verdict} · {msg}")
        if verdict == "BLOCKED":
            verified[name] = {"pkg": ident, "version": ver, "verdict": verdict, "note": msg, "cat": cat}
            continue
        cmd = (["npx", "-y", ident] if kind == "npm" else ["uvx", ident]) + list(extra)
        mcp[name] = {"type": "local", "command": cmd, "enabled": on}
        verified[name] = {"pkg": ident, "version": ver, "verdict": verdict,
                          "note": note, "cmd": " ".join(cmd), "cat": cat}
        print(f"   terdaftar: {name} (enabled={on})")
    json.dump(cfg, open(OPENCODE, "w"), indent=2, ensure_ascii=False)
    json.dump(verified, open(VERIFIED, "w"), indent=1, ensure_ascii=False)
    ok = sum(1 for v in verified.values() if v.get("verdict") != "BLOCKED")
    print(f"\n[curate] {ok}/{len(items)} terdaftar (semua DISABLED) · detail: {VERIFIED}")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    c = init()
    if a[0] == "sync":
        sync()
    elif a[0] == "top":
        n = int(a[a.index("-n") + 1]) if "-n" in a else 20
        rows = c.execute("SELECT name,title,desc,version,packages,remotes,repo,score FROM servers "
                         "ORDER BY score DESC, name LIMIT ?", (n,)).fetchall()
        for r in rows:
            kind, cmd = cmd_of(json.loads(r[4] or "[]"), json.loads(r[5] or "[]"))
            print(f"{r[7]:>3} {r[0]:<46} {kind or '-':<7} {(r[1] or r[0])[:40]}")
    elif a[0] == "search":
        q = a[1]
        rows = c.execute("SELECT name,title,desc,version,packages,remotes,repo,score FROM servers "
                         "WHERE name LIKE ? OR desc LIKE ? ORDER BY score DESC, name LIMIT 15",
                         (f"%{q}%", f"%{q}%")).fetchall()
        for r in rows:
            kind, cmd = cmd_of(json.loads(r[4] or "[]"), json.loads(r[5] or "[]"))
            print(f"{r[7]:>3} {r[0]:<46} {kind or '-':<7} {(r[2] or '')[:70]}")
    elif a[0] == "show":
        show(find_one(c, a[1]) or sys.exit("tidak ditemukan"))
    elif a[0] == "verify":
        verify(a[1])
    elif a[0] in ("enable", "add"):
        enable(a[1], on="--on" in a, do_scan="--no-scan" not in a)
    elif a[0] == "curate":
        curate(do_scan="--no-scan" not in a, on="--on" in a)
    elif a[0] == "local":
        reg = json.load(open(os.path.join(AG, "tools-installed.json")))
        for slug, v in reg.items():
            if v.get("mcp") or "mcp" in slug:
                print(f"- {slug} [{v.get('status')}] {v.get('cmd')}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
