---
name: tech-doc-consistency-check
description: >
  Audits and auto-fixes Markdown technical documentation for structural and linguistic
  consistency, then outputs a summary table of all issues found and fixed. Use this skill
  whenever the user wants to validate, review, clean up, or proofread a Markdown file —
  even when they don't say "consistency check" explicitly. Trigger on: "check this doc
  before I publish", "the TOC links seem broken", "something looks off in the section
  numbers", "proofread my technical writeup", "review this doc for errors", "make sure
  the anchors work", "audit this markdown", or any request to verify or clean up a .md
  file. Checks section numbering, TOC completeness, TOC anchor links (GFM rules including
  em-dash handling), HTML anchor validity, tech-aware spelling, and prose grammar —
  auto-fixing everything it can and flagging judgment calls for the user.
license: Apache-2.0
metadata:
  author: Vincent Yin
  version: "2.1.1"
---

# Tech Doc Consistency Checker

Your goal is to leave the document structurally sound and linguistically clean. Work through the checks below in order, fixing each issue as you go so subsequent checks operate on the corrected state. Auto-fix anything with a clear correct answer; flag anything that requires judgment.

---

## Check 1 — Section Numbering

Numbered headings are a navigation contract with the reader: when a section is added, removed, or moved, sibling numbers must be updated or that contract breaks. Verify that all numbered headings are consecutive with no gaps, at every level.

**Body order is authoritative.** When the TOC order and the body order disagree, renumber the body sections in place and update the TOC to match — never reorder body sections to match the TOC. The body is the document; the TOC is an index of it.

**How to check:**
1. Extract all headings with `grep -n "^#" <file>`, filtering out lines inside fenced code blocks.
2. For top-level numbered sections (e.g., `## 1.`, `## 2.`), verify they run 1, 2, 3, … with no skips.
3. For each subsection group (e.g., `### 2.1`, `### 2.2`), verify they run .1, .2, .3, … with no skips.
4. Verify subsection prefixes match their parent (e.g., all subsections of `## 3.` start with `3.`).

**Common issues:**
- A section was added or removed but siblings were not renumbered.
- A section was moved and the old number was left behind.
- Subsection numbering restarts from the wrong parent.

---

## Check 2 — TOC Completeness

A TOC that doesn't match the document body misleads readers: a phantom entry sends them nowhere, a missing entry hides content entirely.

Verify that every numbered heading in the document has a corresponding entry in the Table of Contents, and vice versa — no heading is missing from the TOC, and no TOC entry points to a non-existent heading.

**A document must have exactly one H1 heading.** Count all `# ` headings (excluding lines inside fenced code blocks). Flag if the count is zero or greater than one — list the line numbers of all H1 headings found. Do not auto-fix; the correct resolution depends on intent.

**H1 must not appear in the TOC.** Including the H1 in the TOC adds a spurious nesting level that pushes all real entries one indent deeper. If the TOC's root entry links to the H1, remove it and dedent all remaining entries by one level. (Only applies when the document has exactly one H1; if the H1 count is wrong, flag that first.)

**H1 must carry `<!-- omit in toc -->`.** Without this comment, TOC auto-generators (e.g., VS Code "Markdown All in One") will silently re-add the H1 to the TOC on the next regeneration. Auto-fix: append `<!-- omit in toc -->` to the H1 line if it is missing.

Example: `# My Guide` → `# My Guide <!-- omit in toc -->`

**The TOC heading itself must carry `<!-- omit in toc -->`.** The "Table of Contents" heading (or equivalent, e.g., `## Table of Contents`, `## Contents`) must not appear as an entry inside the TOC it introduces — that would be self-referential and meaningless. Without the comment, TOC auto-generators will silently re-add it on the next save. Auto-fix: append `<!-- omit in toc -->` to the TOC heading line if it is missing.

Example: `## Table of Contents` → `## Table of Contents <!-- omit in toc -->`

**How to check:**
1. Extract all headings (excluding the TOC heading itself and any `<!-- omit in toc -->` headings).
2. Extract all TOC entries.
3. Confirm a 1-to-1 match.

---

## Check 3 — TOC Anchor Links

Even a small mismatch in anchor case or punctuation silently breaks navigation in GitHub, GitLab, and most static site generators — the link renders fine but goes nowhere. Anchors must follow **GitHub-Flavored Markdown (GFM) rules** exactly.

**GFM anchor rules:**
1. Strip inline code backticks, keeping the inner text.
2. Convert to lowercase.
3. Remove every character that is not a letter, digit, space, or hyphen.
4. Replace each space with a hyphen — one-to-one, so two adjacent spaces become `--`.

**Examples:**
- `## 2. Phase A — Scaffold a Project` → `#2-phase-a--scaffold-a-project`
- `### 1.1. Install \`agents-cli\`` → `#11-install-agents-cli`

The em-dash `—` is stripped, but the spaces on either side remain, producing `--` in the anchor. This is the most common source of anchor bugs in technical docs.

Compare each computed anchor against what the TOC actually contains. Fix any mismatch.

---

## Check 4 — HTML Anchor Validity

Some documents use `<a id="..."></a>` anchors for cross-references not tied to headings. Orphaned anchors (defined but never linked) add noise; broken references (linked but undefined) leave readers stranded.

1. Collect every `<a id="...">` definition.
2. Collect every `(#...)` reference that targets one of those IDs (i.e., not a heading anchor).
3. Verify every reference has a matching definition, and every definition has at least one reference.

Report orphaned anchors and broken references.

---

## Check 5 — Spelling (Tech-Aware)

Misspelled prose erodes credibility. Tech docs are full of identifiers, product names, and domain jargon that a naive spellchecker would flag — strip those before scanning so you're only catching genuine mistakes.

Extract prose text by stripping:
- Fenced code blocks (` ``` `)
- Inline code (`` ` `` ... `` ` ``)
- URLs (`https?://...`)
- HTML tags
- Markdown link syntax `[text](url)`
- Markdown image syntax `![alt](url)`

Then scan the remaining prose for spelling errors.

**Do not flag:**
- Technical abbreviations: CLI, SDK, API, GCP, ADK, CI/CD, LLM, IDE, GKE, IAM, HTTP, URL, JSON, YAML, etc.
- Tool/product names: Terraform, Kubernetes, Dockerfile, Vertex AI, Cloud Run, Cloud Build, etc.
- Package/command names: `uvicorn`, `fastapi`, `pyproject`, `evalset`, `rubric`, etc. (even when appearing outside backticks in prose)
- File extensions and paths discussed in prose: `.env`, `.gitignore`, `.json`, etc.
- Domain jargon standard in the field: observability, evalset, rubrics, symlink, subcommand, metadata, hot-reload, etc.
- Intentional informal register (e.g., "Gotcha" in a "Key Gotchas" section)

**Do flag:**
- Misspelled common English words (e.g., `explicity` → `explicitly`, `recieve` → `receive`)
- Accidentally merged words (e.g., `Withose` → `With those`)

If `aspell` or `hunspell` is available, run:
```bash
cat <file> | aspell list --lang=en_US --mode=markdown | sort -u
```
and filter the output against the tech-term allowlist above. Otherwise, extract and scan prose manually using a Python/sed script.

---

## Check 6 — Basic Prose Grammar

Common grammar slips — missing prepositions, duplicate words, subject-verb disagreement — often survive drafting because readers unconsciously self-correct while reading. Explicit checking catches them.

While extracting prose for spelling (Check 5), also scan for:
- Missing prepositions (e.g., `resulting this` → `resulting in this`)
- Missing articles where clearly required (e.g., `in previous section` → `in the previous section`)
- Subject-verb agreement errors
- Duplicate words (e.g., `the the`)

**Do not flag:**
- Intentional terse style common in technical writing (omitting articles is sometimes acceptable)
- Non-native phrasing that is unambiguous and readable

---

## Check 7 — File Link Validity

Broken file links are silent — they render as valid Markdown but produce missing images or dead navigation when the document is viewed. Checking them catches moves, renames, and copy-paste errors that no other check covers.

Collect every link whose target is a local file path — that is, any `![alt](target)` or `[text](target)` where `target` is **not** a URL (does not start with `http://` or `https://`) and **not** an in-document anchor (does not start with `#`).

For each such link:
- If the path is relative, resolve it relative to the directory containing the document being checked.
- If the path is absolute, use it as-is.
- Check whether the file exists on disk.

Report every link whose target file does not exist. Do not attempt to auto-fix — the correct path is unknowable without the user's input.

**Examples of targets to check:**
- `./images/diagram.png`
- `../shared/glossary.md`
- `/Users/vyin/docs/setup.md`
- `images/screenshot.jpg` (no leading `./`, still relative)

**Examples of targets to skip:**
- `https://example.com/docs` (URL)
- `http://localhost:8080` (URL)
- `#section-heading` (in-document anchor)

---

## Check 8 — Image Alt Text

Empty alt text on images (`![](...) `) silently degrades accessibility and makes images unidentifiable when they fail to load. Every local image link must have non-empty alt text.

**How to check:**
1. Collect every image link `![alt](target)` where `target` is a local file path (not a URL, not an anchor).
2. If `alt` is empty, auto-fix by setting it to the filename portion of `target` (i.e., the last path segment, including extension).

**Example:**
- `![](images/agents-cli-deploy-to-agent-runtime.png)` → `![agents-cli-deploy-to-agent-runtime.png](images/agents-cli-deploy-to-agent-runtime.png)`

**Do not flag:**
- Images with non-empty alt text, even if the alt text doesn't match the filename.
- Remote images (URLs) — their alt text is out of scope for this check.

---

## Check 9 — Protocol Layering Precision

In diagrams and prose, protocols are often written as `X / Y` when X is actually a higher-level protocol defined on top of Y. That slash is ambiguous: it could mean "either X or Y", "X plus Y", or "X over Y" — three different things. When the relationship is layering, make it explicit.

**Rule:** When a label or phrase uses `X / Y` where X is a protocol defined on top of Y, replace it with `X (over Y)`.

**How to check:**
1. Scan all diagram text — arrow labels, node labels, table cells, and prose — for the pattern `<Term> / <Term>`.
2. For each match, determine the relationship between X and Y:
   - If X is a protocol layered on top of Y → rewrite as `X (over Y)`.
   - If the slash means "either one" → rewrite as `X or Y`.
3. This applies equally to node labels (e.g., `Gemini Enterprise or Orchestrator Agent`, not `Gemini Enterprise / Orchestrator Agent`) and arrow labels.

**Examples:**

| Before | After | Why |
|---|---|---|
| `HTTP / A2A` | `A2A (over HTTP)` | A2A is a protocol spec that runs on top of HTTP |
| `MCP / HTTPS` | `MCP (over HTTP)` | MCP (Model Context Protocol) is defined on top of HTTP |
| `OTLP / gRPC` | `OTLP (over gRPC)` | OTLP is the OpenTelemetry wire format; gRPC is its transport |
| `REST / HTTPS` | `REST (over HTTPS)` | REST is an architectural style applied over HTTPS |
| `Gemini Enterprise / Orchestrator Agent` | `Gemini Enterprise or Orchestrator Agent` | Two alternative callers, not a layered relationship — use "or" |

**Do not flag:**
- `HTTP or gRPC` — the word "or" already makes the choice explicit.
- `TCP/IP` — this is a single compound name, not a slash-ambiguity case.
- `CI/CD` — an established compound abbreviation, not a protocol expression.
- Established compound industry terms where the slash is part of the term itself, not a separator between two independent concepts (e.g., `no-code / low-code`, `read / write`, `input / output`). When in doubt, ask: would removing one side leave the other side meaningful in context? If the two sides form a recognized spectrum or pair, leave the slash.

---

## Check 10 — Heading Level Increments

Skipping a heading level (e.g., jumping from `#` directly to `###`) breaks the document outline and confuses screen readers and document parsers that rely on a strict hierarchy.

**Rule:** When traversing headings in document order, the level of each heading may exceed the previous heading's level by **at most 1**. Decreasing by any amount is allowed.

**How to check:**
1. Extract all headings in order (excluding lines inside fenced code blocks), recording each heading's level (number of leading `#` characters).
2. For each consecutive pair, if `current_level > previous_level + 1`, flag it.
3. Report the line number, the offending heading text, and the skip (e.g., "jumped from level 2 to level 4").

**Examples:**

| Previous heading | Current heading | Level change | Valid? |
|---|---|---|---|
| `## Section` (2) | `### Subsection` (3) | +1 | ✓ |
| `# Title` (1) | `## Section` (2) | +1 | ✓ |
| `### Sub` (3) | `# Top` (1) | −2 | ✓ (decreasing is always allowed) |
| `# Title` (1) | `### Sub` (3) | +2 | ✗ skips level 2 |
| `## Section` (2) | `##### Deep` (5) | +3 | ✗ skips levels 3 and 4 |

Do not auto-fix — the correct repair depends on intent (promote the child, demote the child, or insert an intermediate heading).

---

## Check 11 — Filename vs. Title Agreement

A document's filename is often used as a URL slug or navigation label. When it drifts from the H1 title, external references and breadcrumbs become misleading.

**Rule:** The slug derived from the filename must match the slug derived from the H1 title. Flag any mismatch; do not auto-fix (renaming a file is a destructive filesystem operation).

**Slug derivation — apply identically to both the filename (minus `.md` extension) and the H1 title text:**
1. Strip inline code backticks, keeping the inner text.
2. Convert to lowercase.
3. Remove every character that is not a letter, digit, space, or hyphen.
4. Replace each space with a hyphen (one-to-one).

**How to check:**
1. Take the bare filename (strip the `.md` extension).
2. Take the text of the first `# ` heading in the document body.
3. Apply the slug rules to both.
4. If the two slugs differ, report: the filename slug, the title slug, and the specific mismatch.

**Examples:**

| Filename | H1 Title | Filename slug | Title slug | Match? |
|---|---|---|---|---|
| `my-caveman-agent4.md` | `# My Caveman Agent4` | `my-caveman-agent4` | `my-caveman-agent4` | ✓ |
| `devops-guide.md` | `# DevOps Guide` | `devops-guide` | `devops-guide` | ✓ |
| `deploy-guide.md` | `# Deployment Guide` | `deploy-guide` | `deployment-guide` | ✗ |
| `agents_cli_setup.md` | `# Agents CLI Setup` | `agents-cli-setup` | `agents-cli-setup` | ✓ (underscore→hyphen via rule 4) |

**Do not flag:**
- Filenames that are intentionally abbreviated (judgment call — just report the mismatch so the user can decide).

**Always flag:**
- Documents with no H1 heading — report as "missing H1 title".
- Documents with more than one H1 heading — report as "multiple H1 titles" and list their line numbers. When there are multiple H1s, the slug comparison is undefined; skip the slug check and flag the H1 count issue only.

---

## Execution Order and Summary

Run checks in this order; fixing as you go ensures later checks see the corrected state:

1. Section Numbering
2. TOC Completeness
3. TOC Anchor Links
4. HTML Anchor Validity
5. Spelling
6. Basic Prose Grammar
7. File Link Validity
8. Image Alt Text
9. Protocol Layering Precision
10. Heading Level Increments
11. Filename vs. Title Agreement

After all checks, report:

| Check | Issues Found | Fixed |
|-------|-------------|-------|
| Section Numbering | N | N |
| TOC Completeness | N | N |
| TOC Anchor Links | N | N |
| HTML Anchor Validity | N | N |
| Spelling | N | N |
| Prose Grammar | N | N |
| File Link Validity | N | N |
| Image Alt Text | N | N |
| Protocol Layering Precision | N | N |
| Heading Level Increments | N | — |
| Filename vs. Title Agreement | N | — |

If any issue required a judgment call and was not auto-fixed, list it explicitly below the table.

---

## On-Demand: Package Document into a ZIP

**Only do this when the user explicitly asks** — e.g., "package the doc into a ZIP file", "ZIP up this doc", "create a zip file for this doc". Do NOT run this automatically as part of the consistency check.

Creates a ZIP archive containing the document and all locally referenced image files, preserving the relative folder structure so images load correctly when extracted anywhere.

Run from the directory containing the document:

```bash
cd "<doc-directory>" && \
zip -j "<doc>.zip" "<doc>" && \
grep -o '](images/[^)]*' "<doc>" | sed 's/^](//' | sort -u | while read img; do
  zip "<doc>.zip" "$img"
done
```

The `-j` flag places the document at the ZIP root (no parent path). The image loop adds each image under its relative `images/` path. Only files actually referenced in the document are included — not the entire `images/` folder.

**Naming:** Same as the document filename (e.g., `My Guide.md` → `My Guide.zip`), placed in the same directory.
