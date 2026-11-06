#!/usr/bin/env python3
"""skillq — cari skill di katalog lokal, output padat (0 tool MCP).
Pakai: skillq.py "kata kunci" [-n 5]   |   skillq.py -l <nama>   (cetak SKILL.md)
"""
import sqlite3, sys, os, re

DB = os.path.expanduser("~/.agents/skills-index.db")
STOP = set("yang dan dengan untuk dari pada ini itu saya mau bikin buat tolong bisa gimana cara agar supaya the and for with using use add create make new how please want need into that this from a an of to in on".split())

# Istilah Indonesia -> istilah yang benar-benar dipakai di deskripsi skill (Inggris).
# Tanpa ini, "desain dashboard profesional" jatuh ke skill Spanyol hasil auto-forge.
SYN = {
    "desain": "design", "mendesain": "design", "tampilan": "ui interface", "antarmuka": "ui interface",
    "dasbor": "dashboard", "halaman": "page landing", "layar": "screen page", "tombol": "button",
    "warna": "color palette", "huruf": "typography font", "tipografi": "typography", "tata": "layout grid",
    "letak": "layout grid", "animasi": "animation motion", "gerak": "motion animation",
    "aksesibel": "accessibility", "aksesibilitas": "accessibility", "responsif": "responsive",
    "formulir": "form", "kartu": "card", "tabel": "table", "ikon": "icon", "komponen": "component",
    "profesional": "polished professional", "bagus": "better polished", "jelek": "generic ai slop",
    "generik": "generic ai slop", "pasaran": "generic ai slop", "gelap": "dark theme",
    "terang": "light theme", "konsisten": "design system consistency", "rapi": "polished clean",
    "murah": "cheap", "modern": "modern contemporary", "landing": "landing page",
}
# Kata yang menandakan tugas desain -> naikkan skill kategori designer + curated.
DESIGN_HINT = {
    "design", "ui", "ux", "dashboard", "landing", "component", "layout", "grid", "typography",
    "color", "palette", "animation", "motion", "accessibility", "responsive", "theme", "polished",
    "generic", "slop", "page", "screen", "button", "card", "form", "icon", "table", "dark", "light",
}


def terms(q):
    out = []
    for t in re.findall(r"[\w./+-]+", q.lower()):
        if t in STOP or len(t) <= 1:
            continue
        out.extend(SYN.get(t, t).split())
    # buang duplikat, jaga urutan
    seen, uniq = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq or [q.lower()]

def main():
    a = sys.argv[1:]
    if not a:
        sys.exit('pakai: skillq.py "kata" [-n 5] | skillq.py -l <nama>')
    if a[0] == "--design":
        # Koleksi desain terkurasi — supaya skill UI/UX selalu muncul paling depan.
        import json
        cur = os.path.expanduser("~/.agents/design-skills.json")
        names = json.load(open(cur))["core"]
        if len(a) > 2 and a[1] in ("-l", "--load"):
            a = a[1:]  # lanjut ke mode load di bawah
        else:
            if "-n" in a:
                names = names[: int(a[a.index("-n") + 1])]
            c = sqlite3.connect(DB)
            for name in names:
                r = c.execute(
                    "SELECT COALESCE(category,''), COALESCE(description,''), path FROM skills WHERE name=? LIMIT 1",
                    (name,)).fetchone()
                if not r:
                    continue
                cat, desc, path = r
                print(f"- {name} [{cat or '-'}] {(desc or '')[:60]} — {path.replace(os.path.expanduser('~'), '~')}")
            return
    if a[0] in ("-l", "--load"):
        name = a[1]
        c = sqlite3.connect(DB)
        r = c.execute("SELECT path FROM skills WHERE name=? LIMIT 1", (name,)).fetchone()
        if not r:
            r = c.execute("SELECT path FROM skills WHERE name LIKE ? LIMIT 1", (f"%{name}%",)).fetchone()
        if not r:
            sys.exit(f"tidak ada skill '{name}'")
        with open(r[0], encoding="utf-8", errors="ignore") as f:
            print("".join(f.readlines()[:90]))
        return
    n = 5
    if "-n" in a:
        i = a.index("-n"); n = int(a[i+1]); a = a[:i] + a[i+2:]
    q = " ".join(a)
    c = sqlite3.connect(DB)
    rows = []
    q_terms = terms(q)
    design_task = any(t in DESIGN_HINT for t in q_terms)
    # Kolom: name, description, tier, category, path, source.
    # Nama diberi bobot 8: kalau query menyebut "logo", skill yang NAMANYA logo
    # harus menang atas skill yang cuma menyebut logo di deskripsi. Tanpa bobot,
    # bm25 memilih deskripsi terpendek — bukan yang paling relevan.
    order = "bm25(skills, 8.0, 1.0, 0.0, 0.0, 0.0, 0.0) + (CASE WHEN tier = 'curated' THEN 0.0 ELSE 0.8 END)"
    # Nama yang PERSIS atau berawalan salah satu kata query naik ke atas:
    # "bikin logo" → logo-studio, bukan frame-logo-outro yang cuma memuat
    # kata "logo" di tengah nama.
    order += " + (CASE WHEN name = :q THEN -100.0 ELSE 0 END)"
    params = {"q": q.strip().lower(), "n": n}
    for i, t in enumerate(q_terms):
        params[f"t{i}"] = t
        order += f" + (CASE WHEN name LIKE :t{i} || '-%' THEN -25.0 ELSE 0 END)"
    if design_task:
        # Tugas UI/UX: skill designer naik, sisanya tidak dihapus.
        order += " + (CASE WHEN category = 'designer' THEN -1.5 ELSE 0 END)"
    # Buang artefak auto-forge (isi kosong/duplikat) yang dulu membanjiri hasil,
    # dan tier 'junk' yang memang tidak masuk hitungan "siap dipakai".
    junk = (" AND tier <> 'junk'"
            " AND name NOT LIKE 'auto-%' AND name NOT LIKE 'revision-%'"
            " AND path NOT LIKE '%skill-forger%'")
    for joiner in (" AND ", " OR "):
        try:
            params["fts"] = joiner.join(q_terms)
            rows = c.execute(
                "SELECT name, COALESCE(category,''), COALESCE(description,''), path FROM skills "
                f"WHERE skills MATCH :fts{junk} ORDER BY {order} LIMIT :n", params).fetchall()
        except Exception:
            rows = []
        if rows:
            break
    if not rows:
        like = f"%{q}%"
        rows = c.execute(
            "SELECT name, COALESCE(category,''), COALESCE(description,''), path FROM skills "
            "WHERE name LIKE ? OR description LIKE ? LIMIT ?", (like, like, n)).fetchall()
    if not rows:
        print("tidak ada hasil")
        return
    for name, cat, desc, path in rows:
        d = (desc or "").replace("\n", " ").strip()[:60]
        short = path.replace(os.path.expanduser("~"), "~")
        print(f"- {name} [{cat or '-'}] {d} — {short}")

main()
