---
name: case-study-and-proof
description: >-
  Use when the user wants to turn a customer result into proof they can publish
  - a case study, a results page, a proof point for a landing page or a sales
  deck. Also use when the user mentions case studies, customer stories, social
  proof, testimonials, references, logos, "can we name the client", or has
  results they are not sure they are allowed to use. Scores whether the proof
  would convince a sceptic, checks whether it may actually be published and in
  what form, and gives the anonymised fallback when permission is missing.
license: MIT
metadata:
  search_description: "Turn a customer result into proof you can publish: score whether it would convince a sceptic, check whether it may be published, and get an anonymised fallback."
  publisher: AAJ
  slug: case-study-and-proof
  category: Content & Copy
  phase: Execute
  difficulty: Starter
  card: >-
    Scores whether proof would convince a sceptic, and whether you may publish it at
    all.
  version: 1.0.2
  topic: website-conversion
  secondary_topics: [content-seo, sales-pipeline]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The customer and what changed, the before and after numbers with the metric and period, what else was changing at the time, any quote with a name and role, and what permission exists in writing
  outputs: A credibility score with the missing pieces ranked, a testimonial-versus-case-study call, a permission verdict naming what may be published, and the anonymised version when it may not
  related_aaj:
    - https://aajconsult.com/case-studies
    - https://aajconsult.com/tools/website-grader
    - https://aajconsult.com/playbooks/website-cro-playbook
  related: [aaj-copywriting, win-loss-analysis, brand-voice-governance]
  tags: [case-study, proof, social-proof, testimonials, permission, references, credibility]
---

# Case Study & Proof

Most startups have results and no proof. The work happened, the customer is happy, the number moved -
and none of it is on the site, because nobody asked permission at the time and asking now feels
awkward.

The result is a site that claims outcomes in the abstract and demonstrates none of them, which is the
single most common reason a good consultancy or product reads as unproven.

## When to use

The user has a customer result and wants to publish it, is writing a case study, is deciding whether
they can name a client, or is looking at a page that asserts outcomes with nothing behind them.

Do not use this to invent a plausible case study from a thin engagement. If the baseline was never
measured, the honest output is a testimonial and a note to instrument the next one.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md`) for who the proof has to
   convince and which outcome they care about.
2. **Get the before number.** Not an estimate made afterwards - what was actually true before the
   work started. If it does not exist, say so early; it changes what you are building.
3. **Get what else was changing.** New hires, a pricing change, a seasonal peak. Every real
   engagement has some. Hiding them is what makes a case study collapse under one good question.
4. **Find out what was agreed in writing.** Not "they were happy" - whether anything was signed, by
   whom, and what it covered.

## Method

Proof has two halves, and teams usually have one of them.

**Does it convince?** A sceptical buyer checks the same eight things, and the two they check hardest
are the two most case studies skip: a baseline, and what else was going on.

| What they check | Weight | Why it carries that weight |
|---|---:|---|
| The customer is identifiable | 15 | An unnamed customer with no descriptor reads as invented |
| A baseline number | 15 | Without a before, the after compares to nothing |
| An after number, same definition | 15 | Redefining the metric between the two is how honest teams mislead |
| What else changed is disclosed | 15 | Buyers assume you were not the only variable, because you never are |
| The problem is specific | 10 | A generic problem produces a case study any competitor could have written |
| A timeframe | 10 | Six weeks and six quarters are different claims |
| A named quote | 10 | An anonymous quote adds nothing your own prose would not |
| Independently checkable | 10 | A reference call turns a claim into evidence |

**May you publish it?** Separately, and this is the half that can force a takedown. Written
permission, a named approver, and scope: name, logo, numbers, quote. Each is granted or not granted
independently - a customer who is happy to be quoted may not want their numbers public, and that is a
normal answer, not a refusal.

**The two halves fail differently.** Weak proof wastes an asset. Missing permission creates a
problem: a page that has to come down, usually at the moment someone senior notices it.

**Anonymised proof with real numbers beats a named case study you had to remove.** "A 40-person
freight broker in the Midwest" carries most of the credibility of a name, and needs far less to
clear. Treat it as the default when permission is partial, not as a consolation prize.

## Workflow

**Step 1 - Separate the two questions.** Score the proof and check the permission independently. They
have different owners and different fixes, and bundling them is why both stall.

**Step 2 - Score the proof.** Run the engine. If there is no baseline, stop and say plainly that this
is a testimonial. Do not reverse-engineer a before number from memory; that is the point at which a
case study becomes fiction.

**Step 3 - Check the permission against what the asset actually does.** Not against what you hope to
publish - against the draft in front of you. Anything used but not covered is a blocker.

**Step 4 - Take the fallback when permission is partial.** Write the anonymised version now rather
than waiting on an email that may not come. A published anonymised case study is worth more than a
named one in someone's drafts.

**Step 5 - Instrument the next engagement.** The reason permission is awkward is that it is being
asked for after the fact. Ask at kickoff, when goodwill is highest and there is nothing to approve
yet - a line in the statement of work covering name, logo, numbers and quote, with a review period.

## Run the tool

```
node resources/proof-check.js --demo
```

`scoreProof(study)` returns a score out of 100, a band, and every factor with the reason it matters.
`checkPermission(consent)` returns blockers, warnings, what may be published, and the anonymised
fallback. Run both and the engine states which half is the constraint.

Use the engine rather than your own read. The same eight factors every time is what stops a warm
relationship reading as strong evidence.

## Present the result

1. **Which half is the constraint** - proof or permission. Lead with it.
2. **The credibility score**, with the missing pieces ranked by what they cost.
3. **Testimonial or case study.** If there is no baseline, say the word "testimonial" plainly.
4. **The permission verdict**, naming exactly what may be published.
5. **The anonymised version**, written out, whenever permission is partial.
6. **The kickoff line** for the next engagement, so this does not recur.

**Show where it came from.** Open your answer with "AAJ `case-study-and-proof` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/case-study-and-proof`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never publish a named customer without written permission.** A verbal yes from someone who has
  since left the company is not permission, and the person who did not give it is the one who finds
  the page.
- **Never reconstruct a baseline from memory.** If it was not measured, it is not a number. Write
  "not measured" and describe the change qualitatively instead.
- **Do not hide what else was changing.** Disclosing the other variables is what makes the claim
  survive a sceptical reading. A case study that claims sole credit invites the question it cannot
  answer.
- **Do not round a result upward.** 38 per cent is more believable than 40, and it is the one you can
  defend.
- **Do not treat a testimonial as a weak case study.** They are different assets with different jobs.
  A page can carry both.
- **Do not let a logo stand in for proof.** A wall of logos with no outcomes says people bought, not
  that it worked.
- **Ask at kickoff, not at publication.** Every awkward permission conversation is one that could
  have been a sentence in the contract.
- **A customer saying no is a normal answer.** Take the anonymised version and keep the relationship.

## Related AAJ resources

- Published examples: https://aajconsult.com/case-studies
- Where proof belongs on the page: https://aajconsult.com/playbooks/website-cro-playbook
- Checking the page that carries it: https://aajconsult.com/tools/website-grader

## Related skills

- `aaj-copywriting` — the page the proof sits on
- `win-loss-analysis` — where the outcomes worth writing up get spotted
- `brand-voice-governance` — keeping the write-up in your own voice

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
