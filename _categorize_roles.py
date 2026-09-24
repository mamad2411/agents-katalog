#!/usr/bin/env python3
"""
Categorize all .agents skills into agency roles.
Outputs role-skill-map.json with role → [skill names] mapping.
"""
import os, json, re
from collections import defaultdict

HOME = os.path.expanduser("~")
AGENTS = os.path.join(HOME, ".agents")
EXPANDED = os.path.join(AGENTS, "skills-expanded")
CUSTOM = os.path.join(AGENTS, "skills")

# ── Agency Role Taxonomy ──
# Each role has: keywords (to match in skill names), description
# Priority order matters — first match wins. More specific roles first.
ROLES = {
    "designer": {
        "keywords": ["design", "ui-design", "ux-design", "figma", "sketch-app", "adobe-illustrator", "adobe-photoshop", "canva", "framer", "principle-design", "protopie", "motion-design", "typography", "color-palette", "color-scheme", "theme-design", "dark-mode", "light-mode", "brand", "logo", "identity", "brand-guidelines", "style-guide", "design-token", "design-system", "wireframe", "mockup", "persona", "user-research", "usability", "accessibility-design", "a11y-design", "responsive-design", "mobile-first", "grid-layout", "spacing", "icon-set", "illustration", "image-edit", "gradient-design", "shadow", "border-radius", "glassmorphism", "neumorphism", "skeuomorphism", "flat-design", "material-design", "fluent-design", "carbon-design", "figma-plugin", "figma-to-code", "design-review", "design-audit", "design-handoff", "zeplin", "invision", "marvel-app", "flinto", "designops", "creative-direction", "visual", "artboard", "component-library-weaver", "brand-identity"],
        "desc": "UI/UX, brand, design systems, Figma, motion, accessibility"
    },
    "creative-producer": {
        "keywords": ["video", "video-gen", "ai-video", "ai-music", "audio", "music", "sound", "podcast", "voice", "tts", "text-to-speech", "speech", "whisper", "transcribe", "transcription", "subtitle", "caption", "render", "rendering", "blender", "may", "3d-model", "3d-render", "cgi", "vfx-art", "sfx", "video-edit", "film", "cinema", "animation-video", "motion-graphics", "after-effects", "premiere", "davinci", "ffmpeg", "multimedia", "slideshow", "presentation", "pptx", "powerpoint", "slides", "keynote", "infographic", "poster", "flyer", "brochure", "album", "album-cover", "beat", "midi", "synth", "wav", "mp3", "aac", "transcode", "stream", "livestream", "broadcast", "camera", "lens", "photography", "photo-edit", "image-gen", "ai-image", "midjourney", "stable-diffusion", "dall-e", "dalle", "diffusion-art", "generative-art", "algorithmic-art", "pixel-art", "pixel", "sprite", "pixelart"],
        "desc": "Video, audio, music, image generation, presentations, creative media"
    },
    "game-developer": {
        "keywords": ["game", "godot", "unity", "unreal", "bevy", "pygame", "phaser", "babylon", "webgl-game", "shader", "glsl", "hlsl", "vfx-game", "particle", "physics-engine", "collision", "rigidbody", "raycast", "navmesh", "pathfind", "npc", "quest", "inventory", "dialogue", "save-game", "load-game", "scene-management", "prefab", "blueprint", "gdscript", "gdnative", "csharp-game", "ldtk", "tiled", "aseprite", "fbx", "gltf", "glb", "procedural-gen", "terrain", "lod", "culling", "render-pipeline", "deferred-render", "forward-render", "bloom", "ssao", "ssr", "motion-blur", "depth-of-field", "anti-alias", "msaa", "fxaa", "taa", "vsync", "framerate", "game-jam", "playable", "level-design", "game-mechanic", "gameplay", "multiplayer-game", "dedicated-server", "server-authoritative", "latency", "tick-rate", "netcode", "rollback", "prediction", "reconciliation", "steamworks", "itch", "godaddy"],
        "desc": "Game engines, 3D graphics, shaders, physics, game systems"
    },
    "frontend-developer": {
        "keywords": ["react", "vue", "angular", "svelte", "nextjs", "next.js", "nuxt", "nuxtjs", "remix", "astro", "sveltekit", "gatsby", "tailwind", "css", "sass", "scss", "less", "stylus", "postcss", "webpack", "vite", "esbuild", "swc", "rollup", "parcel", "frontend", "front-end", "ui-component", "component-library", "shadcn", "radix", "headless-ui", "htm", "html", "dom", "browser", "threejs", "three.js", "3dsvg", "gsap", "animation", "micro-interaction", "svg", "canvas", "chart", "d3", "plotly", "recharts", "victory", "nivo", "visx", "responsive", "accessibility", "a11y", "wcag", "aria", "typescript", "javascript", "js-frontend", "copilot-instructions", "cursor-rules", "design-system", "figma-to-code", "ui-design", "ux-design", "wireframe", "prototype", "storybook", "chromatic", "cosmos", "react-router", "tanstack", "react-query", "swr", "zustand", "redux", "mobx", "recoil", "jotai", "valtio", "xstate", "fsm", "state-machine"],
        "desc": "Frontend, UI components, design systems, web animation, accessibility"
    },
    "mobile-developer": {
        "keywords": ["android", "ios", "swift", "kotlin-mobile", "flutter", "react-native", "rn-mobile", "expo", "xcode", "android-studio", "gradle-mobile", "cocoapods", "fastlane", "app-store", "play-store", "mobile", "tablet", "phone", "wear-os", "apple-watch", "pwa", "cordova", "capacitor", "ionic", "jetpack", "compose-mobile", "swiftui", "uikit", "widget-mobile", "push-notification", "deep-link", "biometric", "keychain", "keystore", "proguard", "r8", "aab", "apk", "ipa", "crashlytics", "analytics-mobile", "adb", "espresso", "xcuitest", "detox", "maestro", "kmp", "kmm", "kotlin-multiplatform"],
        "desc": "iOS, Android, React Native, Flutter, mobile app development"
    },
    "backend-developer": {
        "keywords": ["api", "backend", "back-end", "server", "endpoint", "rest", "graphql", "grpc", "protobuf", "proto", "microservice", "micro-service", "lambda", "function", "controller", "middleware", "database", "csharp", "c-sharp", "dotnet", "aspnet", "async", "await", "task-parallel", "sql", "postgres", "postgresql", "mysql", "mongo", "mongodb", "redis", "dynamodb", "orm", "prisma", "drizzle", "sequelize", "typeorm", "migration", "schema", "query", "crud", "auth", "authentication", "oauth", "jwt", "session", "rbac", "authorization", "payment", "stripe", "webhook", "queue", "worker", "cron", "scheduler", "rate-limit", "pagination", "filtering", "sorting", "error-handling", "retry", "circuit-breaker", "rpc", "websocket", "sse", "realtime", "real-time", "integration", "sdk", "driver", "connector", "adapter", "wrapper", "client", "http", "request", "response", "handler", "listener", "pubsub", "event", "emitter", "hook", "callback", "middleware", "interceptor", "filter", "guard", "pipe", "validator", "dto", "mapper", "serializer", "deserializer"],
        "desc": "APIs, databases, auth, microservices, backend architecture"
    },
    "devops-engineer": {
        "keywords": ["docker", "kubernetes", "k8s", "helm", "terraform", "ansible", "puppet", "chef", "ci-cd", "ci/cd", "pipeline", "jenkins", "github-actions", "gitlab-ci", "circleci", "deploy", "deployment", "release", "rollback", "infrastructure", "infra", "cloud", "aws", "azure", "gcp", "firebase", "vercel", "netlify", "heroku", "digitalocean", "monitoring", "observability", "prometheus", "grafana", "datadog", "logging", "log", "alerting", "alert", "oncall", "sre", "incident", "health-check", "nginx", "ingress", "load-balanc", "dns", "cdn", "ssl", "tls", "certificate", "secret", "vault", "configmap", "namespace", "hpa", "autoscal", "airflow", "eks", "aks", "gke", "fargate", "ec2", "s3", "rds", "cloudformation", "pulumi", "argo", "istio", "envoy", "consul", "nomad", "docker-compose", "container", "pod", "kubectl", "kustomize", "skaffold", "devcontainer", "dev-container", "registry", "harbor", "acr", "ecr", "ghcr", "playbook", "devspace", "devops", "cloud-platform", "platform-engineer", "platform", "hosting", "serverless", "edge", "cdn-config"],
        "desc": "CI/CD, cloud, containers, infrastructure, monitoring, deployment"
    },
    "qa-engineer": {
        "keywords": ["test", "testing", "qa", "quality", "e2e", "unit-test", "integration-test", "snapshot", "mock", "stub", "fixture", "coverage", "lcov", "jest", "vitest", "playwright", "cypress", "selenium", "puppeteer", "mocha", "jasmine", "karma", "detox", "appium", "espresso", "xcuitest", "tdd", "bdd", "cucumber", "gherkin", "assert", "expect", "should", "flake", "deflake", "fuzz", "mutation-test", "load-test", "stress-test", "benchmark", "performance-test", "security-test", "penetration", "pentest", "owasp", "vulnerability", "scan", "sast", "dast", "iast", "scarif", "sarif", "lint", "eslint", "prettier", "biome", "ruff", "flake8", "mypy", "pylint", "type-check", "typecheck", "type-error", "code-review", "review", "pr-review", "adversarial-review", "audit", "code-audit", "quality-review", "test-quality", "flaky", "regression", "deflake", "tdd", "inspect", "inspector", "debugger", "debug", "troubleshoot", "diagnostic", "profiler", "profiling"],
        "desc": "Testing, code review, quality assurance, linting, security scanning"
    },
    "security-specialist": {
        "keywords": ["security", "secure", "vulnerability", "exploit", "ctf", "penetration", "pentest", "owasp", "cve", "cwe", "sast", "dast", "secret-scan", "secret-detection", "gitleaks", "trufflehog", "supply-chain", "sbom", "dependency-check", "dependabot", "renovate", "ransomware", "malware", "reverse-engineer", "reverse-engineering", "binary", "forensic", "incident-response", "threat", "threat-model", "zero-trust", "zero-day", "hardening", "hardened", "compliance", "gdpr", "hipaa", "pci", "soc2", "iso27001", "fedramp", "rbac", "abac", "access-control", "iam", "policy", "firewall", "waf", "ddos", "bot", "honeypot", "hunting", "living-off-the-land", "lotl", "credential", "phishing", "social-engineer", "crypto", "cryptography", "encryption", "hash", "signature", "pkcs", "x509", "cert", "tls", "mTLS", "oauth", "saml", "sso", "mfa", "2fa", "passkey", "webauthn", "keycloak", "auth0", "cognito", "vault", "secrets-management", "owasp-compliance", "guardrail", "safety-review", "red-team", "blue-team", "purple-team", "siem", "soc", "ir", "dfir"],
        "desc": "Security, compliance, cryptography, threat modeling, incident response"
    },
    "data-scientist": {
        "keywords": ["data", "ml", "machine-learning", "deep-learning", "neural", "transformer", "llm", "gpt", "bert", "embedding", "vector", "rag", "fine-tune", "fine-tuning", "training", "inference", "dataset", "pandas", "numpy", "scipy", "scikit", "sklearn", "tensorflow", "pytorch", "torch", "keras", "jupyter", "notebook", "matplotlib", "seaborn", "plotly", "visualization", "analytics", "statistic", "probability", "regression", "classification", "clustering", "nlp", "sentiment", "tokeniz", "ner", "computer-vision", "opencv", "yolo", "segmentation", "object-detection", "gan", "diffusion", "stable-diffusion", "feature-engineer", "feature-store", "model-registry", "model-card", "mlops", "experiment", "mlflow", "wandb", "hyperparameter", "optim", "gradient", "loss", "accuracy", "precision", "recall", "f1", "auc", "roc", "confusion-matrix", "anomaly-detect", "forecast", "time-series", "survival", "bayesian", "markov", "reinforcement", "rlhf", "benchmark", "eval", "analyzing-data", "anomaly", "data-analysis", "statistical", "model-eval", "prediction", "classifier"],
        "desc": "ML/AI, data analysis, model training, statistics, MLOps"
    },
    "data-engineer": {
        "keywords": ["etl", "pipeline-data", "data-pipeline", "ingest", "extract", "transform", "load", "elt", "dagster", "prefect", "luigi", "dbt", "spark", "databricks", "emr", "glue", "snowflake", "bigquery", "redshift", "athena", "presto", "trino", "kafka", "kinesis", "pubsub", "rabbitmq", "sqs", "sns", "eventbridge", "celery", "dramatiq", "rq", "bull", "sidekiq", "resque", "data-lake", "data-warehouse", "lakehouse", "delta-lake", "iceberg", "hudi", "parquet", "avro", "orc", "schema-registry", "data-governance", "lineage", "catalog", "data-quality", "data-validation", "great-expectations", "soda", "monte-carlo", "search", "index", "elasticsearch", "opensearch", "solr", "meilisearch", "typesense", "algolia"],
        "desc": "ETL, data pipelines, streaming, data lakes, search, data quality"
    },
    "ai-engineer": {
        "keywords": ["ai", "ai-agent", "agent", "llm", "prompt", "rag", "retrieval", "vector-store", "vector-db", "pinecone", "weaviate", "milvus", "qdrant", "chroma", "langchain", "llamaindex", "autogen", "crewai", "semantic-kernel", "prompt-engineer", "prompt-template", "system-prompt", "few-shot", "zero-shot", "chain-of-thought", "cot", "reasoning", "planning", "tool-use", "function-call", "mcp", "model-context-protocol", "openai", "anthropic", "gemini", "mistral", "falcon", "phi-model", "qwen", "deepseek", "groq", "together", "huggingface", "transformers", "diffusers", "accelerate", "peft", "lora", "qlora", "adapter", "quantiz", "gguf", "ggml", "onnx", "tensorrt", "vllm", "tgi", "triton", "inference-server", "model-server", "guardrail", "alignment", "dpo", "ppo", "preference", "constitution", "agent-eval", "agent-orchestrat", "agent-workflow", "multi-agent", "agentic", "skill-creator", "mcp-builder", "orchestrat", "agent-designer", "agent-architecture", "agent-browser", "agent-protocol", "agent-governance", "agent-observability", "agent-harness", "agent-self-eval", "agent-platform", "agentic"],
        "desc": "AI agents, LLMs, prompt engineering, RAG, MCP, model deployment"
    },
    "productivity-automator": {
        "keywords": ["gws", "google-workspace", "googleworkspace", "gmail", "gdrive", "google-drive", "google-sheets", "google-docs", "google-calendar", "google-slides", "google-forms", "calendar", "sheets", "slides", "forms", "meet", "chat-send", "keep", "tasks", "workflow", "automation", "zapier", "n8n", "make-com", "ifttt", "rpa", "macro", "scheduled-task", "cron-job", "email-automation", "sheet-automation", "form-automation", "lark", "feishu", "attendance", "minutes", "memo", "note-taking", "approval", "notion-automation", "obsidian-automation"],
        "desc": "Google Workspace, office automation, workflows, scheduling, productivity integrations"
    },
    "product-manager": {
        "keywords": ["product", "roadmap", "sprint", "agile", "scrum", "kanban", "jira", "linear", "backlog", "user-story", "story-point", "estimation", "planning", "priorit", "requirement", "spec", "specification", "prd", "brd", "frd", "use-case", "personas", "journey-map", "funnel", "retention", "churn", "engagement", "metrics", "kpi", "okr", "north-star", "a/b", "ab-test", "experiment", "feature-flag", "launch", "go-to-market", "gtm", "market", "competitor", "competitive", "research", "survey", "feedback", "interview", "usability", "discovery", "ideation", "workshop", "facilitat", "stakeholder", "demo", "release-notes", "changelog", "advisor", "ceo", "strategy", "strategic", "business", "bmad", "prd", "spec-doc", "market-analysis", "competitive-landscape", "market-research"],
        "desc": "Product strategy, agile, specs, user research, roadmaps, A/B testing"
    },
    "tech-writer": {
        "keywords": ["doc", "docs", "documentation", "readme", "wiki", "guide", "tutorial", "onboard", "instruction", "manual", "help", "faq", "changelog", "release-note", "api-reference", "reference-doc", "technical-writing", "tech-writing", "writing", "blog", "article", "content", "copy", "copywriting", "grammar", "spell", "proofread", "editor", "editing", "markdown", "mdx", "docusaurus", "gitbook", "mkdocs", "sphinx", "jekyll", "hugo", "notion", "confluence", "internal-comms", "comms", "communication", "announcement", "newsletter", "memo", "report", "summary", "translat", "localization", "l10n", "i18n", "linguistic", "language", "citation", "howto", "contributing", "conduct", "curriculum", "course", "freecodecamp", "free-courses", "education", "learning", "teaching", "academy", "lesson", "study"],
        "desc": "Documentation, content, localization, education, technical communication"
    },
    "blockchain-developer": {
        "keywords": ["blockchain", "web3", "solidity", "ethereum", "solana", "polygon", "avalanche", "cosmos", "near-protocol", "tezos", "cardano", "polkadot", "chainlink", "ipfs", "arweave", "filecoin", "nft", "defi", "swap", "liquidity", "yield", "staking", "farming", "vault", "oracle", "bridge", "cross-chain", "layer2", "l2", "rollup", "zksync", "arbitrum", "optimism", "base-chain", "metamask", "wallet", "hardhat", "foundry", "truffle", "ganache", "remix", "wagmi", "viem", "ethers", "web3.js", "rpc", "abi", "erc20", "erc721", "erc1155", "erc4626", "eip", "governance", "dao", "snapshot", "multisig", "gnosis", "safe", "slither", "mythril", "echidna", "gas-optim", "mev", "flashbot", "depin", "0g", "token", "smart-contract"],
        "desc": "Smart contracts, DeFi, NFT, Web3, blockchain protocols"
    },
    "devtools-engineer": {
        "keywords": ["cli", "command", "terminal", "shell", "bash", "zsh", "fish", "powershell", "make", "cmake", "just", "task-runner", "script", "automation", "generator", "scaffold", "template", "boilerplate", "starter", "starter-kit", "monorepo", "turborepo", "nx", "lerna", "pnpm", "yarn", "npm", "bun", "deno", "package", "publish", "semantic-release", "conventional-commit", "commit", "git", "github", "gitlab", "bitbucket", "gitea", "forgejo", "pull-request", "merge", "rebase", "cherry-pick", "bisect", "hook", "pre-commit", "husky", "lefthook", "lint-staged", "editorconfig", "git-hooks", "devcontainer", "dev-environment", "dotenv", "env", "config", "devtool", "tool", "tools", "utility", "util", "helper", "common", "shared", "lib", "library", "pkg", "module", "plugin", "extension", "addon", "add-on", "wrapper", "sdk", "binding", "native", "ffi", "wasm", "webassembly", "emscript", "assemblyscript", "wat", "wasi"],
        "desc": "CLI tools, build systems, package managers, git workflows, scaffolding"
    },
    "architect": {
        "keywords": ["architecture", "architect", "system-design", "design-pattern", "ddd", "domain-driven", "clean-arch", "hexagonal", "onion", "cqrs", "event-sourc", "microservice", "service-oriented", "soa", "event-driven", "adr", "architecture-decision", "system", "system-design", "scalable", "scalability", "distributed", "distributed-system", "consensus", "cap", "consistency", "availability", "partition", "eventual", "strong-consistency", "idempotent", "saga", "outbox", "inbox", "ddd", "aggregate", "value-object", "entity", "repository", "factory", "strategy", "observer", "decorator", "facade", "proxy", "command", "mediator", "memento", "visitor", "state", "template-method", "bridge", "composite", "flyweight", "iterator", "chain-of-responsibility"],
        "desc": "System design, architecture patterns, ADRs, distributed systems"
    },
    "fullstack-generalist": {
        "keywords": ["fullstack", "full-stack", "full stack", "web-app", "webapp", "web-application", "application", "app", "project", "create", "setup", "init", "bootstrap", "starter", "boilerplate", "stack", "framework", "laravel", "django", "flask", "fastapi", "rails", "spring", "spring-boot", "express", "nestjs", "fastify", "gin", "fiber", "actix", "rocket", "symfony", "codeigniter", "yii", "ember", "backbone", "meteor", "system-prompt", "create-an-ecommerce", "create-a", "create-an", "create-an-website", "create-an-cafe", "create-an-instagram", "setup-project", "app-builder", "appstore"],
        "desc": "Full-stack frameworks, project setup, general-purpose web development"
    },
    "analyst": {
        "keywords": ["analysis", "analyze", "analyzing", "analytic", "analytics", "metric", "dashboard", "report", "reporting", "bi", "business-intelligence", "competitive", "landscape", "market-analysis", "market-research", "trend", "insight", "kpi", "funnel", "cohort", "retention", "growth", "monetiz", "revenue", "cost", "price", "pricing", "comparison", "audit", "review", "assess", "assessment", "evaluat", "eval", "rating", "score", "scoring", "index", "rank", "benchmark", "measure", "observ", "track", "monitor", "scan", "survey", "sentiment", "social-listen", "brand-monitor"],
        "desc": "Analytics, business intelligence, market research, competitive analysis"
    },
    "educator": {
        "keywords": ["education", "educator", "teacher", "teaching", "learn", "learning", "course", "courses", "curriculum", "tutorial", "lesson", "lesson-plan", "study", "study-guide", "exam", "examination", "quiz", "test-prep", "flashcard", "anki", "spaced-repetition", "memorize", "memorization", "knowledge", "knowledge-base", "knowledge-graph", "flashcard", "freecodecamp", "free-courses", "coding-interview", "interview-prep", "leetcode", "hackerrank", "codewars", "exercism", "course-curriculum", "syllabus", "module-learn", "training", "workshop", "bootcamp", "onboard", "onboarding", "academy", "guide", "howto", "handbook", "manual"],
        "desc": "Education, courses, tutorials, interview prep, learning resources"
    }
}

def get_all_skills():
    skills = set()
    # Expanded catalog skills
    if os.path.isdir(EXPANDED):
        for name in os.listdir(EXPANDED):
            if os.path.isdir(os.path.join(EXPANDED, name)):
                skills.add(name)
    # Custom skills
    if os.path.isdir(CUSTOM):
        for name in os.listdir(CUSTOM):
            if os.path.isdir(os.path.join(CUSTOM, name)):
                skills.add(name)
    return skills

def normalize(name):
    """Lowercase, replace - and _ with space for keyword matching.
    Also strip tool-specific prefixes like --codebuddy-skills-, --codex-skills- etc."""
    n = name.lower()
    # Strip tool-specific skill path prefixes — extract the actual topic at the end
    # Pattern: repo-name--tool-skills-skill-name-skill -> skill-name
    for sep in ["--codebuddy-skills-", "--codex-skills-", "--cursor-skills-",
                "--gemini-skills-", "--claude-skills-", "--agents-skills-",
                "--codebuddy-skill-", "--codex-skill-", "--cursor-skill-",
                "--gemini-skill-", "--claude-skill-", "--agents-skill-"]:
        if sep in n:
            # Take the part after the last tool prefix
            parts = n.split(sep)
            if len(parts) > 1:
                n = parts[-1]
                break
    # Remove trailing -skill or skill suffix
    n = re.sub(r'[-_]?skill$', '', n)
    return n.replace("-", " ").replace("_", " ").strip()

def categorize(skills):
    role_map = defaultdict(list)
    uncategorized = []
    gh_repos = []
    tool_specific = []
    
    for skill in sorted(skills):
        norm = normalize(skill)
        matched = False
        
        # Special case: gh- prefix = GitHub repo reference
        if skill.startswith("gh-") or skill.startswith("gh_"):
            gh_repos.append(skill)
            continue
        
        # Special case: tool-specific prefixes (cursor-rules, codebuddy, codex, gemini, claude)
        # These are tool config files, not skills per se — but still categorize by content
        
        for role, info in ROLES.items():
            for kw in info["keywords"]:
                kw_norm = kw.lower().replace("-", " ").replace("_", " ")
                if kw_norm in norm:
                    role_map[role].append(skill)
                    matched = True
                    break
            if matched:
                break
        
        if not matched:
            uncategorized.append(skill)
    
    return role_map, uncategorized, gh_repos

def main():
    skills = get_all_skills()
    print(f"Total skills: {len(skills)}")
    
    role_map, uncategorized, gh_repos = categorize(skills)
    
    total_categorized = sum(len(v) for v in role_map.values())
    
    # Build output
    output = {
        "metadata": {
            "total_skills": len(skills),
            "total_categorized": total_categorized,
            "total_uncategorized": len(uncategorized),
            "total_gh_repos": len(gh_repos),
            "coverage_pct": round((total_categorized + len(gh_repos)) / len(skills) * 100, 1) if len(skills) > 0 else 0,
            "roles": len(ROLES),
            "agency_model": "Each role = a team member in the AI agency. Skills are assigned to the best-matching role."
        },
        "roles": {}
    }
    
    for role, info in sorted(ROLES.items()):
        skill_list = sorted(role_map.get(role, []))
        output["roles"][role] = {
            "description": info["desc"],
            "count": len(skill_list),
            "skills": skill_list
        }
        print(f"  {role}: {len(skill_list)} skills")
    
    output["gh_repos"] = {
        "count": len(gh_repos),
        "description": "GitHub repo references — cloned repos used as skill sources, not categorized by role",
        "repos": sorted(gh_repos)
    }
    
    output["uncategorized"] = {
        "count": len(uncategorized),
        "description": "Skills that didn't match any role keyword — candidates for new roles or keyword expansion",
        "skills": sorted(uncategorized)
    }
    
    print(f"\nCategorized: {total_categorized} ({output['metadata']['coverage_pct']}%)")
    print(f"GitHub repos: {len(gh_repos)}")
    print(f"Uncategorized: {len(uncategorized)}")
    
    # Save
    out_file = os.path.join(AGENTS, "role-skill-map.json")
    with open(out_file, "w") as f:
        json.dump(output, f, separators=(",", ":"))
    print(f"\nSaved to {out_file}")

if __name__ == "__main__":
    main()
