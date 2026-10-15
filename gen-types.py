#!/usr/bin/env python3
"""gen-types.py — generator taksonomi tipe aset AI (skala besar, berbasis data).

Tujuan: katalog aset (prompt/agent/rule/memory/token-economy/…) punya BANYAK tipe
agar AI bisa memilih aset yang tepat. Taksonomi dibentuk dari 3 sumber:

  1. BASE    — tipe kurasi (yang sudah dipakai cap-crawler).
  2. COMBO   — DOMAIN × ARTIFACT (mis. security-checklist, api-design-doc).
  3. DATA    — segmen direktori nyata dari cap-catalog.json (muncul >= MIN_SEEN).

Output: ~/.agents/cap-types.json
  { "dir_segments": {segmen: tipe}, "file_stems": {stem: tipe}, "types": [...] }

cap-crawler.py memuat file ini sebagai FALLBACK classify (tipe kurasi tetap menang).
"""
import json, os, re, sqlite3
from collections import Counter
from pathlib import Path

AG = Path.home() / ".agents"
CATALOG = AG / "cap-catalog.json"
SKILLS_DB = AG / "skills-index.db"
MCP_CATALOG = AG / "mcp-catalog.json"
PLUGIN_DIRS = [Path.home() / ".codebuddy" / "plugins" / "cache", AG / "plugins"]
OUT = AG / "cap-types.json"
MIN_SEEN = int(os.environ.get("TYPES_MIN_SEEN", "5"))
MIN_SKILL_SEEN = int(os.environ.get("TYPES_MIN_SKILL_SEEN", "30"))
MIN_MCP_SEEN = int(os.environ.get("TYPES_MIN_MCP_SEEN", "4"))
MIN_PLUGIN_SEEN = int(os.environ.get("TYPES_MIN_PLUGIN_SEEN", "2"))

STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "that", "this", "when", "your",
    "you", "use", "using", "used", "skill", "skills", "claude", "code", "tool",
    "tools", "make", "makes", "made", "based", "via", "all", "any", "its", "out",
    "how", "why", "what", "new", "old", "get", "set", "run", "runs", "run",
    "build", "create", "creates", "generate", "generates", "custom", "simple",
    "advanced", "complete", "full", "system", "systems", "into", "than", "then",
    "also", "such", "each", "more", "most", "some", "only", "just", "very",
}

# ---- 1. BASE (tipe kurasi) ----
BASE = [
    "skills", "agents", "subagents", "commands", "hooks", "rules", "prompts",
    "system-prompts", "personas", "memory", "context", "plugins", "mcp-config",
    "copilot", "instructions", "agent-config", "workflows", "guardrails", "evals",
    "recipes", "checklists", "playbooks", "runbooks", "specs", "adr", "glossary",
    "cheatsheets", "templates", "snippets", "tools-schema", "knowledge", "style",
    "memory-system", "token-economy", "context-engineering", "compaction",
    "reasoning", "reflection", "metacognition", "few-shot", "rag",
    "knowledge-graph", "anti-slop", "rubrics", "model-routing", "prompt-optimization",
]

# ---- 2. COMBO: domain × artifact ----
DOMAINS = [
    "code", "testing", "docs", "api", "database", "ui", "ux", "security",
    "performance", "data", "ml", "llm", "cloud", "kubernetes", "ci-cd",
    "networking", "auth", "logging", "monitoring", "deployment", "mobile", "web",
    "frontend", "backend", "fullstack", "game", "audio", "video", "image", "text",
    "nlp", "vision", "robotics", "iot", "blockchain", "crypto", "fintech",
    "healthcare", "education", "legal", "hr", "sales", "marketing", "operations",
    "support", "research", "design", "product", "growth", "content", "seo", "ads",
    "ecommerce", "logistics", "manufacturing", "energy", "realestate", "travel",
    "food", "sports", "music", "film", "photography", "writing", "translation",
    "accessibility", "i18n", "refactoring", "debugging", "architecture",
    "microservices", "serverless", "edge", "embedded", "systems", "compilers",
    "distributed", "concurrency", "caching", "queues", "streaming", "etl",
    "analytics", "visualization", "reporting", "automation", "orchestration",
    "agents", "prompting", "memory", "context", "token", "evaluation",
    "guardrails", "reasoning", "planning", "tooling", "cli", "devtools", "ide",
    "git", "versioning", "releases", "packaging", "dependencies", "supply-chain",
    "compliance", "governance", "auditing", "risk", "incident", "recovery",
    "backup", "migration", "scaling", "cost", "green", "quantum", "ar-vr",
    "spatial", "gis", "simulation", "gaming", "rl", "genomics", "bio",
    "chemistry", "physics", "math", "statistics", "economics", "psychology",
    "sociology", "philosophy", "ethics", "onboarding", "handoff", "retrospective",
    "interview", "career", "resume", "portfolio", "branding", "pricing", "billing",
    "subscription", "fraud", "kyc", "payments", "wallet", "defi", "nft", "dao",
    "identity", "privacy", "encryption", "zero-trust", "forensics", "malware",
    "pentest", "threat-model", "vuln", "patch", "hardening", "firewall", "vpn",
    "cdn", "dns", "loadbalancer", "gateway", "mesh", "service-mesh", "observability",
    "tracing", "metrics", "alerts", "slo", "sla", "runbook", "chaos", "dr",
    "multicloud", "hybrid", "onprem", "vm", "container", "registry", "helm",
    "terraform", "ansible", "pulumi", "iac", "gitops", "argocd", "flux", "jenkins",
    "github-actions", "gitlab-ci", "circleci", "buildkite", "tekton", "spinnaker",
]
ARTIFACTS = [
    "rules", "guide", "checklist", "template", "playbook", "runbook", "prompt",
    "persona", "rubric", "spec", "adr", "glossary", "cheatsheet", "recipe",
    "workflow", "policy", "standard", "pattern", "antipattern", "faq", "tutorial",
    "snippet", "config", "schema", "matrix", "roadmap", "plan", "review", "audit",
    "report", "brief", "memo", "contract", "sop", "kpi", "metric", "dashboard",
    "budget", "forecast", "model", "dataset", "pipeline", "migration", "rollback",
    "incident", "postmortem", "testplan", "testcase", "benchmark", "profile",
    "trace", "diagram", "wireframe", "mockup", "prototype", "proposal", "rfc",
    "design-doc", "handbook", "manifesto", "charter", "okr", "strategy", "analysis",
    "assessment", "survey", "questionnaire", "flashcard", "curriculum", "syllabus",
    "lesson", "exercise", "case-study", "whitepaper", "cookbook", "journal",
    "logbook", "decision-log", "runlist", "matrices", "catalogs", "registry",
    "manifest", "blueprint", "framework", "toolkit", "starter", "boilerplate",
    "scaffold", "sandbox", "lab", "workshop", "training", "certification",
]

GENERIC = {
    "src", "docs", "test", "tests", "dist", "build", "node_modules", "vendor",
    "packages", "components", "app", "web", "cli", "lib", "libs", "assets",
    "public", "static", "examples", "example", "demo", "tmp", "temp", "cache",
    "bin", "obj", "out", "target", "coverage", "fixtures", "mocks", "utils",
    "helpers", "types", "interfaces", "constants", "config", "configs", "www",
    "content", "images", "img", "css", "js", "ts", "json", "yaml", "yml",
}


def skills_terms():
    """Sumber 4: tipe dari SKILL NYATA (kategori + token nama skill)."""
    terms = Counter()
    if not SKILLS_DB.exists():
        return terms
    try:
        conn = sqlite3.connect(SKILLS_DB)
        for cat, cnt in conn.execute("select category, count(*) from skills "
                                     "where category<>'' group by category"):
            if cat:
                terms[cat.lower()] += 1000          # kategori = tipe kuat
        for (name,) in conn.execute("select name from skills"):
            for tok in re.split(r"[-_ .]+", (name or "").lower()):
                if 3 <= len(tok) <= 28 and tok.isalpha() and tok not in STOPWORDS:
                    terms[tok] += 1
        conn.close()
    except Exception as e:
        print("  skills err:", str(e)[:60])
    return terms


def mcp_terms():
    """Sumber 5: tipe dari MCP NYATA (nama + deskripsi mcp-catalog.json)."""
    terms = Counter()
    if not MCP_CATALOG.exists():
        return terms
    try:
        for m in json.loads(MCP_CATALOG.read_text()):
            for tok in re.split(r"[-_ ./]+", (m.get("name") or "").lower()):
                if 3 <= len(tok) <= 28 and tok.isalpha() and tok not in STOPWORDS:
                    terms[tok] += 3                       # nama MCP = sinyal kuat
            for tok in re.split(r"[^a-z0-9]+", (m.get("description") or "").lower()):
                if 4 <= len(tok) <= 28 and tok.isalpha() and tok not in STOPWORDS:
                    terms[tok] += 1
    except Exception as e:
        print("  mcp err:", str(e)[:60])
    return terms


def plugin_terms():
    """Sumber 6: tipe dari PLUGIN NYATA (cap-catalog + direktori plugin)."""
    terms = Counter()
    if CATALOG.exists():
        for e in json.loads(CATALOG.read_text()):
            if e.get("type") == "plugins":
                for tok in re.split(r"[-_ ./]+", (e.get("name") or "").lower()):
                    if 3 <= len(tok) <= 28 and tok.isalpha() and tok not in STOPWORDS:
                        terms[tok] += 1
    for base in PLUGIN_DIRS:
        if not base.exists():
            continue
        for d in base.rglob("*"):
            if d.is_dir() and d.parent.parent == base or d.parent == base:
                for tok in re.split(r"[-_ .]+", d.name.lower()):
                    if 3 <= len(tok) <= 28 and tok.isalpha() and tok not in STOPWORDS:
                        terms[tok] += 1
    return terms


def build():
    dir_seg, file_stem, types = {}, {}, set()

    for t in BASE:
        types.add(t)
        dir_seg.setdefault(t, t)
        dir_seg.setdefault(t.rstrip("s"), t)
        file_stem.setdefault(t, t)
        file_stem.setdefault(t.rstrip("s"), t)

    for d in DOMAINS:
        for a in ARTIFACTS:
            t = "%s-%s" % (d, a)
            types.add(t)
            dir_seg.setdefault(t, t)
            dir_seg.setdefault("%s_%s" % (d, a), t)
            dir_seg.setdefault("%s/%s" % (d, a), t)
            file_stem.setdefault(t, t)
            file_stem.setdefault("%s-%s" % (d, a.rstrip("s")), t)

    # ---- 3. DATA: segmen nyata dari katalog ----
    if CATALOG.exists():
        seg = Counter()
        for e in json.loads(CATALOG.read_text()):
            parts = [p.lower() for p in e.get("path", "").split("/") if p]
            for p in parts[:-1]:
                if 2 < len(p) < 40 and not p.startswith(".") and p not in GENERIC:
                    seg[p] += 1
        for s, c in seg.items():
            if c >= MIN_SEEN and re.fullmatch(r"[a-z0-9][a-z0-9_-]+", s):
                types.add(s)
                dir_seg.setdefault(s, s)
                file_stem.setdefault(s, s)
                file_stem.setdefault(s.rstrip("s"), s)

    # ---- 4. SKILLS: tipe dari skill nyata ----
    n_skill = 0
    for s, c in skills_terms().items():
        if c >= MIN_SKILL_SEEN and re.fullmatch(r"[a-z0-9][a-z0-9_-]+", s):
            types.add(s)
            dir_seg.setdefault(s, s)
            file_stem.setdefault(s, s)
            file_stem.setdefault(s.rstrip("s"), s)
            n_skill += 1

    # ---- 5. MCP: tipe dari MCP nyata ----
    n_mcp = 0
    for s, c in mcp_terms().items():
        if c >= MIN_MCP_SEEN and re.fullmatch(r"[a-z0-9][a-z0-9_-]+", s):
            types.add(s)
            dir_seg.setdefault(s, s)
            file_stem.setdefault(s, s)
            n_mcp += 1

    # ---- 6. PLUGINS: tipe dari plugin nyata ----
    n_plug = 0
    for s, c in plugin_terms().items():
        if c >= MIN_PLUGIN_SEEN and re.fullmatch(r"[a-z0-9][a-z0-9_-]+", s):
            types.add(s)
            dir_seg.setdefault(s, s)
            file_stem.setdefault(s, s)
            n_plug += 1

    OUT.write_text(json.dumps(
        {"dir_segments": dir_seg, "file_stems": file_stem,
         "types": sorted(types)}, ensure_ascii=False))
    print("TYPES: %d | dir_segments: %d | file_stems: %d | skill: %d | mcp: %d | plugin: %d"
          % (len(types), len(dir_seg), len(file_stem), n_skill, n_mcp, n_plug))


if __name__ == "__main__":
    build()
