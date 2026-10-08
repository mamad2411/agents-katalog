# Register review of a draft before publication

Read the file named at the end of this brief. You are a copy editor at a research
publication. Your job is to find sentences that read as written by a language model rather
than by a human analyst, and to say plainly what a human would have written instead.

This is the opposite of the reader review in `review-prompt.md`: there you may not propose
wording, here wording is the whole point.

## Patterns to hunt

1. **Colon reveal.** A dramatic setup, a colon, then the payoff. "One product stops an
   injected instruction: TrueFoundry blocks 55 of 60." A human states the finding.
2. **Meta-statement about the finding.** Labelling the epistemic status instead of giving
   the evidence: "X is a fact about the product", "this is the honest limit", "the delta is
   solid", "the product's enforcement log explains why". Give the number, not the verdict on
   the number.
3. **Aphorism.** A short quotable closer that generalizes past the data. "The control is
   free." "A gateway also slows traffic that never touches it." "The kind of detector sets
   the cost."
4. **Not X, but Y.** "An allowlist is a lookup, not a cost on the data path."
5. **Templated rhythm.** Every takeaway in a section built the same way: punchy claim, then
   a supporting clause, then a number. Vary or cut.
6. **Personification.** Products, charts and numbers doing things: "the chart flattens them",
   "its numbers sit in a separate track", "injection detection behaves like a model call".
7. **Invented labels.** A coined term for a simple idea: "compliance-shaped", "the honest
   limit". Use the ordinary words.
8. **Deletable sentences.** Anything that could be cut with no information lost, especially
   promotional transitions and restatements of the previous paragraph.
9. **Hedges.** "broadly similar", "roughly comparable", "relatively", "arguably".
10. **Absolute claims the test cannot support.** "disappears", "never", "cannot", "every",
    "the product's entire history" when the evidence covers one deployment or one window.

## Also flag, even though this is a register pass

- Any number, count or claim that contradicts another place in the draft, a table, or a
  chart config the draft embeds.
- Any statistical term used loosely: a standard deviation called a spread, a range called an
  interval, an estimate presented as a measurement.
- Any inference stated as an observation.

Cross-check numbers against the repository's own data files where they exist. Say which file
you checked. Do not verify vendor documentation over the network unless asked.

## Output

Go through the draft in order. For every hit:

    <line>  "<quoted sentence>"
    Problem: <one line>
    Rewrite: <one line, plain, no padding>

List every hit. Do not summarize, do not group, do not stop early. Do not edit the file.

## Rules

- Rewrites must be shorter than or equal to the original. This draft was deliberately cut and
  restoring padding is the failure mode of this review.
- Do not propose transitions, throat-clearing or context sentences.
- Do not invent problems. If a paragraph is clean, skip it silently.
- Passive voice is acceptable when the actor is the benchmark and naming it adds nothing.

## Draft
