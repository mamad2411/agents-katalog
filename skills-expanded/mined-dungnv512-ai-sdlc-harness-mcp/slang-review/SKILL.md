---
name: slang-review
description: Read-only, repo-wide audit for hard-coded user-facing strings and Slang localization boundary violations across every StockBook module. Use when the user asks to check the whole codebase for hard-coded text, verify i18n coverage before a release, or audit Slang ownership/config duplication across modules — not for fixing one feature's strings (use /i18n for that).
---

# slang-review

Audits the entire repository for user-facing text that bypasses Slang, and
for violations of the per-module Slang ownership rules in the root
`CLAUDE.md`. This is a **report-only** pass — it finds and lists problems,
it does not edit call sites or translation files. Use `/i18n` (scoped to a
feature or the current diff) to actually extract and fix findings this
skill surfaces.

## Steps

1. Enumerate scope: every `modules/<name>/lib/src/presentation/**`,
   `lib/` (app shell), and any widget/dialog/snackbar/exception-message
   code outside `domain/`. Skip `docs/`, `docs/raw/`, `docs/wiki/`,
   generated files (`*.g.dart`, `*.freezed.dart`, slang's own
   `*.i18n.dart` output) and test fixtures unless the user asks for tests
   too.
2. Grep for hard-coded literal text reaching the UI, per module:
   - `Text('...')` / `Text("...")` with alphabetic content (not a single
     icon glyph, number, or interpolated variable-only string).
   - String literals passed to `SnackBar(content: ...)`,
     `showDialog`/`AlertDialog(title:|content:)`,
     `AppBar(title: Text(...))`, `Tooltip(message: ...)`,
     `TextField(decoration: InputDecoration(hintText:|labelText: ...))`.
   - Exception/failure messages built from string literals that a UI
     layer later displays (not internal log-only messages).
   - String concatenation or interpolation building user copy inline
     (`'Hello, ' + name`, `'${count} items'`) instead of an ICU
     placeholder in a Slang key.
3. For each finding, capture file:line, the literal text, and the
   feature module it belongs to.
4. Cross-check module Slang ownership against `CLAUDE.md`'s localization
   rules:
   - Confirm the string's owning feature module has its own Slang source
     translations, config and generated accessors — a feature must not
     reach into another module's `t.<namespace>` output.
   - Flag any `core` string that names a StockBook business concept
     (only genuinely common, feature-independent strings belong in
     `core`).
   - Flag a Slang dependency/config duplicated in `modules/shared/` or
     elsewhere purely to simulate inheriting a feature's setup.
   - Flag any hand-edited generated Slang output (diff a generated file
     against what `dart run slang` would produce, or check for edits not
     matching the generator's known output shape).
5. Group the report by module, then by finding type (hard-coded string /
   ownership violation / duplicated config / hand-edited generated file).
   For each hard-coded string, suggest a candidate key in the owning
   feature's namespace (e.g. `feedComposerHint`) — do not create it.
6. If the user wants findings fixed, hand off explicitly: "run `/i18n
   <feature-slug>` for module X" rather than editing translation files or
   call sites yourself.

## Anti-patterns to refuse

- Editing any `lib/i18n/<locale>.json`, call site, or generated Slang file
  — that is `/i18n`'s job, not this skill's.
- Introducing or recommending Flutter's built-in `l10n.yaml` / ARB /
  `AppLocalizations` — Slang is StockBook's only localization system.
- Flagging strings inside `domain/` layers, log-only messages, or
  developer-facing debug output as violations — they are not user-facing
  and are out of scope.
- Treating a `stale`/unverified doc claim about copy as ground truth for
  what a string should say — this skill audits code against `CLAUDE.md`
  and the Slang config on disk, not the product spec.
- Silently allowlisting a hand-edited generated file instead of reporting
  it as a violation.
