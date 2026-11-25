---
name: toon
description: Compresses large, heavy, or verbose prompts into lean, unambiguous, "SWE/SDE-proof" prompts for coding agents and other AI tools, encoding any structured or tabular data inside the prompt using TOON (Token-Oriented Object Notation) to cut token usage. Trigger this skill whenever a message starts with "/toon", or whenever the user asks to compress/optimize/shrink/reduce-tokens/toonify a prompt, spec, system prompt, or set of instructions meant for an AI coding tool or agent (Claude Code, Cursor, Copilot, Antigravity, OpenCode, Windsurf, etc.), or explicitly mentions "TOON format" in connection with a prompt. Also use it when a user pastes a long prompt/spec/JSON payload and asks Claude to make it more efficient, more token-efficient, or ready to hand off to a coding agent without back-and-forth clarification.
---

# /toon — Prompt Compression & TOON Encoding

## What this skill actually does

A "heavy" prompt for an AI coding tool almost always has two different kinds of bulk in it, and they need to be handled differently:

1. **Prose bulk** — instructions, context, requirements, explanations, caveats — written the way humans write when thinking out loud: repeated context, hedging, pleasantries, restated constraints, redundant examples.
2. **Data bulk** — file lists, config values, schemas, sample records, test cases, API responses, directory trees — structured, enumerable information that's usually pasted as JSON, a bullet list, or a table.

Squeezing prose bulk means rewriting it tighter without losing anything an autonomous agent needs to act correctly on the first try. Squeezing data bulk means re-encoding it in [TOON](https://toonformat.dev), which is JSON's data model but laid out YAML-indentation-style with CSV-style rows for uniform arrays — it round-trips losslessly and benchmarks ~30-60% fewer tokens than pretty JSON on uniform, tabular data, while staying more parseable for models than raw CSV (see `references/toon-cheatsheet.md`).

These are separate problems with separate techniques. Don't try to force prose into TOON (it isn't built for that — see "When NOT to use TOON" below), and don't try to hand-compress data that's genuinely tabular (a script does that correctly, you won't).

## Workflow

### Step 1: Get the source prompt

If the user pasted it inline, use that. If they referenced a file, read it (check `/mnt/user-data/uploads` — see the file-reading skill if it's not already in context). If they just said "/toon" with nothing else, ask what prompt they want compressed — don't guess at content that isn't there.

### Step 2: Split prose from data

Read through the prompt and mark which chunks are structured/enumerable (would naturally be a JSON array, a table, a list of key-value config, a batch of examples/test cases) versus which chunks are instructions and context. Most real prompts are prose with data embedded in the middle (e.g. "here's my file structure: {...}", "these are the test cases: - ...", "use this config: ...").

### Step 3: Compress the prose

Work through `references/prompt-compression-guide.md` — it has the specific moves (imperative voice, dedup, cutting hedges/pleasantries) and, critically, the list of things that are NOT allowed to be cut because losing them makes the prompt ambiguous to an autonomous agent (exact paths/names, constraints, acceptance criteria, "do not" boundaries). This is what makes the output "SWE/SDE-proof" — an agent that receives it shouldn't have to guess or ask a clarifying question to proceed correctly. If you find a piece of the original prompt that's genuinely ambiguous (not just verbose), flag it to the user rather than silently resolving it during compression — silently guessing is how compressed prompts cause an agent to build the wrong thing.

### Step 4: Encode the data blocks as TOON

For each structured chunk identified in Step 2, convert it to JSON first if it isn't already (mentally or explicitly — TOON is a JSON data-model encoding), then run it through the converter:

```bash
python3 scripts/to_toon.py input.json
```

(Path is relative to wherever this skill is installed — see the repo's README for install locations across different tools.) The script shells out to the official `@toon-format/cli` via `npx` when the sandbox has network access, which is the authoritative, spec-correct encoder — prefer this path. If npx/network isn't available, it falls back to a bundled pure-Python encoder covering the common cases (flat objects, nested objects, primitive arrays, uniform-object arrays). See `references/toon-cheatsheet.md` if you want to hand-write or sanity-check TOON output yourself instead of running the script — small, obviously-uniform arrays are often faster to encode by eye.

Run with `--stats` (passed through to the CLI) to get a before/after token estimate for that chunk:

```bash
python3 scripts/to_toon.py input.json --stats
```

**Check tabular eligibility before converting.** TOON's savings come almost entirely from uniform arrays of objects (same fields, primitive values, every row). If a data chunk is a single object, a deeply nested/irregular structure, or an array where objects don't share a consistent shape, TOON adds overhead instead of saving tokens — leave that chunk as compact JSON instead and say so. Don't convert something to TOON just because the skill is named toon; convert it because it's genuinely uniform, tabular data. `references/toon-cheatsheet.md` has the quick eligibility check and worked examples.

### Step 5: Assemble the final prompt

Put the compressed instructions first, then the TOON-encoded data in fenced ` ```toon ` code blocks, one per logical dataset, each with a one-line label if it's not obvious what it is (e.g. `# test cases`). TOON is meant to be *shown* to the model, not described — a receiving agent that's never seen TOON before will generally infer the structure correctly from the `[N]{fields}:` header and rows, so you don't need to explain the format itself in the output unless the user specifically wants a primer line included.

Keep any parts you decided not to convert (single objects, prose-embedded short lists, non-uniform structures) in their original compact form — don't force everything into one format.

### Step 6: Report the savings

Give the user a short before/after: rough total token count (or the sum of what `--stats` reported per chunk, plus an estimate for the prose compression — `len(text) / 4` is a fine rough proxy if you need one, no need for a real tokenizer), and call out anything you flagged as ambiguous in Step 3 so they can clarify before handing the prompt to an agent.

## Output format

- If the compressed prompt is short, just show it inline in the chat response.
- If it's long (the kind of "heavy" prompt this skill exists for), save it as a `.md` file to `/mnt/user-data/outputs/` with the compressed instructions plus fenced ```toon blocks embedded, and present it with `present_files`. Don't create a file for something that fits comfortably in a chat message.

## When NOT to use TOON

Be honest with the user about this rather than TOON-ifying everything reflexively:
- **Deeply nested or non-uniform data** (e.g. a config file with many nesting levels, objects whose fields vary): compact JSON is usually smaller. TOON's `[N]{fields}` header is overhead that only pays for itself across many uniform rows.
- **A single object or a handful of key-value pairs**: there's nothing tabular to exploit; just write it as plain `key: value` lines (which is itself already most of what TOON would produce) or leave it as-is.
- **Pure flat tabular data with no risk of truncation/corruption**: raw CSV is smaller than TOON. TOON's `[N]` length marker and `{fields}` header cost ~5-10% more tokens than CSV in exchange for letting the receiving model detect truncated or malformed data — worth it for anything an agent will act on unsupervised, not worth it for a quick throwaway table.
- **The prompt is mostly prose with only a tiny embedded list**: compress the prose (Step 3) and leave the list as a plain bullet list or inline comma list; converting three items to TOON syntax adds punctuation overhead for no benefit.

## Reference files

- `references/toon-cheatsheet.md` — TOON syntax quick reference, tabular-eligibility check, and worked before/after examples. Read this before hand-encoding anything or if you need to sanity-check the script's output.
- `references/prompt-compression-guide.md` — the prose-compression moves and the "never cut this" list for keeping prompts SWE/SDE-proof. Read this before Step 3.
- `scripts/to_toon.py` — JSON → TOON converter (prefers the official `npx @toon-format/cli`, falls back to a bundled pure-Python encoder). Supports `--stats` for token estimates.
