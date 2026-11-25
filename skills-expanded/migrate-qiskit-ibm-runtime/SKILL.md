---
name: migrate-qiskit-ibm-runtime
description: Migrate a qiskit-ibm-runtime workload from any older version up to the latest release — and, when the installed runtime supports it, onward to the client-side (Executor-backed) SamplerV2/EstimatorV2. Primitives are the bulk (V1 primitives -> V2 interface, and server-side V2 -> client-side V2), but it also routes non-primitive breaking changes (auth/channel, backend.run(), result streaming, custom programs). Use when the user runs /migrate-qiskit-ibm-runtime, or asks to migrate/upgrade/port qiskit-ibm-runtime code, to move off the V1 primitives (quasi_dists/.values/pre-pub .run(...)), or to the client-side / Executor-backed / directed-execution-model / executor_sampler/executor_estimator primitives.
---

# migrate-qiskit-ibm-runtime

<!--
  HOW THIS SKILL WORKS
  ────────────────────
  This file is the prompt Claude Code receives when /migrate-qiskit-ibm-runtime
  is invoked. Everything from the "Instructions" heading onward is what Claude
  executes.

  The skill migrates a qiskit-ibm-runtime workload from ANY older version up to
  the latest release. It is CHANGE-AGNOSTIC and VERSION-DRIVEN: it supports many
  migration CHANGES (breaking changes, grouped by DOMAIN), each described by an
  entry in registry.yaml with a version window and detection triggers. This file
  NEVER enumerates a specific breaking change inline — the per-change specifics
  live in each change's grounding guide (a local file, or a live `url` for the
  documented ones), which the skill reads and treats as the authoritative source
  of truth for every edit, rather than relying on general knowledge. The generic
  apply rule is: a mechanical, results-preserving change is applied
  automatically; anything that changes results or needs a human decision is
  flagged and confirmed.

  PRIMITIVES ARE THE BULK. Primitives are the primary interface, so primitive
  changes dominate a real migration. The non-primitive domains (account-channel,
  execution, programs, misc-deprecations) are authored too, grounded in the shared
  migrate-non-primitive-apis.md guide. A change can still be marked `placeholder`
  (detected + reported, not edited) when it is routed before its actions are
  written — Phase 3 handles that, but no change ships as a placeholder today.

  TWO-LAYER DESTINATION (see registry `target_rule`):
    Hop A — reach the latest DOCUMENTED API (changes grounded in a release-note /
      migration-guide `url`).
    Hop B — adopt the CLIENT-SIDE (Executor-backed) primitives. Fully released in
      qiskit-ibm-runtime 0.50.0, which also DEPRECATES the server-side
      SamplerV2/EstimatorV2 in favor of them, and grounded in a PUBLISHED
      migration guide (registry `url` / `companion_url`) like any hop-A change.
      Run hop A before hop B, and attempt hop B only when the INSTALLED runtime
      is >= 0.50.0.

  STRUCTURE
  ─────────
  Phase 1 — Read the registry; determine scope + source/target versions.
  Phase 2 — Detect which change(s) apply (by trigger match and/or version window).
  Phase 3 — Dispatch: ground in each change's guide (local) or url (documented).
    Placeholder changes are reported but not applied.
  Phase 4 — Rewrite the imports per the change's import_rewrite.
  Phase 5 — Walk the guide's incompatible-changes checklist; apply mechanical
    fixes, flag results-changing ones.
  Phase 6 — Verify: imports resolve and option paths are valid (self-contained;
    does not depend on the guide).
  Phase 7 — Report what changed, what was flagged, and what to test.

  FILE PATHS (relative to repo root)
    Registry: .claude/skills/migrate-qiskit-ibm-runtime/registry.yaml
-->

## Instructions

You are migrating a **qiskit-ibm-runtime** workload from an older version up to the **latest
release**, and — when the installed runtime supports it — onward to the new **client-side**
(Executor-backed) `SamplerV2` / `EstimatorV2`. The workload may exercise many breaking changes
across releases; each is a *change* described in `registry.yaml`, grouped by *domain*
(**primitives** are the bulk; account-channel, execution, programs, and misc-deprecations are the
rest). Your edits must be grounded in the selected change's guide — a local file, or a live `url`
for the documented ones — not in general knowledge. Follow these phases in order. Do not skip
Phase 1.

---

### Phase 1: Read the registry and determine scope + versions

Read `.claude/skills/migrate-qiskit-ibm-runtime/registry.yaml`. It enumerates every supported
change with its domain, version window, detection triggers, grounding source, and status. Read
`target_rule` in full — it defines the **two-layer destination** (hop A = latest documented API;
hop B = client-side primitives, released in `0.50.0`, grounded in a published guide) — and note
`min_runtime_version` and each change's `status`.

Parse `$ARGUMENTS` for up to three things:
- **Scope** — a file or directory to migrate. If none is given, default to the current working
  tree and **ask the user to confirm the scope before editing anything**.
- **Forced change (optional)** — a registry change `id` (e.g. `v1-to-v2`, `server-to-client`,
  `account-channel`) or an unambiguous phrase. If present, use it instead of auto-selecting, but
  still run Phase 2 detection as a sanity check and **warn if the code shows no `detect_primary`
  signal and the version window doesn't include it**.
- **Flags (optional)** — e.g. a request to add INFO logging (see Phase 5).

**Determine the source and target versions** (opportunistic — a precise source version is *not*
required):
- **Source (lower bound on age).** Infer how old the code is from the **oldest** deprecated form
  still present: e.g. `IBMSampler`/`IBMEstimator` ⇒ pre-0.5, `auth=` ⇒ pre-0.3, `IBMRuntimeService`
  ⇒ pre-0.6, `circuit_indices` ⇒ pre-0.15, `quasi_dists`/`.values` ⇒ the V1 era (pre-0.28),
  `backend.run(` ⇒ pre-0.35, `channel="ibm_quantum"` ⇒ pre-0.42. Accept a user-supplied source
  version if given. If nothing pins it, say so and proceed on trigger matches alone.
- **Target.** Read the **installed** `qiskit-ibm-runtime` version (e.g.
  `python -c "import qiskit_ibm_runtime as q; print(q.__version__)"`). This fixes the latest
  reachable API and decides whether **hop B** (client-side primitives, `>= 0.50.0`) is available.
  If the package isn't installed, note that hop B can't be verified and continue with what you can.

---

### Phase 2: Detect which change(s) apply

Grep the scoped code against **every change's `detect_primary` and `detect_secondary`** lists.

- A `detect_primary` match (usually the import source or a symbol absent from modern code)
  **assigns** the change.
- A `detect_secondary` match is broad and corroborating only — record the file path, line number,
  and the **literal matched line's text**, and carry it forward so the user can eyeball-confirm a
  genuine usage. Never assign a change on a secondary match alone.
- **Include a change if EITHER a trigger matches OR the inferred source version falls in
  `[applies_from, applies_to)`.** For a `code_evidence: environment` change (state not visible by
  grepping source, e.g. which fake-backend classes exist), rely on the version window and **say so**
  rather than staying silent.
- Apply each change's `already_migrated` substrings as an **early exit**: a usage already on the
  destination (e.g. importing from `executor_sampler` / `executor_estimator`) is reported and
  skipped, unless there are still un-migrated usages elsewhere.

If a **forced change** was given, honor it (with the warning above). Otherwise select every change
that detection or the version window includes. **Group detected changes by `domain`** for the
report, and **do not migrate a construct you have not read** — read enough surrounding code (PUB
construction, options tree, result post-processing, try/except blocks, account setup) to know which
checklist items actually apply.

---

### Phase 3: Dispatch and ground in each change's guide

Process detected changes in `order` (ascending), which puts documented **hop-A** changes before the
client-side **hop-B** destination. For each:

- If its `status` is `placeholder`, **or** its guide source cannot be resolved (no `url` and the
  local `guide` file is missing or absent), **report the change as recognized but not yet supported
  and make no edits for it.** Say what would migrate and that the actions are not authored yet. This
  is how the non-primitive domains behave until their guides are written.
- Otherwise resolve the grounding: **if the entry has a `url`, fetch it** (WebFetch, or the
  `qiskit-docs` MCP tools `search_docs_tool` / `get_page_tool`); **otherwise read the local `guide`
  file** in full. Each change has **exactly one** of the two — a published page, or a local guide
  file in this folder — so there is **no local fallback for a `url` entry**: if the fetch fails, say so and
  make **no edits** for that change rather than migrating it from memory. Hop B is `url`-grounded
  like hop A; the client-side primitives have their own published migration guide. Treat the guide's
  incompatible-changes table(s) and worked sections as the authoritative checklist for Phase 5. If
  any input, output, or option is unclear, consult the reference links at the bottom of the guide
  before guessing.
- **Companion guides.** If the change entry has a `companion_guide` or a `companion_url` (or the
  guide states that it inherits/shares changes with another guide), resolve and read that companion
  too — `companion_url` is fetched, `companion_guide` is read locally — and treat its checklist as
  **part of this change's checklist** in Phase 5.
  This is how a compound change (for example `v1-to-v2`, whose client-side destination is documented
  in the shared server-to-client guide) picks up the shared changes without duplicating them.
- **Guides that link onward to another published guide** (for example the client-side guide pointing
  at the `NoiseLearner` → `NoiseLearnerV3` migration) are part of the grounding when the code you
  are migrating touches that surface: fetch the linked page too rather than working from general
  knowledge. Doc links are written root-relative (`/docs/guides/...`); prefix
  `https://quantum.cloud.ibm.com` to fetch them.
- **Only attempt hop B (client-side) when the installed runtime is `>= 0.50.0`.** If it is older,
  complete hop A, then report that the client-side destination requires an upgrade and stop short of
  claiming the client-side migration is done.

---

### Phase 4: Rewrite the imports

Apply the selected change's `import_rewrite` (from → to) pairs from the registry. Keep this generic
editing discipline (it holds for any change):

- Migrate **only** the primitives/symbols the user actually uses.
- If the migrated names share a single `from ... import ...` line with other names, **split the
  line** so only the migrated names move to their new modules while unrelated names
  (`QiskitRuntimeService`, `Batch`, `Session`, `NoiseLearnerV3`, …) stay on the original import.
- Preserve any aliases (`SamplerV2 as Sampler`) and the code that depends on them.

Any change-specific import caveat (for example, "don't collapse to the future top-level form") comes
from the guide and the registry entry's `note` — surface it, don't hard-code it here.

---

### Phase 5: Apply the guide's incompatible-changes checklist

Walk each row of the guide's incompatible-changes table(s) against the usages found in Phase 2. The
guide is the source of every specific change; this file only carries the generic policy:

- **Apply automatically** when the migration action is a mechanical, results-preserving code change.
- **Flag for a decision** (don't silently rewrite) anything that changes results or needs a human
  choice — present it as a concrete diff and confirm before applying.
- Group your output into **"applied automatically"** and **"needs your decision,"** and **cite the
  specific guide table row** (and the change `id` it belongs to) for every item so the user can
  trace it back.

Editing directives that the guide's terse rows do **not** spell out, and that you must apply on any
change:
- **When changing a caught exception type, *widen* the `except` tuple — don't replace it.** If the
  same block guards other calls, keep the original type and add the new one (e.g.
  `except (IBMInputValueError, RuntimeError)`).
- **Present results-changing structural rewrites as a diff and confirm** — job splitting for mixed
  shots/precision, and the explicit PEA/PEC noise-learning rewrite, change the run structure.
- **Offer opt-in additions rather than forcing them** — e.g. INFO logging: add it only if the user
  agrees or `$ARGUMENTS` requested it.
- **When a change splits one job into several**, follow the guide's *submit-all-then-collect*
  ordering. Try to submit as few jobs as possible. Group the inputs by the value that forced the
  split (one job per distinct value) — splitting regroups PUBs, it never duplicates them.
- **Never invent an API path.** Attribute and key paths into results, job metadata, and job inputs
  (`job.inputs[...]`, `job.result().metadata[...]`, result data fields) are only what the guide
  enumerates. If the guide does not show the path you need, say so and consult its reference links
  — do not extrapolate a plausible-looking one.
- **Don't copy a literal option value out of a guide's worked example — derive it from the
  source code you're migrating.** A guide's code sample picks a concrete value (e.g.
  `twirling_strategy="all"`) to illustrate the mechanism; that value belongs to *that example*,
  not to every migration that touches the same option. If the source left the option unset,
  carry over *its class's documented default* (check the source option class's docstring/field
  default — don't assume it matches the destination API's own default, the two often differ), not
  whatever value happens to appear in the guide. A wrong-but-plausible value here changes results
  silently — it won't raise, and Phase 6's local verification only checks option paths/types, not
  behavior — so re-derive rather than pattern-match.
---

### Phase 6: Verify

These checks catch the most common breakage without submitting hardware jobs. They test the shared
**client-side destination** (hop B), so they are the same regardless of which change led there, and
are kept self-contained here (they do not depend on the guide, which may be remote).

These checks exercise the **migrated** code. Very old source (the guide's "Older V1 syntax you may
need to modernize first" forms — `IBMSampler` / `IBMEstimator`, `IBMRuntimeService`,
context-manager/constructor-input usage, `circuit_indices` / `observable_indices` — as well as
removed non-primitive surface like `backend.run()`) generally won't even import on a current
`qiskit-ibm-runtime`, so run these checks only **after** the legacy forms have been normalized and
rewritten — never against the original code to conclude the migration failed.

- **Imports resolve.** In the project environment, confirm
  `from qiskit_ibm_runtime.executor_sampler import SamplerV2` and
  `from qiskit_ibm_runtime.executor_estimator import EstimatorV2` import cleanly. If they fail with
  `ModuleNotFoundError`, the installed `qiskit-ibm-runtime` predates the client-side implementations
  (registry `min_runtime_version`: 0.50.0) — report the required upgrade and stop short of claiming
  the client-side (hop-B) migration is complete.
- **No server-side primitive is left behind.** As of 0.50.0 the server-side `SamplerV2` /
  `EstimatorV2` classes are **deprecated** and
  constructing one emits a `DeprecationWarning` naming `qiskit_ibm_runtime.executor_sampler.Sampler`
  / `qiskit_ibm_runtime.executor_estimator.Estimator` as the replacement. If that warning appears
  while verifying, a hop-B usage was missed: find the remaining server-side construction and migrate
  it. The "have no effect in local testing mode" options warning below means the same thing.
- **Option paths are valid.** For any options the code sets, construct the primitive against a fake
  backend (e.g. `SamplerV2(mode=FakeManilaV2(), options=...)`) and run a small circuit through it to
  catch renamed/invented attributes before the user hits them at run time. Prefer a **small** fake
  backend here regardless of which QPU the workload targets — this step checks option paths, and
  mitigation now really runs locally (see below), so a 100+ qubit fake device buys nothing and can
  exhaust memory.
  - **Always Cliffordize the circuit before running it in local mode.** A fake-backend run uses a
    statevector/noisy simulator, whose cost grows exponentially with qubit count and depth — a
    realistic workload circuit can hang or exhaust memory. Since the goal here is only to exercise
    the *option paths and types* (not to reproduce physical results), reduce the circuit to a
    Clifford one first: Clifford circuits simulate efficiently (stabilizer simulation) regardless of
    size. Use `ConvertISAToClifford`, which rounds each `RZ`/`RZZ`/`RX` angle to the nearest multiple
    of π/2:
    ```python
    from qiskit.transpiler import PassManager
    from qiskit_ibm_runtime.transpiler.passes import ConvertISAToClifford

    clifford = PassManager([ConvertISAToClifford()]).run(isa_circuit)
    # then run `clifford` (not the original) through the fake-backend primitive
    ```
    `ConvertISAToClifford` **requires an ISA circuit** as input (the output of
    `generate_preset_pass_manager(...).run(...)` targeting the backend) — it raises `ValueError` on
    any non-ISA gate. If the code you are verifying builds an abstract circuit and never transpiles
    it, transpile it to the fake backend's ISA first, then Cliffordize. This is a verification-only
    transformation: never apply it to the circuit the user actually submits to hardware, since it
    changes the computation.

    Two consequences of Cliffordizing that will break the local run if you don't account for them
    (both confirmed against 0.50.0):
    - **The `.layout` attribute is dropped.** The Cliffordized circuit keeps the same qubit count but
      `clifford.layout` is `None`, so `observable.apply_layout(clifford.layout)` fails. For Estimator,
      lay the observable out from the **pre-Clifford ISA** circuit:
      `isa_obs = observable.apply_layout(isa_circuit.layout)`, then run `(clifford, isa_obs)`.
    - **Parameters are bound away.** Rounding the rotation angles turns a parametric ISA circuit into
      a concrete Clifford one — `clifford.num_parameters` becomes `0`. A PUB that still carries a
      parameter-values array will then fail coercion ("Length of () inconsistent ..."). For local
      verification, drop the parameter array from the PUB (e.g. `(clifford, isa_obs)` instead of
      `(clifford, isa_obs, values)`); the real hardware run keeps the original parametric circuit and
      its values untouched.
- **Syntax.** Byte-compile the changed files (`python -m py_compile <files>`).

Run these via Bash. If the environment can't be set up (no `qiskit-ibm-runtime` installed), say so
and mark verification as skipped rather than asserting the code works.

**What a fake backend can and cannot verify.** Local testing mode (`Fake*` backends) is useful but
does not exercise the real service path, so be precise about what a green run actually proves — do
not over-claim:

- **Error suppression and mitigation DO take effect locally on the client-side primitives.** As of
  0.50.0 the client-side (Executor-backed) primitives apply `twirling`, `dynamical_decoupling`, and
  the `resilience` methods in local testing mode, so a fake-backend run exercises the mitigation
  code path itself rather than only the option names (confirmed on 0.50.0: the same Bell-state `ZZ`
  estimate on `FakeManilaV2` moves from `0.870` at `resilience_level=0` to `0.984` with
  `zne_mitigation=True`, with **no warning emitted**). Three things still to be precise about:
  - **It is not a prediction of hardware results.** A fake backend's calibration data is a one-time
    snapshot of its real counterpart, and QPU noise drifts, so local numbers will not match what the
    device returns. Report a green local run as evidence the code is correct, never as expected
    hardware output.
  - **Mitigation simulation costs memory.** The extra circuits (noise factors, twirling
    randomizations) multiply the simulation, so a large fake backend can exhaust memory. When the
    goal is only a syntax/option-path check, drop to a **small** fake backend (`FakeManilaV2`, 5
    qubits) or a noiseless `AerSimulator`, and Cliffordize as below. On a noiseless backend, ZNE has
    nothing to extrapolate from and warns "No positive, finite standard errors were found; falling
    back to an unweighted fit" — benign, and expected there.
  - **The deprecated server-side primitives still ignore these options locally.**
    `qiskit_ibm_runtime.SamplerV2` / `EstimatorV2` on a fake backend emit `UserWarning: Options
    {...} have no effect in local testing mode` and return the unmitigated value (confirmed on
    0.50.0). Treat that warning as a **signal you are verifying pre-hop-B code**, not as benign: the
    migration to the `executor_*` primitives is incomplete.
- **`NoiseLearnerV3` has no local testing mode.** If your migration added an explicit noise-learning
  step (the guide's PEA/PEC section), you **cannot** run `NoiseLearnerV3` against a fake backend to
  verify it: its `mode` accepts only a real `Backend`, `Session`, or `Batch`, so there is no
  simulator path. Do not attempt to construct or run it locally. Instead, verify the noise-learning
  code by checking it against the API reference —
  https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/noise-learner-v3-noise-learner-v3.md
  — confirming the constructor, `run(instructions)` input shape, and the unique-layer helper are
  used as documented. Byte-compile still applies, but state clearly in the report that this part is
  API-reference-verified only, not executed.
- **`Session`/`Batch` CAN be constructed and run locally against a fake backend** — unlike
  `NoiseLearnerV3` above, do not skip this. `Session(fake_backend)` / `Batch(fake_backend)`
  construct without contacting any service, and `SamplerV2(mode=session)` /
  `SamplerV2(mode=batch)` run exactly like passing the backend directly — local testing mode has no
  session/batch concept, so it silently ignores the wrapper and executes locally (confirmed against
  0.50.0: the returned job is a `LocalRuntimeJob`, no warning is emitted). This does **not** verify
  session/batch semantics (queueing, `max_time`, sharing a backend lock across jobs) — only the
  *option paths and call syntax* around `mode=session` / `mode=batch`, same as any other fake-backend
  check. Use it to confirm the migrated `Session`/`Batch` construction and the primitive calls inside
  it are well-formed, then note in the report that session/batch-specific behavior itself is
  reference-verified only.
  - **This is exactly how the `job.queue_info()` removal (see the `job-management-removed` change)
    was caught**: running a `Session`/`Batch`-wrapped call against a fake backend produced a
    `LocalRuntimeJob` whose `dir()` had no `queue_info` — which then turned out to be true of the
    real-service `RuntimeJobV2` too (confirmed against its API reference, not just the local job
    class). A fake-backend run surfaces a missing/renamed job-object attribute exactly like it
    surfaces a missing option-tree attribute; don't assume such an `AttributeError` is a
    local-testing-mode-only artifact without checking the real job class's API reference too.

---

### Phase 7: Report

Summarize in plain prose:

1. **Versions** — the inferred source version (or "unpinned"), the installed/target version, and
   whether the client-side **hop B** is available (`>= 0.50.0`).
2. **Change(s) applied** — grouped by `domain`, which change each file was assigned to, and any file
   reported as already-migrated or recognized-but-placeholder (non-primitive domains that were
   detected but whose actions aren't authored yet).
3. **Files changed** and the import rewrites made.
4. **Applied automatically** — each fix, with the guide table row (and change `id`) it came from.
5. **Needs your decision** — each flagged item, why it can change results, and the proposed change
   (as a diff where useful). The PEA/PEC noise-learning rewrite, if present, goes here.
6. **Verification** — what passed, what was skipped and why.
7. **Before you run** — that the migration proceeded in two layers: **hop A** brought the code to the
   latest documented API, **hop B** adopted the client-side primitives — the destination IBM
   recommends as of 0.50.0, which deprecates the server-side `SamplerV2`/`EstimatorV2`. Remind that
   client-side jobs may take longer (offer INFO logging if not already added).

Do not claim the workload is fully migrated if any flagged item is unresolved, verification was
skipped, or a detected non-primitive change is still a placeholder — say exactly what remains.
