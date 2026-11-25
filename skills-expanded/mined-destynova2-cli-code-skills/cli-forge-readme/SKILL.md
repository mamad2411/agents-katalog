---
name: cli-forge-readme
metadata:
  author: clement
description: "Use this skill whenever the user wants to create, improve, audit, or rewrite a README.md file for any project. Triggers include: 'readme', 'README', 'documentation for my project', 'write a readme', 'improve my readme', 'project landing page', or any request to document a codebase, library, CLI tool, infrastructure project, or research repo. Also triggers when the user asks to 'make my project more accessible', 'add a getting started guide', or wants badges, installation instructions, or contributing guidelines. Use this skill even when the user just says 'document this' or 'make this repo presentable'. Do NOT use for API reference docs generation, full documentation sites (mdbook, docusaurus), or man pages."
argument-hint: "[project-path]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the README in that language. If the project is bilingual, ask the user which language to use before proceeding.

> **Diacritics rule:** When the chosen output language uses diacritics (French, Spanish, Portuguese, etc.), render them correctly — including on capitals (É, À, Ç, Ô…). Never strip accents to ASCII: write "sécurité" not "securite", "Rôle" not "Role". ASCII-flattened French is a defect, not a style.

> **Writing style:** Favor clarity — short sentences, one idea per sentence, plain words. A metaphor only when it clarifies. Keep one consistent register (impersonal/infinitive for operational docs). Separate narrative prose, meant to make the reader understand, from telegraphic content (tables, commands, checklists) which stays terse for action.

> **No fabricated output:** Never invent command output, console captures, API responses, metrics, or logs. When real output is needed, emit a clearly-marked placeholder (🚧 "replace with a real capture"), never plausible-but-fake text presented as real.

# README Generator — Production First

Generate professional README.md files where **results come first, plumbing comes second**.

**Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Philosophy

A README is a **landing page**, not a technical manual.
- 90% of visitors want to know: what, why, how to start
- 10% want to contribute or understand internals
- Structure for the 90%, don't punish them with the 10%

**Tone rule: Friendly on the surface, technical in depth.**
- Tier 1–2: plain language, no jargon, a junior dev or a PM can understand
- Tier 3: full technical depth, assume the reader codes

## Workflow

### Step 1 — Detect project context

Build the shared reconnaissance brief first — read `../shared/recon.md` (what / who / problem / headline / differentiator / golden-path). The same brief feeds prez and demo, so the README, slides, and live demo tell one story.

Then read the project root to auto-detect the type:

| Signal | Project Type |
|--------|-------------|
| `Cargo.toml` | `rust-lib` or `rust-cli` (check `[[bin]]`) |
| `go.mod` | `go-lib` or `go-cli` |
| `package.json` | `js-lib`, `js-app`, or `js-cli` (check `bin` field) |
| `pyproject.toml` / `setup.py` | `python-lib` or `python-cli` |
| `*.tf` / `terragrunt.hcl` | `infra-terraform` |
| `helmfile.yaml` / `Chart.yaml` | `infra-helm` |
| `docker-compose*.yml` + app code | `app-backend` |
| `Containerfile` / `Dockerfile` | `container` |
| `kustomization.yaml` | `kustomize` (+`flux` if `flux-system/`) |
| `site.yml` / `playbooks/` / `roles/` | `ansible` |
| `*.sh` + no other code | `shell-scripts` |

**If nothing detected** → ask user with QCM (project type, language, deployment status).

### Step 2 — Gather content

1. Read existing files: README.md, CHANGELOG, LICENSE, CI configs, manifest
2. Only ask for what's missing
3. Find the hero moment: the ONE thing that makes someone go "I need this"

### Step 3 — Write using the 3-Tier Pyramid

Read `references/pyramid.md` for the detailed tier structure, rules, and badge templates.

| Tier | Audience | Content |
|------|----------|---------|
| **1 — Hook** | Everyone | Project name, one-liner, badges, visual |
| **2 — Get Started** | Most people | Quickstart (3 cmds max), features (5 max), examples with output |
| **3 — Contribute** | Devs / QA | Project structure, dev setup, architecture, contributing, license |

Then apply project-type-specific adaptations. Read `references/project-types.md` for per-type customization.

## Formatting Standards

1. `#` = project name only. `##` = sections. `###` = subsections. Never deeper than `####`
2. Code blocks: always specify language (`bash`, `rust`, `yaml`...)
3. Tables: for structured data only (env vars, flags, endpoints). Never for prose
4. Links: relative for in-repo, absolute for external
5. Target length: Tier 1+2 fit in ~3 screen heights. Tier 3 can expand
6. No empty sections: if nothing to say, omit entirely. No TODOs in shipped READMEs

## Quality Scoring — README Completeness Index (RCI)

```
RCI = Σ(wᵢ × sᵢ) / Σ(wᵢ) × 10
```

| # | Item | Weight |
|---|------|--------|
| 1 | Hook / one-liner | 5 |
| 2 | Quickstart | 5 |
| 3 | Install instructions | 4 |
| 4 | Usage examples | 4 |
| 5 | Badges | 2 |
| 6 | Project structure | 3 |
| 7 | Configuration | 3 |
| 8 | Contributing | 2 |
| 9 | License | 1 |
| 10 | Visual result | 3 |

**Scoring:** 0.0=absent, 0.25=stub, 0.5=exists but weak, 0.75=good, 1.0=excellent

**Thresholds:** 8+ excellent, 6-8 good, 4-6 needs work, <4 incomplete

## Output

- Write to project root as `README.md`
- Show a brief summary: which tier sections were generated, what's missing/skipped
- Output the RCI table at the end of the review

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Project needs full docs, not just README | `/cli-forge-doc` | Full documentation generation |
| Architecture diagram needed | `/cli-forge-schema` | Generate Mermaid |
| Commands section has untested scripts | `/cli-audit-shell` | Verify scripts work |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relation |
|-------|----------|
| `/cli-forge-tree` | Generate the "Project Structure" section automatically |
| `/cli-forge-schema` | Generate the diagrams embedded in the README |
| `/cli-forge-doc` | The README is the entry point for the full documentation |
| `/cli-audit-doc` | Audit the quality of the generated README |
| `/cli-audit-sync` | Verify that the README stays coherent with the code |
| `/cli-cycle` | Included in the cycle's documentation audit |
