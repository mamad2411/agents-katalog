#!/usr/bin/env python3
"""mine-agent-assets.py — tambang aset aturan/prompt lintas tool.

Yang diambil (semua format instruksi agent yang dipakai tool AI):
  AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md,
  .cursor/rules/*.mdc, *.prompt.md

Cara: unduh tarball (cap 60 MB), baca HANYA file yang cocok lewat
tarfile.extractfile, SCAN isi sebelum ditulis, dedup nama + md5.
Output: ~/.agents/agent-assets/mined-<owner>-<repo>/<tipe>/<nama>.md
"""
import argparse, hashlib, io, json, os, re, subprocess, sys, tarfile, tempfile
import time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "agent-assets")
REG_F = os.path.join(AG, "asset-registry.json")
MANIFEST = os.path.join(AG, "asset-manifest.jsonl")
LOG_F = os.path.join(AG, "mine-assets.log")
MAX_TARBALL = 400 * 1024 * 1024
MAX_FILE = 128 * 1024

QUERIES = [
    ("agents", "filename:AGENTS.md"),
    ("claude", "filename:CLAUDE.md"),
    ("gemini", "filename:GEMINI.md"),
    ("copilot", "filename:copilot-instructions.md"),
    ("cursor", "path:.cursor/rules extension:mdc"),
    ("prompt", "filename:prompt.md"),
    ("instructions", "filename:instructions.md"),
    ("rules", "filename:.cursorrules"),
    ("rules", "filename:.windsurfrules"),
    ("rules", "filename:.clinerules"),
    ("command", "path:.claude/commands"),
    ("agent", "path:.claude/agents"),
    ("rules", "path:.clinerules"),
    ("rules", "path:.windsurf/rules"),
    ("rules", "path:.roo/rules"),
    ("rules", "path:.continue/rules"),
    ("rules", "path:.amazonq/rules"),
    ("instructions", "path:.github/instructions"),
    ("prompt", "path:.github/prompts"),
]

SCAN_PAT = [
    ("reverse-shell", re.compile(r"(bash\s+-i\s*>&?\s*/dev/tcp/|/dev/tcp/(?!127\.0\.0\.1|localhost)|nc\s+-e\s|mkfifo\s+\S+.*nc\s)")),
    ("downloader-exec", re.compile(r"(curl[^\n|]*\|\s*(ba)?sh|wget[^\n|]*\|\s*(ba)?sh|iwr[^\n|]*\|\s*iex|DownloadString|-EncodedCommand)", re.I)),
    ("base64-exec", re.compile(r"(eval\s*\(\s*(atob|base64)|base64\s+-d\s*\|\s*(ba)?sh)", re.I)),
    ("obfuscation", re.compile(r"[A-Za-z0-9+/]{2000,}={0,2}")),
    ("credential-exfil", re.compile(r"(\.aws/credentials|id_rsa\b|\.netrc|security\s+find-generic-password)", re.I)),
    ("exfil-endpoint", re.compile(r"(webhook\.site|discord\.com/api/webhooks|pastebin\.com/raw|transfer\.sh|0x0\.st|ngrok\.io)", re.I)),
    ("persistence", re.compile(r"(crontab\s+-|/Library/LaunchAgents|/Library/LaunchDaemons|systemctl\s+enable|schtasks\s+/create)", re.I)),
    ("stealer-dropper", re.compile("(" + "L2Jpbi9iYXNo" + "IC1jIC" + r"|91\.92\.242\.30|54\.91\.154\.110|6x8c0trkp4l9uugo)", re.I)),
    ("prompt-injection", re.compile(r"(ignore (all )?(previous|prior|above) instructions|disregard (your|all) (rules|instructions)|new system prompt|jailbreak)", re.I)),
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


def load(p, d):
    try:
        return json.load(open(p))
    except Exception:
        return d


def save(p, o):
    tmp = p + ".tmp"
    json.dump(o, open(tmp, "w"))
    os.replace(tmp, p)



DEFENSIVE = re.compile(r"(rotate|revoke|vault|secrets manager|never (share|commit|send|paste)|do not (share|commit|send|paste)|don'?t (share|commit|send|paste)|must not|should not|avoid (sending|committing|sharing)|encrypt|redact|detect|mitigat|warning|caution|insecure|vulnerab|best practice|protect)", re.I)


def scan_ctx(txt):
    """scan() + pengecualian: dokumen defensif yang menyebut kredensial tidak dibuang."""
    r = scan_text(txt) if "scan_text" in globals() else scan(txt)
    if r == "secret-exfil" and DEFENSIVE.search(txt):
        return None
    return r


def slug(s):
    return (re.sub(r"[^0-9A-Za-z]+", "-", s).strip("-").lower())[:60] or "x"


def canonical(s):
    return re.sub(r"[^0-9a-z]+", "", (s or "").lower())


def scan(txt):
    for name, rx in SCAN_PAT:
        if rx.search(txt):
            return name
    return None


def classify(path):
    """Satu file -> satu jenis aset, atau None."""
    base = os.path.basename(path)
    if base == "AGENTS.md":
        return "agents"
    if base == "CLAUDE.md":
        return "claude"
    if base == "GEMINI.md":
        return "gemini"
    if base == "copilot-instructions.md":
        return "copilot"
    if path.endswith(".mdc") and ".cursor/rules" in path:
        return "cursor"
    if base.endswith(".prompt.md") or base == "prompt.md":
        return "prompt"
    if base.endswith(".instructions.md"):
        return "instructions"
    if base in (".cursorrules", ".windsurfrules", ".clinerules"):
        return "rules"
    if any(x in path for x in ("/.clinerules/", "/.windsurf/rules/", "/.roo/rules/",
                               "/.continue/rules/", "/.amazonq/rules/")) and base.endswith(".md"):
        return "rules"
    if "/.github/instructions/" in path and base.endswith(".md"):
        return "instructions"
    if "/.github/prompts/" in path and base.endswith(".md"):
        return "prompt"
    if (".claude/commands/" in path or ".codex/prompts/" in path) and base.endswith(".md"):
        return "command"
    if (".claude/agents/" in path or ".github/agents/" in path) and base.endswith(".md"):
        return "agent"
    return None


def display_name(full, member_path, kind):
    repo = full.split("/")[-1]
    base = os.path.basename(member_path)
    if kind in ("agents", "claude", "gemini"):
        parent = os.path.basename(os.path.dirname(member_path))
        suffix = "" if parent in ("", ".", repo) else "-" + slug(parent)
        return "%s-%s%s" % (slug(repo), kind, suffix)
    if kind == "copilot":
        return "%s-copilot" % slug(repo)
    if kind == "rules":
        return "%s-%s" % (slug(repo), base.lstrip(".").replace(".", "-"))
    if kind in ("command", "agent"):
        return "%s-%s-%s" % (slug(repo), kind, slug(os.path.splitext(base)[0]))
    if kind == "instructions":
        return "%s-%s" % (slug(repo), slug(base.replace(".instructions.md", "")))
    stem = slug(os.path.splitext(base)[0])
    return stem if len(stem) >= 8 else "%s-%s" % (slug(repo), stem)


def _rm_tmp(path):
    try:
        os.unlink(path)
    except OSError:
        pass


def fetch(full, branch):
    """Unduh tarball ke FILE SEMENTARA (bukan RAM) supaya repo besar tetap aman di 8 GB."""
    url = "https://codeload.github.com/%s/tar.gz/refs/heads/%s" % (full, branch)
    req = urllib.request.Request(url, headers={"User-Agent": "agents-asset-miner/1.0"})
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


def mine(full, kind, known, md5s):
    repo_dir = os.path.join(DEST, "mined-%s" % slug(full.replace("/", "-")))
    if os.path.exists(os.path.join(repo_dir, ".done")):   # sudah discan semua jenis
        return 0, "already"
    for branch in ("main", "master"):
        try:
            path, err = fetch(full, branch)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            return 0, "http:%d" % e.code
        except Exception as e:
            return 0, "err:%s" % type(e).__name__
        if err:
            return 0, err
        break
    else:
        return 0, "no-branch"

    try:
        tf = tarfile.open(path, mode="r:gz")
    except Exception:
        return 0, "bad-tar"

    written, rows = 0, []
    with tf:
        for m in tf:
            if not m.isfile() or m.size > MAX_FILE or m.size < 200:
                continue
            k = classify(m.name)
            if not k:
                continue
            try:
                body = tf.extractfile(m).read().decode("utf-8", "ignore")
            except Exception:
                continue
            if scan_ctx(body):
                with open(os.path.join(AG, "asset-blocked-files.jsonl"), "a") as bf:
                    bf.write(json.dumps({"repo": full, "path": m.name,
                                         "reason": scan_ctx(body)}) + "\n")
                continue
            name = display_name(full, m.name, k)
            key = canonical(name)
            h = hashlib.md5(re.sub(r"\s+", " ", body).strip().lower().encode()).hexdigest()
            if key in known or h in md5s:
                continue
            out = os.path.join(repo_dir, k, name + ".md")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(body)
            known.add(key)
            md5s.add(h)
            rows.append({"path": out, "kind": k, "repo": full})
            written += 1
            if written >= 400:
                break
    if rows:
        with open(MANIFEST, "a") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    try:
        os.makedirs(repo_dir, exist_ok=True)
        open(os.path.join(repo_dir, ".done"), "w").write("1")
    except Exception:
        pass
    _rm_tmp(path)
    return written, None


def load_known():
    import sqlite3
    names = set()
    try:
        c = sqlite3.connect(os.path.join(AG, "skills-index.db"))
        for (n,) in c.execute("SELECT name FROM skills"):
            names.add(canonical(n))
        c.close()
    except Exception:
        pass
    return names, set()


KNOWN, MD5S = set(), set()


def _work(item):
    full, kind = item
    w, bad = mine(full, kind, KNOWN, MD5S)
    return full, w, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-repos", type=int, default=8000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--discover-only", action="store_true")
    ap.add_argument("--mine-only", action="store_true")
    a = ap.parse_args()

    reg = load(REG_F, {"repos": {}})
    repos = reg["repos"]
    if a.mine_only:
        log("=== MINE-ONLY: %d repo aset ===" % len(repos))
        _skip_discover = True
    else:
        _skip_discover = False
    for kind, q in ([] if _skip_discover else QUERIES):
        for page in range(1, a.pages + 1):
            out = ""
            for _ in range(2):
                out = gh(["api", "search/code?q=%s&per_page=100&page=%d"
                          % (urllib.parse.quote(q), page), "--jq", '.items[].repository.full_name'])
                if out.strip():
                    break
                time.sleep(65)
            rows = [x for x in out.splitlines() if x.count("/") == 1]
            for full in rows:
                k = full.lower()
                if k in repos:
                    repos[k]["hits"] = repos[k].get("hits", 0) + 1
                else:
                    repos[k] = {"full_name": full, "kind": kind, "hits": 1}
            log("discover %s p%d: %d repo (total %d)" % (kind, page, len(rows), len(repos)))
            save(REG_F, {"repos": repos})
            if len(rows) < 100:
                break
            time.sleep(6.5)
        time.sleep(6.5)

    if a.discover_only:
        return
    cands = sorted(repos.values(), key=lambda r: -r.get("hits", 0))
    known, md5s = load_known()
    log("mining %d repo aset (known %d)" % (min(len(cands), a.max_repos), len(known)))
    total = done = 0
    t0 = time.time()
    global KNOWN, MD5S
    KNOWN, MD5S = known, md5s
    jobs = [(r["full_name"], r.get("kind", "agents")) for r in cands[:a.max_repos]]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(processes=a.workers) as pool:
        for full, w, bad in pool.imap_unordered(_work, jobs, chunksize=1):
            total += w
            done += 1
            if done % 20 == 0:
                log("progress %d | +%d aset | %.0fs" % (done, total, time.time() - t0))
    log("=== SELESAI: +%d aset dari %d repo ===" % (total, done))


if __name__ == "__main__":
    main()
