---
name: regex-build
description: Sanook constructs, explains, and tests regular expressions for a stated matching goal — building the pattern, generating positive/negative test cases, and validating against them, while flagging catastrophic-backtracking (ReDoS) risk.
when_to_use: User asks to write/fix/explain a regex, validate input (email/URL/slug/date), extract or replace by pattern, or debug why a pattern over/under-matches.
---

## When to Use

Trigger this skill when the user wants to write, fix, explain, or debug a regular expression. Concrete cues:

- "write a regex that matches X" / "match a valid email|URL|slug|UUID|date|phone|hex color"
- "validate this input" / "extract all X from this text" / "replace X with Y by pattern"
- "why does my regex also match Z" (over-matching) or "why doesn't it match W" (under-matching)
- "is this regex safe / why is it slow / will this hang on big input" (ReDoS)

Do NOT use for: literal string `find/replace` (use a plain string op), glob/shell patterns (`*.js` is not regex), or SQL `LIKE` patterns. Redirect those to the right tool instead of forcing a regex.

## Steps

1. **Pin down two things before writing anything: the exact match goal and the engine flavor.** Flavor changes syntax, so never assume:
   - JS (`RegExp`) — no `\A`/`\Z`, no possessive quantifiers, no atomic groups (pre-ES2018), lookbehind needs modern V8, named groups `(?<name>...)`.
   - PCRE / Python `re` — full feature set: lookbehind, named groups `(?P<name>...)` in Python, atomic groups `(?>...)`, possessive `*+`.
   - Go / RE2 (`regexp`) — **linear-time, no backtracking**: no lookaround, no backreferences at all. If the user needs those, RE2 cannot do it — say so and propose a split-step approach.
   - .NET — has balancing groups; rarely needed but available.
   If the user didn't say, ask once or infer from the surrounding code/file extension, then state the flavor you're targeting.

2. **Clarify ambiguous scope with the smallest set of edge questions, not a generic "give me examples."** For an "email" ask: subdomains? plus-addressing (`a+b@`)? unicode local part? trailing dots? For a "date" ask: which separators, zero-padded, real calendar validation or shape-only? Lock the boundary before coding — most regex bugs are spec bugs.

3. **Build incrementally, not as one blob.** Compose from named fragments and assemble:
   - Anchor when validating a whole string: `^...$` (JS/PCRE) — and remember `$` matches before a trailing `\n`; use `\z` (PCRE/Python) or check length if a trailing newline must be rejected.
   - Default to **specific character classes over `.`** (`[^@\s]` beats `.` for an email local part). `.` is the #1 over-match cause.
   - Make quantifiers **non-greedy (`*?`/`+?`) only when greedy genuinely over-reaches** (e.g. matching `<.+?>` in HTML-ish text). Greedy is the correct default otherwise.
   - Escape regex metacharacters in literal segments: `. ^ $ * + ? ( ) [ ] { } | \ /`.
   - Use non-capturing groups `(?:...)` for grouping-only; reserve capture groups for values you actually extract, and name them.

4. **Generate a should-match / should-NOT-match table and actually run it — do not eyeball.** Build a table of ~5–10 positives and ~5–10 negatives that probe the boundaries you clarified in step 2 (empty string, leading/trailing whitespace, near-miss, unicode, max length). Run it in the target engine and show the pass/fail grid:
   - Node: `node -e "const re=/.../; for(const s of [...]) console.log(re.test(s), JSON.stringify(s))"`
   - Python: `python3 -c "import re; ... [print(bool(re.fullmatch(p,s)), repr(s)) for s in cases]"` — note `fullmatch` vs `search` vs `match` is itself a frequent bug; pick deliberately.
   - Go: `go run` a tiny `regexp.MatchString` loop.
   Every negative must return False and every positive True. If any cell is wrong, fix the pattern and re-run — never ship an unverified regex.

5. **Give a token-by-token plain-language breakdown** so the user can maintain it. One line per meaningful token/group. For non-trivial patterns, also provide the **`x`/verbose (extended) form with inline comments** (`(?x)` in PCRE/Python, or a commented build-up in JS) as the maintainable artifact.

6. **Run a ReDoS check and state the verdict explicitly.** Scan for the dangerous shapes:
   - Nested quantifiers: `(a+)+`, `(a*)*`, `(.+)+`
   - Quantified alternation with overlap: `(a|a)*`, `(\d+|\w+)*`
   - Adjacent overlapping quantifiers around an optional/repeatable seam, e.g. `\s*\s*`, `(\w+\s?)*$`
   These cause **exponential backtracking** on a long non-matching input. If found: demonstrate the risk conceptually, then rewrite — use atomic groups `(?>...)` / possessive `*+` (PCRE), anchor and tighten classes to remove overlap, or recommend a linear-time engine (RE2/`re2`) when the pattern stays untrusted-input-facing. State "ReDoS: safe" or "ReDoS: vulnerable → use <rewrite>" — don't leave it implicit.

7. **Deliver the final artifact in the user's engine syntax**, including the language-literal form (JS `/.../flags`, Python raw string `r"..."`, Go backtick string) and the correct flags (`i`, `m`, `s`/DOTALL, `u`/unicode, `g` for global). If they need more than one flavor, give each variant separately — don't hand them a PCRE pattern to paste into JS.

## Common Errors

- **`.` over-matching.** `.` excludes newline by default (except with `s`/DOTALL) but matches everything else including the very char you wanted to stop at. Replace with a negated class.
- **`$` and trailing newline.** In most engines `^abc$` matches `"abc\n"`. Use `\z` (PCRE/Python) for strict end, and remember `$` is line-end under `m`/MULTILINE.
- **Unescaped delimiter / metachar.** Forgetting to escape `/` in a JS literal, or treating `.`/`-`/`|` inside a class as special when they often aren't (`-` is literal at class edges; `.` is literal inside `[...]`). Over-escaping inside `[...]` is also a smell.
- **Wrong match function.** `re.match` anchors only at start, `re.search` is unanchored, `re.fullmatch` anchors both ends — using `search` for validation lets `"abc evil"` pass. JS `.test()` is unanchored too; anchor the pattern.
- **Greedy capture swallowing.** `".*"` across multiple quoted spans grabs the whole line; `".*?"` or `"[^"]*"` is what you meant.
- **`\d`/`\w` are unicode-wide.** With `u` flag (JS) or by default (Python 3, PCRE UCP), `\d` can match non-ASCII digits and `\w` matches accented letters/underscore. Use `[0-9]`/`[A-Za-z0-9_]` when you mean ASCII.
- **RE2/Go has no lookaround or backreferences — at all.** A pattern that compiles in PCRE will fail to compile in Go. Don't port blindly.
- **Backreference ≠ named group reference confusion** across flavors (`\1` vs `\k<name>` vs `(?P=name)`).
- **Catastrophic backtracking shipped to prod.** A regex that passes on your 10 test strings can hang for seconds/minutes on a crafted 50-char input. The test table won't catch it — the explicit ReDoS scan in step 6 is what catches it.

## Verify

Before declaring done, confirm all of:

1. Every positive test case returns a match and every negative returns no match, **shown as runnable output** (not asserted by hand). Boundary cases (empty, whitespace-padded, near-miss, max-length, unicode) are present in the table.
2. The pattern is anchored correctly for the task (whole-string validation vs. scan/extract) and the right match function is used.
3. The ReDoS verdict is stated explicitly ("safe" or "vulnerable → rewrite given"), with no nested/overlapping quantifiers left in a shippable pattern that faces untrusted input.
4. The final artifact is in the user's actual engine flavor and language-literal form, with the correct flags listed.
5. A token-by-token (or verbose-mode) breakdown is included so the user can maintain it.
