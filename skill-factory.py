#!/usr/bin/env python3
"""skill-factory.py — bikin skill BARU dengan meniru struktur referensi terbaik.

Pemakaian:
  python3 skill-factory.py "<topik>" ["deskripsi singkat + kapan dipakai"]

Cara kerja (namanya referensi):
  1. Cari 3 skill curated paling relevan dengan topik (FTS index)
  2. Bedah struktur mereka: judul, section, pola frontmatter
  3. Tulis SKILL.md baru mengikuti struktur itu (frontmatter + When to Use +
     Workflow + Best Practices + Pitfalls + Referensi skill terkait)
  4. Setelahnya jalankan: python3 ~/.agents/build_skills_index.py
"""
import os, re, sqlite3, sys, time

AG = os.path.expanduser("~/.agents")

def refs_for(topic, n=3):
    conn = sqlite3.connect(os.path.join(AG, "skills-index.db"))
    toks = [t for t in re.findall(r"[a-z0-9]+", topic.lower()) if len(t) > 2][:6]
    q = " OR ".join(toks) if toks else topic
    rows = conn.execute("""SELECT name, path FROM skills
        WHERE skills MATCH ? AND tier='curated' ORDER BY bm25(skills) LIMIT ?""", (q, n)).fetchall()
    conn.close()
    return rows

def structure_of(path):
    try:
        t = open(path, encoding="utf-8", errors="ignore").read(8000)
    except Exception:
        return []
    secs = re.findall(r"^#{1,3}\s+(.+)$", t, re.M)
    return secs[:12]

def slugify(s):
    s = re.sub(r"[^a-z0-9\-]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)[:60] or "new-skill"

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    topic = sys.argv[1]
    desc = sys.argv[2] if len(sys.argv) > 2 else "Use when: %s. Ikuti workflow di bawah, jangan mengarang." % topic
    refs = refs_for(topic)
    print("Referensi struktur:")
    secs_seen = []
    for name, path in refs:
        secs = structure_of(path)
        secs_seen.append(secs)
        print("  - %s: %s" % (name, " > ".join(secs[:6])))
    # section paling umum dari referensi (top 8)
    from collections import Counter
    common = [s for s, _ in Counter([x for secs in secs_seen for x in secs]).most_common(8)]
    name = slugify(topic)
    d = os.path.join(AG, "skills", name)
    if os.path.exists(os.path.join(d, "SKILL.md")):
        print("EXIST: skill '%s' sudah ada -> %s" % (name, d)); return
    os.makedirs(d, exist_ok=True)
    body = f"""---
name: {name}
description: {desc}
---

# {topic.replace('-', ' ').title()}

## When to Use
- {desc}

"""
    for s in common or ["Workflow", "Best Practices", "Pitfalls"]:
        body += f"## {s}\n\n(Tulis langkah konkret di sini — lihat referensi di bawah untuk pola.)\n\n"
    body += "## Referensi\n"
    for rn, rp in refs:
        body += f"- `{rn}` — {rp}\n"
    body += "\n> Dibuat oleh skill-factory dari struktur referensi; perkuat isi sebelum dipakai produksi.\n"
    open(os.path.join(d, "SKILL.md"), "w").write(body)
    print("DIBUAT: %s (jalankan build_skills_index.py lalu skills-router.py)" % d)

if __name__ == "__main__":
    main()
