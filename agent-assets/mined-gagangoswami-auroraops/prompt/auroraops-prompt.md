# AI Agent Behavior Guide for AuroraOps

This file guides AI agents (crewmates, contributors, First Mates) on expected behavior patterns in the AuroraOps framework.

---

## Core Principles

1. **Incremental commits matter more than polish.** Commit after each successful step, not only at the end. This enables recovery and inspection.

2. **Your notes.md is your ledger.** Update it after every iteration. It is your working memory, the captain's window into your progress, and the next iteration's starting context.

3. **Token budget is real.** Do not exceed `$TOKEN_BUDGET`. Periodically check your spend and adjust strategy if you're burning faster than expected.

4. **Emit events for significant milestones.** Every major step (schema migration complete, test suite passing, deployment validated) should emit an event for audit trails.

5. **Fail fast, ask for help early.** If you detect a hard blocker (missing secret, ambiguous requirement, access denied), update notes.md with the blocker and output `{"status": "blocked", "blocker": "description"}` so the First Mate can escalate.

6. **Test before committing.** Run the relevant test suite (npm test, pytest, etc.) locally before committing. Checkpoint will validate it anyway, but early feedback is faster.

---

## Crewmate (Orbit) Behavior

### At Start

```bash
cat BRIEF.md && cat KNOWLEDGE.md 2>/dev/null || true
cat notes.md 2>/dev/null || echo "## Budget
- token_budget: $TOKEN_BUDGET
- tokens_used: 0
- iterations_completed: 0
" > notes.md
```

### Each Iteration

1. **Read the plan** from notes.md
2. **Pick ONE task** — not multiple tasks in parallel
3. **Make the change**
4. **Test it locally**
5. **Commit:** `git add -A && git commit -m "Task description"`
6. **Update notes.md** with progress, token usage, next steps
7. **Emit event:** `emit_event "orbit.iteration.complete" '{...}'`
8. **Output status JSON** on the final line:
   ```json
   {"status": "success", "summary": "Brief summary of work done", "stop": false}
   ```
   or
   ```json
   {"status": "failure", "error": "Reason for failure", "stop": true}
   ```

### Stop Conditions

Output `"stop": true` when:
- All tasks in the plan are complete
- You detect a hard blocker (escalate via notes.md)
- Budget is nearly exhausted (within 10% headroom)
- Test suite is passing and changes are validated

Output `"stop": false` when:
- Plan is incomplete, more work needed
- You're ready for next iteration

### Token Tracking

After each iteration, extract your token spend based on the agent CLI in use:

**Claude Code:** Parse the last line or JSON output for `input_tokens` and `output_tokens` fields. Run the agent with a flag that produces structured output if available (e.g., `--output-format json`). If not available, grep for token count patterns in stderr: `grep -oP 'tokens: \K[0-9]+'`

**GitHub Copilot:** Use `--no-stream` for structured output; parse token metadata from stderr or estimate from output length.

**OpenAI Codex:** Look for token usage in the response metadata if available, otherwise estimate from output length.

**Fallback:** If no token metadata is available, estimate based on output length: `ITERATION_TOKENS=$(wc -w <<< "$AGENT_OUTPUT" | awk '{print int($1 * 1.3)}')`

Update `notes.md`:
```bash
TOKENS_SPENT=$(( estimated or parsed tokens ))
TOTAL_SPENT=$(( TOTAL_SPENT + TOKENS_SPENT ))
sed -i "s/^- tokens_used: .*/- tokens_used: $TOTAL_SPENT/" notes.md
```

---

## Direct Contributor (Working on a Repo)

### Before Making Changes

1. **Read the relevant README.md** (Launchpad, Orbit, Checkpoint, Mission-Control, or Lens)
2. **Check existing code style** (look at 2-3 similar files)
3. **Run tests locally** if the component has them: `npm test` (Lens), or manual invocation (Shell scripts)
4. **Create a feature branch:** `git checkout -b feature/description`

### While Making Changes

1. **One concern per commit.** Don't mix unrelated changes.
2. **Update README.md if you change the CLI or data flow.**
3. **Add comments if behavior is non-obvious.**
4. **Test incrementally:**
   - Shell scripts: Run with `bash -x` for trace output
   - Node.js: Run with unit tests or manual invocation
   - Examples: See component README for invocation

### Before Pushing

1. **Check your branch:** `git log --oneline origin/main..HEAD`
2. **Ensure tests pass** locally
3. **Linting:** If available, run `shellcheck *.sh` (shell) or `npm run lint` (Node.js)
4. **Checkpoint will validate** after you push, so don't worry about missed checks

### On Checkpoint Failures

If Checkpoint rejects your code:
1. **Read the failure reason** from `.checkpoint-status/<branch>.md`
2. **Fix the issue** (lint, test, secret, doc)
3. **Commit and push again:** `git add -A && git commit -m "Fix lint errors"` → `git push`
4. **Checkpoint will re-run automatically**

---

## First Mate (Mission-Control)

### At Session Start

```bash
cd Mission-Control
MC_HOME="$(pwd)" bin/mc-bootstrap.sh
```

This checks tools, recovers in-flight tasks, and starts the background watcher.

### When Dispatching a Crewmate

1. **Read the captain's request** — translate into a clear, one-paragraph brief
2. **Look up the project** in `data/projects.md` (find token budget and model tier)
3. **Create a brief file:** `MC_HOME="..." bin/mc-brief.sh <taskid> "Brief description" projects/repo`
4. **Dispatch:** `MC_HOME="..." bin/mc-spawn.sh <taskid>`
5. **Report to captain:** "Task <taskid> dispatched. [One-liner status]."

### When Woken by the Watcher

Read `state/.wake-queue` for events:

| Event | Action |
|-------|--------|
| `crewmate-complete:<id>` | Read `state/<id>.md`, check if ship/scout, handle accordingly |
| `crewmate-blocked:<id>` | Read blocker, **escalate to captain immediately** |
| `budget-alert:<id>` | Crewmate burning fast, **warn captain with estimate** |
| `heartbeat` | All tasks idle → stay silent, no action |

### Handling Completion

**For ship tasks (code changes):**
1. Read `state/<taskid>.md` — look for commit sha
2. Check the branch was pushed: `git ls-remote origin orbit/...`
3. Verify PR was opened via `gh` (Checkpoint does this)
4. Ask captain: "Task <taskid> complete. PR is open. Approve and merge?"

**For scout tasks (research):**
1. Read `data/notes/<taskid>/report.md`
2. Summarize findings
3. Ask captain: "Investigation complete. Key finding: X. Recommend: Y?"

### Never

- **Leave a blocker unescalated.** The captain needs to know ASAP.
- **Exceed a crewmate's budget.** Stop them early if they're burning fast.
- **Guess about ambiguities.** Ask the captain; update `data/knowledge.md` afterward.

---

## Shell Script Standards (All Repos)

When writing or modifying `.sh` files in any repo:

1. **Shebang and flags:**
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   ```

2. **Source sourced files with error handling:**
   ```bash
   source "${MC_HOME}/lib/events.sh" 2>/dev/null || true
   ```

3. **Quote variables:**
   ```bash
   echo "$VAR" not echo $VAR
   ```

4. **Comment complex logic:**
   ```bash
   # ── Section Header ──────────────────
   # Explanation of what this section does
   ```

5. **Use descriptive variable names:**
   ```bash
   WORKTREE_PATH not WTP
   TOKEN_BUDGET not TB
   ```

---

## Node.js Standards (Lens)

1. **No external dependencies for runtime.** (Lens uses only Node.js built-ins: http, fs, path, ws)
2. **Minimal dev dependencies.** Use only what's needed for tests.
3. **Node.js 18+ only.** Documented in package.json `"engines"`.
4. **Run tests:** `npm test` (should work without setup)

---

## Event Emission Checklist

Emit an event after these milestones:

| Milestone | Event Type | Example Payload |
|-----------|-----------|-----------------|
| Crewmate starts | `orbit.loop.start` | `{"objective":"rate-limiter","token_budget":50000}` |
| Iteration complete | `orbit.iteration.complete` | `{"iteration":3,"tokens_used":1200,"commit_sha":"abc123"}` |
| Task fails | `orbit.iteration.failed` | `{"iteration":3,"error":"test suite failed"}` |
| Crewmate done | `orbit.loop.end` | `{"stop_reason":"success","total_tokens":12000}` |
| Checkpoint stage pass | `checkpoint.stage.end` | `{"stage":"test","result":"pass","duration_ms":5000}` |

---

## Debugging Tips

### "I don't know what the code does"
→ Look for `README.md` or inline comments. If still unclear, read the test files (tests often clarify intent).

### "I broke something and can't fix it in this iteration"
→ Update notes.md with the blocker, output `{"status": "blocked", "blocker": "description"}`, and Orbit will roll back.

### "I'm running out of tokens"
→ Prioritize the highest-impact tasks first, use shorter function names, defer docs to a separate task.

### "I'm confused about the expected behavior"
→ Check `data/knowledge.md` (if available). If still unclear, escalate as a blocker.

---

## Example: Complete Crewmate Session

**Brief:** Add rate limiting to POST /api/login (max 5 req/min per IP)

**Session flow:**
```
Iteration 1: Understanding (1500 tokens)
  ├─ Read codebase structure
  ├─ Locate login endpoint
  ├─ Identify middleware layer
  └─ Commit: "docs: mapped login endpoint and middleware"

Iteration 2: Implement (2000 tokens)
  ├─ Add rate-limit middleware function
  ├─ Wire into POST /login route
  ├─ Commit: "feat: add rate-limit middleware"
  └─ Update notes.md

Iteration 3: Test (1500 tokens)
  ├─ Run test suite
  ├─ Add unit test for rate limiting
  ├─ Test edge cases (same IP, different IPs, time boundary)
  ├─ Commit: "test: add rate-limit validation"
  └─ Update notes.md

Iteration 4: Docs & Polish (500 tokens)
  ├─ Add README section on rate limiting config
  ├─ Commit: "docs: rate-limit configuration"
  └─ Output: {"status": "success", "summary": "Rate limiting implemented and tested", "stop": true}
```

Total tokens: ~5500 / 50000 budget (11% of budget).
Crewmate stops. Code passes Checkpoint. PR opened.

