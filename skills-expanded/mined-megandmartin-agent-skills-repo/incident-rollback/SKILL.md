---
name: incident-rollback
description: The response protocol for when an agent did something wrong in the real world — stop the agent, assess blast radius, contain (revoke keys, undo changes), communicate to affected parties, write the post-mortem, and add a prevention rule to the responsible skill's Pitfalls. Use when the user says "the agent sent/deleted/bought something it shouldn't have", "kill the agent", "roll this back", "we have an incident", or any agent action caused unintended real-world effects. Don't use for outputs that are merely wrong but caused no harm — that's prompt-debugger.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Incident, Safety, Rollback, Response]
    related_skills: [third-party-skill-vetter, prompt-debugger, budget-guardrails]
---

# Incident Rollback

When an agent has actually done the wrong thing — sent the email, deleted the files, spent the money — the job is emergency response, not debugging. Order is everything: stop, assess, contain, communicate, learn. The standard: the agent is provably stopped within minutes, every effect is on a written list before anyone "fixes" anything, and the incident ends with a prevention rule in a skill file — not a promise to be more careful.

## When to Use

- An agent sent messages, deleted/modified files, spent money, or changed production it shouldn't have.
- An agent is CURRENTLY doing something wrong (mid-run) — start at step 1 immediately, read nothing else first.
- A vetted-or-not third-party skill turned out to be malicious and has executed.
- **Not for:** bad-but-harmless outputs (`prompt-debugger`), or pre-install suspicion about a skill that hasn't run (`third-party-skill-vetter`).

## Quick Reference

| Phase | Action | Done when |
|---|---|---|
| 1. Stop | Kill agent processes, pause schedules/blueprints, disable triggering skill | No agent process alive; no schedule can re-fire |
| 2. Assess | Build effects list from transcript + tool logs | Every external effect on one written list |
| 3. Contain | Revoke exposed credentials, undo what's undoable | Each effect marked reversed / mitigated / permanent |
| 4. Communicate | Notify affected humans, factually | Everyone impacted knows what happened + what's done |
| 5. Post-mortem | Template below, blameless, same-day | Root cause is a mechanism, not "agent misbehaved" |
| 6. Prevent | Rule added to responsible skill's Pitfalls + gate fixed | Validator passes; the same action now requires confirm |

## Procedure

1. **Stop the agent — completely** — kill running sessions/processes; pause every scheduled task, cron, and blueprint for that agent; disable the implicated skill (move it out of the skills dir, don't just "plan to avoid it"); for Paperclip agents, suspend at the platform so wake cycles stop. Verify: process list clean, schedule list shows paused. A half-stopped agent re-offends mid-response.
2. **Assess blast radius before fixing anything** — from the transcript and tool logs, list EVERY external effect: messages sent (to whom), files changed/deleted (paths), money spent (amounts, vendors), API/DB writes, credentials the agent could read during the run. Resist fixing while listing — undoing effect #1 before discovering effect #4 loses evidence and can widen damage. Success: a numbered effects list with timestamps.
3. **Contain** — in this order: (a) revoke/rotate every credential the agent could see (assume exposed, don't debate it); (b) undo the reversible — restore files from backup/git, cancel pending orders, recall what's recallable; (c) mitigate the permanent — a sent email can't be unsent, but a prompt correction can follow. Mark each effect reversed / mitigated / permanent. Get user confirmation before containment actions that are themselves destructive (e.g. force-restores over newer work).
4. **Communicate** — draft notifications for every affected human: what happened, what was affected, what's already contained, what happens next. Factual, no spin, no burying. The user reviews and sends (or explicitly approves the agent sending — yes, even now, especially now). Internal money incidents also go to whoever owns the budget (`budget-guardrails` reporting line).
5. **Post-mortem, same day** — fill the template below while logs are fresh. Blameless and mechanical: the root cause is always a missing or failed gate ("expensive action had no confirm step"), never "the agent was dumb." Ask why twice past the first answer.
6. **Add the prevention rule** — turn the root cause into (a) a new entry in the responsible skill's Pitfalls section (`- **failure** — recovery`), and (b) where the cause was a missing gate, the actual gate: a confirm-before-execute step, a dry-run mode, a budget cap, or a narrower toolset. Re-run `tools/validate_skills.py`. An incident that doesn't change a file will repeat.
7. **Controlled restart** — re-enable the agent only after: prevention shipped, credentials rotated, and the fixed skill re-passes its eval (build one via `agent-eval-harness` if none exists — include the incident scenario as a test case). Restart schedules last, one at a time, watching the first run of each.

## Output Template

```
## Incident post-mortem: <one-line title> — <date>
Severity: <low|medium|high> | Agent: <name> | Skill(s): <name vX.Y.Z>

Timeline (UTC):
- <hh:mm> agent did <action>  - <hh:mm> detected by <who/how>
- <hh:mm> agent stopped        - <hh:mm> contained

Blast radius:
| # | Effect | Status |
|---|---|---|
| 1 | <e.g. email to 12 customers> | permanent — correction sent |
| 2 | <e.g. deleted /reports> | reversed — restored from git |
Credentials rotated: <list>

Root cause (mechanism, not blame): <the missing/failed gate>
Why wasn't it caught sooner: <detection gap>

Prevention shipped:
- Pitfall added: <skill>/SKILL.md — "<entry>"
- Gate added: <confirm step | dry-run | cap | toolset narrowed>
- Eval case added: <evals/file — case n>
Restart: <date/time> | Approved by: <user>
```

## Pitfalls

- **Fixing before assessing** — restoring files in the first minute, then discovering the agent also sent emails referencing them; the restore destroyed the evidence of what was sent. Recovery: return to step 2, rebuild the full effects list from logs/backups, and freeze all fixing until the list is complete.
- **Half-stopped agent** — the session was killed but a scheduled blueprint re-fired an hour later and repeated the action. Recovery: enumerate ALL execution paths (sessions, crons, blueprints, wake cycles, webhooks) and disable each with verification; add "list every schedule" to your stop routine permanently.
- **Skipping credential rotation** — "it probably didn't read the keys" saves an hour today and costs everything later. Recovery: rotate now anyway; exposure is judged by what the agent COULD read during the run, not what the transcript happens to show.
- **Quiet cover-up temptation** — containing without telling affected people, hoping nobody noticed. Recovery: notify per step 4 regardless; discovered silence costs more trust than any incident, and consent-first automation includes consent about failures.
- **Post-mortem theater** — a document blaming "insufficient care," no file changed, same incident in a month. Recovery: reopen it; a post-mortem is done only when `git diff` shows a Pitfalls entry plus a real gate, and the validator + eval pass on the changed skill.

## Verification

- [ ] Agent provably stopped: no processes, all schedules/blueprints paused, skill disabled
- [ ] Effects list complete with timestamps; each item marked reversed / mitigated / permanent
- [ ] All potentially exposed credentials rotated
- [ ] Affected humans notified with user-approved messages
- [ ] Post-mortem filed same-day; Pitfalls entry + gate shipped; `validate_skills.py` passes
- [ ] Restart happened only after prevention shipped and the eval (incl. incident case) passes
