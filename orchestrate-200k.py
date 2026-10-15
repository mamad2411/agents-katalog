#!/usr/bin/env python3
"""Orchestrator: kejar katalog skill sampai TARGET (default 200.000).

Loop tiap gelombang:
  1. discover-repos.py        -> tambah repo baru ke registry (rotasi query)
  2. skill-miner.py --registry --tarballs (skip repo yang sudah ditambang)
  3. dedup-skills.py          -> buang duplikat
  4. build_skills_index.py    -> rebuild skills-index.db
  5. hitung total -> lanjut kalau belum capai target & masih ada progres

Jalan lama (jam-an). Jalankan di background, pantau lewat orchestrate-200k.log.
"""
import json, os, re, sqlite3, subprocess, sys, time

AG = os.path.expanduser("~/.agents")
DB = os.path.join(AG, "skills-index.db")
LOG = os.path.join(AG, "orchestrate-200k.log")
TARGET = int(os.environ.get("CATALOG_TARGET", "200000"))
MAX_WAVES = int(os.environ.get("MAX_WAVES", "60"))
WAVE_STATE = os.path.join(AG, ".orchestrate-wave")


def log(msg):
    line = "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


CHILD_LOG = os.path.join(AG, "orch-child.log")


def run(cmd, env=None, timeout=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    log("RUN: %s" % " ".join(cmd[:4]) + (" ..." if len(cmd) > 4 else ""))
    try:
        # stdout anak ditulis ke orch-child.log supaya progres bisa dipantau live
        with open(CHILD_LOG, "w") as f:
            p = subprocess.run(cmd, cwd=AG, env=e, stdout=f, stderr=subprocess.STDOUT,
                               text=True, timeout=timeout)
        try:
            tail = open(CHILD_LOG).read().strip().splitlines()[-3:]
        except Exception:
            tail = []
        for t in tail:
            log("  | " + t[:160])
        if p.returncode != 0:
            log("  ! exit %s" % p.returncode)
        return p.returncode == 0, ""
    except subprocess.TimeoutExpired:
        log("  ! TIMEOUT")
        return False, ""
    except Exception as ex:
        log("  ! ERR %s" % str(ex)[:150])
        return False, ""


def count_db():
    try:
        c = sqlite3.connect(DB)
        n = c.execute("select count(*) from skills").fetchone()[0]
        c.close()
        return n
    except Exception as ex:
        log("db err: %s" % str(ex)[:100])
        return -1


def count_files():
    n = 0
    base = os.path.join(AG, "skills-expanded")
    for root, ds, fs in os.walk(base):
        if "SKILL.md" in fs:
            n += 1
    return n


def registry_size():
    try:
        return len(json.load(open(os.path.join(AG, "repo-registry.json")))["repos"])
    except Exception:
        return -1


def running(name):
    """True kalau proses dengan nama ini sedang jalan (hindari dobel)."""
    try:
        out = subprocess.run(["pgrep", "-f", name], capture_output=True, text=True).stdout
        return bool(out.strip())
    except Exception:
        return False


def main():
    os.chdir(AG)
    token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    start_wave = 0
    try:
        start_wave = int(open(WAVE_STATE).read().strip())
    except Exception:
        pass

    log("=== ORCHESTRATE START target=%d wave=%d ===" % (TARGET, start_wave))
    prev = count_db()
    log("awal: index=%d files=%d registry=%d" % (prev, count_files(), registry_size()))
    stale = 0

    for i in range(start_wave, MAX_WAVES):
        log("---- GELOMBANG %d ----" % i)
        run(["python3", "discover-repos.py", "--wave", str(i)])
        reg_now = registry_size()

        run(["python3", "skill-miner.py", "--registry", "--tarballs"],
            env={"GH_TOKEN": token, "REG_MIN_STARS": "1", "REG_MAX_REPOS": "6000",
                 "REG_LIMIT_PER_REPO": "1500", "REG_SKIP_MINED": "1"})

        run(["python3", "dedup-skills.py"])
        run(["python3", "build_skills_index.py"])

        # refresh TAKSONOMI TIPE supaya ikut skill/MCP/plugin nyata (murah, lokal)
        run(["python3", "gen-types.py"])
        # refresh INDEKS RETRIEVAL (skill+cap+mcp) supaya pencarian selalu terbaru
        run(["python3", "build-retrieve-index.py"])
        # BERSIHKAN MALWARE: buang native executable dari repo mentah (exe/dll/jar/apk/ps1/dll)
        run(["python3", "skill-scan.py", "--t1", "--quarantine"])
        # refresh katalog aset komunitas tiap 3 gelombang (berat/network) — hanya jika belum ada
        if i % 3 == 0 and not running("cap-crawler.py"):
            run(["python3", "cap-crawler.py", "--no-trending"],
                env={"CAP_LIMIT": "60"})

        n = count_db()
        f = count_files()
        log("hasil gelombang %d: index=%d files=%d registry=%d" % (i, n, f, reg_now))
        open(WAVE_STATE, "w").write(str(i + 1))

        if n >= TARGET:
            log("=== TARGET TERCAPAI: %d >= %d ===" % (n, TARGET))
            break

        if n <= prev:
            stale += 1
            log("progres stagnan (%d/%d)" % (stale, 3))
            if stale >= 3:
                log("=== BERHENTI: 3 gelombang tanpa progres. Sumber registry habis. ===")
                break
        else:
            stale = 0
        prev = n
    else:
        log("=== BERHENTI: MAX_WAVES (%d) tercapai ===" % MAX_WAVES)

    log("FINAL: index=%d files=%d" % (count_db(), count_files()))


if __name__ == "__main__":
    main()
