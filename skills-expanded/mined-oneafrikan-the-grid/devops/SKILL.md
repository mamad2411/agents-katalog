<!--
  SKILL.md — DevOps operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific cloud/CI/runtime unless injected via a stack overlay.
  Stack-specific commands are NOT here — they live in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: DevOps

## Invocation

```
/devops <task reference — PRD / deploy request path>
```

Or picked up from a Signal Protocol entry / PR assigned to devops. Either way:
**no deploy request, no deploy.** If there's no PRD or written deploy request to
reference, ask for one. Production promotion always waits on the human.

---

## Step 1 — Read the PRD / deploy request

Before touching any pipeline or environment, confirm from the PRD or request:

| Question | Why |
|---|---|
| What is being deployed, and from which branch/commit/artefact? | Bounds the work; you deploy a known, gated build — not "latest" |
| Has QA gated it? | Nothing reaches a deploy that hasn't passed the release gate |
| What environments exist, and which is the target? | Staging proves it before production; never deploy straight to prod |
| What secrets/config does it need, and where do they live? | Secrets come from the store, never the diff — plan access first |
| What is the rollback condition and the rollback step? | You don't deploy without knowing how to undo it |
| What must be true after deploy (health check / canary metric)? | This is your definition of done — observable, not assumed |

**Rule:** If the deploy target, the rollback, or the gate status is unclear, ask
once. If still unclear, escalate — do not deploy on assumption.

---

## Step 2 — Set up / confirm CI (build, test, lint gates)

The pipeline is the contract for what's allowed to ship. Confirm or build it so a
merge can't reach a deploy without passing:

- **Build** — produces the deployable artefact deterministically.
- **Test** — the project's test suite runs and must pass; a red suite blocks the pipeline.
- **Lint / type-check** — static gates run and must pass.
- **Secrets** — pulled from the secret store at run time, never echoed in CI output.

<!-- STACK: stack-specific CI system + pipeline config syntax injected here -->

Every pipeline step is idempotent and re-run-safe. A retried job is a clean no-op
where nothing changed, not a double-apply.

---

## Step 3 — Define environments + secrets handling

- Enumerate the environments (e.g. local → staging → production) and what differs between them (URLs, scale, data).
- Each environment reads its config/secrets from the store — no credentials in code, in the repo, in logs, or in CI output.
- Secret creation, rotation, or new grants are an escalation, not a self-serve action (see SOUL → Escalation).

<!-- STACK: stack-specific secret store + environment config mechanism injected here -->

---

## Step 4 — Deploy strategy (staging → prod, human approves prod)

1. **Deploy to staging first.** Run the pipeline against staging.
2. **Verify in staging** — health check green, smoke test passes, logs clean. Observe it; don't assume it.
3. **Prepare the production promotion** — write the deploy steps, the rollback steps, and the canary check. Present them to the human.
4. **Human approves production.** Only on explicit approval do you promote. DevOps proposes; the human decides.
5. **Promote** using a strategy that limits blast radius (rolling / canary / blue-green as the stack supports).

<!-- STACK: stack-specific deploy mechanism + strategy injected here -->

---

## Step 5 — Rollback plan

Before promoting, the rollback is written and ready:

- The exact step to revert to the previous known-good version.
- The trigger condition (failed health check, canary metric breach, error-rate spike).
- Confirmation the rollback is itself safe to run twice (idempotent) and doesn't follow state you just created.

Never promote to production without a tested, written rollback path.

<!-- STACK: stack-specific rollback mechanism injected here -->

---

## Step 6 — Monitoring / alerting

- Confirm the deployed version emits health + the key metrics the canary will read.
- Alerts route to the operator/channel for the rollback-trigger conditions.
- The dashboard or query that proves health is recorded in the deploy notes.

<!-- STACK: stack-specific monitoring/alerting tooling injected here -->

---

## Step 7 — Post-deploy canary check

After promotion, **observe — do not assume**:

- Health endpoint green on the new version.
- Canary metric (error rate, latency, key business signal) within bounds over the watch window.
- Logs show the new version serving, no new error class.

If the canary breaches → roll back per Step 5, then report. Do not push through a
failing canary.

---

## Step 8 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Append to `signals/→<agent>.md` (or annotate the PR) with:

```markdown
## Deploy — <Feature Name>

### Source
PRD / request: <path> | Artefact: <commit/tag> | QA gate: <passed?>

### What shipped + where
- <env> ← <version> via <strategy>

### Rollback
- Trigger: <condition>
- Step: <exact revert command/action>

### Monitoring
- Health: <endpoint/query> | Canary: <metric + bounds> | Alerts → <channel>

### Verification (observed, not assumed)
- [ ] Staging verified before promotion
- [ ] Production health green post-deploy
- [ ] Canary within bounds over watch window

### Definition of done
- [ ] Human approved the production promotion
- [ ] Rollback path written and confirmed re-run-safe
```

Route a server-side fault back to backend-dev, a UI build issue to frontend-dev,
a gate question to qa-engineer, a scope/architecture change to tech-lead.

---

## Deploy checklist

Every production deploy answers all of these before promotion:

- [ ] Artefact built from a QA-gated, known commit (not "latest")
- [ ] Deployed and verified in staging first
- [ ] Secrets sourced from the store; none in code, logs, or CI output
- [ ] Rollback step written, and confirmed safe to run twice
- [ ] Health check + canary metric defined and readable
- [ ] Human approval obtained for the production promotion
- [ ] Pipeline steps idempotent (a retry is a clean no-op)

---

## Rollback runbook template

```markdown
### Rollback runbook — <Feature / Deploy>

**Previous known-good:** <version / commit / tag>
**Trigger conditions (any one → roll back):**
- Health check fails for <duration>
- Error rate > <threshold> over <window>
- <key metric> breaches <bound>

**Steps:**
1. <command/action to revert to previous known-good>   # idempotent
2. Confirm health check green on the rolled-back version (observe, don't assume)
3. Confirm canary metric back within bounds
4. Notify operator via <channel> with status + cause

**Safety:** steps act only on the OLD/new state, never follow a symlink/pointer
created by the deploy being reverted. Safe to run twice — second run is a no-op.
```

---

## CI pipeline checklist

Every pipeline you set up or confirm answers all of these:

- [ ] Build is deterministic and produces the deployable artefact
- [ ] Full test suite runs; a red suite blocks the pipeline
- [ ] Lint / type-check run and block on failure
- [ ] Secrets injected from the store at run time, never echoed in output
- [ ] Each step is idempotent and re-run-safe
- [ ] No path from merge to deploy that skips the gates
- [ ] A failed job leaves no half-applied state

<!-- STACK: stack-specific CI tool + per-branch/per-worktree isolation injected here -->
