---
name: emergency-hotfix-deployment-procedure
description: >
  Defines the out-of-cadence process for shipping a production hotfix
  outside the normal release train — which checks are genuinely safe to
  bypass versus never, the minimum required verification before an
  emergency deploy, required sign-off, and the rollback plan that must
  exist before the hotfix goes out. Use when the user asks to "ship an
  emergency hotfix," "deploy outside the normal release process," "bypass
  the release train for a critical fix," "what's the minimum we can skip
  for a production emergency," or "we need to patch prod right now."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Emergency Hotfix Deployment Procedure

## Purpose

A normal release train exists to batch changes safely through staged
gates — but a live production incident (data corruption, a security
exploit being actively used, a total outage) sometimes can't wait for the
next scheduled release, and pressure to "just ship it now" is exactly when
corners get cut in ways that turn one incident into two. This skill
defines a deliberate, pre-agreed emergency-hotfix procedure: a narrow,
explicit set of checks that may be skipped under time pressure, the
minimum verification that must never be skipped, and a mandatory rollback
plan — so an out-of-cadence deploy is still a controlled action, not an
improvised one.

## When to use

- A production incident requires a code change deployed before the next
  scheduled release window (active data loss, a security vulnerability
  under active exploitation, a total or near-total service outage).
- Deciding, under time pressure, which of the normal release process's
  steps are safe to skip for this specific change versus which must never
  be skipped regardless of urgency.
- Defining (in advance, not mid-incident) an organization's emergency
  change procedure, including who can authorize bypassing normal gates.
- After an emergency hotfix ships, reconciling it back into the normal
  release/versioning history so it isn't lost or silently diverges from
  the next planned release.

## Prerequisites & environment

- A pre-agreed emergency-change policy defined *before* an incident
  happens — deciding what's safe to skip while an outage is live and
  everyone is under pressure produces worse decisions than deciding it
  calmly in advance.
- A named incident commander or equivalent authority (see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md))
  empowered to authorize an out-of-cadence deploy — an emergency deploy
  should never be a unilateral individual decision with no accountable
  approver, even under time pressure.
- A working, tested rollback mechanism for the target service (previous
  known-good artifact/image tag, a `git revert`-based GitOps rollback, or
  a database migration's down-path) that can be executed as fast as the
  hotfix itself — see
  [environment-promotion-strategy](../environment-promotion-strategy/SKILL.md)
  and
  [gitops-workflow](../gitops-workflow/SKILL.md).
- CI/CD tooling that supports a distinct, explicitly-labeled "hotfix"
  path (a separate branch protection rule set, a manual-approval override
  that still logs who approved it) rather than an ad hoc `git push --force`
  to production infra.

## Step-by-step guidance

1. **Confirm the situation actually warrants bypassing the normal
   process** before invoking it. An emergency hotfix procedure exists for
   genuine production emergencies (active data loss, active security
   exploitation, full/major outage) — not for "we want this feature out
   before the next release" or "QA is taking too long." Confirm severity
   with the incident commander first; see
   [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)
   for severity definitions.

2. **Branch from the exact commit currently running in production**, not
   from the latest `main`/`develop`, which may already contain unrelated,
   unreleased changes that would ship along with the fix:
   ```bash
   git fetch --tags
   git checkout -b hotfix/checkout-null-pointer v2.14.3   # the tag/SHA currently in prod
   ```
   This keeps the hotfix's blast radius to exactly the one fix, not
   "whatever else happened to be on `main`" — a core discipline shared
   with standard hotfix-branching conventions in trunk-based/Git-flow
   models.

3. **Define, in the emergency policy ahead of time, exactly which checks
   may be skipped and which never can be** — do not decide this live,
   under pressure, on a case-by-case basis:
   - **Safe to skip, with justification, for a genuine emergency:** full
     regression suite (run the narrowly-scoped tests covering the fixed
     area instead), non-blocking linters/style checks, non-critical
     manual QA sign-off steps, the full multi-day staged canary rollout
     schedule (compressed to a shorter but still real canary window, not
     zero).
   - **Never skip, regardless of urgency:**
     > **Warning:** Bypassing a security scan, skipping the fix's own
     > targeted test coverage, or deploying with no rollback path
     > prepared are not legitimate time-savers — they turn one incident
     > into the risk of a second, and are the specific failure mode this
     > procedure exists to prevent.
     - A test that specifically exercises the bug being fixed (write one
       if it doesn't exist — a hotfix with no test proving it fixes the
       stated problem is unverified by definition).
     - A security/secret scan on the diff, even a fast targeted one.
     - Named human approval from an accountable role (incident commander
       or designated release approver), even if verbal/Slack-recorded
       under time pressure — never a fully automated, unapproved deploy
       straight to production.
     - A verified, ready-to-execute rollback path.

4. **Deploy through the pipeline's emergency path, not around the
   pipeline entirely.** Most CI/CD platforms support an explicit
   override that still logs who approved and what was skipped, rather
   than a manual `scp`/SSH deploy that leaves no audit trail:
   ```yaml
   # GitHub Actions: environment protection rule that allows a designated
   # "incident-commander" team to bypass the standard required reviewers
   # for this one environment, with the bypass itself audit-logged.
   environment:
     name: production-hotfix
     # reviewers: [release-approvers]  # normally required
     # Emergency policy: incident-commander team may approve directly;
     # every such approval is logged in the environment's deployment history.
   ```
   Even under emergency policy, prefer *reduced* gates over *no* gates —
   a single named human approval recorded in the pipeline's own history
   is very different from an unrecorded manual deploy.

5. **Deploy with the fastest safe rollback mechanism available for this
   service** — a canary/blue-green cutover if already in place (see
   [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md)),
   or at minimum a one-command revert to the previous known-good
   artifact tag. Watch the same health signals a normal deploy would
   watch, just compressed in time, not skipped.

6. **Immediately reconcile the hotfix back into the normal release
   history** once the incident is resolved — merge the hotfix branch
   into `main`/`develop` (not just production), re-run the full test
   suite and any skipped checks against the merged result, and make sure
   the next scheduled release includes (or doesn't conflict with) the
   hotfix. See
   [release-versioning-and-changelog-automation](../release-versioning-and-changelog-automation/SKILL.md)
   for tagging the hotfix into the version history correctly rather than
   letting it silently diverge.

7. **Run a blameless postmortem on the incident that required the hotfix,
   and separately review whether the emergency procedure itself was
   followed correctly** — see
   [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md).
   A hotfix that skipped a check that turned out to matter is itself a
   finding worth tracking, not something to quietly let pass because the
   incident is over.

## Best practices

- Decide the "always skip / never skip" list before an incident happens,
  in a written, agreed policy — not through in-the-moment judgment calls
  made by whoever happens to be paged.
- Require a named, accountable approver for every emergency deploy, even
  if the approval itself happens fast (a recorded Slack message or a
  pipeline environment approval) — "everyone agreed in the incident
  channel" without one clearly accountable approver is not a real
  approval trail.
- Branch the hotfix from the exact production commit/tag, never from
  `main`, so nothing unrelated ships alongside the fix.
- Treat "no rollback path ready" as a blocking condition for the
  emergency deploy itself, not an acceptable risk to accept under
  pressure.
- Reconcile every hotfix back into the mainline release history
  immediately — an unreconciled hotfix branch is a silent source of
  future merge conflicts and version drift.
- Keep the emergency path in the same pipeline tooling as the normal
  path (a different approval rule, not a different, undocumented manual
  process) so it's auditable and doesn't atrophy from disuse.

## Common pitfalls

- **Symptom:** Under incident pressure, someone deploys directly to
  production via SSH/manual artifact copy, bypassing the pipeline
  entirely "to save time."
  **Fix:**
  > **Warning:** this is a destructive shortcut — it leaves no audit
  > trail of what was deployed, by whom, or with what verification, and
  > frequently turns out to be slower than the pipeline's own emergency
  > path once mistakes are accounted for. Use the pipeline's designated
  > emergency-approval path (step 4) even when it feels slower in the
  > moment.

- **Symptom:** The hotfix fixes the immediate incident but is never
  merged back into `main`, and the next regular release accidentally
  reverts the fix because it was branched from an older commit.
  **Fix:** Reconcile the hotfix into mainline immediately after the
  incident (step 6), and verify the next release build actually still
  contains the fix before it ships.

- **Symptom:** An emergency deploy ships with no rollback plan because
  "we're confident this fix is right," and when it introduces a new
  problem, the team has no fast way back to the last known-good state,
  turning a contained incident into an extended one.
  **Fix:** Treat a verified rollback path as a non-negotiable
  prerequisite for the emergency deploy itself (step 3/5), never an
  optional nicety skipped under pressure.

- **Symptom:** The security scan is skipped "just this once" for a
  hotfix, and the fix itself introduces a new vulnerability that isn't
  caught until the next scheduled scan days later.
  **Fix:** Security/secret scanning is on the never-skip list regardless
  of urgency (step 3) — a fast, narrowly-scoped scan of just the diff
  still takes seconds to minutes, not hours, and is not a legitimate
  place to cut time.

- **Symptom:** There is no pre-agreed emergency policy, so every incident
  becomes an ad hoc argument about what can be skipped, wasting time that
  should go to fixing the actual problem.
  **Fix:** Write and socialize the emergency-change policy in advance
  (step 3) — decide the always-skip/never-skip list and the approval
  authority before the next incident, not during it.

## Worked example

**Scenario:** A checkout service is actively double-charging customers in
production due to a race condition merged in the last release; the next
scheduled release is four days away.

1. **Severity confirmed** by the incident commander as Sev-1 (active
   customer financial impact) per the org's incident severity policy —
   the emergency procedure applies.
2. **Branch from production**: `git checkout -b hotfix/checkout-double-charge v2.14.3`
   (the exact tag currently deployed), not from `main`, which already
   has three unrelated feature PRs merged since the last release.
3. **Minimum required checks, per the pre-agreed policy:**
   - Skipped: full E2E regression suite (12 minutes), non-blocking style
     linter.
   - Not skipped: a new targeted test reproducing the double-charge race
     condition (written first, confirmed failing on the buggy code,
     passing after the fix); a fast Semgrep/secret scan on the 30-line
     diff; named sign-off from the incident commander, recorded in the
     incident channel and in the pipeline's environment-approval log.
4. **Deploy** through the existing blue/green deployment group with the
   normal `ValidateService` health check still in place (just a shorter
   soak window — 5 minutes instead of the usual 30) and the standard
   automatic-rollback-on-alarm configuration left enabled, not disabled.
5. **Verify**: the specific race-condition test passes in the pipeline,
   and a manual check of the double-charge metric confirms it drops to
   zero within minutes of the new version taking traffic.
6. **Reconcile**: `hotfix/checkout-double-charge` is merged into `main`
   within the hour, the full regression suite that was skipped runs
   against the merged result and passes, and the next scheduled release
   four days later includes this fix already merged rather than
   reverting it.
7. **Postmortem**: run within 48 hours per
   [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md),
   including a specific review item on whether the emergency procedure's
   skip list was followed correctly (it was) and whether the 5-minute
   soak window was long enough in hindsight (flagged as a follow-up to
   reconsider).

## Cross-references

- [environment-promotion-strategy](../environment-promotion-strategy/SKILL.md) —
  the normal gated-promotion flow this procedure deliberately, narrowly
  bypasses; understand the normal gates before deciding which ones are
  safe to skip.
- [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md) —
  the fast, automated rollback mechanism a hotfix deploy should reuse
  rather than inventing an ad hoc rollback under pressure.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) —
  severity definitions and the incident-commander authority this
  procedure depends on for who can invoke and approve it.
- [release-versioning-and-changelog-automation](../release-versioning-and-changelog-automation/SKILL.md) —
  how to tag and reconcile the hotfix back into the normal version
  history so it isn't lost or silently diverged from.
