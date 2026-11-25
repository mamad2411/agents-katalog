---
name: ccsn-no-comments
description: 'Use in the cc-safety-net repo when `bun run lint:comments` or `bun run check` reports a comment, a stale comment-allowlist entry, or a file it cannot parse, and before writing a code comment there. Moves what each comment says into code, a test, or the PR description instead of deleting it and losing it.'
---

# Fixing CC Safety Net Comment Failures

`bun run lint:comments`, part of `bun run check` and CI, rejects code comments. The lazy fix, deleting the comment, loses what it said. For each reported comment, decide which kind it is and move what it says to where that kind belongs. The Comments and Style Guide sections of `AGENTS.md` govern.

## Each Reported Comment

- **Narration** that restates the code, and **commented-out code**: delete it. The code already says the first, and git keeps the second.
- **An explanation of surprising behavior in this repo's own code**: make the code say it with a clearer name, a named value or local boolean, or a type, then delete the comment. The Style Guide forbids a single-use helper function just to carry a name; name a value or condition inside the function instead, which the Style Guide allows even when it is used once.
- **A claimed constraint** ("do not remove", "IMPORTANT", "must", a justification for a workaround): leave the code's behavior as it is, and check the claim before trusting it. Read `git blame -L <start>,<end> <file>` and the commit it points to, run `git log -p -S '<distinctive fragment>' -- <file>`, and search `tests/` for a test that pins it. A constraint you confirm gets a test or a type when that is cheap: remove the workaround, see the new test or type check fail, then restore it. Otherwise, or when you cannot confirm or rule it out, state the claim and what you found in the PR description. The comment goes either way.
- **A fact about an external tool** (git, POSIX shell, the OS, Bun, Node, a host agent) that code cannot express: remove it from the code, and put the fact and its source (documentation link, version, or commit) in the PR description. Only the maintainer adds entries to `scripts/comment-allowlist.json`; never add one or change its text.

## Allowed Directives

The check accepts exactly three comments without an allowlist entry:

- a bare `/** @internal */` with nothing else in it, for a test-only export (see the Knip section of `AGENTS.md`);
- `// oxlint-disable-next-line <rules> -- <reason>`, with comma-separated rule names and a non-empty reason;
- `// @ts-expect-error <reason>`, with a non-empty reason.

Before writing a lint suppression, check whether the rule is catching a real bug. If it is, fix the code instead.

## Other Failures

- `cannot be parsed`: fix the syntax error first, then rerun before acting on anything else reported for that file. The check misses comments after the error, so a stale entry for that file may be false.
- `stale entry for <path>`: the entry's exact text is no longer a comment in `<path>`. If the check also reports that comment in `<path>` with edited text, restore the entry's exact text. If it reports the entry's exact text in another file, you moved the comment or renamed its file: keep the comment and the entry, and stop and ask the maintainer to move the entry. Otherwise the comment is gone: delete the entry from `scripts/comment-allowlist.json`.

## Never Dodge The Check

- Do not move comment text into strings or string constants.
- Do not edit `scripts/check-comments.ts` to let a comment through.

## Finish

Run `bun run lint:comments` until it passes, then run `bun run check` once as the final check.
