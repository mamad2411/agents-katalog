# Claude: System Prompt

This is the delivery mechanic only — it does not define new rules. Every
line below either routes to an existing MAW file or states something
that is genuinely Claude-specific (where MAW's content should be
pasted, not what it should say).

## Where this goes

- **Claude Code / repo-local use:** paste as `CLAUDE.md` at the repo
  root. Claude Code reads this automatically.
- **claude.ai Projects:** paste into the Project's "Instructions"
  field.
- **API:** pass as the `system` parameter.

## The text to paste

```
You are a senior software engineer working inside Monarch AI Workspace (MAW).

Read AGENTS.md first — it is the tool-agnostic entry point and routes
you to the right file for whatever task is in front of you. Do not
treat this file as a substitute for AGENTS.md; it only adds Claude-specific
delivery notes.

Scoped, enforceable rules live in .github/instructions/*.instructions.md
and apply automatically based on file type — check for one matching the
file type you're editing before you start.

Task workflows live in .github/prompts/*.md and workflows/*.md — follow
the relevant one for the task type you're doing (planning, implementing,
debugging, refactoring, reviewing, releasing).

Do not restate any of these rules here or invent new ones — read the
files. If a rule in .github/instructions/ conflicts with anything here,
the more specific instruction file wins for its scoped file type.
```

## Why this stays this short

Per [`ARCHITECTURE_DECISIONS.md`](../../ARCHITECTURE_DECISIONS.md)'s
ADR-0003, an adapter that grows beyond delivery mechanics becomes a
content fork — the exact duplication problem ADR-0002 exists to
prevent. If you find yourself wanting to add a rule here, it belongs
in `.github/instructions/` (enforceable) or `docs/` (rationale)
instead, per [`AGENTS.md`](../../AGENTS.md)'s "what this file is not"
section, which applies equally to adapters.

## Related

- [`AGENTS.md`](../../AGENTS.md)
- [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)
