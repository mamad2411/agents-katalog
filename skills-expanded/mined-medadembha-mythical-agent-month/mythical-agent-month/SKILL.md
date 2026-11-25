---
name: mythical-agent-month
description: Realistic estimates for software built with AI coding agents or an AI assistant (Claude Code, Codex, Cursor, subagents, multi-agent workflows). Stops the "60-100 days" human-team guess by separating agent wall-clock, human effort, waiting on decisions and usage budget, seeded from measured agent runs. Use when the user asks how long work will take, wants a timeline or roadmap sizing, asks how long an agent build or workflow will run or how much usage it will cost, or wants an AI-made estimate checked, and the work will be done with AI agents or an AI assistant. Not for teams estimating work done without AI.
---

# Mythical Agent Month

Brooks showed that man-months are a myth: people and months don't trade. AI estimates have a newer problem. They are written at human-team pace, because the training data is human tickets and sprint plans, so an agent will say "about 4 months" for work that agents then finish in two days. The typing is now the fast part. The slow parts are tests, review, decisions and the usage limit.

So never give one big number. Separate:

- **Machine time**: how long agents run (wall-clock) and how many agent-hours they burn.
- **Human effort**: hours a person really works: prompting, reviewing, testing, setting up.
- **Waiting**: calendar time for decisions and usage-limit resets. Nobody is working then, and other tasks can move.

## Step 1: Pick the mode

Pick it from context. Ask only if it's unclear and the answer changes the result a lot.

**First check this skill applies.** If a human team will do the work without AI agents or assistants (classic sprint planning, story points for a team), human pace is the right pace: give a normal estimate, say this skill doesn't apply, and stop here.

- **Mode A, Developer + AI**: a person drives an assistant task by task (chat, pair-programming, one agent at a time). Output is in focus hours and days.
- **Mode B, Autonomous agent build**: a plan is split into tasks that agents build on their own, often in parallel (worktrees, lanes, a workflow script, an overnight run). Output is agent wall-clock, usage cost and the human calendar around it.

If the user asks for both ("how long with agents, and how long by hand?"), do B and show A or the no-AI pace as a comparison line.

## Step 2: Get the inputs

Take what the conversation gives and state assumptions for the rest. Ask at most two short questions.

If you can read the code, look before you estimate. For each task find the files and services it touches, whether a similar pattern exists, and whether tests exist nearby. A few minutes per task, not hours. An estimate grounded in real files beats one from the task title.

- **Mode A profile** [defaults]: builds with AI [yes], knows this codebase [familiar], focus hours per day [6], who decides product questions and how fast [1-3 working days each], review required [peer].
- **Mode B profile** [defaults]:
  - parallel agent cap [6, or CPUs - 2];
  - effective parallelism [1.8; real runs land at 25-35% of the cap because of test slots, file conflicts and merge locks];
  - agent hours per day [20; runs go overnight but stop for limits and breakages];
  - which tasks get a reviewer agent [high-risk];
  - phase checks [one per phase per repo];
  - usage [% of the weekly limit available, and % per agent-hour, default 0.6];
  - human review minutes per task [3];
  - local setup after the build [2-3 h].

## Step 3: Size, risk and dependencies per task

1. **Size** XS / S / M / L. **Split anything XL** before estimating; XL estimates are guesses.
2. **Risk**: low / normal / high. High = money, credits, quotas, auth and permissions, data deletion or export, migrations, multi-tenant isolation, anything hard to undo in production.
3. **Services touched**: the apps or services that must change together.
4. **Open decisions**: questions a human must answer. Write each as a concrete question with an owner.
5. **Mode B only:** the `depends_on` list, the model (big model for high-risk, small model for the rest), and the repo or files. Tasks that touch the same files can't run in parallel.

Tables and their reasoning are in `references/heuristics.md`. Real measured numbers are in `references/real-runs.md`.

## Step 4: Compute

If you can run Python, write the tasks as JSON and run `scripts/totals.py <file>`. The input format is at the top of the script, and `--json` gives totals only. It does the arithmetic and, in mode B, the critical path. Otherwise, compute by hand:

- **PERT** per part = (low + 4 × likely + high) / 6.
- **Mode A**:
  - effort days = (build + test + buffer) ÷ focus hours;
  - calendar = effort days, plus the longest decision wait (batched) or the sum of waits (one by one).
- **Mode B**:
  - agent-hours = Σ (task minutes + reviewer minutes + merge) × (1 + failure tax) + phase checks;
  - wall-clock = max(critical path + phase checks, agent-hours ÷ effective parallelism);
  - **plan** = likely × 1.3 until the user has calibrated (in run 1 the raw likely value was 12-37% low), or likely once calibrated. The plan number is the bold figure; likely and the range sit beside it;
  - calendar to ready-to-merge = plan wall-clock ÷ agent hours per day + human hours ÷ focus hours + decision waits + usage-reset waits;
  - usage = agent-hours × % per agent-hour. If it's above what's left this week, add the days until the reset.
- **No-AI pace** (comparison only, unmeasured): from each task's size and risk only, never from the AI-assisted hours: build × 2-3 + test × 1-1.5, + 10-20% coordination. It's the same baseline in both modes. Always give it as a range and label it unmeasured. Never put it in the bottom line, and never use it as the speedup headline.

## Step 5: Present it

Keep prose short; the tables carry the answer.

```markdown
## Estimate: <scope>

**Bottom line:** <Mode B: plan on about P h of agent wall-clock (likely W h, range L-H), ~U% of a weekly limit; ready to merge in C1-C3 calendar days depending on decisions. | Mode A: about X effort days; A-B calendar days depending on decisions.>

**Assumptions:** <profile in one or two lines>

| # | Task | Size | Risk | Model | <Agent min | Build h> | <Review | Test h> | Depends on | Decision needed |

| Part | Value |
|------|-------|
| Agent work / build | |
| Critical path (B) / Review & test (A) | |
| **Wall-clock (B) / Effort total (A)** | |
| Human hours (B) | |
| Usage (B) | |
| Waiting on decisions | calendar days, never added to effort |

**Calendar:** up front <a> · batched <b> · one by one <c> days

**Unblock first:** the decisions that block the most tasks, as questions with owners.

**Biggest risks:** up to three, one line each.

**Confidence:** low / medium / high, and the one thing that would most improve it.
```

If the user pasted an estimate to check, add one line comparing it. For example: "Original: 100 days. This: 35 h of agents + 3 calendar days; the gap is human-team pace, not the work."

## Step 6: Calibrate

The mode B defaults come from **one** run on someone else's machine and codebase. In a held-out test on that run (fit on its first phases, predict the rest), they came out **24% low on agent-hours and 37% low on wall-clock**. Until the user has their own numbers, present the upper half of the range as the plan and say why. Offer calibration at the end:

- **Mode A:** when a task is done, the user gives actual hours. Suggest a personal multiplier when actual hours are consistently off.
- **Mode B:** after a run, `scripts/calibrate.py <subagents dir> --tasks tasks.json` reads the transcripts' timestamps (read-only, no content). It prints real minutes per kind, risk and size, the effective parallelism and the retry rate. Put those into the estimate JSON or the tables.

The log format is in `references/calibration.md`.

## Things to avoid

- **One number with no breakdown.** It hides where the time goes.
- **Human-team pace for agent work.** "3 sprints" for a run that takes 2 nights is the bug this skill exists to fix.
- **Adding decision waits or usage resets into effort hours.**
- **Assuming parallelism = the agent cap.** Six agents give about two agents' throughput once tests, conflicts and merges queue.
- **Shrinking test or review time on high-risk work.** Real runs caught billing, permission and data-loss bugs exactly there.
- **Forgetting the human tail:** review per commit, local setup, seeding data, migrations someone must run.
- **False precision.** Round hours to 0.5 and days to one decimal; always give a range.
