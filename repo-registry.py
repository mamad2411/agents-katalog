#!/usr/bin/env python3
"""Repo Registry — katalog repo komunitas berkualitas (anti-duplicate).

- Sumber: GitHub search (awesome lists skills/MCP) + repo yang sudah ada di .agents
- Dedup by full_name (lowercase) -> repo-registry.json
- Tanpa clone massal: cuma metadata (name, stars, desc, url, topic)
- --fetch : refresh dari GitHub API (rate-limit friendly, 2s delay)
- --add <full_name> <stars> <desc> : manual
- status default: tampilkan
"""
import json, os, sys, time, urllib.request

REG_F = os.path.expanduser("~/.agents/repo-registry.json")
SEED = [  # hasil discovery verified (bintang komunitas tinggi)
    ("ComposioHQ/awesome-claude-skills", 75280),
    ("hesreallyhim/awesome-claude-code", 54262),
    ("sickn33/agentic-awesome-skills", 46558),
    ("VoltAgent/awesome-agent-skills", 34567),
    ("BehiSecc/awesome-claude-skills", 10153),
    ("appcypher/awesome-mcp-servers", 5771),
    ("0xNyk/awesome-hermes-agent", 5687),
    ("wong2/awesome-mcp-servers", 4317),
    ("bergside/awesome-design-skills", 2840),
    ("rohitg00/awesome-claude-code-toolkit", 2623),
    ("composio-community/awesome-claude-plugins", 1969),
    ("rohitg00/awesome-devops-mcp-servers", 1022),
]

def load():
    try: return json.load(open(REG_F))
    except Exception: return {"repos": {}, "updated": None}

def add(reg, full, stars, desc="", tags=None):
    key = full.lower().strip()
    reg["repos"][key] = {"full_name": full, "stars": stars, "desc": desc[:120],
                         "tags": tags or ["community"], "added": time.strftime("%Y-%m-%d")}

def fetch(reg):
    qs = ["awesome+agent+skills", "awesome+mcp+servers", "awesome+claude+skills",
          "mcp+server+boilerplate", "agent+skill+creator"]
    for q in qs:
        try:
            req = urllib.request.Request(f"https://api.github.com/search/repositories?q={q}&sort=stars&per_page=15",
                                         headers={"Accept": "application/vnd.github+json"})
            d = json.load(urllib.request.urlopen(req, timeout=10))
            for r in d.get("items", []):
                add(reg, r["full_name"], r["stargazers_count"], r.get("description") or "",
                    ["community", q.split("+")[1] if "+" in q else q])
            print(f"  {q}: +{len(d.get('items', []))}")
        except Exception as e:
            print(f"  {q}: skip ({e})")
        time.sleep(2)  # rate-limit friendly
    reg["updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    reg = load(); n0 = len(reg["repos"])
    if "--fetch" in sys.argv: fetch(reg)
    for full, stars in SEED: add(reg, full, stars)
    json.dump(reg, open(REG_F, "w"), indent=2, ensure_ascii=False)
    top = sorted(reg["repos"].values(), key=lambda r: -r["stars"])[:10]
    print(f"REPO REGISTRY: {n0} -> {len(reg['repos'])} repo (dedup by full_name)")
    for r in top: print(f"  {r['stars']:>6}  {r['full_name']}")
