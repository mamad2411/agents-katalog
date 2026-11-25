---
name: adversarial-debate
description: Pressure-tests a built feature, PR, or design against multiple independent, no-context skeptical personas through iterative rounds of objection and rebuttal, until every fixable objection is actually fixed and only genuine values disagreements remain. Trigger when the user says "stress-test this", "pressure-test the PR", "debate this adversarially", "simulate a maintainer who'd reject this", "make this unrejectable", "red-team this before I ship it", or asks for a panel of reviewer personas before shipping.
---

<!-- Design razor: VERIFICATION + CONTEXT. Verification a model won't run honestly on
     itself (it is attached to what it just built), plus two facts about the harness it
     gets wrong by default: a fork is contaminated, and a respawn destroys the
     did-this-change-your-mind signal. The persona catalog is a question framework.
     Delete when: the harness ships a native multi-reviewer mode with fresh context per
     reviewer AND stance preserved across rounds. Fresh context alone is not enough. -->

# Adversarial Debate

Most self-review fails for one reason: you already believe the thing you built is good, so you read past its weak points. This skill exists to get a genuinely ungenerous first reaction, then force every objection to resolve into either a real fix or a named, honest disagreement — never a better-worded excuse.

## The one rule

> **You are not defending the work. You are finding out whether it survives contact with someone who didn't build it and doesn't want it to exist.**

If a persona's objection is correct, the right response is to change the code, not to write a more persuasive paragraph. If you catch yourself drafting a rebuttal to something that's actually true, stop and go fix it instead.

## When to Use

Run this before shipping something that a *specific other person* can reject: an upstream PR, an RFC, a design someone else maintains. It is heavier than the alternatives, so reach for the lighter one when it fits:

| Want | Use |
|---|---|
| To be interviewed about a plan before building | `/grill-me` |
| A checklist pass over a diff | `/code-review` |
| One fresh-context "should this exist at all" | `critic` subagent |
| N independent skeptics, multi-round, to convergence | this skill |

---

## Inputs

| Layer | File | Scope | Why |
|---|---|---|---|
| Reference (stable) | `references/personas.md` | "The proven pair" + the 1–2 entries you picked | Character briefs for the spawn prompts |
| Reference (stable) | `references/personas.md` | "Choosing a panel" | Only when sizing the panel in step 1 |
| Working (per-run) | The artifact under test | Pointer only — paths, PR URL, commit range | See step 1: you pass the pointer, personas read it themselves |

Do not load the whole catalog. Eight of the ten entries are for artifacts you aren't reviewing, and holding them in context biases the panel toward objections nobody is going to raise.

---

## Step 1 — Scope and panel

Confirm what's under test (a diff, a PR, a design doc) and get a *pointer* to it (file paths, PR URL, commit range) — never paste the content into a persona's prompt. Each persona reads it themselves; that's what makes their reaction real instead of a reaction to your summary.

Pick 2–4 personas from `references/personas.md`, chosen by what the artifact actually risks, not by default. A rough recipe:
- Always include one **anchor skeptic** (Puzzled Skeptic) and one **hard gatekeeper** (Blunt Gatekeeper) — they fail in different ways and one will concede points the other won't.
- Add **Security Auditor** if the change touches input parsing, IPC, file I/O, or anything user-suppliable.
- Add **Product Skeptic** if the feature exists on spec rather than a filed issue/request.
- Add **Long-Term Maintainer** if it introduces a new subsystem or abstraction.
- Don't run more than 4 on a small change — past that, personas converge on the same 2–3 objections and the extra rounds are just cost.

## Step 2 — Round 1: independent first reactions

Spawn each persona as a **fresh subagent, never a fork.** Forks inherit this conversation's context and end up primed to be sympathetic to work they watched get carefully built — that defeats the point. Use the `Agent` tool with a generic type (e.g. `general-purpose`), give it only: the persona description, the pointer to the artifact, and an instruction to go read it themselves and write a real review/rejection in that voice, citing specifics (file counts, line numbers, actual behavior) rather than vibes.

Launch all personas for the round **in parallel** (one message, multiple `Agent` calls) — they must not see each other's output.

## Step 3 — Triage in the main thread

Read every objection and classify each one:

| Classification | What it means | What you do |
|---|---|---|
| **Fixable and correct** | The persona found a real gap | Fix the actual code/doc. Don't rebut. |
| **Factually wrong** | The persona misread or assumed something false | Draft a rebuttal citing the specific evidence (the actual test, the actual line, the actual behavior) |
| **Values disagreement** | Real scope/priority/aesthetic disagreement, not a fact either side is wrong about | Name it plainly. Don't try to code your way out of it. |

## Step 4 — Round 2+: resume, never respawn

Reply to each persona by **resuming the same agent** (`SendMessage` to that agent's id/name) — not a fresh one. Resuming preserves their prior stance, which is what makes "does this change your mind?" a real test instead of a blank slate that might rubber-stamp anything. Tell the persona plainly what you did:
- If you fixed something: say what changed and where, and invite it to go re-check the actual file itself rather than trust your description.
- If you're rebutting: give the concrete evidence, not just "that's not true."

## Step 5 — Iterate to convergence or stalemate

Repeat steps 3–4, per persona, until each independently lands on one of:
- **Concedes** — says so explicitly.
- **Bedrock disagreement** — explicitly frames the remaining point as a legitimate scope/values call, not a fact either of you is still wrong about. This is a valid, useful endpoint. Do not keep spinning up more rounds trying to argue away a stated values position — that just wastes rounds and muddies a clean disagreement into a mushy one.

Cap at ~3–4 rounds per persona as a backstop. If a persona is still objecting past that without ever framing it as bedrock, say so honestly to the user rather than forcing a fake resolution either direction.

## Step 6 — Synthesize for the user

Report three buckets, concretely:
- **Fixed** — what changed, with the real diff/commit, because an objection was correct.
- **Rebutted** — what objection turned out to be factually wrong, and the evidence that settled it.
- **Open** — named values disagreements left for the user to decide. Never resolve one of these yourself and never bury it.

---

## Anti-patterns

- Running the debate in the same context that built the feature. Contaminated and sympathetic — always separate agents.
- Respawning a fresh agent each round instead of resuming. Destroys the "did this actually change your mind" signal; a fresh agent might just concede to a persuasive-sounding rebuttal it never actually re-verified.
- Writing a better-worded rebuttal to an objection that's actually correct. Fix the code.
- Treating "bedrock disagreement" as a failure state and running more rounds to argue it away. It's a legitimate stopping condition.
- Silently resolving a values disagreement yourself instead of surfacing it. It's the user's call, not the debate's.
- Running a 5+ persona panel on a small change out of thoroughness-signaling. Match panel size to actual risk surface; diminishing returns set in fast.

See `references/personas.md` for the full persona catalog and when to reach for each one.
