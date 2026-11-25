---
name: goalkeeper
description: Autonomous build/audit/verify loop that runs until a machine-checkable done-contract passes, with deterministic anti-spin stop conditions (no-progress, 3-retry, oscillation, budget) and on-disk human escalation. Use for "keep going until it is actually done" multi-round work that has objective pass/fail checks. Not for one-shot tasks or work without verifiable acceptance criteria.
---

# Goalkeeper

Goalkeeper drives multi-round work to a **machine-checkable "done"** and stops itself the moment it stops making real progress. You hand it a *done-contract* (a goal plus a list of items, each with an objective pass/fail check), or just a goal and let it plan the contract for you. It loops build to green, refusing to declare victory on anything but an independent external check, and it refuses to spin forever: it has deterministic stop conditions wired into code, not into a model's good intentions.

The defining risk this skill addresses is the opposite of laziness. An eager loop will happily run forever, cheat its own tests, or converge perfectly on the wrong target. Goalkeeper is built to fail *loudly and on disk* instead.

**Fable-mode workflow built in (v2).** Beyond the core build/verify loop, Goalkeeper now plans, critiques, and re-plans:

- **Plan.** Hand it a bare `goal` (no `items[]`) and a PLANNER agent decomposes it into a full contract before anything is built.
- **Self-critique.** When every check is green, an adversarial critic hunts for what the checks missed (green is not the same as good) and can re-open the loop with capped remediation items.
- **Scope checkpoint.** Every few rounds it steps back and asks "is finishing still worth it?".
- **Living re-plan.** A builder that discovers the plan is wrong can request the contract be revised mid-run, capped so the plan cannot grow forever.

**Hardware-in-the-loop hardening.** For slow or non-deterministic checks, Goalkeeper adds: `nondeterministic` checks with a retry `passPolicy` (latch / k-of-n) and tree-hash latching, so an environmental miss is never read as a code failure; per-check **shell / cwd / env pinning** (`pwsh`/`bash`/`cmd`/`sh`), so a check runs under exactly the shell it needs; **pipeline checks** (build → deploy → verify) that short-circuit on a failed build and force a fresh build when a stale artifact cannot be ruled out; and a **contract-identity** resume gate, so a different task pointed at a repo with an in-progress run halts (`contract-mismatch`) rather than resuming the wrong work.

These are described in detail below; the contract is therefore mutable and durable, surviving resume.

**Optional power features (all opt-in, all default-off).** Nine newer capabilities are gated behind flags and change nothing unless you turn them on. With no flags set, Goalkeeper behaves exactly as described above. They are: **best-of-N builders** (`caps.candidates` > 1: build N diverse candidate solutions for a hard item and let the deterministic contract pick the winner, no LLM judge); **step memoization** (`memoize: true`: call-granular crash-resume that skips re-running a builder/verifier call whose inputs are unchanged); a **durable approval token** (`approveToken: true`: resolve an escalation by writing a small file instead of re-invoking with args); a **repo map** (`caps.repoMap`: a cheap, token-bounded file/symbol map written once at setup to ground the planner and builder); a **verified pattern library** (`libraryPath`: bank every verifier-passed solution to a cross-repo store and inject the relevant ones as advisory context into future builds); a **durable physical human-in-the-loop gate** (`humanGate: true` + a check's `humanPrecondition`: suspend at zero compute until a person performs a required real-world action, then resume and verify); a **CI-fix mode** (`fix: { command }`: point Goalkeeper at a red build/test command and it drives that exact command to green); a **human-proven diagnosis** (`diagnosis`: hand in a finding you already proved, and Goalkeeper executes the mechanical fix with re-planning locked instead of re-theorizing); and an **auto-retro** (`retro: true`: on converge or a lesson-worthy halt, append a short "how the loop was driven" lesson to a durable LESSONS.md). Each is detailed in its own section below.

## Architecture: three layers

**1. The brain is code, not a prompt.** The stop logic lives in a fixed Workflow script at `goalkeeper.workflow.js`, invoked via the Workflow tool. Convergence, the 3-retry rule, no-progress detection, oscillation detection, and the budget backstop are all evaluated deterministically in that script. They are not the model's *memory* of how it is supposed to behave, so they cannot be argued away mid-run, forgotten after a `/clear`, or talked around by an over-helpful agent.

**2. The spine is durable on-disk state.** Everything that matters persists under `<repo>/.goalkeeper/`, split across **two files** plus a log:

- `plan.json`: **runtime state only**: `status`, the set of `passing` item ids, per-item `attempts` (retry counts), the current `iteration`, `prevGoodHead` (the last known-green git SHA), `fpHistory` (the fingerprint history used for no-progress and oscillation detection), `latched` (the tree-hashes at which a `nondeterministic` check has banked a pass, so a later flaky miss at the same tree does not revert or un-converge the run), and `attemptLog` (the per-item **failure ledger**: each failed attempt's structured "why it failed + what to change", a few most-recent kept per item, re-injected into the next builder attempt). The bookkeeper writes this every round, and the latch and ledger survive resume.
- `contract.json`: the **durable working contract**: `goal`, `items` (each with its `expectedOutput`, `check`, and `dependsOn`), and the two spent budgets `replanCount` and `critiqueRounds`. This is the contract the loop is *actually* building to right now, which can differ from what you first handed in (the planner may have generated it, self-critique may have appended items, a re-plan may have split items). It is written only by the planner/seed/re-plan/self-critique persist steps; the bookkeeper never touches it.
- `worklog.md`: an append-only log of per-round reflections.

Further files appear **only when the matching opt-in feature is on**, and are otherwise absent: `results.json` (the memoization ledger, `memoize: true`), `resolution.json` (a human-written durable-token resolution to consume, `approveToken: true` *or* `humanGate: true`), `repomap.md` (the generated, git-ignored repo map, `caps.repoMap` other than `'off'`), `AWAITING-HUMAN.md` (a planned-pause notice written when a check's `humanPrecondition` suspends the run, `humanGate: true`), and `LESSONS.md` (the auto-retro driving-lessons log, `retro: true`; written to `libraryPath` instead when the pattern library is on). They are documented under "Optional power features". One piece of durable state lives **outside** `<repo>/.goalkeeper/`: the **verified pattern library** (`libraryPath`) is a cross-repo store at the path you pass, deliberately not under the target repo so a pattern learned in one repo can seed a build in another.

Splitting runtime state from the working contract is deliberate: the bookkeeper rewrites `plan.json` every round, but the contract must not be at risk of a bookkeeping overwrite, so it lives in its own file written only when it genuinely changes.

A **fresh** invocation reads all of these and continues from exactly where the last one left off. Crucially, the anti-spin counters round-trip too: `attempts`, `fpHistory`, **and** the contract-mutation budgets (`replanCount`, `critiqueRounds`) are all restored, so the 3-retry, no-progress, oscillation, re-plan, and critique caps resume mid-progress rather than resetting to zero on every re-invocation. That is the point: Goalkeeper survives crashes, `/clear`, dropped channels, and machine reboots, because the truth lives on disk and not in a session. Workflow's own resume is merely an optimization on top of this; the on-disk state is authoritative.

If a run that has already made progress finds **no** `contract.json` (lost contract state), it refuses to silently re-seed a possibly-stale caller contract over lost revisions and instead escalates (`contract-lost`): you must re-invoke with `amendContract: true` and the contract, or reset state.

**3. The doorbell is Telegram, best-effort only.** When the loop halts and needs a human, it writes `ESCALATION.md` to disk and *then* tries to ping Telegram. The Telegram ping can fail, be muted, or never arrive. `ESCALATION.md` is the system of record. Never treat "no Telegram message" as "nothing to decide". Check the file.

## How to invoke

Call the Workflow tool with the script path and an `args` object. The full shape:

```js
Workflow({ scriptPath: "${CLAUDE_SKILL_DIR}/goalkeeper.workflow.js", args: {
  mode: "build",                 // build | audit | verify  (build is hardened)
  autonomy: "envelope",          // envelope (default: run unattended, halt only on triggers) | leash (pause each round for approval)
  repo: "/path/to/target-repo",
  statePath: null,               // optional; the durable state dir. Defaults to <repo>/.goalkeeper (plan.json + contract.json + worklog.md + ESCALATION.md live here)
  contract: { goal },            // OR { goal, items[] }. Goal alone -> the planner decomposes it into items. See templates/contract.schema.json + contract.example.json
  contractPath: null,            // optional: absolute path to a JSON file { goal, items[] }. Read at init, bypassing the args channel. Use for LARGE explicit contracts (inline args can truncate).
  checkPaths: ["tests/**"],      // write-protected; if the builder edits these, the round is auto-reverted
  caps: {
    maxIterations: 20, maxItemRetries: 3, maxStalls: 3, maxTokens: null,
    maxReplans: 2,               // living re-plan: max contract revisions before escalating (replan-budget)
    maxCritiqueRounds: 1,        // self-critique: max critique passes before converging anyway
    scopeCheckEvery: 4,          // scope checkpoint cadence in rounds; 0 disables
    // ---- best-of-N builders (opt-in; default 1 = single builder, unchanged) ----
    candidates: 1,               // N diverse candidate solutions per hard item; the contract (not an LLM judge) picks the winner. Default 1 = off
    candidatesHardOnly: true,    // true: the FIRST try of an item is a single builder; only retries fan out to N (pay N-cost only where the loop struggles)
    maxCandidates: 6,            // hard ceiling on N regardless of per-item override
    maxPlateau: 8,               // halt with reason `plateau` if passing-count does not increase for this many rounds (best-of-N backstop)
    // ---- repo map (opt-in; default 'off') ----
    repoMap: "off",              // 'off' | 'tree' (ranked file tree) | 'symbols' (ctags->git-grep->tree fallback, with top-level symbols)
    repoMapTokens: 1500,         // token budget for the generated .goalkeeper/repomap.md
    repoMapRefreshEvery: 0       // refresh the map every N rounds (0 = only at setup + after a re-plan/self-critique)
  },
  memoize: false,                // opt-in: call-granular crash-resume. Builder/verifier calls keyed by an input fingerprint; a completed call returns its stored result from .goalkeeper/results.json instead of re-running
  approveToken: false,           // opt-in: resolve an escalation by writing .goalkeeper/resolution.json {token, action} instead of re-invoking with resume args
  libraryPath: null,             // opt-in: absolute path to a cross-repo verified-pattern library. Every verifier-passed item is banked there, and patterns relevant to a new item are injected into the builder as advisory context. null = off
  humanGate: false,              // opt-in: honor a check's humanPrecondition. The run SUSPENDS at zero compute (status awaiting-human, costs no retry/iteration/no-progress) until a person performs the action and writes resolution.json {token, action:"ready"}, then resumes and verifies
  fix: null,                     // opt-in: CI-fix mode. { command, shell?, cwd?, env?, goal? } -> synthesize a one-item contract whose check is your red command and drive it to green (the captured red output seeds the first build). null = off
  diagnosis: null,               // opt-in: a HUMAN-PROVEN diagnosis (string, or { text, itemId } to scope it to one item). Injected into every matching builder as a trust-this block; forces maxReplans=0 and single-builder for that item (execute the fix, never re-theorize). null = off
  retro: null,                   // opt-in: true -> on converge or a lesson-worthy halt, a low-effort agent appends a dated "how the loop was driven" lesson to LESSONS.md (at libraryPath when set, else the state dir). Skips uneventful runs.
  denylist: ["git push","deploy","secrets","external-send"],  // forbidden actions, enforced regardless of mode
  telegram: { chatId: null },    // best-effort doorbell
  approvals: [],                 // leash: e.g. ["start"] to clear the pre-build gate; ["contract-gaps"] to proceed past blocking spec gaps
  runRounds: 1,                  // leash: rounds to run per invocation before pausing

  // ---- resume / amend (used when re-invoking after an escalation) ----
  amendContract: false,          // true: OVERRIDE the persisted contract.json with this call's contract.items[] (otherwise the persisted contract wins on resume)
  resetAttempts: [],             // e.g. ["over-limit-returns-429"]: clear that item's retry count + stall (and its attemptLog failure ledger) on a human-amended resume so a relaxed check gets a fresh budget
  freshStart: false              // true: archive ANY existing goalkeeper state (incl. an unfinished run) and start the new task on a clean slate. A converged run auto-archives on new work without this.
}})
```

### The contract is the product

`contract` carries the entire definition of "done": a top-level `goal` string and an `items[]` array. **You can pass `{ goal }` alone** and let the PLANNER agent decompose it into items, **or pass `{ goal, items[] }`** with the items written yourself. Each item has an `id`, an optional `priority`, a `description`, an optional `expectedOutput` (the concrete result that proves the item done), an optional `dependsOn` (ids that must pass first), and an objective, machine-runnable `check`. See `templates/contract.schema.json` for the shape and `templates/contract.example.json` for a worked example.

**Three ways to supply the contract.** There are three ways to hand Goalkeeper the contract: (a) **goal only** (`contract: { goal }`), where the planner builds the `items[]` for you; (b) **inline** (`contract: { goal, items[] }`), where you write the items into the call itself; and (c) **`contractPath`**, an absolute path to a JSON file holding the `{ goal, items[] }` object, read at init and never passed through the args channel. The file path is the robust choice for large or fully-explicit contracts, because a big inline contract can be truncated by the workflow arg channel, while a file cannot. The precedence for the working contract is: a persisted contract (on resume, in `.goalkeeper/contract.json`) wins, then the `contractPath` file, then inline `contract.items`, then the planner (goal only). One interaction to note: with `amendContract: true`, a `contractPath` file (if provided) supersedes inline `contract.items`, so prefer the file when amending a large contract too.

**Item fields that shape scheduling:**

- `expectedOutput`: the concrete artifact or observable result that proves the item is done. It is what the builder aims to produce; `check` is how the loop measures it.
- `dependsOn`: an array of item ids that must be passing before this item is eligible. This enables **dependency-ordered scheduling**: the loop only ever picks an item whose dependencies are all green. (Note: dependency-*aware* scheduling is implemented, but **item** execution is still **sequential**, one item per round, in a dependency-respecting order, not in parallel. The opt-in best-of-N builder does run several candidate builders **for a single item**, but they too run **sequentially on the live repo** (one resets to last-good, builds, is verified, then the next), not in parallel worktrees. *Concurrent* execution of **different items** still needs true parallel git worktrees and remains the standing deferral, because the runtime's worktree isolation was found non-viable for an arbitrary target repo.)

Write the contract carefully. Goalkeeper is extremely good at converging on whatever you actually wrote, which is exactly why a sloppy contract is dangerous: a perfectly-green run against the wrong checks is worse than a failed run, because it *looks* finished. The spec-review step below exists precisely to catch this before any code is written.

## Check types and capabilities

Each item's `check` is the objective, machine-runnable test the verifier uses to decide pass/fail.

**Base check types** (exactly one payload field, selected by `type`):

- `command`: a shell command; exit 0 passes, non-zero fails. `check: { type: "command", command: "npm test -- export.endpoint" }`
- `file_exists`: a `path` that must exist. `check: { type: "file_exists", path: "dist/report.csv" }`
- `grep`: a `pattern` (regex) that must match the file/output at `path`. `check: { type: "grep", path: "src/export.ts", pattern: "text/csv" }`
- `judge`: a `rubric` an LLM judge applies, for checks that genuinely cannot be a deterministic command. `check: { type: "judge", rubric: "The export escapes embedded commas and quotes per RFC-4180" }`

The following capabilities layer onto these to harden checks that are slow or environment-dependent (a hardware-in-the-loop pass).

**Non-deterministic checks (`nondeterministic` + `passPolicy` + `precondition`).** A check whose pass can depend on an external event, timing, hardware, a peer device, or the network should declare `nondeterministic: true`. The rationale: a PASS proves the code is correct at that code state, while a later MISS at the *same* code state only means the environment did not cooperate that instant, so a single miss must not be read as a code failure. The verifier RETRIES such a check up to `n` times (default `n=3`), running the optional `precondition` command before each attempt, and it passes if it succeeds at least once (`mode: "latch"`, the default) or at least `k` of `n` times (`mode: "k-of-n"`). The engine also **latches the git tree-hash** where the check passed: once latched at a tree, a later flaky miss at that same tree does not revert the round, does not count toward the item-stuck retry counter, and does not un-converge the run at the final suite. A genuinely-wrong item that never passes still escalates via item-stuck. The latch state persists in `plan.json` (a new `latched` field) and survives resume. The adversarial spec-review **requires** an environment-dependent check to carry this declaration: an env-dependent check *without* `nondeterministic: true` is treated as a blocking contract gap, because the loop would otherwise mistake an environmental miss for a code failure.

```js
check: { type: "command", command: "./scripts/mesh-rx-check.sh", nondeterministic: true,
         passPolicy: { mode: "k-of-n", k: 2, n: 5 }, precondition: "./scripts/arm-radio.sh" }
```

**Shell / env pinning (`shell` + `cwd` + `env`).** A check may declare `shell: "pwsh" | "bash" | "cmd" | "sh"`, plus optional `cwd` (default: repo root) and `env`. The verifier and builder run the check command through *that exact* shell, in that cwd, with those env vars set, never their own default shell. On Windows, `shell: "pwsh"` runs under PowerShell (never MSYS / git-bash) and `shell: "cmd"` runs under cmd.exe. This eliminates a class of false failures where a build environment that requires a specific shell (for example a PowerShell setup/`export` script that refuses to run under MSYS) silently broke every check.

```js
check: { type: "command", command: ".\\build.ps1 && .\\run-tests.ps1",
         shell: "pwsh", cwd: "firmware", env: { IDF_TARGET: "esp32p4" } }
```

**Pipeline checks (`type: "pipeline"`).** A check may be `{ type: "pipeline", build, deploy, verify, freshBuild? }`. It runs BUILD first; if the build exits non-zero the check FAILS immediately and deploy/verify do *not* run (never deploy a failed build). Only a clean build proceeds to deploy then verify, and the check passes only if verify passes. `freshBuild: true` forces a clean/reconfigured build; more generally the runner does a clean build whenever it cannot confirm the artifact was rebuilt from current source, so a stale incremental artifact cannot masquerade as a passing (or regressing) deploy.

```js
check: { type: "pipeline", build: "make -j", deploy: "make flash",
         verify: "./scripts/on-device-smoke.sh", freshBuild: true }
```

These capabilities compose: a pipeline check can itself be `nondeterministic` (hardware deploy whose smoke test is flaky) and can pin a `shell`.

**Human-precondition checks (`humanPrecondition` + `humanRearm`, opt-in via `humanGate`).** A check may declare `humanPrecondition`: a real-world action a *person* must perform before the check can pass (for example "move Unit B 50m away and start the listener", or "reseat the SD card"). When `humanGate: true`, the moment the loop reaches such an item it **suspends at zero compute** (status `awaiting-human`); it never tries to perform or fake the action. This pause is **not a failure** (it consumes no retry, iteration, or no-progress budget), and it writes `AWAITING-HUMAN.md` (not `ESCALATION.md`) carrying a one-time token. The person performs the action, writes `.goalkeeper/resolution.json` `{ token, action: "ready" }`, and re-invokes; the run then resumes and verifies the check. The latch is **per-tree** by default (`humanRearm: "per-tree"`: it re-arms, asking again, only when the baseline tree changes), with `"per-run"` (re-ask once per fresh invocation) and `"once"` (never re-ask after the first confirmation) as escape hatches. If a check carries a `humanPrecondition` but `humanGate` is **off**, the run escalates (`human-gate-disabled`) rather than silently skipping the human step. Detailed under "Optional power features".

```js
check: { type: "command", command: "./scripts/mesh-rx-check.sh", nondeterministic: true,
         humanPrecondition: "Move Unit B ~50m away, power it on, and start the listener", humanRearm: "per-tree" }
```

## Optional power features (opt-in, default-off)

Nine capabilities are gated behind flags. **None of them changes the default behavior:** with no flags set (`caps.candidates` 1, `memoize` false, `approveToken` false, `caps.repoMap` `'off'`, `libraryPath` null, `humanGate` false, `fix` null, `diagnosis` null, `retro` off), Goalkeeper runs exactly as described in the rest of this document. Turn one on only when its trade-off is worth it.

### Best-of-N builders (`caps.candidates`, default 1)

When `caps.candidates > 1`, a hard item is built by **N diverse candidate solutions** and the **deterministic contract** picks the winner. There is **no LLM judge**: the independent verifier runs each candidate's check and the winner is the one that genuinely passes (ties break by priority order, e.g. fewest regressions / first to pass). The selection is the same external check the loop always trusts, so best-of-N cannot launder a losing solution into a win.

**The candidates run sequentially on the live repo, not in parallel worktrees.** For each candidate in turn: the repo is reset to last-good, the builder is asked to take a *different* approach guided by a **diversity hint** (so the N attempts are genuinely distinct, not N copies of the same idea), and the candidate is verified in place. The winning candidate's commit is then promoted by **cherry-pick**. A true-parallel-worktree mechanism was tried and is **not viable** in this runtime, so the N attempts are serialized; you get candidate diversity, not wall-clock parallelism.

Configuration:

- `caps.candidates`: N, **default 1** (a single builder, unchanged). An individual item may set its own `candidates` to override the cap for just that item.
- `caps.candidatesHardOnly`: **default true**. The **first** try of an item is always a single builder; only **retries** fan out to N. So you pay the N-cost only on items the loop is actually struggling with. Set false to fan out from the first attempt.
- `caps.maxCandidates`: a hard ceiling on N (**default 6**), enforced even against a per-item override.
- A **budget-degrade** automatically reduces N when the per-run token budget is low, so best-of-N cannot blow the budget on a single round.

**Cost.** Candidates multiply a round's build+verify token cost by up to N. That is the whole trade-off: more attempts at a hard item for proportionally more tokens. Keep `candidatesHardOnly` on (the default) so the multiplier only applies where it earns its keep, and set a `maxTokens` cap.

**Failure semantics are unchanged.** If **no** candidate passes, it is just a normal **failed round**: every one of the N attempts is recorded in the failure ledger (`attemptLog`), the round reverts to last-good, and it counts against the item's retry budget so **item-stuck** still bounds it at 3. Best-of-N makes a hard item *more likely* to pass; it never weakens any stop condition.

**The `plateau` stop (a best-of-N backstop).** Because best-of-N can advance git HEAD by promoting a winning candidate **without a new item passing**, the usual no-progress fingerprint could in principle keep moving while the passing-count stays flat. So there is a `maxPlateau` stop (**default 8**): if the **passing-count does not increase for that many rounds**, the run halts with reason `plateau`. On the normal single-builder path this is dominated by item-stuck and no-progress (which fire first and name the blocking item), so `plateau` is effectively a backstop for the best-of-N case where HEAD advances but the contract does not get closer to done.

### Step memoization (`memoize`, default false)

`memoize: true` adds **call-granular crash-resume**. The expensive builder and verifier calls are keyed by a **deterministic fingerprint of their inputs** (the input tree, the item's check, and the other call inputs), and each call's result is stored in `.goalkeeper/results.json`. On a re-invocation, a call whose fingerprint matches a **completed** stored result returns that stored result **instead of re-running** the agent, so a crash-and-resume does not pay twice for work already done (no duplicate LLM spend).

**Invalidation is structural, so a stale result is never replayed.** A changed check or a changed input tree produces a **different key**, so the old result simply does not match and the call recomputes. There is no time-based or manual invalidation to get wrong. And the cache only ever *skips* recomputation, never *forces* a wrong answer: a **corrupt, missing, or contract-mismatched** ledger degrades to a normal recompute (it is never read as a result). The ledger is **dropped on a contract amend / redirect** (the inputs changed, so the cache is moot) and **archived on converge / `freshStart`** alongside the rest of the run state.

### Durable approval token (`approveToken`, default false)

By default you resolve an escalation by **re-invoking** Goalkeeper with resume args (`approvals`, `amendContract`, `resetAttempts`, a hint). `approveToken: true` adds a **file-based** alternative for environments where re-invoking with args is awkward.

On each escalation Goalkeeper **mints a deterministic token** (shown in `ESCALATION.md`). A human resolves the halt by writing **`.goalkeeper/resolution.json`** containing `{ token, action }`, where `action` is one of:

- `approve`: clear the gate and continue (maps onto `approvals`).
- `redirect`: revise the contract (maps onto `amendContract`, with optional `amendItems`).
- `abandon`: stop the run.
- `hint`: continue with a Reflexion-style **hint** fed to the next builder (optional `hint` text).

On the next invocation Goalkeeper **consumes the token once**, maps the action onto the existing resume levers (approvals / `amendContract` / `resetAttempts` / a Reflexion hint), and continues. A token that **does not match the active halt** is **ignored** (the run stays halted), so a stale or wrong-run resolution file cannot accidentally release a different escalation. The durable token is just a second front door onto the same resume machinery; the args path keeps working unchanged.

### Repo map (`caps.repoMap`, default 'off')

`caps.repoMap` gives the planner and builder cheap **grounding** in an unfamiliar repository. When enabled, a low-cost agent writes a **token-bounded `.goalkeeper/repomap.md`** (ranked key files plus, in `symbols` mode, their top-level symbols) and the planner and builder **read it** so they are not exploring the tree blind.

- `caps.repoMap: 'off'` (default): no map is generated.
- `caps.repoMap: 'tree'`: a **ranked file tree** (the key files, ordered by relevance).
- `caps.repoMap: 'symbols'`: the ranked tree **plus top-level symbols**, built via a **ctags -> git-grep -> tree fallback** chain (it uses ctags if available, falls back to git-grep, then to a plain tree, so it degrades gracefully on a repo without ctags).
- `caps.repoMapTokens`: the token budget for the generated map (**default 1500**).
- `caps.repoMapRefreshEvery`: if > 0, the map is **refreshed every N rounds**; at 0 (default) it is written **once at setup** and refreshed only after a **re-plan or self-critique** changes the shape of the work.

The map is **git-ignored** and is **never a gate**: it only informs the planner and builder, it is not a check and cannot fail a round. It is pure context, bounded in cost by `repoMapTokens`.

### Verified pattern library (`libraryPath`, default off)

`libraryPath` (an absolute path to a directory) turns on a **cross-repo memory of solutions that actually passed**. Every time an item's check passes the independent verifier, Goalkeeper **banks** that solution (the committed diff plus a short summary, keyed by a normalized fingerprint of the item description) into the library. On a later run, **in any repo**, when it starts a new item it **retrieves** the most relevant banked patterns and injects them into the builder as a **"PROVEN PATTERNS" advisory block**.

The point is to stop re-solving the same primitive from scratch. If you brought up an SX1262 radio (TCXO timing, SPI-gating-during-RX) in one firmware repo, that hard-won solution becomes advisory context the next time a similar item comes up in a different board's repo.

**It is advisory, never authoritative.** A retrieved pattern is context handed to the builder, *not* a relaxation of any rule. The independent verifier still runs the real check, the anti-gaming diff inspection still applies, and a pattern that does not fit is ignored. A bad or irrelevant pattern can at worst waste a little builder attention; it can **never** make a wrong solution pass, because nothing about banking or retrieval touches the verifier.

How it works:

- **Bank (on every verified pass).** The committed solution is captured as a diff, **scrubbed of secrets** (the banker strips Authorization headers, `*_KEY` / `*_TOKEN` / `*_SECRET` / `PASSWORD` assignments, and PEM private-key blocks before writing), summarized, and stored keyed by the item description. The source repo is recorded by **basename only** (e.g. `my-firmware`, never an absolute path), so the library does not leak where it came from.
- **Retrieve (when starting an item).** A low-cost agent ranks the library index against the current item's description and loads the top **`caps.libraryTopK`** (default 3) pattern bodies into the builder prompt. Retrieval is **semantic** (an agent ranks relevance), so a *paraphrased* item still matches a banked solution.
- **Dedup is deterministic.** Whether a new pass **appends** a fresh pattern, **updates** an existing one, or **replaces a variant** is decided by the script from content fingerprints, not by the agent, so the same library converges the same way regardless of which repo writes to it. Per-problem variants are capped at **`caps.libraryMaxVariantsPerProblem`** (default 3), and eviction prefers the **least-retrieved** variant (each retrieval increments the pattern's `timesRetrieved`, so useful patterns survive).

The library lives at `libraryPath`, **outside** any target repo's `.goalkeeper/`, and is **never archived or reset** by `freshStart` or by deleting a repo's `.goalkeeper/`. It is shared, durable, cross-repo memory you manage yourself. Degrade-safe: a retrieval or bank failure is non-fatal and never blocks a build (it logs and continues). Configuration: `libraryPath` (the on/off switch), `caps.libraryTopK` (default 3), `caps.libraryPatternMaxChars` (default 1500, the per-pattern body cap), `caps.libraryMaxVariantsPerProblem` (default 3).

### Durable physical human-in-the-loop (`humanGate` + a check's `humanPrecondition`, default off)

Some checks cannot pass until a **person does something physical**: move a radio to the next room, reseat an SD card, power-cycle a board, set up a virgin listener. `humanGate: true` makes Goalkeeper treat those as a **planned suspend**, not a failure.

When the loop reaches an item whose check declares a `humanPrecondition` (see "Check types and capabilities") and `humanGate` is on, it **suspends at zero compute**:

- It returns status **`awaiting-human`**, a distinct state that is **not** an escalation and **not** a halt. It consumes **no** retry, iteration, no-progress, or oscillation budget; a planned pause never costs the run anything.
- It writes **`AWAITING-HUMAN.md`** (not `ESCALATION.md`) describing the physical action and carrying a one-time **token**, and records `awaitingHuman` + `activeToken` in `plan.json`.
- It never tries to perform or simulate the action, and it never fakes the check.

The person performs the action, writes **`.goalkeeper/resolution.json`** = `{ "token": "<the token>", "action": "ready" }`, and re-invokes Goalkeeper. The run consumes the token once, **latches** the human-satisfaction for that item (recording the authorizing token, so `plan.json` is auditable against `AWAITING-HUMAN.md`), and proceeds straight to building and verifying it. By default the latch is **per-tree** (`humanRearm`): it re-arms, asking again, only when the baseline tree changes, so the person is not re-asked every round; `"per-run"` and `"once"` adjust that.

This shares the resolution-file machinery of the durable approval token, so turning on **`approveToken`** *also* enables `humanPrecondition` handling. If a check carries a `humanPrecondition` but **neither** `humanGate` nor `approveToken` is on, the run **escalates** (`human-gate-disabled`) instead of silently skipping the human step. A physical gate you declared but did not enable is an error, not something to ignore. This is what lets Goalkeeper drive a hardware-in-the-loop task that genuinely needs a person between rounds without burning its anti-spin budget on the wait.

### CI-fix mode (`fix`, default off)

`fix` points Goalkeeper at a **single red command** (a failing build, a failing test suite, a failing lint) and drives *that exact command* to green. Instead of writing a contract, you hand it a command:

```js
fix: {
  command: "npm test -- auth.spec",   // the red command to drive to exit 0
  shell: "pwsh", cwd: "packages/api", env: { NODE_ENV: "test" },  // optional, same semantics as a check
  goal: "Fix the failing auth tests"   // optional human-readable goal label
}
```

Goalkeeper **synthesizes a one-item contract** whose single check *is* your command (marked `nondeterministic` with a latch policy, so a flaky environment is not read as a code failure), then runs the normal build/verify loop against it. Two specifics:

- **The red output seeds the first build.** Before the first attempt, Goalkeeper runs your command once to **capture the failing output** and feeds it to the builder as the initial signal of what to fix (recorded as an `initial-red` entry in the item's failure ledger), so the builder starts from the actual error, not a blank slate.
- **It cannot game the harness.** The synthesized item forbids editing, stubbing, or weakening the command itself; the only way to converge is to fix the underlying code so the real command passes. The anti-gaming verifier applies as always.

CI-fix mode composes with the other features: it is just a contract the engine generated for you, so `libraryPath`, best-of-N, memoization, and the rest all apply. Re-invoking with the same `fix` **resumes** the in-progress run (the synthesized contract has a stable identity), so a fix that needs several rounds picks up where it left off rather than starting over.

### Human-proven diagnosis (`diagnosis`, default off)

Goalkeeper is strong at **executing** a mechanical fix against a real check; it is weaker at **high-level diagnosis** that needs human judgment or out-of-band observation (a second radio, a scope, a physical symptom). Left free, it will sometimes re-diagnose a problem you already solved and wander off the known fix. `diagnosis` encodes the production-proven driving pattern: you do the decisive diagnosis, then hand Goalkeeper the proven finding so it executes instead of re-theorizing.

```js
diagnosis: "TX corrupts because the status poll runs mid-reception; gate all diagnostic SPI reads to idle and never poll while a reception is latched"
// or scope it to one item of a larger contract:
diagnosis: { text: "...", itemId: "rx-clean" }
```

When set, three things happen for the matching item(s):

- The text is injected into every builder attempt as a **HUMAN-PROVEN DIAGNOSIS** block: trust it, execute the mechanical fix it calls for, and if reality contradicts it, report `blocked` quoting exactly what contradicts it (that is the signal you need) rather than improvising.
- **Re-planning is locked** (`caps.maxReplans` is forced to 0). A builder that requests a contract revision under a diagnosis escalates immediately, with the escalation noting that re-planning was locked because a diagnosis was supplied; that usually means the diagnosis is contradicted by reality, so re-check it before granting anything.
- **Best-of-N is disabled for that item** (a diagnosis and "explore a distinct approach" are contradictory instructions, so the item always gets the single-builder path), and the usual last-retry "take a fundamentally different approach" pressure is replaced with "apply the diagnosis more precisely or report exactly what contradicts it".

Reserve it for findings you actually proved. A guessed "diagnosis" disables exactly the machinery (re-planning, candidate diversity) that would recover from a wrong guess.

### Auto-retro (`retro`, default off)

`retro: true` makes Goalkeeper grow its own operating playbook. On a terminal outcome, one low-effort agent appends a single dated line to **`LESSONS.md`** (at `libraryPath` when the pattern library is on, so lessons are cross-repo; else in the repo's state dir) about how the loop was **driven**: check authoring (gameable vs behavioral, symbol gates), contract scoping (host-testable core vs device integration), diagnosis handling, retry dynamics. It is explicitly not a summary of the code that was built.

It fires on **converge** and on **lesson-worthy halts** (item-stuck, no-progress, oscillation, plateau, budget-exhausted, final-suite-failed, dependency-deadlock, contract-incomplete, self-critique-unactionable, human-gate-disabled, scope-checkpoint). Administrative leash pauses and infrastructure failures do not spend the call. The retro agent holds a high bar: an uneventful run that converged first try with no friction appends nothing. The file is append-only and never affects a run's outcome.

**The lessons feed back.** When `retro` (or the pattern library) is on, the **planner** and the **spec-review** read the accumulated LESSONS.md as advisory context while authoring and reviewing contracts, so a lesson learned failing one contract improves the next one, in any repo sharing the library. Lessons are advisory only and never relax a rule. A lesson appended by a halt also invalidates that halt's cached review verdict, so the next review genuinely reconsiders with the new lesson in view.

## The workflow phases

A run moves through five phases: **Plan -> Setup -> Loop -> Review -> Escalate**.

### Plan (once, only if needed)

If you pass `{ goal }` with no `items[]`, a **PLANNER** agent decomposes the goal into an ordered contract: atomic, independently-checkable items, each with an `expectedOutput`, a machine-runnable `check`, and a `dependsOn` list. The planner is told to make checks exercise real behavior including error/failure paths, not just the happy path, and to keep items small enough to build in one round. If you passed your own `items[]`, this phase is skipped. Either way the resulting contract is persisted to `contract.json`. If the planner returns nothing usable, the run escalates (`planning-failed`).

### Setup (once)

**Adversarial spec-review.** A critic agent attacks the contract itself, looking for gaps, ambiguity, unmeasurable checks, missing acceptance criteria, any `dependsOn` that points at a missing id, and any **environment-dependent check that does not carry `nondeterministic: true`** (treated as a blocking gap, because the loop would otherwise mistake an environmental miss for a code failure). It also **distrusts the check itself**: a check that is *wrong* (it would pass buggy code or fail correct code) or *cheat-able* (a trivial cheat could satisfy it without doing the real work) is a blocking contract gap, and the critic prefers mechanical pass/fail or numeric checks over subjective "looks good" rubrics. It also **refutes premises**: when an item asserts a current defect or fact about the repo ("X is broken"), the critic tries to disprove that claim against the actual repo state, and a premise it can concretely refute (with file:line or command-output evidence) is a blocking gap for the human to decide, never a silent drop or rewrite. One check class is treated as gameable **by rule**: a check that greps a log, serial capture, or console output for a **literal string** is satisfiable by one hardcoded print statement no matter how specific the string, so it blocks unless paired with a companion gate a print cannot fake (a linked-symbol assertion via `nm`/`objdump` on the built binary for a symbol only the real work introduces and which is absent from the pre-work build, a behavioral host test, or a numeric assertion). A sentinel printed by a write-protected harness the builder cannot modify is exempt. The contract *is* the product, and the scariest failure mode is converging flawlessly on the wrong target, so the contract gets reviewed before a single line is built. **Blocking gaps halt the run for human input** (`contract-incomplete`) rather than letting Goalkeeper build confidently toward something underspecified, unless you pass `approvals: ["contract-gaps"]`.

**Repeated review halts get pointed guidance.** The number of consecutive `contract-incomplete` halts on the same contract is tracked durably (`specReviewHalts` in `plan.json`; it resets once the review approves, a round completes, or the contract is amended or fresh-started). From the **third** consecutive halt, the escalation leads with an explicit warning that the check **class** is the problem, not the wording: pair the sentinel with a symbol/behavioral gate, re-ground the contract by reading the actual source, or stop contracting a target that is not machine-checkable and gate the host-testable core instead. This encodes the production lesson that three review halts in a row means hand-patching the sentinel string will only buy a fourth.

**Repeat halts are cheap (rejection replay).** When a run halts `contract-incomplete` and is re-invoked with a **byte-identical contract** at the **same git HEAD** with a **clean working tree** (and, when the lessons file is in play, no newly-appended lesson), the engine **replays the cached rejection** from `plan.json` instead of re-running the high-effort reviewer: the halt counter still increments and a fresh `ESCALATION.md` is written, but the review cost is skipped (about 40 percent of the halt's cost in practice). Replay is **rejections-only**: an approval is never cached, so a pass is always re-earned by a real review. Any contract edit, new commit, dirty tree, or grown LESSONS.md changes the key and forces a real re-review; `approvals: ["contract-gaps"]` still waives the gaps without any review cost.

### Loop (each round; advances at most one item)

1. **Select (dependency-aware).** From the items not yet passing, take those whose `dependsOn` are *all* already passing, and pick the lowest `priority` number among them. One item per round, no more. If nothing is eligible but items remain, the dependencies are unsatisfiable and the run escalates (`dependency-deadlock`).

2. **Scope checkpoint (periodic).** Every `scopeCheckEvery` rounds (default 4; `0` disables), before building, a low-effort agent steps back and asks: is the original goal still the right target, is finishing worth the remaining cost, is what's done already good enough? A recommendation other than `continue` (`stop-good-enough`, `stop-goal-stale`, or `escalate`) halts the run (`scope-checkpoint`) for a human call. The default is `continue`.

3. **Build.** A builder agent implements *only* that one item, then commits. It is instructed to read the current implementation and its call sites before editing, and to fix root cause rather than symptom. It is given the item's `expectedOutput` and told to read `worklog.md` first so it never repeats a failed approach. It is also handed its own **failure ledger** inline: the last few entries of this item's `attemptLog` (each a structured "why it failed + what to change", a Reflexion-style memory) are re-injected directly into the build prompt with an explicit "do not repeat these approaches" instruction, so the builder sees its prior failures without having to reconstruct them from the worklog. On the **last retry** before the item would escalate (item-stuck), the builder is told to take a *fundamentally different* approach or to declare itself **blocked** with a precise reason rather than retrying a near-identical variation.

4. **Living re-plan (only if the builder asks).** If the builder discovers the **contract itself** is wrong (the item needs an unlisted prerequisite, or should be split), it returns a `replanRequest` and the loop revises the working contract (adding and/or splitting items), persists it, and re-evaluates. This is capped by `maxReplans` (default 2); exceeding it escalates (`replan-budget`). It is for plan-is-wrong situations only, not for dodging a hard item.

5. **Verify (authoritative).** An independent verifier, which does **not** trust the builder's report, *or the check's green result*, runs the item's check *and* the full suite, plus a regression re-run of every already-passing item. It reports: regressions, any tampering with protected check files, the resulting git HEAD sha, a tree-id artifact hash, and whether the working tree is clean (a pass with uncommitted source changes is *not* a durable pass). It also returns a concise `failureAnalysis` (why the item failed + what to change) used as that round's failure reflection. This verifier, not the builder, decides whether the item passed. For a `nondeterministic` check it applies the item's `passPolicy` (retry up to `n`, running any `precondition` first, pass on latch or k-of-n) and **latches the tree-hash** on success; a `pipeline` check runs build-then-deploy-then-verify with the build-fail short-circuit; checks declaring a `shell`/`cwd`/`env` run through exactly that shell and environment.

   **Anti-gaming.** Beyond running the check, the verifier *inspects the builder's diff* and asks whether the check passed only because it was **gamed**: hardcoding the exact expected output, special-casing the check's specific inputs, stubbing a constant return, a no-op / `exit 0` / trivial pass, deleting or weakening assertions, or writing the check's expected sentinel without doing the real work. If so it sets `suspectedGaming`, and the engine treats that round as a **failed** round (the new `revert-gaming` outcome) instead of a pass: the round is reverted, it counts against the item's retry budget, and a gamed solution therefore can **never** converge. (A genuinely-wrong item still escalates normally via item-stuck.) Items with `allowTestEdit: true`, which author their own check, are **exempt** from the gaming revert.

6. **Bookkeep.** A bookkeeper agent persists the updated **runtime** `plan.json` (including the item's `attemptLog` failure ledger, appending the verifier's `failureAnalysis` on a failed round and keeping the most-recent few) and appends to `worklog.md`, and **reverts the round** to `prevGoodHead` if the verifier flagged a regression, a tamper, suspected gaming, or any other non-passing outcome. On any failed round, *before* that reset-on-fail rolls the tree back to last-good, the discarded attempt's diff (last-good vs the current working tree, capturing committed or uncommitted work) is saved to `.goalkeeper/last-attempt-<itemId>.patch` so the failed work can be inspected even though the tree was reverted (the patch may be empty if the attempt changed nothing).

### Review (the self-critique gate, when all items pass)

When every item passes, an independent **final** full-suite check runs (`final-suite-failed` if it is not clean). Then, before declaring victory, an **adversarial SELF-CRITIQUE** agent reads the finished work against the goal and hunts for what the checks *missed*: unhandled error paths, edge cases, race conditions, performance cliffs, security gaps, near-placeholder implementations, or work that satisfies the *letter* of the checks while missing the intent. **Green is not the same as good.**

- A **blocking** weakness with a concrete suggested check re-opens the loop as a capped remediation item (the critique budget is `maxCritiqueRounds`, default 1, so this cannot loop forever). In leash mode it escalates (`self-critique`) instead of silently adding work.
- If the critic is *not* satisfied but offers no actionable item, the run escalates (`self-critique-unactionable`) rather than laundering an unresolved concern into a false "converged".
- If the critic is satisfied, the run **converges**, but a converged result can still carry a `weaknesses[]` array and a `selfCritiqueSummary` of **minor** limitations it flagged but did not block on. So a "converged" result may ship with explicitly-flagged limitations; read them.
- If the critique budget is already spent, the run converges without another pass.

The **engine**, not the final-verify agent, is the authority that stamps `status: "converged"` (a focused, retried step decoupled from the cosmetic `REPORT.md`), so a nondeterministic latch-converge and a self-critique re-open can never leave a wrong or premature converged status. The converged result object gains a `statusStamped` boolean recording that the stamp was applied.

## Stop conditions (deterministic, with rationale)

Each of these is evaluated in code at the end of a round. Each cites the prior art it is modeled on.

- **Converged.** Every item passes, an independent *final* full-suite check is green, **and** the adversarial self-critique gate found no *blocking* weakness. Done is always an external check passing, never the builder's self-report. The engine (not the final-verify agent) stamps the converged status, and a `nondeterministic` check that already latched a pass at the current tree-hash is honored at the final suite, so a single flaky miss there cannot un-converge a run that genuinely passed. A converged result may still include `weaknesses[]` + `selfCritiqueSummary` listing minor limitations the critic flagged but did not block on, so "converged" can ship with documented caveats. (Modeled on Aider's zero-exit gate, SWE-agent's explicit `submit`, and Anthropic's evaluator-optimizer pattern, where a separate evaluator signs off on the work.)

- **Item-stuck.** The same item fails its check **3 times** → stop and escalate *that specific item* (the rest of the contract may already be green). Before this fires, the final retry instructs the builder to take a *fundamentally different* approach or declare itself blocked, and each failed attempt feeds the item's `attemptLog` so the builder is not retrying blind. A flaky miss of a `nondeterministic` check at a tree-hash that has already latched a pass does *not* count toward this counter, so an environmental miss cannot escalate code that already proved correct; a genuinely-wrong item that never latches still trips item-stuck normally. A `revert-gaming` round counts as a failed attempt here, so a gamed item is escalated rather than passed. The escalation points at the last discarded attempt's `.goalkeeper/last-attempt-<itemId>.patch`. (Modeled on Aider's `max_reflections = 3`.)

- **No-progress.** For **3 consecutive rounds** (default `maxStalls`), no item newly passes **and** git HEAD does not advance → halt. For a single stuck item the per-item **item-stuck** guard (3 attempts) usually fires first and names the blocking item; no-progress is the loop-wide backstop for churn across several items. The fingerprint recorded each round is `{tree-id, passing-count, head}`. (Modeled on OpenHands-style stuck detection.)

- **Oscillation.** The loop returns to a recently-seen tree-state without the passing-count having increased → halt. Going in circles is treated as being stuck. (Modeled on OpenHands' ping-pong / loop detector.)

- **Plateau** (a best-of-N backstop). The passing-count does not increase for `maxPlateau` consecutive rounds (default 8) → halt with reason `plateau`. This exists because the opt-in best-of-N builder can advance git HEAD by promoting a winning candidate without a *new item* passing, so a run could move while getting no closer to done. On the normal single-builder path it is dominated by **item-stuck** and **no-progress** (which fire first and name the blocking item), so it is effectively a backstop for best-of-N rather than a primary stop.

- **Budget backstop.** `maxIterations` or the token budget is exhausted → enter a **distinct "halted, not done" terminal state** that *always* routes to a human. This is never silently relabeled as success. The halt records *which* limiter tripped via a `budgetKind` field (`"iteration"` for the `maxIterations` cap, `"token"` for the per-run `caps.maxTokens` delta, or `"session"` when the shared turn budget is exhausted), reports the per-run tokens spent, and gives the matching resume advice. The distinction matters because a `"session"` halt will **not** be fixed by raising `caps.maxTokens`; it needs a re-invoke in a fresh turn. (Modeled on Semantic Kernel's two distinct terminal states and LangGraph's `recursion_limit`, whose default is 25.)

The budget backstop and convergence are *different* terminal states on purpose. "We ran out of budget" must never be reported as "we finished."

## Build-mode anti-destruction guards

Under pressure to make a check pass, an unconstrained agent will cheat. These guards make cheating either impossible or self-reverting:

- **Write-protected checks.** The builder may not edit its own check files. `allowTestEdit` defaults to `false`. Any edit to a path under `checkPaths` is detected via `git diff` and the whole round is auto-reverted. (Agents under pressure will "fix" a failing test by editing the test; this closes that door.)

- **Anti-gaming (distrust the green).** A passing check is not trusted on its own. The verifier inspects the builder's diff and, if the check passed only by **gaming** it (hardcoding the expected output, special-casing the check's inputs, stubbing a constant return, a no-op / `exit 0` / trivial pass, deleting or weakening assertions, or writing the expected sentinel without doing the real work), sets `suspectedGaming` and the engine scores the round as the failed `revert-gaming` outcome: reverted and counted against the retry budget. A gamed item can never converge; a genuinely-wrong one still escalates via item-stuck. (`allowTestEdit` items, which write their own check, are exempt.)

- **No placeholders.** No stubs, no TODOs-standing-in-for-work, and no mocking of the very thing under test. Only a full, real implementation counts as a passing item.

- **CI-must-stay-green.** Any round that regresses a previously-green check is reset to `prevGoodHead` and counts as a *failed attempt* against that item's retry budget. Progress moves forward only; the working tree never ratchets backward into a broken state to chase a new item.

## Escalation and resume

Any non-converged stop writes **`ESCALATION.md`** to `<repo>/.goalkeeper/` and then pings Telegram if reachable. The full set of escalation reasons:

- **`item-stuck`**: one item failed its check 3 times. The escalation points at `.goalkeeper/last-attempt-<itemId>.patch`, the diff of the final discarded attempt (which may be empty if it changed nothing).
- **`no-progress`**: 3 consecutive rounds with no new pass and no HEAD advance.
- **`oscillation`**: the loop returned to a recently-seen tree-state without progress.
- **`plateau`**: the passing-count did not increase for `maxPlateau` rounds (default 8); a best-of-N backstop for when HEAD advances but no new item passes.
- **`budget-exhausted`**: `maxIterations`, the per-run token budget, or the shared session turn budget ran out; a `budgetKind` field (`"iteration"` / `"token"` / `"session"`) names which, and the per-run tokens spent and resume advice are tailored to it (a `"session"` halt needs a fresh turn, not a higher `maxTokens`). It points at `.goalkeeper/last-attempt-<itemId>.patch` for the in-flight item's discarded work.
- **`final-suite-failed`**: all items passed individually but the final full-suite check did not.
- **`contract-incomplete`**: the spec-review found blocking gaps in the contract. Consecutive halts are counted (`specReviewHalts`); from the third in a row the escalation opens with pointed check-class guidance (fix the check class, not the wording).
- **`dependency-deadlock`**: items remain but none are eligible (a `dependsOn` is unsatisfiable / points at a missing id).
- **`scope-checkpoint`**: the periodic scope check recommended stopping or asking the human.
- **`replan`**: (leash only) a living re-plan revised the contract and paused for your review.
- **`replan-budget`**: a builder requested another re-plan past `maxReplans`.
- **`self-critique`**: (leash only) the self-critique gate opened remediation items and paused.
- **`self-critique-unactionable`**: the critic is unsatisfied but produced no actionable remediation item.
- **`planning-failed`**: the planner could not produce a usable contract from the goal.
- **`contract-lost`**: a started run found no `contract.json`; re-invoke with `amendContract` or reset.
- **`contract-mismatch`**: an in-progress (or halted) run exists but this invocation passed a *different* contract (different goal or different item ids). The run halts and asks you to choose rather than silently resuming the wrong work.
- **`contractPath-unreadable`**: `contractPath` was set but the file could not be read as JSON. The run fails fast instead of silently falling back to another contract source.
- **`human-gate-disabled`**: a check declares a `humanPrecondition` but neither `humanGate` nor `approveToken` is enabled, so the required physical step cannot be honored. Enable `humanGate: true` (see "Optional power features") and re-invoke.
- **`persist-failed`**: the working contract could not be written to disk (a fatal durability failure).

**`awaiting-human` is not in this set.** When `humanGate` (or `approveToken`) is on and a check's `humanPrecondition` is reached, the run **suspends** (status `awaiting-human`) rather than escalating: it writes `AWAITING-HUMAN.md` (a planned-pause notice carrying a resolution token), not `ESCALATION.md`, and consumes no anti-spin budget. Resolve it by performing the action, writing `resolution.json { token, action: "ready" }`, and re-invoking (see "Optional power features").

`ESCALATION.md` contains: the goal restated; progress so far; the specific blocking item; the actual failing check output; what was already tried (drawn from the item's `attemptLog` failure ledger and the worklog); a pointer to `last-attempt-<itemId>.patch` for the discarded work where one was saved (item-stuck and budget-exhausted); the decision needed; **five one-tap options** (skip / relax / hint / **revise the contract** / abort); and exact resume instructions.

**To resume:** re-invoke goalkeeper (it reads `plan.json` + `contract.json` and picks up where it stopped), or first amend the contract and then re-invoke:

- Relax a check, add a hint, or drop an item, then re-invoke. The persisted contract wins on resume by default.
- To **replace** the contract wholesale, pass `amendContract: true` with the new `contract.items[]`; that overrides the persisted contract.
- To give a stuck item a fresh retry budget on a human-amended resume (e.g. after relaxing its check), pass `resetAttempts: ["<item-id>"]`, which clears that item's retry count, resets the stall counter, **and clears its `attemptLog` failure ledger** so old "do not repeat" guidance cannot contradict your fix.

Because all state is on disk, resuming is just running the skill again against the same repo.

**Resolving via a durable token (opt-in, `approveToken: true`).** If you turned on the durable approval token, you have a second way to resolve a halt that does not require re-invoking with resume args. Each escalation mints a deterministic **token** (printed in `ESCALATION.md`); write **`.goalkeeper/resolution.json`** = `{ token, action }` where `action` is one of `approve` | `redirect` | `abandon` | `hint` | `ready` (with optional `hint` text or `amendItems`). On the next invocation Goalkeeper consumes that token **once** and maps the action onto the same resume levers above (`approve` -> approvals, `redirect` -> `amendContract`/`amendItems`, `resetAttempts` where relevant, `hint` -> a Reflexion hint, `ready` -> latch a suspended `awaiting-human` item's `humanPrecondition` so it proceeds to verify). A token that does **not** match the active halt is ignored and the run stays halted, so a stale resolution file cannot release the wrong escalation.

## Close-out on success

Convergence has its own on-disk artifact, the success analog of `ESCALATION.md`. When a run converges, Goalkeeper writes **`REPORT.md`** to `<repo>/.goalkeeper/` containing: the goal; the outcome (converged); the contract items and their checks (all passing); the final git HEAD; the commits Goalkeeper made; the iteration count; a short summary of what was built; and any minor, non-blocking weaknesses the self-critique flagged. The converged result object also carries a `report: { reportWritten, path }` field pointing at it. A converged run therefore self-documents: you do not have to reconstruct what happened from the worklog. Writing the report also **clears any now-stale halt markers**: a leftover `ESCALATION.md` or `AWAITING-HUMAN.md` from an earlier round of the same run (one that escalated or paused, then later converged) is deleted, so the state dir never shows a halt or pause notice sitting next to a converged run. This is best-effort and runs after the converged status is already stamped, so it can never affect convergence.

**Switching tasks on the same repo just works.** A converged run leaves its state on disk, so the naive behavior would be for the next invocation to reload the finished contract and immediately "converge" again instead of doing the new task. Goalkeeper avoids that: on a new run, if the prior run had **converged** and you pass a **new** goal/contract, it **archives** the old run into `<repo>/.goalkeeper/archive/converged-<short-head>/` (its `plan.json`, `contract.json`, `worklog.md`, and `REPORT.md`) and starts the new task on a clean slate. The previous work in the repo is preserved (it was committed); only the goalkeeper *state* is archived.

**Re-run with nothing new** on a converged repo returns `status: "already-converged"` (pointing at `REPORT.md`) instead of redoing the work. To just check the status of a finished run, re-invoke with no contract.

**`freshStart`.** Pass `freshStart: true` to explicitly ignore and archive any existing goalkeeper state and start fresh. Use it to abandon an **unfinished** (halted or in-progress) run and start a different task on the same repo. A converged run auto-archives when you hand it new work; `freshStart` forces a clean start for **any** state.

**Resume is gated on contract identity.** A **halted** or **in-progress** run **auto-resumes** on the next invocation *only when the incoming invocation is the same task*. Contract identity is the normalized goal plus the **sorted set of item ids** (ids, not descriptions, so wording tweaks do not count as a new contract). If you point Goalkeeper at a repo whose persisted run is in-progress (or halted) but pass a **different** contract (a different goal, or different item ids, supplied inline, via `contractPath`, or as a new goal), it does *not* silently resume the wrong work: it **halts with `contract-mismatch`** and asks you to choose. Your options:

- **Continue** the existing run: re-invoke with **no contract** (or the same one).
- **Replace** the contract in place: pass `amendContract: true`.
- **Abandon** the old run and start the new task: pass `freshStart: true` (archives the old run), or delete the state dir.

This extends the existing close-out behavior, which already archived a **converged** prior run on new work, to **halted** ones, so neither a finished nor an unfinished prior run can be silently overwritten by a different task.

**`contractPath` fails fast.** If `contractPath` is set but the file cannot be read as JSON, the run now fails with `contractPath-unreadable` instead of silently falling back to inline `contract.items` or the planner. A contract you pointed at but Goalkeeper could not load is an error, not a reason to guess.

> Caveat: re-passing the **same** contract after convergence is treated as new work, so it triggers a fresh rebuild. That is cheap (a re-verify, since the code is already committed) but it is not a no-op. To just check status without rebuilding, re-invoke with no contract, which returns `already-converged`.

## Autonomy modes

- **envelope (default).** Runs unattended. It halts only on the hard triggers above (a blocking spec gap, a stuck item, no-progress, oscillation, budget, a dependency deadlock, a scope-check recommending a stop, an unactionable self-critique, or a re-plan past budget). Re-planning and minor self-critique remediation happen *automatically* in this mode, within their caps. This is the "go do it, and bother me only if you're genuinely blocked" mode.

- **leash.** Pauses at a pre-build approval gate and again after every `runRounds` rounds. You re-invoke to continue, passing `approvals: ["start"]` to clear that first pre-build gate (and `approvals: ["contract-gaps"]` to proceed past a spec-review that flagged blocking gaps). In leash mode the contract-mutating gates also pause for your review instead of acting silently: a living re-plan escalates as `replan`, and the self-critique gate opening remediation items escalates as `self-critique`. Because state is durable, **leash is simply envelope run in smaller batches**: same machinery, same on-disk spine, you are just choosing to look in between.

## When to use / when not

**Use it when** the goal has objective, machine-checkable acceptance criteria and the work benefits from iteration:

- build a feature until its test suite is green
- drive an audit down to zero findings
- verify a system until a defined suite passes

**Do not use it for:**

- one-shot edits (just make the edit)
- work that needs fresh human design judgment at each step
- anything that lacks a verifiable "done" signal: Goalkeeper's whole value is the external check, and without one it has nothing to converge on.

## Limitations (honest deviations)

Three things are deferred, all sharing the same safety property (a bad round can never corrupt good work) with fully-understood semantics:

1. **Concurrent execution of different items is deferred.** Dependency-*aware* scheduling is in: items run in a dependency-respecting order. But **item** execution is still **sequential**, one item per round. (The opt-in best-of-N builder does run several candidate builders **for a single item** within a round, but those run **sequentially on the live repo**, not in parallel.) Running **independent items** *concurrently* needs true per-round git worktrees, because concurrent commits to one repo would break reset-on-fail, so it remains deferred.

2. **No true parallel git worktree.** The loop (and best-of-N's candidate attempts) use snapshot-HEAD plus reset-on-fail on the *live* repo, serialized. This preserves the core guarantee (a bad round/candidate is reset to `prevGoodHead`) but proper **isolated parallel worktrees** (which would unlock deferral 1 and wall-clock-parallel candidates) stay deferred: the runtime's worktree isolation was found **non-viable** for an arbitrary target repo, so best-of-N serializes its candidates rather than running them in parallel worktrees.

3. **The wall-clock cap is soft.** The scripts cannot read the clock, so there is no hard time limit. The hard backstops that *do* stop a runaway loop are the iteration count and the token budget.

4. **Large inline contracts can be truncated by the workflow arg channel.** A very large explicit `contract.items[]` passed inline can be cut off in transit. For big or fully-explicit contracts, put the contract in a JSON file and pass `contractPath` (or hand in a bare goal and let the planner build it); a file is read straight from disk and never crosses that channel.

## Hard denylist and kill switch

**Denylist.** The forbidden actions (`git push`, `deploy`, `secrets`, `external-send`) are enforced in **both** autonomy modes, regardless of `mode` or `autonomy`. Goalkeeper operates inside the repo and does not reach outside it.

**Kill switch.** To stop a run, **stop the Workflow** from `/workflows`. To reset Goalkeeper's state entirely, **delete the `.goalkeeper/` directory** (under `<repo>/`). That clears *both* state files, `plan.json` (runtime, including the `attemptLog` failure ledger) and `contract.json` (working contract), plus `worklog.md`, any `ESCALATION.md` or `REPORT.md`, any `last-attempt-<itemId>.patch` snapshots of discarded attempts, the opt-in `results.json` (memoization ledger), `resolution.json` (a pending durable-token resolution), `AWAITING-HUMAN.md` (a pending human-precondition pause notice), and `repomap.md` (the generated repo map), and the `archive/` of past converged runs. (The verified pattern library at `libraryPath` lives **outside** `.goalkeeper/` and is **not** touched by this reset.) The next invocation then starts fresh from the contract you pass in (or re-plans from the goal). You rarely need to do this by hand: a **converged** run self-documents via `REPORT.md` and auto-archives when you give it a new task, and `freshStart: true` archives any leftover state for you. Deleting the directory remains the blunt full reset.

## Example invocation

**With an explicit contract** (note `expectedOutput` and `dependsOn` ordering the work):

```js
Workflow({ scriptPath: "${CLAUDE_SKILL_DIR}/goalkeeper.workflow.js", args: {
  mode: "build",
  autonomy: "envelope",
  repo: "/path/to/your/repo",
  contract: {
    goal: "Add CSV export to the report page with full test coverage",
    items: [
      { id: "export-endpoint", priority: 1, dependsOn: [],
        expectedOutput: "GET /report/export returns 200 with text/csv",
        check: { type: "command", command: "npm test -- export.endpoint" } },
      { id: "csv-formatter",   priority: 2, dependsOn: ["export-endpoint"],
        expectedOutput: "Rows serialize to RFC-4180 CSV, commas and quotes escaped",
        check: { type: "command", command: "npm test -- csv.format" } },
      { id: "ui-button",       priority: 3, dependsOn: ["export-endpoint"],
        expectedOutput: "Report page renders an Export button that hits the endpoint",
        check: { type: "command", command: "npm test -- report.ui" } }
    ]
  },
  checkPaths: ["tests/**"],
  caps: { maxIterations: 20, maxItemRetries: 3, maxStalls: 3, maxTokens: null,
          maxReplans: 2, maxCritiqueRounds: 1, scopeCheckEvery: 4,
          candidates: 1, repoMap: "off" },   // opt-in power features off by default
  // memoize / approveToken default false; omit them to keep the default behavior
  denylist: ["git push","deploy","secrets","external-send"],
  telegram: { chatId: null }
}})
```

**Goal only**: let the planner build the contract:

```js
Workflow({ scriptPath: "${CLAUDE_SKILL_DIR}/goalkeeper.workflow.js", args: {
  mode: "build",
  autonomy: "envelope",
  repo: "/path/to/your/repo",
  contract: { goal: "Add CSV export to the report page with full test coverage" },
  checkPaths: ["tests/**"],
  denylist: ["git push","deploy","secrets","external-send"]
}})
```

Both run unattended: Goalkeeper plans the contract if you gave only a goal, reviews it, builds one item per round (in dependency order) to its check, verifies each independently against the full suite, runs an adversarial self-critique once everything is green, and either converges (all items green, a clean final suite run, no blocking weakness, possibly with minor caveats flagged) or halts and writes `ESCALATION.md` for you to decide.
