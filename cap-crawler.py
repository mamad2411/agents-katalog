#!/usr/bin/env python3
"""cap-crawler.py — crawler aset AI dari komunitas (SELAIN skill/MCP biasa).

Sumber:
  A. GitHub TRENDING (repo baru/populer, sort stars + created:>recency)
     -> telusuri tree tiap repo (1 API call/repo) untuk panen aset berkualitas.
  B. gh search code per-tipe (prompts, agents, commands, hooks, rules, dst).

Tipe aset: prompts, agents, subagents, commands, hooks, rules, style,
plugins, mcp-config, memory, context, skills + 14 tipe pinter
(memory-system, token-economy, context-engineering, compaction,
reasoning, reflection, metacognition, few-shot, rag,
knowledge-graph, anti-slop, rubrics, model-routing,
prompt-optimization) + 10 tipe level-2 (planning, verification,
debate, tool-use, orchestration, long-context, hallucination,
constitutional, distillation, self-improve).

Prinsip:
  * Metadata saja di katalog (+ bintang repo, biar bisa ranking "paling rame").
  * Konten TIDAK diunduh massal; diambil on-demand oleh `cap_get` lalu di-cache.
  * Idle = nol beban.

Output:
  ~/.agents/cap-catalog.json   (id, type, repo, path, name, stars)
  ~/.agents/cap-index.db       (FTS5 tabel `cap`)
"""
import json, os, sqlite3, subprocess, sys, time
from collections import Counter
from pathlib import Path

AG = Path.home() / ".agents"
CATALOG = AG / "cap-catalog.json"
INDEX_DB = AG / "cap-index.db"
LIMIT = int(os.environ.get("CAP_LIMIT", "100"))
SLEEP = float(os.environ.get("CAP_SLEEP", "7"))
TREND_MAX = int(os.environ.get("CAP_TREND_MAX", "150"))
TREND_REPOS_F = AG / "trending-repos.json"

# taksonomi generated (gen-types.py) -> ribuan tipe berbasis data
TYPES_F = AG / "cap-types.json"
_DT, _FT = {}, {}
try:
    _T = json.loads(TYPES_F.read_text())
    _DT = _T.get("dir_segments", {})
    _FT = _T.get("file_stems", {})
except Exception:
    pass

# ---- A. Trending: repo skill/agent populer & baru ----
TREND_QUERIES = [
    "claude skills", "agent skills", "claude code plugin", "awesome claude",
    "subagents", "prompt library", "cursor rules", "agent framework",
    "multi-agent orchestration", "function calling agent", "agent verification",
    "self-improvement agent",
]
TREND_TOPICS = ["claude-skills", "agent-skills", "claude-code", "ai-agents",
                "prompt-engineering", "cursor-rules", "subagents",
                "multi-agent", "agent-orchestration", "tool-calling", "llm-eval"]

# pola path -> tipe aset (untuk panen tree trending)
def classify(path):
    p = path.lower()
    n = p.rsplit("/", 1)[-1]
    if n == "skill.md":
        return "skills"
    if "/.claude/agents/" in p or p.startswith("agents/") or "/subagents/" in p:
        return "agents"
    if "/.claude/commands/" in p or p.startswith("commands/"):
        return "commands"
    if "/.claude/hooks/" in p or n == "hooks.json":
        return "hooks"
    if "/.cursor/rules/" in p or p.endswith(".mdc") or "/rules/" in p:
        return "rules"
    if "/prompts/" in p or p.startswith("prompts/") or "/.github/prompts/" in p:
        return "prompts"
    if n in ("system-prompt.md", "system_prompt.md", "system-prompt.txt") or "/system-prompts/" in p:
        return "system-prompts"
    if "/personas/" in p or n.startswith("persona"):
        return "personas"
    if n in ("agents.md", "claude.md", ".cursorrules") or "/memory/" in p or n == "memory.md":
        return "memory" if ("/memory/" in p or n == "memory.md") else "context"
    if n == "copilot-instructions.md" or "/.github/copilot/" in p:
        return "copilot"
    if n == "instructions.md" or "/.github/instructions/" in p:
        return "instructions"
    if n in ("plugin.json",) or "/.claude-plugin/" in p:
        return "plugins"
    if n in ("mcp.json", "claude_desktop_config.json"):
        return "mcp-config"
    if n == "settings.json" and "/.claude" in p:
        return "agent-config"
    if "/.github/workflows/" in p and (n.endswith(".yml") or n.endswith(".yaml")):
        return "workflows"
    if "/guardrails/" in p or n == "guardrails.md":
        return "guardrails"
    if "/evals/" in p or "/evaluations/" in p or n == "eval.md":
        return "evals"
    if "/recipes/" in p or n == "recipe.md":
        return "recipes"
    if n == "checklist.md" or "/checklists/" in p:
        return "checklists"
    if n == "playbook.md" or "/playbooks/" in p:
        return "playbooks"
    if n == "runbook.md" or "/runbooks/" in p:
        return "runbooks"
    if n == "adr.md" or n.startswith("adr-") or "/adr/" in p:
        return "adr"
    if "/specs/" in p or n == "spec.md":
        return "specs"
    if n == "glossary.md" or "/glossary/" in p:
        return "glossary"
    if n == "cheatsheet.md" or "/cheatsheets/" in p:
        return "cheatsheets"
    if n.endswith(".template.md") or "/templates/" in p:
        return "templates"
    if n.endswith(".code-snippets") or "/snippets/" in p:
        return "snippets"
    if n == "tool-schema.json":
        return "tools-schema"
    if "/knowledge/" in p and n.endswith(".md"):
        return "knowledge"
    # --- tipe "AI lebih pinter / hemat token / memori" ---
    if "/memory-system" in p or n in ("memory-architecture.md", "memory-system.md", "memory-bank.md"):
        return "memory-system"
    if "/token" in p or n in ("token-budget.md", "token-economy.md", "token-guard.md") or "token-optim" in n:
        return "token-economy"
    if n in ("context.md", "context-engineering.md", "context-budget.md") or "/context-engineering/" in p:
        return "context-engineering"
    if n in ("compaction.md", "compact.md", "summarization.md") or "/compaction/" in p:
        return "compaction"
    if "/reasoning/" in p or n in ("reasoning.md", "chain-of-thought.md", "cot.md", "thinking.md"):
        return "reasoning"
    if "/reflection/" in p or n in ("reflection.md", "self-critique.md", "critique.md", "self-eval.md"):
        return "reflection"
    if "/metacognition/" in p or n in ("metacognition.md", "decomposition.md", "planning.md"):
        return "metacognition"
    if "/few-shot/" in p or "/exemplars/" in p:
        return "few-shot"
    if "/rag/" in p or n in ("rag.md", "retrieval.md"):
        return "rag"
    if "/knowledge-graph/" in p or n in ("knowledge-graph.md", "graph.md", "ontology.md"):
        return "knowledge-graph"
    if "/anti-slop/" in p or n in ("anti-slop.md", "quality.md", "quality-gate.md", "de-slop.md"):
        return "anti-slop"
    if "/rubrics/" in p or n in ("rubric.md", "rubrics.md", "grading.md", "scoring.md"):
        return "rubrics"
    if "/model-routing/" in p or n in ("routing.md", "router.md", "model-routing.md", "model-selection.md"):
        return "model-routing"
    if "/prompt-optim" in p or n in ("prompt-optimization.md", "optimize-prompt.md", "prompt-tuner.md"):
        return "prompt-optimization"
    # --- tipe level-2: planning/verifikasi/orkestrasi/tool-use (2026-10-18) ---
    if "/planning/" in p or n in ("task-planning.md", "task-decomposition.md", "plan-and-execute.md", "planner.md"):
        return "planning"
    if "/verification/" in p or n in ("self-check.md", "verify.md", "verification.md", "fact-check.md", "self-verify.md"):
        return "verification"
    if "/debate/" in p or n in ("multi-agent-debate.md", "debate.md", "critic.md", "adversarial.md"):
        return "debate"
    if "/tool-use/" in p or "/tool-calling/" in p or n in ("function-calling.md", "tool-calling.md", "tool-use.md", "function-calling-guide.md"):
        return "tool-use"
    if "/orchestration/" in p or n in ("orchestration.md", "swarm.md", "multi-agent.md", "multi-agent-orchestration.md", "coordinator.md"):
        return "orchestration"
    if "/long-context/" in p or n in ("long-context.md", "needle-haystack.md", "lost-in-middle.md"):
        return "long-context"
    if "/hallucination" in p or n in ("hallucination.md", "hallucination-mitigation.md", "grounding.md", "citation.md"):
        return "hallucination"
    if "/constitutional" in p or n in ("constitution.md", "constitutional-ai.md", "charter.md", "values.md"):
        return "constitutional"
    if "/distillation/" in p or n in ("distillation.md", "distill.md", "teacher-student.md"):
        return "distillation"
    if "/self-improve/" in p or n in ("self-improvement.md", "self-improve.md", "self-refine.md", "iterative-refinement.md"):
        return "self-improve"
    if "style" in n and n.endswith(".md"):
        return "style"
    # --- fallback: taksonomi generated (20k+ tipe, berbasis data) ---
    stem = n.rsplit(".", 1)[0] if "." in n else n
    t = _FT.get(stem) or _FT.get(n)
    if t:
        return t
    for seg in p.split("/")[:-1]:
        if seg in _DT:
            return _DT[seg]
    return None


TYPE_QUERIES = {
    "prompts":      ["path:prompts", "path:.github/prompts", "path:prompts extension:md"],
    "agents":       ["path:.claude/agents", "path:agents", "path:subagents"],
    "commands":     ["path:.claude/commands", "path:commands"],
    "hooks":        ["path:.claude/hooks", "filename:hooks.json"],
    "rules":        ["path:.cursor/rules", "extension:mdc"],
    "plugins":      ["filename:plugin.json", "path:.claude-plugin"],
    "mcp-config":   ["filename:mcp.json", "filename:claude_desktop_config.json"],
    "memory":       ["filename:MEMORY.md", "path:.claude/memory", "filename:memory.md"],
    "context":      ["filename:AGENTS.md", "filename:CLAUDE.md", "filename:.cursorrules"],
    "skills":       ["filename:SKILL.md"],
    # --- tipe tambahan (kelengkapan katalog) ---
    "system-prompts": ["filename:system-prompt.md", "filename:system_prompt.md", "path:system-prompts"],
    "personas":     ["path:personas", "filename:persona.md"],
    "copilot":      ["filename:copilot-instructions.md", "path:.github/copilot"],
    "instructions": ["filename:instructions.md", "path:.github/instructions"],
    "agent-config": ["filename:settings.json path:.claude", "path:.claude/settings"],
    "workflows":    ["path:.github/workflows extension:yml", "path:workflows extension:md"],
    "guardrails":   ["path:guardrails", "filename:guardrails.md"],
    "evals":        ["path:evals", "path:evaluations extension:md", "filename:eval.md"],
    "recipes":      ["path:recipes extension:md", "filename:recipe.md"],
    "checklists":   ["filename:checklist.md", "path:checklists"],
    "playbooks":    ["filename:playbook.md", "path:playbooks"],
    "runbooks":     ["filename:runbook.md", "path:runbooks"],
    "specs":        ["path:specs extension:md", "filename:spec.md"],
    "adr":          ["path:adr", "filename:adr.md"],
    "glossary":     ["filename:glossary.md", "path:glossary"],
    "cheatsheets":  ["filename:cheatsheet.md", "path:cheatsheets"],
    "templates":    ["path:templates extension:md", "filename:*.template.md"],
    "snippets":     ["path:snippets extension:md", "filename:*.code-snippets"],
    "tools-schema": ["filename:tool-schema.json", "path:tools extension:json"],
    "knowledge":    ["path:knowledge extension:md", "path:docs/prompts"],
    "style":        ["filename:style-guide.md", "path:style extension:md"],
    # --- tipe "AI lebih pinter / hemat token / memori" ---
    "memory-system":       ["filename:memory-architecture.md", "path:memory-systems", "filename:memory-bank.md"],
    "token-economy":       ["filename:token-budget.md", "path:token-economy", "filename:token-guard.md"],
    "context-engineering": ["filename:context.md", "path:context-engineering"],
    "compaction":          ["filename:compaction.md", "filename:compact.md", "filename:summarization.md"],
    "reasoning":           ["path:reasoning extension:md", "filename:reasoning.md", "filename:chain-of-thought.md"],
    "reflection":          ["path:reflection extension:md", "filename:self-critique.md", "filename:self-eval.md"],
    "metacognition":       ["path:metacognition", "filename:planning.md", "filename:decomposition.md"],
    "few-shot":            ["path:few-shot", "path:exemplars extension:md"],
    "rag":                 ["filename:rag.md", "path:rag extension:md", "filename:retrieval.md"],
    "knowledge-graph":     ["filename:knowledge-graph.md", "path:knowledge-graph"],
    "anti-slop":           ["path:anti-slop", "filename:anti-slop.md", "filename:quality-gate.md"],
    "rubrics":             ["path:rubrics", "filename:rubric.md", "filename:scoring.md"],
    "model-routing":       ["filename:routing.md", "path:model-routing", "filename:model-selection.md"],
    "prompt-optimization": ["filename:prompt-optimization.md", "path:prompt-optimization"],
    # --- tipe level-2 (2026-10-18) ---
    "planning":       ["path:planning extension:md", "filename:task-planning.md", "filename:task-decomposition.md"],
    "verification":   ["path:verification extension:md", "filename:self-check.md", "filename:verify.md"],
    "debate":         ["path:debate extension:md", "filename:multi-agent-debate.md", "filename:critic.md"],
    "tool-use":       ["path:tool-use extension:md", "filename:function-calling.md", "filename:tool-calling.md"],
    "orchestration":  ["path:orchestration extension:md", "filename:swarm.md", "filename:multi-agent.md"],
    "long-context":   ["filename:long-context.md", "path:long-context extension:md"],
    "hallucination":  ["filename:hallucination.md", "path:hallucination-mitigation", "filename:grounding.md"],
    "constitutional": ["filename:constitution.md", "path:constitutional-ai", "filename:charter.md"],
    "distillation":   ["path:distillation extension:md", "filename:distill.md"],
    "self-improve":   ["filename:self-improvement.md", "path:self-improve extension:md", "filename:self-refine.md"],
}


def gh_json(args, timeout=90):
    try:
        p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=timeout)
        s = p.stdout.strip()
        return json.loads(s) if s else []
    except Exception as e:
        print("  gh err:", str(e)[:70], flush=True)
        return []


def slugify(s):
    out = []
    for ch in s:
        out.append(ch if (ch.isalnum() or ch in "-_.") else "-")
    return "".join(out).strip("-.")[:120] or "item"


def collect_trending():
    """Repo skill/agent populer (bintang) + yang baru naik. Return {full: stars}."""
    repos = {}
    for q in TREND_QUERIES:
        for r in gh_json(["search", "repos", q, "--limit", "100", "--sort", "stars",
                          "--json", "fullName,stargazersCount"]):
            repos[r["fullName"]] = r.get("stargazersCount") or 0
    for t in TREND_TOPICS:
        for r in gh_json(["search", "repos", "--topic=" + t, "--limit", "100",
                          "--sort", "stars", "--json", "fullName,stargazersCount"]):
            repos[r["fullName"]] = r.get("stargazersCount") or 0
    # repo baru naik (proxy trending): dibuat dalam 12 bulan, sort stars
    for q in ["claude skills", "agent skills", "claude code"]:
        for r in gh_json(["search", "repos", q, "--limit", "100", "--sort", "stars",
                          "--created", ">2025-10-01", "--json", "fullName,stargazersCount"]):
            repos.setdefault(r["fullName"], r.get("stargazersCount") or 0)
    top = sorted(repos.items(), key=lambda kv: -kv[1])[:TREND_MAX]
    TREND_REPOS_F.write_text(json.dumps(dict(top), indent=1, ensure_ascii=False))
    return dict(top)


def gh_raw(args, timeout=60):
    """Jalankan gh, kembalikan stdout mentah (untuk --jq yang cetak baris)."""
    try:
        p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=timeout)
        return p.stdout or ""
    except Exception:
        return ""


def harvest_tree(repo, stars, entries):
    """Telusuri seluruh file repo (1 API call) -> panen aset yang cocok."""
    out = gh_raw(["api", "repos/%s/git/trees/HEAD?recursive=1" % repo,
                  "--jq", ".tree[].path"])
    paths = [l.strip() for l in out.splitlines() if l.strip()]
    n = 0
    for path in paths:
        typ = classify(path)
        if not typ:
            continue
        key = (repo.lower(), path.lower())
        if key in entries:
            continue
        name = path.rsplit("/", 1)[-1]
        name = name.rsplit(".", 1)[0] if "." in name else name
        entries[key] = {"id": slugify(typ + "--" + repo.replace("/", "-") + "--" + name),
                        "type": typ, "repo": repo, "path": path, "name": name,
                        "stars": stars}
        n += 1
    return n


def main():
    entries = {}
    trending = {}
    if "--no-trending" not in sys.argv:
        print("[A] trending repos...", flush=True)
        trending = collect_trending()
        print("  -> %d repo trending" % len(trending), flush=True)
        tot = 0
        for i, (repo, stars) in enumerate(trending.items(), 1):
            got = harvest_tree(repo, stars, entries)
            tot += got
            if got:
                print("  %-45s +%d (★%d)" % (repo, got, stars), flush=True)
        print("  -> %d aset dari trending" % tot, flush=True)

    print("[B] code search per-tipe...", flush=True)
    for typ, queries in TYPE_QUERIES.items():
        for q in queries:
            items = gh_json(["search", "code", q, "--limit", str(LIMIT),
                             "--json", "path,repository"])
            added = 0
            for it in items:
                repo = (it.get("repository") or {}).get("nameWithOwner")
                path = it.get("path")
                if not repo or not path:
                    continue
                key = (repo.lower(), path.lower())
                if key in entries:
                    continue
                name = path.rsplit("/", 1)[-1]
                name = name.rsplit(".", 1)[0] if "." in name else name
                entries[key] = {"id": slugify(typ + "--" + repo.replace("/", "-") + "--" + name),
                                "type": typ, "repo": repo, "path": path, "name": name,
                                "stars": trending.get(repo, 0)}
                added += 1
            print("  %-12s %-45s +%d" % (typ, q, added), flush=True)
            time.sleep(SLEEP)

    rows = sorted(entries.values(),
                  key=lambda e: (-(e.get("stars") or 0), e["type"], e["repo"], e["path"]))
    CATALOG.write_text(json.dumps(rows, indent=1, ensure_ascii=False))

    if INDEX_DB.exists():
        INDEX_DB.unlink()
    conn = sqlite3.connect(INDEX_DB)
    conn.execute("CREATE VIRTUAL TABLE cap USING fts5(name, type, repo, path, id, stars)")
    conn.executemany("INSERT INTO cap(name,type,repo,path,id,stars) VALUES(?,?,?,?,?,?)",
                     [(r["name"], r["type"], r["repo"], r["path"], r["id"], r.get("stars") or 0)
                      for r in rows])
    conn.commit()
    conn.close()

    c = Counter(r["type"] for r in rows)
    print("TOTAL %d aset -> %s" % (len(rows), dict(c)), flush=True)
    print("TRENDING repo tersimpan: %s" % TREND_REPOS_F.name, flush=True)
    print("DONE", flush=True)


def gc(days=30):
    store = AG / "cap-store"
    if not store.exists():
        print("cap-store kosong.")
        return
    cut = time.time() - days * 86400
    n = 0
    for p in store.rglob("*.md"):
        try:
            if p.stat().st_mtime < cut:
                p.unlink()
                n += 1
        except OSError:
            pass
    for d in sorted(store.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            try:
                d.rmdir()
            except OSError:
                pass
    print("GC: %d file cache dihapus (>%d hari)." % (n, days))


if __name__ == "__main__":
    if "--gc" in sys.argv:
        i = sys.argv.index("--gc")
        d = int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else 30
        gc(d)
    else:
        main()
