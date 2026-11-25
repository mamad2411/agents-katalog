---
name: knowledge-capture
description: >
  Persist a larger knowledge artifact (research, SOTA map, solve state,
  interview insights) from a context window or session. Use when a research
  or solve session produced knowledge worth keeping beyond the conversation;
  NOT for a single fact (use knowledge_processor) or session bookkeeping.
status: draft
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: knowledge-capture

## Purpose

Substantial knowledge that was developed during a session —
research results, SOTA analyses, RFP outcomes, interview
insights, syntheses — written into the right persistent files
before it gets lost with the context window.

**Boundary against knowledge_processor:** knowledge_processor
extracts FACTS from ongoing work (observations, status changes,
technical decisions) and writes them into context files
(`context/`). knowledge_capture writes LARGER KNOWLEDGE
ARTIFACTS (research documents, SOTA maps, solve state files)
into the appropriate target directories.

```
knowledge_processor:  facts → context/         (small, frequent, inline)
knowledge_capture:    artifacts → docs/, context/ (large, rare, dedicated)
```

Analogy: knowledge_processor is "taking notes during work".
knowledge_capture is "shelving the research paper in the
library".

## Trigger

knowledge_capture is called when:

1. **After research sessions:** a substantive research result
   sits in the context window (frameworks analysed, papers
   read, interviews evaluated).

2. **Before save on substantive knowledge:** the session
   produced knowledge beyond single facts — syntheses,
   comparison tables, position maps, problem statements.

3. **On context-window limit:** the session is nearing its
   end and the developed knowledge is not yet persistent.

4. **After a solve workflow:** RFP results, axioms,
   derivations, problem statements have to become a solve
   state file.

5. **Explicit user trigger:** "Persist the knowledge from this
   session."

**Non-triggers:** single facts (→ knowledge_processor), pure
code changes (→ git), task-status updates (→
task_status_update).

## Classification — recognize the knowledge type

Before writing: classify the knowledge to determine the target
path.

| Knowledge type | Recognition | Example |
|----------------|-------------|---------|
| **Research** | Framework analysis, tool evaluation, benchmark | "14 frameworks compared" |
| **SOTA** | Position map, consensus, the project's placement | "Where do we stand vs SOTA?" |
| **Solve** | RFP result, axioms, problem statement | "Optimal workflow structure analysed" |
| **Interview** | Insights from conversations, conferences, articles | "Leoplo interview insights" |
| **Decision** | Architecture decision, trade-off analysis — **required threshold: ADR-discipline triple** (hard-to-reverse + surprising-without-context + result-of-real-trade-off). When only 1-2 are met: don't capture as a decision; consider an inline comment. Cross-ref `documentation_and_adrs` §When-an-ADR. | "ADR: why X instead of Y (triple satisfied)" |
| **Factual** | A single observed fact | → not knowledge_capture, → knowledge_processor |

## Schema — where to write?

Routing table: knowledge type → target path → format.

**Path convention:** outputs go into
`<active-context>/research/` (default, the consumer path
decides) or for framework-internal knowledge directly into
`docs/research/`. SOTA + interview insights are sub-patterns
within `research/` (prefix `sota-`, suffix
`-interview-insights`).

| Knowledge type | Target path | Filename pattern | Format |
|----------------|-------------|------------------|--------|
| Research | `<active-context>/research/` | `{topic}-{year}.md` | Free form with analysis sections, sources |
| SOTA | `<active-context>/research/` | `sota-{topic}-{year}-{month}.md` | Header + consensus + matrix + position |
| Solve | `docs/solve/` | `{date}-{topic}.md` | Phases (decompose / axioms / derive / challenge / synthesis) |
| Interview | `<active-context>/research/` | `{name}-interview-insights-{year}-{month}.md` | Insights + relevance per insight |
| Decision | `docs/decisions/` | `{number}-{topic}.md` | ADR format (context / decision / consequences) |

### Format rules

**Research files:**
- Detailed. Per framework / tool at least one paragraph of
  analysis.
- Comparison tables where useful.
- Sources section at the end (with links).
- Extend existing files (don't duplicate).

**SOTA files (`sota-*.md`):**
- Compact but complete. Restructuring follows knowledge_processor §6 (`history-imports.md`; size is a review signal); preserve meaningful content.
- Structure: consensus → matrix → position → what to steal /
  avoid.
- Cross-references to related SOTA files.
- Header with session reference and source count.

**Solve state files (`docs/solve/`):**
- Complete. Every phase of the RFP / solve process
  documented.
- Date in the filename.
- Status header (ACTIVE / COMPLETE / SUPERSEDED).
- Next-step at the end.

**Interview insights:**
- Per insight: what was said + relevance to the active scope.
- Context header: who, when, which context.
- Size is a review signal under knowledge_processor, not an eviction limit.

## Process — step by step

### 1. Scan the context

Identify all knowledge in the current context window that has
to become persistent. Checklist:

- [ ] Research results (framework analyses, tool
  evaluations)?
- [ ] SOTA placements (the project vs the field)?
- [ ] Solve / RFP results (axioms, derivations, problem
  statements)?
- [ ] Interview / external insights?
- [ ] Architecture decisions?
- [ ] Syntheses that go beyond single facts?

### 2. Classify

Per identified knowledge artifact:

```
Artifact: [description]
Type: [Research | SOTA | Solve | Interview | Decision]
Target: [path]
Action: [NEW | EXTEND (existing file)]
```

### 3. Check existing files

For every target: does a file already exist? If yes: READ and
delta-check. Extend instead of duplicate. If no: create a new
file.

### 4. Write

For each artifact, write / extend the target file. Format per
the schema table. Write thoroughly — the purpose is token
conservation, not brevity.

### 5. Link references

After writing: establish cross-references.

- SOTA files reference related SOTA files.
- Research files reference SOTA files derived from them.
- Solve state files reference the research / SOTA basis.

### 6. Registration

When new knowledge affects the skill landscape, the process
map, or maturity: update process-map.md (skill list, maturity
registry).

### 7. Confirmation

Return summary with:
- List of every written / changed file (absolute path).
- Per file: NEW or EXTENDED + line delta.
- Open points (when knowledge couldn't be fully persisted).

## Contract

### INPUT
- **Required:** substantive knowledge in the context window
  (research, SOTA, solve, interview, decision).
- **Required:** trigger satisfied (after research session,
  before save, context-window limit, after solve, explicit
  user trigger).
- **Optional:** existing target files — for delta check
  (EXTEND instead of NEW).
- **Context:** target directories
  (`<active-context>/research/` or `docs/research/`,
  `docs/solve/`, `docs/decisions/`).

### OUTPUT
**DELIVERS:**
- Persisted knowledge artifacts in the right directories.
- Correct cross-references between related files.
- process-map.md updates when the skill landscape is
  affected.
- Return summary with the file list.

**DOES NOT DELIVER:**
- No fact extraction (that's knowledge_processor).
- No task-status updates (that's task_status_update).
- No code changes.
- No context-file updates for ongoing project work (that's
  knowledge_processor).

**ENABLES:**
- The next session has access to the developed knowledge via
  persistent files.
- Research can be referenced without searching session logs.
- Solve state files can serve as input for follow-up
  workflows.
- SOTA maps enable rapid positioning in future sessions.

### DONE
- All substantive knowledge artifacts in the context window
  identified and classified.
- Per artifact: target file written or extended (delta check
  on EXTEND).
- Cross-references between related files established.
- Registration in skill-map.md when the skill landscape is
  affected.
- Return summary with the file list (NEW / EXTENDED + line
  delta).

### FAIL
- **Retry:** not foreseen — the skill writes or reports open
  points.
- **Escalate:** knowledge not fully persistable (e.g. too
  complex for focused sectional retrieval) → open points in the
  return summary.
- **Abort:** no substantive knowledge in the context → skip
  with rationale.

## Guardrails

1. **Detail:** this skill produces LONG files. The purpose is
   token conservation — compressed knowledge is worthless if
   it isn't understandable later. Lean toward too much rather
   than too little.

2. **Delta check on EXTEND:** always read existing files
   before extending. No duplication of existing content.

3. **Source requirement:** every research and SOTA file must
   cite sources. A session reference is enough for
   internally developed knowledge.

4. **Size review:** context files (`context/`) around 200
   lines are a review signal for knowledge_processor §6 (`history-imports.md`) restructuring, never deletion. Use the protected
   continuity interface for context publication. Research files (`docs/research/`) and solve state
   files (`docs/solve/`) have NO line limit — they may be as
   long as needed.

5. **No speculation:** persist only knowledge that was
   actually developed. No extrapolation, no assumptions
   without a marker.

## Example call

```
Trigger: research on agentic frameworks completed.

Scan:
  1. Framework analysis (14 frameworks) → Research, EXTEND <active-context>/research/agentic-workflow-frameworks-2026.md
  2. Leoplo interview → Interview, NEW <active-context>/research/leoplo-interview-insights-2026-04.md
  3. RFP result → Solve, NEW docs/solve/<date>-workflow-design-rfp.md
  4. SOTA placement → SOTA, NEW <active-context>/research/sota-agentic-frameworks-2026-04.md

Writing: 4 files, ~600 lines total.
References: SOTA files cross-linked, solve references research + SOTA.
Registration: knowledge_capture in process-map.md skill list + maturity registry.
```
