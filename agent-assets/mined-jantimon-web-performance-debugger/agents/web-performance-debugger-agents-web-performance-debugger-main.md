# Driving wpd from an agent

For an agent consuming `wpd`. wpd finds and investigates; it does not grade, rank, or recommend. It
hands you typed, measurement-tagged numbers and a clean exit code; the judgment stays with you.

## The loop

1. **Record.** `wpd record <module> [flags]` writes a recording plus siblings. One `record` is one
   capture pass.
2. **Query.** Read the recording through the `query` verbs. **Never read the recording file directly**
   -- it can be many MB. Drill instead:

```
query spans <file>              # overview: one row per span, one shape across chrome/firefox/node
  -> query span <file> <kind:label>   # one span's full anatomy
       -> query get <file> <id>       # one raw event (stack + args); needs --deep or firefox
```

- Every verb takes `latest` in place of `<file>` (a cwd-keyed pointer, never resolved by mtime).
- Span identity is **kind + label**. A bare label that matches more than one kind is a collision;
  qualify it (`run`, `step:first increment`, `measure:hydrate`).
- `query spans --label X` with no match is a **filter**: it reports the empty result and exits 0.
  `query span X` with no match is a **lookup**: it exits 1. Pick the verb for the branch you want.
- Other verbs: `query cpu` (hot functions + rollup), `query frame <id>` (one function's callers and
  callees), `query blame --forced` (forced-layout read sites), `query events` (the raw log).

## Output

- **Always pass `--format json` or `--format toon`.** Both are plain: no ANSI, whatever the TTY.
  [TOON](https://github.com/toon-format/toon) is a compact, JSON-shaped text format that spends fewer
  tokens than JSON.
- The view shapes are typed and exported from the package root (`SpansResult`, `SpanAnatomy`,
  `CpuOverview`, `CpuDiffResult`, ...). Import them; do not hand-roll a shape.

## Reading the numbers: three traps

- **`null` is not `0`.** A count or slice the capture could not observe is an explicit `null`
  (not-measured), never `0` (measured clean). Do not coerce it. A gate on such a metric is a loud
  `n/a` FAIL, never a silent pass: `assert --max-forced 0` on a `--breakdown` recording FAILs, because
  forced counts need `--deep`.
- **`jsSelfMs` is the JS headline.** Do not denominate a package share on `activeMs` -- the larger
  non-idle total (js + gc + engine).
- **A function's display name is `fn`, not `name`** (its self time is `selfMs`, its source `source`).
- The full field reference: [README, Consuming the JSON](README.md#consuming-the-json).

## Exit codes and refusals: treat the refusal as the answer

- **A failed gate exits non-zero.** `assert` over a blown budget, `diff`/`cpu-diff` with
  `--fail-on-regression` on a real regression: exit 1. A clean run exits 0. Gate on the exit code.
- **wpd refuses rather than fabricate.** `diff`/`cpu-diff` across an incompatible pair (a different
  browser, runtime, capture mode, workload, iterations, warmup, headless flavour, or throttle) names
  the mismatch and declines to gate. The refusal text is the answer -- do not retry to force a number.
  The **workload** is the whole flow (lane + host page + module): the same host with a different module
  refuses too.
- **Bot-wall.** On `record --url` onto a bot-challenge page (Cloudflare, DataDome), wpd refuses and
  writes a screenshot rather than measure the challenge as the site. `--allow-bot-wall` measures it on
  purpose, with a loud note that the numbers describe the challenge page.

## Where to read more

- Capture modes and what each yields: [README, Choose a capture](README.md#choose-a-capture-what-you-want-to-know).
- The full JSON type table: [README, Consuming the JSON](README.md#consuming-the-json).
- The query verbs: [README, The query verbs](README.md#the-query-verbs).
- Trust tiers (which numbers are exact, which directional): [README, The numbers](README.md#the-numbers-and-how-far-to-trust-them)
  and [docs/verification.md](docs/verification.md).
- The scope boundary (what wpd leaves to you): [docs/dev/orchestrator-boundary.md](docs/dev/orchestrator-boundary.md).
