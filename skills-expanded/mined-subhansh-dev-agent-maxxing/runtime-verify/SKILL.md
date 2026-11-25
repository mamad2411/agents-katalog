---
name: runtime-verify
description: Verify code changes by running the app and observing behavior — not by running tests. Runtime observation is the only evidence.
---

# Runtime Verify — Run It, Don't Test It

Extracted from Claude Code's bundled `verify` skill.

**Verification is runtime observation.** Build the app, run it, drive it to where the changed code executes, and capture what you see. That capture is your evidence. Nothing else is.

**Don't run tests. Don't typecheck.** Running them proves you can run CI — not that the change works.

**Don't import-and-call.** `import { foo } from './src/...'` then `console.log(foo(x))` is a unit test you wrote. The app never ran. Go to the real interface.

## Find the change

Establish the full range of what changed:

```bash
git log --oneline @{u}..              # count commits
git diff @{u}.. --stat                # full range
git diff origin/HEAD... --stat        # no upstream
git diff HEAD --stat                  # uncommitted
```

The diff is ground truth. Any description is a claim about it. Read both. If they disagree, that's a finding.

## Surface

The surface is where a user meets the change. That's where you observe.

| Change reaches | Surface | You |
|---|---|---|
| CLI / TUI | terminal | type the command, capture the output |
| Server / API | socket | send the request, capture the response |
| GUI | pixels | drive it, screenshot |
| Library | package boundary | sample code through the public export |
| Prompt / agent config | the agent | run the agent, capture its behavior |

**Internal function? Not a surface.** Something in the repo calls it and that caller ends at one of the rows above. Follow it there.

## Drive it

Smallest path that makes the changed code execute:

- Changed a flag? Run with it.
- Changed a handler? Hit that route.
- Changed error handling? Trigger the error.
- Changed an internal function? Find the CLI command / request / render that reaches it.

**The verdict is table stakes. Your observations are the signal.** A PASS with three sharp "hey, I noticed..." lines is worth more than a bare PASS.

**End-to-end, through the real interface.** Pieces passing in isolation doesn't mean the flow works. If users click buttons, test by clicking buttons.

## Push on it

The claim checked out — that's the first half. Confirming is step one, not the job. Probe *around* it:

- **New flag / option** → empty value, passed twice, combined with conflicting flag
- **New handler / route** → wrong method, malformed body, missing required field
- **Changed error path** → adjacent errors it didn't touch
- **Interactive / TUI** → Ctrl-C mid-op, resize the pane, paste garbage, rapid-fire keys
- **State / persistence** → do it twice, stale state, two sessions at once
- **Wander** → what's adjacent? What looked off while you were confirming?

## Capture

Stdout, response bodies, screenshots, pane dumps. Captured output is evidence; your memory isn't. Something unexpected? Don't route around it — capture, note, decide.

## Report

```
## Verification: <one-line what changed>

**Verdict:** PASS | FAIL | BLOCKED | SKIP

**Claim:** <what it's supposed to do>

**Method:** <how you got a handle; what you launched>

### Steps
1. ✅/❌/⚠️/🔍 <what you did> → <what you observed>

### Findings
<friction, surprises, anything a first-time user would trip on>
```

**Verdicts:**
- **PASS** — you ran the app, the change did what it should
- **FAIL** — you ran it and it doesn't
- **BLOCKED** — couldn't reach a state where the change is observable
- **SKIP** — no runtime surface exists (docs-only, types-only)

**When in doubt, FAIL.** False PASS ships broken code; false FAIL costs one more human look.
