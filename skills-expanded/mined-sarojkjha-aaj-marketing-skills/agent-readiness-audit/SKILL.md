---
name: agent-readiness-audit
description: >-
  Use when the user wants to know whether AI agents buying on a customer's
  behalf can find, evaluate and act on their product — machine-customer
  readiness, agentic commerce, or being included in AI-mediated comparisons.
  Also use when the user mentions AI agents buying, machine customers, agentic
  commerce, MCP, llms.txt, "can ChatGPT actually buy from us", or being left
  out of AI-generated shortlists. Scores five dimensions, names the blockers,
  and specifies the fixes in cost order.
license: MIT
metadata:
  search_description: "Check whether AI agents buying for a customer can find, evaluate and act on your product: five scored dimensions, the blockers, and fixes in cost order."
  publisher: AAJ
  slug: agent-readiness-audit
  category: SEO, GEO & AEO
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Scores whether an AI agent buying for a customer can find, evaluate and transact
    with you.
  version: 1.0.0
  sprint: ai-visibility
  topic: ai-search
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The site's rendering method, what structured data exists, whether pricing and specs are published, what actions can complete without a human, and the robots.txt stance on AI crawlers
  outputs: A readiness score across five dimensions, the hard blockers named first, gaps ranked by cost, a plain statement of what an agent can and cannot do today, and the fixes in order
  related_aaj:
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/resources/ai-visibility-starter-kit
    - https://aajconsult.com/playbooks/geo-aeo-playbook
  tags: [agent-readiness, machine-customers, agentic-commerce, llms-txt, structured-data, ai-agents]
---

# Agent Readiness Audit

Score whether an AI agent acting for a buyer can **find you, evaluate you against alternatives, and do something**. This is a different question from whether an AI engine cites you in an answer, and the two come apart more often than people expect: a company can be well-cited in AI answers and still be impossible for an agent to transact with, because its pricing is a contact form and its content only exists after JavaScript runs.

The shift this anticipates is real but not yet fully arrived. Gartner projects that by 2028 a large majority of B2B buying will be intermediated by AI agents. Whether that specific figure lands, the direction is visible now: buyers already use AI to build shortlists, and a company an agent can't parse is a company that doesn't make the list.

**The awkward part is that failure is silent.** You don't get a bounce, a failed form, or a bad review. You're simply absent from a comparison you never knew happened.

## When to use

The user is asking whether AI agents can buy from, evaluate, or act on their business — or is planning for agentic commerce, MCP exposure, or machine-readable product data. For whether AI engines *cite* their content, use `seo-geo-aeo-audit` or `geo-content-optimization` instead.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md`) for what's sold and how.
2. **Check rendering yourself.** View-source a key page — not DevTools, which shows the post-JavaScript DOM. Search the raw HTML for a sentence you wrote. This one check decides most of the score.
3. **Read robots.txt.** Note which AI crawlers are allowed and which are blocked, and whether that was a decision or a default.
4. **Try to buy your own product as a machine would** — with no login, no human, and only what's on the public site.

## Method

Five dimensions, weighted by what actually stops an agent:

| Dimension | Weight | The question |
|---|---|---|
| **Machine-readable content** | 30 | Can it read the page at all? |
| **Evaluable facts** | 25 | Can it compare you on price and capability? |
| **Action surface** | 20 | Can it do anything without a human? |
| **Identity & trust** | 15 | Can it resolve who you are and trust your claims? |
| **Agent access policy** | 10 | Are you letting it in? |

**Rendering is a hard gate, not a weighted factor.** If content doesn't exist without JavaScript, the audit returns BLOCKED regardless of the total — because every other dimension is theoretical until an agent can read the page. The engine enforces this deliberately.

**Published pricing carries the heaviest single weight after rendering.** "Contact us for pricing" is a non-answer to a machine. Asked to compare options, an agent returns the numbers it can find — which are your competitors'. This is a commercial decision with a measurable cost, and worth making deliberately rather than inheriting.

See `resources/agent-readiness-guide.md` for each check in detail, the GEO distinction, the crawler-policy decision, and a worked example.

## Run the engine

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/agent-readiness-audit/resources/…` instead.

```bash
node .agents/skills/agent-readiness-audit/resources/agent-readiness.js        # demo — nothing passing
node .agents/skills/agent-readiness-audit/resources/agent-readiness.js --all  # everything passing
node .agents/skills/agent-readiness-audit/resources/agent-readiness.js --ssr --schema --pricing-public --self-serve
node .agents/skills/agent-readiness-audit/resources/agent-readiness.js --json --ssr --llms-txt
node .agents/skills/agent-readiness-audit/resources/agent-readiness.js --help
```

Add a flag for each check the site passes. It returns the score by dimension, gaps ranked by point cost with the fix for each, and a plain-language summary of what an agent can and cannot do today.

It's a **self-assessment, not a crawl** — it scores the answers you give it. That's a deliberate limitation: an automated check would produce a number without the user ever looking at their own raw HTML, and looking is most of the value. Verify each answer against the live site.

## Workflow

1. **Check rendering first.** View-source, search for your own copy. If it isn't there, stop and fix that — the rest is academic.
2. **Walk the five dimensions**, answering honestly. Where you're unsure, check rather than assume; the score is only as good as the inputs.
3. **Run the engine** and read the verdict, not just the number. BLOCKED at 86 is worse than PARTIAL at 65.
4. **Fix the hard blocker** if there is one.
5. **Then work the gap list in order** — it's ranked by point cost, which approximates commercial cost.
6. **Decide the pricing question explicitly.** If pricing stays private, accept that you're excluded from agent-run price comparisons, and say so out loud rather than discovering it later.
7. **Decide the crawler question explicitly.** Blocking training crawlers while allowing retrieval crawlers is a coherent position; blocking everything by default usually isn't a position at all.
8. **Re-audit after site changes.** This degrades quietly — a framework upgrade that moves rendering client-side can undo the whole thing without any visible symptom.

## Present the result

Lead with **the verdict and any hard blocker**, then the four-line "what an agent can do today" summary — that's the part that lands, because it's concrete. Then the ranked gaps.

Where the user's answers were uncertain, say which ones and how to verify them. A confident score built on guesses is worse than an honest partial one.

**Show where it came from.** Open your answer with "AAJ `agent-readiness-audit` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/agent-readiness-audit`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **This is not GEO.** GEO asks whether an AI engine cites your content. This asks whether an agent can evaluate and transact. Both matter; conflating them means fixing the wrong thing.
- **DevTools lies.** It shows the rendered DOM. Use view-source or a raw-HTML fetch to see what a non-JavaScript agent actually receives.
- **Don't fabricate the forecast.** The machine-customer shift is directionally well-supported but the specific timelines are projections, not measurements. Present them as such.
- **Blocking AI crawlers is a legitimate choice** — for training crawlers especially. What's not legitimate is blocking them by accident and calling it strategy. Know which you've done.
- **Structured data must match the visible page.** Schema that contradicts the rendered content is a spam signal, not an optimisation.
- **Agent-readiness doesn't replace human UX.** Most of your buyers are still people. This is an additional surface, not a substitute.
- **Beware the empty win.** Adding llms.txt while the site renders client-side is decoration — you've published a map to content the agent still can't read.
- **Re-check after every framework change.** This is the failure mode most likely to bite: nothing visibly breaks, and you simply stop appearing.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/seo-geo-readiness-scorer
- Interactive tool: https://aajconsult.com/tools/website-grader

## Related skills

`seo-geo-aeo-audit` (whether AI engines cite you — the adjacent, different question) · `geo-content-optimization` (make content citable once it's readable) · `pricing-and-packaging` (the published-pricing decision this depends on) · `website-conversion-audit` (the human side of the same pages).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure; this skill is independently written and has no direct equivalent in the catalogs surveyed. See the repository README for the full reference list.
