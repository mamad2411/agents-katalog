---
name: joss-draft
description: >-
  Draft a JOSS paper (paper.md and paper.bib) for an R or Python package.
  Launches the joss-writer agent, which reuses existing manuscripts and
  maps competing packages, then resolves anything only the author can
  supply (ORCID, AI usage, funding).
argument-hint: "[package path]"
---

# JOSS Paper Drafting

Thin launcher: the drafting workflow lives in the `pub-pipeline:joss-writer` agent. This skill gathers context, dispatches it, and answers its questions in the main session (subagents cannot ask the user).

## 1. Gather context (Read and Bash tools)

- Package root: `$ARGUMENTS` if given, else the current directory (must contain `DESCRIPTION` or `pyproject.toml`).
- Read `.claude/pub-pipeline.local.md` if it exists. If missing, offer to create it from `${CLAUDE_PLUGIN_ROOT}/docs/user-config-template.md` (author, `ai_usage`, and `related_work` feed the paper directly).
- Author metadata: config `author`/`coauthors` first, then `deets show --format json` if available.

## 2. Dispatch (Agent tool)

Launch `subagent_type: pub-pipeline:joss-writer` with:

```xml
<context>
<package_root>[absolute path]</package_root>
<author_metadata>[name, ORCID, affiliation, email for each author, as found]</author_metadata>
<user_config>[frontmatter of .claude/pub-pipeline.local.md, or "none"]</user_config>
</context>
```

## 3. Resolve decisions

Show the agent's draft summary. If it returns a **Decisions Needed** block, ask the user each question (AskUserQuestion when the options are discrete), then re-dispatch the writer with the same context plus:

```xml
<answers>
1. [id]: [user's answer]
</answers>
```

Repeat until no decisions remain or the user chooses to fill the placeholders by hand.

## 4. Next step

Offer `/pub-pipeline:joss-audit` for a full review of the draft against the JOSS checklist.
