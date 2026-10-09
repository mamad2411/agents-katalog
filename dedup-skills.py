#!/usr/bin/env python3
"""dedup-skills.py — bersihkan duplikat katalog (isi sama / nama kanonik sama).
Aturan menang: skills-store (curated) > nama terpendek > alfabet.
Yang kalah DIPINDAH ke ~/.agents/.dupes/ (karantina, reversible) + log JSON.
Idempotent: bisa dijalanin 2x (yg udah di-dupes di-skip).
Pakai: nice -n 15 python3 ~/.agents/dedup-skills.py
"""
import hashlib, json, os, re, shutil, sys
from collections import defaultdict

AG = os.path.expanduser("~/.agents")
QUAR = os.path.join(AG, ".dupes")
LOG = os.path.join(AG, ".dupes-log.json")


def canonical_dirname(d):
    n = re.sub(r"[^a-z0-9-]+", "-", d.lower())
    n = re.sub(r"-{2,}", "-", n).strip("-")
    return re.sub(r"-skill$", "", n)


def frontmatter_name(text):
    m = re.search(r"^name:\s*[\"']?([\w-]+)", text, re.M)
    return (m.group(1).lower() if m else "")


def collect():
    out = []
    for base in ("skills-store", "skills-expanded"):
        root = os.path.join(AG, base)
        if not os.path.isdir(root):
            continue
        for d in sorted(os.listdir(root)):
            p0 = os.path.join(root, d)
            if not os.path.isdir(p0):
                continue
            p = os.path.join(p0, "SKILL.md")
            if os.path.isfile(p):
                out.append((base, d, p, p0))
                continue
            # nested (hasil tarball: mined-<repo>/<grup>/<nama>/SKILL.md)
            try:
                subs = sorted(os.listdir(p0))
            except OSError:
                continue
            for s in subs:
                p1 = os.path.join(p0, s)
                if not os.path.isdir(p1):
                    continue
                q = os.path.join(p1, "SKILL.md")
                if os.path.isfile(q):
                    out.append((base, f"{d}/{s}", q, p1))
    return out


def main():
    items = collect()
    print(f"scan: {len(items)} SKILL.md", flush=True)
    # PASS-1: isi identik (sha256)
    by_hash = defaultdict(list)
    for base, d, p, _ in items:
        try:
            with open(p, "rb") as f:
                by_hash[hashlib.sha256(f.read()).hexdigest()].append((base, d, p))
        except OSError:
            continue
    # PASS-2: nama kanonik sama (frontmatter > slug folder)
    by_name = defaultdict(list)
    for base, d, p, _ in items:
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                head = f.read(4096)
        except OSError:
            continue
        nm = frontmatter_name(head) or canonical_dirname(d.split("/")[-1])
        by_name[nm].append((base, d, p))

    def rank(t):
        base, d, p = t
        return (0 if base == "skills-store" else 1, len(d), d)

    drop = set()
    for groups in (by_hash.values(), by_name.values()):
        for g in groups:
            if len(g) < 2:
                continue
            g = sorted(g, key=rank)
            for loser in g[1:]:
                drop.add(loser)

    print(f"duplikat ketemu: {len(drop)} (hash+nama), pemenang selalu skills-store", flush=True)
    os.makedirs(QUAR, exist_ok=True)
    moved, skipped = 0, 0
    oldrecs = []
    try:
        oldrecs = json.load(open(LOG)).get("items", [])
    except Exception:
        pass
    recs = []

    def src_dir(base, d):
        return os.path.join(AG, base, *d.split("/"))

    def qname(base, d):
        return f"{base}__" + "__".join(d.split("/"))

    for base, d, p in sorted(drop):
        src = src_dir(base, d)
        dst = os.path.join(QUAR, qname(base, d))
        if os.path.exists(dst):
            skipped += 1
            continue
        try:
            shutil.move(src, dst)
            moved += 1
            recs.append({"from": f"{base}/{d}", "to": f".dupes/{qname(base, d)}"})
        except OSError as e:
            print(f"  ! gagal {base}/{d}: {e}", flush=True)
    allrecs = oldrecs + recs
    json.dump({"moved_total": len(allrecs), "pass_moved": moved,
               "skipped_exists": skipped, "items": allrecs},
              open(LOG, "w"), indent=1)
    print(f"KARANTINA: pindah={moved} skip={skipped} total={len(allrecs)} | log: {LOG}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
