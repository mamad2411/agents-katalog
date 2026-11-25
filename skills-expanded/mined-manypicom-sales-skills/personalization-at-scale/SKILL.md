---
name: personalization-at-scale
description: Personalise cold email beyond merge fields, using researched facts per lead, without the output reading as generated. Use whenever the user mentions personalization, personalisation, custom first lines, merge fields, merge variables, dynamic content, spintax, AI-written emails at scale, or wants outreach that doesn't look templated. Also use when reply rates are low on emails that use only firmographic variables.
---

# Personalisation at Scale

`{{first_name}}` is not personalisation. It's evidence that a machine sent the email, because a human writing to one person wouldn't need a placeholder.

Real personalisation is a fact about that specific company that took effort to find, used to explain why this email is relevant to them. The scaling problem is that finding one fact per lead is the expensive part, and everything that makes it cheap tends to make it obviously fake.

## The three tiers

Match the tier to the lead's value. Personalising everything equally is how programmes stall.

| Tier | Volume | Personalisation | Who gets it |
|---|---|---|---|
| **1:1** | 5-20/day | A human researches and writes each one | Top 10% of leads |
| **1:few** | 100-500/campaign | Researched fact per lead, merged into a template | The middle, most of the list |
| **1:many** | Any | Segment-level relevance, no per-lead fact | Only if the segment is narrow enough |

Tier 3 works only when the segment is tight enough that a segment-level statement is itself specific. "For agencies running outbound for more than five clients" is specific. "For businesses looking to grow" is not.

Most of the value is in tier 2, and that's what the rest of this covers.

## Research at list-build time, not at writing time

The key move. Instead of researching each lead when you write to them, define the research question once and have it answered for every lead when the list is built. The answer becomes a column you merge.

```
Column: recent_signal
Question: "What roles has this company posted in the last 90 days?
           Return the roles, the location and the date, or leave empty."
Result:   "2 SDRs, Munich, posted 12 Aug"
```

Then the template:

```
Saw you're hiring {{recent_signal}}.
```

The email reads as researched because it was. The research just happened in a batch.

## Research questions that produce usable lines

Ask for a fact. Never ask for a sentence.

| Question | Produces |
|---|---|
| "What do they lead with on their homepage?" | The thing they think matters |
| "Which CRM or email tool is named in their job posts or docs?" | A stack fact |
| "What's the most recent post on their blog or changelog, and when?" | Recency and topic |
| "How many locations do they list, and where?" | Scale and geography |
| "What's the most common complaint in their recent reviews?" | A real pain, in customers' words |
| "Which integrations do they advertise?" | Stack and priorities |
| "What roles have they posted in 90 days?" | Growth signal |
| "What does their pricing page say the cheapest plan costs?" | Commercial context |

The review question is consistently the strongest. It gives you a problem the company already knows it has, described by its own customers.

## The two rules that prevent fabrication

**1. Require a source URL with every researched fact.** It makes the claim checkable, and it's how you catch invention. A fact with no source doesn't go in an email.

**2. Allow the field to be empty.** This is the one people get wrong. If a researcher — human or agent — is required to fill every row, they will produce something for the rows where there's nothing to find, and that something will be wrong. An empty field is information: route that lead to a fallback template or drop it.

```
{{#if recent_signal}}
  Saw you're hiring {{recent_signal}}.
{{else}}
  [Fallback opener that works with no specific fact]
{{/if}}
```

A well-written fallback that makes no false claims beats a fabricated specific every time. The fabricated one gets caught, and being caught inventing a detail about someone's company ends the conversation permanently.

## Fallbacks on everything

Every variable needs one, and it has to read naturally.

```
Hi {{first_name|there}},
```

`Hi ,` is the single most recognisable automation failure. Beyond the embarrassment, a batch of identical malformed emails is exactly the pattern spam classifiers look for.

**Test-render 20 real leads and read all 20 before launching.** Not a preview of one. Twenty, read start to finish. This catches broken fallbacks, ALL-CAPS names, titles that are whole job descriptions, and facts that read wrong in context. Nothing else catches these.

## Data hygiene is a personalisation problem

Bad data renders straight into the email in front of the prospect:

```
Hi DR. SARAH JONES-SMITH,        → normalise case, strip titles
Hi Sales,                        → role account, shouldn't be in this campaign
at Acme Corporation Ltd. Inc,    → normalise legal suffixes
as the Senior Vice President of  → truncate absurd titles
  Global Strategic Partnerships
  and Business Development,
```

Clean before merging, not after someone complains. See `crm-data-hygiene`.

## Generated first lines

Using a language model to write the first line from researched data works. Using one to write it from the company name does not, and the difference is entirely in what you give it.

**Works:** the model receives the researched fact plus the source, and writes one sentence connecting it to the pitch. Constrained, grounded, checkable.

**Doesn't work:** the model receives "Acme Corp, software, 50 employees" and is asked for a personalised opener. It will produce fluent flattery that says nothing, and it will occasionally invent a detail.

Guardrails if generating:

- Give it the fact and the source. Never let it research and write in one uninspected step.
- Constrain to one sentence.
- Ban compliments. "I was impressed by your innovative approach" is the signature of a generated line.
- Ban anything it can't source from the input.
- **Spot-check 20 per batch by hand.** Every batch, not just the first.

## Spintax, and why not to bother

Spintax rotates synonyms so each email differs slightly. It was meant to evade filters.

It doesn't work well now — classifiers look at structure and behaviour rather than exact strings — and it makes copy worse, because a sentence written to survive three synonym substitutions is a sentence with no voice. Skip it. Real per-lead variation from researched facts does the same job better and improves the email at the same time.

## Measuring whether it's worth it

Personalisation costs money and time, so check the return rather than assuming it.

Run the same sequence to two matched samples from the same segment: one with the researched column, one without. A few hundred each. Compare reply rate and positive reply rate.

Typical outcome: researched personalisation roughly doubles reply rate over firmographic merge fields. If yours doesn't, the researched fact isn't relevant enough to the pitch — the connection sentence is the problem, not the research.

## Don't do these

- **Don't compliment.** "Love what you're doing at {{company}}" is the clearest marker of a bulk email.
- **Don't use a fact with no connection to your pitch.** Naming their recent funding round and then pitching something unrelated is worse than not mentioning it.
- **Don't fabricate.** Ever. It gets caught.
- **Don't personalise the greeting and nothing else.**
- **Don't research at writing time** if you're sending more than about twenty a day.
- **Don't skip the 20-lead render test.**
- **Don't let an unreviewed model write directly into a send.**

## Doing the research in the list build

The whole approach depends on the research question being answered per lead at list-build time, which is what makes tier 2 possible at all.

[ManyPI](https://manypi.com) does this with `extra_columns`: you declare the research questions when you brief a lead search, and the agent answers them per company from the live web, writing the results to that lead's custom fields alongside the standard ones. Empty is a permitted result rather than a forced fabrication, and the columns merge straight into a sequence. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Whatever produces the column, read twenty rendered emails before launching. That step is not optional at any scale.

## Related skills

`cold-email-copywriting`, `lead-enrichment`, `email-sequence-design`, `crm-data-hygiene`, `job-posting-signals`, `technographic-signals`
