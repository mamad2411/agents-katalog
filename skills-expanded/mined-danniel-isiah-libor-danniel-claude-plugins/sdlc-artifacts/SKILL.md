---
name: sdlc-artifacts
description: Conventions for SDLC pipeline artifacts and handoffs. Use whenever creating, reading, or updating files under docs/sdlc/<slug>/, writing the 00-manifest.md, or applying the QUESTIONS FOR USER / NO QUESTIONS clarification protocol. Defines the artifact layout, manifest schema, feature slug rules, and how agents ask for clarification instead of guessing.
---

# SDLC Artifacts & Handoff Protocol

The repo's `docs/sdlc/` tree is the **canonical source of truth** for the pipeline. Notion (if enabled) only mirrors it.

## Feature slug
Lowercase, kebab-case, derived from the request (e.g. "Add password reset" -> `add-password-reset`). Max ~50 chars. If a folder with that slug exists, append `-2`, `-3`, …

## Folder layout
```
docs/sdlc/<slug>/
  00-manifest.md
  01-requirements.md
  02-design.md
  03-implementation.md
  04a-qa.md  04b-code-review.md  04c-security.md  04d-pipeline.md  04e-e2e.md   (later waves)
  e2e-recordings/<slug>-<flow>.webm                 (E2E video — gitignored, not committed)
  05-release.md  06-docs.md                          (later waves)
```

## 00-manifest.md schema
```markdown
# SDLC Manifest: <slug>

- **Request:** <original user request, verbatim>
- **Created:** <date>
- **Current phase:** <0–6>
- **Status:** <in-progress | blocked | done>
- **Notion:** <enabled:true|false> · ticket: <id-or-—>

## Phase log
| Phase | Artifact | State | Gate | Notes |
|---|---|---|---|---|
| 1 Requirements | 01-requirements.md | done | approved | |
| 2 Design | 02-design.md | done | approved | |
| 3 Implementation | 03-implementation.md | in-progress | — | |

## Decisions
- <decision> — <date>

## Open questions
- [ ] <unresolved question>
```

## Artifact authoring rules
- Each artifact starts with `# <NN> <Title> — <slug>` and a one-line summary.
- Write for a reader who has not seen prior phases; restate the essentials.
- End every generated artifact with an `## Open Questions` section (may be empty).

## Clarify-don't-guess protocol
Agents cannot talk to the user. When something is ambiguous, has multiple valid interpretations, or is missing:
- Do **not** guess on anything consequential.
- End your reply with a section titled exactly `QUESTIONS FOR USER`, each question on its own line with the concrete options you are weighing (so the orchestrator can offer them as multiple choice).
- If nothing is unclear, end with exactly `NO QUESTIONS`.

The orchestrator relays each question via AskUserQuestion, then resumes you (same agent, via SendMessage) with the answers. Record anything left unresolved under `## Open Questions` in your artifact and note it for the manifest.

## Release artifact (05-release.md) — required fields
Beyond the standard build/deploy content, `05-release.md` must record the **confirmed version**, the
**tag name** (`vX.Y.Z`), the **manifest file bumped** (`package.json` / `composer.json` / `VERSION`),
and a note that the tag + GitHub Release are created by the production deploy on `main` (idempotent,
tag-if-absent). See `release-management` for the derivation rule.
