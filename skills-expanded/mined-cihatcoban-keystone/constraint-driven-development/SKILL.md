---
name: constraint-driven-development
description: Turns a project's quality bar into a written contract with numbers and stops agents quietly lowering it. Triggers - what coverage target should we set, define our quality standards, agent keeps disabling checks or skipping tests to get green, what threshold to use.
---

# Constraint-Driven Development

Other skills describe what good looks like. That description lives in prose an
agent may or may not follow, and it evaporates when the session ends. This skill
produces something else: **this project's bar, with numbers, in a file, checked
mechanically.**

The failure it prevents is specific and common: an agent meets a constraint by
weakening it. Coverage gate fails → threshold lowered. Type error → suppression
added. Flaky test → skipped. Each step is locally reasonable; the sum is a
project with no standards and a green pipeline.

## Producing the contract

1. Copy `templates/CONSTRAINTS.template.md` to the project root.
2. Interview — one dimension at a time, not a questionnaire dump. For each:
   *"Do you have a number in mind, or should I propose one?"*
3. For every dimension the user has no number for, propose the default below,
   say what it costs and what it buys, and let them adjust.
4. Record the **current measured value** alongside the target. A target below
   today's reality is a ratchet backwards; a target far above it needs a ramp.
5. Wire each threshold to a command that checks it. **An unchecked threshold is
   not a constraint, it is a wish** — delete it or automate it.

## Default thresholds

Starting points, not laws. Say they are adjustable.

| Dimension | Default | Reasoning |
|---|---|---|
| Overall line coverage | 70% | Above this, cost rises faster than value in typical CRUD code |
| Core domain coverage | 90% | Business rules are where silent wrongness is expensive |
| Diff coverage | 85% | Ratchets quality up without a rewrite |
| Cyclomatic complexity | ≤ 10 per function | Above 10, review misses branches |
| PR size | ≤ 400 changed lines | Review quality collapses past this |
| Critical path latency | p95 under 300 ms | Perceived-instant boundary for interactions |
| Build + fast tests | ≤ 10 min | Longer and people stop running them |
| Availability SLO | 99.9% | Start here; raise only with the ops maturity to back it |
| Known high/critical CVEs | 0 | Non-negotiable |
| Secrets in repo | 0 | Non-negotiable |
| Flaky tests | 0 unquarantined | A tolerated flake teaches everyone to ignore red |

Two of these are never negotiable defaults: secrets and known critical
vulnerabilities. Everything else is a trade-off the team owns.

## Validate the instrument before trusting the number

A gate that measures the wrong thing is worse than no gate: it blocks good work
or passes bad work, and it does so with authority. Before a threshold gates
anything, prove the measurement is real:

1. **Break it deliberately.** Delete a test, or a line of coverage, and confirm
   the number moves in the direction and magnitude you expect.
2. **Check the denominator.** Coverage tools disagree about what counts as an
   executable line; complexity tools disagree about what counts as a branch.
   Read one file's report by hand and confirm it matches reality.
3. **Check what is invisible to the tool.** Work in threads, subprocesses,
   generated code or code imported before instrumentation started is routinely
   missed — a coverage figure that excludes your concurrency tests is fiction.
4. **Record what the tool cannot see** next to the threshold, so the next reader
   knows the number's scope.

A suspiciously low number is usually a broken instrument; a suspiciously high
one usually means the denominator is wrong. Investigate both before changing
any code.

## Ramps, not cliffs

A legacy project at 30% coverage cannot adopt 70% today. Write both:

```text
Coverage: current 31% · target 70% · gate: diff coverage ≥ 85%, overall must not decrease
```

The diff gate makes every change improve the average without a rewrite. Revisit
the absolute target quarterly.

## Watching the diff

On every change, scan for bar erosion before reviewing anything else:

| Signal | What it usually means |
|---|---|
| New suppression comment | A real type or lint error was silenced |
| Test deleted or skipped | The test caught something inconvenient |
| Assertion weakened (`toBeTruthy`, `assert x`) | The expected value changed and nobody decided whether it should |
| Threshold edited down in a feature PR | Reaching green by moving the line |
| `catch {}` / `except: pass` added | An error path became invisible |
| Golden file and its producing logic changed together | The oracle was rewritten to match the output |
| Stub left with a passing test | Interface exists, behavior does not |

Response is always the same: **stop, state what was found, state the honest
alternative** (fix it, or lower the bar deliberately in its own PR), and let a
human choose. Never proceed on the quiet lowering.

## When not to use this

Throwaway prototypes, spikes with a stated delete date, and one-off scripts.
Say the exemption out loud and put an expiry on it — "prototype until Friday"
— because the most common way constraints die is a prototype that shipped.

## Exit checklist

- [ ] `CONSTRAINTS.md` exists at the project root with no blank thresholds
- [ ] Every threshold names the command that measures it
- [ ] Each measurement was validated by breaking something and watching the number move
- [ ] Current measured values recorded next to targets
- [ ] Where current is far from target, a ratchet gate is in place
- [ ] Bar-protection triggers are enforced in review and CI
- [ ] Lowering a number is documented as requiring its own PR
