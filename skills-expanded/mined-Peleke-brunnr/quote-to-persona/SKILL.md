---
name: quote-to-persona
description: >
  Quote-to-persona bridge — takes wild-scan JSON output (scored pain quotes) and
  clusters them by behavioral archetype, then synthesizes persona-extract-compatible
  personas with evidence-mapped fields. Bridges the gap between wild-scan harvesting
  and offer-scope consumption. Use when you have harvested quotes and need structured
  buyer personas grounded in real evidence.
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F52C"
---

# Quote to Persona

Transform wild-scan quote harvests into evidence-based buyer personas. Clusters quotes by behavioral archetype (not pain category), synthesizes persona fields compatible with offer-scope input, and maps every synthesized claim back to source quotes. Produces structured JSON and human-readable markdown.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
wild-scan ──→ **quote-to-persona** ──→ offer-scope
                                   └──→ persona-extract (enrichment, optional)
```

This skill consumes wild-scan JSON output and produces persona data formatted for direct consumption by offer-scope. It can optionally feed into persona-extract for deeper enrichment (web search, success stories, Four Forces analysis), but its primary output is self-contained and offer-scope-ready.

### Relationship to persona-extract

- **persona-extract** runs the full Signal-to-Story Pipeline: web search, success stories, Four Forces, decision point mapping. It requires upstream decision-log output and performs live evidence collection.
- **quote-to-persona** works entirely from harvested quotes — no web search, no decision-log dependency. It is faster, lighter, and sufficient when you already have 15+ scored quotes from wild-scan.
- If you want to go deeper after quote-to-persona, run persona-extract on its output to add success stories, Four Forces, and additional web evidence.

## When to Use

- You have a wild-scan JSON file with 15+ scored quotes and need buyer personas
- You want to bridge wild-scan output into offer-scope input without running the full persona-extract pipeline
- You want to cluster harvested quotes by behavioral archetype to understand WHO is in pain (not just WHAT the pain is)
- You need evidence-mapped personas where every claim traces back to a specific quote

## Trigger Phrases

- "Cluster quotes into personas"
- "Quote to persona from [wild-scan file]"
- "Build personas from these quotes"
- "Who is in pain? Cluster the wild-scan data."
- "/quote-to-persona [wild-scan JSON path]"

---

## Prerequisites

Before starting, the following must be available:

1. **Wild-scan JSON file** — A completed wild-scan output file conforming to `wild-scan/references/output-schema.json`. Must contain at least 15 scored quotes with: quote text, author, platform, community, URL, engagement, context, pain_category, scores, and overall_score.
2. **Domain** — The domain being explored (e.g., "DevOps education"). Usually available from the wild-scan's `scan_metadata.topic`.
3. **Opportunity title** — The opportunity being targeted (e.g., "DevOps Learning Path"). If not provided, derive from the topic.

If the wild-scan file is missing or has fewer than 15 quotes, prompt the user to run wild-scan first.

---

## Input

The skill expects:

```typescript
interface QuoteToPersonaInput {
  wild_scan_path: string           // path to wild-scan JSON file
  domain: string                   // e.g., "DevOps education"
  opportunity_title: string        // e.g., "DevOps Learning Path"
  wild_scan_ref?: string           // optional: slug of the wild-scan file for cross-refs
  min_quotes_per_cluster?: number  // optional: default 3
  max_clusters?: number            // optional: default 5
}
```

---

## Workflow

```
Wild-Scan JSON + Domain + Opportunity Title
    |
Phase 1: Load & Validate (read JSON, check schema, summarize)
    |
Phase 2: Cluster (group quotes by behavioral archetype)
    |
Phase 3: Synthesize Personas (build offer-scope-compatible persona per cluster)
    |
Phase 4: Evidence Mapping (link every field back to source quotes)
    |
Phase 5: Export (markdown + JSON to vault)
    |
Output: Markdown persona doc + JSON for offer-scope → vault
```

---

## Phase 1: Load & Validate

Read the wild-scan JSON file and validate:

### Validation Checks

1. **Schema compliance**: File must have `scan_metadata`, `quotes` array, `themes` array (may be empty)
2. **Minimum quotes**: At least 15 quotes present. If fewer, STOP and tell the user to run wild-scan again or combine multiple scan files.
3. **Required fields per quote**: Each quote must have: `quote`, `author`, `platform`, `community`, `url`, `engagement`, `pain_category`, `scores`, `overall_score`
4. **Score range**: All `overall_score` values must be between 1 and 10

### Summary Output

After validation, produce a brief summary for the user:

```
Loaded: [filename]
Topic: [scan_metadata.topic]
Quotes: [count]
Score range: [min] - [max]
Pain categories: [list with counts]
Platforms: [list]
```

Proceed immediately to Phase 2 — do not wait for user confirmation.

---

## Phase 2: Cluster

Group quotes by **behavioral archetype**, NOT by pain_category. Pain categories (tutorial-gap, debugging-hell, etc.) describe WHAT hurts. Archetypes describe WHO is hurting and HOW they relate to the problem.

### Clustering Dimensions

Analyze each quote across four behavioral dimensions:

| Dimension | What to Look For | Examples |
|-----------|-----------------|----------|
| **Journey Stage** | Where are they in their learning/career arc? | Just starting, mid-transition, years in and stuck, burning out |
| **Frustration Type** | HOW do they express their pain? | Desperate plea, bitter humor, resigned acceptance, angry critique |
| **Attempted Solutions** | What have they already tried? | Tutorials, courses, certs, homelabs, job-hopping, nothing |
| **Career Context** | What is their professional situation? | Student, junior, mid-level transitioning, senior frustrated with juniors, solo practitioner, team lead |

### Clustering Process

1. **Read all quotes carefully.** For each quote, note the four dimensions above. Pay attention to the VOICE — not just what they say but how they say it.

2. **Identify natural groupings.** Look for quotes that share 2+ dimensions. These are your candidate clusters.

3. **Name each cluster.** The archetype name should encode the behavioral pattern, not the pain category. Format: "The [Adjective] [Role/Identity]" — e.g., "The Eternal Student", "The Copy-Paste Operator", "The Burned-Out Firefighter", "The Rebranded Sysadmin".

4. **Validate cluster distinctness.** Each cluster must be behaviorally distinct from every other cluster. If two clusters share the same journey stage, frustration type, AND attempted solutions, merge them.

5. **Enforce minimum size.** Each cluster must contain at least 3 quotes. If a cluster has fewer, either:
   - Merge it into the nearest cluster
   - If the quotes are true outliers, group them under "Unclustered" (max 2 quotes here)

### Clustering Rules

- **Dynamic discovery**: Do NOT hardcode archetypes. Let the data speak. The DevOps data might yield "The Eternal Student" or it might yield something you did not expect. Name what you see, not what you assume.
- **Behavioral, not demographic**: "Mid-level engineer" is a demographic. "The person who knows every tool name but can't explain why they'd pick one over another" is a behavioral archetype. Cluster on behavior.
- **Same person can appear in multiple quotes**: If the same author has quotes in different clusters, that is fine — people have multiple dimensions. But if one author dominates a cluster, note it.
- **High-scoring quotes anchor clusters**: When assigning quotes to clusters, let the highest-scoring quotes (overall_score >= 7) define the cluster centers. Lower-scoring quotes fill in around them.
- **3-5 clusters is the target range**: Fewer than 3 means the data is too homogeneous (unlikely with 15+ quotes). More than 5 means you are over-splitting.

### Cluster Output Format

For each cluster, produce:

```
Cluster: [Archetype Name]
Description: [1-2 sentences describing the behavioral pattern]
Quote count: [N]
Avg score: [weighted average of member quotes]
Key dimensions:
  - Journey stage: [description]
  - Frustration type: [description]
  - Attempted solutions: [description]
  - Career context: [description]
Member quotes: [list of quote indices from the wild-scan JSON]
Anchor quotes: [2-3 highest-scoring quotes that define this cluster]
```

See [references/clustering-guide.md](references/clustering-guide.md) for detailed dimension analysis and example patterns.

---

## Phase 3: Synthesize Personas

For each cluster, synthesize a persona that conforms to the offer-scope input format. Every field must be grounded in quote evidence — no fabrication.

### Per Persona, Produce:

#### 1. persona_name
A descriptive name encoding the archetype. Use the cluster name.

#### 2. pain_stories[]

**Minimum 3 per persona.** Each pain story maps directly from one or more quotes:

| Field | Source | Rule |
|-------|--------|------|
| `situation` | Inferred from quote `context` and `pain_category` | Must describe a real scenario, not an abstract state |
| `pain` | Extracted from `quote` text — use their words | Direct extraction, not paraphrase |
| `current_workaround` | Inferred from quote — what are they doing instead? | Look for "I've been doing X", "I just Y", "The only way is Z" |
| `emotional_state` | Extracted from `quote` emotional language + `scores.intensity` | Use their emotional vocabulary: "frustrated", "depressed", "angry", "resigned" |
| `evidence` | The full quote with attribution | Format: `"[quote text]" — [author] on [community] ([engagement.value] [engagement.metric])` |

#### 3. decision_triggers[]

Infer from the quotes: what EVENT would push this persona to search for and buy a solution?

| Field | Source |
|-------|--------|
| `trigger` | The specific event that starts the search (e.g., "Failed a production deploy", "Got passed over for promotion", "Started a new job with DevOps responsibilities") |
| `urgency` | `high` / `medium` / `low` — based on the quote's emotional intensity and career stakes |
| `channel` | Where the persona would search when triggered (based on the `platform` and `community` fields of member quotes) |

**Minimum 2 per persona.**

#### 4. objections[]

Infer from quote evidence: what would make this persona hesitate to buy?

| Field | Source |
|-------|--------|
| `objection` | Derived from the persona's expressed skepticism, past failures, or stated needs |
| `counter` | Evidence-based response, not a dismissal. Use quotes from peers who found solutions. |

**Minimum 2 per persona.**

#### 5. willingness_to_pay

| Field | Source |
|-------|--------|
| `range` | Estimate based on career context, current spend evidence from quotes, and comparable products mentioned |
| `evidence` | Quote or inference supporting the estimate. Be specific about what they mention spending on (courses, certs, homelabs) |
| `anchor_products` | Products mentioned or implied in quotes (Udemy, A Cloud Guru, KodeKloud, etc.) |

#### 6. channels[]

| Field | Source |
|-------|--------|
| `platform` | The `platform` and `community` fields from member quotes |
| `behavior` | How the persona behaves on that platform — posting questions, lurking, replying with advice, venting |

**Minimum 2 per persona.**

### Synthesis Rules

- **No hallucination.** Every field value must trace to at least one quote. If you cannot ground a field in evidence, leave it with a note: `"[inferred — no direct evidence]"`.
- **Use their language.** Pain descriptions, emotional states, and situation descriptions should use vocabulary from the actual quotes, not marketing language.
- **Prioritize high-scoring quotes.** When multiple quotes could inform a field, prefer the one with the highest overall_score.
- **Cross-reference within clusters.** If two quotes in the same cluster describe the same pain from different angles, combine them into one richer pain_story with both as evidence.

---

## Phase 4: Evidence Mapping

Create an explicit evidence map linking every synthesized persona field back to its source quote(s). This prevents fabrication and enables downstream skills to verify claims.

### Evidence Map Format

For each persona, produce:

```json
{
  "persona_name": "The Eternal Student",
  "evidence_map": {
    "pain_stories": [
      {
        "story_index": 0,
        "source_quotes": [0, 3, 10],
        "fields_grounded": {
          "situation": { "quote_index": 0, "excerpt": "..." },
          "pain": { "quote_index": 0, "excerpt": "..." },
          "current_workaround": { "quote_index": 3, "excerpt": "..." },
          "emotional_state": { "quote_index": 0, "excerpt": "..." }
        }
      }
    ],
    "decision_triggers": [
      {
        "trigger_index": 0,
        "source_quotes": [0, 3],
        "inference_basis": "Both quotes describe multi-year course consumption with no progress, suggesting the trigger is hitting a wall after yet another completed course."
      }
    ],
    "objections": [
      {
        "objection_index": 0,
        "source_quotes": [3],
        "inference_basis": "Quote explicitly rejects 'another random list of videos/courses'. The objection is that this looks like more of the same."
      }
    ],
    "willingness_to_pay": {
      "source_quotes": [0, 15],
      "inference_basis": "Quote mentions Udemy courses (typically $10-30), years of investment. Already spending on education, anchored to low price points."
    },
    "channels": [
      {
        "channel_index": 0,
        "source_quotes": [0, 3, 10],
        "inference_basis": "All quotes from r/devops. Posted and engaged there. This is their home community."
      }
    ]
  }
}
```

### Evidence Mapping Rules

- Every pain_story must map to at least 1 source quote
- Every decision_trigger must have an inference_basis explaining why this event was inferred
- If a field has no direct evidence, the inference_basis must say so explicitly: `"No direct evidence — inferred from [reasoning]"`
- Quote indices must match the indices in the source wild-scan JSON file (0-indexed into the `quotes` array)
- The evidence map is included in both the JSON and markdown outputs

---

## Phase 5: Export

Produce two output files saved to the Obsidian vault.

### Vault Output Path

```
{vault}/Admin/Product-Discovery/Personas/
```

Where `{vault}` = `${VAULT}`

### 1. Markdown: `{vault}/Admin/Product-Discovery/Personas/{topic-slug}-personas-{YYYY-MM-DD}.md`

Human-readable persona document.

```markdown
---
type: persona
date: YYYY-MM-DD
status: complete
source_skill: quote-to-persona
tags:
  - hunter/persona
  - hunter/domain/{domain-slug}
  - hunter/opportunity/{opportunity-slug}
wild_scan_ref: "{wild-scan-slug}"
---

# Quote-to-Persona: [Opportunity Title]

**Date**: [date]
**Domain**: [domain]
**Opportunity**: [opportunity title]
**Source**: [[Writing/From-The-Wild/{wild-scan-filename}]]
**Quotes analyzed**: [count]
**Personas synthesized**: [count]

## Persona Summary

| Persona | Archetype | Cluster Size | Avg Score | Top Pain | WTP Range |
|---------|-----------|--------------|-----------|----------|-----------|
| [name] | [description] | [N quotes] | [score] | [pain] | [range] |
| ... | ... | ... | ... | ... | ... |

## Personas

### 1. [Persona Name]

**Description**: [1-2 sentence behavioral description]
**Cluster size**: [N quotes] | **Avg score**: [X.X]
**Journey stage**: [stage] | **Frustration type**: [type]

#### Pain Stories

**Story 1**: [situation]
- **Pain**: [pain — in their words]
- **Workaround**: [current workaround]
- **Emotional State**: [emotional state]
- **Evidence**: "[full quote]" — [author], [community] ([engagement])

**Story 2**: [situation]
...

#### Decision Triggers

| Trigger | Urgency | Channel |
|---------|---------|---------|
| [trigger] | [urgency] | [channel] |
| ... | ... | ... |

#### Objections

| Objection | Counter | Evidence |
|-----------|---------|----------|
| [objection] | [counter] | [source quote reference] |
| ... | ... | ... |

#### Willingness to Pay

**Range**: [range]
**Evidence**: [evidence]
**Anchor Products**: [list]

#### Channels

| Platform | Community | Behavior |
|----------|-----------|----------|
| [platform] | [community] | [behavior] |
| ... | ... | ... |

#### Evidence Map

| Field | Source Quotes | Basis |
|-------|--------------|-------|
| Pain Story 1 | Quote #[N], #[N] | [brief basis] |
| Pain Story 2 | Quote #[N] | [brief basis] |
| Trigger 1 | Quote #[N], #[N] | [brief basis] |
| ... | ... | ... |

### 2. [Next Persona...]

[Repeat structure for each persona]

## Clustering Diagnostics

### Dimension Distribution

| Dimension | Values Found |
|-----------|-------------|
| Journey Stage | [list with counts] |
| Frustration Type | [list with counts] |
| Attempted Solutions | [list with counts] |
| Career Context | [list with counts] |

### Unclustered Quotes

[List any quotes that did not fit cleanly into a cluster, with explanation]

## Next Steps

- **For offer-scope**: Load the companion JSON file as persona input. Top persona for first offer: [name]
- **For persona-extract**: Run persona-extract on this output to add success stories, Four Forces analysis, and additional web evidence
- **For content-planner**: Cross-reference with wild-scan content briefs for persona-targeted content

## References

- **Wild Scan**: [[Writing/From-The-Wild/{wild-scan-slug}]]
```

### 2. JSON: `{vault}/Admin/Product-Discovery/Personas/{topic-slug}-personas-{YYYY-MM-DD}.json`

Structured data directly consumable by offer-scope. Must conform to PipelineEnvelope schema:

```json
{
  "skill": "quote-to-persona",
  "version": "1.0",
  "session_id": "session-YYYY-MM-DD-NNN",
  "timestamp": "ISO 8601",
  "input_refs": ["wild-scan-slug"],
  "output": {
    "domain": "string",
    "opportunity_title": "string",
    "wild_scan_source": "path to source JSON",
    "quotes_analyzed": 25,
    "personas": [
      {
        "persona_name": "string",
        "description": "string",
        "cluster_size": 5,
        "avg_score": 7.5,
        "dimensions": {
          "journey_stage": "string",
          "frustration_type": "string",
          "attempted_solutions": "string",
          "career_context": "string"
        },
        "pain_stories": [
          {
            "situation": "string",
            "pain": "string",
            "current_workaround": "string",
            "emotional_state": "string",
            "evidence": "string — full quote with attribution"
          }
        ],
        "decision_triggers": [
          { "trigger": "string", "urgency": "high|medium|low", "channel": "string" }
        ],
        "objections": [
          { "objection": "string", "counter": "string" }
        ],
        "willingness_to_pay": {
          "range": "string",
          "evidence": "string",
          "anchor_products": ["string"]
        },
        "channels": [
          { "platform": "string", "behavior": "string" }
        ],
        "evidence_map": {}
      }
    ],
    "next_step_hint": {
      "top_persona": "string",
      "top_persona_reasoning": "string",
      "recommended_next_skill": "offer-scope | persona-extract",
      "recommended_action": "string"
    }
  }
}
```

### JSON-to-offer-scope Compatibility

The persona fields are structured to match the `OfferScopeInput.persona` interface exactly:

```typescript
// offer-scope expects:
interface OfferScopeInput {
  persona: {
    persona_name: string
    pain_stories: { situation, pain, current_workaround, emotional_state, evidence }[]
    decision_triggers: { trigger, urgency, channel }[]
    objections: { objection, counter }[]
    willingness_to_pay: { range, evidence, anchor_products }
    channels: { platform, behavior }[]
  }
}

// quote-to-persona outputs personas[] where each element IS this persona shape.
// To use: pick a persona from the output, pass it directly as offer-scope's persona field.
```

---

## Resources

### references/

- `clustering-guide.md` — Behavioral dimension analysis, example archetype patterns, field mapping table (wild-scan → quote-to-persona → offer-scope), quality criteria for clusters

---

## Quality Checklist

Run this checklist before delivering output:

- [ ] Wild-scan JSON loaded and validated (15+ quotes, required fields present)
- [ ] Clustering is behavioral, not by pain_category — archetypes describe WHO, not WHAT
- [ ] Each cluster has at least 3 quotes (no orphan clusters)
- [ ] 3-5 clusters total (not over-split, not under-split)
- [ ] Archetype names are memorable and encode the behavioral pattern
- [ ] Each persona has at least 3 pain_stories with real evidence (full quote + attribution)
- [ ] Each persona has at least 2 decision_triggers with urgency and channel
- [ ] Each persona has at least 2 objections with evidence-based counters
- [ ] Willingness to pay is anchored to products/spend mentioned in quotes
- [ ] Channels are derived from the actual platforms where member quotes were found
- [ ] Evidence map links every synthesized field to source quote index(es)
- [ ] No fabricated evidence — every claim traces to a quote or is explicitly marked `[inferred]`
- [ ] JSON output conforms to PipelineEnvelope schema (skill, version, session_id, timestamp, input_refs, output)
- [ ] JSON persona shape matches offer-scope's expected input interface
- [ ] Markdown output has correct frontmatter (type: persona, date, status, tags, wild_scan_ref)
- [ ] Both files saved to vault at `Admin/Product-Discovery/Personas/`
- [ ] Markdown uses Obsidian wikilinks for cross-references
- [ ] Output is mobile-readable (no overly wide tables, clear headers, scannable structure)
