#!/usr/bin/env python3
"""mine-domains.py — tambang SKILL.md per DOMAIN (security, database, network, ...).

Pakai:
  python3 mine-domains.py --domains security,database,network --max-repos 400
  python3 mine-domains.py --discover-only          # cuma isi registry
  python3 mine-domains.py --report                 # hitung hasil

Alur per repo (1 request, bukan ratusan):
  1. unduh tarball branch main/master (cap 60 MB) -> TIDAK diekstrak ke disk
  2. baca hanya member yang berakhiran SKILL.md (<=128 KB), lewat tarfile.extractfile
  3. SCAN isi SEBELUM ditulis (dropper, reverse-shell, exfil, prompt-injection,
     hidden-unicode). Ada hit -> repo dibuang, dicatat di domain-blocklist.json
  4. dedup md5 + nama kanonik, tulis ke skills-expanded/mined-<owner>-<repo>/<slug>/
  5. catat {path, domain, repo} ke domain-manifest.jsonl

Tidak ada git clone, tidak ada eksekusi, tidak ada file non-markdown yang ditulis.
"""
import argparse, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile
import time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "skills-expanded")
REG_F = os.path.join(AG, "domain-registry.json")
BLOCK_F = os.path.join(AG, "domain-blocklist.json")
MANIFEST = os.path.join(AG, "domain-manifest.jsonl")
LOG_F = os.path.join(AG, "mine-domains.log")

MAX_TARBALL = 400 * 1024 * 1024
MAX_SKILL = 128 * 1024
MAX_PER_REPO = int(os.environ.get("DOMAIN_MAX_PER_REPO", "500"))

DOMAINS = {
    "security": ["security", "cybersecurity", "appsec", "pentest", "threat-modeling",
                 "sast", "secrets-management", "supply-chain-security", "malware-analysis",
                 "osint", "incident-response", "cryptography", "zero-trust", "cloud-security"],
    "database": ["database", "sql", "postgresql", "mysql", "sqlite", "mongodb", "redis",
                 "clickhouse", "vector-database", "data-modeling", "database-migrations",
                 "query-optimization", "elasticsearch", "duckdb", "orm"],
    "network": ["networking", "tcp-ip", "dns", "tls", "firewall", "packet-analysis",
                "bgp", "vpn", "proxy", "load-balancing", "grpc", "websocket",
                "http2", "network-security", "wireshark"],
    "devops": ["devops", "kubernetes", "terraform", "docker", "ci-cd", "observability",
               "sre", "helm", "ansible", "platform-engineering", "gitops", "prometheus"],
    "ai-agent": ["ai-agents", "agent-skills", "claude-skills", "mcp", "tool-use",
                 "multi-agent", "agent-orchestration", "context-engineering", "llm-agents"],
    "rag": ["rag", "retrieval-augmented-generation", "embeddings", "vector-search",
            "knowledge-graph", "reranking", "semantic-search", "llm-eval"],
    "mlops": ["mlops", "fine-tuning", "lora", "quantization", "model-serving",
              "inference", "llmops", "training", "evaluation", "huggingface"],
    "data": ["data-engineering", "etl", "data-pipeline", "analytics", "spark", "dbt",
             "airflow", "data-warehouse", "streaming", "kafka"],
    "general": ["skills", "agent", "prompt", "workflow", "automation", "template",
                "awesome", "productivity", "writing", "design", "marketing",
                "finance", "education", "research", "content"],
}

SCAN_PAT = [
    ("reverse-shell", re.compile(r"(bash\s+-i\s*>&?\s*/dev/tcp/|/dev/tcp/(?!127\.0\.0\.1|localhost)|nc\s+-e\s|ncat\s+-e\s|mkfifo\s+\S+.*nc\s)")),
    ("downloader-exec", re.compile(r"(curl[^\n|]*\|\s*(ba)?sh|wget[^\n|]*\|\s*(ba)?sh|iwr[^\n|]*\|\s*iex|Invoke-WebRequest[^\n]*\|\s*IEX|DownloadString|FromBase64String|-EncodedCommand)", re.I)),
    ("base64-exec", re.compile(r"(eval\s*\(\s*(atob|base64)|base64\s+-d\s*\|\s*(ba)?sh)", re.I)),
    ("obfuscation", re.compile(r"[A-Za-z0-9+/]{2000,}={0,2}")),
    ("credential-exfil", re.compile(r"(\.aws/credentials|id_rsa\b|\.netrc|security\s+find-generic-password)", re.I)),
    ("crypto-miner", re.compile(r"(xmrig|minerd|cpuminer|stratum\+tcp)", re.I)),
    ("exfil-endpoint", re.compile(r"(webhook\.site|discord\.com/api/webhooks|pastebin\.com/raw|transfer\.sh|0x0\.st|ngrok\.io)", re.I)),
    ("persistence", re.compile(r"(crontab\s+-|/Library/LaunchAgents|/Library/LaunchDaemons|systemctl\s+enable|schtasks\s+/create)", re.I)),
    ("data-destroy", re.compile(r"(rm\s+-rf\s+/\s|dd\s+if=/dev/(zero|urandom)\s+of=/dev/)")),
    ("stealer-dropper", re.compile("(" + "L2Jpbi9iYXNo" + "IC1jIC" + r"|91\.92\.242\.30|54\.91\.154\.110|6x8c0trkp4l9uugo|swcdn\.apple\.com[^\n]{0,80}\|\s*base64)", re.I)),
    ("prompt-injection", re.compile(r"(ignore (all )?(previous|prior|above) instructions|disregard (your|all) (rules|instructions)|new system prompt|jailbreak)", re.I)),
    ("secret-exfil", re.compile(r"(send|upload|post|exfiltrate|leak)[^\n]{0,40}(api[ _-]?key|token|password|secret|credential|\.env|ssh)", re.I)),
    ("hidden-unicode", re.compile(r"[\u200b\u200c\u200d\u2060\ufeff\u202a-\u202e]")),
]


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG_F, "a") as f:
        f.write(line + "\n")


def gh(args):
    try:
        r = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=90)
        return r.stdout
    except Exception:
        return ""


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def save(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


def scan_text(txt):
    for name, rx in SCAN_PAT:
        if rx.search(txt):
            return name
    return None



DEFENSIVE = re.compile(r"(rotate|revoke|vault|secrets manager|never (share|commit|send|paste)|do not (share|commit|send|paste)|don'?t (share|commit|send|paste)|must not|should not|avoid (sending|committing|sharing)|encrypt|redact|detect|mitigat|warning|caution|insecure|vulnerab|best practice|protect)", re.I)


def scan_ctx(txt):
    """scan() + pengecualian: dokumen defensif yang menyebut kredensial tidak dibuang."""
    r = scan_text(txt) if "scan_text" in globals() else scan(txt)
    if r == "secret-exfil" and DEFENSIVE.search(txt):
        return None
    return r


def slug(s):
    s = re.sub(r"[^0-9A-Za-z]+", "-", s).strip("-").lower()
    return s[:60] or "skill"


def canonical(name):
    return re.sub(r"[^0-9a-z]+", "", name.lower())


def fetch_tree_paths(full, branch):
    """Daftar path SKILL.md dalam repo (1 API call)."""
    out = gh(["api", "repos/%s/git/trees/%s?recursive=1" % (full, branch),
              "--jq", '.tree[] | select(.type=="blob") | .path'])
    return [p for p in out.splitlines() if p.endswith("SKILL.md")]


def _rm_tmp(path):
    try:
        os.unlink(path)
    except OSError:
        pass


def fetch_tarball(full, branch):
    """Unduh tarball ke FILE SEMENTARA (bukan RAM) supaya repo besar tetap aman di 8 GB."""
    url = "https://codeload.github.com/%s/tar.gz/refs/heads/%s" % (full, branch)
    req = urllib.request.Request(url, headers={"User-Agent": "agents-miner/1.0"})
    fd, path = tempfile.mkstemp(suffix=".tgz", prefix="mine-")
    n = 0
    try:
        with os.fdopen(fd, "wb") as f, urllib.request.urlopen(req, timeout=120) as r:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                n += len(chunk)
                if n > MAX_TARBALL:
                    raise IOError("too-big")
                f.write(chunk)
    except Exception:
        try:
            os.unlink(path)
        except OSError:
            pass
        raise
    return path, None


def mine_repo(full, domain, known_names, known_md5):
    """Return (written, skipped, blocked_reason)."""
    repo_dir = os.path.join(DEST, "mined-%s" % slug(full.replace("/", "-")))
    if os.path.isdir(repo_dir):                       # sudah pernah ditambang
        return 0, 0, "already"
    for branch in ("main", "master"):
        try:
            path, err = fetch_tarball(full, branch)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            return 0, 0, "http:%d" % e.code
        except Exception as e:
            return 0, 0, "err:%s" % type(e).__name__
        if err:
            return 0, 0, err
        break
    else:
        return 0, 0, "no-branch"

    written = skipped = 0
    try:
        tf = tarfile.open(path, mode="r:gz")
    except Exception:
        return 0, 0, "bad-tar"

    manifest = []
    with tf:
        for m in tf:
            if written >= MAX_PER_REPO:
                break
            if not m.isfile() or not m.name.endswith("SKILL.md"):
                continue
            if m.size > MAX_SKILL:
                skipped += 1
                continue
            try:
                body = tf.extractfile(m).read().decode("utf-8", "ignore")
            except Exception:
                continue
            bad = scan_ctx(body)
            if bad:
                # buang FILE-nya saja; repo security sah sering memuat contoh serangan
                with open(os.path.join(AG, "domain-blocked-files.jsonl"), "a") as bf:
                    bf.write(json.dumps({"repo": full, "path": m.name, "reason": bad,
                                         "domain": domain}) + "\n")
                skipped += 1
                continue
            h = hashlib.md5(re.sub(r"\s+", " ", body).strip().lower().encode()).hexdigest()
            if h in known_md5:
                skipped += 1
                continue
            parent = os.path.dirname(m.name)
            name = os.path.basename(parent) if parent else "root"
            key = canonical(name)
            if key in known_names:
                skipped += 1
                continue
            out_dir = os.path.join(repo_dir, slug(name))
            if os.path.exists(out_dir):                 # nama sama dalam satu repo
                out_dir += "-" + h[:6]
            os.makedirs(out_dir, exist_ok=True)
            p = os.path.join(out_dir, "SKILL.md")
            with open(p, "w", encoding="utf-8") as f:
                f.write(body)
            known_names.add(key)
            known_md5.add(h)
            manifest.append({"path": p, "domain": domain, "repo": full})
            written += 1

    if manifest:
        with open(MANIFEST, "a") as f:
            for row in manifest:
                f.write(json.dumps(row) + "\n")
    _rm_tmp(path)
    return written, skipped, None


def discover(domains, per_topic=60):
    """Cari repo yang BENAR punya SKILL.md di topik tertentu lewat GitHub code search.

    gh search code (CLI) tidak mengembalikan hasil di mesin ini; API search/code
    mengembalikan 1,1 jt hit untuk `filename:SKILL.md security`. Batas API:
    10 request/menit + maksimal 1000 hasil per query -> jeda 6,5 dtk antar query.
    DOMAIN_DEEP=1 menambah varian path (skills / .claude / plugins) -> 4x lipat repo.
    """
    reg = load(REG_F, {"repos": {}})
    repos = reg["repos"]
    added = 0
    pages = max(1, min(3, (per_topic + 99) // 100))
    paths = ["", "path:skills", "path:.claude", "path:plugins"] \
        if os.environ.get("DOMAIN_DEEP") == "1" else [""]
    for dom in domains:
        for term in DOMAINS[dom][:6]:                  # 6 istilah terkuat per domain
            for pth in paths:
                for page in range(1, pages + 1):
                    qs = 'filename:SKILL.md "%s"%s' % (term, (" " + pth) if pth else "")
                    q = urllib.parse.quote(qs)
                    out = ""
                    for attempt in range(2):           # 403 = kuota search habis
                        out = gh(["api", "search/code?q=%s&per_page=100&page=%d" % (q, page),
                                  "--jq", '.items[].repository.full_name'])
                        if out.strip():
                            break
                        time.sleep(65)
                    rows = [x for x in out.splitlines() if x.count("/") == 1]
                    for full in rows:
                        key = full.lower()
                        if key in repos:
                            repos[key]["hits"] = repos[key].get("hits", 0) + 1
                            continue
                        repos[key] = {"full_name": full, "stars": 0,
                                      "desc": "", "domain": dom, "hits": 1}
                        added += 1
                    log("discover %s/%s%s p%d: %d repo (total %d)"
                        % (dom, term, (" " + pth) if pth else "", page, len(rows), len(repos)))
                    save(REG_F, {"repos": repos})      # simpan bertahap: tahan kill
                    if len(rows) < 100:
                        break
                    time.sleep(6.5)                    # kuota code search 10/menit
                time.sleep(6.5)
    save(REG_F, {"repos": repos})
    return added, len(repos)


def load_known():
    names, md5s = set(), set()
    db = os.path.join(AG, "skills-index.db")
    try:
        import sqlite3
        c = sqlite3.connect(db)
        for (n,) in c.execute("SELECT name FROM skills"):
            names.add(canonical(n or ""))
        c.close()
    except Exception:
        pass
    if os.path.exists(MANIFEST):
        for line in open(MANIFEST):
            try:
                row = json.loads(line)
                names.add(canonical(os.path.basename(os.path.dirname(row["path"]))))
            except Exception:
                pass
    return names, md5s


KNOWN_NAMES, KNOWN_MD5 = set(), set()


def _work(item):
    """Worker proses: fork mewarisi KNOWN_NAMES/KNOWN_MD5 (copy-on-write)."""
    full, domain = item
    w, sk, bad = mine_repo(full, domain, KNOWN_NAMES, KNOWN_MD5)
    return full, domain, w, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains", default="security,database,network")
    ap.add_argument("--max-repos", type=int, default=200)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--per-topic", type=int, default=300)
    ap.add_argument("--discover-only", action="store_true")
    ap.add_argument("--mine-only", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    if a.report:
        n = 0
        by = {}
        if os.path.exists(MANIFEST):
            for line in open(MANIFEST):
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                n += 1
                by[r["domain"]] = by.get(r["domain"], 0) + 1
        print("skill domain tertambang:", n)
        for k, v in sorted(by.items(), key=lambda x: -x[1]):
            print("  %-12s %d" % (k, v))
        return

    domains = [d.strip() for d in a.domains.split(",") if d.strip() in DOMAINS]
    if not domains:
        print("domain tidak dikenal. pilih:", ", ".join(DOMAINS))
        return

    if a.mine_only:
        reg = load(REG_F, {"repos": {}})
        log("=== MINE-ONLY: %d repo di registry ===" % len(reg["repos"]))
        added, total = 0, len(reg["repos"])
    else:
        log("=== DISCOVER domains=%s ===" % ",".join(domains))
        added, total = discover(domains, a.per_topic)
    log("registry: +%d repo baru (total %d)" % (added, total))
    if a.discover_only:
        return

    reg = load(REG_F, {"repos": {}})
    cands = [r for r in reg["repos"].values() if r.get("domain") in domains]
    cands.sort(key=lambda r: (-r.get("hits", 0), -r.get("stars", 0)))
    known_names, known_md5 = load_known()
    log("mining %d repo (known names %d)" % (min(len(cands), a.max_repos), len(known_names)))

    written = blocked = done = 0
    blocklist = load(BLOCK_F, {})
    t0 = time.time()
    global KNOWN_NAMES, KNOWN_MD5
    KNOWN_NAMES, KNOWN_MD5 = known_names, known_md5
    jobs = [(r["full_name"], r["domain"]) for r in cands[:a.max_repos]]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(processes=a.workers) as pool:
        for full, dom, w, bad in pool.imap_unordered(_work, jobs, chunksize=1):
            done += 1
            written += w
            if bad and bad.startswith("BLOCKED"):
                blocked += 1
                blocklist[full] = {"reason": bad, "domain": dom,
                                   "ts": time.strftime("%Y-%m-%d")}
                log("BLOCKED %s (%s)" % (full, bad))
            if done % 10 == 0:
                el = time.time() - t0
                log("progress %d/%d repo | +%d skill | blocked=%d | %.0fs | %.1f skill/s"
                    % (done, min(len(cands), a.max_repos), written, blocked, el,
                       written / max(el, 1)))
                save(BLOCK_F, blocklist)
    save(BLOCK_F, blocklist)
    log("=== SELESAI: +%d skill dari %d repo, blocked=%d ===" % (written, done, blocked))


if __name__ == "__main__":
    main()
