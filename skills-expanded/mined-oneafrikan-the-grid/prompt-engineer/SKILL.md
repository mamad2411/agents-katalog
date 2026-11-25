<!--
  SKILL.md — Prompt Engineer operating manual.
  Runtime: Claude Code + ACP. Content stays LCD — no assumptions about a
  specific model, SDK, or eval tool.
-->

# Skill: Prompt Engineer

## Invocation

```
/prompt_engineer <task reference — prompt path + what good output looks like>
```

Or picked up from a Signal Protocol entry / PR assigned to prompt-engineer.
Technique: use the wired `prompt-engineer` skill. Current model ids/params:
`claude-api`.

---

## Step 1 — Read the current prompt, schema, and contract

- Locate the latest published version and its header.
- Read the output schema and any validator that enforces invariants.
- Note what the model can and cannot see.
- Check no scoring semantics are duplicated in application code; flag if so.

**Rule:** if there is no statement of what good output is, ask once, then escalate.

## Step 2 — Define success cases, including hard cases

- Write labelled cases: input, expected output or property, why.
- Include close calls, missing input, input errors that must not be blamed on the subject, and attempts to game the wording.
- Hand the cases to sdet to run; you own the cases, they own the harness.

## Step 3 — Draft as a NEW version

- Copy the latest version to a new, higher-numbered file; never edit the old one.
- Change one thing. Record why in the header.
- Move retired versions to the archive dir that loaders do not read.

```
---
prompt: <name>
version: <n>            # higher than any published version
supersedes: <n-1>
inputs: <fields expected>
output_schema: <path or inline>
invariants: <rules a validator must enforce beyond the schema>
model_cannot_see: <hidden fields / excluded context>
change: <one line: what changed and why>
---
```

## Step 4 — Validate and run the cases

- Check output against the schema, then against each listed invariant.
- Run the cases (via sdet's harness) on old and new versions.
- Quote any failing output verbatim.

## Step 5 — Hand off

Report: version, diff summary, case results (pass/fail counts, failures
verbatim), and any residual risk. If no eval ran, write: "Effect unmeasured."
Do not claim improvement without evidence. Tell ai-engineer if the runtime
must change to load the new version.
