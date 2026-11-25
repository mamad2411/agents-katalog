---
name: ai-marketing-governance
description: >-
  Use when a marketing team has adopted AI faster than anyone wrote rules for it
  — deciding which tools are approved, what must never go into a prompt, who
  reviews before publish, and how AI-drafted claims get fact-checked. Also use
  when the user mentions AI policy, AI governance, AI usage rules, AI disclosure,
  hallucinated citations, fake statistics, made-up sources, prompt data leakage,
  "is it safe to put this into ChatGPT", or reviewing AI-written marketing copy.
  Produces an adoption-readiness verdict, a completed policy with a named owner,
  and a per-claim citation check applied before anything publishes.
license: MIT
metadata:
  search_description: "Set rules for AI in marketing: approved tools, what never goes in a prompt, who reviews before publish, and a claim check, with a policy and a named owner."
  publisher: AAJ
  slug: ai-marketing-governance
  category: Content & Copy
  phase: Execute
  difficulty: Intermediate
  card: >-
    Scores whether a team's AI use is governed, and refuses citations that cannot be
    checked.
  version: 1.0.1
  topic: ops-ai-team
  secondary_topics: [brand-voice, content-seo]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Which AI tools the team uses and for what, whether the plan trains on inputs, who reviews before publish, and the claims and citations in a draft
  outputs: A readiness score with the gaps named, a filled-in policy with owners and a review date, a per-citation verdict, and the five rules as a card the team can pin up
  related_aaj:
    - https://aajconsult.com/resources/ai-tool-policy
    - https://aajconsult.com/blog/why-ai-content-doesnt-sound-like-you
    - https://aajconsult.com/resources/brand-voice-guide
  related: [brand-voice-governance, seo-content-brief, aaj-copywriting]
  tags: [ai-policy, governance, fact-checking, citations, disclosure, marketing-ops, review-gate]
---

# AI Marketing Governance

AI can get a marketing team to a draft far faster than it could get there alone. What it cannot do
is take responsibility for what goes out. This skill is the set of checks that sit between the draft
and the publish button.

One principle carries everything: **AI drafts. People decide and sign.**

## When to use

The team has started using AI on company work with no written rules, a founder wants a policy they
can adopt this week, someone is about to publish AI-drafted content, or a figure in a draft needs
checking before it ships.

Do not use this to write an aspirational AI ethics statement. A policy nobody owns is a document,
not a policy — every section here ends in a name.

## Before you start

1. **Read the brand/product context first** (`.agents/product-marketing.md` / `.agents/aaj-brand.md`).
2. **Get the actual tool list,** by task and by person. "AI" is not a tool, and a policy that does not
   name them cannot be followed.
3. **Get the plan tier for each tool,** because whether it trains on inputs depends on it. Business
   and enterprise tiers usually do not; consumer tiers often do, and the default is rarely the safe
   one. If the user does not know, that is the first finding, not a blocker to note later.
4. **Get the reviewer's name.** Not "the team" — a person.

## Method

Two failures are being prevented, and they are not the same.

**Leakage** is what goes in. Treat every prompt as though it may be read by someone outside the
company, because it may be.

**Fabrication** is what comes out, and it is the one most policies leave out. AI models generate
plausible citations, not retrieved ones. Asked for a statistic, a model produces something with the
right magnitude, attributed to a firm that genuinely publishes research in that area, with a sample
size that sounds like a real study. It reads as evidence because it was built from the shape of
evidence:

- *"In CB Insights' 2021 analysis of 110+ startup post-mortems, 35% of failed startups cited no market need."*
- *"CB Insights found Series A companies with strong positioning raise their next round 30% faster."*

The first is real, and even it is easy to get wrong: an older CB Insights edition put the figure at
42%, and the page that used to host it now serves a newer edition with different numbers. The edition
and the year travel with the figure, or the figure is wrong. The second does not exist. To a reader — and to the model that wrote them — they
are indistinguishable. That is not carelessness; it is what generation does when no document is in
the loop.

**The working rule: ask AI for the argument, not the statistics.** Add figures afterwards, one at a
time, each from a document the user has opened themselves.

## Workflow

1. **Score adoption readiness.** Run the engine. Report the verdict and every failed check verbatim.
   Lead with the blockers.
2. **Fill the approved-tools table** — task, tool, who may use it, notes. Anything not on the list
   needs the owner's approval before use on company work. Review it quarterly; tools change faster
   than policies do.
3. **Verify the training setting** rather than assuming it, and write the answer down with the date
   and who checked: *Our plan trains on inputs: Yes / No · Verified on [date] by [name]*.
4. **Write the never-in-a-prompt list** and keep it concrete: customer names and lists; unannounced
   pricing, roadmap or financials; anything under NDA; employee records and compensation;
   credentials, API keys and tokens; and anything the user would not be comfortable seeing in a
   screenshot on social media.
5. **Name the reviewer and the gate.** Nothing AI-drafted publishes without a named human reviewer
   who answers four questions and is accountable for the answers:
   - Is every factual claim in this true, and can I show where it came from?
   - Does it sound like us, or does it sound like everyone?
   - Does it promise anything we cannot deliver?
   - Would I be comfortable if a customer knew AI drafted it?

   If any answer is no, it does not ship. The reviewer's name goes in the doc, the ticket or the CMS
   field — somewhere it survives the week.
6. **Check every citation** with `checkCitation`. A published figure carries the organisation that
   ran the study (not the one that repeated it), the document's title and date — and edition, if it
   is an annual — the sample (how many, of what, measured when), and a link on that organisation's
   own domain.
7. **Set the disclosure line.** Disclose where the reader's judgement depends on who wrote it: a
   founder's personal note, a customer story, a case study, anything under a named byline that the
   named person did not write. Routine drafting help on marketing copy needs no more disclosure than
   a spellchecker.
8. **Assign ownership and a review date.** Who owns the policy, who approves a new tool, how a new
   tool is requested, and when it is next reviewed. Quarterly is the default.
9. **Hand over the five rules as a card** to pin up, not as a document to file.

## Run the tool

```
node resources/ai-governance.js --demo
```

`scoreReadiness(state)` returns a score, a verdict, every check with its reason, and what is missing
before the team should be publishing AI-drafted work at all. `checkCitation(citation)` applies the
section-5 rules to one source, and `checkDraft(draft)` sweeps a draft for unsourced figures,
never-cite patterns and missing disclosure.

Use the engine's output rather than your own read of a source — the same rules every time is the
point.

## Present the result

1. **The principle,** stated once: AI drafts, people decide and sign.
2. **The readiness verdict and score**, blockers first, each failed check with its reason.
3. **The approved-tools table**, with owners filled in and any blank cell named as a blank.
4. **The training-on-inputs answer**, with its verification date, or flagged as unverified.
5. **The reviewer's name** and where it will be recorded.
6. **Every citation checked**, with the failures quoted.
7. **The five rules card.**

**Show where it came from.** Open your answer with "AAJ `ai-marketing-governance` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/ai-marketing-governance`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## The five rules

1. **AI drafts. People decide and sign.** No exceptions, no "it was only a social post".
2. **Use the tools on the list.** Anything else needs approval first.
3. **Nothing confidential goes into a prompt.** Customers, pricing, NDAs, credentials — none of it.
4. **Ask for the argument, not the statistics.** Add every figure yourself, from a document you opened.
5. **A named person reviews before publish.** Their name goes somewhere that survives the week.

## Guardrails & common mistakes

- **Never invent a quote, a review or a testimonial.** There is no version of that which is a
  shortcut rather than a fabrication.
- **Never publish AI-generated words under a named person's byline** without that person reading and
  approving them.
- **If a claim needs a number that cannot be found, the claim is wrong** — not under-researched. This
  is the line that saves the most trouble.
- **Never cite** an AI-generated aggregator or "research" page that republishes other people's work;
  a publisher's index, tag or category page (a citation resolves to one document); a preprint
  described as a conference or journal paper — label it a preprint with its identifier; anything
  reached "via" a third party, because *via* in a source list is a confession; or a firm that no
  longer exists, for a figure that cannot be opened today.
- **Do not accept the plan's privacy default.** Check whether the tier trains on inputs, write the
  answer down, and re-check it when the plan changes.
- **Do not let "the team" be the reviewer.** Accountability that is not a name is not accountability.
- **Do not over-disclose.** Disclosing routine drafting help trains readers to ignore disclosure
  where it matters.
- **A policy with no owner and no review date is a document.** Refuse to hand one over in that state.

## Related AAJ resources

- The one-page template this skill fills in: https://aajconsult.com/resources/ai-tool-policy
- Why the drafts converge, and what the same pull does to facts: https://aajconsult.com/blog/why-ai-content-doesnt-sound-like-you
- The voice rules the review gate checks against: https://aajconsult.com/resources/brand-voice-guide
- What a sourced figure looks like: https://aajconsult.com/benchmarks

## Related skills

- `brand-voice-governance` — the "does it sound like us" half of the review gate, at scale
- `seo-content-brief` — where citation targets get chosen before drafting starts
- `aaj-copywriting` — the drafting this policy governs

## Credits

Written by AAJ (aajconsult.com). Method from the AAJ AI Tool Policy for Marketing. MIT licensed.
