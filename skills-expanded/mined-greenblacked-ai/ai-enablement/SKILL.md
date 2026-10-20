---
name: ai-enablement
description: "Assess how a team uses AI-assisted engineering and produce a rollout plan — baseline current usage, measure the signals of value while refusing the ones that create compliance theatre, check readiness gates on data handling, licensing, review accountability and cost, place the team on the enablement ladder, make repositories runnable by an agent, and run a time-boxed pilot with a pre-registered metric and a kill criterion. Use this skill whenever someone asks how to roll out AI coding tools, whether a team is using them well, what to measure for AI adoption, what repos need before agents can work in them, how to run or evaluate a pilot, or why AI tooling \"is not working here\" — including phrasings like \"we bought licences, now what\", \"is it actually helping\", or \"draft our AI engineering policy\". Not for vendor price comparison, writing code with AI, or writing AGENTS.md itself (agent-instructions)."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# AI Enablement

Good enablement work ends with a team that can say what changed, in numbers they collected before they started, and with a review standard that did not move.

Two failure modes dominate this work, and they look like opposites. The first is enthusiasm: tools rolled out because they are impressive, usage mandated, adoption declared, and no baseline exists so nobody can ever say whether it helped. The second is stalling: a team that concludes AI does not work in their codebase when the real finding is that their codebase is not runnable by a newcomer, human or otherwise. This skill exists to force the unglamorous parts — the baseline, the gates, the repo work — and to keep every claim falsifiable. Interrogate the human for evidence, and where a number was not supplied, write `[TK: metric]` and name where it would come from rather than producing a figure that sounds right.

## Scope

Use for: assessing a team's current AI-assisted engineering practice, designing a rollout, defining what to measure, writing readiness gates and review standards, preparing repositories for agent use, planning and evaluating pilots, and diagnosing a rollout that has stalled.

Do not use for: vendor selection on commercial terms, prompt-level help with a specific coding task, or building the tooling itself. Also not for judging individual engineers by their tool usage — that measurement is the fastest way to destroy the honest feedback the programme depends on.

## Workflow

The work is an assessment followed by a plan. Do not skip to the plan; a plan without the assessment is a set of recommendations that would be identical for any team.

### 1. Baseline before advocating

Find out what people are actually doing today, before proposing anything. Ask, per team:

- Which tools are in use, on what licence, in which surfaces — editor completion, chat, CLI agents, review bots, CI integrations.
- Shadow usage: personal accounts, unapproved tools, browser chat with code pasted into it. This is nearly always present, it is where the real workflow information lives, and it is the source of the most serious data-handling exposure. Ask without consequence attached or it will not be reported.
- What was tried and abandoned, and specifically why. "It was wrong too often" and "it could not run our tests" and "review took longer than writing it" are three different problems with three different fixes.
- Where the current workflow actually hurts — the part of the week people would pay to remove. Enablement that does not attach to a felt pain does not stick.
- Existing usage data from admin consoles, if any, at team-aggregate level only.

Anecdote is not adoption data. "The team loves it" is a hypothesis; seat activation rates, retained weekly usage after month one, and abandonment reasons are the evidence. Where the data does not exist, record `[TK: weekly active users per team, from the vendor admin console]` and treat the baseline as incomplete — which is itself the first finding.

### 2. Decide what to measure, and what to refuse

Measure the delivery system, on comparable work, at team aggregate:

| Signal | What it tells you | Watch for |
| --- | --- | --- |
| Cycle time on comparable work | Whether the change reached delivery, not just typing | Only valid comparing like with like; a shift in work mix invalidates it |
| Review rework rate | Whether generated code costs the reviewer more than it saved the author | Rising rework with flat cycle time means cost moved, not disappeared |
| Time-to-first-PR for new joiners | Onboarding effect, often the largest and earliest measurable win | Small sample; report as a trend across several joiners |
| Incident and change failure rate on AI-assisted changes | Quality effect, the thing enthusiasm hides | Needs a way to tag changes without shaming authors |
| Developer sentiment, qualitative | Whether it helps on real work or only on demos | Ask what they stopped using and why, not satisfaction scores |

Refuse these, and say plainly why when asked for them:

- **Lines of code.** Generation makes the metric trivially inflatable, and more code is a liability, not an output.
- **Acceptance or suggestion-acceptance rate as a headline.** It measures the tool's interaction design, not delivered value. Useful to a vendor; misleading to a manager.
- **Any per-developer usage leaderboard.** Measuring individuals converts a tool into a compliance exercise. People then use it to look compliant, stop reporting where it fails, and the honest feedback the programme runs on disappears. This is not a minor reporting choice; it is the decision that determines whether the rest of the programme gets real information.

### 3. Check the readiness gates

These are gates, not aspirations: scaling past a small pilot without them creates exposure that is expensive to unwind. Assess each as met, partial, or absent. Full detail, including a review-standard wording and an audit checklist, is in `references/readiness-gates.md`.

1. **Data handling** — what may and may not be sent to a model: customer data, personal data, regulated data, third-party confidential material. Written, specific, and reachable from the tools people actually use.
2. **Secrets and code exfiltration** — secret scanning on the paths agents touch, a stated position on which repositories may be sent to which providers, and retention and training terms confirmed per vendor rather than assumed.
3. **Licensing and provenance** — the organisation's position on generated code and its provenance, and whatever attribution or filtering the chosen tools offer.
4. **Review standard** — a human is accountable for merged code regardless of who or what wrote it. This is the load-bearing gate and the one most often left implicit.
5. **Logging and auditability** — for agents with any write access, a record of what ran, on what, at whose request, and what changed.
6. **Procurement and cost visibility** — per-team cost, a trend, and someone who owns the number. Usage-priced agent tooling produces a surprising bill in month three otherwise.

### 4. Place the team on the enablement ladder

Three rungs, in order. The ordering is a dependency chain, not a maturity aesthetic.

**Rung 1 — individual productivity.** Editor completion and chat. Individual workflow, no shared artefacts, no organisational change. Most teams sit here indefinitely and conclude the value is modest, which is an accurate reading of rung 1.

**Rung 2 — team practice.** Repo-level context files, shared prompts and skills held in version control and reviewed like code, agent-assisted review as an input to human review. This is where compounding starts, because the work of one person configuring context benefits everyone touching the repo.

**Rung 3 — system practice.** CI-integrated agents, automated triage and first-pass diagnosis, agents with write access operating behind exactly the controls a human has — branch protection, required review, CI gates, audit trail.

Do not skip rungs. A team that has not agreed a review standard should not be given agents with write access: the control that makes rung 3 safe is precisely the thing rung 2 establishes. Skipping produces either an incident or, more commonly, a quiet decision to stop trusting the tooling.

### 5. Make the repositories agent-ready

Most "AI does not work here" complaints are, on inspection, "our repository is not runnable by a newcomer". An agent has the same needs as a competent new joiner with no tribal knowledge, and it fails louder. This work has value whether or not the AI programme continues, which makes it the easiest part to fund.

Per repository:

- An **`AGENTS.md`** at the root: what the project is, how to set it up, how to run the tests, the conventions that are actually enforced, what not to touch, and how to verify a change locally. Kept next to the code and updated when the commands change.
- **Deterministic setup and test commands** an agent can run without asking — one command to install, one to test, one to lint. If a human needs to be asked which of four commands is current, an agent cannot proceed.
- **Fast feedback.** A forty-minute test suite makes iterative agent work impractical and human work unpleasant. A fast subset that runs in under a couple of minutes is usually enough to unblock both.
- **A CI gate that an agent's change must pass exactly as anyone else's.** No separate track, no relaxed threshold, no auto-merge on a lower bar.

`references/repo-readiness.md` has an `AGENTS.md` outline and a per-repo readiness checklist.

### 6. Run a pilot that can fail

- **Pilot team selection**: a team with a real, felt delivery pain; a repository at or close to agent-ready; a lead who will report honestly rather than protect the initiative; and work that recurs often enough to show an effect within the time box. Avoid the most enthusiastic team if they are also the least representative — their result will not transfer and the organisation will notice.
- **Time-boxed**, six to eight weeks. Long enough to pass the novelty period, short enough that stopping is not a defeat.
- **A pre-registered success metric with a baseline recorded before the start.** Written down, with its threshold, before anyone installs anything. A pilot with no baseline produces a result nobody can dispute and nobody can rely on.
- **A named skeptic** whose objections are written down at the start and answered against evidence at the end. This is not a courtesy. It is the mechanism that keeps the evaluation honest, and it converts the loudest future critic into a participant.
- **An explicit kill criterion**: what result means stop, and what happens to the licences and workflows if it triggers.
- **Then expand**, one team at a time, carrying the artefacts — the `AGENTS.md` pattern, shared prompts and skills, the review standard — rather than only the licences.

Champions and office hours beat mandates. A weekly hour where people bring real problems, plus two or three people whose workflow others copy, moves adoption further than a policy requiring usage — and unlike a mandate, it generates the failure reports you need.

### 7. Produce the assessment and the plan

Rank recommendations by effect over effort, respecting the ladder's dependency order. Say what to stop as clearly as what to start.

## Output format

```markdown
## Current state
[Where the team actually is: tools in use, shadow usage, rung on the ladder,
what was abandoned and why. Every claim sourced or marked [TK:].]

## Gaps by tier
[Readiness gates: met / partial / absent, with the exposure of each gap.
Repo readiness: per repo, what is missing.
Practice: what rung 2 or 3 requires that is not in place.]

## Measurement
[What is being measured now, what should be, what should stop being measured,
and the [TK:] baselines that must be captured before any rollout starts.]

## Recommendations, ranked
[Per item: change | effort (S/M/L) | expected effect | what it unblocks | owner]

## 90-day plan
[Days 0-30: baselines captured, gates closed, pilot repo made agent-ready.
Days 31-60: pilot runs with pre-registered metric and named skeptic.
Days 61-90: evaluate against the pre-registered threshold, decide expand or
kill, and package the artefacts for the next team.]

## Stop doing
[Metrics that damage the programme, mandates, tools nobody retained, and
anything measuring individuals.]
```

## Anti-patterns

**Mandating usage and measuring compliance.** Produces performance of adoption, ends honest reporting of where the tools fail, and leaves you with usage data that predicts nothing.

**A pilot with no baseline.** The result is unfalsifiable, so it is settled by whoever is most senior or most enthusiastic. Capturing the baseline costs days; not capturing it costs the entire evaluation.

**A lower review bar for AI-written code.** Enthusiasm quietly relaxes the standard, defects land, and the programme takes the blame — correctly. The bar is the same, and the accountable human is the one who merges.

**Tool sprawl with no shared context.** Five tools, no `AGENTS.md`, nothing shared between repos. Everyone reconstructs the same context privately and none of it compounds.

**Treating a model upgrade as a strategy.** The next model does not fix an unrunnable repository, an absent review standard, or an unmeasured baseline. Those are the constraints; the model rarely is.

**Skipping rungs.** Agents with write access on a team that has not agreed what "reviewed" means. The controls that make it safe do not exist yet.

**Per-developer dashboards.** Converts a tool into a surveillance instrument and destroys the feedback loop the programme runs on.

**Declaring success from anecdote.** "The team loves it" is a hypothesis. Retained weekly usage, cycle time on comparable work, and rework rate are the evidence.

## Reference files

- `references/readiness-gates.md` — the six gates in detail: what each covers, how to assess it, wording for the review standard, and what to do when a gate is absent. Read before recommending any expansion past a pilot.
- `references/repo-readiness.md` — `AGENTS.md` outline, the per-repo readiness checklist, and the common blockers that make a repo unusable by an agent. Read when preparing repositories or diagnosing "it does not work in our codebase".
