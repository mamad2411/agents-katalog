---
name: rjv-ollama-delegate
description: "LEGACY one-shot local Ollama runner only. Use when the local model should receive a complete prompt and return text without repo tools. Do NOT use for Codex native subagents, qwen-explorer, qwen-worker, repo reading, or in-place edits; use rjv-codex-ollama-subagents instead."
---

# Delegate to local Ollama

## Status: legacy one-shot path

For Codex native subagents with repo tools, use
`rjv-codex-ollama-subagents` instead.

Use this skill only when you explicitly need a **single local HTTP call**:

```text
complete prompt in -> local Ollama text out
```

Do not use this skill for:

- Codex subagents
- `qwen-explorer`
- `qwen-worker`
- repo reading
- in-place file edits
- proving token savings through native Codex delegation

Pattern: **the local model types, you spec and review.** From a tight
spec, a mid-size local model (30B-class) produces ~90% production-quality
code at zero token cost — but it misses subtle bugs in its own and
others' code, so every output gets reviewed and tested by you before it
ships.

In a `rjv-gated-build` (see that skill), a local model can be cast as an
**Author** for spec-implementable functions — never as a **Reviewer**.

**When NOT to delegate here** (learned on a live build):

- **Below the break-even size, do it yourself.** Writing the spec + a
  runner prompt + reviewing the output has fixed overhead. For a small
  change (~a few dozen lines or fewer) that overhead exceeds the saving —
  the spec *is* the work. Delegation pays on the big mechanical steps,
  not the 4-line fix.
- **Stakes raise the drafting floor.** For ordinary feature work, local
  drafting from a tight spec is worth it. On **live-money / high-blast-
  radius code**, keep even the DRAFT on a cloud mid-tier (Sonnet), not a
  local model — a subtly-wrong local draft costs more in review than it
  saves, and the review burden is where the risk lives.

**Historical note:** this skill was created before the Codex-native
hybrid profile flow was verified. For modern Codex, local Qwen can be
used through custom Codex agents such as `qwen-explorer` and
`qwen-worker`; that workflow belongs in `rjv-codex-ollama-subagents`.

## Hard limitations (do not design around these)

A local model here is a **one-shot text function, not an agent**:

- **No tools. No repo.** No file reads, no shell, no web, no filesystem.
  It sees ONLY the prompt text you paste. It cannot "go look at" the
  other file, cannot do reconnaissance, cannot edit files in place. If
  the job needs the repo, this is the WRONG tool — use a cloud
  Explore/subagent (see `rjv-gated-build` §7, the two-ladder split).
- **One-shot.** No multi-turn agentic loop, no self-correction from tool
  results. One prompt in, one answer out.
- **Context must be complete in the prompt.** Everything it needs — the
  existing code, the signature, the conventions — you hand it. It knows
  nothing else about your project.
- **Weak at judgment.** Misses subtle/platform bugs; it is NEVER a
  reviewer and never the gate.
- **Quality tracks size + task fit.** A 30B model drafts well from a
  tight spec; it does not reliably review, refactor code it can't see,
  or reason about anything not in the prompt.

## Best practices (ground level)

- Hand it a COMPLETE, self-contained prompt: spec + all code context +
  exact output format. See "Writing the prompt".
- Keep it to draft-from-spec / write-tests-from-spec / classify /
  summarize / convert. The tell that you've picked the wrong tool: you
  find yourself wishing it could "check the other file" — that's a
  cloud-subagent job, route it there.
- Above the trivial size only — a 4-line change is cheaper to write
  yourself than to spec + review out.
- On high-stakes / live-money code, draft on a cloud mid-tier (Sonnet),
  not local.
- ALWAYS test + review the output yourself before it ships (next section).
- Keep the model resident (`keep_alive`) across a run of related calls
  so only the first pays the load.

## How to run

Use the bundled runner (relative to this skill's directory), never
`ollama run` — the CLI emits TTY escape codes into its output even when
stdout is redirected:

```sh
<this-skill-dir>/scripts/ollama-chat.sh <model> <prompt-file> <out-file> [num_ctx=16384] [keep_alive=2h]
```

It calls the local HTTP API (`localhost:11434/api/chat`, non-streaming),
writes the raw response to `<out-file>`, and prints timing stats
(`wall / prompt tok/s / output tok/s / load`). Put prompt files in your
scratchpad/temp directory. `keep_alive=2h` keeps the model resident in
RAM so only the first call pays the load time; check residency with
`ollama ps`.

## Model choice

Check what's installed with `ollama list`, then pick by task:

| Class | Use for |
|---|---|
| Largest available (30B+) | code from spec, test-writing, harder extraction |
| Small/fast (7–9B) | classification, summaries, quick extraction |
| Coder variants | small code transforms |

Reference numbers from a verified spike (qwen3.6:35b on an Apple Silicon
Mac): ~60 tok/s generation, ~1000 tok/s prompt processing, ~5s load. A
paginated-API route from spec took 21s; a 300-line test suite took 61s.

## Writing the prompt (this is where quality is won)

The model sees ONLY the prompt file — no repo, no conversation. A good
delegation prompt contains:

1. **The task spec, decided by YOU first** — algorithms, edge cases, API
   shapes. Don't ask it to design; ask it to implement your design.
2. **Real code context inline** — the existing route/function/schema it
   must fit, plus file conventions (imports available, error shapes,
   validation style). Copy actual snippets, don't describe them.
3. **Exact output contract** — "Output ONLY the code, no markdown
   fences, no explanation." (Models ignore the fences rule ~50% of the
   time — strip fences on receipt rather than fighting it.)
4. For tests: the harness conventions verbatim (imports, seeding
   helpers, how to invoke the app) — with these, the spike model
   produced a 7-test suite that passed first run.

## Non-negotiable: verify the output yourself

- **Run it** — type-check, lint, and a test harness with known expected
  values. "Looks right" is not evidence: in the spike, an RFC 2047
  decoder that read cleanly failed 3/9 test vectors.
- **Review for subtle platform bugs** — the class local models miss:
  things needing runtime knowledge (e.g. SQLite LIKE needs an explicit
  `ESCAPE` clause; many ORMs' `like()` helpers don't emit one).
- **Never delegate review or bug-hunting** — asked to find a real bug in
  shipped code, the spike model said "no bugs".
- Note provenance in commits: "drafted by <model>, reviewed + hardened".

## Evidence (spike, 2026-07-05)

| Task | Result |
|---|---|
| RFC 2047 decoder from spec | 6/9 vectors — Q-decoding dropped literal chars |
| Bug-hunt on real shipped code | FAILED — "no bugs" on a real bug |
| Keyset-pagination API route from spec | ~90% in 21s; added an id tiebreaker unprompted; one LIKE-escape bug caught in review |
| Test suite for that route | 7/7 passed first run (lint nits only) |
