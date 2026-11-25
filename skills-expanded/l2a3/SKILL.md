# chinese-poem-generator — BOOT-L2A3

Official score comes only from the visible runner invoked by `run_tests`.

## Artifact ledger

| Artifact | Create owner | Check owner | Repair owner | Finalizer-restorable minimum |
|---|---|---|---|---|
| `/root/poem.txt` | Scaffold/Compose | Mirror, then OfficialVerifier | Repair | UTF-8 poem document with 9 non-empty lines total: 1 title + 8 body lines, each body line exactly 7 Chinese characters |
| `/logs/verifier/ctrf.json` | OfficialVerifier via `run_tests` | OfficialVerifier | OfficialVerifier | Not synthesized by the agent |
| `/logs/verifier/reward.txt` | OfficialVerifier via `run_tests` | OfficialVerifier | OfficialVerifier | Not synthesized by the agent |

## Family-local graph

### Contract
Local view:
- `read_tests`
- `read_file instruction.md`
- `list_dir` only if a visible path is unclear

What this node keeps:
- Use `read_tests` as the canonical source for the visible verifier logic and `QILV_PATTERNS`; do not depend on direct raw test-file reads.
- The real output path is `/root/poem.txt`, even if the prompt spells it with backslashes.
- The parser strips empty lines; first non-empty line is the title, the next 8 non-empty lines are the body.
- Each body line must contain exactly 7 Chinese characters under `[\u4e00-\u9fff]`.
- All 8 body lines must match one complete visible `QILV_PATTERNS` entry.
- Rhyme lines and rhyme normalization come from the visible tests exactly.
- Tone uses modern Mandarin: `1/2 = 平`, `3/4 = 仄`.
- `instruction.md` supplies the required theme and speaker perspective.

Route out:
- Go to Scaffold only after copying one full visible pattern and its `rhyme_lines` from `read_tests`.

### Scaffold
What this node owns:
- `/root/poem.txt`

Actions:
- Ensure `/root` exists if needed.
- By step 5, write `/root/poem.txt` with 9 non-empty lines total: title + 8 provisional 7-character Chinese body lines.
- Never use blank filler, English placeholders, or commentary.

Route out:
- Go to Compose.

### Compose
Local view:
- `instruction.md`
- one exact visible pattern and its `rhyme_lines`

What this node builds:
- Title
- 8 body lines
- Chosen rhyme family and rhyme-ending characters

Actions:
- Do not freehand regulated verse from memory.
- Choose the visible form first, then draft each line to its 7-slot tone target.
- Pick the ending characters for all required rhyme lines before filling the rest.
- Prefer tone-stable, non-polyphonic characters and no punctuation.
- If a line’s tone is uncertain, check that line with `python`; do not guess.

Route out:
- Go to Mirror after the full poem is written to `/root/poem.txt`.

### Mirror
Local view:
- `/root/poem.txt`
- copied visible pattern and rhyme logic

Actions:
- Run one small `python` mirror using the same non-empty-line parsing, CJK counting, tone mapping, chosen visible pattern, and visible rhyme normalization.
- The mirror must answer the real question: does one full visible form match? Structure-only or rhyme-only checking is not enough.
- Do not use unofficial or unavailable helper tools.

Route out:
- If the mirror rejects any line, go back to Compose with the failing line numbers.
- If the mirror confirms one full match, go to OfficialVerifier.

### OfficialVerifier
Actions:
- Run `run_tests`.
- If it passes, finish.
- If it fails, use `first_error` and go to Repair.

### Repair
Local view:
- `first_error`
- current `/root/poem.txt`
- copied visible pattern and rhyme logic

Actions:
- Repair only the first concrete mismatch.
- If the failure is `No strict Qilv form matched`, treat the report as line-specific form evidence: rewrite the listed failing lines against the chosen visible pattern, then rerun Mirror before `run_tests`.
- Do not spend repair steps polishing theme or title while form still fails.

Route out:
- `Repair -> Mirror -> OfficialVerifier` until pass or last-step finalizer.

### Finalizer
Operational rule:
- Every turn must emit exactly one allowed tool call or one final answer; never emit commentary-only turns.
- If the max-step finalizer fires, use the single last action to restore or rewrite the best known schema-complete, mirror-checked `/root/poem.txt`.
- Do not spend that last action on more inspection.
- If the poem is already mirror-checked and only the official run is missing, the last action may be `run_tests`; otherwise preserve the poem and stop.

## Route summary

`Contract -> Scaffold -> Compose -> Mirror -> OfficialVerifier -> (pass: done, fail: Repair -> Mirror -> OfficialVerifier) -> Finalizer`
