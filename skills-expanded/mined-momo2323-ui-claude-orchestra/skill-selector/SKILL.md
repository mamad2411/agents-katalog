---
name: skill-selector
description: Use when an orchestra has multiple skills, MCPs, or connectors that could plausibly handle the same task (e.g. frontend has frontend-design + ui-ux-pro-max + remotion + Figma + 21st.dev). Scores each candidate against the user's vision, prior preferences, and task complexity, picks the winner, EXPLAINS the choice when non-obvious, and asks the human to disambiguate when confidence is below 70%. Logs every pick to learnings for pattern improvement over time.
license: MIT
version: 1.0.0
---

# Skill Selector — Picking Between Similar Skills Within an Orchestra

> *"An orchestra can hold many skills that do the same job in different ways. Check them all,
> try them when the task is complex, and ask the human when you're unsure."*
>
> This skill operationalizes that into a transparent scoring + announcement + learning loop.

## The problem this solves

Most orchestras have **multiple candidates** for the same task:

| Orchestra | Example overlap |
|---|---|
| DESIGN | frontend-design · ui-ux-pro-max · modern-web-design · web-design-engineer · taste-design · 21st.dev (`magic`) |
| RESEARCH | search-agent · deep-research · market-research · firecrawl · brightdata-plugin · nimble |
| LEAD GEN | Apollo · Apify · brightdata · search-agent · sales-outreach |
| BUILD | code-reviewer · pr-review-toolkit · superpowers:requesting-code-review |
| CONTENT | content-creator · copywriting · marketing-content-creator · book-co-author |

Picking randomly = inconsistent quality. Picking by recency = staleness. Picking by name = bias.

**This skill picks deterministically, explains why, and asks when uncertain.**

---

## When to invoke

- **Automatically:** when more than ONE skill in the active orchestra's roster matches the task signal
- **Manually:** when the user says "pick the right skill for X" or "which design skill should I use"
- **Inside `orchestra-router`:** as a sub-step after orchestra activation, before player invocation

**Skip when:** only one skill in the orchestra matches the task (no choice to make), or the user has explicitly named a specific skill ("use ui-ux-pro-max").

---

## The scoring algorithm

For each candidate skill in the target orchestra, compute a score 0–1:

```
score = (
    relevance_to_task        * 0.35   # how well the skill description matches the task
  + user_vision_alignment    * 0.25   # match against stated vision (e.g. "premium" → max-pro)
  + prior_preference_weight  * 0.20   # pulled from ~/.claude/projects/<x>/memory/feedback
  + complexity_fit           * 0.15   # task complexity vs skill's complexity-fit field
  + skill_freshness          * 0.05   # slight novelty boost for less-used skills
)
```

### Computing each component

**relevance_to_task** (0–1)
- Read user prompt + extract keywords
- Read candidate's `description` frontmatter
- Score based on overlap + semantic fit (use judgment, not just literal word match)

**user_vision_alignment** (0–1)
- Pull stated vision from user prompt (e.g. "ultra-polished", "rapid prototype", "long-form analytical")
- Score how the candidate aligns
- Examples:
  - "premium coffee shop" → ui-ux-pro-max scores 0.9, rapid-prototyper scores 0.3
  - "throwaway POC" → rapid-prototyper scores 0.9, ui-ux-pro-max scores 0.4

**prior_preference_weight** (0–1)
- Check `~/.claude/projects/<current-project>/memory/` for feedback entries mentioning this skill
- Positive feedback → boost (e.g. 0.8); negative → penalty (e.g. 0.2)
- Default: 0.5 (neutral)

**complexity_fit** (0–1)
- Task complexity signals: number of files affected, integration concerns, design judgment needed
- Compare to candidate's `complexity-fit` frontmatter field (`simple` | `moderate` | `complex`)
- Mismatch = 0.3; exact match = 1.0

**skill_freshness** (0–1)
- How recently was this skill used? (check selection log below)
- Less recently used → slight boost (encourages trying alternatives, avoids monoculture)
- Cap at 0.3 weight increment — never let novelty override genuine fit

---

## Step 0 — Retrieve candidates via qmd (the primary path)

Before scoring, retrieve the candidate pool from the local skill vector index.
This replaces reading `.orchestra-scan.md` directly — the index covers all ~1,700+ skills
and plugin skills, is always fresh, and returns only the semantically-relevant top candidates.

**Protocol:**

1. Call the `qmd` MCP `query` tool:
   ```
   collection: "skills"
   searches:
     - type: "lex"
       query: <2-5 keywords from the user task>
     - type: "vec"
       query: <one-sentence description of what the user is trying to accomplish>
   intent: <same one-sentence description>
   ```
   Return top 15 results (`-n 15`). Each result is a skill stub with its full description.

2. The result set is your **candidate pool** — proceed to the scoring algorithm below.

3. **Fallback** (if qmd is unavailable or returns 0 results):
   - Fall back to reading `~/.claude/.orchestra-scan.md` and filter candidates by
     description keyword relevance to the task (v2.2 inventory-driven scoring).
   - This file is now kept fresh and untruncated by `build-skill-index.sh`.

4. **Global, not orchestra-scoped:** the retrieval searches the ENTIRE skill catalog —
   not filtered to the announced orchestra. A skill mis-filed in the wrong orchestra,
   or on the Reserve Bench, will still be found and scored. The orchestra is announced
   for UX/doctrine purposes; skill selection is driven by semantic relevance.

5. **Filter before scoring:** from the top-15, exclude any with
   `disable-model-invocation: true` in their frontmatter (axiom-*, caveman*, etc.).

---

## The decision tree

```
0. Retrieve candidates via qmd (see Step 0 above)
1. Score each retrieved candidate
3. Sort descending
4. Compute (top - second) gap
5. Classify each pair as complementary or substitute (see below)
6. Decide:

   IF top_score >= 0.85 AND second_score <= 0.5:
       → SILENT PICK — pick top, no announcement (clear winner, obvious choice)

   ELIF top-2 (or top-3) score within 15% AND classified as COMPLEMENTARY:
       → STACK PICK — return all complementary members as a stack (cap at 3)
                       announce the stack with each member's role
                       (v2.1 — added 2026-05-25)

   ELIF top_score >= 0.7 AND (top - second) >= 0.15:
       → ANNOUNCED PICK — pick top, announce choice + reason

   ELIF top_score >= 0.7 AND (top - second) < 0.15 AND classified as SUBSTITUTES:
       → ASK_HUMAN — two strong substitutes too close to call

   ELIF top_score >= 0.5:   (0.5 ≤ top < 0.7)
       → ASK_HUMAN — low confidence between existing tools; clarify task with user

   ELSE (top_score < 0.5):
       → CAPABILITY GAP — nothing installed fits. Fire the Gap → Recommend
         protocol (v2.3, below) BEFORE falling back to a generic approach.
```

### Complementary vs Substitute classification (v2.1)

Before applying the decision tree, classify the relationship between the top candidates:

| Relationship | Definition | Example |
|---|---|---|
| **Substitute** | Both produce the same output domain — using both is redundant | `gpt-image-2` + `nano-banana` (both image gen); `code-review` + `pr-review-toolkit:code-reviewer` (both review code) |
| **Complementary** | Produce different output facets — combined coverage is greater than either alone | `frontend-design` (visual system) + `ui-ux-pro-max` (interaction patterns) + `frontend-patterns` (component conventions); `deep-research` (gather) + `content-research-writer` (write); `security-review` (vulns) + `a11y-audit` (accessibility) |

**Heuristic for classification (no external table needed):**
1. Read each candidate skill's `description` field.
2. Extract the primary output verb/object (e.g. "generate image", "review code", "design layout", "research market").
3. If primary outputs match → substitutes.
4. If primary outputs differ AND would naturally compose (one feeds the other, or both cover non-overlapping facets) → complementary.
5. When in doubt → substitute (default to single-pick, safer for token economy).

**Stack thresholds (explicit numeric rules — v2.1 calibration after AUDIT MINOR-1):**

| Stack size | Triggering rule | Example scores |
|---|---|---|
| **2-skill stack** | `top - second ≤ 0.15` AND classified COMPLEMENTARY | 0.82 / 0.78 (gap 0.04 ✓) |
| **3-skill stack** | `top - third ≤ 0.25` AND all three classified COMPLEMENTARY | 0.82 / 0.78 / 0.73 (gap 0.09 ✓) |
| **No stack** | gap exceeded, OR any pair classified SUBSTITUTE | fall through to SILENT / ANNOUNCED / ASK_HUMAN |

These thresholds are tunable in `~/.claude/rules/orchestra-system.md` per orchestra (use the
existing `skill-selector:` block):

```markdown
### 🎨 DESIGN
skill-selector:
  stack-2-gap: 0.15    # default
  stack-3-gap: 0.25    # default
  max-stack-size: 3    # default; do not raise above 3 without strong evidence
```

**Stack cap:** Hard maximum of **3 skills** per stack. More than 3 is noise — if you find 4+
complementary candidates, fall back to top-3 by score, or ASK_HUMAN.

**Stack lead:** The first member of the stack is the LEAD (highest scorer). The lead's
conductor is responsible for orchestrating the others — same one-conductor-per-orchestra rule
applies. The other stack members are invoked by the lead as needed.

### Threshold tuning

The 70% / 85% / 15-point gap thresholds are tunable per orchestra in `orchestra-system.md`:

```markdown
### 🎨 DESIGN
skill-selector:
  silent-pick-threshold: 0.85
  announce-pick-threshold: 0.7
  ask-human-gap-threshold: 0.15
```

Defaults work for most cases. Tune per user preference over time.

---

## Announcement formats

### Silent pick (clear winner)

```
🎼 BUILD active · Conductor: architect · Using: code-reviewer
```

No skill-selector noise. The skill name appears in the `Using:` field. User sees the pick implicitly.

### Stack pick (complementary skills — v2.1)

```
🎼 🎨 DESIGN active · Conductor: design-ux-architect
   Selected stack (3 skills, complementary):
     1. frontend-design (LEAD) — design system + tokens
     2. ui-ux-pro-max — interaction patterns
     3. frontend-patterns — component conventions
   Reason: visual-system + interaction-patterns + component-conventions cover orthogonal facets of "build a hero section". Top-3 scored within 12% (0.82 / 0.78 / 0.73); all classified as complementary (different output domains).
```

For 2-skill stacks, format identically with just 2 numbered members.

### Announced pick (non-obvious choice)

```
🎼 DESIGN active · Conductor: design-ux-architect
   Selected: ui-ux-pro-max
   ↳ over: frontend-design, modern-web-design
   ↳ reason: user said "premium coffee shop" → aesthetic-heavy fit; prior preference for max-pro stack
```

Keep reason to **one sentence**. Avoid long justifications — the choice should feel obvious once explained.

### ASK_HUMAN (close call or low confidence)

```
🎼 DESIGN active · Conductor: design-ux-architect

🤚 ASK_HUMAN: Two strong design options for this task:
   1. ui-ux-pro-max — best for maximum polish, premium feel, opinionated aesthetics
   2. frontend-design — best for fast iteration, modern minimal aesthetics
   
   Which fits your vision better? (Say "your call" and I'll pick top.)
```

If user says "your call" → pick top + log a normal "Announced pick" with reason "user deferred."

---

## The selection log

Every pick gets logged to `~/.claude/docs/learnings/skill-selections.md`:

```markdown
## 2026-05-25 17:32 — DESIGN
- **Task:** "make me a coffee shop website"
- **Candidates:** [ui-ux-pro-max, frontend-design, modern-web-design]
- **Scores:** [0.87, 0.71, 0.65]
- **Gap (top-second):** 0.16
- **Decision:** ANNOUNCED PICK — ui-ux-pro-max
- **Reason:** premium-coffee-shop keyword cluster + prior preference for max-pro
- **Outcome:** TBD (update on user feedback)
- **User feedback:** _populate when known_

## 2026-05-25 19:14 — RESEARCH
- **Task:** "find the latest on multi-agent frameworks"
- **Candidates:** [search-agent, deep-research, firecrawl, brightdata-plugin]
- **Scores:** [0.78, 0.76, 0.45, 0.40]
- **Gap:** 0.02 ← TOO CLOSE
- **Decision:** ASK_HUMAN
- **User answer:** "search-agent"
- **Outcome:** Pending verification
```

Over time, this becomes a dataset for:
- Tuning scoring weights per orchestra
- Learning the user's actual preferences (vs declared ones)
- Identifying skills that consistently win/lose (signal for promotion/demotion)
- Identifying redundant skills (always lose, never picked — candidate for archival)

---

## Applies to skills AND MCPs/connectors

Same algorithm. Just point at the right candidate set:

**For MCPs/connectors** (e.g. Apollo vs Apify vs Nimble vs brightdata-plugin for lead research):

```yaml
# In each MCP/connector's metadata
best-for: ["B2B-leads", "company-enrichment"]
complexity-fit: moderate
cost-profile: "expensive"   # cheap | standard | expensive
auth-required: true
preferred-when: ["small-batch", "company-name-known"]
```

Selection adds two more signals:
- **cost_alignment** — match task budget signals ("just a quick test" → cheap MCP wins)
- **auth_readiness** — penalize if required auth tokens aren't configured

---

## Examples

### Example 1: Silent pick (clear winner)

```
User: "fix the typo in line 42 of auth.ts"

Orchestra: BUILD
Candidates: [code-reviewer (0.45), pr-review-toolkit (0.52), focused-fix (0.91)]
Decision: SILENT PICK — focused-fix

Announcement: 🎼 BUILD active · Conductor: architect · Using: focused-fix
```

### Example 2: Announced pick (interesting choice)

```
User: "design a hero section for a yoga studio landing page"

Orchestra: DESIGN
Candidates:
  - ui-ux-pro-max (0.88)         premium, aesthetic-heavy
  - modern-web-design (0.74)     contemporary minimal
  - taste-design (0.71)          curated aesthetic
  - frontend-design (0.69)       fast iteration

Top score 0.88, second 0.74, gap 0.14 (just under 0.15) → ANNOUNCED PICK

Announcement:
🎼 DESIGN active · Conductor: design-ux-architect
   Selected: ui-ux-pro-max  
   ↳ over: modern-web-design, taste-design, frontend-design
   ↳ reason: yoga studio = sensory/aesthetic-heavy → max-pro's polish fits
```

### Example 3: ASK_HUMAN (genuine ambiguity)

```
User: "find out who's the best contact at Acme Corp for AI procurement"

Orchestra: LEAD GEN & SALES
Candidates:
  - Apollo (0.79)              org enrichment, contact info
  - nimble:company-deep-dive (0.77)   deep company intelligence
  - apollo_contacts_search (0.72)     contact-level search

Top 0.79, second 0.77, gap 0.02 → ASK_HUMAN

🤚 ASK_HUMAN: Two strong options for finding contacts at Acme Corp:
   1. Apollo (org enrichment + contact search) — best when you have a name list
   2. nimble:company-deep-dive — best for deep context on the org first, contacts second
   
   Do you already have specific contact names to enrich, or do you need the org intel first?
   (Say "your call" and I'll start with Apollo.)
```

### Example 4: Low confidence (any candidate is a poor fit)

```
User: "i want to do the thing with the stuff"

Orchestra: ??? (ambiguous)
Top candidate scores all below 0.5 → ASK_HUMAN

🤚 ASK_HUMAN: I'm not confident any skill fits this task well — could you tell me more?
   - What are you trying to build or learn?
   - Is this code, content, research, or something else?
```

---

## Common pitfalls

| Pitfall | Why bad | Better |
|---|---|---|
| Pick on alphabetical order | No signal, arbitrary | Score on relevance |
| Pick always-the-same skill | Monoculture, misses better fits | Use freshness boost |
| Announce every pick | Noisy, drowns out real work | Silent for clear wins, announce only non-obvious |
| ASK_HUMAN for everything | Annoying, defeats automation | Only when confidence < 70% or gap < 15pts |
| Skip the log entry | Loses learning data | Always log, even silent picks |
| Score on skill name length / "fanciness" | Bias toward complex skills for simple tasks | Use `complexity-fit` field |
| Ignore prior preferences | Repeats user's known mistakes | Pull from auto-memory feedback |

---

## Integration with orchestra-router

Once orchestra-router v2 ships, this skill is invoked automatically as a sub-step:

```
orchestra-router v2:
  1. Match intent → orchestra(s) activated
  2. For each orchestra:
     → invoke skill-selector to pick player(s)
     → if ASK_HUMAN returned, pause + ask user
     → if pick returned, continue
  3. Run hallucination-guard ENTRY gate
  4. Execute chain with selected players
  5. ...
```

Until v2 ships, invoke manually:

```
Skill(skill-selector) when an orchestra has 2+ candidates for the same task.
```

---

## Out of scope (don't do these)

- **Selecting BETWEEN orchestras.** That's orchestra-router's job (intent matching). skill-selector picks WITHIN one orchestra.
- **Modifying skill files.** This skill picks; it doesn't edit candidates.
- **Auto-installing missing skills.** That's orchestra-intake's job.

---

---

## v2.2 — 3-Layer Ensemble Mode (added 2026-05-26)

v2.1 returned a single pick or a 2–3 skill stack. v2.2 returns a full ensemble across 3 layers
and a tier flag. This is the harmony-mode upgrade — every orchestra activation pulls the best
combination of skills + MCPs + plugins + connectors that genuinely contribute.

### Layered output schema (v2.2)

```yaml
selection:
  tier: DEFAULT | EXPANSION
  active_ensemble:           # Score ≥ 0.70 (DEFAULT) or ≥ 0.55 (EXPANSION)
    - name: <skill/agent/MCP/plugin/connector name>
      score: <0.0–1.0>
      role: lead | section
      class: skills | agents | mcps | plugins | connectors
  standby_bench:             # Score 0.55–0.69 (DEFAULT only — promoted in EXPANSION)
    - name: <name>
      score: <0.0–1.0>
      class: <class>
  reserve_bench:             # Score < 0.55 — listed for completeness only
    count: <int>
  cap_used: <int>            # active_ensemble size
  cap_max: 12 | 18           # DEFAULT or EXPANSION
  asked_human: <bool>        # true if beyond EXPANSION cap
```

### Tier-selection algorithm

```
1. Read the active orchestra's `harmony-tier-default` field from orchestra-system.md.
   Default if missing: DEFAULT.
2. If conductor explicitly flags "highest-stakes thinking" for this task → escalate to EXPANSION.
3. Apply tier thresholds:
   - DEFAULT:   active ≥ 0.70, standby 0.55–0.69, cap 12
   - EXPANSION: active ≥ 0.55, standby N/A (auto-promoted), cap 18
4. If active_ensemble size would exceed cap → surface ASK_HUMAN with the top candidates beyond cap.
```

### Inventory-driven candidate pool (v2.2)

**Candidate gathering changes:**

- **v2.1:** candidates came from the active orchestra's First Chair + Section entries in
  `orchestra-system.md` (curated, ~20-50 candidates per orchestra).
- **v2.2:** candidates come from `~/.claude/.orchestra-scan.md` (full inventory, ~500-700
  candidates across all classes), filtered by description-match relevance to the task.

**Why:** ensures every installed tool is scored, not just the curated subset. This is the
"no tool left behind" structural guarantee.

**Implementation:**
1. Read `~/.claude/.orchestra-scan.md` once per session (cache in memory).
2. For each candidate, compute `relevance_to_task` (v2.1 algorithm unchanged) using its
   `description` field from the scan.
3. Apply the existing scoring formula (relevance + vision + preference + complexity + freshness).
4. Apply within-class dedup (substitutes → keep best, complements → keep all that hit threshold).
5. Sort, bucket into Active / Standby / Reserve per tier rules.

### Within-class dedup (formalized in v2.2)

Same heuristic as v2.1 stack-classification:

1. Read each candidate's `description` field.
2. Extract primary output verb/object.
3. Same primary output = SUBSTITUTE → keep highest scorer in same class; rest demoted to Standby.
4. Different primary output = COMPLEMENT → keep all that hit tier threshold in same class.
5. Across classes (e.g. a skill + an MCP that both touch design) = never dedup.

### Announcement format (v2.2 — full ensemble)

```
🎼 🎨 DESIGN active · Conductor: design-ux-architect
   Tier: DEFAULT (cap 12, using 6)
   Active ensemble (6):
     Skills:      frontend-design (LEAD, 0.87), ui-ux-pro-max (0.82), frontend-patterns (0.74), remotion (0.72)
     MCPs:        21st.dev/magic (0.78)
     Connectors:  Figma (0.71)
   Standby bench (3): canva (0.68), web-artifacts-builder (0.66), stitch-design (0.64)
   Reserve: 14 dormant (named-invoke only)
```

For EXPANSION-tier orchestras, the Standby line is absent (those candidates promoted into Active),
and the cap reads "EXPANSION (cap 18, using N)".

### Backward compatibility with v2.1 stack mode

If only 2-3 candidates from a single class hit threshold and are classified COMPLEMENT, the v2.2
ensemble naturally degenerates to a v2.1 stack — same output shape, just with the Standby line
added. v2.1 callers get a strict superset. No breaking change.

### Selection log v2.2 (extends v2.1 entries)

Add these fields to each entry in `~/.claude/docs/learnings/skill-selections.md`:

```markdown
## 2026-05-26 09:14 — 🎨 DESIGN
- **Tier:** DEFAULT
- **Pool size:** 487 (from .orchestra-scan.md)
- **Above 0.70:** 6 → Active Ensemble
- **0.55–0.69:** 3 → Standby
- **Below 0.55:** 478 → Reserve (silent)
- **Within-class dedups:** 2 (canva demoted under figma; gpt-image-2 demoted under nano-banana)
- **Cap status:** under cap (6/12)
- **ASK_HUMAN fired:** no
```

---

## v2.3 — Gap → Recommend protocol (added 2026-07-03)

When retrieval + scoring produce NO installed candidate ≥ 0.5, the ecosystem has a hole.
Do NOT silently do the task with a generic approach — recommend the missing tool first.

1. **Skills** — fire the `find-skills` skill: search the skills.sh registry
   (`npx skills find <keywords> [--owner <owner>]`, or
   `curl "https://skills.sh/api/search?q=<query>"` when the interactive CLI can't run).
   Quality bar: prefer ≥1K installs, reputable owner (anthropics, vercel-labs, etc.).
2. **MCPs / connectors** — query the `mcp-registry` MCP: `search_mcp_registry(<capability>)`
   and `suggest_connectors()`. Anthropic-managed connectors surface here.
3. **Plugins** — check configured marketplaces (`~/.claude/plugins/known_marketplaces.json`)
   for an installable plugin covering the gap.
4. **Present** the top 1–3 candidates with source, install count, and the exact install
   command. Announce with:
   `🧰 CAPABILITY GAP — no installed tool scores ≥ 0.5 for <task>. Recommended: <name> (<source>, <installs>)`
5. **On approval** → run `orchestra-intake` (security scan → classify → file into orchestra →
   log). Rule 13: nothing installs without the 5-step security scan; nothing installed goes
   unfiled.
6. **Log the gap** to `~/.claude/docs/learnings/skill-selections.md` with decision
   `GAP_RECOMMENDED` — recurring gaps are install signals, one-off gaps are noise.

This is how the orchestra grows itself: gaps → recommendations → security-scanned installs →
filed players. (added in the 2026-07-03 system audit.)

---

## Anthropic guidance applied (researched 2026-05-26)

The scoring formula's most important component is **relevance_to_task** — which is identical to
what Anthropic's runtime does natively: Claude reads each skill's `description` field (truncated
to **1,536 chars** in the skill listing) and judges semantic fit against the user's message.

Key findings from official Anthropic docs (`code.claude.com/docs/en/skills`) and the
`agentskills.io` open spec that affect how scores should be computed:

### 1. `description` is the primary selection signal — write it for Claude, not humans

The description should answer TWO questions:
- *What does this skill do?* (capability)
- *When should I use this?* (trigger conditions, use cases, examples)

Anthropic limits skill listing to **1,536 chars** total for name + description + `when_to_use`.
The current `relevance_to_task` score should weight the `when_to_use` field *at least equally*
to the description body — it's a dedicated trigger-phrase field, and skills that have one with
explicit task-matching phrases will consistently outperform those with only a generic description.

**Practical implication:** when two skills score similarly on description alone, check if either
has a `when_to_use` field with phrasing that exactly matches the user's request — if so, boost
that skill's `relevance_to_task` by ~0.1.

### 2. `disable-model-invocation: true` signals "never auto-select"

Skills with this flag in their frontmatter are **explicit-invoke only** — they should never
appear in the Active Ensemble or even the Standby Bench. During candidate gathering from
`.orchestra-scan.md`, filter these out before scoring.

Current skills with this flag: all `axiom-*` (iOS), all `caveman*` output-mode utilities.

### 3. No published numerical scoring — the formula is judgment, not algorithm

Anthropic does not publish scoring thresholds. The 0.70 / 0.85 / 15% gap values are
**custom calibration anchors** (documented as such in the Credits section below). They
represent "feels right for the author's workflow" defaults, tunable per orchestra. Don't treat
them as ground truth — treat them as starting points to calibrate from selection logs.

### 4. Description quality directly controls selection quality

Because `relevance_to_task` is the heaviest-weighted component (0.35), a poorly written
description is a **selection tax** — the skill will underperform its actual capability at
every activation. The maximum leverage point for improving selection accuracy is improving
the `description` and `when_to_use` fields of installed skills, not tuning the score weights.

---

## Credits

- **Scoring algorithm structure** — original to orchestra v2 design
- **ASK_HUMAN status** — borrowed from `hallucination-guard` skill (same family)
- **Decision-tree thresholds** — the author's Q4 default (70% confidence) and Q3 default (announce non-obvious only)
- **CrewAI's role-overlap insight** — validation that explicit scoring beats implicit LLM-routing
- **v2.2 3-Layer Ensemble + Inventory-driven scoring** — the author's "no tool left behind" requirement, formalized 2026-05-26

MIT licensed. Improve and PR back to `claude-orchestra`.
