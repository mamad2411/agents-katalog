---
name: joss-audit
description: >-
  Evaluate an R or Python package and its paper.md against the full JOSS
  reviewer checklist. Launches the joss-reviewer agent (software, community,
  and field specialists in parallel) and returns a gap report with
  Critical, Major, and Minor findings, then offers fixes.
argument-hint: "[package path]"
---

# JOSS Submission Audit

Thin launcher: the audit workflow lives in the `pub-pipeline:joss-reviewer` agent. This skill gathers context, dispatches it, answers its questions in the main session (subagents cannot ask the user), and offers fixes.

## 1. Gather context (Read tool)

- Package root: `$ARGUMENTS` if given, else the current directory (must contain `DESCRIPTION` or `pyproject.toml`).
- Read `.claude/pub-pipeline.local.md` if it exists. If missing, offer to create it from `${CLAUDE_PLUGIN_ROOT}/docs/user-config-template.md`.

## 2. Dispatch (Agent tool)

Launch `subagent_type: pub-pipeline:joss-reviewer` with:

```xml
<context>
<package_root>[absolute path]</package_root>
<user_config>[frontmatter of .claude/pub-pipeline.local.md, or "none"]</user_config>
</context>
```

## 3. Present and resolve

Present the report. If it ends with a **Decisions Needed** block, ask the user each question; when an answer changes a checklist result (e.g. confirming the submitting author is a major contributor), update that item yourself. Re-dispatch only if an answer requires new evidence to be gathered.

## 4. Offer to fix

Offer the automatable fixes the report calls for:
- No `paper.md` or weak sections: `/pub-pipeline:joss-draft`
- Add `CONTRIBUTING.md` (bug reports, PRs, support)
- Add missing ORCID fields, fix frontmatter (`%e %B %Y` date), add the AI usage disclosure section
- Add missing BibTeX entries sourced from DOIs

Re-run this audit after fixes.
