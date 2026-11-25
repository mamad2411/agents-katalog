---
name: deploy
description: Release step that closes the loop after /ship — drive a change out to a running environment using the PROJECT'S OWN deploy mechanism (detect, never prescribe a stack), then smoke-test the deployed artifact and keep a guarded rollback path. Deploy is more outward-facing than git push, so it is arm-to-fire — plan and pre-check, then HALT and require an explicit `arm deploy` before any real outward action. Opt-in; invoked explicitly. Use after /ship to push a verified change to staging/prod under the harness's boundary discipline.
---

# /deploy — detect, plan, arm, deploy, smoke, guard

Goal: take a change that has passed the harness's gates and `/harness-claude:ship` has prepared, and
drive it out to a running environment — **using whatever deploy mechanism the project already has** —
with the same boundary discipline the rest of the harness applies to outward actions. The pipeline's
front door stops at the repo edge; `/harness-claude:deploy` is the step *past* it. The discipline is
**arm-to-fire**: plan the deploy and run pre-checks, then **stop and wait** for an explicit arm
before anything leaves your machine.

> **Opt-in.** Invoked explicitly; nothing auto-deploys. **Git boundary:** `/harness-claude:deploy`
> never commits, pushes, or branches. **Arm-to-fire boundary:** it performs **no real outward
> action** (deploy or rollback) until you type the explicit arm signal — planning and smoke-checks
> are safe; firing is not, and is never implied by "looks good."

## When `/harness-claude:deploy`, when `/harness-claude:ship`
- **`/harness-claude:ship`** prepares a clean commit / PR summary and stops at the repo boundary.
  It is the *last in-repo* step.
- **`/harness-claude:deploy`** is the *first out-of-repo* step — it pushes an already-shipped change to
  a live environment and verifies it there. Run `ship` first; `deploy` does not commit your work.

## How it works
```
detect mechanism → name rollback path → pre-deploy smoke → ARM-TO-FIRE HALT
  → (on `arm deploy`) deploy in tmux → smoke the DEPLOYED artifact → guarded rollback on failure
```

## Do this
1. **Detect the deploy mechanism — never prescribe one.** Find the project's existing mechanism, in
   priority order: `vercel.json` / Vercel project → `Dockerfile` (+ registry/compose) → a `Makefile`
   `deploy`/`release` target → CI config (`.github/workflows`, etc.) → `package.json` `scripts.deploy`
   → other declared scripts. When a platform skill matches what you detect, **delegate to it** rather
   than reinventing (e.g. `vercel:deploy` / `vercel:vercel-cli` when a Vercel project is present). If
   **no** mechanism is found, say so and **stop** — do not invent a deploy command. (AC-D1)
2. **Name the rollback path up front.** Before anything else, state the concrete rollback for the
   detected mechanism — e.g. `vercel rollback`, redeploy the previous image tag, re-run CI on the
   previous SHA. Surface it in the plan. If no rollback path is identifiable, say so explicitly so the
   risk is visible *before* the HALT. (AC-D2)
3. **Run pre-deploy smoke checks.** Confirm the change is actually deployable: repo green
   (`/harness-claude:health`), build succeeds, working tree clean. Surface any failure now, not after
   firing. If the build breaks, delegate the `harness-claude:build-error-resolver` agent to get it green.
4. **HALT — arm-to-fire.** Show the deploy **plan**: detected mechanism, exact command, target
   environment, and the rollback path from step 2. Then **STOP. Do not proceed until the user types
   `arm deploy`.** "The plan looks fine" is **not** an arm; only the explicit signal fires. (AC-D4)
5. **On `arm deploy`: deploy in tmux.** Run the deploy command inside a **tmux** session (tooling
   default — long deploys survive and stream). If a build break appears mid-deploy, delegate the
   `harness-claude:build-error-resolver` agent; re-arm before re-firing. (AC-D6)
6. **Smoke-test the DEPLOYED artifact, then guard.** Verify the *live* target, not just local tests —
   reuse `/harness-claude:health`'s runner against the deployed URL:
   ```
   node scripts/eval/continuous.js --cmd 'curl -fsS https://<deployed-url>/health'
   ```
   (or the project's smoke suite pointed at the deployed target). (AC-D3) On **failure**: surface the
   rollback command from step 2 and **execute it only if the user types `arm rollback`**; otherwise
   HALT with the rollback ready. **Never leave a known-broken deploy silently in place.** (AC-D5)

## Security & trust
- **Arm-to-fire is absolute.** Nothing in this skill is permission to fire without `arm deploy` /
  `arm rollback`. A future session reading these steps must treat the HALT as a hard stop.
- The deploy/smoke commands are author-authored shell run with your privileges — same trust boundary
  as `/harness-claude:health`. Don't `/deploy` a project whose deploy scripts you don't trust.
- **No secrets inline.** Deploy targets and smoke URLs may be public; never embed tokens/keys in the
  smoke `--cmd` or the plan — read them from the environment / the platform's own secret store.

## Notes
- Self-contained: a single skill that *leads* and reuses existing tools — tmux (long-running),
  `/harness-claude:health` (the deployed-artifact smoke), `harness-claude:build-error-resolver`
  (mid-deploy build breaks), and any matching platform deploy skill (`vercel:deploy`, …). **No new
  agent, no new dependency, no new MCP server, no new runtime.**
- Distinct from `/harness-claude:ship` (prepares a commit/PR, stops in-repo). A single guarded action,
  not a loop — it does **not** need `/harness-claude:operate`'s durable `.claude/runs/<id>.json` state.
- The skill *is* the lead — there is no separate deploy agent (the same pattern as
  `/harness-claude:fix`, `/harness-claude:orchestrate`, `/harness-claude:operate`).

## Exit criterion
The deploy plan was shown (mechanism + rollback path), the arm-to-fire HALT fired, and — only after an
explicit `arm deploy` — the artifact was deployed, the **deployed** smoke passed, **or** a guarded
rollback was taken with its result surfaced. Never a silent outward action without an arm, and never a
known-broken deploy left in place.
