#!/usr/bin/env python3
"""mcp-slim-all.py — rapikan MCP di SEMUA tool AI (kebijakan repo: skill-catalog + mcp-router).

Latar: AGENTS.md §Aturan keras "MCP default MATI (2026-09-25): hanya skill-catalog +
mcp-router (+skill-graph di Codex) yang terdaftar; sisanya di mcp-parked.json → hidup
on-demand via mcp_use". Kebijakan itu baru diterapkan di Claude/Codex/Gemini; audit
2026-09-26 menemukan 12 tool lain masih mendaftarkan 9 server (context7, fetch,
filesystem, git, memory, playwright, sequential-thinking, time) — skema tool mereka
ikut ke system prompt tiap sesi = fixed cost besar yang tidak dipakai.

Pakai:
  python3 ~/.agents/mcp-slim-all.py            # dry-run (laporan saja)
  python3 ~/.agents/mcp-slim-all.py --apply    # tulis (backup .bak-YYYYMMDD dulu)

Server yang dilepas TIDAK hilang: namanya ditulis ke ~/.agents/mcp-parked.json
(dipakai mcp-lifecycle/mcp-router untuk hidup on-demand).
Idempoten: dijalankan 2× hasilnya sama.
"""
import glob
import json
import os
import shutil
import sys
import time

HOME = os.path.expanduser("~")
KEEP = {"skill-catalog", "mcp-router"}
PARKED = os.path.join(HOME, ".agents", "mcp-parked.json")
STAMP = time.strftime("%Y%m%d")


def configs():
    out = []
    for pat in ("/.[a-z]*/mcp.json", "/.[a-z]*/.mcp.json"):
        out += sorted(glob.glob(HOME + pat))
    return out


def load_json(p):
    try:
        if os.path.getsize(p) > 2_000_000:
            return None
        return json.load(open(p))
    except Exception:
        return None


def main():
    apply = "--apply" in sys.argv
    parked = load_json(PARKED) or {}
    if isinstance(parked, list):
        parked = {k: {} for k in parked}
    planned = {}
    changed_files = []

    for p in configs():
        d = load_json(p)
        if not isinstance(d, dict):
            continue
        key = "mcpServers" if "mcpServers" in d else ("servers" if "servers" in d else None)
        if not key or not isinstance(d.get(key), dict):
            continue
        servers = d[key]
        drop = [s for s in servers if s not in KEEP]
        if not drop:
            continue
        keep = [s for s in servers if s in KEEP]
        planned[p.replace(HOME, "~")] = (len(servers), len(keep), drop)
        changed_files.append((p, d, key, drop))

    print("=== RENCANA RAMPING MCP (%s) ===" % ("APPLY" if apply else "dry-run"))
    for p, (before, after, drop) in sorted(planned.items()):
        print("  %-34s %d -> %d server | dilepas: %s" % (p, before, after, ", ".join(drop)))
    print("file terpengaruh: %d | server dilepas (unik): %d"
          % (len(planned), len({s for _, _, _, d in changed_files for s in d})))
    if not changed_files:
        print("tidak ada yang perlu diubah (sudah ramping)")
        return 0
    if not apply:
        print("\nJalankan ulang dengan --apply untuk menulis (backup otomatis).")
        return 0

    for p, d, key, drop in changed_files:
        shutil.copy2(p, "%s.bak-%s" % (p, STAMP))
        for s in drop:
            parked.setdefault(s, {})
            parked[s]["parked_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            parked[s]["from"] = p.replace(HOME, "~")
        d[key] = {k: v for k, v in d[key].items() if k in KEEP}
        tmp = p + ".tmp%d" % os.getpid()
        with open(tmp, "w") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, p)
        try:
            json.load(open(p))          # validasi; rusak → balikkan
        except Exception:
            shutil.copy2("%s.bak-%s" % (p, STAMP), p)
            print("GAGAL (dipulihkan):", p)
            continue
        print("OK:", p.replace(HOME, "~"), "| backup .bak-%s" % STAMP)

    tmp = PARKED + ".tmp%d" % os.getpid()
    with open(tmp, "w") as f:
        json.dump(parked, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    os.replace(tmp, PARKED)
    print("parked diperbarui:", PARKED.replace(HOME, "~"), "(%d entri)" % len(parked))
    print("hidupkan lagi kapan saja: python3 ~/.agents/mcp-lifecycle.py --on <nama>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
