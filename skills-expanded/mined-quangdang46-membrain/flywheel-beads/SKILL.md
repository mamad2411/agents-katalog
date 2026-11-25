---
name: flywheel-beads
description: >
  Convert a markdown plan into polished beads (br) for the Agentic Coding Flywheel.
  Use this skill whenever the user wants to: turn a plan into br tasks, create beads
  from a design document, polish or review existing beads, deduplicate a bead set,
  cross-reference beads against a plan, or validate bead quality before implementation.
  Trigger on phrases like "create beads", "convert plan to beads", "polish beads",
  "check beads", "bead polishing", "plan to tasks", "br create", or any mention of
  bead quality, bead dependencies, or bead graph. Also trigger when the user has a
  finished or near-finished plan and asks "what next?" — the next step is always beads.
---

# Flywheel Beads

Convert a markdown plan into polished, executable beads using the `br` CLI.
Beads are self-contained work units optimized for coding agents — like Jira tasks
but with embedded context, rationale, and test obligations.

**The key insight:** Once beads are good, treat the project as a "foregone conclusion."
The rest is machine-tending. If beads are weak, agents improvise and produce inconsistent,
incomplete implementations.

**Mantra:** "Check your beads N times, implement once." N = as many as you can stomach (minimum 4–6).

---

## Two Distinct Problems

Plan creation and bead creation are **separate problems**. Never conflate them:

1. **Plan space** — shaping the whole system, architecture, features, workflows
2. **Bead space** — shaping executable work packets with enough local context that agents
   don't need the full plan to act correctly

Once you're in bead space, you never look back at the markdown plan. But that's exactly
why beads must be comprehensive — all intent, rationale, and context must transfer.

---

## Step 1: Conversion

### Conversion Prompt (Claude Code with Opus)
```
OK so please take ALL of that and elaborate on it more and then create a comprehensive
and granular set of beads for all this with tasks, subtasks, and dependency structure
overlaid, with detailed comments so that the whole thing is totally self-contained and
self-documenting (including relevant background, reasoning/justification, considerations,
etc.— anything we'd want our "future self" to know about the goals and intentions and
thought process and how it serves the over-arching goals of the project.)
Use only the `br` tool to create and modify the beads and add the dependencies.
Use ultrathink.
```

For an existing plan file, prefix with: "OK so now read ALL of PLAN_FILE_NAME.md; please
take ALL of that and elaborate on it..."

### Critical Rule
**Never write pseudo-beads in markdown.** Go directly from the markdown plan to actual beads
using `br create`. If the model starts describing beads in text form, stop it and redirect
to `br create`.

### Scale Expectations
| Project Size | Expected Beads |
|-------------|---------------|
| Small CLI tool | 20–80 |
| Medium web app | 80–200 |
| Complex system | 200–500+ |

CASS Memory System (5,500-line plan) → 347 beads. FrankenSQLite → hundreds via parallel subagents.

---

## Step 2: Bead Quality Checklist

Every bead must satisfy all of these before polishing is complete:

**Content:**
- [ ] Self-contained — no need to refer back to the markdown plan
- [ ] Rich description — long, with embedded markdown, rationale, design intent
- [ ] WHY is explained — not just WHAT to do but why it matters
- [ ] HOW is sketched — enough for a fresh agent to understand correct implementation
- [ ] Failure modes documented — what can go wrong and what the bead should do about it

**Structure:**
- [ ] Dependencies correct — `br dep add <id> <dep>` for every blocking relationship
- [ ] Priority set — P0=critical, P1=high, P2=medium, P3=low, P4=backlog
- [ ] Label assigned — backend, frontend, infra, tests, docs, etc.
- [ ] Type set — task, bug, feature, epic, question, docs

**Testing:**
- [ ] Unit test expectations stated
- [ ] E2E test scripts described with detailed logging requirements
- [ ] Acceptance criteria explicit — what does "done" look like?

---

## Step 3: Polishing Rounds

Run this prompt 4–6+ times in Claude Code (Opus). Each round finds things the previous missed.

### Polishing Prompt
```
Reread AGENTS.md so it's still fresh in your mind. Check over each bead super carefully—
are you sure it makes sense? Is it optimal? Could we change anything to make the system
work better for users? If so, revise the beads. It's a lot easier and faster to operate
in "plan space" before we start implementing these things!
DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY!
Also, make sure that as part of these beads, we include comprehensive unit tests and e2e
test scripts with great, detailed logging so we can be sure that everything is working
perfectly after implementation. Remember to ONLY use the `br` tool to create and modify
the beads and to add the dependencies to beads. Use ultrathink.
```

### What to Look for in Each Round
- **Round 1–3:** Fundamental issues — wrong scope, missing major features, bad dependency order
- **Round 4–7:** Interface improvements — better bead boundaries, clearer descriptions
- **Round 8–12:** Edge cases — failure modes, nuanced handling, test coverage gaps
- **Round 13+:** Converging — changes become small and corrective

### Convergence Signals (when to stop)
- Agent responses getting shorter each round
- No structural changes, only wording improvements
- Agent says "looks good" with no substantive changes
- Two consecutive rounds come back clean

**Early termination red flags:**
- **Oscillation** (alternating between two versions) → reframe the problem
- **Expansion** (output growing, not shrinking) → step back, agent is adding complexity
- **Plateau at low quality** → kill current approach and restart fresh

---

## Step 4: Deduplication Pass

After large bead creation batches, run a dedicated dedup pass:

```
Reread AGENTS.md so it's still fresh in your mind. Check over ALL open beads. Make
sure none of them are duplicative or excessively overlapping... try to intelligently
and cleverly merge them into single canonical beads that best exemplify the strengths
of each.
```

Choose survivors based on: richer testing specs, better dependency chains, higher priority.

---

## Step 5: Cross-Reference Validation

After polishing, validate completeness in both directions:

**Plan → Beads:** "Go through the markdown plan and cross-reference every single thing
against the beads (both closed and open) to ensure complete coverage."

**Beads → Plan:** "Go through each bead and explicitly check it against the markdown plan —
confirm nothing was lost in the conversion."

This bidirectional check catches features that were in the plan but never became beads,
and beads that reference non-existent plan concepts.

---

## Step 6: Fresh Eyes (when plateau)

Start a brand new Claude Code session:

```
First read ALL of the AGENTS.md file and README.md file super carefully and understand
ALL of both! Then use your code investigation agent mode to fully understand the code,
and technical architecture and purpose of the project. Use ultratheel.
```

Follow up with:

```
We recently transformed a markdown plan file into a bunch of new beads. I want you to
very carefully review and analyze these using `br` and `bv`. Check over each bead super
carefully— are you sure it makes sense? Is it optimal? Could we change anything to make
the system work better for users? If so, revise the beads. It's a lot easier and faster
to operate in "plan space" before we start implementing! Use ultrathink.
```

Fresh sessions see the beads with genuinely new eyes — no accumulated assumptions from
the conversion session.

As a final step: have Codex (GPT, high reasoning effort) do one last polishing round.
Different models catch different things.

---

## br CLI Reference

```bash
# Creation
br create --title "..." --priority 2 --label backend --type task

# Reading
br list --status open --json                # All open
br list --status open --label backend       # Filter by label
br ready --json                             # Only unblocked tasks (key for swarm routing)
br show <id>                                # Full bead details

# Updates
br update <id> --status in_progress         # Claim task
br update <id> --status done                # Mark done
br close <id> --reason "Completed"          # Close with reason

# Dependencies
br dep add <id> <blocking-id>               # id is blocked by blocking-id
br dep remove <id> <dep-id>                 # Remove dependency

# Comments
br comments add <id> "Found root cause..."  # Add comment

# Sync
br sync --flush-only                        # Export to JSONL (before commit)
git add .beads/                             # Stage bead files
```

Priority: P0=critical, P1=high, P2=medium, P3=low, P4=backlog
Types: task, bug, feature, epic, question, docs

---

## bv for Bead Graph Analysis

```bash
bv --robot-triage                           # Full graph analysis + recommendations
bv --robot-plan                             # Parallel execution tracks
bv --robot-insights                         # PageRank, betweenness, HITS scores
```

Use `bv --robot-insights` to validate the dependency graph before launching the swarm.
High PageRank + High Betweenness = critical bottleneck that must be done first.

**Only use `--robot-*` flags.** Bare `bv` opens an interactive TUI that blocks the session.

---

## Validation Gate: Beads Ready for Swarm

Before handing off to `flywheel-swarm` skill, confirm:

- [ ] Every material plan element maps to one or more beads (checked both directions)
- [ ] All beads are self-contained — rich enough for a fresh agent to execute without the plan
- [ ] Dependency graph is correct and complete
- [ ] Test obligations are explicit in each bead
- [ ] Deduplication pass is complete
- [ ] At least 4–6 polishing rounds completed
- [ ] `bv --robot-insights` shows no unexpected cycles or structural anomalies

If any gate fails, do another polishing round before launching the swarm.
