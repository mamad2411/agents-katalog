#!/usr/bin/env python3
"""skill-miner.py — tambang SKILL.md dari repo komunitas -> skills-expanded/mined-*

- Sumber: daftar SOURCES (repo besar berisi banyak skill) + discovery dari awesome-lists
- Dedup: by nama (sudah ada di index -> skip) + by konten (md5) + nama dikanonikalisasi
- Skill tanpa deskripsi tetap diimpor tapi ditandai (tier nanti diputuskan index builder)
- Ringan: API GitHub cuma untuk trees (1 req/repo); isi file via raw.githubusercontent
"""
import json, os, re, hashlib, sqlite3, sys, tarfile, tempfile, shutil, time, urllib.request

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "skills-expanded")
RAW = "https://raw.githubusercontent.com/{repo}/{branch}/{path}"
API = "https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"

SOURCES = [
    ("obra/superpowers", "main"),
    ("anthropics/skills", "main"),
    ("github/awesome-copilot", "main"),
    ("VoltAgent/awesome-agent-skills", "main"),
    ("ComposioHQ/awesome-claude-skills", "main"),
]
AWESOME_DISCOVERY = {"VoltAgent/awesome-agent-skills", "ComposioHQ/awesome-claude-skills"}
LIMIT_PER_REPO = int(os.environ.get("MINER_LIMIT", "400"))
# --registry : tambang dari repo-registry.json (quality gate: bintang, jumlah repo dibatasi)
REG_MIN_STARS = int(os.environ.get("REG_MIN_STARS", "100"))
REG_MAX_REPOS = int(os.environ.get("REG_MAX_REPOS", "40"))
REG_LIMIT_PER_REPO = int(os.environ.get("REG_LIMIT_PER_REPO", "60"))


def registry_sources():
    f = os.path.join(AG, "repo-registry.json")
    out = []
    try:
        reg = json.load(open(f)).get("repos", {})
        cands = [(r["full_name"], r.get("stars", 0), r.get("desc", ""))
                 for r in reg.values() if r["full_name"].lower().count("/") == 1]
        cands.sort(key=lambda x: -x[1])
        for full, stars, desc in cands:
            if len(out) >= REG_MAX_REPOS:
                break
            if stars and stars < REG_MIN_STARS:
                continue
            if any(full.lower().endswith(s[0].lower()) for s in SOURCES):
                continue  # sudah di SOURCES default
            out.append((full, "main"))
        print("registry mode: %d kandidat (stars>=%d)" % (len(out), REG_MIN_STARS))
    except Exception as e:
        print("registry gagal dibaca:", e)
    return out

FM = re.compile(r"^---\n(.*?)\n---", re.S)
NAME = re.compile(r"^name:\s*['\"]?([\w\-./ ]+)", re.M)
DESC = re.compile(r"^description:\s*['\"]?(.{5,})", re.M)

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "skill-miner/1.0"})
    tok = os.environ.get("GH_TOKEN", "")
    if tok and "api.github.com" in url:
        req.add_header("Authorization", "Bearer " + tok)
    try:
        return urllib.request.urlopen(req, timeout=timeout).read()
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):  # rate limit: tunggu 60dtk, coba 1x lagi
            time.sleep(60)
            return urllib.request.urlopen(req, timeout=timeout).read()
        raise

def canonical(n):
    n = re.sub(r"[^a-z0-9\-]+", "-", n.strip().lower())
    n = re.sub(r"-{2,}", "-", n).strip("-")
    return re.sub(r"-skill$", "", n)[:60] or "unnamed"

def tree(repo, branch):
    d = json.loads(get(API.format(repo=repo, branch=branch)).decode())
    return [t["path"] for t in d.get("tree", []) if t["type"] == "blob" and t["path"].endswith("SKILL.md")]

def discover(repo, branch):
    """README awesome-list -> tambah repo ke repo-registry.json (bahan batch berikutnya)."""
    try:
        md = get(RAW.format(repo=repo, branch=branch, path="README.md")).decode("utf-8", "ignore")
    except Exception as e:
        print("  discovery gagal:", e); return 0
    urls = sorted(set(re.findall(r"github\.com/([\w\-.]+/[\w\-.]+)", md)))
    regf = os.path.join(AG, "repo-registry.json")
    reg = json.load(open(regf)) if os.path.exists(regf) else {"repos": {}}
    n0 = len(reg["repos"])
    for u in urls:
        k = u.lower()
        if k not in reg["repos"]:
            reg["repos"][k] = {"full_name": u, "stars": 0, "desc": "discovered-from:" + repo,
                               "tags": ["mined-ref"], "added": time.strftime("%Y-%m-%d")}
    json.dump(reg, open(regf, "w"), indent=2, ensure_ascii=False)
    print("  discovery: +%d repo ke registry" % (len(reg["repos"]) - n0))
    return len(reg["repos"]) - n0

def process(repo, p, body, branch, slug, conn, seen, stats):
    """Simpan 1 SKILL.md hasil tambang (dedup md5 + nama, tulis REPO-REF.md)."""
    h = hashlib.md5(body.encode()).hexdigest()
    if h in seen: stats["dup"] += 1; return
    seen.add(h)
    m = FM.search(body)
    name = (NAME.search(m.group(1)).group(1).strip() if m and NAME.search(m.group(1)) else "")
    if not name:
        parts = p.split("/"); name = parts[-2] if len(parts) >= 2 else parts[0]
    name = canonical(name)
    if conn.execute("SELECT 1 FROM skills WHERE name=? LIMIT 1", (name,)).fetchone():
        stats["exists"] += 1; return
    desc = ""
    if m and DESC.search(m.group(1)):
        desc = DESC.search(m.group(1)).group(1).strip()[:200]
    if not desc:
        hm = re.search(r"^#\s+(.+)$", body, re.M)
        desc = (hm.group(1) if hm else (body.strip().splitlines()[0] if body.strip() else ""))[:200]
    d = os.path.join(DEST, slug, name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "SKILL.md"), "w").write(body)
    open(os.path.join(d, "REPO-REF.md"), "w").write(
        "# Repo Ref\n- source: https://github.com/%s (path: %s, branch: %s)\n- mined: %s\n- desc: %s\n"
        % (repo, p, branch, time.strftime("%Y-%m-%d"), desc))
    stats["new"] += 1


def mine_tarball(sources, conn, seen, stats):
    """Mode --tarballs: 1 unduhan per repo via codeload.github.com.
    Tidak menyentuh kuota API dan tahan abuse-detection (beda endpoint)."""
    ok = fail = 0
    total = len(sources)
    for i, (repo, branch) in enumerate(sources, 1):
        slug = "mined-" + repo.replace("/", "-")
        tarfile_path = None
        for br in (branch, "main", "master"):
            url = "https://codeload.github.com/%s/tar.gz/refs/heads/%s" % (repo, br)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "skill-miner/1.0"})
                resp = urllib.request.urlopen(req, timeout=60)
                tmp = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)
                shutil.copyfileobj(resp, tmp, length=1 << 20)
                tmp.close(); resp.close()
                tarfile_path = tmp.name
                branch = br
                break
            except Exception:
                tarfile_path = None
                continue
        if not tarfile_path:
            print("%d/%d %s: tarball gagal" % (i, total, repo), flush=True)
            fail += 1; continue
        try:
            n0 = stats["new"]
            with tarfile.open(tarfile_path, "r:gz") as tf:
                for mem in tf:
                    if not mem.isfile() or not mem.name.endswith("SKILL.md"):
                        continue
                    p = mem.name.split("/", 1)[-1]  # buang prefix folder root tarball
                    f = tf.extractfile(mem)
                    if not f: continue
                    body = f.read().decode("utf-8", "ignore")
                    if len(body) > 200000: continue  # file raksasa = bukan skill
                    process(repo, p, body, branch, slug, conn, seen, stats)
            print("%d/%d %s: +%d new" % (i, total, repo, stats["new"] - n0), flush=True)
            ok += 1
        except Exception as e:
            print("%d/%d %s: extract err %s" % (i, total, repo, str(e)[:60]), flush=True)
            fail += 1
        finally:
            try: os.unlink(tarfile_path)
            except OSError: pass
        time.sleep(0.5)  # sopan santun antar repo
    print("tarball selesai: ok=%d fail=%d" % (ok, fail), flush=True)


def main():
    if "--registry" in sys.argv:
        sources = registry_sources()
        global LIMIT_PER_REPO
        LIMIT_PER_REPO = REG_LIMIT_PER_REPO
    else:
        sources = SOURCES
    stats = {"new": 0, "exists": 0, "dup": 0, "err": 0}
    conn = sqlite3.connect(os.path.join(AG, "skills-index.db"))
    seen = set()
    if "--tarballs" in sys.argv:
        mine_tarball(sources, conn, seen, stats)
        conn.close()
        print("STATS:", stats)
        return
    for repo, branch in sources:
        try:
            paths = tree(repo, branch)
        except Exception:
            try:
                paths = tree(repo, "master")
                branch = "master"
            except Exception as e:
                print("%s: skip (%s)" % (repo, str(e)[:60])); continue
        print("%s -> %d SKILL.md" % (repo, len(paths)))
        if repo in AWESOME_DISCOVERY:
            discover(repo, branch)  # list, bukan kumpulan skill
        slug = "mined-" + repo.replace("/", "-")
        for p in paths[:LIMIT_PER_REPO]:
            try:
                body = get(RAW.format(repo=repo, branch=branch, path=p)).decode("utf-8", "ignore")
            except Exception:
                stats["err"] += 1; continue
            process(repo, p, body, branch, slug, conn, seen, stats)
    conn.close()
    print("STATS:", stats)

if __name__ == "__main__":
    main()
