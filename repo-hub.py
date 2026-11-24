#!/usr/bin/env python3
"""repo-hub — bikin repo di ~/.agents/repo-refs benar-benar kepakai.

Subcommand:
  stats                     ringkasan isi ~/.agents/repos.db
  harvest                   tarik slug repo dari sumber LOKAL (0 request jaringan)
  expand [--target N]       tambah repo via GitHub search API (resumable)
  ingest                    daftarkan SKILL.md dari repo-refs ke skills-store + skills-index.db
  search "kata" [-n 10]     cari repo (nama/deskripsi/topik)
  get <owner/name>          shallow clone repo saat benar-benar dibutuhkan
  catalog                   tulis ~/.agents/repo-catalog.md

DB: ~/.agents/repos.db   |   Store skill: ~/.agents/skills-store
"""
import os, re, sys, json, time, shutil, sqlite3, subprocess

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
DB = os.path.join(AG, "repos.db")
SKILL_DB = os.path.join(AG, "skills-index.db")
REFS = os.path.join(AG, "repo-refs")
STORE = os.path.join(AG, "skills-store")

# pola berbahaya di dalam skill dari repo asing -> tidak di-ingest
# aturan kritis untuk GATE ingest (pola penyadapan/eksfiltrasi/reverse shell)
BLOCK = [
    re.compile(r"(?:curl|wget)\s+[^\n|]*\|\s*(?:ba|z|fi)?sh", re.I),
    re.compile(r"(?:base64\s+(?:-d|--decode)|FromBase64String)[^\n|]*\|\s*(?:ba|z)?sh", re.I),
    re.compile(r"rm\s+-rf\s+/(?:\s|$|\*)"),
    re.compile(r"\bnc\s+-[a-z]*e\b|/dev/tcp/|socat[^\n]*exec:"),
    re.compile(r":\(\)\s*\{.*\|.*&.*\}", re.S),
    re.compile(r"security\s+find-(?:generic|internet)-password|security\s+dump-keychain"),
    re.compile(r"xmrig|stratum\+tcp|minerd|cpuminer"),
    re.compile(r"launchctl\s+(?:load|submit)|LaunchAgents/[^\n]{0,60}\.plist"),
    re.compile(r"powershell[^\n]*-enc(?:odedcommand)?\s+[A-Za-z0-9+/=]{40,}|Invoke-Expression"),
    re.compile(r"(?:cat|cp|tar|zip)[^\n]{0,60}(?:\.ssh/id_|\.aws/credentials|\.netrc|key4\.db|Login Data)"),
    re.compile(r"pynput\.keyboard|keyboard\.Listener|CGEventTapCreate|SetWindowsHookEx|GetAsyncKeyState"),
]


def connect():
    c = sqlite3.connect(DB, timeout=60)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=60000")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS repos(
      slug TEXT PRIMARY KEY, owner TEXT, name TEXT, url TEXT,
      desc TEXT, stars INTEGER DEFAULT 0, lang TEXT, topics TEXT,
      origin TEXT, has_skill INTEGER DEFAULT 0, skill_count INTEGER DEFAULT 0,
      local_path TEXT, state TEXT DEFAULT 'stub', added_at TEXT
    );
    CREATE INDEX IF NOT EXISTS repos_stars ON repos(stars DESC);
    CREATE INDEX IF NOT EXISTS repos_state ON repos(state);
    CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
    CREATE VIRTUAL TABLE IF NOT EXISTS repos_fts USING fts5(slug, desc, topics);
    """)
    return c


def slugify(s):
    return re.sub(r"[^a-z0-9._-]+", "-", s.lower()).strip("-")


def upsert(c, slug, **kw):
    slug = slug.lower()
    row = c.execute("SELECT slug FROM repos WHERE slug=?", (slug,)).fetchone()
    owner, name = (slug.split("/", 1) + [""])[:2]
    if row:
        sets, vals = [], []
        for k, v in kw.items():
            if k == "origin":
                continue  # asal pertama kali ditemukan dipertahankan
            if v in (None, "", 0) and k not in ("state",):
                continue
            sets.append(f"{k}=?"); vals.append(v)
        if sets:
            c.execute(f"UPDATE repos SET {','.join(sets)} WHERE slug=?", vals + [slug])
        return False
    kw.setdefault("origin", "harvest")
    c.execute(
        "INSERT INTO repos(slug,owner,name,url,desc,stars,lang,topics,origin,has_skill,"
        "skill_count,local_path,state,added_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (slug, owner, name, kw.get("url") or f"https://github.com/{slug}",
         kw.get("desc") or "", kw.get("stars") or 0, kw.get("lang") or "",
         kw.get("topics") or "", kw["origin"], kw.get("has_skill") or 0,
         kw.get("skill_count") or 0, kw.get("local_path") or "",
         kw.get("state") or "stub", time.strftime("%Y-%m-%d")))
    c.execute("INSERT INTO repos_fts(slug,desc,topics) VALUES(?,?,?)",
              (slug, kw.get("desc") or "", kw.get("topics") or ""))
    return True


GH_RE = re.compile(r"github\.com[/:]([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


def scan_local_paths():
    """(slug, local_path) dari repo-refs + slug dari sumber skill lokal."""
    found = {}
    if os.path.isdir(REFS):
        for d in os.scandir(REFS):
            if not d.is_dir():
                continue
            parts = d.name.split("_", 1)
            if len(parts) == 2:
                found[f"{parts[0]}/{parts[1]}".lower()] = d.path
    return found


def harvest(args):
    c = connect()
    local = scan_local_paths()
    added = 0
    for slug, path in local.items():
        real = os.path.isdir(os.path.join(path, ".git")) or os.path.exists(os.path.join(path, ".cloned"))
        prev = c.execute("SELECT has_skill FROM repos WHERE slug=?", (slug.lower(),)).fetchone()
        st = "ingested" if (prev and prev[0]) else ("cloned" if real else "stub")
        if upsert(c, slug, origin="repo-refs", local_path=path, state=st):
            added += 1
    c.commit()
    print(f"[harvest] repo-refs: {len(local)} terdaftar, {added} baru")

    # sumber lokal lain: URL github di katalog skill + file awesome-list
    slugs = set()
    try:
        s = sqlite3.connect(SKILL_DB)
        for (src,) in s.execute("SELECT DISTINCT source FROM skills WHERE source LIKE '%github%'"):
            for m in GH_RE.finditer(src or ""):
                slugs.add(f"{m.group(1)}/{m.group(2)}".lower().removesuffix(".git"))
        s.close()
    except Exception as e:
        print("  (skills-index.db dilewati:", e, ")")
    for root, _, files in os.walk(AG):
        if "/.git" in root or "/node_modules" in root:
            continue
        for f in files:
            if not (f.endswith(".txt") or f.endswith(".md")):
                continue
            if root.count(os.sep) - AG.count(os.sep) > 2:
                continue
            try:
                txt = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for m in GH_RE.finditer(txt):
                slugs.add(f"{m.group(1)}/{m.group(2)}".lower().removesuffix(".git"))
    added2 = 0
    for slug in slugs:
        if "/" not in slug or len(slug) > 120:
            continue
        if upsert(c, slug, origin="harvest-url"):
            added2 += 1
    c.commit()
    print(f"[harvest] dari URL lokal: {len(slugs)} slug, {added2} baru")
    stats(args)


def gh(path):
    """gh api GET -> dict/list, tahan 403/429."""
    for attempt in range(5):
        p = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github+json", path],
                           capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout or "null")
        msg = (p.stderr or "") + (p.stdout or "")
        if "rate limit" in msg.lower() or "403" in msg or "429" in msg:
            wait = 65
            m = re.search(r"reset[^0-9]*(\d{10})", msg)
            if m:
                wait = max(30, min(3600, int(m.group(1)) - int(time.time()) + 5))
            print(f"  rate limit, tidur {wait}s ...", flush=True)
            time.sleep(wait)
            continue
        raise RuntimeError(msg[:300])
    return None


TOPICS = [
    "claude-skills", "claude-code", "agent-skills", "ai-agents", "mcp-server", "mcp",
    "claude", "llm", "autonomous-agents", "ai-tools", "rag", "llmops",
    "prompt-engineering", "skills", "codex", "gemini-cli", "opencode", "cursor",
    "vibe-coding", "computer-use", "browser-automation", "security-tools", "devops",
    "cli", "whatsapp-api", "mcp-servers", "agent-framework", "multi-agent",
    "ai-coding-assistant", "workflow-automation", "self-hosted", "automation",
    "developer-tools", "api-client", "sdk", "terraform", "kubernetes", "docker",
    "monitoring", "observability", "data-analysis", "web-scraping", "sql",
    # gelombang 2: topik sempit & minim tumpang-tindih -> yield per request lebih tinggi
    "django", "laravel", "rails", "spring-boot", "flutter", "swiftui", "android",
    "ios", "golang", "typescript", "jupyter", "ansible-role", "grafana", "prometheus",
    "elasticsearch", "kafka", "redis", "postgresql", "mysql", "mongodb", "supabase",
    "firebase", "nextjs", "nuxt", "svelte", "astro", "tailwindcss", "shadcn-ui",
    "expo", "tauri", "electron", "wasm", "grpc", "graphql", "openapi", "swagger",
    "oauth", "stripe-api", "telegram-bot", "discord-bot", "slack-bot", "notion-api",
    "airtable", "google-sheets", "pdf-generation", "ocr", "speech-to-text",
    "translation", "image-generation", "ffmpeg", "crawler", "scraper", "etl",
    "airflow", "dbt", "mlops", "pytorch", "tensorflow", "huggingface", "ollama",
    "local-llm", "benchmark", "reverse-engineering", "cybersecurity", "appsec",
    "sast", "secrets-management", "vulnerability-scanner", "log-analysis",
    "incident-response", "backup", "cron", "systemd", "nginx", "traefik", "vault",
    # gelombang 3 (cadangan kalau target belum tercapai)
    "vue", "react", "angular", "solidjs", "remix", "htmx", "alpinejs", "jquery",
    "phoenix", "elixir", "haskell", "scala", "kotlin", "dotnet", "java", "csharp",
    "rust", "zig", "lua", "perl", "ruby", "php", "nodejs", "deno", "bun",
    "fastapi", "flask", "express", "nestjs", "actix", "axum", "gin", "fiber",
    "prisma", "drizzle", "typeorm", "sequelize", "sqlalchemy", "alembic",
    "playwright", "cypress", "selenium", "vitest", "jest", "pytest", "junit",
    "eslint", "prettier", "biome", "ruff", "mypy", "clippy",
    "github-actions", "gitlab-ci", "jenkins", "argocd", "fluxcd", "helm",
    "pulumi", "cloudformation", "serverless", "lambda", "cloudflare-workers",
    "aws", "gcp", "azure", "digitalocean", "vercel", "netlify",
    "queues", "rabbitmq", "nats", "temporal", "websocket", "sse",
    "authentication", "authorization", "rbac", "jwt", "saml", "webauthn",
    "penetration-testing", "osint", "red-team", "blue-team", "threat-modeling",
    "supply-chain-security", "sbom", "container-security", "kubernetes-security",
    "email-automation", "crm", "erp", "ecommerce", "payments", "invoicing",
    "notifications", "sms", "push-notifications", "webhooks", "webhook",
    "scraping-proxy", "dataset", "data-labeling", "analytics", "bi",
    "search-engine", "vector-search", "embeddings", "knowledge-graph",
]
BUCKETS = ["0..4", "5..9", "10..24", "25..49", "50..99", "100..299", "300..999", ">=1000"]


def plan_queries():
    for t in TOPICS:
        for b in BUCKETS:
            yield t, b


def expand(args):
    target = int(args[args.index("--target") + 1]) if "--target" in args else 100000
    budget_min = 45
    if "--minutes" in args:
        budget_min = int(args[args.index("--minutes") + 1])
    c = connect()
    start = time.time()
    done = {r[0] for r in c.execute("SELECT k FROM meta WHERE k LIKE 'q:%'")}
    total = c.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
    print(f"[expand] mulai: {total} repo, target {target}", flush=True)

    for topic, bucket in plan_queries():
        if total >= target:
            break
        if (time.time() - start) / 60 > budget_min:
            print("[expand] budget waktu habis, lanjutkan nanti (resume otomatis)", flush=True)
            break
        key = f"q:{topic}:{bucket}"
        if key in done:
            continue
        q = f"topic:{topic}+stars:{bucket}"
        for page in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            if total >= target:
                break
            try:
                r = gh(f"/search/repositories?q={q}&sort=stars&order=desc&per_page=100&page={page}")
            except Exception as e:
                print(f"  [{topic}:{bucket} p{page}] gagal: {e}", flush=True)
                break
            items = (r or {}).get("items") or []
            if not items:
                break
            for it in items:
                if upsert(c, it["full_name"], desc=(it.get("description") or "")[:400],
                          stars=it.get("stargazers_count") or 0,
                          lang=it.get("language") or "",
                          topics=" ".join(it.get("topics") or []),
                          origin=f"api:{topic}"):
                    total += 1
            c.commit()
            time.sleep(2.1)  # search API 30 req/menit
        c.execute("INSERT OR REPLACE INTO meta(k,v) VALUES(?,?)", (key, str(int(time.time()))))
        c.commit()
        print(f"  {topic}:{bucket} -> total {total}", flush=True)
    print(f"[expand] selesai: {total} repo", flush=True)
    stats(args)


def _token():
    try:
        p = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=20)
        return (p.stdout or "").strip()
    except Exception:
        return ""


def _api_fast(url, token, tries=4):
    import urllib.request, urllib.error
    for i in range(tries):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "repo-hub",
        })
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                time.sleep(20 + i * 20)
                continue
            raise
        except Exception:
            time.sleep(3)
    return None


def expand_fast(args):
    """Versi paralel: 4 worker + pace 28 req/menit (batas search API 30/menit)."""
    from concurrent.futures import ThreadPoolExecutor
    target = int(args[args.index("--target") + 1]) if "--target" in args else 100000
    budget_min = int(args[args.index("--minutes") + 1]) if "--minutes" in args else 90
    token = _token()
    if not token:
        sys.exit("token GitHub tidak ada (jalankan `gh auth login`)")
    c = connect()
    done = {r[0] for r in c.execute("SELECT k FROM meta WHERE k LIKE 'q:%'")}
    total = c.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
    print(f"[expand-fast] mulai: {total} repo, target {target}", flush=True)

    tasks = [(t, b) for t, b in plan_queries() if f"q:{t}:{b}" not in done]
    # topik yang lebih jarang dipakai didahulukan (yield per request lebih tinggi)
    tasks = [(t, b) for t, b in reversed(tasks)]
    start = time.time()
    recent = []

    def throttle():
        while True:
            now = time.time()
            recent[:] = [x for x in recent if now - x < 60]
            if len(recent) < 26:
                recent.append(now)
                return
            time.sleep(max(0.3, 60 - (now - recent[0]) + 0.5))

    for topic, bucket in tasks:
        if total >= target or (time.time() - start) / 60 > budget_min:
            break
        added = 0
        for page in range(1, 11):
            if total >= target:
                break
            throttle()
            r = _api_fast(f"https://api.github.com/search/repositories?q=topic:{topic}+stars:{bucket}"
                          f"&sort=stars&order=desc&per_page=100&page={page}", token)
            items = ((r or {}).get("items") or [])
            page_added = 0
            for it in items:
                if upsert(c, it["full_name"], desc=(it.get("description") or "")[:400],
                          stars=it.get("stargazers_count") or 0,
                          lang=it.get("language") or "",
                          topics=" ".join(it.get("topics") or []),
                          origin=f"api:{topic}"):
                    page_added += 1
            c.commit()
            added += page_added
            total += page_added
            print(f"  {topic}:{bucket} p{page} +{page_added} -> total {total}", flush=True)
            if len(items) < 100:
                break
        c.execute("INSERT OR REPLACE INTO meta(k,v) VALUES(?,?)",
                  (f"q:{topic}:{bucket}", str(int(time.time()))))
        c.commit()
    print(f"[expand-fast] selesai: {total} repo", flush=True)
    stats(args)


SEC_RULES = [
    ("critical", "reverse-shell", r"\bnc\s+-[a-z]*e\b|/dev/tcp/|\bsocat\b[^\n]*exec:|\bbash\s+-i\s+>&"),
    ("critical", "pipe-to-shell", r"(?:curl|wget)\s+[^\n|]{0,200}\|\s*(?:ba|z|fi)?sh\b"),
    ("critical", "python-remote-exec", r"python[0-9.]*\s+-c\s*[\"']?\$\(curl|eval\s*\$\(curl"),
    ("critical", "powershell-encoded", r"powershell[^\n]*-enc(?:odedcommand)?\s+[A-Za-z0-9+/=]{40,}|Invoke-Expression"),
    ("critical", "rm-rf-root", r"rm\s+-rf\s+/(?:\s|$|\*|~)"),
    ("critical", "credential-read", r"(?:cat|less|head|cp|tar|zip)[^\n]{0,60}(?:\.ssh/id_|\.aws/credentials|\.netrc|\.config/gh/hosts\.yml|login\.keychain|key4\.db|Local State|Login Data)"),
    ("critical", "keychain-dump", r"security\s+find-(?:generic|internet)-password|security\s+dump-keychain"),
    ("critical", "browser-stealer", r"(?:Cookies|Login Data|Local State|key4\.db)[^\n]{0,80}(?:base64|curl|http|upload)"),
    ("critical", "crypto-miner", r"xmrig|stratum\+tcp|minerd|cpuminer"),
    ("critical", "persistence", r"launchctl\s+(?:load|submit)|LaunchAgents/[^\n]{0,60}\.plist|crontab\s+-\s*<|/etc/sudoers"),
    ("critical", "obfuscated-payload", r"(?:base64\s+(?:-d|--decode)|FromBase64String)[^\n|]{0,80}\|\s*(?:ba|z)?sh"),
    ("high", "exfil-possible", r"(?:curl|wget|http\.client|requests\.(?:post|put)|fetch\()[^\n]{0,150}(?:\$\(cat|os\.environ|\$\{?(?:TOKEN|KEY|SECRET|PASSWORD|AWS_)|\$HOME/\.)"),
    ("high", "exfil-endpoint", r"webhook\.site|requestbin|pipedream\.net|transfer\.sh|ngrok\.io|\.ngrok-free\.app|burpcollaborator"),
    ("high", "eval-dynamic", r"\beval\s*\(\s*(?:requests|urllib|fetch|response|r\.text|data)|\bexec\s*\(\s*(?:requests|urllib|response)"),
    ("high", "screen-capture", r"screencapture\s+-|CGWindowListCreateImage|GetDC\(|pyautogui\.screenshot[^\n]{0,60}(?:upload|post|curl)"),
    ("high", "mic-capture", r"ffmpeg[^\n]{0,80}-f\s+avfoundation[^\n]{0,40}:0|arecord[^\n]{0,40}\|\s*curl"),
    ("high", "keylogger", r"pynput\.keyboard|keyboard\.Listener|GetAsyncKeyState|CGEventTapCreate|SetWindowsHookEx"),
    ("high", "env-dump-network", r"(?:printenv|env)\s*\|\s*(?:curl|nc)\b|os\.environ\.(?:items|copy)\(\)[^\n]{0,60}(?:post|curl)"),
    ("high", "write-etc", r"(?:>|tee|cp\s+\S+\s+)/etc/(?:passwd|shadow|hosts|sudoers|cron)"),
    ("high", "persistence-soft", r"chmod\s+\+x[^\n]{0,60}(?:/tmp|~/\.)|\bnohup\b[^\n]{0,80}&|systemctl\s+enable"),
    ("medium", "shortener", r"https?://(?:bit\.ly|tinyurl\.com|t\.co|is\.gd|cutt\.ly)/"),
    ("medium", "hidden-unicode", r"[\u202a-\u202e\u2066-\u2069\u200b-\u200f]"),
    ("medium", "pip-remote", r"pip[0-9.]*\s+install[^\n]{0,80}(?:https?://|git\+)"),
    ("medium", "telegram-exfil", r"api\.telegram\.org/bot[0-9:]+/send(?:Document|Photo|Message)"),
]
EXEC_EXT = (".sh", ".bash", ".zsh", ".py", ".js", ".mjs", ".ts", ".ps1", ".bat", ".rb", ".php")
SCAN_EXT = (".md", ".sh", ".bash", ".zsh", ".py", ".js", ".mjs", ".ts", ".tsx",
            ".rb", ".php", ".ps1", ".bat", ".yml", ".yaml", ".json")
SCAN_SKIP = {".git", "node_modules", "vendor", "__pycache__", ".venv", "venv"}
# prefilter murah: tanpa salah satu kata ini, tidak mungkin ada temuan
QUICK = re.compile(r"curl|wget|base64|\.ssh|aws|keychain|token|secret|password|nc\s|\beval\b|"
                   r"exec\(|osascript|screencapture|avfoundation|launchctl|crontab|sudoers|"
                   r"webhook|ngrok|telegram|stratum|Invoke-Expression|powershell|/dev/tcp", re.I)


def scan(args):
    skip_next = set()
    for flag in ("-n", "--report"):
        if flag in args:
            i = args.index(flag)
            if i + 1 < len(args):
                skip_next.add(args[i + 1])
    roots = [a for a in args if not a.startswith("-") and a not in skip_next]
    report = os.path.join(AG, "security-scan-report.md")
    if "--report" in args:
        report = args[args.index("--report") + 1]
        roots = [r for r in roots if r != report]
    if not roots:
        roots = [os.path.join(REFS), os.path.join(STORE)]
    compiled = [(sev, name, re.compile(rx)) for sev, name, rx in SEC_RULES]
    findings, scanned = [], 0
    total_files = 0
    for root in roots:
        if not os.path.isdir(root):
            continue
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SCAN_SKIP]
            for fn in files:
                if not fn.endswith(SCAN_EXT):
                    continue
                p = os.path.join(base, fn)
                try:
                    if os.path.getsize(p) > 2_000_000:
                        continue
                    txt = open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                total_files += 1
                if not QUICK.search(txt):
                    continue
                scanned += 1
                b64 = None
                if len(txt) < 500_000:
                    for ln in txt.splitlines():
                        if len(ln) > 320 and re.fullmatch(r"[A-Za-z0-9+/=]{320,}", ln.strip()):
                            b64 = ln.strip()
                            break
                for sev, name, rx in compiled:
                    m = rx.search(txt)
                    if not m:
                        continue
                    line = txt.count("\n", 0, m.start()) + 1
                    snippet = txt[max(0, m.start() - 40):m.start() + 80].replace("\n", " ")
                    # konteks: pola di file dokumentasi (.md) bukan eksekusi -> turunkan jadi "docs"
                    eff = sev if fn.endswith(EXEC_EXT) else "docs"
                    findings.append((eff, name, p, line, snippet))
                    if sev == "critical":
                        break
                if b64 and len(b64) > 320:
                    findings.append(("medium", "long-base64", p, 0, b64[:120]))
    order = {"critical": 0, "high": 1, "medium": 2, "docs": 3}
    findings.sort(key=lambda f: order[f[0]])
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"# Scan keamanan skill/repo\n\nfile dilihat: {total_files} · dianalisis: {scanned} · temuan: {len(findings)}\n\n")
        for sev, name, p, line, snip in findings[:400]:
            f.write(f"- **{sev}** `{name}` {p}:{line}\n  ```{snip[:150]}```\n")
    if "--json" in args:
        print(json.dumps([{"severity": a, "rule": b, "path": c, "line": d, "snippet": e}
                          for a, b, c, d, e in findings]))
        return 1 if any(f[0] == "critical" for f in findings) else 0
    shown = int(args[args.index("-n") + 1]) if "-n" in args else 25
    for sev, name, p, line, snip in findings[:shown]:
        short = p.replace(HOME, "~")
        print(f"[{sev}] {name} {short}:{line}")
    crit = sum(1 for f in findings if f[0] == "critical")
    print(f"(dilihat {total_files} file, dianalisis {scanned}, {len(findings)} temuan — {crit} critical · laporan: {report})")
    return 1 if crit else 0


def top(args):
    n = int(args[args.index("-n") + 1]) if "-n" in args else 25
    c = connect()
    for slug, stars, hs, lang, desc in c.execute(
            "SELECT slug, stars, has_skill, lang, substr(COALESCE(desc,''),1,70) FROM repos "
            "ORDER BY stars DESC LIMIT ?", (n,)):
        tag = "skill" if hs else (lang or "-")
        print(f"- {slug} ⭐{stars} [{tag}] {desc}")


def trending(args):
    """Repo baru (<=60 hari) yang paling cepat naik bintang — indikator hits di komunitas."""
    n = int(args[args.index("-n") + 1]) if "-n" in args else 20
    token = _token()
    since = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 60 * 86400))
    c = connect()
    added = 0
    for q in ("topic:claude-skills", "topic:ai-agents", "topic:mcp-server", "topic:security-tools",
              "topic:agent-skills", "claude OR skills OR agents"):
        r = _api_fast("https://api.github.com/search/repositories?q="
                      f"{q.replace(' ', '+')}+created:>{since}&sort=stars&order=desc&per_page=50", token)
        for it in ((r or {}).get("items") or []):
            if upsert(c, it["full_name"], desc=(it.get("description") or "")[:400],
                      stars=it.get("stargazers_count") or 0, lang=it.get("language") or "",
                      topics=" ".join(it.get("topics") or []), origin="api:trending"):
                added += 1
    c.commit()
    print(f"[trending] +{added} repo baru (dibuat setelah {since})")
    for slug, stars, hs, desc in c.execute(
            "SELECT slug, stars, has_skill, substr(COALESCE(desc,''),1,70) FROM repos "
            "WHERE origin='api:trending' ORDER BY stars DESC LIMIT ?", (n,)):
        print(f"- {slug} ⭐{stars} [{'skill' if hs else 'repo'}] {desc}")



def hits(args):
    """Gabungan: repo populer + yang sedang naik + yang disebut di awesome-list lokal."""
    n = int(args[args.index("-n") + 1]) if "-n" in args else 15
    c = connect()
    out = os.path.join(AG, "repo-hits.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Repo hits (bintang + tren + sebutan komunitas)\n\n")
        f.write("Sumber: `python3 ~/.agents/repo-hub.py hits` — data GitHub API + katalog lokal.\n\n")
        sections = [
            ("Sedang naik (dibuat <60 hari, urut bintang)", "origin='api:trending'"),
            ("Paling populer (semua waktu)", "1=1"),
            ("Disebut di awesome-list / katalog skill lokal", "origin LIKE 'harvest%'"),
        ]
        for title, where in sections:
            f.write(f"## {title}\n\n")
            rows = c.execute(
                "SELECT slug, stars, has_skill, substr(COALESCE(desc,''),1,80) FROM repos "
                f"WHERE {where} ORDER BY stars DESC LIMIT ?", (n,)).fetchall()
            for slug, stars, hs, desc in rows:
                tag = "skill" if hs else "repo"
                f.write(f"- `{slug}` \u2b50{stars} [{tag}] {desc}\n")
                print(f"- {slug} \u2b50{stars} [{tag}] {desc}")
            f.write("\n")
    print(f"(laporan: {out})")



AGENT_DIR = os.path.join(HOME, ".config", "opencode", "agents")
DEFAULT_AGENT_MODEL = "opencode/deepseek-v4.1-flash-free"


def _agent_frontmatter(txt):
    if not txt.startswith("---"):
        return None, txt
    end = txt.find("\n---", 3)
    if end < 0:
        return None, txt
    fm = txt[3:end]
    body = txt[end + 4:]
    d = {}
    for line in fm.splitlines():
        m = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if m:
            d[m.group(1).lower()] = m.group(2).strip().strip("'\"")
    return d, body


def install_agents(args):
    """Ubah agent (gaya Claude Code) dari sebuah repo jadi agent opencode.

    Tanpa --apply: hanya daftar kandidat. Dengan --apply: tulis file baru
    ke ~/.config/opencode/agents/<nama>.md (tidak menimpa yang sudah ada).
    """
    if not args:
        sys.exit("pakai: repo-hub.py install-agents <dir-repo> [--pick a,b,c] [--apply]")
    root = os.path.expanduser(args[0])
    pick = None
    if "--pick" in args:
        pick = {x.strip() for x in args[args.index("--pick") + 1].split(",") if x.strip()}
    apply_ = "--apply" in args
    cands = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(base, fn)
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            fm, body = _agent_frontmatter(txt)
            if not fm or not fm.get("description") or len(body.strip()) < 500:
                continue
            name = slugify(fm.get("name") or os.path.splitext(fn)[0])
            cands.append((name, fm.get("description") or "", fm.get("tools") or "", p, body))
    if not cands:
        print("tidak ada kandidat agent (butuh frontmatter name+description dan isi >500 char)")
        return
    print(f"{len(cands)} kandidat agent di {root.replace(HOME, '~')}")
    if not apply_:
        for name, desc, tools, p, _ in cands[:40]:
            print(f"- {name:32s} tools={tools or '-'}  {desc[:60]}")
        print("\nTambah dengan: --pick nama1,nama2 --apply")
        return
    picked = [c for c in cands if pick and c[0] in pick] if pick else cands
    os.makedirs(AGENT_DIR, exist_ok=True)
    written = skipped = 0
    for name, desc, tools, p, body in picked:
        dest = os.path.join(AGENT_DIR, f"{name}.md")
        if os.path.exists(dest):
            skipped += 1
            continue
        t = {x.strip().lower() for x in tools.split(",") if x.strip()}
        can_edit = bool(t & {"write", "edit", "multiedit", "notebookedit"})
        can_bash = "bash" in t
        can_web = bool(t & {"webfetch", "websearch"})
        perm = ["permission:", f"  edit: {'allow' if can_edit else 'deny'}",
                "  task: deny", "  read: allow", "  glob: allow", "  grep: allow"]
        perm.append(f"  bash: {'allow' if can_bash else 'deny'}")
        if can_web:
            perm.append("  webfetch: allow")
        out = ("---\n"
               f"description: {json.dumps(desc, ensure_ascii=False)}\n"
               "mode: subagent\n"
               f"model: {DEFAULT_AGENT_MODEL}\n"
               "steps: 12\n" + "\n".join(perm) + "\n---\n\n"
               + body.strip() + "\n")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(out)
        written += 1
        print(f"+ {name}")
    print(f"selesai: {written} ditulis, {skipped} dilewati (sudah ada) -> {AGENT_DIR.replace(HOME, '~')}")


def read_fm(text):
    name = desc = None
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            fm = text[3:end]
            m = re.search(r"^name:\s*(.+)$", fm, re.M)
            if m:
                name = m.group(1).strip().strip("'\"")
            m = re.search(r"^description:\s*(.+)$", fm, re.M)
            if m:
                desc = m.group(1).strip().strip("'\"")
    if not desc:
        for line in text.splitlines():
            line = line.strip().lstrip("#").strip()
            if len(line) > 20 and not line.startswith("---"):
                desc = line
                break
    return name, desc


def dangerous(text):
    for rx in BLOCK:
        if rx.search(text):
            return rx.pattern
    return None


def ingest(args):
    c = connect()
    s = sqlite3.connect(SKILL_DB)
    existing = {r[0] for r in s.execute("SELECT DISTINCT name FROM skills")}
    added = skipped = blocked = 0
    repos = 0
    for d in sorted(os.scandir(REFS), key=lambda x: x.name):
        if not d.is_dir():
            continue
        skills = []
        for root, dirs, files in os.walk(d.path):
            dirs[:] = [x for x in dirs if x not in (".git", "node_modules")]
            if "SKILL.md" in files:
                skills.append(root)
            if root.count(os.sep) - d.path.count(os.sep) > 6:
                dirs[:] = []
        if not skills:
            continue
        repos += 1
        inserted = 0
        for root in skills:
            try:
                text = open(os.path.join(root, "SKILL.md"), encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            bad = dangerous(text)
            if bad:
                blocked += 1
                continue
            if len(text) < 400:  # halaman arsip/stub, tidak berguna
                skipped += 1
                continue
            fm_name, fm_desc = read_fm(text)
            base = slugify(fm_name or os.path.basename(root) or d.name)
            if not base or len(base) < 3:
                continue
            name = base
            if name in existing:
                # sudah ada skill dengan nama sama & isi serupa -> tidak perlu duplikat
                old = s.execute("SELECT COALESCE(description,'') FROM skills WHERE name=? LIMIT 1",
                                (name,)).fetchone()
                if old and (old[0] or "")[:50].strip() == (fm_desc or "")[:50].strip():
                    skipped += 1
                    continue
                name = slugify(f"{d.name.split('_', 1)[-1]}-{base}")
            dest = os.path.join(STORE, name)
            if os.path.exists(dest):
                skipped += 1
                continue
            try:
                shutil.copytree(root, dest, ignore=shutil.ignore_patterns(".git", "node_modules"))
            except Exception:
                skipped += 1
                continue
            path = os.path.join(dest, "SKILL.md")
            s.execute("INSERT INTO skills(name,description,tier,category,path,source) VALUES(?,?,?,?,?,?)",
                      (name, (fm_desc or f"Skill dari repo {d.name}")[:200],
                       "curated", "repo-refs", path, f"repo-refs/{d.name}"))
            existing.add(name)
            inserted += 1
            added += 1
        if inserted:
            upsert(c, d.name.replace("_", "/", 1), has_skill=1, skill_count=inserted,
                   local_path=d.path, state="ingested")
        s.commit()
        print(f"  {d.name}: {inserted} skill", flush=True)
    c.commit()
    print(f"[ingest] {repos} repo berskill, {added} skill baru, {skipped} dilewati, {blocked} diblokir")
    stats(args)


def dedupe(args):
    """Buang skill hasil ingest yang isinya duplikat skill yang sudah ada."""
    c = connect()
    s = sqlite3.connect(SKILL_DB, timeout=30)
    allrows = s.execute("SELECT name, COALESCE(description,''), path FROM skills").fetchall()
    byname = {}
    for n, d, p in allrows:
        byname.setdefault(n, (d, p))
    rows = s.execute("SELECT name, COALESCE(description,''), path FROM skills "
                     "WHERE source LIKE 'repo-refs/%'").fetchall()
    store_prefix = os.path.join(STORE, "")
    removed = 0
    for n, d, p in rows:
        parts = n.split("-")
        cands = {"-".join(parts[i:]) for i in range(1, len(parts))}
        for base in cands:
            if base not in byname:
                continue
            bd = byname[base][0]
            if d[:50].strip() and d[:50].strip() == (bd or "")[:50].strip():
                s.execute("DELETE FROM skills WHERE name=? AND path=?", (n, p))
                if p.startswith(store_prefix):
                    try:
                        shutil.rmtree(os.path.dirname(p))
                    except Exception:
                        pass
                removed += 1
                break
    s.commit()
    print(f"[dedupe] {removed} skill duplikat dibuang")


def search(args):
    n = int(args[args.index("-n") + 1]) if "-n" in args else 10
    rest = list(args)
    if "-n" in rest:
        i = rest.index("-n")
        rest = rest[:i] + rest[i + 2:]
    q = " ".join(rest).strip()
    c = connect()
    try:
        rows = c.execute(
            "SELECT r.slug, r.stars, r.state, r.has_skill, substr(r.desc,1,80) "
            "FROM repos r WHERE r.slug IN (SELECT slug FROM repos_fts WHERE repos_fts MATCH ?) "
            "ORDER BY r.stars DESC LIMIT ?", (q, n)).fetchall()
    except Exception:
        rows = c.execute("SELECT slug,stars,state,has_skill,substr(desc,1,80) FROM repos "
                         "WHERE slug LIKE ? OR desc LIKE ? ORDER BY stars DESC LIMIT ?",
                         (f"%{q}%", f"%{q}%", n)).fetchall()
    if not rows:
        print("tidak ada repo cocok")
        return
    for slug, stars, state, hs, desc in rows:
        print(f"- {slug} ⭐{stars} [{state}{'/skill' if hs else ''}] {desc}")


def get(args):
    slug = args[0].lower()
    owner, name = slug.split("/", 1)
    dest = os.path.join(REFS, f"{owner}_{name}")
    if os.path.exists(os.path.join(dest, ".cloned")):
        print(dest)
        return
    if os.path.isdir(dest):
        # ada dir lama tapi bukan clone (stub metadata) -> simpan, jangan dibuang
        backup = dest + ".stub"
        if not os.path.exists(backup):
            os.rename(dest, backup)
            print(f"(stub lama dipindah ke {backup})")
        else:
            dest = dest + "__clone"
    p = subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{slug}.git", dest],
                       capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"gagal clone {slug}: {p.stderr[:200]}")
    # hemat disk: buang .git (history), repo-refs hanya untuk baca/referensi
    try:
        shutil.rmtree(os.path.join(dest, ".git"))
    except Exception:
        pass
    try:
        open(os.path.join(dest, ".cloned"), "w").write(slug + "\n")
    except Exception:
        pass
    c = connect()
    upsert(c, slug, local_path=dest, state="cloned")
    c.commit()
    print(dest)
    if "--ingest" in args:
        ingest([])


def stats(args=None):
    c = connect()
    total = c.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
    by_state = c.execute("SELECT state, COUNT(*) FROM repos GROUP BY state ORDER BY 2 DESC").fetchall()
    by_origin = c.execute("SELECT origin, COUNT(*) FROM repos GROUP BY origin ORDER BY 2 DESC LIMIT 8").fetchall()
    print(f"[stats] total repo: {total}  (target 100000)")
    print("  state: " + ", ".join(f"{k}={v}" for k, v in by_state))
    print("  asal : " + ", ".join(f"{k}={v}" for k, v in by_origin))


def catalog(args):
    c = connect()
    out = [os.path.join(AG, "repo-catalog.md")]
    with open(out[0], "w", encoding="utf-8") as f:
        f.write("# Katalog repo (~/.agents/repo-refs)\n\n")
        f.write("Dibuat oleh `~/.agents/repo-hub.py catalog`. Cari: `python3 ~/.agents/repo-hub.py search \"kata\"`\n\n")
        f.write("## Statistik\n\n```\n")
        total = c.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
        f.write(f"total repo terdaftar: {total}\n")
        for st, n in c.execute("SELECT state,COUNT(*) FROM repos GROUP BY state").fetchall():
            f.write(f"{st}: {n}\n")
        f.write("```\n\n## Repo lokal yang benar-benar ada kodenya (siap dijalankan)\n\n")
        man = ("package.json", "pyproject.toml", "requirements.txt", "Cargo.toml",
               "go.mod", "Makefile", "composer.json", "Gemfile")
        for slug, lp in c.execute("SELECT slug, local_path FROM repos WHERE local_path<>'' AND state IN ('cloned','ingested')"):
            if not lp or not os.path.isdir(lp):
                continue
            if not os.path.isdir(os.path.join(lp, ".git")) and not os.path.exists(os.path.join(lp, ".cloned")):
                continue
            ents = set(os.listdir(lp))
            if ents & set(man):
                f.write(f"- `{slug}` — {lp}\n")
        f.write("\n## Repo dengan skill ter-ingest (siap dipakai `sk`)\n\n")
        for slug, n, desc in c.execute(
                "SELECT slug, skill_count, substr(desc,1,90) FROM repos WHERE has_skill=1 ORDER BY skill_count DESC"):
            f.write(f"- `{slug}` — {n} skill — {desc}\n")
        f.write("\n## 100 repo paling populer\n\n")
        for slug, st, desc in c.execute(
                "SELECT slug, stars, substr(desc,1,90) FROM repos ORDER BY stars DESC LIMIT 100"):
            f.write(f"- `{slug}` ⭐{st} — {desc}\n")
    print(out[0])


CMDS = {"stats": stats, "harvest": harvest, "expand": expand, "expand-fast": expand_fast, "ingest": ingest, "dedupe": dedupe, "scan": scan, "top": top, "trending": trending, "hits": hits, "install-agents": install_agents,
        "search": search, "get": get, "catalog": catalog}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
