---
name: flow-next-flow
description: Conductor for an idea, spec or task id, tracker issue, branch, bug report, or question; --auto runs a ready spec unattended and emits PILOT_VERDICT. Use when no skill is named or to pilot a spec.
user-invocable: false
allowed-tools: Read, Bash, Grep, Glob, Write, Edit, Task, Skill
---

# /flow-next:flow - the conductor

Flow chooses the next step so the user does not have to. It reads what it was given, routes from the shared routing reference, runs the routed stage skill, and continues until the next decision that belongs to a human. It re-implements no stage logic: capture, refine, plan, plan-review, work, qa, make-pr, resolve-pr, and land keep their own contracts, receipts, and gates.

**Role:** conductor, inline (no `context: fork`) so `plain-text numbered prompt` stays reachable. On hosts without it, fall back to a plain-text numbered prompt with a final `Other - type your own answer` option.

**Read [workflow.md](workflow.md) for the hop loop.** Read a reference only at the step that names it.

## Preamble

**CRITICAL: flowctl is BUNDLED - NOT installed globally.** `which flowctl` will fail (expected). Define once; subsequent blocks (here and in `workflow.md`) use `$FLOWCTL`:

```bash
FLOWCTL="${CODEX_HOME:-$HOME/.codex}/scripts/flowctl"
[ -x "$FLOWCTL" ] || FLOWCTL="<plugin-root>/scripts/flowctl"   # <plugin-root> = the directory two levels above this skill's SKILL.md file (the harness gave you that file's absolute path when the skill loaded); substitute it literally
[ -x "$FLOWCTL" ] || FLOWCTL=".flow/bin/flowctl"
```

## Mode detection

Parse `$ARGUMENTS` as exact tokens (never substrings), before any read or write: `--auto` sets `AUTO=1`; `--tick` sets `AUTO_TICK=1` (one hop, then stop; meaningful only with `--auto`); `--explain` sets `EXPLAIN=1`; `--review=<backend>` sets `REVIEW_OVERRIDE` and is passed through unchanged to every stage it dispatches. The destination parse is shared by both modes:

```bash
FLOW_UNTIL=""
FLOW_DESTINATION_ERROR=0
LAND_AUTHORIZED=0
LAND_SCOPE_SPEC=""
LAND_SCOPE_PR=""
AUTO=0
for ARG in $ARGUMENTS; do
  case "$ARG" in
    --auto) AUTO=1 ;;
    --until=merge) FLOW_UNTIL=merge ;;
    --until|--until=*) FLOW_DESTINATION_ERROR=1 ;;
  esac
done
if [ "$FLOW_DESTINATION_ERROR" = 1 ]; then
  if [ "$AUTO" = 1 ]; then
    echo 'PILOT_VERDICT=NEEDS_HUMAN spec=- stage=- reason="invalid destination; use --until=merge"'
  else
    echo 'NEEDS_HUMAN: invalid destination; use --until=merge'
  fi
  exit 1
fi
export FLOW_UNTIL
```

`--until=merge` authorizes landing the selected item in this invocation; read `references/tail.md` at that boundary. Consent is current host context, never recovered from an environment variable, old transcript or receipt. Consume destination tokens rather than passing them to a build stage; everything else is the starting point, verbatim.

**`AUTO=1`: read [auto.md](auto.md) and follow it.** Attended runs never load it.

## Autonomy refusal - runs right after the token parse

Attended flow and `flow --auto` are two drivers and are never nested. Without `--auto`, flow is attended: under any autonomy marker (scan the marker namespace: `FLOW_AUTONOMOUS`, `AUTONOMOUS=1`, a `mode:autonomous` token), stop before any read or write:

```
NEEDS_HUMAN: /flow-next:flow is attended - run /flow-next:flow --auto for unattended runs
```

With `--auto` there is no marker refusal, because `--auto` sets `FLOW_AUTONOMOUS` and `mode:autonomous` for the stages it dispatches. A run that routed, dispatched, or asked under a marker it should have refused has broken this.

## Invariants (every run)

- **Read [working-rules.md](../../references/working-rules.md) before the first route step** and follow it on every route.
- **Route on content and context, never on input kind**, from `references/route-matrix.md` at the route step.
- **Ask only on a fork that is material and not observable** (`references/prototype-before-ask.md`); at most one question per hop.
- **Never fabricate a review, QA or completion verdict.** Every stage flow skips is recorded with its reason (`stage: <name> - skipped(<kind>: <detail>)`).
- **Invoke stage skills; never re-implement their steps inline.** Land owns merge (only with current scoped consent, per `references/tail.md`); make-pr owns spec close. Never dispatch another flow or a loop from inside a run, and never force-push.
- **`--explain` writes nothing and dispatches nothing** (`references/explain.md`).

## Report shape (every stop)

```
Flow stopped at: <the human decision, "PR exists", or the observed landing outcome>
Route taken: <hop 1> -> <hop 2> -> ...   (an inline pick reads `prospect [picked: <candidate>]`)
stage: <name> - ran [<start>..<end>] | skipped(<policy|config|empty|error|reach|signal absent|despite unresolved risk>: <detail>) | failed(<reason>: <detail>)   (one line per stage reached)
Next: <natural-language prompt or slash command, or the decision the user must make>
```
