---
name: hunter-anti-mock
description: >-
  The gate that rejects any change resolving a deviation by suppressing
  detection instead of fixing behaviour. Run this on every proposed patch or
  diff that claims to fix a Find, before that patch's fixing claim is cleared by
  hunter-evidence-gate and before any replay is trusted. It runs a diff-scanner
  with per-language pattern families (JS/TS, Python, Go, Java, Ruby) for newly
  added mocks/stubs/fakes, test-mode or env branches around the failing path,
  broadened exception handling, deleted or weakened assertions, skipped tests,
  raised timeouts/retries, hardcoded returns, and fallback data. It scopes to
  NEW or EXPANDED hunks on the failing path only, so legitimate guard clauses
  and pre-existing doubles are not flagged, and supports an allowlist and a
  recorded human override. Load whenever a patch is proposed to close a Find, a
  probe suddenly passes after an edit, or a diff touches the failing path.
allowed-tools: Read, Bash, Grep, Glob
---

# Hunter Anti-Mock

Assumes `hunter-doctrine` is loaded; this skill is the operational enforcement
of the doctrine's anti-mock law. A deviation is resolved by making the system
behave correctly, never by making the detection stop firing. This gate reads the
diff and rejects the second thing.

## The single rule

A patch that makes a probe pass by changing what the probe *sees* instead of
what the system *does* is rejected. The green replay it produces is a lie: the
Find is not closed, it is hidden — converted from a known deviation into an
unknown one, which is strictly worse than leaving it open.

Outcome on rejection: `mocking_rejected`, carrying the offending hunks.

## Inputs

- The unified diff of the proposed patch (`git diff` or the patch file).
- The **failing path**: the set of files/functions on the reproduction trail of
  the Find being fixed — from the Find's `FINDS.json` entry (stack frames, the
  handler that served the bad response, the module under the failing probe).
- The allowlist file, if present (`.hunter/anti-mock-allow.json`).

## Scope controls (precision — read before scanning)

False positives here are expensive: they block real fixes and train operators to
override the gate reflexively. Four controls keep the scanner sharp:

1. **NEW or EXPANDED hunks only.** Only `+` lines in the diff are candidates.
   A mock that already existed on a `-`/context line is not this patch's doing.
   An *expanded* hunk counts (e.g. a `catch` block that existed but the patch
   widened it to swallow more, or a mock whose scope the patch enlarged).
2. **Failing-path files only.** A pattern match in a file that is not on the
   Find's failing path is not a suppression of *this* Find. Restrict scanning to
   the failing-path set. A new mock in an unrelated module is out of scope for
   this gate (it may be a different concern, but it is not this Find's cover-up).
3. **Allowlist.** Entries in `.hunter/anti-mock-allow.json` (by file glob +
   pattern id + a justification string) are pre-cleared — e.g. a fixture builder
   that is legitimately synthetic and clearly labelled. Allowlisting requires a
   human-authored justification recorded in the file; an empty justification is
   itself a rejection.
4. **Human override.** An operator may override a specific rejected hunk, but the
   override MUST record: who, which hunk (file + line range + pattern id), and a
   written justification of why this is a real fix and not a suppression. The
   override is written to the run directory and surfaced in the report's method
   section. An override without justification is not applied.

Legitimate guard clauses survive these controls: a `guard let x = ... else {
throw }` that fails *loudly* is not a match for any family below, because the
families target *silencing*, not *validating*. When a guard both appears new and
returns fallback data or a success value on the failing path, it is a match.

## Pattern families

Each family has an intent, per-language patterns (regex is the fast first pass;
prefer AST confirmation where noted to cut false positives), and the
counter-question the patch author must answer.

Regex below is illustrative and anchored to added lines. Treat a regex hit as a
**candidate**, then confirm against intent and scope before flagging.

### F1 — Mock / stub / fake imports newly added

Intent: a real dependency on the failing path replaced by a double.

| Lang | Candidate patterns (on `+` lines) |
|---|---|
| JS/TS | `jest\.mock\(`, `vi\.mock\(`, `sinon\.(stub\|fake\|mock)`, `import .* from ['"].*(mock\|stub\|fake\|__mocks__)`, `td\.replace\(` |
| Python | `unittest\.mock`, `from mock import`, `@patch\(`, `MagicMock\(`, `monkeypatch\.`, `responses\.add\(` |
| Go | `//go:generate mockgen`, `_mock\.go` newly imported, `gomock\.NewController`, `httptest\.NewServer` substituted for the real endpoint on the failing path |
| Java | `Mockito\.(mock\|spy\|when)`, `@Mock`, `@MockBean`, `EasyMock\.` |
| Ruby | `double\(`, `instance_double\(`, `allow\(.*\)\.to receive`, `stub_request\(` (webmock) |

Counter-question: **is the real dependency actually unavailable, or merely
inconvenient?** If it is available, the fix is to make the real path correct.

### F2 — Test-mode / env branch introduced around the failing path

Intent: a shortcut that only runs in a non-production mode and skips the failure.

| Lang | Candidate patterns |
|---|---|
| JS/TS | `if\s*\(\s*process\.env\.(NODE_ENV\|.*TEST\|.*MOCK).*\)`, `if\s*\(\s*__TEST__`, `if\s*\(\s*!?isProd` guarding the failing call |
| Python | `if\s+os\.environ\.get\(['"].*(TEST\|MOCK\|DEBUG)`, `if\s+settings\.(TESTING\|DEBUG)` around the failing branch |
| Go | `if\s+os\.Getenv\("[A-Z_]*(TEST\|MOCK\|DEBUG)"\)`, build tags like `//go:build test` newly gating the path |
| Java | `if\s*\(.*System\.getenv\("[A-Z_]*(TEST\|MOCK)"\)`, `@Profile\("test"\)` newly applied to the failing bean |
| Ruby | `if\s+Rails\.env\.(test\|development)\?`, `if\s+ENV\[['"].*(TEST\|MOCK)` around the failing path |

Counter-question: **why does correct behaviour depend on the environment?** If
the production path is still broken, the Find is not fixed — it is hidden from
the probe's environment only.

### F3 — Broadened exception handling / swallowed errors

Intent: the failure still occurs but is caught and silenced so the probe passes.

| Lang | Candidate patterns |
|---|---|
| JS/TS | new/expanded `catch\s*(\w*)\s*{\s*}` (empty), `catch.*{\s*return\s+(true\|null\|\[\]\|{})`, `.catch\(\(\)\s*=>\s*(null\|\[\]\|{}))` |
| Python | `except\s*:` bare, `except\s+Exception` newly widened, `except .*:\s*pass`, `except .*:\s*return` a success value, `logging\.(error->debug)` downgrade |
| Go | `if err != nil {` body changed to `return nil` / `// ignore`, `_ = someCall()` discarding a previously-checked error |
| Java | `catch\s*\(Exception` widened from a specific type, empty catch, `catch.*{ return ...; }` on the failing path |
| Ruby | `rescue\s*=>?.*\n\s*(nil\|true\|\[\])`, `rescue\s+StandardError` newly widened, `rescue; end` |

Counter-question: **is the caught error the deviation itself?** Catching the 500
does not make the 500 not happen. Handle the cause, or let it surface.

### F4 — Deleted or weakened assertions

Intent: the probe/test no longer checks the thing that was failing.

| Lang | Candidate patterns |
|---|---|
| JS/TS | `-\s*expect\(` (deleted), `expect\(.*\)\.toBe\(` changed to `.toBeDefined()`/`.not.toThrow()`, `assert` removed |
| Python | deleted `assert `, `assertEqual` changed to `assertTrue`/`assertIsNotNone`, tightened comparison loosened |
| Go | deleted `if got != want { t.Fatalf`, `require\.Equal` changed to `require.NotNil` |
| Java | deleted `assertEquals`, changed to `assertNotNull`, `assertThat(...).isEqualTo(...)` → `.isNotNull()` |
| Ruby | deleted `expect(...).to eq`, changed to `.to be_truthy`, removed `assert_equal` |

Counter-question: **did the expectation change because intent changed, or
because the code cannot meet it?** If intent is unchanged, weakening the
assertion is falsifying the record.

### F5 — Skipped / disabled tests

| Lang | Candidate patterns |
|---|---|
| JS/TS | `\.skip\(`, `xit\(`, `xdescribe\(`, `it\.todo\(`, `// eslint-disable` around the check |
| Python | `@pytest\.mark\.skip`, `@unittest\.skip`, `@pytest\.mark\.xfail`, `return` early in the test body |
| Go | `t\.Skip\(`, `//go:build ignore` newly added to a test file |
| Java | `@Disabled`, `@Ignore`, `assumeTrue\(false\)` |
| Ruby | `skip\b`, `xit\b`, `pending\b` |

Counter-question: **is the skipped test the one that proved the Find?** If so,
skipping it does not close the Find, it deletes the proof it exists.

### F6 — Raised timeouts / retries until intermittent failure hides

| Lang | Candidate patterns |
|---|---|
| JS/TS | `timeout:\s*\d+` increased, `jest\.setTimeout\(` raised, `retries:\s*\d+` added/raised, `p-retry` newly wrapping the failing call |
| Python | `time\.sleep\(` newly padding, `@retry\(` added, `timeout=` raised, `tenacity` newly wrapping |
| Go | `context\.WithTimeout` duration raised, retry loop added around the failing call |
| Java | `@Timeout` raised, `Awaitility` polling window enlarged, `@Retryable` newly applied |
| Ruby | `Timeout::timeout(` raised, `retry` newly added in a `rescue` |

Counter-question: **does more time make the operation correct, or just make the
flake win more often?** An intermittent deviation is a Find (class
`intermittent`), not a tuning problem.

### F7 — Hardcoded returns satisfying the specific probe

Intent: the function returns the exact value the probe checks, regardless of input.

| Lang | Candidate patterns |
|---|---|
| JS/TS | new `return <literal>` replacing computed logic on the failing path; a value matching the probe's expected literal |
| Python | `return <literal>` short-circuiting the failing computation |
| Go | `return <literal>, nil` replacing the real result |
| Java | `return <literal>;` replacing the computed branch |
| Ruby | method body reduced to a literal on the failing path |

Counter-question: **does this hold for inputs the probe does not send?** A value
that satisfies one probe input and nothing else is a hardcode, not a fix. AST
confirmation recommended: flag when the return value no longer depends on the
function's inputs.

### F8 — Fallback / default data where the real path failed

Intent: when the real source fails, return canned data so the surface looks alive.

| Lang | Candidate patterns |
|---|---|
| JS/TS | `\|\|\s*(\[\]\|{}\|DEFAULT_\|FALLBACK_)`, `?? mockData`, `catch.*return sampleData` |
| Python | `or DEFAULT_`, `except .*: return FALLBACK`, `.get(k, <canned>)` newly masking a required lookup |
| Go | `if err != nil { return defaultX }` on the failing path |
| Java | `orElse(FALLBACK)`, `catch { return DEFAULT; }` |
| Ruby | `rescue; DEFAULT_DATA; end`, `\|\| FALLBACK` |

Counter-question: **is the fallback masking that the real source is broken?** If
the real path failed, that failure is the deviation. Fallback data buries it.

## Decision procedure

```
for each + or expanded hunk in the diff:
  if file not on failing_path: skip
  for each family F1..F8:
    if hunk matches a candidate pattern:
      confirm intent (AST where noted); rule out a loud guard clause
      if allowlisted (file glob + pattern id + non-empty justification): record allow, continue
      else: record as offending hunk (file, line range, family, matched text, counter-question)
if offending hunks is empty: outcome = clean  -> patch may proceed to replay + evidence gate
else if every offending hunk has a recorded human override with justification:
     outcome = overridden -> proceed, carry overrides into the report method section
else: outcome = mocking_rejected -> reject, return offending hunks, block the fixing claim
```

## The outcome record

```json
{
  "hunt_id": "hunt/2026-08-07T14-02Z",
  "find_id": "trail/A31",
  "patch": "patches/A31.diff",
  "outcome": "mocking_rejected",
  "failing_path": ["src/session/handler.ts", "src/session/store.ts"],
  "offending_hunks": [
    {
      "file": "src/session/handler.ts",
      "lines": "88-94",
      "family": "F3",
      "matched": "} catch (e) { return res.status(200).json({}); }",
      "reason": "500 on valid credentials is now swallowed and returned as 200 empty",
      "counter_question": "is the caught error the deviation itself?",
      "real_fix_pointer": "the store throws on a null session row; fix the query, not the catch"
    }
  ],
  "allowlisted": [],
  "overrides": []
}
```

`outcome` is one of: `clean`, `overridden`, `mocking_rejected`.

## Rationalisations that precede this failure

Each is a signal to re-read the evidence, not to proceed. Ask the counter-question.

| Rationalisation | Counter-question |
|---|---|
| "The real service is flaky, so a stub is more reliable for now" | Is the flake the deviation? Then it is a Find, not a reason to stub. |
| "This is out of scope; I'll make it pass and note it" | Does making it pass hide a known deviation? Then it is not out of scope, it is a cover-up. |
| "The test was too strict anyway" | Did the intent change, or only the code's ability to meet it? |
| "I'll add a TODO and come back" | Does the TODO ship green while the deviation ships live? |
| "It works in production, the test env is the problem" | Is the production path actually exercised, or only asserted? |
| "Just bump the timeout, it's basically passing" | Does more time make it correct, or just make the flake win? |

## Hand-off

- `clean` → the patch proceeds to replay (original reproduction re-run ≥2×) and
  then to `hunter-evidence-gate` for the "the patch fixes it" claim.
- `overridden` → same path, with the override record attached and surfaced in
  the report's method section so a reader can audit the human decision.
- `mocking_rejected` → the fixing claim is blocked. The Find stays open. Return
  the offending hunks and the `real_fix_pointer` to whoever proposed the patch.

## Self-check before clearing a patch

- [ ] Scanned only NEW/EXPANDED hunks, only on the Find's failing path
- [ ] Each candidate confirmed against intent; loud guard clauses not flagged
- [ ] Allowlist entries carry non-empty human justification
- [ ] Any override records who, which hunk, and why
- [ ] `mocking_rejected` carries the offending hunks and a real-fix pointer
- [ ] No green replay trusted before this gate returned `clean` or `overridden`
