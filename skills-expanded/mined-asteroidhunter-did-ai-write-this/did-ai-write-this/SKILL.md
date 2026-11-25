---
name: did-ai-write-this
description: Run Pangram's v3 AI-detection on a chunk of text and return a structured verdict (label + three fractions summing to 1.0). Use whenever the user asks "is this AI?", "did a human write this?", "did ChatGPT write this?", "is this AI-generated?", "check if AI", "verify this source", or any variant question about text authorship. **Does not auto-run on WebFetch by default** — every call costs a Pangram credit, so proactive use is opt-in. To enable proactive checks during research, the user can add an instruction to their CLAUDE.md (e.g. "When I'm in a research flow, run did-ai-write-this on every WebFetch'd page before citing"). Output is compact JSON (label, three fractions, char count) when stdout is piped, a one-line summary on a TTY; a fraction_ai >= 0.5 verdict means do not cite as human-authored. Pangram needs at least 50 words for reliable detection (the CLI rejects shorter input with exit 6).
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/.venv/bin/python *)
---

## When to use

- **Direct user request** — the user pastes text and asks whether it was AI-written, or any phrasing of that question ("is this AI?", "did ChatGPT write this?", "human or AI?", etc.). This is the only auto-trigger case.
- **Proactive post-WebFetch check (opt-in only)** — skipped by default because every call costs the user a Pangram credit. If the user has added an instruction to their `CLAUDE.md` along the lines of *"when researching, run did-ai-write-this on WebFetch'd pages before citing"*, honor that. Otherwise wait for an explicit ask — do not call this skill on every WebFetch.
- Not for stylistic AI-detection guesses based on writing patterns — those are unreliable and this skill exists precisely to replace them with a calibrated, vendor-backed signal.

## How to invoke

The CLI sits next to this `SKILL.md` and runs inside a self-contained venv populated by `install.py`. Always invoke through `${CLAUDE_SKILL_DIR}` so the path works regardless of where the skill is installed.

**Positional argument** (short snippet, one shot):

```bash
${CLAUDE_SKILL_DIR}/.venv/bin/python ${CLAUDE_SKILL_DIR}/cli.py "the text to check"
```

**From a file** (longer documents):

```bash
${CLAUDE_SKILL_DIR}/.venv/bin/python ${CLAUDE_SKILL_DIR}/cli.py --file /path/to/document.txt
```

**From stdin** (piping output of another command, common for `WebFetch` content saved to a temp file or var):

```bash
cat /tmp/fetched.txt | ${CLAUDE_SKILL_DIR}/.venv/bin/python ${CLAUDE_SKILL_DIR}/cli.py --stdin
```

**Per-paragraph attribution** for mixed documents — adds a `windows` array showing which segments drove the overall label:

```bash
${CLAUDE_SKILL_DIR}/.venv/bin/python ${CLAUDE_SKILL_DIR}/cli.py --full --file /path/to/mixed_doc.txt
```

Force the output format if needed: `--json` (always JSON) or `--pretty` (always one-line summary). Default behavior is JSON when stdout is captured (your Bash tool case) and pretty when stdout is a terminal (user case), so the flags are usually unnecessary.

## Interpreting the output

Default JSON output (what you receive when invoking through Bash):

```json
{"label": "AI", "fraction_ai": 0.94, "fraction_ai_assisted": 0.04, "fraction_human": 0.02, "chars": 1284}
```

Fields:

- `label` — one of `"AI"`, `"AI-Assisted"`, `"Human"`, `"Mixed"`. This is Pangram's overall verdict.
- `fraction_ai`, `fraction_ai_assisted`, `fraction_human` — floats in `[0, 1]` summing to 1.0. The breakdown explains a `"Mixed"` label and gives you a confidence sense even when the label is decisive.
- `chars` — length of the submitted text.

With `--full`, the response also includes:

- `windows` — list of per-segment classifications, each with `text`, `label`, `ai_assistance_score`, `confidence`, character offsets, word count, and token length. Use this when the overall label is `"Mixed"` and you need to know *which* paragraphs are AI.

**Decision heuristic:** treat `fraction_ai >= 0.5` as "do not cite as human-authored". For `"AI-Assisted"` and `"Mixed"` labels, surface the verdict to the user before citing — the source may still be usable but the AI involvement should be disclosed.

## Errors

The CLI exits non-zero with a stderr message on failure. Map:

| Exit | Meaning | What to do |
|------|---------|------------|
| 0 | Success — verdict on stdout | Use the result |
| 1 | Generic / unexpected error, including unwrapped network errors from `requests` | Surface stderr to the user; check network |
| 2 | `PANGRAM_API_KEY` missing or `.env` not loadable | Tell the user to re-run `python install.py` from the cloned repo |
| 3 | Pangram rejected the API key (HTTP 401 — bad key or out of credits) | Tell the user to check their Pangram dashboard for credits and key validity |
| 4 | Pangram server error after one automatic retry (5xx) | Surface; suggest retry later. Pangram-side outage |
| 6 | Input below 50 words | Don't retry with the same text — either gather more or skip the AI-detection step entirely for this snippet |

## Privacy note

Text passed to this skill is sent to Pangram's API (`text.api.pangram.com/v3`) for classification. Don't run it on private or confidential content unless the user has authorized third-party processing of that content.
