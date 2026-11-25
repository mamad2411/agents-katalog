---
name: new-source
description: Add a literature source beyond ACL Anthology and arXiv (e.g. Semantic Scholar, ACM DL, OpenReview, PubMed) as a project skill with its own adapter.
disable-model-invocation: true
argument-hint: "Which source? (name or URL)"
---

Build a project-local source: an adapter the core scripts call, plus a skill that tells the agent when and how to use it. It lives in the paper project, not in the plugin.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

## 1. Pin down the source

Research the source's public API: search endpoint, how to get a PDF, and where an **authoritative BibTeX entry** comes from (an export endpoint, a DOI resolved via `https://doi.org/<doi>` with `Accept: application/x-bibtex`, DBLP). A source without an authoritative BibTeX route cannot be added as is: say so and offer the fallback (search and PDF here, entries pasted by the user via `bib-paste`).

Also find the source's rate limits, API key requirements and terms of use. Show the user what you found and agree on the source name (kebab-case, e.g. `semantic-scholar`) before writing code. An API key goes in an environment variable the adapter reads, never in a file.

## 2. Write the adapter

Copy `${CLAUDE_SKILL_DIR}/adapter_template.py` to `.claude/skills/<name>-source/adapter.py` and implement the three functions. The docstring of `${CLAUDE_PLUGIN_ROOT}/scripts/paperkit/sources.py` defines the contract, and `${CLAUDE_PLUGIN_ROOT}/scripts/sources/arxiv_source.py` is a worked example. Keep the adapter to fetching: duplicate checks, files, notes and bib handling belong to the core.

Third-party packages go in `REQUIRES`. Ask before installing them into the project env (`python` in `paper.config.json`).

## 3. Register and test

Add `"<name>": ".claude/skills/<name>-source/adapter.py"` under `sources` in `paper.config.json`. Ask the user for a paper they know is on the source, then run:

```
PK test-source <name> "<query matching that paper>" <its id>
```

Every line must read ✅. `PK doctor` must list the source without ⚠️.

## 4. Write the project skill

Create `.claude/skills/<name>-source/SKILL.md`, modelled on `${CLAUDE_PLUGIN_ROOT}/skills/arxiv/SKILL.md`:

- frontmatter `name: <name>-source` and a description that names the source and the cases that should reach it (paper types, id formats, URLs)
- the search command with the query syntax the source supports and its rate limit
- the add command, and a pointer to the `literature` skill for reading and citing

Finish by showing the user the two files and the config change.
