---
name: ask
description: "[OMCP] Process-first advisor routing for Claude, Codex, or Gemini via `/omcp:ask`, with artifact capture and no raw CLI assembly"
---

# Ask

Use omcp's canonical advisor skill to route a prompt through the local Claude, Codex, or Gemini CLI and persist the result as an ask artifact.

## Usage

```bash
/omcp:ask <claude|codex|gemini> <question or task>
```

Examples:

```bash
/omcp:ask codex "review this patch from a security perspective"
/omcp:ask gemini "suggest UX improvements for this flow"
/omcp:ask claude "draft an implementation plan for issue #123"
```

## Routing

**Required execution path — always go through this `/omcp:ask` skill:**

```bash
/omcp:ask {{ARGUMENTS}}
```

This skill *is* the advisor wrapper: follow the procedure below to select the
provider, build a minimal correct invocation, run it, and persist the artifact.
**Do NOT bypass this routing by improvising raw provider CLI flags ad hoc.**
Parse `{{ARGUMENTS}}` as `<provider> <question>`, confirm the provider CLI is
installed (see Requirements), invoke it with the question, then write the result
to the artifact path below. This keeps flag selection, artifact persistence, and
provider-version handling consistent across every advisor call.

> This plugin ships no standalone `omc`/`omcp` advisor binary — the `/omcp:ask`
> skill body is the authoritative routing path.

## Requirements

- The selected local CLI must be installed and authenticated.
- Verify availability with the matching command:

```bash
claude --version
codex --version
gemini --version
```

## Artifacts

`/omcp:ask` writes artifacts to:

```text
.omcp/artifacts/ask/<provider>-<slug>-<timestamp>.md
```

Task: {{ARGUMENTS}}
