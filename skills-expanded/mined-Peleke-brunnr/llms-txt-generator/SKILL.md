---
name: llms-txt-generator
description: Generate llms.txt and llms-full.txt files for any MkDocs documentation site, following the llms.txt standard. Creates a curated index of doc pages and a MkDocs build hook that auto-generates the full inlined version from source markdown. Use when adding AI-queryable docs to a project with an existing MkDocs site.
license: Complete terms in LICENSE.txt
metadata:
  openclaw:
    emoji: "\U0001F916"
    requires:
      bins: ["python3"]
---

# llms.txt Generator

> Add AI-queryable documentation to any MkDocs site. Generates `llms.txt` (curated index) and a build hook that produces `llms-full.txt` (all docs inlined) from source markdown.

## TL;DR Execution Flow

```
Phase 0: Pre-flight checks (MkDocs site exists, nav structure, GitHub Pages)
Phase 1: Discovery (read mkdocs.yml nav, read all doc pages, classify sections)
Phase 2: Generate llms.txt (curated index with section organization)
Phase 3: Generate build hook (MkDocs on_pre_build hook for llms-full.txt)
Phase 4: Wire into build (mkdocs.yml hooks, .gitignore, verify build)
Phase 5: Commit, PR, verify deployment
```

## When to Use

- Adding llms.txt to an existing MkDocs documentation site
- Making project docs queryable by AI tools (Context7, mcpdoc, Claude Code, Cursor)
- Phase 0 of a docs-as-MCP initiative

## Inputs

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_root` | path | cwd | Project root directory |
| `site_url` | string | from mkdocs.yml | Base URL for the docs site |
| `optional_sections` | string[] | `["Theory", "Optional"]` | Nav sections to put under `## Optional` in llms.txt |
| `issue_number` | int \| null | null | GitHub issue to close with the PR |

---

## Phase 0: Pre-Flight Checks

### 0.1 MkDocs Site Exists

```
Verify:
- mkdocs.yml exists at project root
- docs/ directory exists with .md files
- site_url is configured in mkdocs.yml (or provided as input)
- nav: section exists in mkdocs.yml (required for structured generation)

If mkdocs.yml has no nav:, STOP and inform user.
The nav structure is what determines llms.txt organization.
```

### 0.2 Existing llms.txt

```
Check for:
- docs/llms.txt        → Already exists, ask user: overwrite or update?
- docs/llms-full.txt   → Generated file, safe to overwrite
- hooks/ directory      → May already have MkDocs hooks
- mkdocs.yml hooks:     → May already have hooks registered

If llms.txt exists, switch to "update" mode.
```

### 0.3 GitHub Pages Status

```bash
# Is the site deployed?
gh api "/repos/{OWNER}/{REPO}/pages" 2>/dev/null
# 200 = deployed (we can verify URLs after)
# 404 = not deployed (note for user)
```

---

## Phase 1: Discovery

**Goal:** Understand the docs structure completely before generating anything.

### 1.1 Parse mkdocs.yml Nav

Read `mkdocs.yml` and extract the full navigation tree:

```
For each nav entry:
  - Section name (H2 in llms.txt)
  - Page title
  - Page path (relative to docs/)
  - Nesting depth

Output: Ordered list of (section, title, path) tuples
```

### 1.2 Read All Doc Pages

For each page in the nav:

```
Read the .md file and extract:
  - First heading (H1) — use as display name if different from nav title
  - First paragraph — use as description in llms.txt link entry
  - Total line count — for size estimation of llms-full.txt
```

### 1.3 Classify Sections

Determine which nav sections are "core" vs "optional":

```
Core (always included):
  - Getting Started, Installation, Quick Start
  - Guides, How-to, Usage
  - Reference, API, CLI
  - Architecture

Optional (included under ## Optional):
  - Theory, Tutorials, Background
  - Philosophy, About
  - Roadmap, Changelog
  - Contributing, Development
  - Any section matching optional_sections input

The user's optional_sections input overrides defaults.
```

---

## Phase 2: Generate llms.txt

### 2.1 Structure

Follow the [llms.txt specification](https://llmstxt.org/):

```markdown
# {Project Name}

> {site_description from mkdocs.yml}

{Summary paragraph — 2-3 sentences describing what the project does,
 its core mechanism, and primary use case. Derive from docs/index.md.}

## {Core Section 1}

- [{Page Title}]({full_url}): {One-line description from first paragraph}
- [{Page Title}]({full_url}): {One-line description}

## {Core Section 2}

- [{Page Title}]({full_url}): {One-line description}

## Optional

- [{Page Title}]({full_url}): {One-line description}
```

### 2.2 URL Construction

```
base_url = site_url from mkdocs.yml (ensure trailing slash)

For each page path from nav:
  - getting-started/installation.md → {base_url}getting-started/installation/
  - index.md → {base_url}
  - theory/index.md → {base_url}theory/

MkDocs URL convention: .md extension → trailing slash directory URL
```

### 2.3 Description Extraction

For each page, generate a one-line description:

```
Priority:
1. If page has a clear opening sentence, use it (truncate to ~100 chars)
2. If page starts with a list of features, summarize: "Covers X, Y, and Z"
3. If page is mostly code examples, describe: "Commands for X and Y"
4. Fallback: Use the nav title as-is
```

### 2.4 Write File

Write to `docs/llms.txt`. This file is committed to the repo.

---

## Phase 3: Generate Build Hook

### 3.1 Hook Script

Create `hooks/generate_llms_full.py`:

```python
"""MkDocs hook: generate llms-full.txt from llms.txt + source markdown.

Runs on_pre_build so the generated file is available for MkDocs to copy
to the site output directory.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

SITE_URL = "{site_url}"  # From mkdocs.yml
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
LLMS_TXT = DOCS_DIR / "llms.txt"
LLMS_FULL_TXT = DOCS_DIR / "llms-full.txt"


def _url_to_local_path(url: str) -> Path | None:
    """Convert a site URL to a local docs/ markdown file path."""
    parsed = urlparse(url)
    path = parsed.path

    # Strip the site prefix — extract from SITE_URL
    prefix = urlparse(SITE_URL).path
    if not path.startswith(prefix):
        return None
    relative = path[len(prefix):]

    # Trailing slash -> try as directory/index.md first, then as file.md
    if relative.endswith("/"):
        relative += "index.md"
    elif not relative.endswith(".md"):
        relative += ".md"

    candidate = DOCS_DIR / relative
    if candidate.exists():
        return candidate

    # Try without the trailing directory (installation/ -> installation.md)
    if relative.endswith("/index.md"):
        alt = DOCS_DIR / relative.replace("/index.md", ".md")
        if alt.exists():
            return alt

    return None


def _parse_llms_txt(content: str) -> tuple[list[str], list[tuple[str, str, str]]]:
    """Parse llms.txt into preamble lines and (section, name, url) entries."""
    preamble: list[str] = []
    entries: list[tuple[str, str, str]] = []
    current_section = ""
    in_preamble = True

    for line in content.splitlines():
        h2_match = re.match(r"^## (.+)$", line)
        if h2_match:
            current_section = h2_match.group(1)
            in_preamble = False
            continue

        link_match = re.match(r"^- \[(.+?)\]\((.+?)\)", line)
        if link_match:
            name = link_match.group(1)
            url = link_match.group(2)
            entries.append((current_section, name, url))
            in_preamble = False
            continue

        if in_preamble:
            preamble.append(line)

    return preamble, entries


def generate_llms_full() -> str:
    """Generate llms-full.txt content from llms.txt + source markdown."""
    llms_content = LLMS_TXT.read_text()
    preamble, entries = _parse_llms_txt(llms_content)

    parts: list[str] = []
    parts.append("\n".join(preamble).strip())
    parts.append("")

    current_section = ""
    for section, name, url in entries:
        if section != current_section:
            current_section = section
            parts.append(f"\n## {section}\n")

        local_path = _url_to_local_path(url)
        if local_path and local_path.exists():
            md_content = local_path.read_text().strip()
            parts.append(md_content)
            parts.append("")
        else:
            parts.append(f"### {name}\n\nSee: {url}\n")

    return "\n".join(parts)


def on_pre_build(**kwargs) -> None:
    """Generate llms-full.txt before MkDocs builds the site."""
    if not LLMS_TXT.exists():
        return
    content = generate_llms_full()
    LLMS_FULL_TXT.write_text(content)


if __name__ == "__main__":
    if not LLMS_TXT.exists():
        print(f"Error: {LLMS_TXT} not found")
        raise SystemExit(1)
    content = generate_llms_full()
    LLMS_FULL_TXT.write_text(content)
    print(f"Generated {LLMS_FULL_TXT} ({len(content)} bytes)")
```

**IMPORTANT:** Replace `{site_url}` with the actual `site_url` from mkdocs.yml. The URL prefix extraction must match exactly.

### 3.2 Hook Must Handle

- Pages that resolve to `dir/index.md` or `dir.md` (MkDocs supports both)
- Missing pages (fallback to link reference, don't crash)
- Preamble preservation (H1, blockquote, overview paragraphs pass through)
- Section headers from llms.txt H2s

---

## Phase 4: Wire Into Build

### 4.1 Register Hook in mkdocs.yml

Add to mkdocs.yml (before `markdown_extensions:` if it exists):

```yaml
hooks:
  - hooks/generate_llms_full.py
```

If `hooks:` already exists, append to the list.

### 4.2 Update .gitignore

Add to .gitignore:

```
# Generated docs (rebuilt by MkDocs hook)
docs/llms-full.txt
```

### 4.3 Verify Build

```bash
# Generate standalone
python hooks/generate_llms_full.py

# Full MkDocs build
python -m mkdocs build --strict

# Verify both files in site output
ls -la site/llms.txt site/llms-full.txt
```

Both files must be present in `site/`. If `--strict` fails, fix warnings before proceeding.

---

## Phase 5: Commit, PR, Verify

### 5.1 Branch and Commit

```bash
# Create branch (if not already on a feature branch)
git checkout -b feat/llms-txt

# Stage relevant files only
git add docs/llms.txt hooks/generate_llms_full.py mkdocs.yml .gitignore

# Commit
git commit -m "feat: add llms.txt and build hook for AI-queryable docs"
```

Do NOT stage `docs/llms-full.txt` — it's generated and gitignored.

### 5.2 Create PR

```bash
git push -u origin feat/llms-txt

gh pr create \
  --title "feat: add llms.txt for AI-queryable docs" \
  --body "Adds llms.txt (curated index) and llms-full.txt (all docs inlined) \
to the documentation site. MkDocs build hook auto-regenerates llms-full.txt \
from source markdown on every build. Follows the llms.txt standard for \
Context7, mcpdoc, and other AI tools. Closes #{issue_number}"
```

### 5.3 Post-Deploy Verification

After merge and GitHub Pages deploy:

```bash
# Verify files are accessible
curl -s -o /dev/null -w "%{http_code}" {site_url}llms.txt
# Should return 200

curl -s -o /dev/null -w "%{http_code}" {site_url}llms-full.txt
# Should return 200

# Test with mcpdoc (if available)
# claude mcp add {project}-docs -- npx mcpdoc {site_url}llms.txt
```

---

## Quality Checklist

### llms.txt Content
- [ ] H1 matches project name from mkdocs.yml
- [ ] Blockquote has concise project summary
- [ ] All nav pages are referenced (none missing)
- [ ] URLs use full absolute paths with site_url prefix
- [ ] Each link has a meaningful one-line description
- [ ] Core sections come before ## Optional
- [ ] Theory/background/changelog are under ## Optional

### Build Hook
- [ ] `SITE_URL` matches mkdocs.yml `site_url` exactly
- [ ] All linked pages resolve to local .md files
- [ ] Hook handles both `dir/index.md` and `dir.md` patterns
- [ ] Missing pages fall back to link reference (no crash)
- [ ] `python hooks/generate_llms_full.py` runs standalone
- [ ] `mkdocs build --strict` passes

### Integration
- [ ] `hooks:` registered in mkdocs.yml
- [ ] `docs/llms-full.txt` in .gitignore
- [ ] Both files present in `site/` after build
- [ ] Accessible at `{site_url}llms.txt` after deploy

---

## Reference: The llms.txt Standard

From [llmstxt.org](https://llmstxt.org/):

- Format: Markdown
- Location: Site root (`/llms.txt`)
- Required: H1 heading (project name)
- Optional: Blockquote (summary), detail paragraphs, H2 sections with link lists
- Special: `## Optional` section — content that can be skipped for shorter context
- Companion: `llms-full.txt` — expanded version with all linked content inlined
