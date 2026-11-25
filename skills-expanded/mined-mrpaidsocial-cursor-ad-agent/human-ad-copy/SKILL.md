---
name: human-ad-copy
description: >-
  Writes and revises specific, natural direct-response ad copy without generic
  AI-writing habits. It applies to every request for Meta, Facebook, or Instagram
  primary text, body copy, hooks, headlines, titles, descriptions, copy variants,
  or meta-ad-builder copy.json files. It also applies when copy needs to be
  humanized, de-slopped, checked for AI tells, or adapted from winning ads.
---

# Human ad copy

Write copy that earns attention through a real observation, useful detail, or
checkable claim. Do not try to "beat" AI detectors. Authorship detectors are
unreliable, and no wording pattern proves who or what wrote a passage. This
skill is an editorial system for removing generic patterns that readers often
associate with low-effort generated copy.

**Hard requirement (operator mandate): never use em dashes (`—`) in ad copy.**
This applies to every body, title, description, hook, and draft, with no
exceptions. Rewrite with a period, comma, colon, or a split sentence. The
validator treats any em dash as a HARD failure that blocks handoff.

## Required inputs

Before drafting, identify:

- Offer: product, price or terms, mechanism, and destination.
- Audience: situation, awareness level, pain, desired outcome, and objections.
- Creative: what the image or video already communicates.
- Voice: supplied brand guidance or representative approved copy.
- Receipts: verified numbers, dates, names, features, demos, quotes, results,
  constraints, and failures.
- Action: the one thing the reader should do.

Ask only for missing facts that materially change the copy. If a draft can
proceed with placeholders, use explicit brackets such as `[verified result]`.
Never turn an assumption into a claim.

## Workflow

### 1. Build a claim ledger

List each material claim and its source before writing. A receipt can be a
measured result, product specification, named source, customer quote, screenshot,
demo, policy, price, or dated event.

- Keep verified claims.
- Mark claims that still need evidence.
- Cut claims that cannot be checked.
- Preserve testimonials verbatim apart from approved typo fixes. Never invent a
  customer, quote, statistic, deadline, scarcity condition, or endorsement.

Specificity is not decoration. A precise unsupported number is still false.

### 2. Choose genuinely different angles

Read [the 15 direct-response frameworks](references/frameworks.md), then match
frameworks to the available receipts and the creative. One framework is enough
for one ad. A variant set should test different bets, not synonyms.

Change at least two of these between primary-text variants:

- reader problem or awareness level
- opening mechanism
- proof or receipt
- objection
- framework
- call to action

Do not label five paraphrases as five concepts.

### 3. Draft in plain language

Apply these defaults:

1. Lead with the pain, result, observation, or receipt. Skip scene-setting.
2. Prefer plain verbs such as `is`, `has`, `uses`, `built`, `tested`, and `saved`.
3. Give every material benefit a mechanism or proof point.
4. State the positive claim directly. Avoid negative rhetorical seesaws.
5. Never use em dashes. This is a permanent operator mandate, not a style
   preference.
6. Vary sentence and paragraph length naturally. Fragments are allowed when
   they fit the brand voice.
7. Avoid mechanically balanced triads, identical bullet shapes, and repeated
   CTA syntax.
8. Repeat the natural product name instead of inventing elegant synonyms.
9. Admit real constraints when relevant. Do not manufacture flaws to sound human.
10. Replace generic adjectives with facts, not different generic adjectives.

Read [the AI-tell editorial rules](references/ai-tells.md) before the final pass.
These are heuristics and house rules, not evidence of AI authorship.

### 4. Fit the Meta fields

These are creative guidelines, not universal platform limits. Placements and
rendering can vary.

- **Primary text (`bodies`)**: put the hook or proof in the opening line. Roughly
  125 characters often appear before expansion, but long primary text is valid.
- **Headline (`titles`)**: aim for about 40 characters or fewer. Make it concrete
  enough to work with any body in the set.
- **Description (`descriptions`)**: aim for roughly 30 to 50 characters. Use a
  supporting fact, term, or mechanism rather than a second headline.
- **Liquidity set**: default to 5 bodies, 5 titles, and 3 descriptions when
  preparing copy for this repository's `meta-ad-builder`.

All titles and descriptions should pair truthfully with all bodies because Meta
may mix them. Do not rely on a description to carry required context.

### 5. Validate mechanically

Save the draft as text or save the deployment payload as JSON, then run:

```bash
python3 skills/human-ad-copy/scripts/validate_copy.py draft.txt
python3 skills/human-ad-copy/scripts/validate_copy.py copy.json
python3 skills/human-ad-copy/scripts/validate_copy.py copy.json --output json
```

The validator checks this `meta-ad-builder` shape:

```json
{
  "bodies": ["primary text 1", "primary text 2"],
  "titles": ["headline 1", "headline 2"],
  "descriptions": ["supporting line 1"]
}
```

For deployment, use 5/5/3. Titles and descriptions may also use the supported
`{"text": "..."}` form, while bodies must be strings.

Finding levels:

- `HARD`: deterministic contract failure, including an em dash, invalid JSON
  shape, empty value, or exact duplicate variant. Fix before handoff.
- `REVIEW`: heuristic editorial cue, lexical near-duplicate, unsupported-claim
  cue, or count/length guidance. Inspect in context.

Exit code `1` means hard findings exist. Review-only findings return `0`.
CLI or unreadable-input errors return `2`. A clean scan does not certify human
authorship or guarantee performance.

### 6. Make the judgment pass

The scanner cannot reliably judge truth, voice, rhythm, semantic paraphrase, or
strategic fit. Read the set aloud and ask:

- Does the first line earn the second?
- Could this sentence describe ten unrelated offers?
- Is each claim traceable to a receipt?
- Would a real customer or operator use these exact words?
- Does each variant test a different reason to act?
- Does the CTA match the destination and creative?

## Output contract

When the user requests `copy.json`, return valid JSON with only the deployment
fields unless they ask for commentary. Keep unverified notes outside the JSON.
When no format is specified, label primary text, headline, and description
clearly, followed by a short `Claims to verify` list only when needed.

## Rewrite examples

Illustrative facts below are placeholders, not claims to reuse.

Generic:

> Unlock a seamless way to transform your workflow and achieve powerful results.

Specific:

> Thursday's report took 47 minutes because three CSV exports broke. This tool
> pulls the same fields into one sheet, then flags the rows that failed.

Paraphrase set:

> Build reports faster.
>
> Create reports in less time.
>
> Speed up every report.

Angle set:

> The 47-minute export failure, told as an operator story.
>
> A side-by-side count of the old and new steps.
>
> The security reviewer's objection, answered with the actual data flow.
