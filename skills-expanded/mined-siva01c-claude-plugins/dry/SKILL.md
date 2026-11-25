---
name: dry
description: >
  DRY (Don't Repeat Yourself) review rules for code reviews: find the same knowledge — a rule, a
  constant, a parser, a validation, a protocol detail — implemented in several places that must
  change together, and tell it apart from code that merely looks alike. Use when reviewing a
  diff, a pull request or recent changes for duplication, on "DRY review", "is this
  duplicated", "copy-paste check", or when a review checklist asks for DRY. Pair it with the
  solid skill for design and with owasp-asvs for security.
---

# DRY Review

DRY is about **knowledge, not text**. A finding is the same decision encoded in two or more
places that have to change together — so that changing one and forgetting the other is a bug
waiting to happen. Two blocks of similar-looking code that encode *different* decisions are not
duplication, and merging them would couple things that should vary independently.

## What to look for

- **Rules and validation** — the same allow-list, regex, limit or permission check in a form,
  an API endpoint and a CLI command.
- **Constants and magic values** — a status name, a timeout, a URL, a field name or a path
  spelled out in several files instead of defined once.
- **Parsers and formats** — two hand-written parsers or serializers for the same file, header,
  JSON shape or command output.
- **Protocol details** — the same auth header, retry policy, pagination loop or error mapping
  re-implemented per client.
- **Copied functions** — a helper copied into a second module with small edits, where both
  copies are still meant to behave the same.
- **Docs and code** — a procedure described in two documents, or a value documented in a README
  and hard-coded elsewhere, when both must stay in sync.

In a diff, check first whether the change **adds** a copy of something that already exists in
the codebase: search for the key identifiers, strings and regexes it introduces.

## Not a finding

- Similar code that encodes different decisions, or would diverge on the next change.
- Two or three lines of glue, test setup or boilerplate the framework expects.
- Tests that restate expected values on purpose.
- Duplication across separately released projects (a public library and a private monorepo)
  that are deliberately kept standalone.
- Generated, vendored and lock files.

## Severity

- `high` — the copies have **already drifted**: they disagree today, and you can show the input
  that behaves differently in each.
- `medium` — default: the copies are identical now but must change together, and nothing ties
  them.
- `low` — small repeated literals or helpers where a mismatch would be cosmetic.

## Reporting a finding

Each finding carries:

- **rule** — `DRY`;
- **locations** — `file:line` of **every** copy, not just the one in the diff;
- **knowledge** — one sentence naming the single decision the copies share;
- **cost** — what goes wrong when one copy changes and the other does not (or already has);
- **fix direction** — where the one source of truth should live, preferring an existing module,
  config or constant over a new abstraction.

Verify each finding by reading all copies side by side before keeping it. Fewer, true findings
beat a long list.
