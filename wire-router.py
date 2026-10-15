#!/usr/bin/env python3
"""wire-router.py — pasang mcp-router + blok trigger ke SEMUA AI tool.

- JSON config  : tambah server `mcp-router` kalau belum ada (cursor, codebuddy, claude, gemini).
- Markdown     : inject blok antara <!-- cap-router:start/end --> (idempotent).
- Tiap file yang diubah dibackup ke <file>.bak-router-<YYYYMMDD>.

Pakai: python3 ~/.agents/wire-router.py            # laporan + terapkan
"""
import json, os, shutil, time, sys
from pathlib import Path

HOME = Path.home()
ROUTER = str(HOME / ".agents" / "mcp-router.py")
STAMP = time.strftime("%Y%m%d")
START, END = "<!-- cap-router:start -->", "<!-- cap-router:end -->"

BLOCK = """<!-- cap-router:start -->
## Router aset (MCP + prompt/agent/rule) — ON-DEMAND, jangan nyalakan semua

Satu meta-server `mcp-router` tahu **semua** aset: MCP (`mcp-catalog.json`) +
aset komunitas (`cap-catalog.json`: prompts, agents, rules, hooks, plugins,
memory, dst) + **indeks retrieval** (`retrieve.db`, skill+MCP+prompt ~147k aset).

- Butuh aset → **`retrieve(query, k[, kind])`** (BM25) → balikin top-k + id.
  **PAKAI INI DULU** sebelum memuat banyak aset — hemat token.
- Ambil isi 1 aset → `cap_get(id)`. Butuh MCP → `mcp_search` lalu `mcp_use(name, tool, arguments)`.
  MCP nyala **cuma saat dipakai**; idle 300s **auto-mati** (anti-overheat).
- **Sebelum kirim jawaban final → `self_check(text)`** (anti-slop + struktur +
  boros). Perbaiki dulu kalau skor < 85.
- **Jangan** nyalakan semua MCP. Cek `mcp_status` untuk yang sedang hidup.
- Butuh kapabilitas baru? Cari dulu di router sebelum bilang "tidak bisa".

## Otomatis — tanpa perlu user ketik /perintah
- **Retrieve dulu**; jangan dump semua konteks.
- **Self-check** tiap jawaban final; poles sebelum kirim (anti-slop).
- **Compact proaktif** saat konteks >40% (jangan tunggu disuruh).
- **Hemat token**: ringkas output tool ≤800 char, jangan baca ulang file yang
  sama, batch panggilan yang saling bebas.
- **Model routing**: tugas remeh → model murah/cepat; tugas sulit (arsitektur,
  debug rumit, review kritis) → flagship.
- Ukur pemborosan: `python3 ~/.agents/token-telemetry.py`.
<!-- cap-router:end -->"""

JSON_TARGETS = [
    HOME / ".cursor" / "mcp.json",
    HOME / ".codebuddy" / "mcp.json",
    HOME / ".claude.json",
    HOME / ".gemini" / "settings.json",
]
MD_TARGETS = [
    HOME / ".claude" / "CLAUDE.md",
    HOME / ".codex" / "instructions.md",
    HOME / ".codex" / "AGENTS.md",
    HOME / ".codebuddy" / "AGENTS.md",
    HOME / ".gemini" / "GEMINI.md",
    HOME / ".cursorrules",
]


def backup(p):
    shutil.copy2(p, str(p) + ".bak-router-" + STAMP)


def wire_json(p):
    if not p.exists():
        return "absent"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return "ERR parse: %s" % str(e)[:50]
    ms = d.setdefault("mcpServers", {})
    if "mcp-router" in ms:
        return "sudah ada"
    ms["mcp-router"] = {"command": "python3", "args": [ROUTER]}
    backup(p)
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return "DITAMBAH"


def wire_md(p):
    if not p.exists():
        return "absent"
    t = p.read_text(encoding="utf-8", errors="ignore")
    if START in t and END in t:
        head = t.split(START)[0]
        tail = t.split(END, 1)[1]
        new = head + BLOCK + tail
        if new != t:
            backup(p)
            p.write_text(new, encoding="utf-8")
            return "DIPERBARUI"
        return "sudah ada"
    backup(p)
    p.write_text(t.rstrip() + "\n\n" + BLOCK + "\n", encoding="utf-8")
    return "DITAMBAH"


def main():
    print("== JSON (registrasi mcp-router) ==")
    for p in JSON_TARGETS:
        print("  %-42s %s" % (str(p).replace(str(HOME), "~"), wire_json(p)))
    print("== MARKDOWN (blok trigger) ==")
    for p in MD_TARGETS:
        print("  %-42s %s" % (str(p).replace(str(HOME), "~"), wire_md(p)))
    # cursor rule baru
    r = HOME / ".cursor" / "rules" / "cap-router.mdc"
    r.parent.mkdir(parents=True, exist_ok=True)
    fm = "---\ndescription: Router aset on-demand (MCP + prompt/agent/rule)\nalwaysApply: true\n---\n\n"
    body = fm + BLOCK + "\n"
    if not r.exists() or r.read_text(encoding="utf-8") != body:
        if r.exists():
            backup(r)
        r.write_text(body, encoding="utf-8")
        print("  %-42s DIBUAT" % str(r).replace(str(HOME), "~"))
    else:
        print("  %-42s sudah ada" % str(r).replace(str(HOME), "~"))


if __name__ == "__main__":
    main()
