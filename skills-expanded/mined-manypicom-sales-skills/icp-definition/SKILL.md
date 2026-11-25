---
name: icp-definition
description: Define an ideal customer profile precise enough to build a lead list from, including buying triggers and disqualifiers. Use whenever the user mentions ICP, ideal customer profile, target market, buyer persona, target accounts, account list, who to sell to, market segmentation, or says their outbound isn't working and they aren't sure who to target. Also use before any lead sourcing or cold email work, because a list built from a vague ICP wastes every downstream step.
---

# ICP Definition

Most outbound fails before a single email is sent, because the list was built from a description too vague to filter on. "B2B SaaS companies" is not an ICP. It's a category.

A usable ICP is one a stranger could take, go to the web, and come back with the same 200 companies you would have picked. If two people working from your ICP would build different lists, it isn't finished.

## Start from customers, not from ambition

The ICP is a description of who already buys and gets value, not who you'd like to sell to. Derive it from evidence:

- **Your best 10 to 20 customers.** Best by retention and expansion, not by contract size. A large customer who churned at month four is not a template.
- **Your fastest closes.** Short cycles mean the value was obvious, which means the fit was real.
- **Your worst churn.** The pattern in who leaves is usually clearer than the pattern in who stays, and it becomes the disqualifier list.
- **Deals you lost on fit** rather than on price or timing.

If there are no customers yet, the ICP is a hypothesis. Say so, write it as one, and design the first campaign to test it rather than to scale it.

## The five layers

Each layer has to be observable from outside the company. If you can't determine it from a website, a profile or a public source, it can't go in the filter — it's a qualification question for the call.

**1. Firmographics.** Industry, employee count, revenue or funding stage, geography, business model. The floor, not the definition. Everyone has these and they discriminate weakly.

**2. The situation that creates the need.** This is the layer that actually matters and the one usually missing. Not what the company is, but what's true about it right now that makes your product relevant. "Runs outbound sales with more than two SDRs", "ships physical product to more than three countries", "has a self-serve signup and a sales team".

**3. Triggers.** Events that make the need urgent this quarter rather than someday. Covered below.

**4. The person.** Titles vary wildly across companies of different sizes, so define the role by what they own rather than by what they're called. "Whoever owns pipeline generation" resolves to VP Sales at 200 people and to the founder at 15.

**5. Disqualifiers.** Explicit, hard excludes. This is the highest-leverage part of an ICP and the most often skipped.

## Triggers

A trigger turns a fit into a reason to reply now. The strongest ones are observable and recent:

| Trigger | Signals | Why it works |
|---|---|---|
| Hiring for the role | Job posts for SDRs, RevOps, growth | They're building the function you serve |
| Funding round | Announcement, filings | Budget just appeared and there's pressure to spend it |
| New executive in the role | Title changes | New leaders replace tooling in their first 90 days |
| Tech stack change | Adding or removing a tool | Active evaluation is happening |
| Expansion | New market, new office, new product line | New problems at a known scale |
| Public pain | Reviews, forum posts, support complaints about an incumbent | Stated dissatisfaction |
| Growth in headcount | Steady hiring across functions | Scaling breaks whatever they built at half the size |

Each of these has its own sourcing skill. See `job-posting-signals`, `funding-news-signals` and `technographic-signals`.

## Disqualifiers

Write these as explicitly as the includes. A lead sourcing agent or a researcher needs to know what to throw away, and vague ICPs produce lists padded with agencies, consultancies, competitors and companies a tenth of the right size.

Typical hard excludes:

- Agencies and consultancies, when you sell to end operators
- Companies below the size where the problem exists
- Companies above the size where they'd build it internally
- Competitors and their resellers
- Existing customers and open opportunities
- Regions you can't service, bill or legally contact
- Industries you can't serve for compliance reasons

## Write it so it can be executed

The output should be usable as a brief for a researcher or an agent, not as a slide.

```markdown
# ICP: [name of the segment]

## In one paragraph
[Companies that ___, where ___ is true, currently ___. We reach the
person who owns ___.]

## Firmographics
- Size:        [range, and what it's a proxy for]
- Geography:   [countries or regions, and why]
- Industry:    [verticals, or "any, provided the situation below is true"]
- Stage:       [funding, revenue or maturity]

## The situation
- [Observable fact 1 — how to verify it from outside]
- [Observable fact 2]
- [Observable fact 3]

## Triggers (nice to have, not required)
- [Event] — found via [source]

## The person
- Owns:       [the outcome, not the title]
- Titles:     [the actual title variants across company sizes]
- Not:        [titles that look right and aren't]

## Disqualify if
- [Hard exclude 1]
- [Hard exclude 2]

## Evidence
- Based on: [which customers, what pattern]
- Confidence: [tested / hypothesis]
```

The "how to verify it from outside" annotations are what make this list buildable. Without them you have preferences rather than filters.

## Segment rather than broaden

When outbound underperforms, the instinct is to widen the ICP to get more volume. It's almost always the wrong move — a wider list means a vaguer message, and a vague message to more people performs worse than a specific message to fewer.

The right move is to split into narrower segments, each with its own message. Three segments of 300 companies with three different first lines beat one list of 900 with a generic one, and you learn three times as much.

Test one segment at a time. A campaign to a mixed list tells you nothing about which part of the list worked.

## Sanity checks before building the list

- **Is the market big enough?** Count the addressable companies. If the segment has 40 companies in it, outbound is the wrong channel and a named-account approach is the right one.
- **Can you name 20 example companies right now?** If not, the ICP is still abstract.
- **Would your best customer match this ICP?** Run it backwards. It's surprising how often the profile excludes the people already paying.
- **Is the pain expensive enough to act on?** A real problem people live with is not a buying trigger.
- **Can you reach the person?** An ICP built around a role that doesn't publish contact details is a channel problem, not a targeting one.

## Don't do these

- **Don't write an ICP from aspiration.** Enterprise logos in the profile when every customer is a 30-person company produces a list nobody can sell to.
- **Don't confuse a persona with an ICP.** The persona is the human. The ICP is the company plus the situation. You need both and they're not the same document.
- **Don't use "any industry" as a shortcut.** If the industry genuinely doesn't matter, say which situation replaces it as the filter.
- **Don't set it once.** Revisit after every 500 emails sent. The reply data tells you which part of the profile was wrong.
- **Don't build the list before finishing this.** Every downstream cost — research, verification, sending, reputation — is spent on whatever this document says.

## Turning it into a list

The ICP is the input to lead sourcing. Written as above, the paragraph and the disqualifier list drop almost directly into a research brief. See `lead-sourcing`.

[ManyPI](https://manypi.com) takes this shape directly: a free-text ICP description plus structured criteria (`locations`, `industries`, `company_size`, `titles`, `keywords`, `exclusions`, `required_fields`), and its agent researches the live web against it rather than filtering a static database — which matters when the defining trait is a situation rather than a firmographic. It runs over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Whatever builds the list, the quality ceiling is set by this document.

## Related skills

`lead-sourcing`, `lead-scoring-qualification`, `cold-email-copywriting`, `job-posting-signals`, `funding-news-signals`, `technographic-signals`
