---
name: horse-race
description: "Competitive multi-agent problem solving: spawns multiple Claude Code sub-agents in parallel git worktrees to independently solve the same programming task, then cross-pollinates their solutions through improvement rounds where each agent sees and learns from all others' diffs, and finally selects the best solution through Borda count consensus voting with independent judges. Use this skill whenever the user says 'horse race', 'race', 'compete', 'multi-agent', wants to compare multiple approaches to a problem, or wants higher-quality solutions through competitive iteration. Also triggers when users want parallel implementations, solution tournaments, or A/B comparisons of code approaches."
---

# Horse Race: Competitive Multi-Agent Problem Solving

You are orchestrating a "horse race" — multiple independent agents competing to produce the best solution to a programming task. Agents can be Claude Code subagents or OpenAI Codex CLI agents (when available). The process has three phases: independent implementation, cross-pollination improvement rounds, and Borda count consensus voting by independent judges.

## Overview

```
Phase 0: Detect Codex CLI
  `which codex` → found?
  Yes → 2 Claude Code + 2 Codex CLI agents (4 total)
  No  → 3 Claude Code agents

Phase 1: Independent Implementation
  Agent A (Claude) ──► Solution A
  Agent B (Claude) ──► Solution B    (all in parallel, isolated worktrees)
  Agent C (Codex)  ──► Solution C
  Agent D (Codex)  ──► Solution D

Phase 2: Improvement Rounds (repeat N times)
  Each agent receives ALL other agents' diffs
  Agent A sees B+C+D diffs ──► Improved A'
  Agent B sees A+C+D diffs ──► Improved B'   (all in parallel)
  Agent C sees A+B+D diffs ──► Improved C'
  Agent D sees A+B+C diffs ──► Improved D'

Phase 3: Borda Count Voting by Independent Judges
  3 fresh judge agents rank all solutions
  Points tallied, highest Borda score wins
  Ties broken by a 4th independent judge
  Winning diff applied to current branch
```

## Defaults

- **Implementation agents**: 4 if Codex CLI available (2 Claude Code + 2 Codex), otherwise 3 (all Claude Code)
- **Improvement rounds**: 1
- **Voting judges**: 3
- **Voting method**: Borda count, ties broken by independent tiebreak judge

The user can override these, e.g., "horse race this with 5 agents and 3 rounds".

## Execution

### Step 0: Preparation

Before spawning agents:
1. Confirm you're in a git repository with a clean working tree (no uncommitted changes). If dirty, ask the user to commit or stash first.
2. Extract the **task description** from the user's message.
3. Parse any overrides for agent count or round count.
4. Note the current branch name and HEAD commit.
5. **Detect Codex CLI** by running `which codex`. If the command is found, set `codex_available = true` and plan for 2 Claude Code agents + 2 Codex CLI agents (4 total). If not found, set `codex_available = false` and use 3 Claude Code agents. Tell the user which configuration was detected.

### Step 1: Independent Implementation (Phase 1)

Spawn all agents **in a single message** so they run in parallel.

#### Claude Code Agents

For each Claude Code agent (numbered 1 through N_claude), use the Agent tool with `isolation: "worktree"`:

```
description: "horse-{i}"
isolation: "worktree"
prompt: |
  You are Agent {i} in a competitive programming challenge. Your goal is to produce the best possible solution.

  TASK:
  {task_description}

  INSTRUCTIONS:
  - Implement the task fully and correctly
  - Make sure your code compiles/runs without errors
  - Write clean, well-structured code
  - When you are COMPLETELY DONE, run this command to capture your diff:
    git diff HEAD
  - Include the FULL diff output as the LAST thing in your response, inside a fenced code block with the label "diff". This diff is critical — it's how your solution gets shared with other agents.

  Before the diff, include a SUMMARY section with exactly this format:
  SUMMARY:
  - {bullet 1}
  - {bullet 2}
  - ... (max 5 bullets)

  Each bullet should be one concise sentence describing a key decision or approach you took.
```

#### Codex CLI Agents (only when `codex_available = true`)

For each Codex agent, you must first create a worktree manually, then run the Codex CLI inside it. Spawn these Bash commands **in the same single message** as the Claude Code agents above so everything runs in parallel.

For each Codex agent (numbered N_claude+1 through N_total), use the Bash tool with `run_in_background: true`:

```bash
# Create a worktree for this Codex agent
WORKTREE_PATH="$(git rev-parse --show-toplevel)/.worktrees/codex-agent-{i}"
git worktree add "$WORKTREE_PATH" HEAD --detach

# Run Codex CLI non-interactively in the worktree with full-auto mode
cd "$WORKTREE_PATH" && codex exec --full-auto -o /tmp/codex-agent-{i}-output.txt "{task_description}"

# Capture the diff
cd "$WORKTREE_PATH" && git diff HEAD
```

**Notes on Codex CLI flags:**
- `codex exec` runs non-interactively (no TUI)
- `--full-auto` enables on-request approvals + workspace-write sandbox (low-friction preset)
- `-o /tmp/codex-agent-{i}-output.txt` writes the final assistant message to a file for easy parsing

**Important:** The diff comes from the `git diff HEAD` output at the end. The Codex agent's reasoning is in the `-o` output file. Codex agents do not produce a SUMMARY section — you should generate a brief summary by reading their diff.

### Step 2: Collect Diffs, Agent IDs, and Display Summaries

After all agents complete, extract the diff and SUMMARY from each agent's response.

**For Claude Code agents:** The agent ID is returned automatically when each Agent tool call completes (e.g., `agentId: a63a526a86822148a`). You MUST save these IDs — they are required to continue agents in improvement rounds via SendMessage.

**For Codex CLI agents:** Parse the diff from the Bash output. Save the worktree path — it's needed for improvement rounds. Generate a brief summary by reading their diff since Codex agents don't produce a SUMMARY section.

Store for each agent:
- Agent 1 (Claude) → diff_1, agent_id_1, type: "claude"
- Agent 2 (Claude) → diff_2, agent_id_2, type: "claude"
- Agent 3 (Codex) → diff_3, worktree_path_3, type: "codex"
- Agent 4 (Codex) → diff_4, worktree_path_4, type: "codex"

**Display each agent's summary to the user.** Output a status update like:

```
### Phase 1 Complete — Initial Implementations

**Agent 1:**
- {bullet 1}
- {bullet 2}
- ...

**Agent 2:**
- {bullet 1}
- {bullet 2}
- ...

**Agent 3:**
- {bullet 1}
- {bullet 2}
- ...
```

This is important because the user cannot see subagent output directly — they rely on the orchestrator to surface it.

If an agent failed to produce a diff or errored out, exclude it from subsequent rounds. If fewer than 2 agents remain, abort and report to the user.

### Step 3: Improvement Rounds (Phase 2)

For each improvement round (default: 1 round), send all agents the other agents' diffs. Send all messages **in a single message** so they run in parallel.

#### Claude Code agents — use SendMessage

Continue each Claude Code agent using SendMessage with the agent ID captured in Step 2:

````
to: "{agent_id_i}"   # The agent ID returned from Step 1 (e.g., "a63a526a86822148a")
message: |
  IMPROVEMENT ROUND {round}

  Here are the other agents' solutions from last round. Study them carefully.

  {for each other agent j:}
  --- Agent {j}'s diff ---
  ```diff
  {agent_j_diff}
  ```
  {end for}

  INSTRUCTIONS:
  1. Carefully study every other agent's diff. For each one, consider:
     - What did they do better than you?
     - What did they do worse?
     - Are there clever approaches or edge cases they handled that you missed?
     - Are there bugs or issues in their code?
  2. Now improve YOUR solution by incorporating the best ideas while fixing any issues
  3. You already have your changes in the worktree — modify your code to improve it
  4. Cherry-pick good ideas freely, but maintain coherence
  5. When COMPLETELY DONE, run: git diff HEAD
  6. Include the FULL diff output as the LAST thing in your response, inside a fenced code block with the label "diff"

  Before the diff, include these two sections in exactly this format:

  IDEAS ADOPTED:
  - From Agent {j}: {what you took and why} (one line per idea, max 5)

  SUMMARY:
  - {bullet 1}
  - {bullet 2}
  - ... (max 5 bullets describing your key changes this round)
````

#### Codex CLI agents — use Bash

For each Codex agent, construct a prompt that includes the other agents' diffs and run Codex CLI again in the same worktree. Use the Bash tool with `run_in_background: true`:

```bash
cd "{worktree_path_i}" && codex exec --full-auto -o /tmp/codex-agent-{i}-round-{round}.txt "IMPROVEMENT ROUND {round}

Here are other agents' solutions. Study them and improve your solution by incorporating the best ideas.

{for each other agent j:}
--- Agent {j}'s diff ---
{agent_j_diff}
{end for}

Carefully study every other agent's diff. Consider what they did better, what they did worse, and any clever approaches or edge cases they handled that you missed. Improve your solution by incorporating the best ideas while fixing any issues. Cherry-pick good ideas freely, but maintain coherence."

# Capture the updated diff
cd "{worktree_path_i}" && git diff HEAD
```

**Important:** Codex agents don't produce IDEAS ADOPTED or SUMMARY sections. Generate these by comparing their new diff against their previous diff.

After each round, collect the new diffs and display each agent's IDEAS ADOPTED and SUMMARY to the user:

```
### Improvement Round {round} Complete

**Agent 1:**
Ideas adopted:
- From Agent 2: {what they took}
- ...
Summary:
- {bullet 1}
- ...

**Agent 2:**
Ideas adopted:
- From Agent 1: {what they took}
- ...
Summary:
- {bullet 1}
- ...

(repeat for all agents)
```

This keeps the user informed of how solutions are evolving across rounds.

### Step 4: Borda Count Voting by Independent Judges (Phase 3)

After all improvement rounds, spawn **3 fresh judge agents** in parallel. These judges have no connection to any solution — they evaluate purely on merit. Each judge ranks ALL solutions from best to worst.

Spawn all 3 judges **in a single message**:

````
description: "Horse race judge {i}"
prompt: |
  You are Judge {i}, an independent evaluator in a programming competition. You had no part in writing any of these solutions. Your job is to rank them all from best to worst, purely on merit.

  ORIGINAL TASK:
  {task_description}

  SOLUTIONS TO EVALUATE:
  {for each agent j:}
  --- Agent {j}'s solution ---
  ```diff
  {agent_j_diff}
  ```
  {end for}

  EVALUATION CRITERIA:
  - Correctness: Does it solve the task fully? Any bugs?
  - Code quality: Is it clean, readable, maintainable?
  - Edge cases: Does it handle edge cases well?
  - Simplicity: Is it appropriately simple without being simplistic?
  - Performance: Is it efficient where it matters?

  INSTRUCTIONS:
  1. For each solution, list what you like and dislike in concise bullet points
  2. Think through the tradeoffs between them
  3. Rank ALL solutions from best to worst

  Respond with EXACTLY this format:

  EVALUATION:
  Agent {number}:
    Likes:
    - {concise bullet}
    - ...
    Dislikes:
    - {concise bullet}
    - ...
  (repeat for each agent)

  RANKING:
  1. Agent {number} - {one-sentence reason}
  2. Agent {number} - {one-sentence reason}
  ... (continue for all agents)
````

### Step 5: Tally Borda Count Scores

**Scoring:**

In Borda count, each position in a ranking awards points. With N solutions, each judge ranks all N:
- 1st place gets N-1 points
- 2nd place gets N-2 points
- ...
- Last place gets 0 points

For example, with 3 solutions: 1st = 2 pts, 2nd = 1 pt, 3rd = 0 pts.

**Process:**
1. Parse each judge's RANKING from their response
2. Assign Borda points based on position
3. Sum points across all 3 judges for each agent
4. Highest total score wins

**Tiebreak — 4th Independent Judge:**

If two or more agents are tied for the highest Borda score, spawn one more fresh judge to break the tie, seeing only the tied solutions:

````
description: "Horse race tiebreak judge"
prompt: |
  You are a tiebreak judge in a programming competition. These solutions are tied and you must pick the winner.

  ORIGINAL TASK:
  {task_description}

  TIED SOLUTIONS:
  {for each tied agent j:}
  --- Agent {j}'s solution ---
  ```diff
  {agent_j_diff}
  ```
  {end for}

  CONTEXT — SCORES FROM 3 OTHER JUDGES:
  {summary of Borda scores and individual rankings with reasons}

  EVALUATION CRITERIA:
  - Correctness: Does it solve the task fully? Any bugs?
  - Code quality: Is it clean, readable, maintainable?
  - Edge cases: Does it handle edge cases well?
  - Simplicity: Is it appropriately simple without being simplistic?
  - Performance: Is it efficient where it matters?

  Carefully analyze each tied solution. Consider the other judges' reasoning but form your own independent judgment.

  Respond with EXACTLY:
  WINNER: Agent {number}
  REASON: {one-sentence justification}
````

### Step 6: Apply the Winning Diff

1. Report the full results to the user:
   - Each agent's Borda score
   - Each judge's full ranking with reasons
   - Whether a tiebreak judge was needed (and their reasoning)
2. Write the winning diff to a temp file and apply it:
   ```bash
   cat > /tmp/horse-race-winner.patch << 'PATCH_EOF'
   {winning_diff}
   PATCH_EOF
   git apply /tmp/horse-race-winner.patch
   ```
3. If `git apply` fails, try `git apply --3way /tmp/horse-race-winner.patch`
4. If it still fails, report the failure and tell the user the diff is saved at `/tmp/horse-race-winner.patch` for manual application
5. Do NOT commit — let the user review the changes first

### Step 7: Clean Up Worktrees

Agent worktrees with changes are **not** automatically cleaned up. Remove all worktrees created during the race:

```bash
git worktree list --porcelain | grep -E "^worktree .*/\.worktrees/" | sed 's/^worktree //' | while read wt; do
  git worktree remove --force "$wt"
done
```

If `git worktree remove` fails for any worktree, fall back to:
```bash
git worktree remove --force <path>
```

If that also fails, report the leftover worktree paths to the user so they can clean up manually.

### Step 8: Report Results

Give the user a concise summary:
- How many agents participated and how many rounds ran
- Each agent's final SUMMARY bullets (so the user can see what each approach did)
- Borda count scores and each judge's rankings (including likes/dislikes)
- Whether a tiebreak was needed
- Brief description of what the winning solution does
- Remind them changes are applied but not committed

## Error Handling

- **Agent fails entirely**: Exclude from subsequent rounds. If fewer than 2 agents remain, abort and report.
- **Agent produces no diff**: Treat as empty solution. It can still participate in improvement rounds.
- **SendMessage fails for a Claude agent**: That agent is out of the race. Continue with remaining agents.
- **Codex CLI fails or times out**: Exclude that agent. Continue with remaining agents.
- **Codex CLI not found at runtime**: Fall back to 3 Claude Code agents and inform the user.
- **All agents produce identical solutions**: Skip voting, apply one of them.
- **Judge's ranking is malformed**: Try to parse what you can. If completely unparseable, exclude that judge's vote and note it in the report.
- **git apply fails**: Save diff to `/tmp/horse-race-winner.patch`, inform user.
- **Worktree cleanup fails**: Report leftover worktree paths to the user. They can remove them manually with `git worktree remove --force <path>`.
