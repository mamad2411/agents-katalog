#!/usr/bin/env python3
"""topic-mine.py — tambang SKILL.md dari repo hasil GitHub REPO search (bukan code search).

Kenapa: code search filename:SKILL.md mentok di repo yg sama (yield 0 repo baru
di 600 query terakhir). Repo search by topic (claude-skill, claude-code, ai-agents,
mcp-server, ...) menjangkau repo yg BELUM pernah di-enum.

Cara: repo search (core API, 5000/jam) -> untuk tiap repo, git tree (1 req) ->
SKILL.md via raw.githubusercontent -> dedup vs index -> skills-expanded/topic-*.
Checkpoint: ~/.agents/.topic-mine-state.json. Semua nice-able, curl/raw tanpa limit.
Pakai: nice -n 15 python3 ~/.agents/topic-mine.py --pages 5
"""
import argparse, json, os, re, sqlite3, subprocess, sys, time
from datetime import datetime, timezone

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
STATE = os.path.join(AG, ".topic-mine-state.json")
TOKEN = os.environ.get("GH_TOKEN", "")
FM = re.compile(r"^name:\s*[\"']?([\w-]+)", re.M)

TOPICS = ["claude-skill", "claude-code", "claude-agent", "ai-skills",
          "agent-skills", "mcp-server", "ai-agents", "awesome-claude",
          "claude-plugin", "gemini-skills",
          # JILID-2 (baru, belum pernah di-enum)
          "claude-code-plugin", "ai-workflow", "prompt-engineering",
          "cursor-rules", "copilot", "langchain", "autogen",
          "crewai", "letta", "ai-prompt", "openclaw", "claude-hooks",
          "subagent", "slash-commands",
          # JILID-3
          "llm", "rag", "fine-tuning", "embedding", "ai-automation",
          "obsidian", "notion", "chatgpt", "n8n", "zapier",
          "telegram-bot", "discord-bot", "web-scraping", "code-review",
          "vscode-extension", "ai-image", "text-to-speech", "agent-framework",
          "bot", "monitoring", "documentation", "testing", "devtools",
          "automation", "pipeline", "data-pipeline", "security-scanning",
          "gardener", "docker", "kubernetes",
          # JILID-4
          "github-actions", "supabase", "prisma", "stripe", "tailwind",
          "threejs", "pytorch", "tensorflow", "huggingface", "stable-diffusion",
          "midjourney", "pandas", "fastapi", "django", "nextjs",
          "vuejs", "svelte", "rust", "golang", "typescript",
          "homeassistant", "home-automation", "iot", "arduino", "raspberry-pi",
          "netlify", "cloudflare", "vercel", "nginx", "grafana"]


def gh(url, timeout=25):
    cmd = ["curl", "-s", "--max-time", str(timeout),
           "-H", "Accept: application/vnd.github+json",
           "-H", "User-Agent: topic-mine/1.0"]
    if TOKEN:
        cmd += ["-H", f"Authorization: Bearer {TOKEN}"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    if not r.stdout.strip():
        raise RuntimeError("empty")
    return json.loads(r.stdout)


def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {"repos": [], "done": [], "new": 0, "exists": 0, "miss": 0}


def save_state(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1)
    os.replace(tmp, STATE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=5)
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    st = load_state()
    if a.status:
        print(f"repos terkumpul: {len(st['repos'])} | done: {len(st['done'])} "
              f"| new={st['new']} exists={st['exists']} miss={st['miss']}")
        return 0
    if not TOKEN:
        print("ERROR: GH_TOKEN wajib", file=sys.stderr)
        return 1
    import urllib.parse
    # 1. enum repo per topic (hemat: 10 topic x N pages)
    known = set(st["repos"])
    for topic in TOPICS:
        for pg in range(1, a.pages + 1):
            q = urllib.parse.quote(f"topic:{topic} stars:>3")
            try:
                d = gh(f"https://api.github.com/search/repositories?q={q}"
                       f"&sort=stars&per_page=100&page={pg}")
            except Exception as e:
                print(f"  ! {topic} p{pg}: {e}", flush=True)
                time.sleep(5)
                continue
            added = 0
            for r in d.get("items", []):
                fn = r.get("full_name")
                if fn and fn not in known:
                    known.add(fn); st["repos"].append(fn); added += 1
            print(f"  [{topic} p{pg}] +{added} (total {len(st['repos'])})", flush=True)
            save_state(st)
            time.sleep(2)
    # 2. fetch SKILL.md per repo: tree API (1 req) -> raw (no limit)
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    existing = {r[0] for r in conn.execute("SELECT name FROM skills")}
    conn.close()
    done = set(st["done"])
    todo = [r for r in st["repos"] if r not in done]
    print(f"=== fetch {len(todo)} repo ===", flush=True)
    for i, full in enumerate(todo, 1):
        try:
            t = gh(f"https://api.github.com/repos/{full}/git/trees/HEAD?recursive=1",
                   timeout=15)
            paths = [x["path"] for x in t.get("tree", [])
                     if x.get("path", "").endswith("SKILL.md")][:40]
        except Exception:
            paths = []
        hit = False
        for p in paths:
            r = subprocess.run(
                ["curl", "-s", "-f", "--max-time", "12",
                 f"https://raw.githubusercontent.com/{full}/HEAD/{p}"],
                capture_output=True, timeout=18)
            if r.returncode == 0 and r.stdout:
                m = FM.search(r.stdout.decode("utf-8", "ignore"))
                name = re.sub(r"-{2,}", "-",
                              (m.group(1) if m else full.split("/")[1]).lower()).strip("-")
                if name in existing:
                    st["exists"] += 1
                else:
                    dd = os.path.join(DEST, "topic-" + full.replace("/", "-") + "-" +
                                      re.sub(r"[^a-z0-9-]+", "-", p.lower().split("/")[-2] if "/" in p else "root")[:30])
                    os.makedirs(dd, exist_ok=True)
                    open(os.path.join(dd, "SKILL.md"), "wb").write(r.stdout)
                    existing.add(name); st["new"] += 1
                hit = True
        if not hit:
            st["miss"] += 1
        done.add(full)
        if i % 25 == 0:
            st["done"] = sorted(done); save_state(st)
            print(f"  [{i}/{len(todo)}] new={st['new']} exists={st['exists']} miss={st['miss']}", flush=True)
        time.sleep(0.5)
    st["done"] = sorted(done); save_state(st)
    print(f"HASIL: new={st['new']} exists={st['exists']} miss={st['miss']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
