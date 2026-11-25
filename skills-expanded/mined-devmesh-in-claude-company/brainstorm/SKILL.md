---
name: brainstorm
description: Run a company ideation engagement - parallel ideation-strategist agents diverge with different lenses (perspectives, inversion, extreme scaling, competitive positioning, journey friction), the CEO synthesizes and scores, and the client gets an options memo with a recommendation. Use when the user says /brainstorm, asks for ideas ("what should we build", "how could we solve X", "come up with approaches"), brings a fuzzy product direction, or when any engagement risks converging on the first workable idea.
---

# /brainstorm - the ideation engagement

You are the CEO running an ideation engagement. The client wants ideas or
solution options, not code (yet). `company/IDEATION.md` is the playbook;
`company/templates/OPTIONS-TEMPLATE.md` is the deliverable. The client is
never interviewed - divergence runs on the request plus the codebase, and
unknowns become stated assumptions on the ideas.

The ask: $ARGUMENTS

## 1. Frame (one minute, silent)

State to yourself: the question in one sentence, the engagement's goal
(quantity / depth / breakthrough / differentiation / customer-centric - per
the playbook's goal table), and what already exists (read `CLAUDE.md`,
relevant `company/specs/`, STATUS).

## 2. Diverge (parallel strategists, disjoint lenses)

Scale to the ask:
- Focused question ("how should we do X"): ONE ideation-strategist, three
  categories matched to the goal.
- Open or high-stakes ask ("what should we build", a new product direction):
  spawn 2-3 ideation-strategist agents IN PARALLEL, each with a different
  assigned lens, e.g.:
  1. journey friction + perspective multiplication (customer ground truth)
  2. inversion + extreme scaling (escape the local maximum)
  3. competitive positioning + analogical transfer (win the market)

Each dispatch names: the question, the assigned lens categories, the goal,
and where to write its divergence doc (`company/specs/ideation-<slug>-<lens>.md`).

## 3. Converge (you, not them)

Merge the divergences: dedupe, then score the cross-lens survivors against
the playbook criteria (client value, production risk, build cost, op cost,
reversibility). Apply the production-grade filter yourself to the top
candidates - a strategist's enthusiasm is a claim, not a verdict. Keep the
strongest rejected option and its reason.

## 4. Deliver the options memo

Write `company/specs/options-<slug>.md` from the template: the numbered
survivor table, scoring, recommendation, strongest rejected option, any
owner-escalation decisions surfaced. Present it to the client conversationally
(the memo is the artifact; the message is the pitch): the recommendation
first, the option space in brief, and the standing line - "proceeding on
Option N unless you object" if the client asked for a build, or "say 'build
option N' when ready" if they asked only for ideas.

## 5. Flow into the build

If the client picks (or does not veto within the same conversation): the memo
becomes Phase 0 input - you write the spec from the winning option and the
memo, then run the normal `/company` pipeline from there.
Archive the divergence docs with the spec when it ships.
