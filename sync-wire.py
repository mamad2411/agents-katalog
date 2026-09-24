#!/usr/bin/env python3
"""sync-wire.py — bersihkan pemakaian skill kadaluarsa + symlink katalog curated
ke folder skills AI (TIERED), + pastikan MCP skill-catalog terpasang.

Kebijakan v2 (tiered wiring — biar AI TIDAK berat):
  - Yang di-symlink native HANYA "core" (~55 skill harian) dari skill-core.json.
    Alasan: Claude Code memindai ~/.claude/skills secara native — makin banyak
    entri, makin berat discovery-nya di tiap sesi.
  - Sisa 14.916 skill TETAP bisa dipakai semua AI via MCP skill-catalog
    (skill_for_task/skill_search/skill_load) atau CLI skill-search.sh — ringan.
  - full_native (di skill-core.json): daftar tambahan yang mau di-link penuh.
  - Aturan lama tetap berlaku:
    - symlink MATI (target sudah tidak ada, mis. ke junk yang dihapus) -> dihapus.
    - symlink ke ~/.agents/skills-expanded padahal nama ada di core -> arahkan ulang.
    - real dir (klon/bucket plugin, mis. ~/.claude/skills/synced) -> TIDAK disentuh.
    - skill core yang belum ter-link -> dibuatkan symlink.
  - OPSI: --full  = kembalikan perilaku lama (link SEMUA curated; berat).
  Log audit: ~/.agents/sync-wire-log.json
"""
import glob
import json
import os
import time

HOME = os.path.expanduser("~")
SRC = os.path.join(HOME, ".agents", "skills")
EXPANDED = os.path.join(HOME, ".agents", "skills-expanded")
CORE_F = os.path.join(HOME, ".agents", "skill-core.json")
LOG_F = os.path.join(HOME, ".agents", "sync-wire-log.json")
FULL = "--full" in __import__("sys").argv

JSON_PROVIDERS = [
    "~/.hermes/mcp.json", "~/.codebuddy/mcp.json", "~/.continue/mcp.json",
    "~/.aider/mcp.json", "~/.opencode/mcp.json", "~/.windsurf/mcp.json",
    "~/.cline/mcp.json", "~/.trae/mcp.json", "~/.roo/mcp.json",
    "~/.tabnine/mcp.json", "~/.qwen/mcp.json", "~/.goose/mcp.json",
    "~/.kiro/mcp.json", "~/.copilot/mcp.json", "~/.gemini/settings.json",
    "~/.antigravity/mcp.json", "~/.claude.json",
]


def curated_map():
    out = {}
    for name in sorted(os.listdir(SRC)):
        if os.path.isfile(os.path.join(SRC, name, "SKILL.md")):
            out[name] = os.path.join(SRC, name)
    return out


def tool_dirs():
    out = []
    for p in glob.glob(os.path.join(HOME, ".*", "skills")):
        if os.path.realpath(p) == os.path.realpath(SRC):
            continue  # sumber itu sendiri
        if os.path.isdir(p):
            out.append(p)
    return sorted(out)


def core_map():
    """Skill yang akan di-symlink native: core + full_native dari skill-core.json.
    Hanya nama yang ADA di katalog curated yang diikutkan; --full = semua curated."""
    curated = curated_map()
    if FULL:
        return curated
    want = []
    try:
        d = json.load(open(CORE_F, encoding="utf-8"))
        want = list(d.get("core") or []) + list(d.get("full_native") or [])
    except Exception as e:
        print("  !! skill-core.json gagal dibaca (%s) — pakai core kosong" % e)
    out = {}
    missing = []
    for name in want:
        if name in curated:
            out[name] = curated[name]
        elif name not in missing:
            missing.append(name)
    if missing:
        print("  (core tak ketemu di curated, dilewati: %s)" % ", ".join(missing[:8]) +
              (" …" if len(missing) > 8 else ""))
    return out


def wire_tools(wire):
    totals = {"dead_removed": 0, "retargeted": 0, "created": 0,
              "kept_valid": 0, "real_dir_kept": 0, "pruned": 0}
    removed_log = []
    for tool in tool_dirs():
        per = {"dead": 0, "retgt": 0, "new": 0, "pruned": 0}
        for e in os.scandir(tool):
            if not e.is_symlink():
                if e.is_dir():
                    totals["real_dir_kept"] += 1
                continue
            if not FULL and e.name not in wire:
                # kebijakan tiered: symlink non-core dihapus (bisa diakses via MCP).
                try:
                    os.unlink(e.path)
                    removed_log.append({"tool": tool, "name": e.name, "why": "non-core"})
                    totals["pruned"] += 1; per["pruned"] += 1
                except FileNotFoundError:
                    pass                                    # race: sudah dihapus instans lain
                continue
            tgt = os.readlink(e.path)
            tgt_abs = os.path.normpath(os.path.join(tool, tgt)) if not os.path.isabs(tgt) else tgt
            if not os.path.exists(e.path):                       # symlink mati
                try:
                    os.unlink(e.path)
                except FileNotFoundError:
                    totals["kept_valid"] += 1
                    continue
                removed_log.append({"tool": tool, "name": e.name, "target": tgt})
                totals["dead_removed"] += 1; per["dead"] += 1
            elif tgt_abs.startswith(EXPANDED + os.sep) and e.name in wire:
                os.unlink(e.path)                                # arahkan ulang
                os.symlink(wire[e.name], e.path)
                totals["retargeted"] += 1; per["retgt"] += 1
            else:
                totals["kept_valid"] += 1
        for name, path in wire.items():                          # link core yang belum ada
            dst = os.path.join(tool, name)
            if not os.path.lexists(dst):
                try:
                    os.symlink(path, dst)
                except FileExistsError:
                    continue                                     # race: sudah dibuat instans lain
                totals["created"] += 1; per["new"] += 1
        print("  %-24s mati:%-4d arah-ulang:%-4d baru:%-4d pangkas:%-5d" % (
            os.path.dirname(tool).replace(HOME, "~"), per["dead"], per["retgt"], per["new"], per["pruned"]))
    return totals, removed_log
# === lanjutan file ===

def ensure_mcp():
    entry = {"command": "python3", "args": [os.path.join(HOME, ".agents", "skill-mcp.py")]}
    changed = 0
    for p in JSON_PROVIDERS:
        f = os.path.expanduser(p)
        if not os.path.exists(f):
            continue
        try:
            d = json.load(open(f))
        except Exception:
            continue
        m = d.get("mcpServers")
        if m is None and p.endswith("settings.json"):
            m = d.setdefault("mcpServers", {})
        if not isinstance(m, dict):
            continue
        if "skill-catalog" not in m:
            import shutil
            shutil.copy2(f, f + ".bak-sync")
            m["skill-catalog"] = entry
            json.dump(d, open(f, "w"), indent=2, ensure_ascii=False)
            changed += 1
            print("  + skill-catalog -> %s" % p)
    print("  MCP skill-catalog: %d file ditambah (sisanya sudah ada)" % changed)


def purge_usage():
    """Hapus catatan pemakaian MCP yang servernya sudah tidak terdaftar (kadaluarsa)."""
    uf = os.path.join(HOME, ".agents", "mcp-usage.json")
    if not os.path.exists(uf):
        return
    reg = set()
    for p in JSON_PROVIDERS:
        f = os.path.expanduser(p)
        try:
            d = json.load(open(f))
            reg |= set((d.get("mcpServers") or {}).keys())
        except Exception:
            pass
    toml = os.path.join(HOME, ".codex", "config.toml")
    if os.path.exists(toml):
        import re
        reg |= set(re.findall(r"^\[mcp_servers\.([^\.\]]+)",
                              open(toml, errors="ignore").read(), re.M))
    u = json.load(open(uf))
    keep = {k: v for k, v in u.items() if k.startswith("_") or k in reg}
    drop = len(u) - len(keep)
    if drop:
        json.dump(keep, open(uf, "w"), indent=2)
    print("  mcp-usage: %d catatan kadaluarsa dihapus, %d tersisa" % (drop, len(keep)))


def main():
    t0 = time.time()
    wire = core_map()
    print("sumber: %s (%d skill curated)" % (SRC, len(curated_map())))
    print("mode: %s — di-link native: %d skill %s" % (
        "FULL" if FULL else "TIERED", len(wire),
        "" if FULL else "(sisanya via MCP skill-catalog — ringan)"))
    print("[1/3] wiring semua tool AI:")
    totals, removed_log = wire_tools(wire)
    print("[2/3] MCP skill-catalog:")
    ensure_mcp()
    print("[3/3] pemakaian MCP kadaluarsa:")
    purge_usage()
    json.dump({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "mode": "full" if FULL else "tiered",
               "wired": sorted(wire), "totals": totals,
               "removed": removed_log[:2000]}, open(LOG_F, "w"), indent=1)
    print("total: mati-%d, arah-ulang-%d, baru-%d, pangkas-%d, valid-dipertahankan-%d, real-dir-dibiarkan-%d"
          % (totals["dead_removed"], totals["retargeted"], totals["created"],
             totals.get("pruned", 0), totals["kept_valid"], totals["real_dir_kept"]))
    print("log audit: %s (%.1fs)" % (LOG_F, time.time() - t0))


if __name__ == "__main__":
    main()