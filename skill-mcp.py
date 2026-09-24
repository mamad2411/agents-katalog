#!/usr/bin/env python3
"""skill-mcp.py — MCP server (stdio, stdlib only) untuk katalog skill ~/.agents.

Tools: skills_available, skill_search, skill_for_task, skill_load, agent_context.

Daftarkan:
  claude mcp add --scope user skill-catalog -- python3 ~/.agents/skill-mcp.py
"""
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

AG = Path.home() / ".agents"
DB = AG / "skills-index.db"
USAGE_F = AG / "mcp-usage.json"


EFF_F = AG / "skill-efficacy-log.json"


def _record_usage(tool_name="", extra=None):
    """Catat pemakaian tool — kumulatif, TIDAK direset harian.

    Format per tool: {count, first_used, last_used, days_active}.
    'days_active' = himpunan tanggal (dibatasi 90 hari terakhir) -> bahan GC
    lifecycle yang jujur (bedakan 'sering dipakai' vs 'sekali coba').
    'extra' = dict opsional, mis. {'skill': name} untuk skill_load ->
    juga dicatat ke efficacy log (fondasi ukur efektivitas nyata).
    """
    try:
        u = json.loads(USAGE_F.read_text()) if USAGE_F.exists() else {}
        today = time.strftime("%Y-%m-%d")
        now = time.time()
        e = u.get(tool_name, {"count": 0, "first_used": now, "last_used": 0,
                              "days_active": []})
        e["count"] += 1
        e.setdefault("first_used", now)
        e["last_used"] = now
        days = e.get("days_active", [])
        if today not in days:
            days.append(today)
        e["days_active"] = days[-90:]
        u[tool_name] = e
        tmp = USAGE_F.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(u, indent=2))
        tmp.replace(USAGE_F)
    except Exception:
        pass  # logging tidak boleh bikin tool gagal
    if extra and extra.get("skill"):
        _record_efficacy(extra["skill"], tool_name)


def _record_efficacy(skill_name, via=""):
    """Efficacy log nyata: skill apa yang di-LOAD (dipakai beneran, bukan
    sekadar direkomendasikan). Fondasi ukur 'skill efektif' vs 'sekadar tenar'."""
    try:
        log = json.loads(EFF_F.read_text()) if EFF_F.exists() else []
        if not isinstance(log, list):
            log = []
        log.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "skill": skill_name, "via": via})
        EFF_F.write_text(json.dumps(log[-2000:], indent=1))
    except Exception:
        pass
IDX = AG / "skills-index.json"
CODEX_CFG = Path.home() / ".codex" / "config.toml"
MAX_LOAD = 6000
TIERS = ("curated", "reference", "docs")


STOP = {
    "yang", "dan", "dengan", "untuk", "dari", "pada", "ini", "itu", "saya", "mau", "bikin",
    "buat", "tambah", "tambahkan", "tolong", "bisa", "gimana", "cara", "agar", "supaya",
    "the", "and", "for", "with", "using", "use", "add", "create", "make", "new", "how",
    "please", "want", "need", "into", "that", "this", "from", "your", "our", "my", "me",
    "us", "we", "they", "them", "their", "we", "you", "he", "she", "it", "his", "her", "its",
    "a", "an", "is", "are", "was", "were", "been", "being", "have", "has", "had", "do", "does",
    "did", "will", "would", "can", "could", "may", "might", "must", "shall", "should", "to",
    "of", "in", "on", "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "up", "down", "out", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "also", "",
}
KEEP_SHORT = {"db", "ci", "ui", "ux", "ai", "ml", "qa", "js", "ts", "k8s", "ws", "api",
              "pr", "io", "os", "vm", "kpi", "csv", "sql", "npm", "sdk",
              "dev", "ops", "cli", "srv", "svc", "pkg", "mod", "app", "lib"}
# CATATAN: "go" SENGAJA tidak ada di sini. Token 2 huruf "go" bikin false-positive
# ke "golang"/"gooserelay" (mis. "cara main pokemon go" → rekomendasi golang-patterns).
# Kata "golang" sendiri panjang (6) sehingga tetap ikut terindeks normal.


def tokens(q):
    raw = [re.sub(r"[^A-Za-z0-9._-]", "", t).lower() for t in re.split(r"\s+", (q or "").strip())]
    return [t for t in raw if t and t not in STOP and (len(t) > 2 or t in KEEP_SHORT)]


ID_EN = {
    "keamanan": ("security", "hardening", "vulnerability"),
    "uji": ("test", "testing"),
    "lambat": ("performance", "optimization"),
    "cepat": ("performance", "fast"),
    "penyimpanan": ("storage",),
    "berkas": ("file",),
    "jaringan": ("network",),
    "wadah": ("docker", "container"),
    "penjadwalan": ("scheduling", "cron"),
    "riset": ("research",),
    "mendalam": ("deep", "in-depth"),
    "kompetitor": ("competitor", "competitive"),
    "pesaing": ("competitor", "competitive"),
    "sumber": ("source", "citation"),
    "sitasi": ("citation", "source"),
    "laporan": ("report",),
    "dokumen": ("document", "docs"),
    "panduan": ("guide",),
    "pengujian": ("testing", "test"),
    "kinerja": ("performance",),
    "biaya": ("cost", "billing"),
    "kualitas": ("quality",),
    "struktur": ("structure", "architecture"),
    "alur": ("flow", "workflow"),
    "migrasi": ("migration", "migrate"),
    "pindah": ("migration", "migrate"),
    "ekstrak": ("extract", "extraction"),
    "teks": ("text",),
    "gambar": ("image", "picture"),
    "galat": ("error",),
    "kesalahan": ("error", "bug"),
    "perbaiki": ("fix", "repair"),
    "unggah": ("upload",),
    "unduh": ("download",),
    "pecahkan": ("split", "break"),
    "gabung": ("merge", "combine"),
    "halaman": ("page",),
    "jadwal": ("schedule",),
    "pantau": ("monitor",),
    "amankan": ("secure",),
}


def expand(toks):
    """Perluas token dengan sinonim ID→EN biar bahasa natural Indonesia tetap kena."""
    out = list(toks)
    for t in toks:
        for syn in ID_EN.get(t, ()):
            if syn not in out:
                out.append(syn)
    return out[:10]


def q_fts(q, mode="or"):
    toks = expand(tokens(q))[:10]
    if not toks:
        return ""
    parts = ['"%s"*' % t for t in toks]
    return (" OR ".join(parts)) if mode == "or" else " ".join(parts)


def _conn():
    return sqlite3.connect("file:%s?mode=ro" % DB, uri=True)


def search_like(q, limit=10):
    """Fallback bila FTS tidak kena (nama/deskripsi mengandung kata secara literal)."""
    toks = tokens(q)[:6]
    if not toks:
        return []
    where = " OR ".join(["lower(name) LIKE ? OR lower(description) LIKE ?"] * len(toks))
    args = []
    for t in toks:
        args += ["%" + t + "%", "%" + t + "%"]
    args.append(int(limit))
    sql = ("SELECT name, tier, COALESCE(category,''), COALESCE(description,'') FROM skills "
           "WHERE (%s) AND tier != 'docs' ORDER BY (tier='curated') DESC, name LIMIT ?" % where)
    conn = _conn()
    try:
        return conn.execute(sql, args).fetchall()
    finally:
        conn.close()


def search(q, tier=None, limit=10, mode="or"):
    m = q_fts(q, mode)
    if not m:
        return []
    # bm25() = skor relevansi FTS5 (makin kecil makin cocok). Tier curated dapat bonus.
    score = "bm25(skills) + (CASE WHEN tier = 'curated' THEN 0.0 ELSE 1.5 END)"
    where, args = "AND tier != 'docs'", [m]      # docs = bukan skill, jangan direkomendasikan
    if tier in TIERS:
        where, args = "AND tier = ?", [m, tier]
    args.append(int(limit))
    sql = ("SELECT name, tier, COALESCE(category,''), COALESCE(description,'') FROM skills "
           "WHERE skills MATCH ? %s ORDER BY %s, name LIMIT ?" % (where, score))
    conn = _conn()
    try:
        rows = conn.execute(sql, args).fetchall()
    finally:
        conn.close()
    if not rows and not tier:
        rows = search_like(q, limit)
    return rows


def skill_path(name):
    conn = _conn()
    try:
        row = conn.execute("SELECT path FROM skills WHERE name = ? LIMIT 1", (name,)).fetchone()
    finally:
        conn.close()
    return row[0] if row else ""


def fmt(rows):
    if not rows:
        return "(tidak ada hasil — coba kata kunci lain)"
    out = []
    for name, tier, cat, desc in rows:
        line = "- `%s` [%s%s]" % (name, tier, "/" + cat if cat else "")
        if desc:
            line += " — " + desc[:150]
        out.append(line)
    return "\n".join(out)


def load_catalog_json():
    try:
        return json.loads(IDX.read_text())
    except Exception:
        return {}


def dir_count(p):
    try:
        with os.scandir(p) as it:
            return sum(1 for _ in it)
    except Exception:
        return 0


def tool_skills_available(args):
    d = load_catalog_json()
    if not d:
        return "Katalog belum dibangun. Jalankan: python3 ~/.agents/skills-router.py"
    cats = d.get("summary", {})
    top = sorted(cats.items(), key=lambda kv: -kv[1]["tier1"])[:15]
    lines = [
        "**%d skill siap pakai** (curated %d dari %d entri index)."
        % (d.get("tier1_count", 0), d.get("total_curated", 0), d.get("total_index", 0)),
        "",
        "Katalog: ~/.agents/SKILLS-AVAILABLE.md · kategori: ~/.agents/SKILLS-CATEGORIES.md",
        "",
        "| Kategori | Tersedia | Total curated |", "|---|---|---|",
    ]
    for c, v in top:
        lines.append("| %s | %d | %d |" % (c, v["tier1"], v["curated"]))
    lines += ["", "Pakai `skill_for_task` (intent) atau `skill_search` (kata kunci) untuk memilih."]
    return "\n".join(lines)


def tool_skill_search(args):
    rows = search(args.get("query", ""), args.get("tier"), int(args.get("limit", 10) or 10))
    return "Hasil untuk `%s`:\n%s" % (args.get("query", ""), fmt(rows))


LANG_TOKENS = {"golang", "python", "java", "javascript", "typescript", "php", "ruby", "rust",
               "csharp", "dotnet", "dart", "kotlin", "swift", "scala", "elixir", "perl",
               "haskell", "lua", "matlab", "julia", "clojure", "erlang", "ocaml", "objc"}


def _score_row(toks, name, tier, desc):
    """Skor satu kandidat: cocok KATA UTUH + bonus nama.

    Bukti dari eval:
      1. Cocok harus kata utuh → 'nasi' tidak lagi nyasar ke 'nasiko-control-plane'.
      2. Awalan sebagian (test→testing, postgres→postgresql) dapat kredit 3.
      3. Token 'go' dibuang dari KEEP_SHORT (menghentikan false-positive golang).
      4. Teknologi yang BENTROK dihukum: task minta 'golang' tapi kandidat 'dart-*'
         → sinyal -15 (dulu 'dart-add-unit-test' menang atas 'golang-testing').
    """
    hay = (name + " " + (desc or "")).lower()
    word_hits = [t for t in toks
                 if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", hay)]
    parts = [p for p in name.lower().split("-") if p]
    exact = sum(1 for t in toks if t in parts)
    partial = sum(1 for t in toks
                  if t not in parts and any(len(p) > len(t) and p.startswith(t) for p in parts))
    # SINYAL = murni dari kecocokan (skala kecil & jujur). Bonus tier TIDAK masuk
    # ke sinyal — hanya dipakai sebagai pengurut (lihat rank_with_scores). Dengan
    # begitu "sok tahu" terukur: 1 kata generik saja ≈ 10 (di bawah ambang 11).
    sig = len(word_hits) * 5 + exact * 5 + partial * 3
    task_langs, name_langs = set(toks) & LANG_TOKENS, set(parts) & LANG_TOKENS
    if task_langs and name_langs:
        # Teknologi disebut di task: cocok → boost, bentrok → hukum.
        # (Dulu 'dart-add-unit-test' menang atas 'golang-testing' untuk task golang.)
        sig = max(0, sig + (15 if (task_langs & name_langs) else -15))
    return sig


def rank_with_scores(task, top=8, pool=60):
    """Kandidat + SINYAL — dipakai tool_skill_for_task DAN skill-eval.py (satu logika).

    Urutan akhir = sinyal + bonus tier (curated lebih diutamakan bila sinyal mirip),
    tapi yang dilaporkan sebagai skor adalah SINYAL-nya (jujur, tanpa tiupan tier).
    """
    rows = search(task, None, pool)
    toks = set(expand(tokens(task)))
    scored = []
    for name, tier, cat, desc in rows:
        sig = _score_row(toks, name, tier, desc)
        if sig > 0:
            order = sig + (7 if tier == "curated" else 0)
            scored.append((sig, order, name, tier, cat, desc))
    scored.sort(key=lambda r: (-r[1], -r[0], r[2]))
    return [(s, n, t, c, d) for s, _o, n, t, c, d in scored[:top]]


def rank_for_task(task, top=8, pool=60):
    """Rekomendasi final untuk AI: (nama, tier, kategori, deskripsi)."""
    return [(n, t, c, d) for _s, n, t, c, d in rank_with_scores(task, top, pool)]


def tool_skill_for_task(args):
    task = args.get("task", "")
    top = rank_for_task(task)
    head = ("Rekomendasi skill untuk: **%s**\n" % task) if top else \
           "Tidak ada skill yang cocok langsung untuk: **%s**\n" % task
    tail = ("\n\nKalau tidak ada yang cocok: cek MCP + repo ref (`agent_context`); "
            "kalau tetap tidak ada, buat skill baru (skill `skill-creator`).")
    return head + fmt(top) + tail


def tool_skill_load(args):
    name = args.get("name", "")
    p = skill_path(name)
    if not p or not os.path.exists(p):
        return "Skill `%s` tidak ditemukan." % name
    with open(p, encoding="utf-8", errors="ignore") as f:
        text = f.read(MAX_LOAD)
    more = "" if len(text) < MAX_LOAD else "\n\n[...dipotong; buka file: %s]" % p
    return "**%s** — %s\n\n%s%s" % (name, p, text, more)


def tool_agent_context(args):
    d = load_catalog_json()
    mcp = 0
    if CODEX_CFG.exists():
        mcp = len(set(re.findall(r"^\[mcp_servers\.([^.\]]+)", CODEX_CFG.read_text(errors="ignore"), re.M)))
    return "\n".join([
        "# Konteks agen — lihat dulu sebelum bertindak",
        "",
        "1. **Skill** — %d siap pakai (`skills_available` / `skill_search` / `skill_for_task`)."
        % d.get("tier1_count", 0),
        "2. **MCP** — %d server terdaftar (codex config); audit: `python3 ~/.agents/mcp-hygiene.py`." % mcp,
        "3. **Repo referensi** — %d repo di ~/.agents/repo-refs (dump README/AGENTS untuk pola)."
        % dir_count(AG / "repo-refs"),
        "4. **Aturan** — ~/.agents/AGENTS.md (sumber tunggal, larangan klon, MCP <=20).",
        "5. **Entry point repo kerja** — AGENTS.md proyek (mis. voralens-v2/AGENTS.md) + docs-nya.",
        "",
        "Alur: cari skill -> kalau ada, ikuti; kalau tidak, cek MCP/repo; baru tulis sendiri.",
    ])


TOOLS = [
    ("skills_available", "Ringkasan katalog skill: jumlah, kategori teratas, contoh.",
     {"type": "object", "properties": {}}),
    ("skill_search", "Cari skill berdasarkan kata kunci (FTS5).",
     {"type": "object", "properties": {
         "query": {"type": "string", "description": "kata kunci, mis. 'postgres index'"},
         "tier": {"type": "string", "enum": ["curated", "reference", "docs"], "description": "opsional"},
         "limit": {"type": "integer", "description": "maks hasil (default 10)"}},
      "required": ["query"]}),
    ("skill_for_task", "Rekomendasi skill untuk sebuah tugas/intent (pakai sebelum mulai kerja).",
     {"type": "object", "properties": {
         "task": {"type": "string", "description": "mis. 'tambah endpoint Go + test'"}},
      "required": ["task"]}),
    ("skill_load", "Ambil isi SKILL.md sebuah skill.",
     {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    ("agent_context", "Paket 'lihat dulu': skill + MCP + repo + aturan.",
     {"type": "object", "properties": {}}),
]
HANDLERS = {
    "skills_available": tool_skills_available,
    "skill_search": tool_skill_search,
    "skill_for_task": tool_skill_for_task,
    "skill_load": tool_skill_load,
    "agent_context": tool_agent_context,
}


def reply(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def handle(msg):
    mid = msg.get("id")
    method = msg.get("method", "")
    if method == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion") or ""
        reply({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": want if isinstance(want, str) and want else "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "skill-catalog", "version": "1.0.0"}}})
    elif method in ("notifications/initialized", "notifications/cancelled"):
        return
    elif method == "ping":
        reply({"jsonrpc": "2.0", "id": mid, "result": {}})
    elif method == "tools/list":
        reply({"jsonrpc": "2.0", "id": mid, "result": {"tools": [
            {"name": n, "description": d, "inputSchema": s} for n, d, s in TOOLS]}})
    elif method == "tools/call":
        p = msg.get("params") or {}
        fn = HANDLERS.get(p.get("name", ""))
        if not fn:
            reply({"jsonrpc": "2.0", "id": mid,
                   "error": {"code": -32602, "message": "tool tidak dikenal: %s" % p.get("name")}})
            return
        try:
            args = p.get("arguments") or {}
            result = fn(args)
            extra = {"skill": args.get("name")} if p.get("name") == "skill_load" and args.get("name") else None
            _record_usage(p.get("name", "tool"), extra)  # pemakaian kumulatif + efficacy log
            reply({"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": result}], "isError": False}})
        except Exception as e:
            reply({"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": "ERROR: %s" % e}], "isError": True}})
    elif mid is not None:
        reply({"jsonrpc": "2.0", "id": mid,
               "error": {"code": -32601, "message": "method tidak didukung: %s" % method}})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        for m in (msg if isinstance(msg, list) else [msg]):
            handle(m)


if __name__ == "__main__":
    main()

