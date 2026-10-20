---
name: QCOE
version: 1.0.0
description: Structured COE (Correction of Errors) with 5-Whys root cause analysis. Use when the user asks to "run a COE", "root cause analysis", "5 whys", "post-mortem", "incident review", "what went wrong", or needs to analyze any failure, bug, or process gap.
trigger: QCOE
claude_tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
dependencies:
  agents: []
tools: []
---

# QCOE - Structured COE Workflow

## Purpose

Guide the user through a structured Correction of Errors (COE) process — from incident description to publishable COE document — using 5-Whys root cause analysis. Works in any project, any language, any team size.

---

## Input Modes

QCOE accepts incidents in three modes:

**Mode 1: Free-form description (most common)**
```
/qcoe "Standing orders were all dispatched to one agent for 2 weeks"
```

**Mode 2: Agent failure reference (projects with agents/ directory)**
```
/qcoe agent:social-post-daily-draft run:abc123
```

**Mode 3: Interactive (no arguments — prompted step by step)**
```
/qcoe
```

**Resume a saved draft:**
```
/qcoe --resume docs/coe/2026-04-11-draft.md
```

---

## Workflow

### Phase 0: Pattern Scan

Before starting analysis, scan for related prior COEs.

**Actions:**
1. Check if `docs/coe/` exists (or similar: `coes/`, `post-mortems/`, `.coe/`)
2. If found, Grep for keyword overlap with the current incident description
3. If matches found, surface: "This may be related to [N] prior COEs: [titles]. Consider whether this is a repeat pattern before proceeding."
4. Check git log for commits referencing "coe", "fix", "revert", or the incident keywords — limit scope to `docs/` and relevant agent directories only

**Output to user:**
- Count of related COEs found (0 = green, proceed; 1+ = surface titles and ask if this is a new incident or follow-up)
- If this is identified as a repeat pattern, flag it explicitly: "REPEAT PATTERN — this class of failure has occurred before. Root cause analysis must address why prior fixes did not hold."

**Time estimate shown up front:**
- Free-form mode: ~5 minutes
- Interactive mode: ~10 minutes
- Agent failure mode: ~3 minutes

---

### Phase 1: Gather Context

Accept the incident description and extract structured facts.

**For Mode 1 (free-form):**
Extract from the user's description:
- What happened (symptom)
- When it happened (timestamp or approximate)
- Who noticed (reporter)
- What broke (affected system/feature)
- What was the impact (scope, duration, severity indicators)

If any of the above are missing, ask for them before proceeding. Minimum required: what happened + what broke.

**For Mode 2 (agent failure):**
- Check for `agents/<name>/` directory — read `agent.json` if present (do not read other agents' contracts)
- Check for error logs in `data/`, `logs/`, or project-specific log paths
- Check git log scoped to `agents/<name>/` for recent changes
- Construct the incident summary from structured data

**For Mode 3 (interactive):**
Prompt for each field in sequence:
1. "What happened? (describe the failure or gap)"
2. "When did it happen? (date/time or approximate)"
3. "Who noticed it and how?"
4. "What was broken or impacted?"
5. "What was the business impact? (users affected, data lost, SLA missed, etc.)"

**--resume flag:**
If `--resume path/to/draft.md` is provided:
- Read the draft file
- Identify which phase was last completed
- Resume from the next phase
- Confirm with user: "Resuming COE draft from Phase [N]. Continue? (yes/no)"

---

### Phase 2: Classify Severity

Based on gathered context, classify the incident:

| Severity | Criteria |
|----------|----------|
| **sev1** | Complete system outage, data loss, customer data exposed |
| **sev2** | Major feature down, significant customer impact, SLA breach |
| **sev3** | Degraded service, missed internal SLA, repeated failure pattern |
| **Process Failure** | Behavioral/operational gap, decision error, repeat process mistake |
| **Near Miss** | Could have caused impact but did not — still worth documenting |

Present the classification with reasoning: "Based on what you've described, this is a **[severity]** because [reason]. Correct?"

Allow user to override the classification.

---

### Phase 3: Build Timeline

Construct a chronological timeline from available evidence.

**Evidence sources to check (in order):**
1. User-provided timestamps (always highest priority)
2. Git log — scope to `docs/`, `agents/<name>/`, relevant config files ONLY. Do not scan entire repo.
   ```bash
   git log --oneline --since="[incident_date - 7 days]" -- docs/ agents/<name>/
   ```
3. File modification dates for relevant files
4. Agent run logs if present

**Evidence-light path:**
If the user has only a narrative and no structured data (no git history, no logs, no timestamps):
- Do not block. Proceed with what is available.
- Mark timeline entries as "approximate" or "user-reported"
- Note in the COE document: "Timeline reconstructed from user narrative; limited forensic evidence available."

**Timeline format:**
| When | What | Source |
|------|------|--------|
| YYYY-MM-DD HH:MM | Event description | git commit abc123 / user-reported / file mtime |

---

### Phase 4: 5-Whys Analysis

Generate all 5 Whys based on available context, then present them ALL together for user review.

**Do NOT ask 5 separate questions.** Generate the full chain, then ask for corrections.

**Why structure:**

| Why | Focus | Question Frame |
|-----|-------|----------------|
| Why 1 | Symptom | "What was the direct observable failure?" |
| Why 2 | Trigger | "Why did that failure occur?" |
| Why 3 | Contributing factor | "Why was that trigger possible?" |
| Why 4 | Detection gap | "Why wasn't this caught before impact?" |
| Why 5 | Structural root cause | "What system/process design allowed this?" |

**For each Why, include:**
- Specific question (tailored to this incident, not generic)
- Answer (factual, evidence-based)
- Evidence citation (file path, log entry, commit hash, timestamp, or "user-reported")

**Presentation format:**

```
--- 5-Whys Draft ---

Why 1: [specific question]
Answer: [answer]
Evidence: [citation]

Why 2: [specific question]
Answer: [answer]
Evidence: [citation]

Why 3: [specific question]
Answer: [answer]
Evidence: [citation]

Why 4: [specific question]
Answer: [answer]
Evidence: [citation]

Why 5: [specific question]
Answer: [answer]
Evidence: [citation]

---
Do any of these need correction? Reply with the Why number and your correction, or "looks good" to proceed.
```

**Auto-save after Phase 4:**
After the user confirms the 5-Whys, write a draft to `docs/coe/YYYY-MM-DD-[slug]-draft.md` before proceeding. Confirm: "Draft saved to [path]. Proceeding to root cause synthesis."

---

### Phase 5: Root Cause Synthesis

Synthesize the root cause in one paragraph.

**Rules:**
1. Root cause is always **structural** — a system design flaw, a missing mechanism, a process gap
2. **Never** accept "someone forgot" or "we didn't think of it" as a root cause. If the 5-Whys chain lands there, push one level deeper: "What mechanism should have prevented someone from needing to remember this?"
3. **External/boundary-of-control root causes are valid** (e.g., "AWS us-east-1 outage", "third-party API rate limit"). When the root cause is external, the pivot question becomes: "Why didn't we detect or mitigate faster?" — and the preventive mechanisms address detection/mitigation, not prevention.
4. **Multi-root-cause incidents:** If the analysis surfaces more than one root cause, cap at **3 primary 5-Whys chains**. Additional factors are listed as "contributing factors" without full chains.

**Output:**

```
Root Cause: [one paragraph]

[If multi-root-cause:]
Primary causes (full chains above):
1. [cause 1]
2. [cause 2]
3. [cause 3 — if applicable]

Contributing factors (no full chain needed):
- [factor A]
- [factor B]
```

---

### Phase 6: Corrective Actions

Generate a table of corrective actions.

**Include:**
- Actions already taken (if any — mark as Done)
- Actions needed (mark as Pending)
- Owner for each action (use "TBD" if unknown)

**Format:**
| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | [action] | [owner] | Done |
| 2 | [action] | [owner] | Pending |

Ask the user: "Are there any actions already taken that I should add? Or any to remove?"

---

### Phase 7: Preventive Mechanisms

This is the highest-value section. Each preventive mechanism must satisfy all three criteria:

| Criterion | Requirement |
|-----------|-------------|
| **Deterministic** | Enforced by code or configuration — not by behavior or memory |
| **Automatic** | Runs without human intervention |
| **Testable** | Can be verified to be working (has a test or check) |

**Behavioral fixes are rejected.** If a candidate mechanism includes "we'll remember to..." or "the team should always..." — reject it and push for structural alternatives:

```
Rejected: "Engineers will always check X before deploying"
Required: "CI pipeline check that fails if X is not satisfied"

Rejected: "We'll add a comment to remind us"
Required: "Linter rule or pre-commit hook that enforces the constraint"
```

**Exception:** If no structural fix is genuinely possible (rare), document why explicitly and flag for periodic manual review as an interim measure. This must include: the reason no structural fix is possible, the manual review cadence, and who owns it.

**Suggested format for each mechanism:**
```
### 1. [Mechanism Name] (deterministic)
What it does: [description]
How it's enforced: [code/config/CI/alert]
How it's tested: [test name or check]
```

---

### Phase 8: Metrics to Watch

Define 3-5 metrics that would detect this class of failure earlier next time.

For each metric:
- **Name** — what is being measured
- **Target value** — what "healthy" looks like
- **Current value** — current state (use "unknown" if not established)
- **Measurement method** — how to collect this (log query, monitoring alert, dashboard metric)

**Format:**
| Metric | Target | Current | How to Measure |
|--------|--------|---------|----------------|
| [name] | [target] | [current] | [method] |

---

### Phase 9: Generate COE Document

Before writing, perform a sanitization check.

**Sanitization scan:**
Scan the assembled content for:
- Patterns matching credentials: `sk-`, `Bearer `, `password=`, `secret=`, API key formats
- Email addresses not already in the incident report as owners
- Internal URLs containing `.internal`, `.local`, or private IP ranges
- File paths that expose home directories or system paths unnecessarily

If sensitive content is detected:
```
SANITIZATION WARNING: The following may contain sensitive information:
- [item 1] at [location]
- [item 2] at [location]

Please review and redact before I write the file. Reply with the redacted versions or "proceed" to write as-is.
```

**Output path validation:**
- Default path: `docs/coe/YYYY-MM-DD-kebab-case-title.md`
- If user specifies a path, validate it:
  - Reject any path containing `..` segments
  - Reject any path outside the project root
  - Confirm the resolved path with the user before writing

**Lessons generation:**
Before assembling the document, generate 2-3 actionable lessons from the root cause analysis and preventive mechanisms. Lessons must be specific to this incident — not platitudes. Frame each as: what the team now knows that it didn't before, stated as a reusable principle.

**Document assembly:**
Use the template from `references/coe-template.md`. Populate all sections with the synthesized content from Phases 1-8, including the generated lessons.

**Append JSON metadata block** at the end of the document (for agent consumers):
```
<!-- COE-METADATA: {"severity":"[sev]","root_cause":"[one-liner]","action_count":[N],"file_path":"[path]","related_coes":["[title1]"]} -->
```

---

### Phase 10: Save and Report

Write the COE document to the validated path.

Confirm to the user:
```
COE saved: docs/coe/YYYY-MM-DD-title.md

Summary:
- Severity: [classification]
- Root cause: [one-liner]
- Corrective actions: [N] ([done] done, [pending] pending)
- Preventive mechanisms: [N]
- Metrics to watch: [N]
[If related COEs found:] Related COEs: [titles]
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No git repo | Skip git-based timeline. Rely entirely on user input. Note in document. |
| No agents/ directory | Skip agent-specific analysis. Use general 5-Whys. |
| Insufficient context | Block at Phase 1. Minimum required: what happened + what broke. |
| Behavioral root cause | Push one level deeper. "What mechanism should prevent this?" |
| Duplicate COE | Surface in Phase 0. Ask user to confirm this is a new incident. |
| Multiple root causes | Cap at 3 full chains. Additional factors as contributing factors list. |
| COE about a prior fix failing | Reference the prior COE. Flag explicitly as REPEAT PATTERN. |
| No structural fix possible | Document why. Add to manual review cadence. Flag as interim. |
| External root cause | Pivot to detection/mitigation question. Preventive mechanisms address speed of response. |

---

## Output Format

The final COE document follows `references/coe-template.md`.

Key formatting rules:
- Title: `# COE: [descriptive title in plain English]`
- All 5 Whys must cite evidence — no unevidenced claims
- Root cause paragraph: always ends with the structural gap, never with a person's name or action
- Preventive mechanisms: always labeled "(deterministic)" — if not deterministic, explain why as an exception
- Metadata block appended as HTML comment (invisible in rendered Markdown)

---

## Success Criteria

- Incident fully described with impact quantified
- Severity classification confirmed by user
- Timeline constructed from available evidence
- All 5 Whys answered with evidence citations
- Root cause is structural (or external with mitigation pivot)
- Corrective actions table complete with owners and status
- Every preventive mechanism is deterministic, automatic, and testable
- 3-5 metrics defined with measurement methods
- COE document written to validated path
- JSON metadata block appended
- Related prior COEs surfaced if found

## Related Skills

- **QCHECK**: Code review — use before committing the corrective action fix
- **QPLAN**: Planning — use to break down corrective actions into sprint tasks
- **QGIT**: Commit — use after the COE document is written
