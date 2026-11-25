---
name: grimoire
description: Grimoire — turn a PDF/document/raw text into reading notes + a reusable skill pack in one parse. Auto-classifies book/paper/document, scaffolds type-specific notes for an Obsidian vault, and mines per-source skills merged per book/course. Built on the MinerU parsing API (OCR, formula/table, batch). Scripts never call an LLM and never write the vault; skill install is OPT-IN (--install / scripts/skill-install.sh) and deliberately crosses the candidate-only boundary by explicit user request, recorded in the manifest. Raw text → skill via --from-text; cross-agent install + management via the grimoire-manage companion skill.
triggers:
  - grimoire
  - 魔典
  - 把这本书炼成魔典
  - pdf 转笔记
  - pdf to notes
  - 帮我读这个 pdf
  - 帮我读这个 pdf 写笔记并提炼 skill
  - 读书笔记
  - 论文笔记
  - 文档笔记
  - 这个 pdf 是书还是论文
  - reading notes
  - book to skill
  - 书籍转 skill
  - 从书中提炼 skill
  - 技能提炼
  - mineru
  - pdf解析
  - 文档解析
  - document parsing
  - pdf to markdown
  - extract pdf
  - 文本转 skill
  - text to skill
  - from-text
  - 把技能装到其它 agent
  - 跨 agent 安装技能
  - install skill across agents
  - skill 没出现在某个 agent
  - 重新同步技能
  - skill 确认门
---

# Grimoire · 魔典 — Document → Notes + Skill Pack

> One source, parsed once, woven into typed reading notes (→ Obsidian) and a
> per-source skill pack. Primary entry point: `scripts/grimoire.sh`.
> Full product overview and bilingual docs: see [README.md](README.md).
>
> The sections below are the underlying MinerU parsing API reference that the
> `grimoire` toolchain is built on.

### Flow: Markdown first, the grimoire is opt-in · 先转 MD,魔典是可选续跑

The pipeline is **gated**, not automatic:

1. **Always first → Markdown.** A source becomes Markdown via `pdf2md` /
   `mineru-local` (or any MinerU parse). For many requests this is the whole
   job — **stop here**. Do not auto-run notes/skill mining.
2. **Opt-in → the grimoire.** Only when the user actually wants reading notes
   and/or a packaged skill, continue **from that Markdown** with
   `grimoire.sh --from-markdown <md>`. Nothing is re-uploaded; the parse is
   skipped. `--only notes|skills|both` is the second opt-in: notes only,
   the skill (engineering-prompt) packaging only, or both.
3. **`--only both` is two-stage, not parallel.** Stage 1 writes the
   type-specific notes from the source. Stage 2 is a deliberate
   **re-learning pass (重复学习)**: the agent re-reads the notes it just
   wrote and mines the skill pack **from those notes' knowledge points**,
   not the raw source (`source-markdown/` is then only for evidence
   anchors). `--only skills` (no notes) keeps mining from the source.

> 默认只到 MD;笔记 / 把内容封装成 skill 工程提示属于用户主动选择的下游,
> 用 `--from-markdown` 从已有 MD 续跑,不重新上传、不重复解析。
> `--only both` 是两段式:先写笔记,再「重复学习」从笔记里挖技能包,
> 不是同段并行。

This keeps the live `pdf2md` / `mineru-local` path unchanged — Grimoire does
not steal its triggers; it is the deliberate next step after Markdown.

## Overview
MinerU converts PDF, DOC, DOCX, PPT, PPTX, PNG, JPG, JPEG, HTML into machine-readable Markdown/JSON. Supports OCR (109 languages), formula/table recognition, cross-page table merging, and batch processing.

This skill can also stage a parsed long-form source as a **source skill pack**:
a workspace that a large language model can read to extract candidate agent
skills, grouped by source first and then by chapter, lesson, section, or note.
The workflow does not call an LLM and does not install generated skills
automatically.

It can additionally run a **source-to-notes** pipeline: parse a document,
**auto-classify it as `book` / `paper` / `document`** (hybrid heuristic + AI
confirmation), scaffold the matching note discipline, and stage the final note
for the Obsidian Knowledge-Hub vault. The agent does the reading and writing;
the scripts never call an LLM and never write into the vault directly.

**Two modes:**
- **Cloud API** — `https://mineru.net/api/v4` (no GPU required, token-based)
- **Local API** — `mineru-api --port 8000` (self-hosted, requires GPU or CPU backend)

## Authentication (Cloud API)

- **Token file**: `~/.config/mineru/token`
- **Header**: `Authorization: Bearer <token>`
- **Get token**: https://mineru.net/apiManage/token

```bash
mkdir -p ~/.config/mineru
echo "YOUR_TOKEN" > ~/.config/mineru/token
chmod 600 ~/.config/mineru/token
```

## Limits (Cloud API)

| Item | Limit |
|------|-------|
| Single file size | 200MB max |
| Single file pages | 600 pages max |
| Daily priority pages | 2000 pages/account |
| Batch upload | 200 files/request |
| Token validity | 90 days |

## Model Versions

| Model | Use Case | Speed | Notes |
|-------|----------|-------|-------|
| `vlm` | **Default.** MinerU2.5, complex layouts, highest accuracy | Slower | Cloud-recommended; needs GPU locally |
| `pipeline` | General documents, CPU-friendly | Fast | Pure CPU support, lower accuracy |
| `MinerU-HTML` | HTML output, preserves formatting | Medium | For web content |
| `hybrid` | ~~Default pre-2026-04~~ | — | **RETIRED on the cloud API** — returns `code -10002 "version field invalid"`. Do not use against `mineru.net`. |

## API Endpoints (Cloud)

Base URL: `https://mineru.net/api/v4`

### 1. Create Extraction Task (Single File)
```
POST /extract/task
```

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| url | string | yes | - | File URL (no direct upload) |
| model_version | string | no | vlm | `vlm` / `pipeline` / `MinerU-HTML` (`hybrid` retired, returns `-10002`) |
| is_ocr | bool | no | false | Enable OCR |
| enable_formula | bool | no | true | Formula recognition |
| enable_table | bool | no | true | Table recognition |
| language | string | no | ch | Document language |
| data_id | string | no | - | Custom identifier |
| page_ranges | string | no | - | e.g. "2,4-6" |
| callback | string | no | - | Callback URL for async results |
| extra_formats | array | no | - | `["docx"]`, `["html"]`, `["latex"]` |

**Response:**
```json
{"code": 0, "data": {"task_id": "xxx"}, "msg": "ok"}
```

### 2. Get Task Results
```
GET /extract/task/{task_id}
```

**States:** `pending` → `running` → `done` / `failed` / `converting`

**Done response:** includes `full_zip_url` (download link)

### 3. Batch Upload Local Files
```
POST /file-urls/batch
```
Returns presigned upload URLs (valid 24h). System auto-submits extraction after upload.

### 4. Batch URL Extraction
```
POST /extract/task/batch
```
Submit multiple URLs at once, returns `batch_id`.

### 5. Batch Results
```
GET /extract-results/batch/{batch_id}
```

## Local API (Self-Hosted)

### Start Server
```bash
# FastAPI server
mineru-api --host 0.0.0.0 --port 8000

# Gradio WebUI
mineru-gradio --server-name 0.0.0.0 --server-port 7860

# OpenAI-compatible server (for remote VLM inference)
mineru-openai-server --port 30000
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `MINERU_MODEL_SOURCE` | Model source: `modelscope` / `huggingface` | huggingface |
| `MINERU_API_MAX_CONCURRENT_REQUESTS` | Max concurrent API requests | Unlimited |
| `MINERU_API_ENABLE_FASTAPI_DOCS` | Enable /docs page | true |

### Local API Docs
Access at `http://127.0.0.1:8000/docs` after starting.

### Use CLI with Remote Server
```bash
mineru -p input.pdf -o output/ -b hybrid-http-client -u http://server:30000
```

## Error Codes

| Code | Issue | Fix |
|------|-------|-----|
| A0202 | Token invalid | Check Bearer prefix and token |
| A0211 | Token expired | Recreate at mineru.net |
| -60002 | Unrecognized format | Check file extension |
| -60005 | File too large | Max 200MB |
| -60006 | Too many pages | Max 600, split document |
| -60008 | URL timeout | Check URL accessibility |
| -60012 | Task not found | Verify task_id |

## Helper Script

`~/.claude/skills/mineru/scripts/mineru-parse.sh` — full-featured CLI wrapper.

```bash
# URL mode
mineru-parse.sh https://example.com/doc.pdf

# Local file with options
mineru-parse.sh /path/to/file.pdf --model vlm --ocr --output /tmp/result

# Extra formats
mineru-parse.sh doc.pdf --format docx --format latex

# Page ranges
mineru-parse.sh doc.pdf --pages "1-5,8" --output ./results

# Auto-extract markdown from zip
mineru-parse.sh doc.pdf --output ./results --extract

# Extract without printing book-sized markdown and write a local manifest
mineru-parse.sh book.pdf --output ./results --extract --no-print-md --manifest ./results/parse_manifest.json
```

## Source-to-Skill Workflow

Use this when the user uploads a book, course, paper, manual, article
collection, or other long-form text and wants the agent to learn which reusable
skills can be extracted from it.

### Commands

```bash
# Local files are uploaded to the MinerU cloud API; --cloud-ok is required.
~/.claude/skills/mineru/scripts/mineru-source-to-skill.sh /path/to/book.pdf \
  --title "Book Title" \
  --type auto \
  --output ./source-workspaces \
  --cloud-ok

# If the source is already parsed to Markdown, stage a pack directly.
~/.claude/skills/mineru/scripts/source-skill-pack.sh ./mineru-extracted/book \
  --title "Book Title" \
  --type auto \
  --output ./source-skill-packs
```

Compatibility wrappers are still available for older automation:
`mineru-book-to-skill.sh`, `book-skill-pack.sh`, and
`vivo-agent-workspace.sh`.

### Output Contract

The wrapper creates a source-scoped workspace:

```text
source-workspaces/
└── sources/
    └── <source-slug>/
        ├── README.md
        ├── source/
        ├── mineru/
        │   ├── parse_manifest.json
        │   ├── *_result.zip
        │   └── <extracted markdown files>
        └── analysis/
            └── source-skill-pack/
                ├── README.md
                ├── manifest.json
                ├── LLM_EXTRACTION_PROMPT.md
                ├── BOOK_SKILL_INDEX.md
                ├── MANAGE_SKILLS.md
                ├── MINDMAP.md
                ├── source-markdown/
                ├── segments/
                │   ├── manifest.json
                │   └── 001-<chapter-or-section>.md
                ├── chapter-skills/
                │   └── 001-<chapter-or-section>/
                │       ├── CHAPTER_SKILL_INDEX.md
                │       └── skills/
                ├── whole-book/
                │   └── WHOLE_BOOK_SUMMARY.md
                └── skills/
```

Give `LLM_EXTRACTION_PROMPT.md`, `segments/`, and `chapter-skills/` to the
active agent. The agent should fill:

- `chapter-skills/*/CHAPTER_SKILL_INDEX.md`: what each segment contributes before whole-source synthesis.
- `chapter-skills/*/skills/*.md`: one narrow candidate skill per segment-level capability.
- `whole-book/WHOLE_BOOK_SUMMARY.md`: source-level capability summary after segment extraction.
- `MINDMAP.md`: topic classification and skill-family map.
- `BOOK_SKILL_INDEX.md`: what this source can help the agent do, when to reference it, and a table of skill candidates.
- `skills/*.md`: reviewed cross-segment candidates only, using the generated `_skill-template.md`.

### Extraction Criteria

Extract only content that can become an operational skill:

- procedures and workflows
- checklists
- diagnostics
- decision rules
- reusable prompt patterns
- coding or analysis patterns
- frameworks with clear trigger situations

Keep broad concepts and background theory as reference-only material unless the source gives a concrete procedure.

### Manage Skills Boundary

Long-form skill packs are candidates. Do not automatically install, enable, or sync generated skills. After human review, promote only stable skills into the managed skills repository, then run the local skills manager separately, for example:

```bash
skills enable <promoted-skill-name>
```

The generated pack must not store API tokens, authorization headers, remote result URLs, or private account data.

### Source Type Classification

Use `--type auto` by default. The packer records detected type metadata for
books, courses, papers, manuals, article collections, videos, web sources,
mixed source sets, and project notes. Override with `--type book`,
`--type course`, `--type paper`, `--type manual`, `--type article-collection`,
`--type video`, `--type audio`, `--type web`, `--type mixed`, or
`--type project-notes` when the automatic classifier is wrong.

## Source-to-Notes Workflow

Use this when the user gives a PDF/document and wants the agent to **read it
and write notes** (not extract agent skills). The pipeline auto-decides the
note discipline from the document itself.

### Commands

```bash
# One shot: parse + classify + scaffold notes workspace.
# Local files are uploaded to the MinerU cloud API; --cloud-ok is required.
~/.claude/skills/mineru/scripts/mineru-to-notes.sh /path/to/source.pdf \
  --title "Source Title" \
  --type auto \
  --cloud-ok

# Already have MinerU Markdown? Stage the notes pack directly:
~/.claude/skills/mineru/scripts/reading-notes-pack.sh ./mineru-extracted/doc \
  --title "Source Title" --type auto

# RECOMMENDED MD-first continuation: pdf2md already produced Markdown, the
# user now opts in to the grimoire. No re-upload, no re-parse.
~/.claude/skills/mineru/scripts/grimoire.sh \
  --from-markdown ./mineru-extracted/doc \
  --title "Source Title" \
  --only both          # or: notes | skills
```

### Classification (hybrid, autonomous)

`scripts/lib/reading-types.sh` scores filename + parsed-Markdown structure into
three buckets and a confidence band:

| Type | Trigger signals | Note discipline |
|------|-----------------|-----------------|
| `book` | many `第N章`/`Chapter N`, TOC, ISBN, long page count | **chapter-by-chapter complete notes** |
| `paper` | abstract, DOI/arXiv, references, related work, venue | **detailed structured reading / excerpt notes** |
| `document` | API ref / install / config / report / spec / slides, short | **content-adaptive structured notes** |

- High/medium confidence → the scaffold proceeds for that type.
- **Low confidence → AI fallback**: the pack writes `AI_CLASSIFY.md` with a text
  sample and a strict book/paper/document decision contract. The agent confirms
  the type (Step 0) before reading; if it disagrees with the heuristic it
  re-runs the packer with the correct `--type`.

Manual override is always available with `--type book|paper|document`.

### Output Contract

```text
reading-workspaces/sources/<slug>/
  README.md
  source/
  mineru/parse_manifest.json + extracted Markdown
  notes/reading-notes-pack/
    classification.json        detected type / confidence / signals
    AI_CLASSIFY.md             only when confidence is low
    AI_READING_TASK.md         the reading contract (entry point)
    OBSIDIAN_PLAN.md           exact vault target + house-style rules
    manifest.json
    source-markdown/
    segments/                  chapter/section split (book & document)
    notes/<slug>.md            scaffold from the matching template
```

Give the agent `AI_READING_TASK.md`. It reads `source-markdown/` (and
`segments/` for books/documents), fills `notes/<slug>.md` using the
type-specific template, passes a quality self-check (> 2KB real synthesis,
evidence anchors, `[[wikilinks]]`, no placeholders), then writes the final
note into the Obsidian vault path from `OBSIDIAN_PLAN.md` and appends a
`log.md` line.

### Obsidian Knowledge-Hub Boundary

The vault target folder is `book → Books/`, `paper → Papers/`,
`document → Documents/`. Vault root defaults to `$MINERU_OBSIDIAN_VAULT` or
`~/Documents/Obsidian-Vaults/Knowledge-Hub` and is overridable with `--vault`.
The scripts **never create or modify a vault file** — the agent writes the
note after the quality self-check, matching the house style of an existing
sibling note. Generated packs store no API tokens, auth headers, or remote
result URLs.

## Vivo Agent Workflow

Use this when the user gives text or source metadata and wants Codex, Claude
Code, or another agent to first identify the object type, write the matching
notes, then distill candidate skills from books, papers, courses, web pages,
videos, audio transcripts, PDFs, or existing notes.

```bash
~/.claude/skills/mineru/scripts/vivo-workspace.sh \
  --title "Knowledge Source" \
  --type mixed \
  --agent "Claude Code" \
  --output ./vivo-workspaces
```

Vivo creates `AGENT_TASK.md`, `SOURCES.md`, `notes/live-notes.md`,
`notes/source-type-confirmation.md`, `notes/topic-classification.md`,
`notes/skill-discovery-coverage.md`, `captured-markdown/`, and `packs/`. The
script does not call OpenAI, Claude, or any model. The active agent performs
capture and reasoning with its available tools:

- web pages: browser, fetch, web search, or OpenAI-backed web capability
- videos: subtitles or transcript tools
- audio: transcript or speech-to-text tools when available
- PDFs: MinerU parsing or another local converter
- courses: lesson/module/topic classification
- notes: first source-type confirmation, then typed notes while capture happens

After type confirmation and typed notes, the agent runs `source-skill-pack.sh`
over `captured-markdown/` and fills segment skills,
`whole-book/WHOLE_BOOK_SUMMARY.md`, `MINDMAP.md`,
`SKILL_DISCOVERY_COVERAGE.md`, and `BOOK_SKILL_INDEX.md` before promoting
reviewed candidates. Stop only when a full pass over every source unit finds no
new supported operational skills.

## Quick Parse (Python)

```python
import requests, time

TOKEN = open("~/.config/mineru/token").read().strip()
BASE = "https://mineru.net/api/v4"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def parse_document(url, model="vlm", ocr=False, extra_formats=None):
    """Parse a document from URL, return download link."""
    body = {
        "url": url, "model_version": model,
        "is_ocr": ocr, "enable_formula": True, "enable_table": True,
    }
    if extra_formats:
        body["extra_formats"] = extra_formats

    resp = requests.post(f"{BASE}/extract/task", headers=HEADERS, json=body)
    task_id = resp.json()["data"]["task_id"]

    while True:
        result = requests.get(f"{BASE}/extract/task/{task_id}", headers=HEADERS).json()
        state = result["data"]["state"]
        if state == "done":
            return result["data"]["full_zip_url"]
        elif state == "failed":
            raise Exception(f"Task failed: {result}")
        time.sleep(5)
```

## Quick Parse (curl)

```bash
TOKEN=$(cat ~/.config/mineru/token)

# Submit
curl -s -X POST "https://mineru.net/api/v4/extract/task" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/doc.pdf","model_version":"vlm"}'

# Check result
curl -s "https://mineru.net/api/v4/extract/task/{task_id}" \
  -H "Authorization: Bearer $TOKEN"
```

## Installation (Local Mode)

```bash
pip install uv
uv pip install -U "mineru[all]"
```

Requirements: Python 3.10-3.13, 16GB+ RAM, 20GB+ SSD. GPU optional (Volta+ or Apple Silicon).
