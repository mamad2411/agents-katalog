#!/usr/bin/env python3
"""skill-promote.py — naikkan skill arsip (skills-expanded) jadi curated (skills-store).

Gerbang kualitas (semua harus lulus):
  1. frontmatter punya name == slug folder & description >= 40 char
  2. body >= 20 baris efektif
  3. ada minimal 1 blok kode (```) ATAU bagian langkah/checklist
  4. nama belum ada di skills-store
  5. ukuran folder <= 2 MB

Pakai:
  python3 skill-promote.py --limit 50            # dry-run: lihat kandidat + skor
  python3 skill-promote.py --limit 50 --apply    # salin ke skills-store
  python3 skill-promote.py --status
Exit: 0 ok, 1 argumen salah.
"""
import json
import os
import re
import shutil
import sqlite3
import sys
import time

AG = os.path.expanduser("~/.agents")
SRC = f"{AG}/skills-expanded"
DST = f"{AG}/skills-store"
LOG = f"{AG}/.promoted.json"
DB = f"{AG}/skills-index.db"
MAX_SIZE = 2 * 1024 * 1024


def parse_fm(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    fm, body = text[3:end], text[end + 4:]
    data = {}
    key = None
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", lines[i])
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in ("|", ">", "|-", ">-", "|+", ">+"):
                buf = []
                i += 1
                while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                    buf.append(lines[i].strip())
                    i += 1
                data[key] = " ".join(x for x in buf if x).strip()
                continue
            data[key] = val.strip('"').strip("'")
        i += 1
    return data, body


def dir_size(p):
    total = 0
    for root, _, files in os.walk(p):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
            if total > MAX_SIZE:
                return total
    return total


def score(p):
    """0..100, atau (0, alasan) bila gugur."""
    d = os.path.dirname(p)
    slug = os.path.basename(d)
    try:
        text = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return 0, "tidak terbaca"
    fm, body = parse_fm(text)
    if fm is None:
        return 0, "tanpa frontmatter"
    name = (fm.get("name") or "").strip()
    desc = (fm.get("description") or "").strip()
    if not name:
        return 0, "nama kosong"
    if not desc or len(desc) < 40:
        return 0, "deskripsi pendek"
    lines = [l for l in body.splitlines() if l.strip()]
    if len(lines) < 20:
        return 0, "body tipis"
    has_code = "```" in body
    has_steps = bool(re.search(r"(?im)^\s*(#{1,4}\s*)?(langkah|steps?|checklist|usage|cara pakai)", body))
    if not (has_code or has_steps):
        return 0, "tanpa contoh/langkah"
    if dir_size(d) > MAX_SIZE:
        return 0, "folder >2MB"
    s = 40
    s += min(20, len(desc) // 20)
    s += min(15, len(lines) // 20)
    s += 10 if has_code else 0
    s += 5 if has_steps else 0
    s += 5 if os.path.isdir(os.path.join(d, "scripts")) else 0
    return min(100, s), "ok"


def existing_names():
    try:
        c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        names = {r[0] for r in c.execute("SELECT name FROM skills")}
        c.close()
        return names
    except Exception:
        return set(os.listdir(DST))


def candidates(limit, min_score):
    names = existing_names()
    out, rejected = [], {}
    for root, dirs, files in os.walk(SRC):
        if "SKILL.md" not in files:
            continue
        p = os.path.join(root, "SKILL.md")
        sc, why = score(p)
        if sc == 0:
            rejected[why] = rejected.get(why, 0) + 1
            continue
        slug = os.path.basename(root)
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
            fm, _ = parse_fm(text)
            fname = re.sub(r"[^a-z0-9]+", "-", (fm.get("name") or "").lower()).strip("-")
        except Exception:
            fname = ""
        if fname and len(fname) >= 3:
            slug = fname
        if slug in names:
            rejected["nama sudah ada"] = rejected.get("nama sudah ada", 0) + 1
            continue
        if sc < min_score:
            rejected["skor rendah"] = rejected.get("skor rendah", 0) + 1
            continue
        out.append((sc, p, slug))
        if limit and len(out) >= limit * 3:
            break
    out.sort(key=lambda x: -x[0])
    return (out[:limit] if limit else out), rejected


def promote(items):
    done = []
    log = []
    if os.path.exists(LOG):
        try:
            log = json.load(open(LOG))
        except Exception:
            log = []
    for sc, p, slug in items:
        src_dir = os.path.dirname(p)
        dst_dir = os.path.join(DST, slug)
        if os.path.exists(dst_dir):
            continue
        try:
            shutil.copytree(src_dir, dst_dir)
        except Exception as e:
            print(f"  gagal {slug}: {e}", file=sys.stderr)
            continue
        done.append({"slug": slug, "score": sc, "from": src_dir,
                     "at": time.strftime("%FT%T")})
        log.append(done[-1])
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    json.dump(log, open(LOG, "w"), indent=1)
    return done


def main():
    apply_ = "--apply" in sys.argv
    limit = 50
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    min_score = 60
    if "--min-score" in sys.argv:
        min_score = int(sys.argv[sys.argv.index("--min-score") + 1])

    if "--status" in sys.argv:
        n = len(json.load(open(LOG))) if os.path.exists(LOG) else 0
        print(f"sudah dipromosikan: {n}")
        return 0

    items, rejected = candidates(limit, min_score)
    print(f"kandidat lolos gerbang: {len(items)} (limit {limit}, min skor {min_score})")
    for why, c in sorted(rejected.items(), key=lambda x: -x[1])[:6]:
        print(f"  gugur · {why}: {c}")
    for sc, p, slug in items[:10]:
        print(f"  {sc:3d}  {slug}")
    if not apply_:
        print("\n(dry-run — tambahkan --apply untuk menyalin)")
        return 0
    done = promote(items)
    print(f"\ndipromosikan: {len(done)}")
    if done:
        print("jalankan: python3 build_skills_index.py && python3 skills-index-md.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
