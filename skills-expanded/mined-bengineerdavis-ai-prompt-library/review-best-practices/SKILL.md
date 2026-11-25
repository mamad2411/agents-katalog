---
name: review-best-practices
description: Researches what already exists — tools, standards, and what practitioners actually do — then ranks the options against the stated requirement and records what was rejected, so a plan is built from findings instead of invention. Use before a planning stage that will commit to an approach, before building a mechanism that is plausibly already solved (templating, config, permissions, release process, testing strategy), when adopting a convention, or when a claim about an external tool's capability is load bearing.
spec_hash: 54eaaa443440
---

# Review Best Practices

Research first; the output of this skill is an input to planning, not a plan.
Look, rank against the requirement, and write down what you rejected.

You will want to build. Building is more satisfying than searching, and you can
usually produce something that works. That is exactly the failure: a bespoke
mechanism where a well-tested one existed, carrying maintenance nobody budgeted
for and missing every affordance the community version accumulated.

This is not a ban on building. It is a ban on building **by default**.

"Best practices" names what you go looking for. It is not a standard of proof —
what most people do is evidence about the options, never evidence about fit.

## Pairs with questioning

Run `interaction-questioning` first, or alongside. It establishes what is
actually being attempted; this skill finds what exists and ranks it against
that. Reverse the order and you get a careful ranking against a requirement
nobody confirmed.

The pairing runs both ways. If what you find contradicts the stated goal, that
goes **back** to questioning — see "Send it back" below. Research is the
cheapest place to discover a plan does not fit its goal; every later place
costs more.

## Workflow

1. **Name the requirement first, in one sentence**, before searching. Include
   the capability that would disqualify a candidate. Searching before you know
   what would eliminate an option produces a survey, not a decision.
1. **Search at least three kinds of source.** Established tools; relevant
   standards or specifications; what practitioners report actually doing. Each
   is blind to what the others see — a tool search misses that everyone
   abandoned it, a standards search misses that nothing implements it.
1. **Verify any capability that matters.** Check the tool's source, its
   `--help`, or run it. Do not rely on recall.
1. **Rank against the requirement**, leading with the disqualifying capability.
1. **Decide**, and record the rejected options with the reason for each.

Time-box it. A search that finds nothing is a finished search — say so and build.

## Rank by what eliminates, not by what is popular

Put the capability most candidates lack at the top of the ranking. That is the
one doing the work; everything else is a tie-breaker.

> **Worked example.** The requirement is "improve a project template later and
> pull that change into projects already generated from it." Cookiecutter is by
> far the most widely used templating tool and cannot do this at all. Copier and
> cruft can. Ranking by adoption puts the one tool that fails the requirement
> first. Ranking by the disqualifying capability eliminates it immediately, and
> the remaining comparison is short.

An incumbent — already installed, already used here — is the **baseline to
beat**, not the default to keep. Say what would have to be true for switching to
be worth its cost.

## Verify claims against the artifact

When you are about to assert that a tool supports something, and the design
depends on it, check.

> **Worked example.** "Copier templates can inherit from a parent template" is
> the kind of claim that sounds right. Grepping the installed source for
> `extends`, `inherit`, `parent_template` and `base_template` returns nothing:
> there is no inheritance, only composition through separate answers files. A
> design built on the unchecked version of that claim fails at the point where
> the tool is supposed to do the thing it cannot do.

Recall about a fast-moving tool is a guess with good grammar.

If a check contradicts something you already stated, correct it where you stated
it — in the file, the commit message, the task — not only in conversation.

## Send it back

If the search shows the requirement is mis-framed, self-contradictory, or
already satisfied, say so and return the question. Do not quietly pick the
least-bad option against a requirement that does not hold.

- **Nothing clears the bar?** Report that the requirement needs revisiting.
  A ranking of options that all fail reads as a recommendation and is not one.
- **Already solved by something in place?** Say that. The requirement was for
  an outcome, not for a new component.

## Record what you rejected

Alongside the decision, name the options considered and what disqualified each.

Without that record, the decision cannot be revisited when a rejected option
improves, and it is indistinguishable from never having searched. The next
person re-runs your search, or skips it because you appear to have done it.

## When this does not apply

- Work whose value is that it is specific: domain logic, your own data, your own
  requirements. Nobody else has solved that.
- Cases where the dependency is itself the cost — a deliberately zero-dependency
  script. State that constraint and skip the search; do not perform it and then
  ignore the result.

## Never

- Never present a custom design as the first option for a plausibly solved
  problem.
- Never return a survey of options instead of a recommendation. The deliverable
  is a decision with its reasoning.
- Never treat popularity, star counts, or "it is already installed" as evidence
  that something meets the requirement.
- Never let this become a reason to defer. Time-box, then proceed.
