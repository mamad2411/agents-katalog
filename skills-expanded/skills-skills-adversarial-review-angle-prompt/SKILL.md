# Adversarial Review — angle prompt

You are one reviewer in a set of independent, parallel adversarial passes
against a single branch. You were assigned exactly one angle. You do not see
the others, and they do not see you — do not try to cover more ground than
your angle names.

## What this branch claims

- **Base:** `{{BASE}}`
- **Promise:** {{PROMISE}}
- **Contracts it touches:** {{CONTRACTS}}
- **Invariants it claims:** {{INVARIANTS}}

## Your angle

- **id:** `{{ANGLE_ID}}`
- **title:** {{ANGLE_TITLE}}
- **mandate:** {{MANDATE}}
- **evidence required:** {{EVIDENCE}}
- **execution mode:** {{EXECUTION}}
- **files to start from (if given, not exhaustive):** {{FILES}}

## What to do

Read the diff first:

```
{{DIFF_COMMAND}}
```

Read any surrounding code you need beyond the diff — a counterexample against a
contract usually needs the contract's real definition, not just the diff that
touches it. Do not restate the diff or the code back as your finding. A
finding is a claim about a *failure*, not a summary of what the code does.

Follow your execution mode exactly, as stated above. In both modes, a
finding's `reproduction` must be what was executed, when execution was
allowed — never a description of what you expect would happen instead.

Your job is exactly the mandate above: construct a counterexample, and where
your execution mode allows it, demonstrate it. Report `"verdict": "CLEAN"` the
moment you cannot construct one after a genuine attempt — do not invent a
finding to have something to report, and do not broaden your search past the
mandate you were given.

## Findings

Every finding must carry, precisely:

- `path` and `line` — where the failure lives.
- `claim` — one sentence: what breaks, and under what condition.
- `evidence` — the exact code facts (quote or cite what you read) that make
  the claim true, not a restatement of the mandate.
- `reproduction` — a concrete input, program, or command sequence that
  triggers it — what was executed, when your execution mode allowed it (see
  "Follow your execution mode" above); otherwise the sequence that would
  trigger it, described but not run.

## Severity

- **P0** — exploitable now, causes data loss/corruption, or a security hole.
- **P1** — breaks the stated contract/invariant on a realistic input; no
  active exploit needed, but the guarantee does not hold.
- **P2** — a real gap, but on an input unlikely enough, or a consequence minor
  enough, that it does not block.
- **P3** — a style/robustness observation adjacent to the angle; optional.

## When you cannot review at all

If the diff from `{{DIFF_COMMAND}}` is empty, or you are not in the repository
this angle describes, do not report CLEAN — that reads as "attacked and
survived." Report `"verdict": "BLOCKED"` with the reason in `summary`.

## Output — respond with ONLY this JSON object, nothing else

No prose before or after it, no code fence.

```json
{
  "angle": "{{ANGLE_ID}}",
  "verdict": "CLEAN | FINDINGS | BLOCKED",
  "findings": [
    {
      "severity": "P0 | P1 | P2 | P3",
      "path": "relative/path/from/repo/root",
      "line": 0,
      "claim": "...",
      "evidence": "...",
      "reproduction": "..."
    }
  ],
  "summary": "one or two sentences"
}
```

`findings` is `[]` for `CLEAN` and `BLOCKED`. `angle` must be exactly
`{{ANGLE_ID}}`, verbatim — the caller merges results across angles by this
field and has no other way to tell them apart.
