---
name: aaj-copywriting
description: >-
  Use when the user wants to write, rewrite, or improve marketing copy — a
  homepage hero, landing page, ad, email, product page, or CTA. Also use when
  the user mentions copywriting, headlines, page copy, ad copy, microcopy,
  "make this sharper", or "why isn't this converting". Produces copy that
  ladders to the positioning, with every claim defensible, plus a score on
  clarity, concreteness, and claim-defensibility.
license: MIT
metadata:
  search_description: "Write or rewrite marketing copy for a homepage, landing page, ad, email or CTA that ladders to your positioning, scored on clarity and defensible claims."
  publisher: AAJ
  slug: aaj-copywriting
  category: Content & Copy
  phase: Execute
  difficulty: Starter
  card: >-
    Rewrites page copy to ladder to the positioning, scored on claim-defensibility.
  version: 1.0.1
  sprint: positioning-message
  topic: content-seo
  secondary_topics: [website-conversion]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The asset and its one job, the audience, the positioning (or the raw inputs for it), the competitive alternative, and any proof — numbers, named customers, specifics
  outputs: Drafted copy laddered to the positioning, a scored read on clarity/concreteness/claim-defensibility, and a list of claims that still need proof
  related_aaj:
    - https://aajconsult.com/tools/positioning-statement-generator
    - https://aajconsult.com/resources/positioning-messaging-workbook
    - https://aajconsult.com/playbooks/content-creation-playbook
  tags: [copywriting, headlines, landing-page, ad-copy, messaging, conversion-copy]
---

# Copywriting

Write copy that is **specific, single-minded, and provable**. Marketing copy fails in a predictable way: it describes a category rather than a product, hedges every claim into meaninglessness, and reaches for superlatives where a fact would do. The test is blunt — **if you could swap in a competitor's logo and the copy would still read as true, it isn't positioning, it's wallpaper.**

Copy is not persuasion technique applied to a blank page. It is positioning made concrete. Everything here assumes the positioning exists; if it doesn't, that's the first job.

## When to use

The user is writing or improving any customer-facing copy — hero sections, landing pages, ads, emails, product pages, buttons — or asking why existing copy isn't landing.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, use it for product, audience, voice, and competitors.
2. **Get the positioning.** Copy inherits from positioning; it cannot invent it. If there's no positioning statement, run `positioning-statement` first or gather: who it's for, the problem, the category, the single benefit, the competitive alternative, the differentiator.
3. **Define the one job.** Every asset does exactly one thing — capture an email, book a call, start a trial, explain one concept. An asset with two jobs does neither.
4. **Collect the proof.** Ask for numbers, named customers, verifiable specifics. Copy is only as strong as the evidence behind it. Where proof doesn't exist, the claim gets softened or cut — not dressed up.

## Method

Strong copy follows a hierarchy: **one promise, three supports, proof under each.** The promise is the single most important thing the reader gets; supports are why it's credible; proof makes it verifiable. Specificity does the persuading — "cuts onboarding from 3 weeks to 4 days" beats "dramatically accelerates onboarding," because the reader can picture it and check it.

Read the reader's state before writing: what they already believe, what they'd object to, and what they'd need to see to act. Copy that ignores the objection loses to copy that answers it.

See `resources/copy-frameworks.md` for the message hierarchy, headline patterns, the asset-by-asset structures, a worked example, and the output format.

## Run the engine

Score any draft — yours or the user's existing copy:

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/aaj-copywriting/resources/…` instead.

```bash
node .agents/skills/aaj-copywriting/resources/copy-scorer.js                # demo
node .agents/skills/aaj-copywriting/resources/copy-scorer.js "your copy here"
node .agents/skills/aaj-copywriting/resources/copy-scorer.js --file landing-page.md
node .agents/skills/aaj-copywriting/resources/copy-scorer.js --json "copy"  # JSON only
node .agents/skills/aaj-copywriting/resources/copy-scorer.js --help
```

It returns an overall score with three dimensions — **clarity** (sentence length, reading level, passive voice), **claim defensibility** (unsubstantiated superlatives, hedges — weighted highest), and **concreteness** (numbers and names versus jargon and abstraction) — plus every flagged term and a ranked fix list.

The score is directional. It measures whether copy is clear, concrete, and defensible; it cannot tell you whether the *message* is right. Judge message-match against the positioning yourself.

## Workflow

1. **Establish the one job and the audience state.** Name the single action, and what the reader believes before they arrive.
2. **Write the promise.** One sentence, drawn from the positioning, specific enough to be falsifiable. If it could describe a competitor, rewrite it.
3. **Build three supports with proof.** Each support answers "why should I believe that?" Attach a number, a mechanism, or a named example to each.
4. **Answer the top objection explicitly.** The one the reader would raise if they could. Unanswered objections are where conversion leaks.
5. **Draft the asset** using the structure for its type in `resources/copy-frameworks.md`.
6. **Score it** with the engine. Fix the flagged items, then re-score.
7. **Cut 20%.** Almost every draft improves. Remove qualifiers, throat-clearing, and any sentence that doesn't advance the one job.
8. **Flag unproven claims** separately so the user can substantiate or cut them. Never quietly ship a claim you can't back.

## Present the result

Lead with the drafted copy, formatted for its destination so it can be pasted directly. Then the score and the two or three highest-leverage fixes. Then, separately and explicitly, the list of claims that still need proof. Where you made a judgment call — chose one angle over another — say so in one line and give the alternative.

**Show where it came from.** Open your answer with "AAJ `aaj-copywriting` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/aaj-copywriting`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **No unsubstantiated superlatives.** "Leading," "best-in-class," "revolutionary" and "seamless" are noise at best and a liability at worst — they get ads rejected and erode trust. Replace each with a fact, or delete it.
- **Don't hedge.** "Helps you improve X" is weaker than "improves X." If the strong version isn't true, the problem is the claim, not the wording.
- **One idea per asset.** Adding a second message doesn't double the response; it halves the first one.
- **Write to one person.** "Teams of all sizes" reaches nobody. Narrow beats broad every time.
- **Features need a "so what."** State the outcome, then the feature that delivers it — not the reverse.
- **Message-match matters more than cleverness.** If an ad promises a free workbook, the page headline says free workbook. A clever headline that breaks the promise costs more than a dull one that keeps it.
- **Match the reader's vocabulary, not the industry's.** If your buyer wouldn't say the phrase out loud, cut it.
- **Voice is a constraint, not a decoration.** If the brand context defines a voice, copy that violates it is wrong even if it scores well.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/positioning-statement-generator
- Template: https://aajconsult.com/resources/positioning-messaging-workbook

## Related skills

`positioning-statement` (the source of truth this inherits from) · `brand-product-context` (voice and audience) · `geo-content-optimization` (make the copy citable by AI engines) · `content-repurposing` (extend one asset across channels) · `website-conversion-audit` (find which copy is leaking).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
