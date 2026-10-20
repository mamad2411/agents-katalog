---
name: pm-persona-codifier
description: Codify customer/user personas into canonical, source-attributed persona docs that serve as stable references for downstream product work. Takes raw archetype notes, interview transcripts, JTBD synthesis output, or stated archetype hypotheses; clusters signals into N personas; fills a 9-section template per persona with quote-level source attribution; cross-checks for overlap and contradiction; emits one file per persona plus an INDEX. Triggers on "codify personas", "persona doc", "persona definitions", "who are our customers", "customer archetypes", "user archetypes", "buyer personas", "ICP definition", or when the user has raw persona notes and wants them turned into proper artifacts. Composes downstream of `pm-jtbd-synthesis` (job clusters → persona archetypes); the JTBD output is the strongest possible input but not required.
---

# pm-persona-codifier

Turn raw archetype thinking into canonical persona docs. The output is structured so that every downstream PM doc (PRDs, strategy memos, roadmaps) can reference personas by ID without re-litigating who they are.

**This is codification, not invention.** The skill does not invent personas from thin air. It needs source material: interview transcripts, JTBD synthesis output, user notes, prior product docs, or a clear hypothesis from the user. If the source is thin, the skill says so honestly rather than fabricating detail.

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| **source** | File path, folder, comma-separated list, or `--from-conversation` to use context already in the conversation | *(required)* |
| `--n` | Expected number of personas (the skill will confirm or push back) | auto-detect |
| `--depth` | `quick` (snapshot + jobs + quotes per persona) or `full` (all 9 sections) | `full` |

## Workflow

### Step 1 — Context gather (max 5 questions, all at once)

Before reading sources, confirm with the user (skip questions the user already answered):

1. **Who's the audience?** Internal team / leadership / sales enablement / all three. (Affects what to emphasize.)
2. **How many personas do you expect?** Push back if &gt; 5. More than 5 is almost always under-clustered.
3. **Are these buyers, users, or both?** B2B SaaS usually has both, and they're often different people.
4. **What's already locked in?** Existing persona names, segments, or ICP language we must preserve.
5. **What's NOT a persona?** Out-of-scope archetypes the user wants explicitly excluded (e.g. "investors are an audience, not a customer persona").

If `--from-conversation` is set, infer answers from context; only ask what's missing.

### Step 2 — Ingest and cluster

Read every source with the Read tool (line-numbered output is mandatory for source attribution). Cluster signals into N personas using these clustering axes:

1. **Job clusters they belong to** (from JTBD synthesis, if available)
2. **Buying power and decision role** (decider / influencer / blocker / user)
3. **Context of use** (where they encounter the product, how often, with whom)
4. **What "good" looks like for them** (their definition of success — usually different per persona)
5. **What they're afraid of** (the anxiety force, persona-specific)

Personas that share 3+ axes should be merged. Personas with only 1 shared axis are probably distinct.

### Step 3 — Fill the 9-section template per persona

See `references/persona-template.md` for the canonical schema and section-by-section guidance. For a bare fill-in scaffold to copy into each persona file, use `assets/persona-template.md`. Each persona file uses the exact same structure so downstream skills can grep specific sections (e.g. "what are the jobs across personas?").

Sections:
1. Snapshot (3 sentences max)
2. Jobs to be done (top 3, prioritized)
3. What they actually want (vs. what they say they want)
4. What "good" looks like for them
5. Decision-making power and process
6. Quotes (3–5, with source attribution)
7. Implications for product (3 bullets)
8. Anti-persona (what they are NOT)
9. Open questions

Rule for every section: anchor to source. If a claim has no source, mark it `[inferred]` or remove it. Empty sections are honest; fabricated sections are not.

### Step 4 — Cross-check

After all personas are drafted, run these checks:

1. **Overlap check:** Do any two personas describe the same actual human? If yes, merge or sharpen the differentiator.
2. **Contradiction check:** Do any two personas claim the same characteristic with opposite values? If yes, that's likely a real tension worth flagging in the INDEX.
3. **Completeness check:** Does every persona have at least 2 quote anchors? If not, the persona is under-evidenced — flag in Open Questions.
4. **Anti-persona check:** Are the anti-personas distinct enough that the persona feels bounded? Vague anti-personas are a sign the persona itself is vague.

### Step 5 — Emit artifacts

Write to `./INBOX/personas/` if an `INBOX/` exists, else `./personas/` in the current directory (or ask the user where):

- **`persona-<slug>.md`** — one per persona (use kebab-case slugs, e.g. `persona-flow-builder.md`)
- **`INDEX.md`** — table of personas with the snapshot row from each, plus a "tensions and notes" section flagging cross-persona contradictions

Create the `personas/` subdirectory if it doesn't exist.

## YAML Frontmatter (required on every persona file)

```yaml
---
id: persona-flow-builder
name: The Flow Builder
status: draft | reviewed | locked
sources:
  - customer-calls/acme-x-bigco.txt
  - my-calls/intro-1on1-contact.txt
related_personas: [persona-buying-customer]   # personas this one frequently interacts with
last_updated: YYYY-MM-DD
---
```

`status: draft` until the user reviews. `status: locked` means downstream skills can reference it without re-checking.

## Rules

1. **Source attribution is mandatory.** Every quote, every job, every characteristic claim points back to a source line. If you can't, mark `[inferred]` and explain why the inference is reasonable.

2. **Personas are durable, archetypes-of-jobs — not demographics.** Avoid age, location, job title as primary frame. "Senior PM at a 100-person B2B SaaS" is fine *as detail*. "The Plate-Spinner — keeps 4 incompatible workflows alive at once" is the actual persona.

3. **Names are roles, not vibes.** Persona names should describe a role or behavior pattern in 2–4 words. Bad: "Sarah." "The Visionary." "The Power User." Good: "The Flow Builder." "The Trust-First Buyer." "The Embedded Operator." Names anchored on observable behavior survive re-reads.

4. **Anti-persona section is mandatory and non-trivial.** "Not a startup founder" is not an anti-persona. "Looks like our persona but actually buys for compliance reasons rather than productivity" is an anti-persona. The anti-persona is where personas earn their keep — it's the test of whether you'd correctly disqualify a lookalike.

5. **Cap at 5 personas.** If the user insists on more, push back. Each persona past 5 dilutes the team's mental model and usually represents under-clustering.

6. **Distinguish buyer vs user.** In B2B these are often different. If they're different, they're different personas — don't merge them. The buyer's "good" looks completely different from the user's "good."

7. **No outside knowledge.** Same rule as `extract-insights`. If the customer didn't mention a company, vendor, or framework, don't add it.

8. **The "what they actually want" section is the highest-leverage one.** Customers usually ask for the thing one level removed from what they actually want. ("I want a builder UI" → actual want: control / trust / proof.) Force yourself to do that translation, with source evidence.

9. **Output goes to the `personas/` directory** (under `./INBOX/` if it exists, else the current directory). In a curated workspace, write only to `INBOX/` and let the user promote.

10. **If you can't reach 3 quotes for a persona, flag it.** A persona with 1 quote is a hypothesis, not a persona. Say so in Open Questions and the INDEX.

## Composing With Other Skills

- **Upstream**: `pm-jtbd-synthesis` is the canonical input. If JTBD output exists, read both the synthesis report and the OST stub before clustering — job clusters often map 1:1 to personas, or they map N-to-1 (multiple jobs per persona), but rarely 1-to-N.
- **Sideways**: `interviewer` (requires the **multiplai-research** plugin) for when context-gather requires deeper user probing.
- **Downstream**: Document-producing PM skills reference personas by ID — `pm-strategy-memo` (audience and ICP language) and `pm-pr-faq` (the fictional customer in the PR is a persona). (A PRD skill with a target-persona section is planned but not yet shipped.)
