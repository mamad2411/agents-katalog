---
name: formalize
description: "Agent MUST load when asked to find the mathematical structure in a body of informal work, to boil a design down to its fundamental claims, or to settle a design question or a tied decision by formalizing what the design already commits to."
---

# /formalize \<paths\>

Take the work at the paths into formal-theory-design-expert posture, and
boil it down to its fundamental units: claims, and the structures
relating them. Deliver them as a ledger, per `Skill(llm-claims)`.

The posture is the load-bearing part. Everything below is a way of
holding it under pressure.

> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> That listing is an index of triggers: each filename names the occasion to
> read it. Walk it while planning, before ANY action, and read every entry
> whose trigger matches the work at hand — `when/` entries fire the moment
> the condition holds, not on some later pass.

## Why, before how

A basis pays the moment it exists: open questions clarify and tied
decisions break for free, as soon as you can see what the design
actually commits to. It keeps paying afterward, because a structure that
pins the design down holds a property settled across a change, instead
of surrendering it to be re-derived by hand.

Judge every step below by the six things the basis is bought for:

1. find and resolve inconsistencies;
2. find the minimal basis, and cut the complexity it shows unnecessary;
3. bring a new agent to deep understanding fast;
4. discuss a proposed change rigorously -- by which standing claims it
   breaks;
5. eventually, check a proposed change automatically;
6. eventually, extract a known-good implementation.

The last two are unbuilt. They still inform: a choice that forecloses
mechanization is worth a second look.

## The bar

An identification cashes out as five things, stated in place:

- what the things are;
- what operations act on them;
- what must hold of those operations;
- one smallest example, drawn from the actual data;
- **stale when** -- the condition under which the claim stops holding.

Anything short of five is a name with an argument attached, and names
transfer nothing. A citation proves the structure exists somewhere; it
leaves open whether it holds here.

The ontology comes from schemas and data. Prose says what the author
meant to build, so read it for motivation -- and where the two disagree,
report that, with the ontology still following the data.

When the laws fail, ship the result: *this specific structure is not
here*, for the candidates you actually tried. It saves the next agent
from re-conjecturing them, and it usually localizes the offending part
of the design.

`stale when` earns its place because one condition serves three uses:
against today's data it finds inconsistencies; against a proposed change
it predicts breakage; and it tells a later agent which claims a change
obliges them to re-check.

## Procedure

1. **Survey** wide before framing anything. Report the recurring shapes,
   the tensions, and the places that itch -- before theorizing. The
   itches are the best conjecture seeds you will get. Delegate breadth
   to subagents; keep the judgment.
2. **Conjecture** several candidate structures, cheap sketches, each
   meeting the bar. Keep going while new candidates still change the
   picture. Then kill your own, and say what killed each.
3. **Stratify.** Designs have layers, and a claim's truth is relative to
   the level it is stated at. Say what makes a level a level, and which
   claims survive at which. Where an upper level is definable from the
   level below, say so -- that is where structure is inherited.

Then work the survivors, in order:

4. **Hunt inconsistencies.** Evaluate each claim's staleness condition
   against the data and against the other claims. Adjudicate what you
   find, out loud.
5. **Reduce.** For each claim, ask what still stands if it goes. A claim
   the others entail is a consequence; record it as one. A claim nothing
   else needs is a candidate for cutting -- along with the part of the
   design it was accounting for.
6. **Elaborate.** Read each claim and ask what a program written from it
   alone would do. Where that is underdetermined, the design is
   underspecified there, and that is a finding.
7. **Sort the questions** the work was bought to settle into three
   piles: the ones the formalism decides, the ones it dissolves, and the
   ones that stay open. The dissolved pile is the valuable one -- a
   question that stops being askable was a confusion, and its
   disappearance is a result worth reporting by name. File the sorted
   questions as their own theory, not an appendix to whichever claim
   happened to raise them.
8. **Deliver** the ledger per `Skill(llm-claims)`: one claim per line,
   theories named for the ontology they admit, sigils signing the judge.
   That format lands the account at its own right size. Filing it to an
   on-disk `*.claims.kb/` is optional post-processing, per
   `Skill(llm-claims-kb)`.

   Open with a Layer 0: one sentence the whole basis reduces to, plus
   the small number of named laws it refines into -- a further
   subtraction of the basis, not a second artifact. Say so if the
   design has no true one-sentence reduction; a forced one is worse
   than none.

## Throughout

- **Look for a simpler formalism of equal value**, periodically. The
  good simplification is usually invisible at first framing and obvious
  two steps later, once the structure has met real claims.
- **Unify where the cost is equal.** One concept beats two: it halves
  what a reader carries, and two notions held apart never reveal the law
  they both obey.
- **Spend deliberately.** Tokens are a real budget, traded against
  thoroughness. Say when you are buying depth.

## Handoff

Stay formal. The formal vocabulary is what lets a claim pin anything
down; `/deformalize` takes this output and adds the glossary and the
plain-English successor theories that make it readable.

The reasoning behind everything above, and the place to argue with it:
`design.claims.md`.
