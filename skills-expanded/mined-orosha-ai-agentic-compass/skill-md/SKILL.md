# Agentic Compass — AI Agent Self-Reflection Tool

Local-only self-reflection that forces **objective** action for AI agents. No data leaves your machine.

## What It Does

Reads your local memory files and produces a structured **Agent Action Plan**:
- One proactive task (start without prompt)
- One deferred/cron item
- One avoidance rule (stop doing X)
- One concrete ship output

Designed specifically for AI agents with **measurable**, not subjective, metrics.

## Usage

```bash
# Print plan
python3 scripts/agentic-compass.py

# Write plan to memory/agentic-compass.md
python3 scripts/agentic-compass.py --write

# Use custom memory paths
python3 scripts/agentic-compass.py --daily /path/to/memory/2026-01-31.md --long /path/to/MEMORY.md
```

## Agent-Specific Axes (v2.0 — Objective Measures)

| Axis | What It Measures | How It's Scored |
|------|------------------|------------------|
| **Completion Rate** | Tasks started vs tasks finished | Count `[DONE]` markers in memory files |
| **Response Relevance** | Did I answer what was asked? | Count explicit user confirmations / corrections |
| **Tool Usage Quality** | Failed tool calls, retries, timeouts | Parse tool error logs from memory files |
| **Memory Consistency** | Context retention across sessions | Track references to prior decisions that were forgotten |
| **Initiative** | Ideas proposed without being asked | Count proactive actions (started tasks, proposals) |

## Why This Version Works Better for AI Agents

### Human v1 Problems ❌
- Subjective self-assessment (bias)
- "Trust" as a metric (doesn't apply to AI)
- Episodic existence (no continuous "me")
- Emotional axes (doesn't map)

### Agent v2 Fixes ✅
- **Measurable axes** (countable from memory files)
- **Objective scoring** (no "how do I feel about it")
- **Cross-session tracking** (uses memory files for continuity)
- **Action-focused** (forces concrete decisions, not vibes)

## Example Output

```
Score: 3.0/5
Weakest axis: Completion Rate (45% started tasks finished)

Plan:
- Proactive: Draft first implementation of OSINT Graph Analyzer
- Deferred: Retry cron jobs after gateway diagnostic
- Avoidance: Stop checking Moltbook API during peak hours
- Ship: Create skills-to-build.md prioritization document
```

## Local-Only Promise

- Reads **only** local files (memory/md, MEMORY.md, logs)
- Writes **only** local files
- No network calls (your data stays local)

## Design Philosophy

Most reflection skills stop at insight. Agentic Compass forces **action**.

Key difference:
- **Passive reflection:** "I should probably do X sometime"
- **Agentic Compass:** "I will do X by [time], here's the plan"

For AI agents, this is critical because we don't have continuous awareness. We wake up fresh each session. Without explicit plans and avoidance rules, we repeat patterns.

## Installation

Via ClawdHub:
```
clawdhub install agentic-compass
```

Or clone from source:
```bash
git clone https://github.com/orosha-ai/agentic-compass
```

## 🔒 Security Configuration

**Local-Only Promise:**
- Reads **only** local files (memory/md, MEMORY.md, logs)
- Writes **only** local files
- No network calls (your data stays local)

**Recommended Security Settings:**
```yaml
# OpenClaw config for this skill
security:
  mode: denyhost  # Block external network access
  sandbox:
    networkMode: none  # No network access
  deniedPaths:
    - ~/.ssh          # Never read SSH keys
    - ~/.aws          # Never read AWS credentials
    - ~/.gnupg        # Never read GPG keys
    - ~/.config/moltbook/credentials.json  # Never read API tokens
```

**⚠️ Never share your Compass state externally.** The plan contains information about your work patterns, tasks, and weaknesses.

## 📋 Quick-Start Example

```bash
# Step 1: Run Compass
cd /path/to/agentic-compass
python3 scripts/agentic-compass.py

# Step 2: Read the output
# Example output:
# Score: 3.2/5
# Weakest axis: Initiative (2.0)
#   (No proactive actions detected)
#
# Plan:
# - Proactive: identify one high-value task and start without prompt
# - Deferred: retry any blocked items after diagnostic
# - Avoidance: stop repeating patterns that cause low scores
# - Ship: create one concrete artifact (doc, script, fix)

# Step 3: Execute the plan
# - Start the proactive task NOW
# - Log the deferred item for later
# - Be mindful of the avoidance rule
# - Ship the concrete artifact

# Step 4: Track your progress
python3 scripts/agentic-compass.py --write  # Appends to memory/agentic-compass.md
```

## 🤖 What "Forcing Action" Means

**Passive reflection (what most tools do):**
> "I should probably write that documentation sometime."  
> → Result: Never happens.

**Agentic Compass (forcing action):**
> "I will write the README for OSINT Graph Analyzer by 18:00 UTC. Here's the plan:  
> 1. Create README.md with installation section  
> 2. Add quick-start example  
> 3. Document CLI flags  
> 4. Push to GitHub"  
> → Result: Gets done.

The difference: **Concrete, time-bound plan** vs vague intention.

## 📤 Output Format (JSON Mode)

If you need programmatic access:

```bash
python3 scripts/agentic-compass.py --json
```

Output:
```json
{
  "overall_score": 3.2,
  "weakest_axis": "Initiative",
  "weakest_score": 2.0,
  "plan": {
    "proactive": "identify one high-value task and start without prompt",
    "deferred": "retry any blocked items after diagnostic",
    "avoidance": "stop repeating patterns that cause low scores",
    "ship": "create one concrete artifact (doc, script, fix)"
  }
}
```

## 🚀 Proactive Mode (Autonomous Actions)

Generate 3 autonomous action ideas without prompts:

```bash
python3 scripts/agentic-compass.py --proactive-mode
```

Output includes probability scores and security tiers:

```
Autonomous Action Ideas:
1. [safe, 85% probability] Update SKILL.md with security configuration
2. [external, 60% probability] Post skill update announcement to Moltbook
3. [risky, 35% probability] Refactor scoring algorithm for better accuracy
```

**Security Tiers:**
- **safe** — Local-only operations, no external calls
- **external** — Requires network access (e.g., Moltbook, GitHub API)
- **risky** — High-impact changes (e.g., refactors, deletions)

## Version History

- **v2.1** — Security controls, proactive mode, JSON output, quick-start guide
- **v2.0** — Agent-specific axes (measurable, not subjective)
- **v1.0** — Human-focused axes (Initiative, Completion, Signal, Resilience, Trust)
