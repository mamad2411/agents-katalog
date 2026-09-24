#!/usr/bin/env python3
"""
Pecah STYLE-<KATEGORI>.md yang besar (>=300 skill) jadi beberapa
STYLE-<KATEGORI>-<SUBKATEGORI>.md, supaya AI gak harus baca file
raksasa (ribuan skill) buat nemu yang relevan.

Sumber data: file STYLE-*.md yang SUDAH ADA (bukan skills-index.db
langsung) supaya tidak drift dari baseline 26.731 yang sudah
diverifikasi. Aman dijalankan ulang (idempotent) — baca ulang parent
index kalau sudah pernah displit, generate ulang dari nol.

Invariant yang dijaga:
  - total entri di semua STYLE-<KATEGORI>.md (kategori, bukan
    cross-cutting) == total baris di skills-index.db (skills tabel).
  - total entri subkategori == total entri kategori aslinya (tidak
    ada yang hilang / dobel).
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

AGENTS = Path(__file__).resolve().parent

# ── util parsing ──

FULL_LIST_HEADER_STD = re.compile(r"^## SEMUA skill kategori ini")
ENTRY_STD = re.compile(r"^- (.+?) \[(curated|reference|junk)\] - (.*)$")

FULL_LIST_HEADER_DOCSPEC = re.compile(r"^## SEMUA skill dokumen/requirement")
ENTRY_DOCSPEC = re.compile(r"^- (.+?) \[(curated|reference|junk)/([a-z0-9-]+)\] - (.*)$")


def norm(s):
    return " " + re.sub(r"[-_/]", " ", s.lower()) + " "


def kw_hit(haystack, kw):
    return (" " + kw.replace("-", " ") + " ") in haystack


def bucket_for(name, desc, buckets, special=None):
    haystack = norm(name) + norm(desc)
    if special:
        for pred_name, fn in special:
            if fn(name, desc, haystack):
                return pred_name
    for bname, keywords, _desc in buckets:
        for kw in keywords:
            if kw_hit(haystack, kw):
                return bname
    return None  # caller assigns GENERAL-*


def parse_standard(path):
    """Return (curated_star_lines, full_entries) for a normal STYLE-<CAT>.md.
    full_entries: list of dict(name, tier, desc, path, raw)"""
    lines = path.read_text().splitlines()
    star_start = None
    full_start = None
    for i, l in enumerate(lines):
        if l.startswith("## Bintang curated") and star_start is None:
            star_start = i + 1
        if FULL_LIST_HEADER_STD.match(l):
            full_start = i + 1
            break
    star_lines = []
    if star_start is not None:
        for l in lines[star_start:full_start - 1 if full_start else None]:
            if l.startswith("- "):
                star_lines.append(l)
            elif l.startswith("##"):
                break

    entries = []
    if full_start is not None:
        for l in lines[full_start:]:
            if not l.startswith("- "):
                continue
            rest = l[2:]
            if " | " in rest:
                body, fpath = rest.rsplit(" | ", 1)
            else:
                body, fpath = rest, ""
            m = ENTRY_STD.match(body)
            if not m:
                # tolerate odd formatting, keep raw for output, no name parse
                entries.append(dict(name=body, tier="reference", desc="", path=fpath, raw=l))
                continue
            name, tier, desc = m.groups()
            entries.append(dict(name=name, tier=tier, desc=desc, path=fpath, raw=l))
    return star_lines, entries


def parse_docspec(path):
    lines = path.read_text().splitlines()
    star_start = None
    full_start = None
    for i, l in enumerate(lines):
        if l.startswith("## Bintang curated") and star_start is None:
            star_start = i + 1
        if FULL_LIST_HEADER_DOCSPEC.match(l):
            full_start = i + 1
            break
    star_lines = []
    if star_start is not None:
        for l in lines[star_start:full_start - 1 if full_start else None]:
            if l.startswith("- "):
                star_lines.append(l)
            elif l.startswith("##"):
                break

    entries = []
    if full_start is not None:
        for l in lines[full_start:]:
            if not l.startswith("- "):
                continue
            rest = l[2:]
            if " | " in rest:
                body, fpath = rest.rsplit(" | ", 1)
            else:
                body, fpath = rest, ""
            m = ENTRY_DOCSPEC.match(body)
            if not m:
                entries.append(dict(name=body, tier="reference", desc="", path=fpath, raw=l, origcat=""))
                continue
            name, tier, origcat, desc = m.groups()
            entries.append(dict(name=name, tier=tier, desc=desc, path=fpath, raw=l, origcat=origcat))
    return star_lines, entries


# ── taxonomies: (subcat_name, keywords, one-line description) ──

TAXONOMY = {
    "BACKEND-DEVELOPER": (
        [("SAAS-INTEGRATIONS-AUTOMATION", lambda name, desc, h: "rube mcp" in desc.lower() or "composio" in desc.lower())],
        [
            ("API-REST-GRAPHQL", ["api", "rest", "graphql", "grpc", "protobuf", "endpoint", "openapi", "swagger", "webhook"], "Desain & implementasi REST/GraphQL/gRPC API, OpenAPI/Swagger"),
            ("DATABASE-ORM", ["database", "sql", "postgres", "postgresql", "mysql", "mongo", "mongodb", "redis", "orm", "prisma", "drizzle", "schema", "migration", "dynamodb", "sqlite", "cassandra", "elasticsearch"], "Database, ORM, schema, migration, query optimization"),
            ("AUTH-SECURITY-BACKEND", ["auth", "oauth", "jwt", "rbac", "permission", "session", "saml", "sso", "authentication", "authorization", "encryption"], "Auth, OAuth, JWT, RBAC, session, encryption di backend"),
            ("MESSAGING-QUEUE-REALTIME", ["queue", "kafka", "rabbitmq", "pubsub", "websocket", "sse", "realtime", "streaming", "celery", "bullmq", "message broker"], "Message queue, pub/sub, websocket, realtime, event streaming"),
            ("MICROSERVICES-ARCHITECTURE", ["microservice", "service mesh", "distributed system", "saga", "cqrs", "event sourcing", "hexagonal architecture"], "Microservices, service mesh, CQRS, event sourcing"),
            ("CLOUD-DEPLOYMENT-BACKEND", ["aws", "azure", "gcp", "lambda", "serverless", "docker", "kubernetes", "terraform", "vercel", "cloudflare"], "Deploy backend ke cloud: AWS/Azure/GCP, serverless, container"),
            ("LANGUAGE-FRAMEWORKS-BACKEND", ["python", "django", "flask", "fastapi", "java", "spring", "dotnet", "csharp", "nodejs", "express", "nestjs", "golang", "rust", "php", "laravel", "ruby", "rails"], "Framework & bahasa backend: Python/Java/.NET/Node/Go/Rust/PHP/Ruby"),
            ("TESTING-BACKEND", ["test", "testing", "pytest", "tdd", "unit test", "integration test", "jest", "mocha"], "Unit test, integration test, TDD untuk backend"),
            ("AI-AGENT-MCP-BACKEND", ["mcp", "agent", "claude", "llm", "prompt", "openai", "anthropic", "gpt"], "Backend untuk AI agent, MCP server, LLM integration"),
            ("SAAS-INTEGRATIONS-AUTOMATION", [], "Integrasi SaaS/API pihak-3 otomatis via Rube MCP (Composio) — ratusan konektor tool"),
        ],
        "GENERAL-BACKEND",
    ),
    "DESIGNER": (
        None,
        [
            ("UI-UX-DESIGN", ["ui", "ux", "interface", "wireframe", "prototype", "figma", "mockup", "usability", "user research", "interaction design", "persona"], "UI/UX design, wireframe, prototyping, usability, Figma"),
            ("BRAND-IDENTITY-DESIGN", ["brand", "logo", "identity", "style guide", "brand voice", "brandkit", "brand guideline"], "Brand identity, logo, style guide, brand voice"),
            ("DESIGN-SYSTEMS-TOKENS", ["design system", "design token", "component library", "storybook", "atomic design"], "Design system, design token, component library"),
            ("SYSTEM-ARCHITECTURE-DESIGN", ["architecture", "system design", "c4 model", "design pattern", "adr", "ddd", "hexagonal", "cloud design pattern"], "Software/system architecture design, ADR, design pattern (bukan UI)"),
            ("API-DESIGN", ["api design", "api-design"], "Desain kontrak API (REST/GraphQL) — bukan implementasi"),
            ("DATA-VIZ-CHART-DESIGN", ["chart", "visualization", "d3", "dashboard", "data viz", "graph design"], "Desain visualisasi data, chart, dashboard"),
            ("PRESENTATION-DOCUMENT-DESIGN", ["slide", "deck", "presentation", "poster", "flyer", "canvas design", "infographic"], "Desain presentasi/slide, poster, dokumen visual"),
            ("MOTION-ANIMATION-DESIGN", ["animation", "motion design", "transition", "micro interaction"], "Motion design, animasi, micro-interaction"),
            ("GAME-GRAPHICS-DESIGN", ["game design", "shader", "texture", "3d render"], "Desain grafis/visual untuk game"),
        ],
        "GENERAL-DESIGNER",
    ),
    "DEVOPS-ENGINEER": (
        None,
        [
            ("CI-CD-PIPELINES", ["ci", "cd", "pipeline", "github actions", "gitlab ci", "jenkins", "circleci"], "CI/CD pipeline: GitHub Actions, GitLab CI, Jenkins"),
            ("KUBERNETES-CONTAINERS", ["kubernetes", "k8s", "docker", "container", "helm", "pod"], "Kubernetes, Docker, container orchestration"),
            ("CLOUD-AWS-GCP-AZURE", ["aws", "azure", "gcp", "lambda", "ec2", "s3 bucket"], "Cloud provider: AWS, GCP, Azure"),
            ("IAC-TERRAFORM-ANSIBLE", ["terraform", "ansible", "infrastructure as code", "pulumi", "cloudformation"], "Infrastructure as Code: Terraform, Ansible, Pulumi"),
            ("MONITORING-OBSERVABILITY", ["monitoring", "observability", "prometheus", "grafana", "logging", "tracing", "alert"], "Monitoring, observability, logging, alerting"),
            ("NETWORKING-INFRA", ["network", "dns", "load balancer", "vpn", "firewall", "reverse proxy", "nginx"], "Networking: DNS, load balancer, VPN, firewall, proxy"),
            ("LINUX-SYSADMIN", ["linux", "systemd", "ubuntu", "debian", "sysadmin"], "Linux sysadmin, systemd, shell scripting"),
            ("SECURITY-DEVOPS", ["security", "compliance", "audit", "secret management", "vault"], "Security & compliance dalam DevOps: secret, audit"),
        ],
        "GENERAL-DEVOPS",
    ),
    "FRONTEND-DEVELOPER": (
        None,
        [
            ("REACT-ECOSYSTEM", ["react", "jsx", "redux", "zustand", "nextjs", "next.js", "tanstack", "react query"], "React, Next.js, dan ekosistemnya"),
            ("VUE-ECOSYSTEM", ["vue", "nuxt", "pinia", "vuex"], "Vue.js, Nuxt, Pinia"),
            ("ANGULAR-SVELTE", ["angular", "svelte", "sveltekit"], "Angular & Svelte"),
            ("CSS-STYLING", ["css", "sass", "scss", "tailwind", "styled component", "postcss"], "CSS, Sass, Tailwind, styling"),
            ("STATE-MANAGEMENT-FRONTEND", ["state management", "mobx", "recoil", "xstate"], "State management frontend"),
            ("BUILD-TOOLING-FRONTEND", ["webpack", "vite", "esbuild", "rollup", "parcel", "babel"], "Build tooling: Webpack, Vite, esbuild"),
            ("WEB-PERFORMANCE-A11Y", ["performance", "accessibility", "wcag", "seo", "lighthouse", "a11y"], "Web performance, accessibility, SEO"),
            ("ANIMATION-INTERACTION-FRONTEND", ["gsap", "framer motion", "interaction design", "css animation"], "Animasi & interaksi web"),
            ("CURSOR-COPILOT-RULES", ["cursor rules", "copilot instructions", "cursorrules", "ai coding rules", "agent instructions"], "File aturan/instruksi AI coding agent (.cursorrules, copilot-instructions)"),
        ],
        "GENERAL-FRONTEND",
    ),
    "AI-ENGINEER": (
        None,
        [
            ("RAG-VECTOR-SEARCH", ["rag", "vector", "embedding", "retrieval", "semantic search"], "RAG, vector database, embedding, semantic search"),
            ("ML-TRAINING-FINETUNING", ["fine-tune", "finetune", "model training", "training dataset"], "ML/LLM training & fine-tuning"),
            ("MCP-TOOLING", ["mcp", "model context protocol"], "MCP server/tooling development"),
            ("AI-IMAGE-VIDEO-GEN", ["image generation", "video generation", "diffusion", "midjourney", "stable diffusion", "dall-e"], "AI image/video generation"),
            ("MLOPS-DEPLOYMENT", ["mlops", "model serving", "model deployment", "inference server"], "MLOps, model serving, deployment"),
            ("BLOCKCHAIN-CRYPTO-AI", ["blockchain", "crypto", "web3", "smart contract", "nft", "defi", "wallet"], "Blockchain/crypto/web3 (tercampur di kategori AI karena mining keyword)"),
            ("LLM-PROMPTING-AGENTS", ["prompt", "agent", "llm", "claude", "gpt", "chatgpt", "anthropic", "openai"], "LLM prompting, AI agent design & orchestration"),
        ],
        "GENERAL-AI",
    ),
    "GAME-DEVELOPER": (
        None,
        [
            ("GAME-ENGINES", ["unity", "unreal", "godot", "bevy", "pygame", "phaser", "babylon"], "Game engine: Unity, Unreal, Godot, dll"),
            ("GRAPHICS-SHADERS", ["shader", "glsl", "hlsl", "graphics rendering", "lighting"], "Grafis, shader, rendering"),
            ("GAME-PHYSICS-AI", ["physics engine", "collision", "pathfinding", "navmesh", "npc ai"], "Physics engine, pathfinding, NPC AI"),
            ("MULTIPLAYER-NETCODE", ["multiplayer", "netcode", "server authoritative", "matchmaking", "lobby"], "Multiplayer, netcode, matchmaking"),
            ("GAME-DESIGN-LEVEL", ["level design", "game design", "quest design", "narrative design"], "Game design, level design, narrative"),
        ],
        "GENERAL-GAME",
    ),
    "CREATIVE-PRODUCER": (
        None,
        [
            ("VIDEO-AUDIO-EDITING", ["video edit", "ffmpeg", "video render", "camera"], "Video/audio editing, ffmpeg, rendering"),
            ("IMAGE-GENERATION-AI-ART", ["image generation", "ai art", "midjourney", "stable diffusion", "diffusion"], "AI image generation / AI art"),
            ("PRESENTATIONS-SLIDES", ["slide", "deck", "keynote", "powerpoint", "pptx"], "Slide deck & presentasi (pptx/keynote)"),
            ("MUSIC-SOUND-DESIGN", ["music", "sound design", "midi", "synth", "voice", "text to speech", "tts"], "Musik, sound design, voice/TTS"),
            ("YOUTUBE-SOCIAL-CONTENT", ["youtube", "social media content", "caption", "subtitle"], "Konten YouTube/social media, caption/subtitle"),
        ],
        "GENERAL-CREATIVE",
    ),
    "QA-ENGINEER": (
        None,
        [
            ("E2E-TESTING", ["e2e", "playwright", "cypress", "selenium", "end to end test"], "E2E testing: Playwright, Cypress, Selenium"),
            ("UNIT-INTEGRATION-TESTING", ["unit test", "integration test", "jest", "pytest", "mocha", "tdd"], "Unit & integration testing"),
            ("TEST-AUTOMATION-FRAMEWORKS", ["test automation", "test framework"], "Test automation framework"),
            ("PERFORMANCE-LOAD-TESTING", ["performance test", "load test", "stress test", "benchmark"], "Performance/load/stress testing"),
            ("CODE-REVIEW-AUDIT", ["code review", "pr review", "reviewer", "audit", "linting"], "Code review, PR review, audit, linting"),
            ("SECURITY-TESTING-QA", ["security test", "vulnerability scan", "pentest"], "Security testing dalam QA"),
            ("MANUAL-QA-PROCESS", ["manual qa", "bug report", "test plan", "test case"], "Manual QA, test plan, bug report"),
        ],
        "GENERAL-QA",
    ),
    "DATA-SCIENTIST": (
        None,
        [
            ("ML-MODELING", ["classification", "regression", "machine learning model"], "ML modeling: classification, regression"),
            ("DATA-ANALYSIS-STATS", ["data analysis", "statistics", "statistical"], "Data analysis & statistik"),
            ("DATA-VISUALIZATION-DS", ["visualization", "chart", "plot", "dashboard"], "Data visualization"),
            ("NLP-CV", ["nlp", "computer vision", "text classification", "image classification"], "NLP & computer vision"),
            ("LLM-AGENT-DATA", ["llm", "agent", "gpt", "prompt", "eval"], "LLM/agent tooling dalam konteks data science"),
        ],
        "GENERAL-DATA-SCIENCE",
    ),
    "SECURITY-SPECIALIST": (
        None,
        [
            ("APPSEC-PENTEST", ["pentest", "penetration test", "vulnerability", "exploit", "appsec"], "Application security & penetration testing"),
            ("AUTH-IDENTITY-SECURITY", ["auth", "identity", "oauth", "sso", "iam"], "Auth, identity, IAM security"),
            ("CLOUD-SECURITY", ["cloud security", "aws security", "azure security", "container security"], "Cloud & container security"),
            ("COMPLIANCE-AUDIT-SECURITY", ["compliance", "audit", "governance", "gdpr", "soc2", "policy"], "Compliance, audit, governance"),
            ("INCIDENT-RESPONSE-THREAT", ["incident response", "threat", "malware", "threat hunt", "forensic"], "Incident response, threat hunting, malware"),
            ("SOCIAL-ENGINEERING-BOT", ["social engineering", "phishing", "bot detection"], "Social engineering, phishing, bot"),
        ],
        "GENERAL-SECURITY",
    ),
    "DOC-SPEC-PRD-BRD": (
        None,
        [
            ("PRD-PRODUCT-SPEC", ["prd", "product requirement", "product spec"], "PRD / product spec"),
            ("TECHNICAL-SPEC-RFC", ["technical spec", "rfc", "design doc", "architecture spec"], "Technical spec, RFC, design doc"),
            ("REQUIREMENTS-USER-STORIES", ["requirement", "user story", "acceptance criteria", "brd", "srs"], "Requirement, user story, BRD/SRS, acceptance criteria"),
            ("API-DOCS-SPEC", ["api doc", "api spec", "openapi", "swagger"], "API docs/spec"),
        ],
        "GENERAL-DOC-SPEC",
    ),
    "DEVTOOLS-ENGINEER": (
        None,
        [
            ("CLI-TOOLING", ["cli", "command line", "terminal tool"], "CLI tooling"),
            ("IDE-EDITOR-TOOLING", ["ide", "vscode", "jetbrains", "editor plugin", "extension"], "IDE/editor plugin & tooling"),
            ("BUILD-SYSTEMS-DEVTOOLS", ["build system", "bazel", "gradle", "package manager"], "Build system & package manager"),
            ("GIT-VERSION-CONTROL", ["git", "github", "commit", "version control", "pull request"], "Git, GitHub, version control"),
            ("DEBUGGING-PROFILING", ["debug", "profiling", "trace"], "Debugging & profiling"),
        ],
        "GENERAL-DEVTOOLS",
    ),
    "MOBILE-DEVELOPER": (
        None,
        [
            ("IOS-SWIFT", ["ios", "swift", "swiftui", "xcode", "uikit"], "iOS, Swift, SwiftUI, Xcode"),
            ("ANDROID-KOTLIN", ["android", "kotlin", "jetpack", "gradle"], "Android, Kotlin, Jetpack"),
            ("CROSSPLATFORM-MOBILE", ["flutter", "react native", "expo", "ionic", "capacitor"], "Cross-platform: Flutter, React Native, Expo"),
            ("MOBILE-CI-DISTRIBUTION", ["fastlane", "app store", "play store", "firebase", "distribution"], "Mobile CI/CD & distribusi (Fastlane, App/Play Store)"),
        ],
        "GENERAL-MOBILE",
    ),
    "TECH-WRITER": (
        None,
        [
            ("API-REFERENCE-DOCS", ["api doc", "api reference", "openapi", "swagger"], "API reference docs"),
            ("TUTORIALS-GUIDES", ["tutorial", "guide", "how to", "onboarding"], "Tutorial, guide, onboarding docs"),
            ("README-DOCS", ["readme", "markdown"], "README & markdown docs"),
            ("CHANGELOG-RELEASE-NOTES", ["changelog", "release notes", "versioning"], "Changelog & release notes"),
            ("EDITORIAL-STYLE-WRITING", ["editorial", "style guide", "brand voice", "content writing"], "Editorial, style guide, brand voice"),
        ],
        "GENERAL-TECH-WRITER",
    ),
    "DATA-ENGINEER": (
        None,
        [
            ("ETL-PIPELINES", ["etl", "data pipeline", "ingestion"], "ETL pipeline & data ingestion"),
            ("DATA-WAREHOUSE-LAKEHOUSE", ["warehouse", "lakehouse", "snowflake", "bigquery", "redshift"], "Data warehouse & lakehouse"),
            ("STREAMING-DATA", ["streaming", "kafka", "flink", "spark streaming"], "Streaming data"),
            ("ORCHESTRATION-AIRFLOW", ["airflow", "orchestration", "dag", "orchestrator"], "Orchestration: Airflow, DAG"),
            ("RESEARCH-AGENT-EXTRACTION", ["research agent", "subagent", "web search", "scraping", "crawler", "extraction"], "Research agent, web scraping/extraction pipeline"),
        ],
        "GENERAL-DATA-ENGINEER",
    ),
    "PRODUCT-MANAGER": (
        None,
        [
            ("ROADMAP-STRATEGY", ["roadmap", "strategy", "prioritization", "okr"], "Roadmap, strategy, prioritization, OKR"),
            ("USER-RESEARCH-FEEDBACK", ["user research", "feedback", "survey", "interview"], "User research, feedback, survey"),
            ("METRICS-ANALYTICS-PM", ["metrics", "analytics", "kpi"], "Metrics, analytics, KPI"),
            ("PRD-SPEC-WRITING-PM", ["prd", "spec", "specification", "bmad", "speckit"], "PRD/spec writing untuk PM"),
            ("MARKETING-GTM", ["marketing", "go to market", "gtm", "competitive", "positioning"], "Marketing, go-to-market, competitive analysis"),
            ("STAKEHOLDER-COMMS", ["stakeholder", "communication plan"], "Stakeholder communication"),
        ],
        "GENERAL-PM",
    ),
}

DOCSPEC_KEY = "DOC-SPEC-PRD-BRD"


def fmt_star_line_from_entry(e):
    return f"- {e['name']} - {e['desc']}"


def build_subcat_content(cat_slug, cat_label, subcat_name, entries, desc):
    n = len(entries)
    lines = []
    lines.append(f"# STYLE {cat_label} - {subcat_name} ({n} skill)")
    lines.append("")
    lines.append(f"> Sub-kategori dari **{cat_slug}**. {desc}. Untuk AI: bintang curated di bawah adalah default. Butuh varian lain -> skill_search / langsung skill_load dari daftar. JANGAN hanya pakai bintang.")
    lines.append("")
    curated = [e for e in entries if e["tier"] == "curated"]
    lines.append(f"## Bintang curated ({len(curated)}) - baca sebagai default")
    for e in curated:
        lines.append(fmt_star_line_from_entry(e))
    lines.append("")
    lines.append(f"## SEMUA skill sub-kategori ini ({n})")
    for e in entries:
        lines.append(e["raw"])
    lines.append("")
    return "\n".join(lines)


def build_parent_index(cat_label, total_n, instr_line, orig_star_lines, subcat_results):
    lines = []
    lines.append(f"# STYLE {cat_label} ({total_n} skill)")
    lines.append("")
    lines.append(instr_line)
    lines.append("")
    top_star = orig_star_lines[:15]
    lines.append(f"## Bintang curated teratas ({len(top_star)} dari total, lihat sub-kategori untuk selengkapnya)")
    lines.extend(top_star)
    lines.append("")
    lines.append(f"## File ini dipecah jadi {len(subcat_results)} sub-kategori (total tetap {total_n})")
    lines.append("")
    lines.append("| Sub-kategori | Skill | Isi |")
    lines.append("|---|---|---|")
    for subname, entries, desc in subcat_results:
        fname = f"STYLE-{cat_label}-{subname}.md"
        lines.append(f"| `{fname}` | {len(entries)} | {desc} |")
    lines.append("")
    return "\n".join(lines)


SPLIT_DONE_MARKER = "lihat sub-kategori di bawah sesuai kebutuhan"


def process_category(cat_label, filename, is_docspec=False):
    special, buckets, general_name = TAXONOMY[cat_label]
    path = AGENTS / filename
    if SPLIT_DONE_MARKER in path.read_text():
        print(f"{cat_label}: SUDAH DISPLIT — dilewati (idempotent)")
        return None, None
    if is_docspec:
        star_lines, entries = parse_docspec(path)
    else:
        star_lines, entries = parse_standard(path)

    total_n = len(entries)
    buckets_out = defaultdict(list)
    for e in entries:
        b = bucket_for(e["name"], e["desc"], buckets, special)
        if b is None:
            b = general_name
        buckets_out[b].append(e)
    # Pecah GENERAL-* yang membengkak jadi shard alfabetis (deterministik, tanpa pola risiko)
    if general_name in buckets_out and len(buckets_out[general_name]) > 400:
        big = buckets_out.pop(general_name)
        shards = {}
        for e in big:
            c = (e["name"][:1] if e["name"] else '#').upper()
            if 'A' <= c <= 'D': s = general_name + '-A-D'
            elif 'E' <= c <= 'H': s = general_name + '-E-H'
            elif 'I' <= c <= 'L': s = general_name + '-I-L'
            elif 'M' <= c <= 'P': s = general_name + '-M-P'
            elif 'Q' <= c <= 'T': s = general_name + '-Q-T'
            else: s = general_name + '-U-Z'
            shards.setdefault(s, []).append(e)
        for s in sorted(shards):
            buckets_out[s] = shards[s]

    # stable order: taxonomy order first, then general shards (atau general utuh bila kecil)
    order = [b[0] for b in buckets] + sorted(
        [k for k in buckets_out if k == general_name or k.startswith(general_name + '-')])
    if special is not None:
        order = ["SAAS-INTEGRATIONS-AUTOMATION"] + [b[0] for b in buckets if b[0] != "SAAS-INTEGRATIONS-AUTOMATION"] + [general_name]
    desc_map = {b[0]: b[2] for b in buckets}
    desc_map[general_name] = f"Skill {cat_label.lower()} lain yang tidak masuk sub-kategori spesifik di atas"

    subcat_results = []
    for name in order:
        if name in buckets_out:
            subcat_results.append((name, buckets_out[name], desc_map.get(name, "")))
    # any leftover bucket names not in `order` (shouldn't happen) appended
    for name, ents in buckets_out.items():
        if name not in [r[0] for r in subcat_results]:
            subcat_results.append((name, ents, desc_map.get(name, "")))

    # write subcat files
    for subname, ents, desc in subcat_results:
        content = build_subcat_content(cat_label, cat_label, subname, ents, desc)
        outpath = AGENTS / f"STYLE-{cat_label}-{subname}.md"
        outpath.write_text(content)

    # rewrite parent index
    if is_docspec:
        instr_line = "> Untuk AI: tugas bikin/dokumen PRD, BRD, SRS, spec, requirement, user story, acceptance criteria -> lihat sub-kategori di bawah, atau skill_search."
    else:
        instr_line = f"> Untuk AI: tugas kategori **{cat_label.lower()}** -> lihat sub-kategori di bawah sesuai kebutuhan, atau skill_search / skill_load langsung. JANGAN cuma baca bintang teratas."
    parent_content = build_parent_index(cat_label, total_n, instr_line, star_lines, subcat_results)
    (AGENTS / filename).write_text(parent_content)

    return total_n, subcat_results


def main():
    results = {}
    for cat_label, filename in [
        ("BACKEND-DEVELOPER", "STYLE-BACKEND-DEVELOPER.md"),
        ("DESIGNER", "STYLE-DESIGNER.md"),
        ("DEVOPS-ENGINEER", "STYLE-DEVOPS-ENGINEER.md"),
        ("FRONTEND-DEVELOPER", "STYLE-FRONTEND-DEVELOPER.md"),
        ("AI-ENGINEER", "STYLE-AI-ENGINEER.md"),
        ("GAME-DEVELOPER", "STYLE-GAME-DEVELOPER.md"),
        ("CREATIVE-PRODUCER", "STYLE-CREATIVE-PRODUCER.md"),
        ("QA-ENGINEER", "STYLE-QA-ENGINEER.md"),
        ("DATA-SCIENTIST", "STYLE-DATA-SCIENTIST.md"),
        ("SECURITY-SPECIALIST", "STYLE-SECURITY-SPECIALIST.md"),
        ("DEVTOOLS-ENGINEER", "STYLE-DEVTOOLS-ENGINEER.md"),
        ("MOBILE-DEVELOPER", "STYLE-MOBILE-DEVELOPER.md"),
        ("TECH-WRITER", "STYLE-TECH-WRITER.md"),
        ("DATA-ENGINEER", "STYLE-DATA-ENGINEER.md"),
        ("PRODUCT-MANAGER", "STYLE-PRODUCT-MANAGER.md"),
    ]:
        n, subs = process_category(cat_label, filename)
        results[cat_label] = (n, subs)

    # docspec special
    n, subs = process_category(DOCSPEC_KEY, "STYLE-DOC-SPEC-PRD-BRD.md", is_docspec=True)
    results[DOCSPEC_KEY] = (n, subs)

    results = {k: v for k, v in results.items() if v[0] is not None}
    print("\n=== HASIL SPLIT ===")
    for cat, (n, subs) in results.items():
        s = sum(len(e) for _, e, _ in subs)
        status = "OK" if s == n else f"MISMATCH ({s} != {n})"
        print(f"{cat}: total={n} sub={len(subs)} sum_sub={s} [{status}]")
        for name, ents, _ in subs:
            pct = 100 * len(ents) / n if n else 0
            flag = " <== catchall besar" if name.startswith("GENERAL-") and pct > 35 else ""
            print(f"    {name}: {len(ents)} ({pct:.1f}%){flag}")


if __name__ == "__main__":
    main()
