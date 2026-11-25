---
name: openarc
description: Use when a user asks to use OpenArc generally, initialize governance, improve repository continuity, audit governance drift, migrate an existing workspace, or choose which OpenArc skill should handle a request.
---

# OpenArc Entry

Use this as the first stop when the user says "use OpenArc" or asks for repository governance without naming a specific skill.

## Fast Routing

Map the user's request to the narrowest skill:

| User Intent | Use |
| --- | --- |
| "Set up OpenArc here" | `repository-governance`, then profile-specific governance skills as needed |
| "What is missing?" / "Audit this repo" | `repository-governance` in read-only audit mode, then run the scan helper if available |
| "Clarify this request" / "New feature" / "New goal" | `clarification-gate`, then route to PRD, spec, plan, or implementation |
| "Fix this bug" / routine implementation | Implement directly when scope, constraints, and validation are clear |
| "Write PRD" | `product-governance` |
| "Write spec" | `spec-workflow` |
| "Plan implementation" | `planning-engine` |
| "Define design system" | `design-governance` |
| "Define brand" | `brand-governance` |
| "Organize assets" | `assets-governance` |
| "Migrate existing workspace" | `workspace-migration` |
| "Version this change" | `version-governance` |
| "Branch, commit, or PR" | `release-workflow`; stop after the requested git/PR work |
| "Release or publish" | `release-workflow`; require an explicit release request and confirmation |
| "Prepare for open source" | `open-source-maintenance` |

## Default First Pass

For a new or unfamiliar repository:

1. Scan existing files before writing.
2. Use the detected `repo_profile` to separate required, relevant, and optional governance.
3. For an `unknown` profile, use only a README and one agent guide as the minimum baseline; report missing files, but create them only when setup is explicitly requested. Do not infer product, design, brand, spec, plan, task, or archive needs from the profile alone.
4. Report what already exists, what is profile-relevant missing, and what conflicts.
5. Choose the smallest next action:
   - direct implementation for routine work with clear scope and validation
   - clarification only for material unknowns
   - one spec when behavior, acceptance criteria, or compatibility needs durable alignment
   - one plan when sequencing, migration, rollback, or validation risk needs structure
   - `docs/TASKS.md` only for work spanning multiple stages, people, or agents
   - bootstrap or migration only when explicitly requested
6. Ask only for decisions that materially affect output.

## Helper Scripts

If this plugin's `scripts/openarc.py` is available, prefer:

```bash
python3 plugins/openarc/scripts/openarc.py scan .
python3 plugins/openarc/scripts/openarc.py doctor plugins/openarc
```

Use script output as evidence, not as a replacement for judgment.

## Rules

- Do not load every OpenArc skill by default.
- Treat audit, review, scan, and "what is missing?" requests as read-only. Report findings without creating or modifying files.
- Write governance files only when the user explicitly requests setup, initialization, apply, repair, or migration work.
- A branch, commit, or PR request does not authorize a release. Trigger or publish a release only after an explicit release request and confirmation.
- Do not create all governance docs unless the user asks for full setup.
- Do not make governance setup, a spec, a plan, or tasks prerequisites for routine implementation.
- Use `clarification-gate` before PRD, spec, plan, or implementation work only when material product, behavior, compatibility, migration, or risk decisions remain unresolved.
- Use `docs/specs/*` as the canonical spec location and `docs/TASKS.md` as the canonical active task source.
- Do not require `docs/DESIGN.md`, `docs/BRAND.md`, or `docs/assets/*` for script, CLI, automation, library, or docs-only repositories unless the repo already has UI or brand signals.
- Prefer a small first useful artifact over a complete governance dump.
- Existing repository conventions win over OpenArc templates.
