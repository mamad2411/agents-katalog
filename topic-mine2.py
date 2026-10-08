#!/usr/bin/env python3
"""topic-mine2.py — worker-2 paralel: fetch repo dari BELAKANG (LIFO) biar
tidak rebutan dengan worker-1 (FIFO dari depan). State file SAMA
(.topic-mine-state.json) tapi worker ini hanya ambil repo yg belum done
dan tulis balik dengan merge (baca ulang state sebelum save).

Notasi dir: topic2-* (bedakan dari topic-* worker-1, hindari tabrakan nama).
Pakai: GH_TOKEN=... nice -n 15 python3 ~/.agents/topic-mine2.py
"""
import json, os, re, sqlite3, subprocess, sys, time

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
STATE = os.path.join(AG, ".topic-mine-state.json")
TOKEN = os.environ.get("GH_TOKEN", "")
FM = re.compile(r"^name:\s*[\"']?([\w-]+)", re.M)


def gh(url, timeout=20):
    cmd = ["curl", "-s", "--max-time", str(timeout),
           "-H", "Accept: application/vnd.github+json",
           "-H", "User-Agent: topic-mine2/1.0"]
    if TOKEN:
        cmd += ["-H", f"Authorization: Bearer {TOKEN}"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    if not r.stdout.strip():
        raise RuntimeError("empty")
    return json.loads(r.stdout)


def load_state():
    return json.load(open(STATE))


def save_merge(mydone, mynew, myexists, mymiss):
    # baca ulang (worker-1 mungkin nulis duluan), merge, tulis
    for _ in range(5):
        try:
            st = json.load(open(STATE))
            break
        except Exception:
            time.sleep(2)
    else:
        return
    done = set(st.get("done", [])) | mydone
    st["done"] = sorted(done)
    st["new"] = st.get("new", 0) + mynew
    st["exists"] = st.get("exists", 0) + myexists
    st["miss"] = st.get("miss", 0) + mymiss
    # repos juga merge (kalau worker-1 nambah enum baru)
    known = set(st.get("repos", []))
    for r in load_state_cached_repos():
        if r not in known:
            known.add(r)
            st["repos"].append(r)
    tmp = STATE + ".tmp2"
    json.dump(st, open(tmp, "w"), indent=1)
    try:
        os.replace(tmp, STATE)
    except Exception:
        pass


_repos_cache = None


def load_state_cached_repos():
    global _repos_cache
    if _repos_cache is None:
        try:
            _repos_cache = list(json.load(open(STATE)).get("repos", []))
        except Exception:
            _repos_cache = []
    return _repos_cache


def main():
    if not TOKEN:
        print("ERROR: GH_TOKEN wajib", file=sys.stderr)
        return 1
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    existing = {r[0] for r in conn.execute("SELECT name FROM skills")}
    conn.close()
    st = load_state()
    # LIFO: dari belakang, skip yg sudah done
    done = set(st["done"])
    todo = [r for r in reversed(st["repos"]) if r not in done]
    print(f"worker-2: {len(todo)} repo (LIFO dari belakang)", flush=True)
    mydone, mynew, myexists, mymiss = set(), 0, 0, 0
    for i, full in enumerate(todo, 1):
        # cek ulang: worker-1 mungkin sudah kerjakan repo ini
        try:
            cur = set(json.load(open(STATE)).get("done", []))
        except Exception:
            cur = set()
        if full in cur or full in mydone:
            continue
        try:
            t = gh(f"https://api.github.com/repos/{full}/git/trees/HEAD?recursive=1",
                   timeout=15)
            paths = [x["path"] for x in t.get("tree", [])
                     if x.get("path", "").endswith("SKILL.md")][:40]
        except Exception:
            paths = []
        hit = False
        for p in paths:
            r = subprocess.run(
                ["curl", "-s", "-f", "--max-time", "12",
                 f"https://raw.githubusercontent.com/{full}/HEAD/{p}"],
                capture_output=True, timeout=18)
            if r.returncode == 0 and r.stdout:
                m = FM.search(r.stdout.decode("utf-8", "ignore"))
                name = re.sub(r"-{2, }", "-",
                              (m.group(1) if m else full.split("/")[1]).lower()).strip("-")
                name = re.sub(r"-{2,}", "-", name)
                if name in existing:
                    myexists += 1
                else:
                    sub = p.lower().split("/")[-2] if "/" in p else "root"
                    dd = os.path.join(DEST, "topic2-" + full.replace("/", "-") + "-" +
                                      re.sub(r"[^a-z0-9-]+", "-", sub)[:30])
                    if not os.path.exists(os.path.join(dd, "SKILL.md")):
                        os.makedirs(dd, exist_ok=True)
                        open(os.path.join(dd, "SKILL.md"), "wb").write(r.stdout)
                        existing.add(name); mynew += 1
                    else:
                        myexists += 1
                hit = True
        if not hit:
            mymiss += 1
        mydone.add(full)
        if i % 10 == 0:
            save_merge(mydone, mynew, myexists, mymiss)
            mydone, mynew, myexists, mymiss = set(), 0, 0, 0
            print(f"  w2 [{i}/{len(todo)}] merged", flush=True)
        time.sleep(1.5)  # jeda lebih longgar (2 worker paralel)
    save_merge(mydone, mynew, myexists, mymiss)
    print("worker-2 SELESAI", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
