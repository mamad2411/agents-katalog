---
name: borderline
description: >-
  Delegate mechanical, boring, low-risk tasks to the Antigravity CLI (agy) where
  it is just as reliable as Claude: bulk translations and i18n, trivial CSS/color/style
  changes, repetitive renames and replacements across many files, boilerplate,
  formatting and simple copy rewrites. Use it when the task is monotonous, its
  correctness is verifiable at a glance, and being wrong is cheap. Do NOT use it
  for business logic, architecture decisions, security, ambiguous requirements,
  or changes where a mistake is costly.
argument-hint: "<task to delegate to agy>"
---

# Borderline — transparent Claude ⇄ agy pipeline

Borderline exists to **offload boring, safe work to the Antigravity CLI (`agy`)** so
Claude can stay focused on what needs judgment. Communication must be **transparent**:
always tell the user what you delegated, in which mode, and what you reviewed.

> **Operating requirement:** this flow launches `agy` via `Bash` without asking
> for permission on every step, so Claude must run with `--dangerously-skip-permissions`.
> Otherwise every call prompts for confirmation and the pipeline stops being transparent.

> **`agy` is agentic — and the fix is structural.** Left alone, agy takes the current
> directory as its workspace and **explores it** (lists files, reads README, opens scripts)
> before answering, even with a concrete prompt and even when told not to. Each read is a
> request against agy's rate-limit, so a context-free translation ends up scanning the repo
> and burning quota. The wrapper (`delegate.sh`) defeats this by **running agy from an empty
> scratch directory in `--text`**: no workspace → nothing to scan → no divagation, no wasted
> requests. **Always go through the wrapper.**

> **Long context "just works" — pass big prompts on stdin, not as an argument.** A command
> line is capped by the OS (`ARG_MAX`, ~1 MB on macOS). The old wrapper handed the whole
> prompt to `agy -p "<prompt>"`, so a large i18n batch or a long document blew that ceiling
> and the call **failed or hung** ("Argument list too long", mis-reported as a rate-limit).
> The wrapper now **streams the prompt to `agy --print` on stdin**, which has no size limit.
> For content so large it can't even fit on `delegate.sh`'s own command line, **write it to a
> temp file and pass `@/path/to/file`** (or pipe it and pass `-`); the wrapper reads the file
> and streams it in. A 1.3 MB prompt that is impossible via `-p` goes through cleanly this way.

> **A stuck call always returns control.** agy's own `--print-timeout` bounds the model wait
> but **not** input ingestion or a silent rate-limit stall, so it can hang far past it. The
> wrapper adds a **hard wall-clock watchdog** (`--print-timeout` + 30 s): if agy overruns, it
> is killed and you get a `borderline: HARD TIMEOUT …` line instead of an indefinite hang.

## 1. Is it a *borderline* task? (classify first)

**DO delegate** — mechanical, repetitive, verifiable at a glance:
- Bulk translations and **i18n** (translate/populate `locales/*.json`, `.po`, `messages.*`).
- Trivial style changes: background/text color, spacing, CSS token swaps.
- Repetitive renames and replacements across many files (same pattern N times).
- Predictable boilerplate, sample data/fixtures, formatting, simple copy rewrites.

**DON'T delegate** — keep it in Claude:
- Business logic, algorithms, concurrency, state.
- Architecture, API design, decisions with trade-offs.
- Security, auth, secret handling, data migrations.
- Anything with ambiguous requirements or where a mistake is costly.

When in doubt, **don't delegate**: do it yourself.

## 2. Choose the mode

| Mode | When | What it does |
|------|------|--------------|
| `--text` | **Small / context-free** work (one color, one string, a batch of strings to translate) | runs agy from an **empty scratch dir** so it can't scan the repo; **returns text only**, you apply it with Edit/Write |
| `--edit` | **Bulk** file work (mass i18n across files, replacements across many files) | runs agy in the repo; it reads and **writes** the named files itself, scoped to those files |

**Prefer `--text` for translations.** Don't point agy at repo files — that's exactly what
triggers its agentic scanning and burns the rate-limit. **Paste the source content inline**
in the prompt, ask for the translated output only, and let Claude write the file. Because
`--text` runs agy from an empty directory, divagation is structurally impossible. Reach for
`--edit` only when the volume of files makes inlining impractical.

## 3. Run the delegation

Always call the wrapper (it centralizes flags, the anti-exploration preamble, model and mode):

```bash
# Preferred for translations: inline the source, get output only, you write the file.
"${CLAUDE_PLUGIN_ROOT}/scripts/delegate.sh" --text 'Translate this JSON object to neutral Spanish. Output ONLY the translated JSON, same keys/order, do NOT touch {var} placeholders or HTML tags:
{"save":"Save","cancel":"Cancel","items":"You have {n} items"}'
```

```bash
# Bulk across files when inlining is impractical.
"${CLAUDE_PLUGIN_ROOT}/scripts/delegate.sh" --edit "Translate ALL keys in locales/en.json and write locales/es.json with the same keys, neutral Spanish, without touching {var} placeholders or HTML tags. Operate only on those two files."
```

```bash
# Tiny text answer.
"${CLAUDE_PLUGIN_ROOT}/scripts/delegate.sh" --text "Give me only the hex of a blue 20% darker than #3B82F6. Reply with the value only."
```

```bash
# LARGE content (big i18n batch, long document): don't inline it on the command line —
# write it to a temp file (Write tool) and pass the path with '@'. No size limit.
"${CLAUDE_PLUGIN_ROOT}/scripts/delegate.sh" --text @/tmp/borderline-batch.txt
```

For long prompts, **always prefer `@file`** (write the source + instructions to a temp file,
pass its path). Inlining a very large prompt as a quoted argument can exceed the shell's
`ARG_MAX` and fail before the script even runs; `@file` (and `-` for stdin) sidestep that
entirely and stream the content to agy on stdin.

Rules when building the prompt for agy:
- Be **explicit and scoped**: exact files (in `--edit`), output format, what NOT to touch
  (placeholders `{var}`, `%s`, tags, keys, ordering).
- In `--text`, ask for **the result only** (no explanations) so you can apply it cleanly,
  and **include the source content inline** so agy needs no repo access.
- In `--edit`, **name the input and output files** and the success criteria, and remind it
  to operate only on those files.

Tunables (env vars, optional): `BORDERLINE_MODEL` (default `Gemini 3.5 Flash (High)`),
`BORDERLINE_TIMEOUT` (default `2m`), `BORDERLINE_CLI` (default `agy`),
`BORDERLINE_THROTTLE_MS` (sleep before the call; set `3000`–`5000` for batch i18n).

### Rate-limit (read before batch jobs)

agy rate-limits by request **frequency**, and the throttle is **silent**: no 429, no message —
the call just **hangs and returns empty**. The wrapper bounds this two ways: agy's own
`--print-timeout`, and a **hard wall-clock watchdog** (`--print-timeout` + 30 s) that kills agy
if it overruns, so the call can never hang the agent indefinitely. You'll see either
`borderline: HARD TIMEOUT …` (agy had to be killed) or `borderline: agy returned EMPTY …`
(agy gave up on its own) — both mean the same thing: **a silent rate-limit**. When you see it:
**do not hammer-retry** (worsens it), **do not run calls concurrently** (frequency is what
triggers the block), let agy **rest several minutes**, then send **one** call. For batches, set
`BORDERLINE_THROTTLE_MS=3000`–`5000` and prefer **one big `--text` batch** over many small
calls. Healthy calls return in ~4–17 s regardless of size.

## 4. ALWAYS review (non-negotiable)

After delegating, **verify before accepting**:
1. **Diff**: if it's a git repo, `git diff --stat` then `git diff` of the touched files.
   If it's not git, `Read` the files agy was supposed to change.
2. **Sanity**: for i18n, keys must match the source with none missing/extra, and
   placeholders must stay intact. For style, the value must be the requested one.
3. **Build/lint** if they exist and are fast (`npm run lint`, `tsc --noEmit`, etc.).
4. If something is wrong: fix it yourself or **re-delegate** with more precise
   instructions. Never let dubious work through.

## 5. Report (transparency)

Always close with one or two lines stating:
- What you delegated and in which mode (`--edit`/`--text`).
- What changed (files / number of strings).
- What you verified and the result (diff reviewed, lint OK, etc.).

Example: *"Delegated to agy (--edit mode) the translation of 142 keys into
`locales/es.json`. Reviewed the diff: keys aligned with `en.json`, placeholders intact,
`lint` OK."*

## Common errors
- `agy: command not found` / exit 127 → the Antigravity CLI is not installed/on PATH.
  **Do NOT try to install it yourself.** It requires the user to sign in, so an unattended
  install would be useless. Just hand the user the URL and ask them to install it **and sign
  in**, then retry: **https://antigravity.google/product/antigravity-cli** . (Override the
  binary with `BORDERLINE_CLI` if it lives elsewhere.)
- `borderline: agy returned EMPTY …` or `borderline: HARD TIMEOUT …` → **silent rate-limit**
  (see the Rate-limit section). Stop, let agy rest minutes, send one call. Don't retry-storm or
  run calls concurrently. Run one delegation at a time.
- `Argument list too long` → the prompt exceeded the shell's `ARG_MAX` as an inline argument.
  Don't inline huge prompts: write the content to a temp file and pass `@/path/to/file` (the
  wrapper streams it to agy on stdin, which has no size limit).
- agy starts exploring/auditing the repo → either the wrapper wasn't used, or you used
  `--edit` (which runs in the repo) for something that should have been `--text`. For
  context-free work always use `--text` — it runs agy from an empty dir so there's nothing
  to scan.
