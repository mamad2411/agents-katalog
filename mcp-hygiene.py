#!/usr/bin/env python3
"""mcp-hygiene.py — audit + prune sprawl MCP (P0 ringan, reversible).

Default = LAPORAN saja (tidak menulis apa pun).
--apply  = tulis perubahan ke config TOML (backup otomatis + validasi tomllib):
             * buang server auto-clone ber-prefix `gh_`
             * buang varian nama duplikat (underscore vs kebab); simpan yang kebab
             * opsional `--keep <file>`: allowlist (1 nama/baris) → sisanya dibuang

Pakai:
  python3 ~/.agents/mcp-hygiene.py
  python3 ~/.agents/mcp-hygiene.py --apply
  python3 ~/.agents/mcp-hygiene.py --apply --keep ~/.agents/mcp-allowlist.txt
"""
import argparse
import json
import os
import re
import shutil
import sys
import tomllib
from datetime import datetime

HOME = os.path.expanduser("~")
DEFAULT_TOML = os.path.join(HOME, ".codex", "config.toml")
JSON_CONFIGS = [
    os.path.join(HOME, ".windsurf", "mcp.json"),
    os.path.join(HOME, ".codebuddy", "mcp.json"),
    os.path.join(HOME, ".gemini", "settings.json"),
    os.path.join(HOME, ".claude.json"),
]
HDR_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")
NAME_RE = re.compile(r"^mcp_servers\.([^.\[\]]+)")
REPORT = os.path.join(HOME, ".agents", "mcp-hygiene-report.md")


def parse_toml_blocks(text):
    """name -> [(start_idx, end_idx)] untuk tiap blok [mcp_servers.NAME*]."""
    lines = text.splitlines(keepends=True)
    segs, cur = {}, None
    for i, ln in enumerate(lines):
        m = HDR_RE.match(ln)
        if m:
            nm = NAME_RE.match(m.group(1))
            new = nm.group(1) if nm else None
            if cur and segs[cur][-1][1] is None:
                segs[cur][-1][1] = i
            cur = new
            if new:
                segs.setdefault(new, []).append([i, None])
    if cur and segs.get(cur) and segs[cur][-1][1] is None:
        segs[cur][-1][1] = len(lines)
    return lines, segs


def norm(n):
    """Nama ternormalisasi untuk deteksi duplikat penamaan."""
    return re.sub(r"-+", "-", n.lower().replace("_", "-"))


def pick_keeper(group, segs):
    """Varian yang dipertahankan: utamakan tanpa underscore, lalu blok terbesar."""
    def key(n):
        size = sum(e - s for s, e in segs[n])
        return ("_" in n, -size, n)
    return sorted(group, key=key)[0]


def report_json_configs():
    rows = []
    for p in JSON_CONFIGS:
        if not os.path.exists(p):
            continue
        try:
            with open(p) as f:
                d = json.load(f)
            rows.append((p, "ok", len(d.get("mcpServers") or {})))
        except Exception as e:
            rows.append((p, "error: %s" % e, 0))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_TOML)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--keep", default=None)
    ap.add_argument("--report", default=REPORT)
    a = ap.parse_args()

    if not os.path.exists(a.config):
        print("ERROR: config tidak ada: %s" % a.config)
        return 1
    with open(a.config, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    lines, segs = parse_toml_blocks(text)

    names = sorted(segs)
    gh = [n for n in names if n.startswith("gh_")]
    groups = {}
    for n in names:
        groups.setdefault(norm(n), []).append(n)
    variants = {k: v for k, v in groups.items() if len(v) > 1}
    losers = []
    for v in variants.values():
        keep = pick_keeper(v, segs)
        losers += [n for n in v if n != keep]

    keepset = None
    if a.keep:
        with open(a.keep) as f:
            keepset = {l.strip() for l in f if l.strip() and not l.startswith("#")}

    if keepset is not None:
        remove = [n for n in names if n not in keepset]
    else:
        remove = list(gh) + losers
    remove = sorted(set(remove) & set(names))

    md = [
        "# MCP Hygiene Report — %s" % datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
        "Config: `%s`" % a.config,
        "",
        "- Server MCP: **%d**" % len(names),
        "- Auto-clone `gh_*`: **%d**" % len(gh),
        "- Grup nama duplikat: **%d** (varian berlebih: %d)" % (len(variants), len(losers)),
        "- Kandidat dibuang: **%d** → sisa **%d**" % (len(remove), len(names) - len(remove)),
        "",
    ]
    if variants:
        md += ["## Duplikat penamaan (underscore vs kebab)", ""]
        for k, v in sorted(variants.items())[:25]:
            md.append("- `%s` → %s" % (k, ", ".join("`%s`" % x for x in v)))
        md.append("")
    md += ["## Server non-gh tersisa", ""]
    removed_set = set(remove)
    for n in [x for x in names if x not in removed_set]:
        md.append("- `%s`" % n)
    rows = report_json_configs()
    if rows:
        md += ["", "## Config JSON agen lain (laporan saja)", "",
               "| File | Status | Jumlah server |", "|---|---|---|"]
        md += ["| `%s` | %s | %d |" % r for r in rows]
    with open(a.report, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print("config      : %s" % a.config)
    print("server MCP  : %d" % len(names))
    print("gh_*        : %d" % len(gh))
    print("duplikat    : %d grup (%d varian berlebih)" % (len(variants), len(losers)))
    print("akan dibuang: %d  → sisa %d" % (len(remove), len(names) - len(remove)))
    print("laporan     : %s" % a.report)

    if not a.apply:
        print("\n(dry-run — jalankan dengan --apply untuk menulis)")
        return 0

    drop = set()
    for n in remove:
        for s, e in segs[n]:
            drop.update(range(s, e))
    new_text = "".join(ln for i, ln in enumerate(lines) if i not in drop)
    try:
        tomllib.loads(new_text)          # validasi: harus tetap TOML valid
    except Exception as e:
        print("ABORT: hasil tidak valid TOML (%s) — config tidak diubah" % e)
        return 1

    backup = "%s.bak-%s" % (a.config, datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(a.config, backup)
    with open(a.config, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("\nAPPLIED. backup: %s" % backup)
    print("baris: %d → %d" % (len(lines), len(new_text.splitlines())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
