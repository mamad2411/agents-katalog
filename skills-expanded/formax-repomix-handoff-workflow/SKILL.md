---
name: formax-repomix-handoff-workflow
description: "Use when preparing a Formax code handoff: selecting files, generating repomix bundles, and writing a high-quality prompt for WebGPT or another coding agent with clear constraints and validation scope."
---

# formax-repomix-handoff-workflow

## Goal
Create a clean handoff package for another AI with:
- the smallest correct repomix bundle
- a prompt that matches the target environment
- explicit acceptance criteria and non-goals
- predictable artifact naming + validation (so uploads stay consistent)

## Where to change what
- All handoff artifacts live in one folder: `repomix-output/`
- Bundle output: `repomix-output/repomix-<topic>-<tier>.txt`
- Handoff prompt: `repomix-output/<topic>-handoff-prompt.md`
- File manifest notes: `repomix-output/repomix-<topic>-files.md`
- Template references: `references/prompt-templates.md`

> Required hygiene: each new pack run must clear previous files in `repomix-output/` first, so users can upload that folder as-is without manual file picking.

## Pack tiers (default taxonomy)
Use exactly one tier label in bundle filename:

- `minimal`: changed runtime files + direct dependencies + adjacent tests.
- `core`: `minimal` + only critical contract/design docs needed for intent.
- `full`: broad context pack for deep investigations (cross-subsystem docs/tests).

Example names:
- `repomix-topic-minimal.txt`
- `repomix-topic-core.txt`
- `repomix-topic-full.txt`

## Patterns
1. Classify target runtime first
- `Static consumer` (e.g., WebGPT): cannot run local commands or tests.
- `Executable agent` (repo access): can run local commands/tests.

2. Pick a pack tier first (`minimal` / `core` / `full`)
- Default to `minimal`.
- Upgrade to `core` only when architecture/contracts matter.
- Use `full` only when root cause plausibly spans multiple subsystems.

3. Build the include set for that tier
- Include changed runtime files + direct dependencies + adjacent tests.
- Include only docs needed for intent/constraints at the chosen tier.
- Avoid unrelated folders to keep context small.

4. Pack with deterministic command (single folder, auto-clean)
```sh
bunx repomix . \
  --style plain \
  --no-git-sort-by-changes \
  -o repomix-output/repomix-<topic>-<tier>.txt \
  --include "<comma-separated-file-list>"
```
Or use the helper script:
```sh
bash .codex/skills/formax-repomix-handoff-workflow/scripts/build-repomix.sh \
  repomix-<topic>-<tier>.txt \
  "<comma-separated-file-list>"
```
The helper script will:
- create `repomix-output/` if missing
- delete previous files under `repomix-output/` (except `.gitkeep`)
- write the new bundle into `repomix-output/`

5. Write prompt + file manifest with naming convention
- Prompt: `repomix-output/<topic>-handoff-prompt.md`
- Manifest: `repomix-output/repomix-<topic>-files.md`
- Always use **repo-relative paths** in prompt + manifest (no machine absolute paths).

6. Write prompt with explicit boundaries
- State known symptoms.
- State hard constraints (what must not change).
- Define deliverables (root cause model, options, recommended plan, test/validation matrix).
- Include acceptance criteria with observable assertions.

7. Run artifact validation (required)
```sh
bash .codex/skills/formax-repomix-handoff-workflow/scripts/check-handoff-artifacts.sh \
  repomix-<topic>-<tier>.txt \
  <topic>
```
This check enforces:
- Bundle/prompt/manifest files all exist.
- Prompt and manifest reference the current bundle name.
- Manifest references the prompt filename.
- Prompt + manifest do not contain local absolute paths.

8. Sanity-check before handoff
- `repomix-output/` only contains current-round artifacts.
- Bundle exists and includes the expected files.
- Prompt has no impossible instructions for the target runtime.
- Prompt does not ask static consumers to run commands.
- Naming is topic-driven and consistent across all three artifacts.

See `references/prompt-templates.md` for copy-ready templates.

## Tests to update
- No repository tests required for creating the handoff itself.
- If target is executable, include a suggested minimal test list in the handoff prompt.

## Guardrails
- Never include `bun run test:coverage` in a static-consumer prompt.
- Never assume the other AI can read files outside the provided bundle unless explicitly attached.
- Keep asks decision-oriented first (root cause/options) before patch implementation.
- Prefer concrete acceptance checks over vague goals.
- Avoid mixing unrelated bugfixes into one handoff package.
- Never leak machine absolute paths (e.g., `/Users/...`) in prompt/manifest.
