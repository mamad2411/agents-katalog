---
name: anti-hallucination-gates
description: Use before claiming done/fixed/passing — or before asserting something is absent: not installed, not available, no such function, couldn't find it. Default-FAIL runs both ways — every claim needs an evidence path. A negative claim must carry its search scope and observation date; state calibrated uncertainty when evidence is missing.
---

# Anti-Hallucination Gates

The most common agent failure is **declaring victory too early**. This skill is the gate between "I think it works" and "evidence proves it works".

## The Iron Rule

> No claim of "done" / "fixed" / "passing" without a concrete artifact path proving it.

A claim like *"I fixed the bug"* is incomplete. The proper form:

> "Fixed by commit `abc123`. Test `tests/foo.test.ts::handles-edge-case` now passes (output captured in `.harness-anchor/test-2026-05-28.log`). Build still passes (`.build/last-build.log` exit 0)."

## The Iron Rule runs both ways

The rule above governs claims that something IS. Claims that something IS NOT are
the same failure with the sign flipped, and until v0.17.0 this skill said nothing
about them.

> No claim that something is **absent** without stating the scope you actually
> searched and when you looked.

*"clang-tidy isn't installed on this machine"* is incomplete in exactly the way
*"I fixed the bug"* is incomplete. The proper form:

> "searched PATH + the VS-bundled LLVM and CMake directories, not found (as of 2026-07-29)"

### Two classes, two probes

| Class | Sounds like | What counts as evidence |
|---|---|---|
| **Capability** | "not installed", "not available here", "this platform can't do X" | The search chain's **coverage** plus the **date you looked**. C/C++ tools: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/cpp-tool-discovery.sh <tool>` — its `NOT_FOUND` line already enumerates its own scope. Other ecosystems: `command -v` **plus** that platform's known install locations. |
| **Search** | "there's no such function", "nothing tests this", "that option isn't in the config" | The **command you actually ran** and its **coverage**: which paths, which glob, case-sensitive or not, whether ignored files were included. |

An empty result proves only that *your search* found nothing. That is a different
proposition from *the thing is absent*, and conflating the two is what this
section exists to stop.

### The "there is no" detector

The mirror of the "should" detector further down. When you are about to type
*not installed*, *doesn't exist*, *isn't supported*, *couldn't find*, *there is
no* — stop. Either:

- **Widen the search**, then state the coverage you reached. Capability → run the
  discovery chain, not just `command -v` / `where`. Search → loosen the glob, drop
  case sensitivity, include ignored files.
- **Or scope-and-date the claim** in the mandated form above.

### Out of scope, deliberately: judgement-shaped negatives

"This is impossible", "that approach won't work", "the library can't do this" are
NOT covered here. They carry no executable evidence path, and pulling them in
would turn a verifiable contract into unverifiable moralising — softening the very
invariant this skill holds (CLAUDE.md #8). State them as the judgements they are,
with reasoning. Do not dress them up as findings.

### Residual blind spot — read this before trusting the section above

This contract binds only when this skill is **loaded**, and it loads from its
description. A negative assertion made in a turn where the description didn't
match is entirely unguarded: no hook, no probe, no test stands behind it.
Coverage is strictly narrower than the failure. **A session that never triggered
this skill is not a session in which negative claims were checked.**

The second line of defence is `init-verification`, which re-checks negative
capability conclusions already written into `AGENTS.md` at the start of the next
session. It catches what this section missed — one session late, which is not
never, but is also not here.

## Default-FAIL Evaluation Contract

Adapted from [Anthropic's Code with Claude 2026 reference impl](https://github.com/anthropics/cwc-long-running-agents):

> "Every criterion starts false; the agent can't mark it passing without opening evidence first."

### Standard criteria (adapt to project)

| Criterion | What counts as evidence |
|---|---|
| **Compile / build passes** | Build log path + exit code 0, or compiler stdout/stderr captured |
| **Type-check passes** | `tsc --noEmit` (or equivalent) output |
| **Tests pass** | Test runner output showing N passed, **0 failed**, **0 errored** |
| **Coverage obligations** *(non-trivial / risk-bearing features)* | The spec/code obligations are exercised by tests the run actually executes — for features with real logic or risk constructs, a `/test-plan` report (`.harness-anchor/coverage-<ts>.md`) with no open gaps. A green suite that skips the risk path is a false pass. |
| **Static analysis** | Lint report file, OR explicit "no warnings" line in output |
| **Test integrity** *(when tests changed in the same diff)* | The claim names why each test change happened (new coverage vs adjusted expectation) — `/verify` reports this as `### Integrity`; a weakened assertion that makes failing behavior "pass" is a red flag |
| **Deliverable committed & reproducible** *(when claiming "done / shipped / committed")* | Full `git status` reviewed (the whole tree, not just state files) **and** the committed `HEAD` builds — not only the dirty working tree. A feature marked `pass` whose source isn't committed is not delivered: HEAD won't reproduce the evidence. |
| **Manual smoke** | Concrete steps + observed result (only if the above can't cover) |

### Filling out evidence in `feature_list.json`

```json
{
  "id": "doc-list-rendering",
  "status": "pass",
  "evidence": {
    "timestamp": "2026-05-28T13:45:21Z",
    "commit": "abc123def456",
    "artifacts": [
      ".harness-anchor/build-2026-05-28T13-44.log",
      ".harness-anchor/test-2026-05-28T13-45.txt"
    ],
    "notes": "All 47 tests pass. Build clean. clang-tidy: 0 warnings on changed files."
  },
  "completedAt": "2026-05-28T13:45:21Z"
}
```

**`evidence: null` ⇒ `status` cannot be `"pass"`.** This is enforced by `feature_list.schema.json`.

## Calibrated Uncertainty (2026 consensus)

When evidence is missing or partial, do NOT bluff. The 2026 LLM-hallucination research consensus is:

> "Aim for calibrated uncertainty: systems that transparently signal doubt and can safely refuse to answer when unsure."

Templates for expressing uncertainty:

- *"I am uncertain whether the test passes because I didn't run it. Recommend `npm test -- --testPathPattern foo` to verify."*
- *"The build appears to succeed based on no error in the output, but I did not see an explicit success line. Recommend `cmake --build .build && echo BUILD_OK`."*
- *"This fix may resolve the issue, but I have not reproduced the original failure. To gain confidence, run `./repro.sh` before and after the change."*

These statements **earn user trust**. Confident-but-wrong claims destroy it.

## Anti-patterns

Do NOT say:
- "Should work now."
- "The build should pass."
- "Tests should be green."
- "This looks correct."
- "These are old / unrelated changes." (said about uncommitted files **without** running `git diff` to confirm — verify before you dismiss; this is how a `pass`'s own source gets left behind)
- "clang-tidy isn't installed on this machine." / "There's no such function." (a negative claim with no search scope and no date)

Say instead:
- "Build passes (evidence: <path>) / Build pending verification (recommend: <command>)"
- The test status alongside a captured artifact path.
- "searched PATH + <locations>, not found (as of <date>)"

## The "should" detector

When you find yourself typing "should", "probably", "I think", or "looks like" about a behavioural claim, pause. Either:
- Run the command to verify, then state the observed result, OR
- Explicitly mark the claim as unverified per the templates above.

## Pre-claim checklist

Before saying ANY of {"done", "fixed", "ready", "complete", "passing", "working"}:

```
- [ ] I ran the build/compile, observed exit code 0
- [ ] I ran the test suite, observed N passed / 0 failed
- [ ] the passing tests exercise the spec's edge cases / risk paths — not just the happy path (run `/test-plan` if unsure)
- [ ] if tests changed alongside source: I explained each test change (new coverage vs adjusted expectation)
- [ ] I have a file path for each piece of evidence
- [ ] if I claimed something is **absent** (not installed, no such function, nothing found): I stated the scope I searched and the date — `searched <scope>, not found (as of <date>)`
- [ ] feature_list.json is updated with evidence object + timestamp + commit
- [ ] if I claimed "committed / shipped / delivered": I reviewed the **full** `git status` and confirmed the committed HEAD builds (not just the working tree)
```

If any box is unchecked: state uncertainty explicitly, do NOT flip status to `pass`.

## When to invoke

- The user asks "is it done?"
- You're about to update `feature_list.json` `status` to `"pass"`
- You're about to say "the fix should work"
- You're about to say a tool/function/file/test **doesn't exist** or **isn't available**
- The PostToolUse hook injected warnings — do NOT silently ignore them; surface and address per `self-correction-loop`

## Looking up evidence commands for unfamiliar frameworks

When the project uses a test/lint framework you don't have committed to memory (Catch2, doctest, ruff, deno test, etc.) — invoke the `docs-lookup` skill before constructing the verification command. The lookup result becomes part of the evidence trail.

Bluffing the command and not actually running it is the anti-pattern this skill exists to prevent — that's why **lookup precedes execution** here.

## Related

- `verification-before-completion` (superpowers) — the same Iron Law (no completion claim without fresh evidence). This skill is its harness-anchor counterpart and **superset**: it adds the on-disk evidence record (`feature_list.json`) and the `/verify` subagent. One verification run satisfies both gates — capture the evidence once, don't re-verify.
- `feature-state-keeper` — actual writes to feature_list.json
- `test-coverage-design` / `/test-plan` — derive the coverage obligations this gate checks (are the right things tested, and actually run?)
- `self-correction-loop` — what to do when evidence shows failure
- `/verify` command — full automated verification pass via `verification-runner` subagent
