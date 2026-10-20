---
name: messageformat
description: >-
  Unicode MessageFormat (MF2, LDML 48.2): write, review and implement localizable messages with .input, .local, .match variants, placeholders, markup and escaping; the default functions (:string, :number, :integer, :offset, :currency, :percent Stable; :date, :time, :datetime, :unit Draft); plural, ordinal and exact selection; errors and fallbacks; bidi isolation; the JSON data model. Also ICU MessageFormat 1 ({count, plural, one {...} other {...}}, select, selectordinal, #, apostrophe quoting) and migrating it to MF2. Lines: Unicode MessageFormat LDML 48 (current), LDML 47 (supported), ICU MessageFormat 1 (own family, older format), LDML 49 draft (preview, track); the LDML 45 to 46.1 tech preview is legacy. Use when writing or translating UI strings, building a message formatter, parser or linter, fixing plural bugs, or converting ICU MessageFormat patterns. Triggers: MessageFormat 2, MF2, UTS #35 Part 9, ICU MessageFormat, plural rules, CLDR, i18n, l10n.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode MessageFormat

Unicode MessageFormat, developed as MessageFormat 2.0 (MF2), is Part 9 of Unicode Technical Standard #35 (LDML), published by the Unicode Consortium. It defines the syntax, data model, formatting, selection and errors of dynamic, translatable messages, and succeeds ICU MessageFormat. With this skill the agent writes and reviews messages, implements or checks formatters, and migrates ICU MessageFormat 1 patterns.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Part 9 has no section numbers, so citations name its headings, such as (Matcher) or (Fallback Resolution). When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: message author or translator, implementer (parser, formatter, function handler), or tool builder (linter, converter, translation tool).
- Target version: Unicode MessageFormat LDML 48 (default, at 48.2). Unicode MessageFormat LDML 47 is supported for implementations that have not moved yet. The MessageFormat 2.0 Tech Preview is legacy: read it and upgrade from it, never author it. ICU MessageFormat 1 is a separate, older family: read it, maintain it where the runtime has nothing newer, and migrate it. The Unicode MessageFormat LDML 49 draft is a preview (posture: track): never emit it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the UTS #35 latest version and proposed update and the message-format-wg releases for a newer LDML release, and update the pins.
- Locales: the source locale and every target locale, as BCP 47 language tags.
- Output: a single string, or parts (for markup, rich text or a DOM).
- Function set: which default and custom functions the target implementation supports, and whether Draft functions are acceptable.
- Existing messages: their format (ICU MessageFormat 1, a tech-preview MF2 dialect, or none).

## Invariants

1. **Every `.match` has an all-`*` variant**, each variant has one key per selector, and no two variants share a key list (Matcher; Data Model Errors).
2. **Selectors are declared variables with a function**: `.input {$n :integer}` then `.match $n`; an expression in `.match` is not valid, nor is a selector with no function (Selector; Missing Selector Annotation).
3. **No redeclaration.** A variable is declared once and never after it was used in an earlier declaration (Declarations; Duplicate Declaration).
4. **Escape only what the syntax needs**: `\\`, `\{`, `\}` in patterns, `\\` and `\|` in quoted literals. There are no other escapes; newlines and apostrophes are plain text (Text; Literals; Escape Sequences).
5. **Pattern whitespace is content.** A simple message cannot start with `.`, and its leading and trailing spaces are kept; quote the pattern with `{{…}}` when a container might trim it (The Message; Text).
6. **A literal without a function is a string**: write `{42 :number}` to get a number (Expression Resolution).
7. **Numeric `select` is a literal** (`plural`, `ordinal` or `exact`). Exact numeric keys beat plural categories, which beat `*` (Number Selection).
8. **Know which functions are Draft.** In LDML 48.2, `:string`, `:number`, `:integer`, `:offset`, `:currency` and `:percent` are Stable; `:datetime`, `:date`, `:time` and `:unit` are Draft and may change (Stability Policy; Default Functions).
9. **Custom functions, markup, attributes and options on default functions use a namespace**, such as `:ns:fn`; `u:` is reserved (Names and Identifiers; Default Functions).
10. **Valid messages always format.** Failed expressions become fallbacks (`{$var}`, `{|lit|}`, `{:ns:fn}`), an invalid message becomes the context fallback or `{�}`, and the caller can find at least one error. Syntax and Data Model Errors come first (Error Handling; Fallback Resolution; Formatting Fallback Values).
11. **String output uses the Default Bidi Strategy** by default: placeholders are isolated with LRI, RLI or FSI and PDI by their direction, which is not guessed from the formatted characters (Handling Bidirectional Text).
12. **Markup formats to the empty string** in string output, and attributes never affect output (Formatting of the Selected Pattern; Attributes).
13. **Each expression is evaluated at most once**, and function handlers get read-only access to the context (Formatting; Function Handler).
14. **ICU MessageFormat 1 `plural`, `selectordinal` and `select` always have `other`** (ICU4J `PluralFormat`; `SelectFormat`).

## Workflow

1. **Pick the version.** Use Unicode MessageFormat LDML 48 unless a named implementation is on LDML 47 or only has ICU MessageFormat 1.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded, and it is neither the tech preview nor the LDML 49 draft.
2. **Set the formatting context.** Record the locale as a BCP 47 tag with its fallback chain, the base direction, the input variables and their types, and the available functions.
   -> [`references/selection-and-errors.md`](references/selection-and-errors.md)
   ✓ Every variable the message uses has a name, a type and a source.
3. **Write the message structure.** Choose a simple message or a complex one with `.input`, `.local` and a quoted pattern or matcher; escape text and literals.
   -> [`references/syntax.md`](references/syntax.md)
   ✓ The message parses with no Syntax Error.
4. **Choose functions and options.** Annotate each number, currency, percent or date with its function in a declaration, use only defined options, and flag Draft functions.
   -> [`references/functions.md`](references/functions.md)
   ✓ No option outside the spec unless namespaced; every Draft function is noted.
5. **Add selection.** Declare each selector, match on it, give each variant a full sentence, and include `*`. Use `plural` (default) or `ordinal` for counts and exact keys only for integers.
   -> [`references/selection-and-errors.md`](references/selection-and-errors.md)
   ✓ No Data Model Error, and translators can add the plural categories their language needs.
6. **Handle errors and fallback** (implementers). Emit the right error category, keep formatting valid messages, and use the fallback strings.
   -> [`references/selection-and-errors.md`](references/selection-and-errors.md)
   ✓ Each error example in the spec produces its named error and the documented fallback output.
7. **Handle direction.** Apply the Default Bidi Strategy for string output, expose direction for parts output, and use `u:dir` where a value's direction differs.
   -> [`references/selection-and-errors.md`](references/selection-and-errors.md)
   ✓ RTL values in an LTR message, and the reverse, are wrapped in isolates.
8. **Exchange messages** (tools). Use the interchange data model and validate JSON against `message.json`.
   -> [`references/syntax.md`](references/syntax.md)
   ✓ Parse, serialize and reparse gives an equivalent message.
9. **Migrate ICU MessageFormat 1** (when asked). Map arguments, flatten nested selection into one `.match`, and replace `#`, `offset:` and apostrophe quoting.
   -> [`references/icu-mf1-migration.md`](references/icu-mf1-migration.md)
   ✓ The MF2 message formats the same output as the MF1 pattern for the same inputs and locales.
10. **Upgrade** (only when asked). Follow the upgrade section for each step from the source version to the target.
    -> [`references/versions.md`](references/versions.md)
    ✓ The message parses and validates under LDML 48 and formats the same.

## Verify before done

- [ ] Every message is well-formed and valid under the LDML 48 ABNF and Data Model rules; run it through a parser or the message-format-wg test suite cases where available.
- [ ] Every `.match` selector is a declared variable with a function, every variant has one key per selector, and an all-`*` variant exists.
- [ ] Numeric selectors use a literal `select`, and no exact key depends on fraction or significant-digit options (Exact Literal Match Serialization).
- [ ] Only Stable functions are used, or each Draft one (`:datetime`, `:date`, `:time`, `:unit`) is called out.
- [ ] Custom functions and options are namespaced; no `u:locale` remains.
- [ ] Text escapes only `\`, `{`, `}`; quoted literals escape only `\`, `|`; bidi controls sit inside placeholder braces, not in the output text.
- [ ] Implementations: errors are reported with Syntax and Data Model Errors first, valid messages still format, fallbacks match the spec strings, and string output uses the Default Bidi Strategy.
- [ ] Migrated ICU MessageFormat 1 messages give the same output for the same inputs, and `other` became `*`.
- [ ] Nothing from the LDML 49 draft is relied on.

## Reference index

- **`references/versions.md`**: every version line with its status, which to use, what changed per LDML release, upgrade steps and the LDML 49 draft. Load for steps 1 and 10.
- **`references/syntax.md`**: simple and complex messages, declarations, patterns, escaping, expressions, matcher, keys, markup, attributes, names, whitespace and bidi in the source, and the interchange data model with `message.json`. Load for steps 3 and 8.
- **`references/functions.md`**: Stable and Draft default functions with their operands, options and defaults, `u:id`, `u:dir`, and custom function rules. Load for step 4.
- **`references/selection-and-errors.md`**: formatting context, pattern selection, number selection, translator-friendly variants, error categories and handling, fallback strings, the Default Bidi Strategy and security. Load for steps 2, 5, 6 and 7.
- **`references/icu-mf1-migration.md`**: ICU MessageFormat 1 syntax, plural, select, `#`, offsets and apostrophe quoting, and the mapping and steps to Unicode MessageFormat. Load for step 9.

## Related skills

- `ecmascript-temporal` for the date and time values passed to `:datetime`, `:date` and `:time`: `npx skills add ScaleDockHQ/scaledock-skills --skill ecmascript-temporal`.
- `wcag` for accessible presentation of the formatted text, including language and direction: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`.
- `cldr`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill cldr`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [UTS #35 Part 9: MessageFormat (latest)](https://www.unicode.org/reports/tr35/tr35-messageFormat.html): Unicode Technical Standard (approved, stable), LDML 48.2 (tr35-78, 2026-03-03), checked 2026-10-05.
- [UTS #35 Part 9: MessageFormat, LDML 49 draft](https://www.unicode.org/reports/tr35/tr35-79/tr35-messageFormat.html): Proposed Update (draft), CLDR 49 draft (tr35-79, 2026-09-24), checked 2026-10-05.
- [UTS #35 Part 9: MessageFormat, LDML 47](https://www.unicode.org/reports/tr35/tr35-75/tr35-messageFormat.html): Unicode Technical Standard (superseded), LDML 47 (tr35-75), checked 2026-10-05.
- [UTS #35 Part 9: MessageFormat, LDML 46.1](https://www.unicode.org/reports/tr35/tr35-74/tr35-messageFormat.html): Unicode Technical Standard (superseded; MF2 Final Candidate), LDML 46.1 (tr35-74), checked 2026-10-05.
- [UTS #35 Part 9: MessageFormat, LDML 46](https://www.unicode.org/reports/tr35/tr35-73/tr35-messageFormat.html): Unicode Technical Standard (superseded; MF2 Tech Preview), LDML 46 (tr35-73), checked 2026-10-05.
- [UTS #35 Part 9: MessageFormat, LDML 45](https://www.unicode.org/reports/tr35/tr35-72/tr35-messageFormat.html): Unicode Technical Standard (superseded; MF2 Tech Preview), LDML 45 (tr35-72), checked 2026-10-05.
- [message-format-wg specification (editor's copy)](https://github.com/unicode-org/message-format-wg/tree/main/spec): editor's draft, `main` as of 2026-08-31, checked 2026-10-05.
- [message-format-wg releases](https://github.com/unicode-org/message-format-wg/releases): release notes, LDML48.2 (2026-04-21), checked 2026-10-05.
- [message-format-wg test suite](https://github.com/unicode-org/message-format-wg/tree/main/test): conformance tests, `main` as of 2026-08-31, checked 2026-10-05.
- [ICU User Guide: Formatting Messages](https://unicode-org.github.io/icu/userguide/format_parse/messages/): ICU documentation, current site (ICU 79 listed), checked 2026-10-05.
- [ICU4J MessageFormat API](https://unicode-org.github.io/icu-docs/apidoc/released/icu4j/com/ibm/icu/text/MessageFormat.html): API documentation, ICU4J 78, checked 2026-10-05.
- [ICU4J PluralFormat API](https://unicode-org.github.io/icu-docs/apidoc/released/icu4j/com/ibm/icu/text/PluralFormat.html): API documentation, ICU4J 78, checked 2026-10-05.
- [ICU4J SelectFormat API](https://unicode-org.github.io/icu-docs/apidoc/released/icu4j/com/ibm/icu/text/SelectFormat.html): API documentation, ICU4J 78, checked 2026-10-05.
- [ICU4J MessagePattern.ApostropheMode API](https://unicode-org.github.io/icu-docs/apidoc/released/icu4j/com/ibm/icu/text/MessagePattern.ApostropheMode.html): API documentation (Stable since ICU 4.8), ICU4J 78, checked 2026-10-05.
- [BCP 47](https://www.rfc-editor.org/info/bcp47): IETF Best Current Practice, RFC 5646 and RFC 4647, checked 2026-10-05.
- [RFC 5646: Tags for Identifying Languages](https://www.rfc-editor.org/rfc/rfc5646): RFC (Best Current Practice, BCP 47), RFC 5646, checked 2026-10-05.
- [RFC 4647: Matching of Language Tags](https://www.rfc-editor.org/rfc/rfc4647): RFC (Best Current Practice, BCP 47), RFC 4647, checked 2026-10-05.
