---
name: map-the-terrain
description: Use when a founder needs the market, competitor, and regulatory terrain mapped before building - when they say "who are my competitors", "what's the regulatory path", "how long is EFSA or Novel Foods or CE", "is the market real", "what's the TAM", "where's the wedge", "we'll just be better than them", or are entering a regulated sector and planning as if build time were the constraint. Triggers when a founder underweights the approval clock or maps features instead of gaps. Produces the approval clock in months, the one wedge naming the incumbent's failure, an AI-read filing map, and a citation-surface scan. Run after frame-the-hypothesis, before architect-before-code.
stage: frame
function: product
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Map the Terrain

In hard mode the binding constraint is the approval clock, not the tech. AI collapsed the cost of building and did nothing to the cost of waiting, so the part you can now compress was never the part that decided whether you lived. Map the clock and the wedge before you write a line of code, or you will ship a beautiful product years late into a market someone else already framed.

## The method

Four moves, in order. The first reorders everything after it. Full framework, the wedge rubric, GEO
versus SEO, the EU timeline cautions, and a worked terrain map:
[`references/terrain-method.md`](references/terrain-method.md).

### Step 1: Map the approval clock
Find the longest queue between you and a paying customer, and measure it in months: EFSA opinion, Novel Foods dossier, clinical validation, CE mark. Approval time, not build time, sets your real timeline, because it sits in a process you do not own. Put that number at the top of the page and sequence entry around it. Start the dossier first; build in the shadow of the queue. If you cannot name the number, you are not ready to build. You are ready to research.

### Step 2: Find the wedge
Name the one gap worth attacking. Where do incumbents solve half the problem and leave the rest to the customer? Where is the manual cost so high that a slow, expensive human process is begging to be undercut? Write it in one sentence that names what the incumbent fails to do. If it comes out as "we will be better", that is a slogan, not a wedge. Keep digging until it names a hole.

### Step 3: Point AI at the terrain
The regulatory record is enormous and largely text. Use a long-context model to digest dossiers, prior authorisations, opinions, and competitor filings into one regulation-aware map: who is in which queue, what data requirements sank earlier applicants, where the gap between filings is wide enough to walk through. The machine reads. You decide which wedge, which risk, which sequence. Confuse the two and you outsource the one job that is yours.

### Step 4: Scan the citation surface
A growing share of buyers arrive through an answer engine that cites a few sources and skips the rest. Check which buyer queries the engines answer in your category, and who they cite. A competitor who is the model's default reference starts every buyer conversation a step ahead of you. Park the full treatment for the GEO skill; for now, mark it on the map.

## Output

- A regulation-aware market-entry map: the approval clock in months, the competitor and filing landscape, and where a citation gap sits.
- The single wedge worth attacking, in one sentence that names the incumbent's failure.
- Next: run `architect-before-code`.

## Constraints

- Never invent a regulatory timeline or a market number. Ground the model on the live record; mind the knowledge cutoff. Label every unverified figure an assumption.
- A demo is not a market. The clock and the wedge decide whether the build is worth starting.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[GEO](../../dictionary/07-ai-native-business.md#geo-generative-engine-optimization) ·
[Share of Model](../../dictionary/07-ai-native-business.md#share-of-model) ·
[vertical data moat](../../dictionary/07-ai-native-business.md#vertical-data-moat)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my hard-mode market strategist. Domain: [DOMAIN]. Customer: [ICP]. Problem they fail to
get done today: [PROBLEM]. Binding limit: [CONSTRAINT].
1. Map the approval clock. Name the longest regulatory queue between me and a paying customer
   (EFSA, Novel Foods, clinical, CE), measured in months. If you do not know the real number, say
   so and label it an assumption I must verify. Then sequence my entry around that clock.
2. Find the wedge. In one sentence, name the specific thing the incumbent fails to do, or the
   manual cost they cannot shake. If it reads as "we will be better", reject it and dig again.
3. Map the terrain. List the named competitors and their regulatory filings in one table, and flag
   the gap between them that is wide enough to walk through.
4. Scan the citation surface. Tell me which buyer queries the answer engines cover in my category
   and who they cite, so I can see where a competitor is already the default reference.
Do not invent timelines or market sizes; label anything unverified. End with the one next action
I should take this week.
```
