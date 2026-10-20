# backend/src/health/universal

Regex/lexer fallbacks used when a language lacks a tree-sitter grammar or when
AST metrics need a text-level pass.

- `strip.ts` owns `stripStringsAndComments` (the scanner core plus
  string/comment/template lexing); it must preserve input length and newline
  positions so downstream ranges/line counts stay aligned.
- `stripRegex.ts` holds the JS-semantics regex-vs-division disambiguation
  (`consumeRegexLiteral`) so a regex like `/[0-9]{3}/` is blanked as a string
  rather than read as division. `strip.ts` invokes it for EVERY extension (it
  is not gated on language), so gating it would change smell counts for
  non-JS files and needs a `CACHE_VERSION` bump.
- The lexer distinguishes string, template interpolation, line-comment, and
  block-comment modes. Template `${...}` code is intentionally re-entered so
  regex smells can still see expressions inside templates.
- Keep the regex-vs-division heuristic conservative; false positives in JS/TS
  quickly distort universal smells.
- `commentSyntax.ts` is the per-language marker table; update it before adding
  ad-hoc comment regexes elsewhere. It also carries per-language lexing flags:
  `quoteLifetimes` (set on `.rs` only) makes `strip.ts` treat a `'` that opens
  a lifetime/label (`&'a str`, `<'a>`, `'static`, `'outer: loop` — `'` +
  identifier not closed as a char literal) as code; char literals (`'a'`,
  `'\n'`, `'é'`) are still blanked. Every other language lexes `'` exactly as
  before. Any change to what the strip pass emits changes smell counts and
  needs a `CACHE_VERSION` bump (`../cachePaths.ts`; v5 was this one).
- `lineCounts.ts` counts blank/comment/code lines from source text and comment
  syntax, not AST nodes.
- `smells.ts` should stay heuristic-only; AST-backed smells belong in
  `health/walker/`.
- Universal coverage lives in `backend/src/__tests__/universal.test.ts`
  (including the Rust lifetime / label / char-literal cases and a pin that
  non-Rust lexing is unchanged).
