---
name: wikiskill
description: >-
  Executes autonomous closed-loop agent skill evolution, trace diagnosis, refinement, and optimization using Google Research's WikiSkill framework (arXiv:2608.27454). Use when the user invokes /wikiskill or /evolve-skill, asks to evolve, optimize, improve, debug, or refine a skill, or after observing tool failures, user corrections, or sub-optimal agent trajectories. Don't use for ingesting domain documents into the Obsidian Vault (use ingest) or checking markdown frontmatter links (use vault-lint).
---

# 🧬 WikiSkill: Autonomous Agent Skill Evolution (`/wikiskill`)

> **Status**: Stable in v1.1+ (see `STABILITY.md`).

This skill implements the Google Research **WikiSkill** framework (Tang et al., 2026) to discover, compile, and evolve modular procedural skills (`SKILL.md`) using a **three-layer architecture**, **on-demand ReAct proposing**, and **asymmetric rollback gating**.

---

## 🚀 Triggers & Commands

- `/wikiskill <target_skill_or_tool>` or `/evolve-skill <target_skill>`
- Natural language triggers:
  - *"Evolve our ingest skill based on recent PDF runs"*
  - *"Optimize the google-antigravity-sdk skill to handle local models better"*
  - *"Refine our chrome-extensions skill after recent WebExtension errors"*
  - *"Improve skill based on the latest conversation trace"*

---

## 🏛 The 4-Agent Evolutionary Loop

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WIKISKILL 4-AGENT EVOLUTIONARY LOOP                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Trace Ingestion (Layer 1: Raw Traces)                                   │
│     Parse transcript.jsonl using analyze_trace.py to extract tool errors.   │
│                                │                                            │
│                                ▼                                            │
│  2. Wiki Compilation (Layer 2: Persistent Knowledge)                        │
│     Diagnose root causes & compile into ObsidianVault/wiki/patterns/*.md    │
│                                │                                            │
│                                ▼                                            │
│  3. ReAct Skill Proposer (Layer 3: Candidate Directives)                    │
│     Read wiki/index.md, impact ledger & fetch patterns on demand.           │
│     Draft minimal, atomic patch P_k for target SKILL.md.                   │
│                                │                                            │
│                                ▼                                            │
│  4. Validation Gating & Asymmetric Rollback                                 │
│     Run test tasks (Inference agent isolated from wiki).                   │
│     ├── IF PASS: Retain SKILL.md and log "Accepted" in skill-impact.md      │
│     └── IF FAIL: Roll back SKILL.md, but log "Rejected" in skill-impact.md  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Execution Workflow

### Step 1: Trace Ingestion & Diff-Only Proposals (`analyze_trace.py`)
1. Locate recent conversation transcripts in `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` or hook telemetry in `${XDG_STATE_HOME:-~/.local/state}/knowledge-compiler/logs/error_traces.jsonl`.
2. Run the trace analyzer to extract tool errors, user corrections, and structured diff-only candidate guardrails (written outside the vault under `$XDG_STATE_HOME/knowledge-compiler/proposals` with `0700`/`0600` permissions and secret redaction):
   ```bash
   python3 <plugin_dir>/skills/wikiskill/scripts/analyze_trace.py <path_to_transcript.jsonl> --propose --json
   ```
3. Inspect `latest_proposals.md` / `latest_proposals.json` to identify recurring error signatures, parameter schema violations, or procedural ambiguities.

### Step 2: Compile Pattern Dossier (`wiki/patterns/`)
1. Create or update a persistent pattern dossier at:
   `${OBSIDIAN_VAULT_PATH:-~/ObsidianVault}/wiki/patterns/<error_pattern_name>.md`
2. Include OKF v0.2 frontmatter:
   ```yaml
   ---
   title: "Pattern: Error or Strategy Name"
   type: concept
   tags:
     - skill-evolution/pattern
   status: stable
   sources:
     - "[[wiki/sources/...]]"
   aliases: []
   ---
   ```
3. Document:
   - **Observed Failure Trace**: Tool call arguments, error messages, and incorrect assumptions.
   - **Root Cause**: Why the model failed (missing flag, incorrect schema, context truncation).
   - **Corrective Strategy**: The verified, minimal procedural directive to prevent recurrence.

### Step 3: On-Demand Skill Proposing
1. Read the target skill (e.g. `<plugin_dir>/skills/<skill>/SKILL.md` or `.agents/skills/<skill>/SKILL.md`).
2. Read `${OBSIDIAN_VAULT_PATH:-~/ObsidianVault}/wiki/skill-impact.md` to review prior accepted and rejected proposals (avoiding previously failed approaches).
3. Draft a clean, atomic patch $P_k$ to a candidate copy of `SKILL.md` (never auto-mutating instruction files unattended).

### Step 4: Deterministic Validation Gating & Asymmetric Rollback (`vault-wikiskill-eval`)
1. Execute offline Asymmetric Rollback Evaluation against deterministic test cases:
   ```bash
   python3 <plugin_dir>/scripts/wikiskill_eval.py \
     --baseline-skill <baseline_SKILL.md> \
     --candidate-skill <candidate_SKILL.md> \
     --eval-suite <eval_suite.json> \
     --vault "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" \
     --apply-impact --json
   ```
2. **Failure Mode Isolation**: `wikiskill_eval.py` rejects candidate skills with invalid frontmatter, exceeded byte budgets, or `[[wiki/...]]` links inside `SKILL.md` (no background wiki cheating).
3. **Asymmetric Decision**:
   - **If `decision == "ACCEPTED"` (`exit 0`)**: Present the validated diff to the user for explicit approval before applying to the target `SKILL.md`; `--apply-impact` appends an `Accepted` ledger record to `wiki/skill-impact.md` via SHA-256 CAS.
   - **If `decision == "REJECTED"` (`exit 1`)**: Discard the candidate patch (keeping baseline $S_{k-1}$ intact). `--apply-impact` appends a `Rejected` entry to `wiki/skill-impact.md` with the diff and regression reason. **The wiki record is never rolled back**.

### Step 5: Update Master Index & Vault Log
1. Add new pattern notes to `${OBSIDIAN_VAULT_PATH:-~/ObsidianVault}/index.md`.
2. Append entry to `${OBSIDIAN_VAULT_PATH:-~/ObsidianVault}/log.md`:
   `## [YYYY-MM-DD] evolve | <Target Skill Name>`

---

## 📚 Reference Assets
- **Asymmetric Rollback Protocol**: [references/rollback_protocol.md](references/rollback_protocol.md)
- **Trace Analyzer**: [scripts/analyze_trace.py](scripts/analyze_trace.py)
