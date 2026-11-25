---
name: prose-guard
description: Enforce this user's writing conventions on any human-facing English, chiefly no em dashes, no AI-tell vocabulary, no hedge stacking, and no bullet bloat. Use when writing or editing a README, docs, CLAUDE.md, commit message, PR body, or release note, and whenever asked to review, tighten, de-slop, or humanize writing. Detection runs through scripts/prose_lint.py rather than by reading files.
---

# prose-guard

## Order of operations

Run the linter first. Do not read files hunting for violations by hand, that is what the script is for.

```bash
python <skill>/scripts/prose_lint.py <paths...>
```

With no paths it lints every git-tracked `.md` file in the repo. Output is one finding per line as `path:line:col [rule] message`.

Then fix what it found, and re-run until clean.

## Flags worth knowing

| Flag | Effect |
| --- | --- |
| `--fail-on medium` | Treat medium findings as failures too. Use on docs meant for other people. |
| `--fix` | Rewrites the two unambiguous shapes: a pair of dashes around an aside becomes commas, and a dash after a bold or code term that opens a line becomes a colon. Reports the rest. Re-read the touched lines afterwards. |
| `--json` | Machine-readable, for wiring into a hook or CI. |
| `--stats` | Counts by rule instead of per-line findings. Use on a large first pass. |

## Fixing

The rules themselves live in [references/rules.md](references/rules.md). Read that file when you need the reasoning or the rewrite patterns, not before.

Two rules need judgment rather than a mechanical swap:

- **Em dashes.** The replacement depends on the clause. A parenthetical takes commas or parentheses. A pivot takes a period and a new sentence. A list intro takes a colon. Do not blanket-replace with commas.
- **Medium-severity words.** `robust`, `curated`, `comprehensive`, `state of the art` and similar are legitimate in technical writing. Keep them where they carry meaning, cut them where they are decoration. Full list and the replacement table are in [references/tells.md](references/tells.md).

## Writing new prose

When you are producing the text rather than reviewing it, apply the hard rules as you write and run the linter once at the end. The four that catch most output:

1. No em dashes anywhere.
2. Delete the opener. Start on the claim.
3. One hedge per sentence, or none.
4. If a bullet is over forty words, it is a paragraph.

## Scope

Skip files the user has said are stored verbatim, vendored third-party text, and generated output. If a file is exempt for good, add `<!-- prose-lint: off -->` at the top rather than remembering to pass `--exclude` every time.
