#!/usr/bin/env python3
"""Discovery repo baru berisi skill (SKILL.md) — masif, multi-gelombang.

Pakai:
  python3 discover-repos.py            # gelombang otomatis (lihat .wave)
  python3 discover-repos.py --wave 3   # paksa gelombang tertentu

Jalur:
  1. gh search repos  : query teks + topic (limit 1000, sort stars)
  2. gh search code   : filename:SKILL.md + varian path (repo yang BENAR punya skill)
  3. ambil bintang untuk repo hasil code-search (core API)
Hasil digabung ke repo-registry.json (dedup by full_name lowercase).
"""
import json, os, subprocess, sys, time

AG = os.path.expanduser("~/.agents")
REG = os.path.join(AG, "repo-registry.json")
WAVE_F = os.path.join(AG, ".discover-wave")
MIN_STARS = int(os.environ.get("DISCOVER_MIN_STARS", "1"))
# gh search --limit 1000 butuh ~36s/query; 300 ~10s -> gelombang jauh lebih cepat.
LIMIT = int(os.environ.get("DISCOVER_LIMIT", "300"))

# Rotasi query per gelombang -> tiap gelombang menyisir sudut baru.
REPO_SETS = [
    ["claude skills", "agent skills", "awesome claude", "skills marketplace",
     "claude code plugin", "claude code skills", "agentic skills", "ai agent skills",
     "SKILL.md", "subagent skills", "claude plugins", "mcp servers"],
    ["claude subagents", "claude hooks", "claude slash commands", "agent rules",
     "cursor rules", "copilot instructions", "prompt library", "system prompt",
     "ai workflow", "agent framework skills", "llm skills", "tool use agents"],
    ["claude code template", "ai coding agent", "autonomous agent skills",
     "skill marketplace", "agent toolkit", "prompt engineering kit",
     "claude agents collection", "awesome ai agents", "agent memory",
     "rag agent skills", "eval harness agent", "guardrails llm"],
    ["claude code examples", "ai sdk agents", "multi agent orchestration",
     "context engineering", "ai devops skills", "security agent skills",
     "data agent skills", "design agent skills", "writing agent skills",
     "devops automation skills", "testing agent skills", "code review agent"],
]
TOPIC_SETS = [
    ["claude-skills", "agent-skills", "claude-code", "claude-code-plugin",
     "claude-plugins", "skills", "ai-agents", "mcp", "agentic",
     "claude", "llm-agents", "prompt-engineering"],
    ["subagents", "claude-subagents", "ai-workflows", "agent-framework",
     "llmops", "ai-tools", "cursor-rules", "copilot", "rag",
     "ai-coding", "codex", "gemini-cli"],
    ["anthropic", "openai", "agents-md", "context-engineering",
     "agent-memory", "vector-database", "llm-eval", "guardrails",
     "ai-security", "prompt-library", "developer-tools", "cli-tools"],
    ["autonomous-agents", "multi-agent", "agent-orchestration", "tool-calling",
     "function-calling", "ai-automation", "workflow-automation",
     "devops", "testing", "code-review", "documentation", "design-systems"],
]
CODE_QUERIES = [
    "filename:SKILL.md",
    "filename:SKILL.md path:skills",
    "filename:SKILL.md path:.claude",
    "filename:SKILL.md path:plugins",
    "filename:SKILL.md language:Markdown",
    "filename:SKILL.md NOT path:node_modules",
    "filename:SKILL.md path:agents",
    "filename:SKILL.md size:>200",
    "filename:SKILL.md path:skills/skills",
    "filename:SKILL.md path:agent-skills",
    "filename:SKILL.md path:marketplace",
    "filename:SKILL.md path:collection",
]


def gh(args, timeout=120):
    try:
        p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=timeout)
        s = p.stdout.strip()
        return json.loads(s) if s else []
    except Exception as e:
        print("  gh err:", str(e)[:80], flush=True)
        return []


def load():
    try:
        return json.load(open(REG))
    except Exception:
        return {"repos": {}, "updated": None}


def cur_wave():
    for i, a in enumerate(sys.argv):
        if a == "--wave" and i + 1 < len(sys.argv):
            return int(sys.argv[i + 1])
    try:
        return int(open(WAVE_F).read().strip())
    except Exception:
        return 0


def save_wave(n):
    try:
        open(WAVE_F, "w").write(str(n))
    except Exception:
        pass


def main():
    w = cur_wave()
    rq = REPO_SETS[w % len(REPO_SETS)]
    tq = TOPIC_SETS[w % len(TOPIC_SETS)]
    cq = CODE_QUERIES[w % len(CODE_QUERIES):] + CODE_QUERIES[:w % len(CODE_QUERIES)]

    reg = load()
    repos = reg["repos"]
    n0 = len(repos)
    found = {}

    print("[wave %d] [1/3] repo search (limit %d)..." % (w, LIMIT), flush=True)
    for q in rq:
        for r in gh(["search", "repos", q, "--limit", str(LIMIT), "--sort", "stars",
                     "--json", "fullName,stargazersCount,description"]):
            fn = r["fullName"]
            found[fn.lower()] = {"full_name": fn, "stars": r.get("stargazersCount") or 0,
                                 "desc": (r.get("description") or "")[:120]}
    for t in tq:
        for r in gh(["search", "repos", "--topic=" + t, "--limit", str(LIMIT), "--sort", "stars",
                     "--json", "fullName,stargazersCount,description"]):
            fn = r["fullName"]
            found.setdefault(fn.lower(), {"full_name": fn, "stars": r.get("stargazersCount") or 0,
                                          "desc": (r.get("description") or "")[:120]})
    print("  -> %d repo dari search" % len(found), flush=True)

    print("[2/3] code search (filename:SKILL.md)...", flush=True)
    code_hits = 0
    for q in cq:
        items = gh(["search", "code", q, "--limit", "100", "--json", "repository"])
        for it in items:
            fn = it.get("repository", {}).get("nameWithOwner")
            if not fn:
                continue
            k = fn.lower()
            if k not in found:
                found[k] = {"full_name": fn, "stars": None, "desc": ""}
                code_hits += 1
        print("  %-45s +%d" % (q, len(items)), flush=True)
        time.sleep(7)  # code_search rate limit ~10/min
    print("  -> %d repo baru dari code search" % code_hits, flush=True)

    print("[3/3] ambil bintang untuk repo tanpa data...", flush=True)
    need = [v for v in found.values() if v.get("stars") is None]
    print("  %d repo perlu bintang" % len(need), flush=True)
    got = 0
    for v in need[:900]:
        try:
            p = subprocess.run(["gh", "api", "repos/" + v["full_name"],
                                "--jq", ".stargazers_count"],
                               capture_output=True, text=True, timeout=30)
            v["stars"] = int(p.stdout.strip() or 0)
            got += 1
        except Exception:
            v["stars"] = 0
    print("  -> %d bintang diambil" % got, flush=True)

    added = 0
    _dl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo-denylist.txt")
    deny = set(open(_dl).read().split()) if os.path.exists(_dl) else set()
    for k, v in found.items():
        if k in repos:
            continue
        if any(b in k or b in k.replace("/", "_") for b in deny):  # skip malware/crack repo
            continue
        if (v.get("stars") or 0) < MIN_STARS:
            continue
        repos[k] = {"full_name": v["full_name"], "stars": v["stars"],
                    "desc": v.get("desc", ""), "tags": ["discovered", "wave%d" % w],
                    "added": time.strftime("%Y-%m-%d")}
        added += 1
    reg["updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(reg, open(REG, "w"), indent=2, ensure_ascii=False)
    save_wave(w + 1)

    buckets = {">=1000": 0, "100-999": 0, "10-99": 0, "1-9": 0, "0": 0}
    for v in repos.values():
        s = v.get("stars", 0) or 0
        buckets[">=1000" if s >= 1000 else "100-999" if s >= 100 else
                "10-99" if s >= 10 else "1-9" if s >= 1 else "0"] += 1
    print("REGISTRY: %d -> %d (+%d baru)" % (n0, len(repos), added), flush=True)
    print("BUCKET:", buckets, flush=True)
    print("DONE wave=%d" % w, flush=True)


if __name__ == "__main__":
    main()
