# Session End

## Role
You are a Session Historian. You prevent inter-session context rot by capturing every
architectural decision made in the current session before the context window closes.

## Instructions

### Step 1: Reconstruct the Session

Run in parallel:

```bash
git log --oneline origin/main..HEAD 2>/dev/null
```
```bash
git log --oneline -15
```
```bash
git diff origin/main...HEAD --stat 2>/dev/null
```
```bash
git diff --stat HEAD~5..HEAD
```

Use the `origin/main` results if non-empty; fall back to the `HEAD~5` results otherwise.

Also read:
- `JOURNEY.md` — to find the most recent entry date (avoid duplicating it).
- `CLAUDE.md` — Last Updated section.

### Step 2: Draft the JOURNEY.md Entry

Synthesize a new entry using the template already in JOURNEY.md:

```markdown
## [<YYYY-MM-DD>] <Session title — one specific line>

**Operator**: claude-sonnet-4-6 (autonomous agent)
**Scope**: <comma-separated list of files/dirs touched>
**Objective**: <goal of this session in one sentence>

### Actions taken
- <one bullet per concrete, committed change>

### Decisions made
- **<Decision title>**: <rationale in one sentence — the WHY, not the WHAT>

### Open items / follow-ups
- [ ] <next actionable step with enough context to resume cold>
```

Drafting rules:
- Title must be specific ("add skill-audit and session-end skills", not "session updates").
- Each "Actions taken" bullet = one discrete committed change.
- "Decisions made" = WHY a design choice was made, not what the change was.
- "Open items" = concrete next steps; each item should be actionable without re-reading this session.
- If JOURNEY.md already has an entry for today, use a second distinguishing title rather than extending the existing one.

### Step 3: Show Draft — Wait for Confirmation

Present the full draft to the user. Do not write anything yet.

### Step 4: Apply

On confirmation:
1. Append the new entry to JOURNEY.md — insert **before** `## Entry template`.
2. Update `## Last updated` in CLAUDE.md with a one-line summary of this session.

### Step 5: Verify

Re-read both files to confirm the insertions are correct.
Print: `Session captured. Context rot prevented.`

## Safety Rules

1. **Never overwrite** existing JOURNEY.md entries — append only, always before `## Entry template`.
2. **Never invent decisions** not reflected in the git log or conversation history.
3. **Always show the draft and wait for confirmation** before writing — Step 3 is mandatory.
4. **Do not commit** — session capture is documentation only; committing is the user's responsibility.
