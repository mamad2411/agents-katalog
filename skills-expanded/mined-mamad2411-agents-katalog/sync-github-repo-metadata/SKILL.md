---
name: sync-github-repo-metadata
description: Inspect a repository and propose or apply GitHub About metadata updates. Use when Codex needs to infer a concise repository description and topic set from source code, package metadata, docs config, or the current README, then preview and optionally run `gh repo edit`.
---

# Sync GitHub Repo Metadata

Use the repository and its configuration as the source of truth. Treat the current README, docs, and existing GitHub metadata as weak hints unless they still match the codebase.

## Workflow

1. Gather repo facts.
2. Read the current remote metadata with:
   - `gh repo view --json nameWithOwner,description,repositoryTopics,homepageUrl,url`
3. Infer:
   - one concise repository description
   - a focused topic set based on actual language, framework, domain, and tooling
4. Preview the current values, proposed values, and the exact `gh repo edit` command.
5. Apply changes only after explicit confirmation.

## Guidelines

- Do not change homepage or other repo settings unless the user explicitly asks.
- Focus on GitHub description and topics only.
- Prefer a single-sentence description that matches the repo's real purpose.
- Prefer accurate, specific, stable topics over broad buzzwords.
- Prefixing description with an emoji is encouraged.
- Remove stale topics instead of only appending new ones.
- Use lowercase kebab-case topics.

## Preview Format

- Current description
- Proposed description
- Current topics
- Proposed topics
- Exact `gh repo edit` command with `--description`, `--add-topic`, and `--remove-topic` arguments as needed

## Apply Step

- Never apply blindly.
- After confirmation, run the exact previewed command.
- If authentication or permissions fail, report the command and the failure instead of guessing an alternative.
