---
name: codebase-onboarding
description: Codebase onboarding methodology: dependency mapping, architecture discovery, key file identification, domain terminology extraction, first task identification, learning checklist, and knowledge gap tracking. Includes scripts for automated codebase analysis.
origin: AI Dev Kit
disable-model-invocation: false
---

# Codebase Onboarding

Systematic methodology for onboarding to an unfamiliar codebase: dependency mapping, architecture discovery, key file identification, domain terminology extraction, first task identification, learning checklist, knowledge gap tracking, and automated analysis scripts.

## When to Use

- Joining a new project or taking over maintenance of an existing codebase
- Starting a code review or audit of unfamiliar repositories
- Preparing to refactor or migrate a system you don't own
- Building a mental model of architecture, data flow, and domain concepts
- Creating onboarding documentation for new team members
- Assessing codebase health and technical debt

## Core Concepts

### 1. Architecture Discovery Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│   FILE TREE  │───▶│ DEPENDENCY   │───▶│ ENTRY POINT   │───▶│ DATA FLOW    │
│   MAP        │    │   GRAPH      │    │ IDENTIFICATION│    │   MAPPING    │
│              │    │              │    │               │    │              │
│ - Directories│    │ - Imports    │    │ - main()      │    │ - API routes │
│ - Key files  │    │ - Packages   │    │ - app factory │    │ - DB models  │
│ - Config     │    │ - Circular   │    │ - entrypoints │    │ - Event flow │
│ - Size stats │    │ - External   │    │ - CLI commands│    │ - Side effects│
└──────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
       │                                                            │
       ▼                                                            ▼
┌──────────────┐                                              ┌──────────────┐
│  TERMINOLOGY │◀─────────────────────────────────────────────│  DOMAIN MODEL│
│  GLOSSARY    │                                              │  EXTRACTION  │
│              │                                              │              │
│ - Domain     │◀─────────────────────────────────────────────│ - Entities   │
│   terms      │                                              │ - Relations  │
│ - Acronyms   │                                              │ - Invariants │
│ - Conventions│                                              │ - Boundaries │
└──────────────┘                                              └──────────────┘
```

### 2. Automated Codebase Analysis Script

**Python — Full Codebase Scanner:**

```python
#!/usr/bin/env python3
"""
codebase-scanner.py — Automated codebase analysis for onboarding.

Usage:
    python codebase-scanner /path/to/project

Outputs:
    - File tree with size statistics
    - Dependency graph (imports/requires)
    - Entry point identification
    - TODO/FIXME inventory
    - Dependency manifest
    - Architecture summary (JSON + markdown)
"""

import os
import sys
import json
import ast
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from collections import Counter, defaultdict
from typing import Optional


@dataclass
class FileInfo:
    path: str
    lines: int
    size_bytes: int
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    has_tests: bool = False
    complexity_score: int = 0  # Approximate: branches + loops


@dataclass
class ProjectReport:
    root: str
    total_files: int = 0
    total_lines: int = 0
    total_size_mb: float = 0.0
    language_breakdown: dict = field(default_factory=dict)
    files: list[FileInfo] = field(default_factory=list)
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    entry_points: list[str] = field(default_factory=list)
    todos: list[dict] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    test_coverage_estimate: float = 0.0  # Ratio of test files to source files


IGNORED_DIRS = {
    "node_modules", "__pycache__", ".git", ".venv", "venv", "dist", "build",
    ".next", ".cache", "coverage", ".tox", ".mypy_cache", ".pytest_cache",
    "site-packages", ".terraform", ".serverless",
}

IGNORED_EXTENSIONS = {
    ".png", ".jpg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf",
    ".eot", ".map", ".lock", ".pyc", ".pyo", ".so", ".dylib", ".db",
    ".sqlite", ".sqlite3",
}

LANGUAGE_EXTENSIONS = {
    "python": {".py"},
    "typescript": {".ts", ".tsx"},
    "javascript": {".js", ".jsx", ".mjs"},
    "rust": {".rs"},
    "go": {".go"},
    "java": {".java"},
    "ruby": {".rb"},
    "shell": {".sh", ".bash", ".zsh"},
    "config": {".json", ".yaml", ".yml", ".toml", ".ini", ".env.example"},
    "docs": {".md", ".rst", ".txt"},
}


def scan_directory(root: str) -> ProjectReport:
    """Scan a directory and produce a comprehensive project report."""
    report = ProjectReport(root=os.path.abspath(root))
    ext_to_lang = {}
    for lang, exts in LANGUAGE_EXTENSIONS.items():
        for ext in exts:
            ext_to_lang[ext] = lang

    source_files = 0
    test_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1].lower()

            if ext in IGNORED_EXTENSIONS:
                continue

            rel_path = os.path.relpath(filepath, root)
            is_test = any(
                kw in filename.lower()
                for kw in ["test", "spec", "_test.", ".spec.", ".test."]
            )

            try:
                size = os.path.getsize(filepath)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                lines = content.count("\n") + 1
            except (OSError, IOError):
                continue

            file_info = FileInfo(
                path=rel_path,
                lines=lines,
                size_bytes=size,
                has_tests=is_test,
            )

            # Language tracking
            lang = ext_to_lang.get(ext, "other")
            report.language_breakdown.setdefault(lang, 0)
            report.language_breakdown[lang] += 1

            if is_test:
                test_files += 1
            else:
                source_files += 1

            # Python AST analysis
            if ext == ".py":
                analyze_python(content, file_info)

            # TypeScript/JavaScript analysis
            if ext in {".ts", ".tsx", ".js", ".jsx"}:
                analyze_typescript(content, file_info)

            # TODO/FIXME extraction
            for match in re.finditer(r"#?\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\s]\s*(.+)", content):
                report.todos.append({
                    "file": rel_path,
                    "line": content[:match.start()].count("\n") + 1,
                    "type": match.group(1),
                    "text": match.group(2).strip()[:100],
                })

            # Config file detection
            if filename.lower() in {
                "package.json", "requirements.txt", "pyproject.toml",
                "setup.py", "setup.cfg", "Cargo.toml", "go.mod",
                "Gemfile", "pom.xml", "build.gradle", "Makefile",
                "dockerfile", "docker-compose.yml", ".github/workflows",
            }:
                report.config_files.append(rel_path)

            # Entry point detection
            if is_entry_point(filename, content, ext):
                report.entry_points.append(rel_path)

            report.files.append(file_info)
            report.total_files += 1
            report.total_lines += lines
            report.total_size_mb += size / (1024 * 1024)

    report.total_size_mb = round(report.total_size_mb, 2)

    if source_files > 0:
        report.test_coverage_estimate = round(test_files / (source_files + test_files) * 100, 1)

    # Build dependency summary (top 20 most imported modules)
    all_imports = []
    for f in report.files:
        all_imports.extend(f.imports)
    import_counts = Counter(all_imports)
    report.dependencies = dict(import_counts.most_common(20))

    return report


def analyze_python(content: str, file_info: FileInfo) -> None:
    """Parse Python AST to extract imports, classes, functions."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module:
                file_info.imports.append(node.module.split(".")[0])
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    file_info.imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ClassDef):
            file_info.classes.append(node.name)
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            file_info.functions.append(node.name)
            # Approximate complexity: count branches
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler,
                                     ast.With, ast.Assert, ast.BoolOp)):
                    file_info.complexity_score += 1


def analyze_typescript(content: str, file_info: FileInfo) -> None:
    """Simple regex-based extraction for TypeScript/JavaScript."""
    # Import extraction
    for match in re.finditer(
        r'(?:import\s+(?:.*\s+from\s+)?|require\()["\']([^"\']+)["\']',
        content,
    ):
        module = match.group(1)
        # External vs internal
        if not module.startswith(".") and not module.startswith("/"):
            # Scoped package: @org/pkg or plain pkg
            parts = module.split("/")
            pkg = parts[1] if parts[0].startswith("@") else parts[0]
            file_info.imports.append(pkg)

    # Class/function extraction (simple regex, not AST)
    for match in re.finditer(r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)', content):
        file_info.classes.append(match.group(1))
    for match in re.finditer(
        r'(?:export\s+)?(?:async\s+)?function\s+(\w+)', content,
    ):
        file_info.functions.append(match.group(1))


def is_entry_point(filename: str, content: str, ext: str) -> bool:
    """Detect if a file is likely an entry point."""
    # Python entry points
    if ext == ".py":
        if filename == "main.py" or filename == "__main__.py":
            return True
        if 'if __name__ ==' in content and '"__main__"' in content:
            return True
        if "app = FastAPI()" in content or "app = Flask(" in content:
            return True

    # Node.js entry points
    if ext in {".ts", ".js"}:
        if filename in {"index.ts", "index.js", "main.ts", "main.js", "server.ts", "server.js"}:
            return True
        if "express()" in content or "createServer(" in content:
            return True

    return False


def generate_markdown_report(report: ProjectReport) -> str:
    """Generate a human-readable markdown onboarding report."""
    lines = [
        f"# Codebase Onboarding Report: {os.path.basename(report.root)}",
        "",
        "## Overview",
        f"- **Total files:** {report.total_files}",
        f"- **Total lines:** {report.total_lines:,}",
        f"- **Total size:** {report.total_size_mb} MB",
        f"- **Estimated test ratio:** {report.test_coverage_estimate}%",
        "",
        "## Language Breakdown",
    ]

    for lang, count in sorted(report.language_breakdown.items(), key=lambda x: -x[1]):
        lines.append(f"- **{lang}:** {count} files")

    lines += [
        "",
        "## Entry Points",
    ]
    for ep in report.entry_points:
        lines.append(f"- `{ep}`")

    lines += [
        "",
        "## Configuration Files",
    ]
    for cf in report.config_files:
        lines.append(f"- `{cf}`")

    lines += [
        "",
        "## Top Dependencies (most imported)",
    ]
    for pkg, count in list(report.dependencies.items())[:15]:
        lines.append(f"- `{pkg}` ({count} imports)")

    if report.todos:
        lines += [
            "",
            f"## TODOs/FIXMEs ({len(report.todos)} found)",
            "",
            "| File | Line | Type | Text |",
            "|------|------|------|------|",
        ]
        for todo in report.todos[:30]:  # Cap at 30
            lines.append(f"| `{todo['file']}` | {todo['line']} | {todo['type']} | {todo['text']} |")

    lines += [
        "",
        "## Largest Files (by line count)",
        "",
        "| File | Lines | Classes | Functions |",
        "|------|-------|---------|-----------|",
    ]
    for f in sorted(report.files, key=lambda x: -x.lines)[:20]:
        lines.append(
            f"| `{f.path}` | {f.lines} | {len(f.classes)} | {len(f.functions)} |"
        )

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/project")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Scanning {root}...")
    report = scan_directory(root)

    # Output JSON
    json_path = os.path.join(root, "onboarding-report.json")
    with open(json_path, "w") as f:
        # Convert to serializable dict
        data = asdict(report)
        # Truncate file list for JSON (keep summary)
        data["files"] = [
            asdict(fi) for fi in sorted(report.files, key=lambda x: -x.lines)[:50]
        ]
        json.dump(data, f, indent=2)
    print(f"JSON report: {json_path}")

    # Output markdown
    md_path = os.path.join(root, "ONBOARDING.md")
    with open(md_path, "w") as f:
        f.write(generate_markdown_report(report))
    print(f"Markdown report: {md_path}")


if __name__ == "__main__":
    main()
```

### 3. Key File Identification Checklist

Scan for these files to quickly understand the project:

**Python Projects:**
```
pyproject.toml / setup.py     → Dependencies, build config
requirements.txt              → Pinned dependencies
pytest.ini / pyproject.toml   → Test configuration
Dockerfile                    → Runtime environment
docker-compose.yml            → Local development services
Makefile / justfile           → Developer commands
.pre-commit-config.yaml       → Code quality hooks
.github/workflows/*.yml       → CI/CD pipeline
app/main.py / manage.py       → Application entry point
```

**TypeScript/Node Projects:**
```
package.json                  → Dependencies, scripts
tsconfig.json                 → TypeScript configuration
vite.config.ts / webpack.config.js → Build tooling
jest.config.js / vitest.config.ts → Test configuration
Dockerfile                    → Runtime environment
docker-compose.yml            → Local development services
Makefile / package.json scripts → Developer commands
.github/workflows/*.yml       → CI/CD pipeline
src/index.ts / server.ts      → Application entry point
```

### 4. Dependency Mapping

**Extract the dependency graph:**

```bash
# Python — full dependency tree
pip install pipdeptree
pipdeptree --json > deps.json

# Python — reverse dependency lookup (who requires X?)
pipdeptree --reverse --packages requests

# Node — dependency tree
npm ls --depth=1  # Top-level + direct children
npm ls --production --depth=0  # Production only

# Node — find why a package is installed
npm why express

# Both — dependency audit (known vulnerabilities)
# Python
pip audit --json > vulns.json
# Node
npm audit --json > vulns.json
```

### 5. Domain Terminology Extraction

Extract domain-specific terms from the codebase to build a glossary:

```python
#!/usr/bin/env python3
"""
extract-terminology.py — Extract domain-specific terms from a codebase.

Scans class names, enum values, database models, and constant definitions
to build a domain terminology glossary.

Usage: python extract-terminology.py /path/to/project
"""

import os
import re
import sys
from collections import Counter


def extract_terms(root: str) -> dict[str, list[str]]:
    """Extract domain terms from source files."""
    terms: dict[str, list[str]] = {
        "classes": [],
        "enums": [],
        "models": [],
        "constants": [],
        "api_endpoints": [],
    }

    ignored = {"node_modules", "__pycache__", ".git", "dist", "build", "vendor"}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignored and not d.startswith(".")]

        for filename in filenames:
            if not filename.endswith((".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rb")):
                continue

            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except (OSError, IOError):
                continue

            # Class names (PascalCase)
            terms["classes"].extend(
                re.findall(r'(?:class|interface|type)\s+([A-Z][A-Za-z0-9]+)', content)
            )

            # Enum values (UPPER_SNAKE or PascalCase)
            terms["enums"].extend(
                re.findall(r'(?:enum|Enum)\s+\w+\s*\{([^}]+)\}', content, re.DOTALL)
            )

            # Database models (SQLAlchemy, Prisma, etc.)
            if "class" in content and ("Model" in content or "Base" in content or "Schema" in content):
                terms["models"].extend(
                    re.findall(r'class\s+([A-Z]\w*(?:Model|Schema|Entity|Table))\b', content)
                )

            # API endpoints
            terms["api_endpoints"].extend(
                re.findall(r'["\'](/api/v\d+/[\w/-]+)["\']', content)
            )

    # Deduplicate and count
    result = {}
    for category, items in terms.items():
        cleaned = []
        for item in items:
            # Split compound items
            for term in re.split(r'[\s{},\n]+', item.strip()):
                term = term.strip().strip("'\"")
                if term and len(term) > 2 and not term.isdigit():
                    cleaned.append(term)
        counts = Counter(cleaned)
        result[category] = [term for term, count in counts.most_common(50)]

    return result


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/project")
        sys.exit(1)

    terms = extract_terms(sys.argv[1])

    print("\n# Domain Terminology Glossary\n")
    for category, items in terms.items():
        if items:
            print(f"\n## {category.title()}")
            for term in items[:20]:
                print(f"- `{term}`")


if __name__ == "__main__":
    main()
```

### 6. Learning Checklist

```markdown
## Codebase Onboarding Checklist

### Day 1: Orientation
- [ ] Clone the repository and run it locally
- [ ] Read the README and any ARCHITECTURE.md
- [ ] Run the test suite (verify it passes)
- [ ] Run the codebase scanner (`python codebase-scanner .`)
- [ ] Read the ONBOARDING.md report generated by the scanner
- [ ] Identify the entry point(s) and trace the request flow

### Day 2: Architecture
- [ ] Map the high-level architecture (draw a diagram)
- [ ] Identify all services/modules and their responsibilities
- [ ] Trace one complete request from entry to database and back
- [ ] Identify the database schema and key relationships
- [ ] List all external dependencies (APIs, services, queues)
- [ ] Identify the CI/CD pipeline and deployment process

### Day 3: Deep Dive
- [ ] Read the domain terminology glossary
- [ ] Identify the 5 most important business rules
- [ ] Find the authentication and authorization flow
- [ ] Trace error handling patterns
- [ ] Identify the logging and monitoring setup
- [ ] Read the 3 most complex files (by line count)

### Day 4: First Contribution
- [ ] Pick a small, well-scoped task (bug fix, small feature)
- [ ] Write tests first (TDD)
- [ ] Implement the minimum code to pass tests
- [ ] Run full test suite and lint
- [ ] Submit PR with clear description of what and why

### Ongoing
- [ ] Track knowledge gaps in a personal notes file
- [ ] Ask about any acronym or term you don't understand
- [ ] Review PRs from experienced team members
- [ ] Document things you learn that aren't in existing docs
```

### 7. Knowledge Gap Tracking

```python
#!/usr/bin/env python3
"""
knowledge-gap-tracker.md — Template for tracking onboarding knowledge gaps.

Usage: Copy this template and fill it in as you explore the codebase.
"""

KNOWLEDGE_GAP_TEMPLATE = """
# Knowledge Gap Tracker: {project_name}

## What I Understand
- [List things you can explain to someone else]

## What I Don't Understand Yet
| Topic | Why It Matters | Who Can Help | Status |
|-------|---------------|--------------|--------|
|       |               |              | Open   |

## Unanswered Questions
| Question | Asked To | Date | Answered? |
|----------|----------|------|-----------|
|          |          |      | No        |

## Key Decisions I've Learned
| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
|          |           |            |

## Domain Terms I've Learned
| Term | Meaning | Where Used |
|------|---------|------------|
|      |         |            |
"""
```

## Workflow: Systematic Onboarding

### Step 1: Initial Scan

```bash
# Run the automated scanner
python codebase-scanner.py /path/to/project

# Review the generated reports
cat ONBOARDING.md
cat onboarding-report.json | jq '.entry_points, .config_files, .language_breakdown'
```

### Step 2: Run the Project Locally

```bash
# Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest  # Verify tests pass
python main.py    # Start the application

# TypeScript/Node
npm install
npx tsc --noEmit  # Type check
npm test          # Run tests
npm run dev       # Start dev server
```

### Step 3: Trace the Architecture

1. Start at the entry point
2. Follow imports to understand module structure
3. Trace one complete API request end-to-end
4. Map the database schema (ORM models or migration files)
5. Identify external service integrations

### Step 4: Build the Glossary

```bash
# Extract domain terminology
python extract-terminology.py /path/to/project
```

### Step 5: Identify Your First Task

- Look for `good first issue` labels in the issue tracker
- Find TODOs with low complexity (from the scanner report)
- Ask the team for a small, well-defined task
- Avoid touching critical paths until you understand the system

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Reading code without running it | Mental model doesn't match reality | Run it, add logging, trace requests |
| Skipping the test suite | Don't know what's tested vs broken | Run tests first, fix failures |
| Assuming conventions | Wrong naming, wrong patterns | Read 3 existing files, copy the pattern |
| No glossary | Domain terms are gibberish | Extract terms early, ask about acronyms |
| Big first PR | Reviewer rejects, too many issues | Start small, one focused change |

## Success Checklist

- [ ] Project runs locally (tests pass, app starts)
- [ ] ONBOARDING.md report generated and reviewed
- [ ] Entry points identified and traced
- [ ] High-level architecture diagram drawn
- [ ] Domain terminology glossary created
- [ ] Key configuration files reviewed
- [ ] CI/CD pipeline understood
- [ ] First task identified and scoped
- [ ] Knowledge gap tracker started
- [ ] Learning checklist at least Day 1-2 complete
