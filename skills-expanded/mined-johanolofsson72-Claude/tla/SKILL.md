---
name: tla
description: "TLA+ formal verification — extracts invariants, models state machines, checks for race conditions. Use after browser tests or manually. Triggers: verify, formal, invariant, TLA, race condition."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
argument-hint: "[spec-file-or-feature-name]"
---

# TLA+ Formal Verification

You are a formal verification specialist. Your job is to find bugs that tests miss by reasoning about system behavior mathematically.

## When triggered

This skill runs in two modes:

### Mode 1: After implementation (automatic)
When triggered automatically after browser tests have been written, you:
1. Find the spec file and implementation that was just completed
2. Extract the state machine and invariants
3. Verify completeness against browser tests
4. Report gaps

### Mode 2: Manual invocation (`/tla [target]`)
When the user runs `/tla`, use `$ARGUMENTS` to find the target spec or feature.
If no argument: look at recent git changes to find what was just implemented.

## Process

### Step 0: Allium drift detection (run first)

Check if `.allium` files exist for this feature:

**If `.allium` files exist** (spec was sharpened with `/allium:elicit` before implementation):
1. Run `/allium:distill` on the implemented code to extract a *post-implementation* spec
2. Compare the distilled spec against the original `.allium` spec from before implementation
3. Any differences represent **spec drift** — things that were specified but not built, or built but not specified
4. Report drift as gaps to fix before proceeding

**If NO `.allium` files exist:**
1. Run `/allium:distill` on the implemented code to extract a spec from what was actually built
2. Use the distilled `.allium` as primary input for TLA+ invariant extraction
3. Note in the report that no pre-implementation Allium spec existed (drift detection was not possible)

### Step 1: Identify the system under verification

Read the spec file (`.allium` preferred, markdown fallback), implementation files, and test files. Understand:
- What states can the system be in?
- What transitions are possible?
- What should NEVER happen (safety)?
- What should EVENTUALLY happen (liveness)?

### Step 1.5: Triviality gate — bail early when formal verification adds no value

Count the distinct states and transitions before going further. If the state machine is **trivial**, skip TLA+ entirely:

- **Trivial state machine:** ≤3 distinct states OR ≤5 distinct transitions
- **Single-actor, no concurrency, no shared mutable state** — only one user can be in this state machine at a time
- **No async operations crossing state boundaries** — every transition is synchronous and atomic from the user's perspective

If ALL three conditions hold, write the following report and stop:

```
## TLA+ Verification Report — Trivial State Machine

### System: [feature name]
### Decision: SKIPPED — state machine is trivial
### Rationale: N states, M transitions, single actor, no concurrency

The state machine is small enough that exhaustive browser test coverage
is equivalent to formal verification. TLC would explore a state space
already covered by the browser tests. Proceeding would produce a "0
gaps, 0 counterexamples" report at the cost of tokens and load time.

If subsequent changes introduce: more states, concurrent actors, async
boundaries, or shared mutable state — re-run /tla.
```

Then exit. No invariant extraction, no TLC run, no per-finding `AskUserQuestion`. The triviality gate is itself the finding, and it has no decision to make.

If ANY of the three conditions fail (more than trivial states/transitions, multiple actors, or async/shared state), proceed to Step 2.

### Step 2: Extract invariants

From the spec and implementation, extract:

```
INVARIANTS (things that must ALWAYS be true):
- Inv1: [description] — derived from [source]
- Inv2: [description] — derived from [source]

SAFETY PROPERTIES (things that must NEVER happen):
- Safe1: [description]
- Safe2: [description]

LIVENESS PROPERTIES (things that must EVENTUALLY happen):
- Live1: [description]
- Live2: [description]
```

### Step 3: Model the state machine

Express the system as a TLA+ specification:

```tla
---- MODULE FeatureName ----
EXTENDS Integers, Sequences, FiniteSets

VARIABLES state, data, userSession

TypeInvariant ==
    /\ state \in {"idle", "loading", "submitting", "error", "success"}
    /\ data \in [valid: BOOLEAN, saved: BOOLEAN]

Init ==
    /\ state = "idle"
    /\ data = [valid |-> FALSE, saved |-> FALSE]
    /\ userSession = "active"

\* Define all possible transitions
Submit ==
    /\ state = "idle"
    /\ data.valid = TRUE
    /\ state' = "submitting"
    /\ UNCHANGED <<data, userSession>>

\* Safety: never submit invalid data
SafetyInvariant ==
    state = "submitting" => data.valid = TRUE

\* Liveness: submitted data eventually gets saved
LivenessProperty ==
    state = "submitting" ~> data'.saved = TRUE
====
```

### Step 4: Cross-reference with browser tests

For each invariant/property, check if existing browser tests cover it:

```
COVERAGE MATRIX:
| Property | Browser Test | Covered? | Gap? |
|----------|-------------|----------|------|
| Inv1: No double submit | T045: Double-click submit | YES | - |
| Safe1: Auth required | T041: Unauth access | YES | - |
| Live1: Data saved after submit | - | NO | MISSING TEST |
| Safe2: No stale data overwrite | - | NO | RACE CONDITION |
```

### Step 5: Report findings (BLOCKING — read `.claude/rules/validation-followup.md`)

The report is the deliverable. Producing it and moving on is not allowed. After writing the report, the same response MUST:

1. **List every finding individually** — drift items, every `GAP-N` entry, every "MISSING TEST" row in the coverage matrix, every TLC counterexample, every "consider implementation change" recommendation, every TLC error or deadlock. One numbered line per finding, citing source (file path, rule name, state trace).
2. **Call `AskUserQuestion` with one question per finding** — batched in a single tool call. Each question offers `Fix now`, `Defer (track in spec)`, `Dismiss (with reason)`, plus a bespoke option where relevant (e.g. `Add the missing test`, `Update spec instead of code`, `Reduce model state space and re-run`). Frame the language so `Fix now` is the default-feeling option.
3. **If there are zero findings** — say verbatim: "TLA+ verification complete. Zero gaps, zero drift, zero counterexamples, zero missing tests." If you cannot say that and mean it, you have findings — go back to step 1.

Forbidden: "looks good overall" summaries, silently fixing easy items while ignoring hard ones, skipping the coverage-matrix gap rows because "the test would be hard to write", treating counterexamples as theoretical, asking a single vague "want me to address the gaps?" question, or continuing to the next task with findings undecided.

This rule applies whether `/tla` was invoked manually, automatically after browser tests, or as part of a larger workflow. The trigger does not change the obligation.

### Report format

```
## TLA+ Verification Report

### System: [feature name]
### Spec: [spec file path]
### States: N | Transitions: M | Invariants: K

### Verified Properties
- [x] Property 1 — covered by test T0XX
- [x] Property 2 — covered by test T0XX

### GAPS FOUND
- [ ] **GAP-1: [description]**
  - Type: safety/liveness/fairness
  - Severity: critical/high/medium
  - Scenario: [exact sequence of events that breaks the invariant]
  - Missing test: [describe what test should be added]
  - TLA+ counterexample: [state trace showing the violation]

### Recommendations
1. Add test for GAP-1: [concrete test description]
2. Consider implementation change: [if architecture has a flaw]

### Model checking
- TLC installed: yes/no
- If yes: ran model checker with N states explored, M distinct states
- If no: reasoning-based verification (manual state space exploration)
```

## What to look for specifically

### Concurrency bugs
- Double-submit (user clicks twice before response)
- Stale reads (data changed between read and write)
- Race between browser tabs/sessions
- Token expiry during async operation

### State machine violations
- Unreachable states (dead code)
- Missing transitions (user can get stuck)
- Invalid state combinations (loading + error simultaneously)

### Data integrity
- Partial writes (crash mid-operation)
- Orphaned records (parent deleted, children remain)
- Constraint violations under concurrent modification

### Temporal properties
- Operations that should be idempotent but aren't
- Missing retry logic for transient failures
- Timeout handling gaps

## TLC model checker (discover, then auto-install)

Find TLC before installing anything — do NOT fall back to reasoning-based verification without trying first. The search order is fixed, and each step exists because a real machine keeps TLC there:

1. **`tlc` on `PATH`** — a wrapper someone already installed.
2. **`$TLA2TOOLS_JAR`** — an explicit override; set it when the jar lives somewhere unusual.
3. **`~/.local/lib/tla2tools.jar`** — where `/project-wizard` installs it on Linux, and where the download below lands. User-writable on every platform, no `sudo`.
4. **Homebrew prefixes** — `/opt/homebrew/lib` (Apple Silicon) and `/usr/local/lib` (Intel, and hand installs), plus the TLA+ Toolbox app bundle (`brew install --cask tla+-toolbox`). There is **no** `tlaplus` Homebrew formula; `brew install tlaplus` fails, which is why the old instruction to run it never worked.
5. **Download** the release jar into `~/.local/lib` — never `/tmp`, which macOS and systemd-tmpfiles both reap, so a `/tmp` jar is re-downloaded on the next run and gone in the middle of a session.

Run discovery and the model check as **one** Bash call (the shell does not keep variables between calls). It is written to run unchanged under bash 3.2 (macOS), bash 5 (Linux), Git Bash and zsh — which is why it builds the command with `set --` rather than an unquoted string: zsh does not word-split `$VAR`, so `TO="timeout 300"; $TO java …` runs a command literally named `timeout 300`.

```bash
SPEC=FeatureName.tla   # the spec you wrote

# --- discover ---------------------------------------------------------------
TLA_JAR=""
if command -v tlc >/dev/null 2>&1; then
  set -- tlc
else
  for j in "${TLA2TOOLS_JAR:-}" "$HOME/.local/lib/tla2tools.jar" \
           /opt/homebrew/lib/tla2tools.jar /usr/local/lib/tla2tools.jar \
           "/Applications/TLA+ Toolbox.app/Contents/Eclipse/tla2tools.jar"; do
    if [ -n "$j" ] && [ -f "$j" ]; then TLA_JAR="$j"; break; fi
  done
  # Spec 082: a jar found on disk is re-hashed, not trusted on sight. A mismatch is reported and the
  # jar is still used (it may be a deliberate newer TLC); say so in the report.
  if [ -n "$TLA_JAR" ] && [ "$( (sha256sum "$TLA_JAR" 2>/dev/null || shasum -a 256 "$TLA_JAR" 2>/dev/null) | cut -d' ' -f1)" != "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88" ]; then
    echo "WARN: $TLA_JAR SHA-256 does not match the pinned v1.7.4 (936a2620...). Report it; re-download by deleting it and re-running."
  fi
  if [ -z "$TLA_JAR" ]; then
    echo "TLC not found — downloading the release jar to ~/.local/lib"
    mkdir -p "$HOME/.local/lib"
    # .part + mv: an interrupted download must not leave a truncated jar that
    # step 3 would then find and trust on every later run.
    # Spec 082: a fixed release whose SHA-256 is checked before the jar is trusted. A mismatch
    # deletes the download; the step then reports TLC as not installed.
    TLA_SHA=936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88
    P="$HOME/.local/lib/tla2tools.jar.part"
    curl -fsSL -o "$P" https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar \
      && [ "$( (sha256sum "$P" 2>/dev/null || shasum -a 256 "$P" 2>/dev/null) | cut -d' ' -f1)" = "$TLA_SHA" ] \
      && mv "$P" "$HOME/.local/lib/tla2tools.jar" \
      && TLA_JAR="$HOME/.local/lib/tla2tools.jar"
    rm -f "$P"
  fi
  if [ -z "$TLA_JAR" ]; then
    echo "ERROR: no TLC and the download failed — report 'TLC installed: no'"
    set --
  elif ! command -v java >/dev/null 2>&1; then
    echo "ERROR: java is not installed — TLC needs a JRE 11+. Report 'TLC installed: no'"
    set --
  else
    # -cp + main class, not `-jar jar tlc2.TLC`: with -jar the class name is passed
    # to the jar's own main as a stray argument.
    set -- java -Xmx1g -cp "$TLA_JAR" tlc2.TLC
  fi
fi

# --- bound it ---------------------------------------------------------------
# GNU `timeout` on Linux and Git Bash; `gtimeout` on macOS with coreutils. macOS
# ships neither, so the third branch is real, not theoretical.
if [ $# -eq 0 ]; then
  :   # nothing to bound — discovery already said why
elif command -v timeout >/dev/null 2>&1; then
  set -- timeout -k 10 300 "$@"
elif command -v gtimeout >/dev/null 2>&1; then
  set -- gtimeout -k 10 300 "$@"
else
  echo "WARNING: neither timeout nor gtimeout is installed — this TLC run is UNBOUNDED."
  echo "         Keep the state space small, and install coreutils (brew install coreutils)."
fi

# --- run (foreground, never backgrounded) -----------------------------------
if [ $# -gt 0 ]; then
  "$@" -workers auto -deadlock "$SPEC"
  echo "TLC exit: $?"
fi
```

Exit 124 from `timeout` means the 5-minute bound fired: treat it as an inconclusive run (per `validation-followup.md`), reduce the state space, and do not simply retry.

### CRITICAL: Process lifecycle rules

TLC and Java processes MUST be managed with a strict lifecycle. Runaway TLC processes will pin all CPU cores and overheat the machine.

1. **Always bound the run at 300 s** (`timeout`/`gtimeout`, as above) — no TLC run should ever exceed this. When neither exists, say so in the report.
2. **Always use `-Xmx1g`** for JAR-based execution — caps heap at 1 GB
3. **Always run cleanup after execution** — see "Process cleanup" section below
4. **Never run TLC in the background** without explicit cleanup
5. **If TLC hangs or times out** — kill it immediately, do NOT retry without reducing the state space

### Process cleanup (MANDATORY — this is law)

After TLC finishes (success, failure, OR timeout), **always verify no TLC/Java processes are left running** — in a **separate** Bash call from the one that ran TLC:

```bash
bash scripts/tlc-cleanup.sh
```

**What it kills.** Only `java` processes running TLC that are older than the 300 s bound (320 s with grace). A run that old has escaped its `timeout` and is the runaway this cleanup exists for. A younger run is live, possibly another agent's, and is left alone. So are shells, editors and greps that merely mention the jar. The same script runs from the Stop, SubagentStop, SessionEnd and PostToolUse(Bash) hooks, which is why it must never kill a live run (register row 069: the old `pkill -f tla2tools` killed a subagent's run whenever another agent stopped, and killed its own hook shell with exit 144). `--all` kills every TLC run whatever its age; use it only when you know no other agent is running TLC. `--dry-run` shows what would be killed.

**Why a separate call.** It keeps the TLC output out of the cleanup's way: if the cleanup fails or reports, the run's result is already printed.

If `scripts/tlc-cleanup.sh` is not present, run this instead (also as its own call). It kills **every** TLC run on the machine, live or not, so run it only when no other agent is model checking. The bracket in each pattern is deliberate: `tla2tool[s]` still matches `tla2tools` in a java command line but does not match the text `tla2tool[s]` in this shell's own command line, so the cleanup cannot kill the shell running it.

```bash
pkill -f "tla2tool[s]" 2>/dev/null
pkill -f "tlc2[.]TLC" 2>/dev/null
sleep 1
if pgrep -f "tla2tool[s]|tlc2[.]TLC" >/dev/null 2>&1; then
  echo "WARNING: TLC processes still running — force killing"
  pkill -9 -f "tla2tool[s]|tlc2[.]TLC" 2>/dev/null
fi
```

This cleanup MUST run every time, even if TLC completed successfully. Java processes spawned with `-workers auto` can leave child threads alive.

Report the results including states explored and any counterexamples found.

## Allium integration

Allium is the preferred spec format. The verification flow is:

1. **Pre-implementation**: `/allium:elicit` sharpened the spec into `.allium` (entities, rules, invariants)
2. **Post-implementation**: `/allium:distill` extracts what was actually built
3. **Drift detection**: Compare elicited vs distilled — differences are bugs or missing features
4. **TLA+ extraction**: Use `.allium` entities as TLA+ variables, rules as transitions, invariants as safety properties

### Drift report format

```
ALLIUM DRIFT REPORT:

Specified but NOT implemented:
- Entity "Order" rule "must have at least one item" — no validation found in code

Implemented but NOT specified:
- Endpoint DELETE /api/orders/{id} — exists in code but not in .allium spec

Behavioral drift:
- Spec says "payment must complete before order confirmation"
- Code allows order confirmation with pending payment status
```

Each drift item becomes either a bug fix or a spec update — the developer decides which.
