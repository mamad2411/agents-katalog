---
name: memory-publication-auditor
description: Audit private skills, memories, notes, or operational logs before turning them into public skills, templates, docs, or reusable patterns. Use when scanning personal/private memory for publishable knowledge, redaction needs, privacy risks, source-visibility leaks, or PR-ready public skill candidates.
argument-hint: "[private-path ...] [--output .agent/publication-audits/<id>/audit.md]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Memory Publication Auditor

Audit private experience before publication. This skill answers: **Which private memory or skill content can become public knowledge, and what must stay private or be redacted?**

This is not a copying skill. It is a conservative sieve: private material comes in, sanitized reusable patterns may come out.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── scripts/
│   └── scan_publication_candidates.py
├── references/
│   └── classification-policy.md
└── templates/
    ├── audit-report.md
    └── publication-candidate.md
```

## Core Contract

- Default to `private-only` or `needs-human-review` when uncertain.
- Never publish account names, usernames, hostnames, private IPs, tokens, local paths, private server names, unpublished project details, collaborator identities, or raw trajectories.
- Distinguish **private facts** from **publishable operational patterns**.
- Produce an audit report first; only draft public skills/docs from sanitized candidates.
- Keep audit artifacts local/private by default under `.agent/publication-audits/`.

## Classification Labels

- `private-only`: cannot be published, even with light edits.
- `redactable`: useful pattern exists, but private identifiers or context must be replaced.
- `publishable`: safe as written, after normal quality review.
- `reusable-pattern`: abstract method, workflow, checklist, or diagnostic pattern worth turning into a public skill/template.
- `needs-human-review`: ambiguous ownership, privacy, copyright, collaborator, or unpublished-project risk.

## Workflow

1. Read `references/classification-policy.md`.
2. Identify input paths: private skill directories, memory files, notes, sidecar decisions, or sanitized logs.
3. Run the deterministic scanner when scanning files:

```bash
python3 <installed-skill-dir>/scripts/scan_publication_candidates.py \
  --input <private-path> \
  --output .agent/publication-audits/<audit-id>/audit.md
```

4. Review the report before reading raw private files in detail.
5. Classify each candidate:
   - private facts -> keep private
   - private facts plus reusable method -> draft a redacted pattern
   - already generic workflow -> mark publishable
6. If drafting a public artifact, fill `templates/publication-candidate.md` and replace all private specifics with placeholders.
7. Route next:
   - public skill candidate -> create manually or use `skill-system-auditor` to check collection fit before adding
   - docs/template candidate -> `update-docs`
   - private preference -> `personalization-memory`
   - source-visibility risk -> `research-project-memory`

## Output Rules

- Audit reports may contain redacted evidence snippets, not raw secrets or private context.
- Public candidates must use placeholders such as `<host>`, `<target-ip>`, `<project-root>`, `<user>`, `<cluster>`, and `<private-path>`.
- Do not include concrete private examples from the source material just to make the public version vivid.
- If a claim depends on private evidence, say "derived from private operational memory" rather than exposing the evidence.
