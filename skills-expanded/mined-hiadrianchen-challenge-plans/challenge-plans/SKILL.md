---
name: challenge-plans
description: Before you execute a drafted plan/spec/design doc, run a multi-agent adversarial cross-review to surface the flaws that cause downstream rework, aggregating "evidenced, cross-family-verified" objections into a verdict. Use when the user asks to "review this plan/spec", "can this approach be executed", "poke holes / adversarial review / QA this", "harden before executing", or when an agent is about to hand a drafted decision/QA back to the user — first run this skill and present the cross-review recommendation plus surviving objections. Runs on local subscription CLIs (claude/codex), no per-token API cost. Not for "help me pick among options" — that's the weigh-options deliberation skill.
runtime_mode: cli_tool
---

# challenge-plans

Harden a plan/spec in multi-agent adversarial review before execution, to reduce rework. Slots into `writing-plans → challenge-plans → executing-plans`.

## When to use (routing signals)

- Input is a **single drafted artifact** + intent "review / find flaws / can this execute / harden / QA" → **use this skill**. Pick `--type` by what the artifact *is*:
  - a **spec / design doc / PRD** you're about to build → `--type spec`
  - **any plan with steps** to execute (dev or not — a trip, a launch, a hire) → `--type plan`
  - a **code change** (`git diff`) → `--type diff`
  - a **decision already made** (an ADR / "we chose X because Y" — a tech-stack pick, a vendor, a hire) → `--type decision`. Audits the *choice itself*: skipped alternatives, weak evidence, sunk-cost reasoning, irreversibility.
- An agent has finished something and is **about to ask the user to decide or QA** → run this first and present the cross-review recommendation.
- Input is **≥2 options still open to choose among** → use the sibling `weigh-options` (deliberation/voting), not this. (`--type decision` is the opposite: one option *already* chosen, audited after the fact.)

## Run

```bash
# Installed from PyPI (pip install challenge-plans) — the console command is available directly.
# Already installed but on an old version? update: pip install -U challenge-plans (pipx: pipx upgrade; uvx: append @latest).
challenge-plans doctor                                                            # check adapter login state first
challenge-plans run <artifact> --type spec --profile standard --sink markdown     # review a plan/spec
challenge-plans run <artifact> --type spec --profile standard --sink markdown --lang zh   # localized output
# code-diff gate:  git diff > change.diff && challenge-plans run change.diff --type diff --sink markdown
# From a source checkout instead (not pip-installed): PYTHONPATH=src python3 -m challenge_plans.cli <args>
```

- `--type spec|diff|plan|decision`. `diff` reviews a raw `git diff`; **`plan` reviews ANY plan (a trip, a launch, a hire — not just dev specs)** with domain-neutral failure types (missing success criteria / ignored constraint / unaddressed risk / sequencing gap / unstated assumption / goal misalignment / irreversibility / no fallback) and feasibility·risk·goal-alignment lenses; **`decision` audits a choice already made** (ignored alternative / weak evidence / unstated assumption / sunk-cost bias / unaddressed downside / irreversibility / no review trigger / misframed problem) with alternatives·evidence·reversibility-cost lenses. All run the same verdict pipeline.
- `--profile fast|standard|deep`, `--sink stdout|markdown`, `--enforce` (`request_changes`/`inconclusive`/`schema_invalid` exit non-zero; `discuss`/`approve` exit 0); `--strict` (hard gate — only a clean `approve` passes); default advisory exits 0.
- `--lang <code>` (default `en`): write the review prose in the user's language, e.g. `--lang zh`. **Set this from the user's language** so the whole review comes back localized; JSON keys / enums / `L12-15` anchors stay stable. Equivalent to exporting `CHALLENGE_PLANS_LANG`.
- Output: a 6-state verdict + surviving objections. `[sev✓]` = cross-family Verifier-confirmed, may hard-gate; `[sev?]` = unverified, advisory only.

## If no backend is ready

challenge-plans needs **at least one logged-in subscription CLI** (it has no model of its own and uses no API keys). If `doctor` shows nothing `ready`, don't retry blindly — **ask the user, then route**:
1. **Has a Claude or ChatGPT subscription, but the CLI is missing / logged out** → walk them through the exact step `doctor` prints (install it, or `claude` → `/login`, or sign in to `codex`).
2. **No subscription yet but wants one** → point them to subscribe (Claude Pro/Max or ChatGPT), then install + log in the CLI.
3. **No subscription and doesn't want one** → explain challenge-plans cannot run without one, and stop — don't loop.

`doctor` already prints the per-backend fix plus this guidance; surface it to the user rather than failing silently.

**BYO backends (optional).** The user can register extra Anthropic-compatible endpoints (GLM/Kimi/a proxy) via env: `CP_BYO_<n>_BASE_URL` + `CP_BYO_<n>_FAMILY` + `CP_BYO_<n>_TOKEN` (all required; `_MODEL` optional; `_1/_2/…` for several). Two caveats to relay honestly: (1) the declared family is **user-declared, not verified** — confirmations through it render `✓(user-declared family)` and diversity built on it is flagged, so never present a BYO pairing as the verified builtin claude+gpt cross-family guarantee; (2) the token goes only into that backend's subprocess and never appears in any output — but advise the user to set it via a secrets manager / leading-space export rather than plain shell history. A backend missing one of the three vars is skipped with a warning (never a fallback to subscription auth).

## If a backend is too old / a run degrades or errors opaquely

A **backend CLI that is logged in but out of date** is a distinct failure from "logged out": `login status` still passes, but a real call is rejected server-side (observed: codex 400 "the model requires a newer version of Codex"), so a voter reports `exit_nonzero` and the run silently drops to a single family. A run can't cheaply tell this apart mid-flight — but **`doctor` now can**: it sends a real minimal call per backend, so a too-old codex reads `unsupported_version → update Codex CLI: npm i -g @openai/codex@latest` instead of a false `ready`.

So when a run errors, comes back single-family unexpectedly, or a voter shows `exit_nonzero`: **run `doctor` and update any `unsupported_version` backend before retrying** — don't just report the error to the user. Updating the backend CLI (`npm i -g @openai/codex@latest`, or update Claude Code) is part of the standard fix path, not a dead end to hand back.

## Presenting to the user

Surface the verdict + **surviving objections (✓ verified vs ? unverified)** + missing required fields as "my cross-review recommendation", then let the user decide — rather than handing them a bare decision. See [README.md](README.md) for the full picture.

## Composing with planning skills

- **superpowers** (`writing-plans → executing-plans`): after `writing-plans` saves a plan file (default `docs/superpowers/plans/<date>-<feature>.md` — read the actual path), run `challenge-plans run <plan> --type spec` **before** `executing-plans`. It occupies the same pre-execution review seam as superpowers' built-in `plan-document-reviewer`, but as a multi-CLI cross-family pass. Route surviving objections back into the plan, then execute.
- **grill-me** (mattpocock/skills): complementary and earlier — it interactively aligns the user while the plan forms (no file output). Run challenge-plans *after* a written plan/PRD exists.
- Nothing auto-invokes challenge-plans; the calling agent wires it into the seam and chooses `--type` from the routing signals above.
