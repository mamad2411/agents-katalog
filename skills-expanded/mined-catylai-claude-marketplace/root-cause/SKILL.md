---
name: root-cause
description: "Runs a bug investigation from symptom to verified fix: collects the symptoms, delegates read-only root-cause analysis to the debugger agent, then applies the smallest fix and checks it against the full test output in the main thread. Use for a crash, a failing test, a regression, or behaviour nobody can explain. Not for a code-quality review with no defect (use code-review-core:review-scan); not for a live production incident (use observability-core:incident-declaration)."
argument-hint: "[bug description, error message, or failing test]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Agent, AskUserQuestion
license: MIT
---

# Root cause

Owns a complete debugging session in the main thread. The fix-and-verify loop stays here because
each fix depends on the raw output of the last run, and a subagent only returns a summary. The
one part that summarizes well — a focused read-only investigation — goes to the `debugger` agent.

The reported problem: $ARGUMENTS

## Step 1 — Gather symptoms

Start from the report above and collect what is missing:

- **Expected** — what should happen.
- **Actual** — what happens instead.
- **Errors** — the exact text and the full stack trace, not a paraphrase.
- **Started** — when it broke, or whether it ever worked.
- **Reproduction** — the command or steps, and whether they trigger it every time.

Ask about the reporter's experience rather than their theory of the cause: a reporter's theory is
the most common source of anchoring, and locating the cause is the investigation's job. Use
`AskUserQuestion` when several facts are missing at once. Record intermittent reproduction as a
finding, because it changes which hypotheses are plausible.

## Step 2 — Delegate the root-cause analysis

Spawn the `debugger` agent with the symptoms filled in:

```
Agent(
  subagent_type: "debugger",
  description: "Root-cause <short slug>",
  prompt: "Investigate this bug and return a diagnosis; leave the fix to me.

  Expected: ...
  Actual: ...
  Errors: ...
  Started: ...
  Reproduction: ...

  Return exactly one of: ## ROOT CAUSE FOUND, ## INVESTIGATION INCONCLUSIVE, or
  ## CHECKPOINT REACHED, in the formats your instructions define."
)
```

Handle each return by its header:

| Header | What to do |
| --- | --- |
| `## ROOT CAUSE FOUND` | Go to Step 3. |
| `## CHECKPOINT REACHED` | Perform the action it names, or put the decision to the user, then re-delegate with the result. If the remaining work is small, finish it here instead. |
| `## INVESTIGATION INCONCLUSIVE` | Investigate the top-ranked remaining possibility yourself, or show the ranked list to the user and ask which to pursue. Re-spawning the same investigation unchanged returns the same answer. |

**Without the debugger agent** (Cowork/web, where subagents are unavailable, or the spawn is
denied): run the same investigation inline — three falsifiable hypotheses, one read-only
observation per hypothesis, and conclude only on observed evidence — then continue at Step 3.

**Without a checkout:** work from the code, logs and test output the user pastes, and hand them
the verification command to run in Step 4.

## Step 3 — Apply the fix

1. Read the cited files completely and re-derive the mechanism yourself. A diagnosis you cannot
   re-derive is one you cannot verify.
2. Make the smallest change that addresses the root cause. Keep adjacent improvements for a
   separate change so the verification stays unambiguous.
3. Follow the repository's conventions for the files you touch.

If the fix treats a symptom rather than the mechanism, say so before writing it. A symptom patch
is sometimes the right call, but only as a labelled, deliberate choice.

## Step 4 — Verify

1. Run the exact reproduction the diagnosis named, and read the whole output.
2. Confirm the symptom is gone and that you can explain why the change removes it. A symptom that
   vanished for an unexplained reason is not fixed.
3. Run the surrounding tests for regressions.
4. For an intermittent bug, run the reproduction three times.
5. If verification fails, treat it as a fresh observation: form a new hypothesis and iterate here,
   or re-delegate if the picture changed enough to warrant a clean investigation. Revert a fix you
   can no longer explain before trying the next one.

Done means: the symptom no longer occurs, you understand the mechanism, related tests still pass,
and the result holds across repeated runs.

## Step 5 — Report

```markdown
**Root cause:** <mechanism, one or two sentences>
**Fix:** <file:line — what changed>
**Verified by:** <command> → <result>, <n> runs
**Ruled out:** <hypothesis — the observation that refuted it>
**Status:** fixed | symptom-patched (labelled) | unresolved
```

The ruled-out list is the part a future session cannot rediscover cheaply. Commit only when
asked.
