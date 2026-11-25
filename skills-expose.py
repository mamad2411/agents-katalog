#!/usr/bin/env python3
"""skills-expose — daftarkan skill pilihan ke opencode native (~/.opencode/skills) via symlink.

Kenapa dibatasi: opencode menyuntik nama+deskripsi setiap skill terdaftar ke prompt.
304k skill = prompt meledak. Jadi: kurasi ±60 skill, sisanya tetap 0 token lewat `sk`.

Pakai:
  python3 skills-expose.py --list              # lihat yang sudah terekspos
  python3 skills-expose.py --top 60            # ekspos 60 skill terbaik (idempotent)
  python3 skills-expose.py --add nama1,nama2   # ekspos manual
  python3 skills-expose.py --remove nama        # cabut
  python3 skills-expose.py --cost              # estimasi token daftar skill
"""
import json
import os
import sqlite3
import sys

HOME = os.path.expanduser("~")
DB = os.path.join(HOME, ".agents", "skills-index.db")
READY = os.path.join(HOME, ".agents", "skills-readiness.json")
TARGET = os.path.join(HOME, ".opencode", "skills")

# domain yang paling sering dipakai di mesin ini
PRIORITY = [
    "security", "cloudflare", "deploy", "docker", "kubernetes", "git", "github",
    "test", "review", "refactor", "debug", "performance", "sql", "database",
    "api", "frontend", "react", "vue", "next", "design", "accessibility",
    "docs", "research", "ocr", "pdf", "excel", "slides", "video", "image",
    "whatsapp", "telegram", "email", "scrape", "crawl", "mcp", "agent", "prompt",
]


CORE = [
    # deploy & infra
    "all-deploy", "cloudflare-deploy", "self-hosted-docker-stack",
    # kualitas kode
    "verification-loop", "systematic-debugging", "writing-tests", "refactor",
    "code-security", "code-review", "audit-project",
    # dokumen & data
    "pdf", "xlsx", "baca-gambar", "deep-research",
    # UI
    "anti-ui-slop", "frontend-design",
    # meta
    "skill-creator", "mcp-builder", "web-scraping-python", "skill-router",
]
MANIFEST = os.path.join(HOME, ".agents", ".skills-exposed-manifest.json")


def ready_map():
    try:
        return json.load(open(READY))
    except Exception:
        return {}


def candidates(min_chars=1500):
    c = sqlite3.connect(DB, timeout=30)
    rows = c.execute("SELECT name, COALESCE(description,''), path FROM skills").fetchall()
    out = []
    for name, desc, path in rows:
        if not path or not os.path.exists(path):
            continue
        if "/skills-store/" not in path and "/skills-expanded/" not in path:
            continue
        try:
            size = os.path.getsize(path)
        except Exception:
            continue
        if size < min_chars:
            continue
        low = (name + " " + desc).lower()
        score = sum(10 for kw in PRIORITY if kw in low)
        score += min(size // 2000, 8)
        if "skills-store" in path:
            score += 6
        out.append((score, name, desc, path, size))
    out.sort(key=lambda x: (-x[0], x[1]))
    return out


def exposed():
    if not os.path.isdir(TARGET):
        return []
    return sorted(d for d in os.listdir(TARGET)
                  if os.path.isdir(os.path.join(TARGET, d)) and not d.startswith("."))


def add_links(picked):
    os.makedirs(TARGET, exist_ok=True)
    have = set(exposed())
    added = 0
    for name, path in picked:
        if name in have:
            continue
        src = os.path.dirname(path)
        dst = os.path.join(TARGET, name)
        try:
            os.symlink(src, dst)
            added += 1
        except FileExistsError:
            pass
    return added


def main():
    a = sys.argv[1:]
    rm = ready_map()
    if "--list" in a:
        for d in exposed():
            print("-", d)
        return
    if "--cost" in a:
        c = sqlite3.connect(DB, timeout=30)
        tot = 0
        for d in exposed():
            r = c.execute("SELECT COALESCE(description,'') FROM skills WHERE name=? LIMIT 1",
                          (d,)).fetchone()
            tot += len((r[0] if r else "") + d)
        print(f"{len(exposed())} skill terekspos · ±{tot // 4} token di prompt per request")
        return
    if "--remove" in a:
        name = a[a.index("--remove") + 1]
        p = os.path.join(TARGET, name)
        if os.path.islink(p):
            os.unlink(p)
            print(f"dicabut: {name}")
        else:
            print("tidak ada symlink:", name)
        return
    if "--add" in a:
        names = [x.strip() for x in a[a.index("--add") + 1].split(",") if x.strip()]
        c = sqlite3.connect(DB, timeout=30)
        picked = []
        for n in names:
            r = c.execute("SELECT name, path FROM skills WHERE name=? LIMIT 1", (n,)).fetchone()
            if r:
                picked.append(r)
            else:
                print("tidak ada:", n)
        print("ditambah:", add_links(picked))
        return
    if "--curate" in a:
        # simpan manifest dulu supaya bisa dipulihkan
        with open(MANIFEST, "w") as f:
            json.dump({"before": exposed()}, f)
        cur = set(exposed())
        keep = set()
        for n in CORE:
            p_dir = os.path.join(TARGET, n)
            if os.path.isdir(p_dir):
                keep.add(n)
            else:
                print("  (tidak ada, dilewati):", n)
        removed = 0
        for n in cur - keep:
            p_dir = os.path.join(TARGET, n)
            if os.path.islink(p_dir):
                os.unlink(p_dir)
                removed += 1
        c = sqlite3.connect(DB, timeout=30)
        tot = 0
        for n in sorted(keep):
            r = c.execute("SELECT COALESCE(description,'') FROM skills WHERE name=? LIMIT 1", (n,)).fetchone()
            tot += len((r[0] if r else "") or "") + len(n)
        print(f"[curate] dicabut={removed} · tersisa={len(keep)} · ±{tot // 4} token (sebelumnya {len(cur)})")
        print(f"manifest: {MANIFEST}  (pulihkan: --restore)")
        return
    if "--restore" in a:
        try:
            before = json.load(open(MANIFEST)).get("before", [])
        except Exception:
            print("manifest tidak ada"); return
        c = sqlite3.connect(DB, timeout=30)
        picked = []
        for n in before:
            r = c.execute("SELECT name, path FROM skills WHERE name=? LIMIT 1", (n,)).fetchone()
            if r:
                picked.append(r)
        print("dipulihkan:", add_links(picked))
        return
    top = int(a[a.index("--top") + 1]) if "--top" in a else 60
    pool = [x for x in candidates() if rm.get(x[1], {}).get("ready", True)]
    picked = [(n, p) for _, n, _, p, _ in pool[:top]]
    added = add_links(picked)
    print(f"[expose] {added} symlink baru -> {TARGET} (total {len(exposed())})")
    print("Catatan: skill baru terlihat opencode setelah server reload/restart.")


if __name__ == "__main__":
    main()
