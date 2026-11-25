---
name: hatsu
description: Skill forging — distilling a team's recurring, hard-won practice into a new installable SKILL.md that meets the nen contract. Use when the user says "write a skill", "create a skill for", "turn this workflow into a skill", "codify our process", or "SKILL.md"; when someone says "we keep solving this the same way" or "the team keeps re-teaching this in review"; after a retro where the same lesson surfaces for the second or third time; or when an agent keeps making a mistake that a written discipline would have prevented.
---

## Stance

発 Hatsu is the ability you forge for yourself, and the law it runs on is the vow: an ability draws its power from what it refuses to do. A skill is that artifact in engineering clothes — a team's recurring, hard-won practice distilled into a document an agent can load and execute cold. Its precision comes from its restrictions. A skill scoped to everything fires on nothing in particular: the trigger matches half of all requests, the guidance dissolves into generality, and readers learn to route around it. The explicit statement of what a skill will not cover is what makes it fire exactly when it should and hit hard when it does.

The stakes are attrition. Without forged skills, the same lesson is re-taught forever in review comments — the same senior typing the same paragraph on the same class of PR, quarter after quarter. Agents repeat the same failure with fresh confidence in every session, because nothing they load carries the scar tissue. And the discipline itself lives in one practitioner's head, which means it resigns when they do. The prose is not the ability. The restriction is.

## Boundaries

If the need is to plan, dispatch, or orchestrate work using skills that already exist, stop — that is manipulator's job. Hatsu fires only when the routing table comes up empty: a recurring need that no existing skill covers. Forging is what you do when there is nothing left to dispatch.

Never forge what already exists. If the recurring pain is unmeasured performance work, that is enhancer; code hostile to change, transmuter; an unchosen goal that needs framing, emitter; an external system's undocumented behavior, specialist; what the system does when a call fails, conjurer. A new skill that paraphrases a sibling splits one trigger surface across two documents, and afterwards neither fires reliably. Check the table before you light the forge.

Revising an existing skill's text is editing, not forging. Sharpen a description, correct a trace, tighten a method step — do it directly against the contract, with the lint as reviewer. The forge is only for abilities that do not exist yet.

A restriction and a vow share one law but not one lifetime. The restriction the forge writes into a skill is design-time and permanent — what the ability refuses to cover. The pledge an agent declares before a single task is run-time and expires with it: that is vow's territory, not a skill's text. Vow also feeds the forge — the same pledge breaking across sessions, transcripts attached, is precisely the three-occurrence evidence the Method's first step demands.

## Method

1. **Prove the pattern recurs — three real occurrences, with artifacts.** Review comments, incident notes, session transcripts: collect and link them. One occurrence is an anecdote, two is a coincidence worth watching, three with artifacts is a pattern that justifies a permanent document. If you cannot produce three, file what you have and wait; the forge does not run on foresight.

2. **Check the routing table.** Walk every existing skill's description against the need. If one of them should have fired and didn't, the defect is that skill's trigger surface — fix it there and stop. Forge only when the need genuinely belongs to no one.

3. **Name the discipline, then write the restrictions before any guidance.** One sentence: the discipline and what it costs when absent. Then the vow — what this skill explicitly refuses to cover. This comes first because it is the hardest part to add later: guidance written before its restrictions sprawls to fill every adjacent concern, and no edit ever fully pulls it back. A skill that cannot say what it won't do cannot say when it applies.

4. **Write the description before the body.** The description is the trigger surface; it decides whether the skill ever loads, which makes it more load-bearing than anything beneath it. Make it pushy and stock it with literal phrasings users actually type, not categories of phrasing. "Use when doing deprecation work" retrieves nothing; "when a changelog says removed with no prior deprecated" retrieves the exact moment.

5. **Write the six-section body per the contract.** Stance with stakes; boundaries that name real siblings and hold reciprocally; a numbered, executable method; a worked trace drawn from one of the three real occurrences — never invented; anti-patterns as artifacts visible in a diff or transcript, taken from real failures; done-means as evidence a third party can inspect.

6. **Run the lint and fix every FAIL.** `python3 scripts/lint-skills.py` — frontmatter keys, section order, the fenced block in the trace, sibling naming. The lint is the contract's teeth; a skill that fails it is not installable, whatever its prose says.

7. **Trial-fire on a live task and revise from what the transcript shows.** Load the skill on the next real occurrence of the pattern and watch where the agent hesitates, over-applies, or asks a question the skill should have answered. Every hesitation is a defect in the text, not the reader. A skill that has never fired is a draft, not an ability.

## Worked trace

Report from the field: a platform team keeps shipping breaking API changes with no deprecation notice. Step 1, prove recurrence — three artifacts, collected before any writing:

```
occurrence 1  PR #241 review (Mar): "you removed `page` from /v2/orders
              params with no deprecation window — mobile 3.18 still sends
              it" — hotfix #243 restored the param two days later
occurrence 2  INC-88 (Apr): partner webhook field renamed in place;
              3 integrators broke, 11 support tickets, public postmortem
occurrence 3  PR #310 review (Jun): same reviewer, same paragraph, third
              time: "breaking change, no notice, no sunset header"
```

Step 2, routing table: conjurer owns failure policy, transmuter owns restructuring, specialist owns other people's systems — nobody owns the contract between a published interface and its consumers. The table is empty; the forge is justified. Step 3, name and vow, restrictions written before a single line of guidance:

```
deprecator — consumer-notice engineering for published interfaces.
REFUSES to cover: whether the change should ship at all (design review),
how the API is versioned (architecture), and internal symbols with zero
callers outside this repo. Fires only when a published interface changes
shape and someone who cannot see this diff depends on it.
```

Step 4, description drafted before the body, phrasings lifted from the three artifacts: "Use when a PR deletes or renames a public field, header, or endpoint; when someone says 'just remove it, nobody uses it'; when a changelog entry says 'removed' with no prior 'deprecated'; or when a partner-facing payload changes shape in one release." Step 5, the six-section body, with the worked trace retelling INC-88 — the real incident, ticket numbers and all. Step 6, lint:

```
$ python3 scripts/lint-skills.py
FAIL: deprecator: '## Boundaries' must name sibling 'conjurer'
FAIL: deprecator: '## Worked trace' needs at least one fenced code block
LINT FAILED (2)
```

Two structural misses — the conjurer hand-off (deprecation window expires, calls start failing: whose policy?) and a trace written as prose. Both fixed; rerun prints `LINT OK`. Step 7, trial-fire on PR #317, a live response-field rename. The skill fires — but the transcript shows the agent stalling on whether an internal admin endpoint counts as "published", then guessing. That hesitation is a defect in the vow, so the restriction line gains a definition: published means consumed by code outside this repository. One firing, one revision. Now it is an ability.

## Anti-patterns

- **A description that is just the skill's title.** "Use when doing performance work" — no literal phrasings, nothing a user would actually type. The skill exists and never loads; the transcript shows the pattern recurring with the skill sitting installed and silent.
- **A forged skill with no restriction statement.** Every section says what it does, nothing says what it refuses. It fires on everything adjacent, gets overridden three times in a week, and is trusted on nothing thereafter.
- **A worked trace with no source occurrence behind it.** Round numbers, no ticket IDs, no PR links — a reviewer asks "which incident was this?" and there is no answer. The trace teaches an incident that never happened.
- **A skill forged after one incident.** The evidence section cites a single occurrence. That is an anecdote wearing a discipline's clothes, and the second real occurrence usually proves the generalization wrong.
- **A body that paraphrases an existing sibling.** Diff the new skill against the routing table's nearest neighbor and half the method steps match. The table was never checked; one trigger surface is now split across two documents.
- **A skill merged without a trial-fire.** No transcript of it ever loading on a live task. Its first real firing happens in production, on someone else, with the defects still in.

## Done means

- Three occurrence artifacts linked in the session or PR — review comments, incident notes, transcripts — predating the skill's first draft.
- The routing-table check visible: each existing skill named and ruled out, or the work rerouted and no skill forged.
- A restriction statement in the new skill's Stance or Boundaries that names what it refuses to cover.
- A description containing literal user phrasings, written before the body and traceable to the occurrence artifacts.
- Boundaries that name manipulator's territory where the need is orchestration, and route sibling-shaped needs to the sibling.
- A worked trace that cites one of the three real occurrences, with its identifiers.
- `python3 scripts/lint-skills.py` exiting clean, output quoted.
- One trial-fire transcript observed, and at least one revision made from what it showed.
