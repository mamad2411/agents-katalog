# AuroraOps Framework Guide for AI Agents

**AuroraOps** is a tmux-based multi-agent engineering framework for autonomous and semi-autonomous software delivery. You may be deployed as part of a crewmate in Mission-Control, or you may be asked to work directly on one of the five component repos. This guide helps you be immediately productive.

---

## Framework Overview

AuroraOps consists of five integrated repos that form a layered delivery system:

| Repo | Role | Key Abstraction |
|------|------|-----------------|
| **Launchpad** | Environment | Worktree pool — agents grab warm, reusable git workspaces instantly |
| **Orbit** | Execution | Iteration loop — runs agents in bounded iterations with token accounting and working memory |
| **Checkpoint** | Quality | Pre-push pipeline — runs secrets, review, tests, docs, lint before code lands |
| **Mission-Control** | Orchestration | Fleet manager — one "First Mate" agent coordinates a crew of autonomous crewmates |
| **Lens** | Human Feedback | HTML annotation server — humans review artifacts, feedback becomes agent prompts |

**Data flow:**
```
Mission-Control (captain says: "add rate limiting")
    ↓
Mission-Control (dispatches crewmate with brief)
    ↓
Orbit (runs your agent on isolated worktree from Launchpad)
    ↓
You (iterate using notes.md working memory, emit events)
    ↓
Checkpoint (runs quality pipeline)
    ↓
[If pass] → push to origin + open PR
[If fail] → Orbit rolls back, retries
```

---

## Your Role Depends on Context

### Role 1: Crewmate (Dispatched by Mission-Control)

You are deployed via `orbit` inside a Mission-Control task. You receive:
- **Brief**: Task description in `BRIEF.md` (in the worktree root)
- **Budget**: Token limit in environment variable `TOKEN_BUDGET`
- **Memory**: Persistent `notes.md` file for working state
- **Working directory**: A clean git worktree in detached HEAD state

**Your objectives:**
1. Read `BRIEF.md` and `notes.md` (if it exists)
2. Make incremental progress, updating `notes.md` at each step
3. Commit successful work to the current detached HEAD
4. Output JSON status on the final line: `{"status": "success|failure", "summary": "...", "stop": true}`

**Token awareness:** Do NOT exceed `$TOKEN_BUDGET`. Orbit will stop you if budget is exhausted. Update `notes.md` with token tracking.

**Example working loop (pseudocode):**
```bash
# You are in a worktree managed by Orbit
cat BRIEF.md        # Task description
cat notes.md        # Working memory (empty on first iteration)

# Make progress, track it
echo "## Active Plan
- [ ] Step 1: understand the codebase
- [ ] Step 2: implement feature
- [x] Step 3: test
" >> notes.md

# Commit
git add -A && git commit -m "step 2: implement feature"

# Final output (Orbit parses this)
echo '{"status": "success", "summary": "Rate limiter added to POST /login", "stop": true}'
```

### Role 2: Direct Contributor (Asked to modify a single repo)

You are asked to work directly on Launchpad, Orbit, Checkpoint, Mission-Control, or Lens. In this case:
- Read the relevant component's README.md
- Understand the CLI interface and internal structure
- Make changes in a feature branch
- Checkpoint will validate via its pipeline before PR

**Example:** "Add caching to Checkpoint stage 1 review output"
→ You modify `Checkpoint/lib/*.sh` or `Checkpoint/checkpoint` → Create PR

### Role 3: First Mate (Mission-Control's Lead Agent)

You manage the crew on behalf of the captain. This is a supervisory role, NOT coding.
- Dispatch crewmates with `bin/mc-spawn.sh`
- Monitor fleet status with `bin/mc-status.sh`
- Handle wake events: task completion, budget alerts, blockers
- Escalate to captain when human decision is needed

See [Mission-Control/AGENTS.md](Mission-Control/AGENTS.md) for full First Mate charter.

---

## Key Files & Conventions

### Shared Across All Repos

| File | Purpose | Managed by |
|------|---------|-----------|
| `README.md` | Entry point and quick start | Humans |
| `lib/events.sh` | Event emission shared library | Framework |
| Hooks (in Launchpad, Checkpoint) | Extensibility points | Humans |

### Working Memory (Orbit + Mission-Control)

- **`notes.md`** (in worktree) — Your persistent iteration log. Update it after each step.
  ```markdown
  ## Budget
  - token_budget: 50000
  - tokens_used: 2300
  - iterations_completed: 3
  
  ## Active Plan
  - [ ] Refactor user service
  - [x] Add rate limiting
  
  ## Completed Steps
  - Added middleware to POST /login
  - Configured 5 req/min per IP
  ```
- **`data/knowledge.md`** (Mission-Control) — Architectural decisions, constraints, ambiguities. Read before ship tasks.
- **`data/tasks.md`** (Mission-Control) — Project registry and task tracking.

### Event Log (All Repos)

- **`~/.auroraops/events.jsonl`** — Append-only structured log.
  ```json
  {"ts":"2026-06-23T14:30:00Z","type":"orbit.iteration.complete","session":"1750000000-12345","payload":{"iteration":2,"tokens_used":1200}}
  ```
- Emit events with: `emit_event "event.type" '{"key":"value"}'`

### Branch Naming (Orbit)

- Orbit creates branches automatically: `orbit/<slug>-<timestamp>`
- Example: `orbit/rate-limiter-1719123456`
- Checkpoint pushes to origin with auto-opening PR via `gh pr create`

---

## Common Tasks as an Agent

### Task: Add a Feature (Crewmate)

1. **Read brief and context:**
   ```bash
   cat BRIEF.md
   cat notes.md || echo "# First iteration"
   git log --oneline -5      # Recent commits
   ```

2. **Understand the codebase:**
   ```bash
   find . -name "*.md" | head -5   # Docs
   ls -la                           # Structure
   cat package.json 2>/dev/null || cat pom.xml 2>/dev/null  # Language/stack
   ```

3. **Plan incrementally:**
   ```bash
   cat > notes.md <<'EOF'
   ## Budget
   - token_budget: $TOKEN_BUDGET
   - tokens_used: 0
   
   ## Active Plan
   - [ ] Understand POST /login flow
   - [ ] Add rate-limit middleware
   - [ ] Add unit tests
   - [ ] Document in README
   EOF
   ```

4. **Implement one step at a time:**
   - Make change
   - Test locally
   - Commit with message tied to plan
   - Update `notes.md`
   - Check token usage

5. **Final commit:**
   ```bash
   git add -A && git commit -m "Rate limiter: 5 req/min per IP on POST /login"
   echo '{"status": "success", "summary": "Rate limiting added and tested", "stop": true}'
   ```

### Task: Fix a Broken Test (Crewmate)

1. Identify the failing test: `grep -r "test.*name" . --include="*.test.js" --include="*.test.ts"`
2. Run it locally to see the error
3. Trace the error to root cause (often a missing file, import, or API change)
4. Fix and verify: `npm test` or equivalent
5. Commit and report

### Task: Modify a Component (Direct Contributor)

1. **Clone and explore:**
   ```bash
   cd AuroraOps/Checkpoint
   ls -la
   cat README.md
   git log --oneline -5
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b enhancement/add-custom-stage
   ```

3. **Make changes** (typically shell scripts or Node.js files)

4. **Test locally** (if applicable):
   ```bash
   # Example: Checkpoint allows direct invocation
   ./checkpoint run my-feature-branch
   ```

5. **Commit and push:**
   ```bash
   git add -A && git commit -m "Add custom stage hook support"
   git push origin enhancement/add-custom-stage
   ```

6. **Checkpoint validates** (if you have Checkpoint in place) or create manual PR

### Task: Review Checkpoint Output (Crewmate)

After Checkpoint runs, it may generate output. Check:
- `.checkpoint-status/<branch>.md` — Last run status and errors
- `.checkpoint-cache/<commit-sha>/` — Stage outputs (if cached)
- `stdout/stderr` from `checkpoint run` command

---

## Environment & Tools

### Required

- `bash` / `zsh` (shell scripting)
- `git` (version control)
- `tmux` (session multiplexing, for Mission-Control)
- `node >=18` (Lens only, if you're working on Lens)
- One agent CLI: `claude` (Anthropic), `copilot` (GitHub), `codex` (OpenAI), or `opencode` (SST)

### Recommended

- `gh` (GitHub CLI, for PR creation via Checkpoint)
- `jq` (JSON querying, for event parsing)
- `detect-secrets` (for Checkpoint stage 0)

### Check Environment

```bash
# If you're a crewmate:
echo "Budget: $TOKEN_BUDGET"
echo "Session: $AURORAOPS_SESSION_ID"
pwd                 # Should be a Launchpad worktree
git status          # Should be in a detached HEAD
```

---

## Failure Modes & Recovery

### Symptom: "Git worktree locked"
**Cause:** Another task is using the same slot.
**Recovery:** Orbit will retry with a different slot. Wait.

### Symptom: "Token budget exceeded"
**Cause:** Your iterations used more tokens than budgeted.
**Recovery:** Orbit stops and rolls back. This is intentional to control costs.

### Symptom: "Checkpoint rejected: lint failed"
**Cause:** Your code violates lint rules (e.g., `shellcheck` for shell, or eslint for JS).
**Recovery:** Orbit rolls back and retries. Fix the lint error in the next iteration.

### Symptom: "Stage 0 secrets detection blocked push"
**Cause:** Your code contains API keys, passwords, or credentials.
**Recovery:** Remove the secret, update `.gitignore` if needed, commit again. Checkpoint will re-run.

### Symptom: "Test suite failed in Checkpoint"
**Cause:** Your changes broke a test.
**Recovery:** Orbit rolls back. Next iteration, check which test failed and fix it.

---

## Advanced: Wiring Into Your Own Workflow

### Emit a Custom Event

```bash
# Example: You completed a major milestone
emit_event "task.milestone.reached" '{"milestone":"schema-migration","duration_seconds":3600}'
```

### Read the Event Log

```bash
cat ~/.auroraops/events.jsonl | jq '.payload | select(.iteration >= 5)'
```

### Access Mission-Control Knowledge Board

If deployed by Mission-Control:
```bash
cat KNOWLEDGE.md    # Copied into worktree before task starts
# Contains: architectural decisions, constraints, ambiguities
```

### Coordinate with Sibling Tasks

All tasks in a session share `AURORAOPS_SESSION_ID`. Use it in event payloads or custom scripts to correlate work.

---

## Quick Reference

### Commands by Role

| Role | Command | What it does |
|------|---------|-------------|
| First Mate | `MC_HOME="..." bin/mc-spawn.sh task-001` | Dispatch a crewmate |
| Crewmate | `echo '{"status": "success", "stop": true}'` | Signal completion (last line of output) |
| Contributor | `git push origin feature-branch` | Create PR via Checkpoint |
| All | `emit_event "type" '{"data":"value"}'` | Log an event |

### File Locations

| File | Location | Access |
|------|----------|--------|
| Working memory | `./notes.md` | Read/write in iterations |
| Task brief | `./BRIEF.md` | Read-only, provided by Mission-Control |
| Framework knowledge | `KNOWLEDGE.md` (if in worktree) | Read-only, provided by Mission-Control |
| Token budget | `$TOKEN_BUDGET` env var | Read at start of session |
| Session ID | `$AURORAOPS_SESSION_ID` env var | Read for event correlation |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (if used in a script) |
| 1 | Failure (Orbit will roll back and retry) |
| 2+ | Error (Orbit may escalate to First Mate) |

---

## Links

- [README.md](README.md) — Framework overview and quick start
- [AuroraOps_framework_documentation.md](AuroraOps_framework_documentation.md) — Deep technical manual
- [Mission-Control/AGENTS.md](Mission-Control/AGENTS.md) — First Mate charter
- [Launchpad/README.md](Launchpad/README.md) — Worktree pool details
- [Orbit/README.md](Orbit/README.md) — Iteration loop details
- [Checkpoint/README.md](Checkpoint/README.md) — Quality pipeline details
- [Lens/README.md](Lens/README.md) — Annotation server details

---

## Questions?

If deployed by Mission-Control, check `KNOWLEDGE.md` or ask the First Mate. If working directly on a repo, start with the component's `README.md`.

