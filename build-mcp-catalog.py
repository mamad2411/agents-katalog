#!/usr/bin/env python3
"""build-mcp-catalog.py — bangun katalog MCP dari awesome-mcp-servers.

Output: ~/.agents/mcp-catalog.json  (metadata: name, repo, desc, lang, scope, run_hint)
Tujuan: daftar ~1000 MCP "terinstall" secara metadata, TIDAK jalan (parkir).
Aktivasi on-demand via mcp-lifecycle.py --on <name> setelah run-config dikonfirmasi.

Kenapa metadata dulu? Karena run-command tiap MCP beda (npx/uvx/go run/python -m).
Parkir metadata = 0 CPU/0 RAM. Saat dibutuhkan, AI/user kasih run-config,
baru masuk mcp-parked.json.
"""
import json, os, re, sys

AGENTS = os.path.expanduser("~/.agents")
SRC = os.path.join(AGENTS, "repo-refs/awesome-mcp-servers/README.md")
OUT = os.path.join(AGENTS, "mcp-catalog.json")

LANG_MAP = {
    "🐍": "python",  "🐍 ": "python",
    "📇": "typescript", "📇 ": "typescript",
    "🏎️": "go", "🏎": "go",
    "🦀": "rust",   "🦀 ": "rust",
    "#️⃣": "csharp", "💎": "ruby", "☕": "java", "🌊": "cpp",
}
SCOPE_MAP = {"☁️": "cloud", "🏠": "local", "📟": "embedded"}

def run_hint(lang, repo):
    owner, name = repo.split("/")[-2:]
    if lang == "python":
        return f"uvx {name.lower().replace('_','-')}"
    if lang in ("typescript", "javascript"):
        return f"npx -y {name.lower()}"
    if lang == "go":
        return f"go run github.com/{repo}"
    return None

ENTRY = re.compile(r'^- \[([^/\]]+/[^]]+)\]\((https://github\.com/[^)]+)\)\s*(.*?)$')

def parse():
    if not os.path.exists(SRC):
        print(f"sumber tidak ada: {SRC}", file=sys.stderr); return []
    seen = set(); items = []
    for line in open(SRC, encoding="utf-8"):
        m = ENTRY.match(line)
        if not m: continue
        repo, url, rest = m.group(1), m.group(2), m.group(3)
        if repo in seen: continue
        seen.add(repo)
        # skip non-server (clients/awesome meta)
        if repo.lower() in ("punkpeye/awesome-mcp-servers","punkpeye/awesome-mcp-clients"): continue
        desc = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', rest).strip()
        desc = re.sub(r'^\[.*?\]\([^)]*\)\s*', '', desc).strip()
        # emoji detect
        lang = None; scope = None
        for emo,l in LANG_MAP.items():
            if emo in rest: lang = l; break
        for emo,s in SCOPE_MAP.items():
            if emo in rest: scope = s; break
        # deskripsi: buang emoji + strip leading "-"
        desc = re.sub(r'^[\U0001F300-\U0001FAFF\U00002600-\U000027BF\uFE0F#️⃣☕🌊💎 ]+ - ?', '', desc).strip()
        desc = desc.lstrip('- ').strip() or "(no description)"
        name = repo.split('/')[-1].lower()
        items.append({
            "name": name,
            "repo": repo,
            "url": url,
            "description": desc[:200],
            "lang": lang,
            "scope": scope,
            "run_hint": run_hint(lang, repo),
        })
    return items

if __name__ == "__main__":
    items = parse()
    # dedup by name (keep first)
    by_name = {}
    for it in items:
        by_name.setdefault(it["name"], it)
    final = list(by_name.values())
    json.dump(final, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"katalog: {len(final)} MCP (dari {len(items)} entri)")
    by_lang = {}
    for it in final:
        by_lang[it["lang"] or "unknown"] = by_lang.get(it["lang"] or "unknown", 0) + 1
    print("per bahasa:", by_lang)
    print(f"file: {OUT}")
