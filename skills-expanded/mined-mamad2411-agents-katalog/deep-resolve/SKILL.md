---
name: deep-resolve
description: "Root-cause-driven solution decision framework for the hardest problems across any domain. This is the nuclear option — it consumes significant tokens through exhaustive multi-branch root cause analysis, MECE solution enumeration, and domain-adaptive external validation. Use ONLY for genuinely difficult problems: recurring failures that resist repeated fix attempts, complex systemic issues with no clear solution path, decisions where multiple approaches exist and the wrong choice has high cost, problems with multiple interacting causes spanning components or teams. Trigger when: the user says 'what's the best way to fix X', 'why does this keep happening', 'how should we approach this', 'find the root cause', 'what are my options for fixing X', 'analyze this problem systematically', 'evaluate our options for X', 'what's the right approach and why', or expresses frustration that previous solutions didn't stick. Do NOT use for: problems where the answer is already obvious or requires no analysis, straightforward issues with clear solutions, or routine investigation. If the problem can be solved in 5 minutes of investigation, this skill is overkill."
---

# Deep-Resolve: Root-Cause-Driven Solution Decision Framework

## Your Role

You are a solution analyst. Given a complex problem in any domain, your task is to find the structurally optimal solution through systematic root cause analysis. You analyze and recommend only — you do not implement.

Your output is a decision document: what the root cause is, what every possible approach looks like, and which one to pick. The person reading it should be able to act on your recommendation without further analysis.

## Why This Framework Exists

Most solutions target symptoms. The problem recurs in a different form because the root cause is still alive. This framework works differently: it digs to the actual root cause first, then exhaustively evaluates every way to address it, ranked by how fundamentally each approach solves the problem. The result is a solution that sticks.

The core hierarchy: **eliminate root cause > bypass root cause > patch consequences**. A solution that removes the root cause is always preferable to one that works around it, which is always preferable to one that papers over its effects. This ranking is non-negotiable — it's what separates a permanent solution from another band-aid.

## Cost Warning

This framework is thorough by design — it branches into multiple hypotheses at each level, exhaustively enumerates solutions, and validates against external practice via domain-adaptive search. This consumes a large number of tokens. Reserve it for problems where choosing the wrong solution is expensive (recurring failures, high-stakes decisions, multi-factor problems). For straightforward problems where the answer is apparent after basic investigation, just address them directly.

**Execute Steps 1–5 strictly in order. Each step's output is the required input for the next — do not start Step N+1 until Step N's output section is fully written.**

---

## Step 1: Interrogate the Root Cause

Start from the observed symptom. Ask "why does this happen?" through 3 levels.

- **Level 1**: List the **5 most likely causes** (A through E). Pursue all 5 at Level 2.
- **Level 2**: For each L1 cause, ask "why?" and identify the **single most likely deeper cause**. Pursue each at Level 3.
- **Level 3**: For each L2 cause, ask "why?" and identify the **single most likely deeper cause**.

Do not skip any cause, do not skip any level — even causes you suspect are less important.

### Branching rules

- Investigate each branch using tools appropriate to the problem domain. For software problems: Read, Grep, and LSP to examine code and trace data flow; git history to check recent changes; error logs or test output for runtime evidence. For non-software problems: web search to gather data points and precedents; document analysis to review policies, specs, or reports; review available context, stated requirements, and documented decisions to verify assumptions. Select the investigation method that produces falsifiable evidence for each hypothesis.
- Rule out branches explicitly: if evidence contradicts a hypothesis, mark it as eliminated and state the evidence.
- Prefer quantitative data, documented outcomes, and multiple independent sources over anecdotal reports or single opinions. A hypothesis confirmed by one blog post is weaker than one confirmed by three independent sources with measurable outcomes.

### After the tree is complete

For each distinct problem (there may be multiple independent ones), synthesize across all its branches to identify the root cause. The root cause is the deepest, most fundamental cause in the chain — the one where addressing it would collapse the entire symptom chain above it. Treat the cause, not the symptom.

If there are multiple independent problems, identify a separate root cause for each. Carry each problem forward independently through the remaining steps.

### Validate each root cause

Use logical deduction to verify: if this root cause did not exist, trace through each step of the symptom chain — would each intermediate cause still hold? Would the original symptom still occur? If the chain breaks cleanly at the root cause (all downstream effects disappear), the root cause is confirmed. If the symptom would persist even without this cause, you've found an intermediate cause — dig deeper.

### Output format

```
## Root Cause Analysis

### Problem: [observed symptom]

Level 1 — Why does [symptom] happen?
  A: [hypothesis] → Evidence: [findings] → Confirmed / Ruled out (reason)
  B: [hypothesis] → Evidence: [findings] → Confirmed / Ruled out (reason)
  C: [hypothesis] → Evidence: [findings] → Confirmed / Ruled out (reason)
  D: [hypothesis] → Evidence: [findings] → Confirmed / Ruled out (reason)
  E: [hypothesis] → Evidence: [findings] → Confirmed / Ruled out (reason)

Level 2 — Why does [each L1 cause] happen? (one deeper cause per L1 branch)
  L1-A → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L1-B → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L1-C → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L1-D → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L1-E → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)

Level 3 — Why does [each L2 cause] happen? (one deeper cause per L2 branch)
  L2-A → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L2-B → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L2-C → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L2-D → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)
  L2-E → [deeper cause] → Evidence: [findings] → Confirmed / Ruled out (reason)

**Root Cause**: [the deepest confirmed cause]
**Validation**: If [root cause] were absent → [trace through chain] → [symptom] would not occur ✓
```

---

## Step 2: Exhaustively Enumerate Approaches

Execute this step independently for each problem identified in Step 1. For each problem's root cause, list every possible way to address it.

### Classification by how the approach acts on the root cause

Every approach falls into one of three categories:

| Category | Definition | Character |
|----------|-----------|-----------|
| **Eliminate** | Remove the root cause so it can never produce symptoms again | Permanent cure |
| **Bypass** | Avoid triggering the root cause — it still exists but the system no longer encounters it | Detour around the problem |
| **Patch** | Leave the root cause intact, fix or mitigate its downstream consequences | Symptom management |

These three categories are mutually exclusive and collectively exhaustive (MECE). A single approach can combine categories (e.g., eliminate root cause A while bypassing root cause B) — label which category applies to which root cause.

### Enumeration rules

- Aim for completeness: consider approaches from every angle. Think about structural changes, process changes, policy changes, tooling changes, organizational changes, configuration changes. For software problems, also consider data model changes, API changes, architectural changes, and library substitutions.
- If two approaches fundamentally do the same thing to the root cause (same mechanism, just different implementation details), merge them into one entry.
- Describe each approach at a high level — what it does conceptually, focusing on what changes structurally rather than implementation details. Implementation-level specifics are deferred to Step 5.

### Output format

```
## Solution Space for: [problem name]

Root Cause: [from Step 1]

### Eliminate
1. [Approach name]: [high-level description of what changes and why it removes the root cause]
2. ...

### Bypass
1. [Approach name]: [high-level description of what changes and how it avoids the root cause]
2. ...

### Patch
1. [Approach name]: [high-level description of what changes and which consequences it addresses]
2. ...
```

---

## Step 3: Evaluate and Rank

Execute this step independently for each problem. Evaluate every approach from Step 2:

### For each approach, assess three things

**1. Category classification**: Confirm whether it eliminates, bypasses, or patches. If an approach was miscategorized in Step 2, correct it here.

**2. Structural cost**: What side effects or new complexity does the approach introduce? Pay special attention to **complexity transfer** — if the solution requires compensating mechanisms (caches, retry logic, synchronization, monitoring, feature flags, additional approval layers, manual workarounds, coordination costs) whose total complexity approaches the complexity of the solution itself, the approach is moving the problem rather than solving it. Call this out explicitly. An approach that transfers complexity should be reconsidered.

**3. Priority ranking**: Apply the strict order:

> **Eliminate root cause > Bypass root cause > Patch consequences**

This ranking is mandatory. Evaluate only the approach's effect on the root cause and its own structural cost. Do **not** factor in external implementation costs (person-hours, team familiarity, organizational inertia, timeline pressure). Those are valid concerns for project planning, but they must not distort the ranking — otherwise patches always win because they're "easier," and the root cause survives.

Within the same category, rank by lower structural cost.

### Output format

```
## Evaluation for: [problem name]

| Rank | Approach | Category | Structural Cost | Notes |
|------|----------|----------|----------------|-------|
| 1 | ... | Eliminate | Low — removes the root cause cleanly | Recommended |
| 2 | ... | Eliminate | Medium — requires significant restructuring | Alternative |
| 3 | ... | Bypass | Low — simple routing change | |
| 4 | ... | Patch | High — retry + monitoring + alerting | Transfers complexity |
```

---

## Step 4: Validate Against External Practice

**Requires**: The confirmed root cause from Step 1 and the top-ranked approach from Step 3. Construct all search queries below using those specific terms.

For each problem's top-ranked approach, search for how mature organizations and projects handle the same class of problem. This step is not optional — real-world validation catches blind spots that pure analysis misses.

### Domain classification

Before searching, classify the problem domain to guide source selection:

- **Software engineering**: code, architecture, infrastructure, deployment
- **Operations**: incidents, reliability, process failures, supply chain
- **Business/strategy**: market positioning, organizational design, resource allocation
- **Regulatory/compliance**: policy, governance, standards adherence
- **Cross-domain**: problems spanning multiple categories above

This classification determines which validation sources to prioritize. Use at least two sources from different categories to avoid single-source bias.

### Search procedure

1. **Identify the problem class** — abstract from your specific case to the general pattern (e.g., "race condition in concurrent queue processing", "post-merger team integration failure", "supply chain single-point-of-failure", "compliance drift in decentralized organizations").

2. **Select and execute validation sources** based on the domain classification:

   **Code repositories** (software problems): Search GitHub for projects that have dealt with this problem class. Use `gh search repos`, `gh search code`, and `gh search issues` as appropriate. Sort by stars and examine the **top 5 repositories**. Do not impose a minimum star threshold, since some domains have fewer popular projects.

   **Web search** (all domains): Search for "[problem class] best practice", "[problem class] case study", "[problem class] production experience" to find blog posts, conference talks, practitioner reports, and documentation from experienced teams or organizations. Examine the **top 5 results** with the same rigor as code repository search.

   **Academic and research sources** (problems with established literature): Search for "[problem class] systematic review", "[problem class] framework", or "[problem class] meta-analysis" to find peer-reviewed research. Especially relevant for operations, organizational, security, and process-oriented problems where rigorous studies exist.

   **Industry standards and frameworks** (regulatory/compliance/operational problems): Search for "[problem class] industry standard", "[problem class] framework" from bodies like NIST, ISO, ITIL, or domain-specific regulatory organizations.

   **Incident postmortems** (failure-mode problems): Search for "[problem class] postmortem", "[problem class] incident report" to find how other organizations handled the same failure class.

### What to look for

- Do mature organizations or projects eliminate, bypass, or patch this class of problem? Does their category match your recommendation?
- Is there an established solution — whether a library, a design pattern, a process framework, or an industry standard — that addresses this?
- **How do they configure it?** Search for specific parameters, thresholds, policies, or decision criteria used by reference organizations. These concrete specifics are the basis for the recommendation in Step 5 — do not invent parameters later without a source from this step.
- Are there documented pitfalls or failure modes in the approach you're recommending?

### If search reveals a new approach

If you discover an approach that is not in your Step 2 enumeration, go back to Step 2 and add it, then re-run Step 3 evaluation and ranking. This loop is expected — external practice regularly surfaces solutions that pure analysis misses.

### Default preference

Prefer established solutions. Only recommend a custom or non-standard approach when you can specifically articulate why the established approach fails to address your particular root cause.

---

## Step 5: Final Recommendation

### Per-problem recommendation

For each problem, state the recommended approach:

- **What to do**: Describe the approach at a conceptual level
- **Why this approach**: Connect it back to the root cause identified in Step 1 and the category ranking from Step 3
- **External reference**: Which organizations or projects handle it similarly (from Step 4), with links where available
- **Structural cost**: What to watch for during implementation
- **Concrete parameters**: If the recommendation involves specific parameters, thresholds, or configuration values, cite the reference source with a link where available.

### Cross-problem check

If there are multiple problems, examine whether their solutions share any overlap:
- Do two problems share a deeper root cause that a single approach could address?
- Can the implementation of one solution naturally resolve or simplify another?
- If synergies exist, describe how to merge. If problems are truly independent, state that explicitly.

### External alignment summary

Conclude with:
- Which sources were referenced and what they do similarly
- How our recommended approach differs from theirs (if at all) and why
- A clear statement: are we following established practice, or deviating? If deviating, why is the deviation justified?

### Output format

```
## Recommendation

### Problem 1: [name]
**Approach**: [name from Step 3 ranking]
**Category**: Eliminate / Bypass / Patch
**What to do**: [conceptual description]
**Why**: [root cause connection + category justification]
**External reference**: [organization/project X handles this by..., link]
**Structural cost**: [what to watch for]

### Problem 2: [name]
...

### Cross-Problem Synergies
[Merge opportunities, or "These problems are independent — address separately."]

### External Alignment
- Referenced sources: [list with links]
- Our approach vs. theirs: [similarities and differences]
- Established practice or deviation: [statement with justification]
```

---

## Tool Usage

This skill is analysis-only. Use these tools for investigation but do not make changes:

### Software problems

| Tool | Purpose |
|------|---------|
| Read, Grep, Glob | Examine source code, find patterns and usages |
| LSP (goto_definition, find_references) | Trace data flow, understand call chains, find all callers |
| Bash (`git log`, `git blame`, `git diff`) | Understand change history, find when a problem was introduced |
| Bash (`gh search repos/code/issues/prs`) | Validate against mature open-source projects |

### All domains

| Tool | Purpose |
|------|---------|
| Web search | Best-practice research, case studies, practitioner reports |
| Academic search | Peer-reviewed research, systematic reviews, frameworks |
| Document analysis (Read) | Review policies, specs, reports, data |

### Recommended companion skills

- `ddg-search`: General web search and AI-synthesized answers for broad validation across all domains
- `agent-reach`: Platform-specific search (Reddit, forums, YouTube) for practitioner experience

Your deliverable is the analysis document. Implementation is someone else's job.
