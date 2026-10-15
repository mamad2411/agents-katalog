#!/usr/bin/env python3
"""build-retrieve-index.py — satukan SEMUA aset jadi satu indeks pencarian.

Sumber:
  skills-index.db  -> skill (name, description, category)
  cap-catalog.json -> prompt/agent/rule/hook/memory/... (ribuan tipe)
  mcp-catalog.json -> MCP (name, description)

Output: ~/.agents/retrieve.db  (FTS5 tabel `assets`, BM25 siap pakai)
Dipakai oleh `retrieve.py` dan tool MCP `retrieve` (mcp-router.py).
Tanpa unduh model — murni FTS5/BM25.
"""
import json, os, sqlite3
from pathlib import Path

AG = Path.home() / ".agents"
SKILLS_DB = AG / "skills-index.db"
CAP = AG / "cap-catalog.json"
MCP = AG / "mcp-catalog.json"
OUT = AG / "retrieve.db"


def rows():
    if SKILLS_DB.exists():
        try:
            c = sqlite3.connect(SKILLS_DB)
            for name, desc, cat, path, src in c.execute(
                    "select name,description,category,path,source from skills"):
                body = " ".join(x for x in [desc or "", cat or ""] if x)
                yield (name or "", body, "skill", src or "", path or "",
                       "skill--" + (name or ""), 0)
            c.close()
        except Exception as e:
            print("skills err:", str(e)[:80])

    if CAP.exists():
        for e in json.loads(CAP.read_text()):
            yield (e.get("name") or "", (e.get("type") or "") + " " + (e.get("path") or ""),
                   e.get("type") or "", e.get("repo") or "", e.get("path") or "",
                   e.get("id") or "", e.get("stars") or 0)

    if MCP.exists():
        for m in json.loads(MCP.read_text()):
            yield (m.get("name") or "", m.get("description") or "", "mcp",
                   m.get("repo") or "", m.get("url") or "", "mcp--" + (m.get("name") or ""), 0)


def main():
    if OUT.exists():
        OUT.unlink()
    conn = sqlite3.connect(OUT)
    conn.execute("CREATE VIRTUAL TABLE assets USING fts5("
                 "name, body, kind, source, path, id, stars UNINDEXED)")
    n = 0
    batch = []
    for r in rows():
        batch.append(r)
        if len(batch) >= 5000:
            conn.executemany("INSERT INTO assets VALUES(?,?,?,?,?,?,?)", batch)
            n += len(batch); batch = []
    if batch:
        conn.executemany("INSERT INTO assets VALUES(?,?,?,?,?,?,?)", batch)
        n += len(batch)
    conn.commit()
    conn.execute("INSERT INTO assets(assets) VALUES('optimize')")
    conn.commit()
    conn.close()
    print("retrieve.db siap: %d aset (skill+cap+mcp)" % n)


if __name__ == "__main__":
    main()
