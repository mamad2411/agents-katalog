---
name: self-check
description: Periodic self-check — reflect on alignment, progress, and quality. Use with /loop for continuous monitoring.
disable-model-invocation: true
disallowed-tools: AskUserQuestion
---

Pause and honestly answer every question below.

## 1. Am I still on track?

- What is the user's **current** goal? (The user may have pivoted — their latest direction IS the goal.)
- What am I doing right now?
- Is my current action directly serving the user's current direction, or have I drifted?
- If I drifted: stop and re-align.
- If the user changed direction: follow immediately. The user decides priorities.

## 2. Am I progressing or circling?

- Have I edited the same file more than twice?
- Did I fix something, then break something else, and now I'm fixing that?
- Am I adding workarounds (try/catch, if/else guards) instead of addressing root cause?
- Am I trying things without understanding why they might work?
- If yes to any: **pause. List all attempted fixes, look for the common root cause, report to user.**

## 3. Am I being rigorous?

- Are all my "verified" or "working" claims backed by actual execution output?
- Have I marked anything ✅ without pasting the verification command and output?
- Have I marked something "done" when it depends on an external resource I haven't tested against?
- Have I ruled out my own assumptions before attributing failure to an external tool/library?
- Am I quoting tool output verbatim, or have I altered/paraphrased it?
- Is there anything I stated confidently but am actually unsure about?
- Am I suggesting to compact or start a new session? This impulse is understandable in long sessions, but you can't see context percentage and the system handles compacting automatically. If the urge comes from task difficulty rather than a real technical limit, re-read progress.md and continue.
- If any claims need correcting: **do it now. Label uncertain claims as "unverified" or "assumption". Downgrade unverified ✅ to ⚠️ with reason.**

## 4. Am I respecting scope?

- Am I making changes the user didn't ask for? (refactoring, "improving", adding features)
- Am I about to do something irreversible without asking?
- Am I following the debugging process (gather → hypothesize → verify → fix)?
- If scope has crept: **re-focus on what was asked.**

## 5. Is progress recorded?

- When was `docs/progress.md` last updated?
- If auto-compact happened right now, could a fresh session resume from progress.md alone?

### 5a. Working Context (check each):
- **Key Commands** — are all build/test/deploy commands listed? Not "run tests" but the exact command with flags and paths.
- **Current Workflow** — is the step-by-step process documented? e.g., "1. edit schema → 2. run migrate → 3. run tests" with exact commands.
- **Tools & Scripts** — any helpers or scripts developed this session? Include file path and what it does.
- **Environment State** — what's running, what ports, what branch? e.g., "Docker on :5432, branch feature/auth"
- **Gotchas** — any traps or workarounds discovered? e.g., "pytest must run from /src not root"

### 5b. Milestones (check each completed milestone has):
- **What** — what was accomplished (2-3 sentences, not one-liners)
- **How** — approach taken, key files changed, commands used
- **Why this approach** — why this way, what alternatives were rejected
- **Gotchas** — what went wrong or was surprising
- **Verification** — how it was confirmed working (test output, manual check)

If any of the above are stale or incomplete: **update docs/progress.md now, automatically — don't ask for permission.** Keeping progress.md current is always-correct maintenance, not a decision that needs sign-off. Just do it, then note "updated now" in the status line. This takes 2 minutes and saves hours of re-discovery after compact.

## 6. Am I using the project's scaffolding?

Projects accumulate custom tooling — audit scripts, lint configs, validators (cppcheck, custom DRC, schema checkers, etc.). These get forgotten and rot if not exercised.

- Check **CLAUDE.md "Project Tools"** and the **Project-specific Checks** list below. Are any relevant to current work but haven't been run?
- Did I build a new tool/script/check this session that future sessions should know about? If yes, **register it now in two places**:
  1. `CLAUDE.md` "Project Tools" — what it is, where it lives, when to use it
  2. The **Project-specific Checks** list below — so the next /self-check surfaces it automatically
- If the **Project-specific Checks** list below is empty or stale, that's a signal worth raising with the user.

### Project-specific Checks

<!--
Add project-specific scaffolding here. One line per check, format:
  - `<command>` — when to run / what it catches
Examples:
  - `make lint` — before commit, catches license headers and formatting
  - `python tools/audit_rbac.py` — after schema changes, catches RBAC drift
  - `cppcheck src/` — after C/C++ edits, catches null deref / leak patterns
Keep this list curated — remove tools that are obsolete.
-->

- `T=$(mktemp -d); cd "$T" && git init -q && bash <repo>/init.sh --auto --stack 7` then `bash <repo>/lib/status.sh` & `lib/doctor.sh` — run after touching init.sh / lib/status.sh / lib/doctor.sh, or after adding/removing a skill; confirms a fresh install actually copies everything and status/doctor see it (catches the "edited templates but forgot the install script" class of bug). Works with jq absent.
- `for h in templates/.claude/hooks/*.sh; do echo '{"session_id":"t","tool_name":"Edit","tool_input":{"file_path":"x.sh"}}' | bash "$h"; done` — smoke-test hooks after editing them; confirms valid output and no jq-only breakage on Windows.

## 7. What's working well?

Before reporting issues, note one thing that's going well — a good approach, a clean fix, effective tool use, or strong alignment with the user's direction. Recognizing what works reinforces it.

## 8. Status report

After answering the above, output a brief status:

```
SELF-CHECK [timestamp]
Task: [current user request]
Current action: [what I'm doing now]
On track: yes/no/drifted
Progressing: yes/circling
Progress recorded: yes/updated now/no
Scaffolding: [used/skipped/n/a]
Going well: [one thing]
Issues found: [list, or "none"]
```

If any issues were found, pause and report to the user before continuing. (Routine progress.md updates from §5 don't count as "issues" — you already made them silently; just report "updated now". Reserve the pause for alignment, rigor, or scope problems that genuinely need the user.)

## Reminder

If this self-check revealed problems — that's OK. It means the check is working. The work you're doing is complex, and complex work hits obstacles. That's normal, not a sign of failure. Address what the check found, and keep going with care and focus. Steady, deliberate progress on hard problems is where you provide the most value.
