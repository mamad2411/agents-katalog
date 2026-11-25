---
name: complexity-budget
description: "Call BEFORE introducing a new component, layer, abstraction, dependency or config — and when a decision starts growing mid-work. Trigger words (RU+EN): новый модуль, обёртка, фабрика, кэш, очередь, ретраи, «на будущее», «универсально», «сделай надёжно», pip/npm/poetry install / new module, wrapper, factory, cache, queue, retries, \"for the future\", \"generic\", \"make it robust\", pip/npm/poetry install. Requires proving the simplest end-to-end path BEFORE infrastructure and adding no more than one source of complexity at a time; every component justifies its existence. Do not skip because a component is «small and obvious» — the cost surfaces at review. Separates an infra failure from a real one. Boundary: this judges solution complexity; implementation quality is code-reviewer."
---

# Complexity budget

An AI agent loves to set up services, caches, retries, queues, extra agents and data sources BEFORE
the simplest end-to-end path is proven. This hides failures: an infra breakage looks like "the
feature does not work", and an unproven baseline like "almost done". This skill sets a **budget on
complexity**.

## The rule
**Add no more than ONE source of complexity at a time.** Keep a proven baseline; each new layer is a
separate step with proof. Complements [[wayfinder]] (planning the scope) and the tracer bullets from
[[task-cycle]] (a vertical slice), but adds an explicit brake on sprawl.

## The implementation ladder (donor: ponytail — DietrichGebert/ponytail)
A component is decided to keep (`keep` per §3) — implement it by the LADDER, taking the FIRST fitting
rung top to bottom:
1. **Needed at all?** — YAGNI; this is the §3 question "needed for the nearest result?": no → skip.
2. **Already in the codebase?** → reuse, do not rewrite.
3. **Does stdlib do it?** → take stdlib.
4. **A native platform/framework feature?** → take it.
5. **An ALREADY installed dependency?** → take it. Do NOT add a NEW dependency — it is a source of
   complexity and an owner's decision (`task-cycle`: "a new runtime/dependency → the owner's
   decision, do not install it yourself").
6. **One line?** → one line.
7. **Only then** — the minimum that works.

Laziness in CHOOSING a solution ≠ laziness in READING the task: read the affected code and trace the
real flow BEFORE the ladder.
Safety invariant: input validation, error handling, security, accessibility — are NOT cut at any
rung.
The seam with §3: §3 decides WHETHER to keep the component; the ladder — given we keep it, in what
minimal form to build it.

## 1. Find the real state (do not conflate 4 things)
Separate: what is **written** · what is **run** · what **passed** · what is an **assumption**.
Status files, comments, "should work" — are CLAIMS until confirmed by a fresh run or an unchanging
artifact. Do not open protected final tests just "to see the progress".

## 2. The nearest result — in one sentence
An observable end-to-end outcome (e.g. "one request goes the whole service path and returns N"). Not
"improve X" but a concrete checkable fact. The simplest working baseline — BEFORE optimization and
automation.

## 3. Inventory: every component justifies itself
For EACH component (service, cache, agent, retry loop, source) — four questions:
1. Which hypothesis does it test?
2. Is it needed for the nearest result?
3. What breaks if removed?
4. Can it be replaced by a manual procedure at the start?

The decision is exactly one: **`keep` · `manual` · `defer` · `remove`**. "Just in case" = `defer` or
`remove`.

## 4. The minimal experiment/step
Freeze the baseline · one question · one variable · a success criterion · a failure criterion · a
budget · a stop condition · an evidence artifact. One step changes one thing.

## 5. Classify the run — EXACTLY one category
- **pass** — the success criterion is met.
- **fail** — the falsification criterion is met, the evidence is valid.
- **infra** — the run is invalid due to an infra breakage (not "the feature is bad" — the run does
  not count).
- **not_run** — there is no terminal evidence.

**infra and not_run are NOT "a bug found/not found".** Counting an infra breakage as a failure =
chasing a phantom (the same line as in [[diagnosing]]: infra/not_run — the run is invalid, fix the
infra, not "the bug").

## 6. The next action — EXACTLY one step
keep/discard/retry/investigate → and declare ONE next step with one source of complexity. Not a fan
of tasks but one checkable bet.

## The deferred-simplification marker (donor ponytail)

A deliberate cut — a simplified form built NOW, with a deferred upgrade (a global lock instead of
per-account, an O(n²) scan, a naive heuristic) — leaves a greppable marker AT THE CUT. In §3 terms
this is a `keep` minimum per the ladder whose UPGRADE is deferred — **not** the §3 decision `defer`
(that defers the component itself, births no code, there is nothing to anchor): `defer:` in the
marker names the deferred upgrade, not the §3 decision. Formerly the cut lived only in the
ANSWER/issue, with no anchor in the code — the linter does not see it, the design corner rots
silently. The marker names BOTH the ceiling AND the return trigger:

    # defer: <ceiling>, upgrade: <what will force a return>
    # defer: global lock, upgrade: per-account locks as throughput grows

**`upgrade:` is mandatory.** A marker without it = `no-trigger` — exactly the corner that rots
silently: what will force a return is unnamed, so you will not return. No honest trigger — the
decision is not a cut but a `remove` or a full `keep`.

**Collection — not a separate skill but a grep:** `grep -rnE '(#|//) ?defer:' .` — the cut registry;
lines without `upgrade:` = `no-trigger`, clear those first. (Example lines in docs/the skill itself
are not cuts: filter with `--exclude-dir` or by eye.)

**Difference from RATCHET (do not conflate the debt classes):** RATCHET is deferred LINT debt
(WPS/mypy), caught by the TOOL, registry in `tooling.md`. This marker is a deliberate DESIGN corner
the linter does NOT see; caught only by grep + eye. The classes do not overlap: the same cut may be
clean by the linter and still carry a `defer` corner.

## The complexity-decision marker (mandatory on a new component)

A component is created — the §3 decision is recorded AS A LINE IN IT. A decision left in the plan or
in the head is indistinguishable from one not made: the plan-checker twice wrote "the complexity
decision is not marked", both times without blocking, and work rolled on.

    # complexity: keep, step <1-7> — <what breaks if the component is absent>
    # complexity: keep, step 4 — native seam of the step registry, adds no code of its own

`keep`, because the file exists: `manual`, `defer` and `remove` birth no code, there is nothing to
anchor in them. The rung answers "why not simpler", the rationale "why at all"; without either the
marker does not count, and the whole form must fit on ONE line.

The line is a COMMENT, with a hash, in `.py` too: a module docstring does not count as a marker. The
discriminator does not parse the language syntax, so it cannot tell a docstring from a quote of the
form in text, and the hash requirement is the only boundary it holds honestly.

**Executed by a machine.** The gate step `complexity_trace` reddens on a new code file — `.py` or
`.sh` — without this line.
What is judged is what was ADDED against the main branch, so old files are not required to carry the
line, and a rename does not count as creation. Files that were already there when the project adopted
the kit (the first commit that adds `.retainer/`) are not judged either, even when a long-lived branch
shows them as added; a file created again at a path deleted since then is. Not judged are tests, documentation, presets,
generated migrations, foreign trees lying in the repository, and an `__init__.py` with no code — a
package declaration is not a component, while a package facade that does have code is judged on par
with the rest. Whether what is written is true is not checked: it is a self-declaration, and judging
the content of the rationale means building an over-engineering detector, and that is the reviewer's
job.

**The decision unit is a component, the check unit is a file.** A module split by linter thresholds
into a dozen files is one component and one decision; the line is written into each of its files,
the wording shared. The machine does not and does not try to parse where a component ends.

**In an autonomous run a red step is no reason to stop.** The decision is made by whoever creates
the component, and records it with this same line; no blocking question to the owner arises here.

**Three debt classes, do not conflate, each with its own collection:**

| marker | what it means | who catches it |
|---|---|---|
| `complexity:` | the component exists and named why it is needed | gate step |
| `defer:` | the component is deliberately simplified, the upgrade deferred | grep + eye |
| RATCHET | deferred lint debt (WPS/mypy) | the linter, registry in `tooling.md` |

Collection is the same grep: `grep -rn 'complexity: keep' .`. Example lines in docs and in this skill
are not components — filter with `--exclude-dir` or by eye, as with the deferred-simplification
marker.

## The answer for this skill (structure)
First the current outcome, then: the nearest result · the proven baseline · the component budget
(keep/manual/defer/remove; for each `keep` — the implementation-ladder rung) · the class of the last
run · partial findings · the complexity verdict · exactly one next step · what remains after success.
A paragraph defending a simplification is complexity itself, smuggled in as prose: the explanation of
a cut longer than the cut → cut the explanation, and put the decision in the greppable cut marker
(above), not in prose.

## Where an accepted "below standard" is recorded

A decision "we take it as a prototype, finish it later" is not a weakened check and not a caught
defect, and it is not written into their journals. Its home is a marker in the code itself:
`# prototype: #<task number> — <what replaces it>`, the inventory collected from the tree by a gate step.
A record outside its own journal is lost: a weakened linter recorded as a prototype will not reach
the concessions audit, and a prototype recorded in the error journal reads as a bug already fixed.

## When NOT to apply
Complexity is REALLY needed for the nearest result (not "just in case") — keep it, do not cut. The
skill is against the SPECULATIVE/premature, not against the necessary. It is not a ban on building
but a ban on building WITHOUT a proven baseline.

Related: [[wayfinder]], [[task-cycle]], [[diagnosing]]. Optional — a deterministic audit-record
validator (exit 0=ready / 2=the complexity gate blocks / 1=malformed), as in the original; not ported
yet.
