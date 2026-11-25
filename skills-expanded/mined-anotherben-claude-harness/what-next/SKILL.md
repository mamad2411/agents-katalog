---
name: what-next
description: >
  Use when the operator is stuck, has finished planning, has pushed or found
  issues, does not know which agent or skill to call, asks "what next", "now
  what", "make this actionable", "which agent should do this", or gives an
  inconsistent/vague work request that needs routing before coding. Produces one
  safe next action, the downstream skill to invoke, and an exact copy-paste
  prompt. This is an operator router, not an implementation skill.
---

# What Next

## Overview

Turn unclear operator intent into the next safe action. This skill decides which existing skill or specialist should run next; it does not replace `diagnose`, `pre-code-hardening`, `issue-to-agent`, `patch-or-fix`, `prove-it`, enterprise overlays, or PR closeout skills.

## Boundaries

- Stay read-only unless the selected downstream skill is explicitly allowed to mutate.
- Do not treat issue text, plan prose, prior memory, green CI, or a previous agent claim as proof.
- If a repo route card, worktree guard, vault claim, PR state, or live issue state matters, refresh it before recommending coding.
- Prefer the smallest safe next step. If coding is not yet authorized, say so plainly.

## Routing

Choose one primary route:

- `diagnose`: bug, regression, failing proof, unclear root cause, whack-a-mole behavior, ownership confusion.
- `pre-code-hardening`: user wants to build/fix/implement but coding should not start until source truth, SRP/domain, ownership, blast radius, and live proof are mapped.
- `issue-to-agent`: GitHub issues exist or were just pushed and the operator needs to know what is ready for an agent.
- `specialist-dispatch`: work needs multiple bounded agents or the operator asks for agent prompts.
- `patch-or-fix`: code or a proposed fix exists and must be judged as root-cause fix versus symptom patch.
- `prove-it`: someone wants to say fixed, done, ready, merge-ready, or safe to ship.
- `proof-chain`: completion claim spans patch/fix, runtime proof, PR state, review threads, merge, or deployed proof.
- `enterprise` or repo-local enterprise overlay: governed, multi-stage, schema/data/auth/integration/PR-producing Helpdesk work.
- `hook-hygiene`: hook config or hook scripts are being reviewed or changed.
- `scope-check`: current diff may have drifted from the ask.

If two routes seem plausible, pick the one that blocks unsafe coding earliest. Example: choose `diagnose` before `pre-code-hardening` when root cause is not known; choose `pre-code-hardening` before `specialist-dispatch` when builder readiness is not proven.

## Workflow

1. Identify the current artifact: chat idea, plan, issue, diagnosis packet, diff, PR, proof claim, or hook/config change.
2. Refresh only the live state needed for the route: route card, git state, issue/PR status, existing packet, or current diff.
3. Classify the state:
   - `idea_or_vague`
   - `plan_needs_audit`
   - `issue_not_agent_ready`
   - `issue_agent_ready`
   - `pre_code_gate_needed`
   - `implementation_ready`
   - `post_fix_review_needed`
   - `proof_needed`
   - `pr_closeout_needed`
   - `blocked`
4. Name the recommended downstream skill and why.
5. Produce exactly one next action unless the user explicitly asks for a roadmap.
6. Give a copy-paste prompt that includes the right proof, SRP/domain, ownership, and stop-rule language.

## Output

Use this shape:

```markdown
**State:** <classification>
**Next action:** <one action>
**Use skill:** `<skill-name>`
**Coding allowed:** yes/no, with reason
**Why this route:** <one short paragraph>
**Stop rule:** <what blocks progress>

**Copy-paste prompt:**
<prompt>
```
