---
name: i18n-scan
description: "i18n detector: copy, catalog parity, plurals, formats, RTL, lang/dir, bidi."
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: i18n-scan

## Premise

An i18n defect is copy the user cannot read in their own language, or a layout that is wrong in it. An English label sits in an Arabic screen. A key exists in `en` and nowhere else, so production renders `orders.card.invalid_status`. `count === 1 ? 'item' : 'items'` is right for English and wrong for the six CLDR plural categories of Arabic. A date formats in the server's locale. `margin-left` puts the gap on the wrong side of an RTL layout. A Latin username scrambles the punctuation of the Arabic sentence around it. None of this fails a type check or a test written in the developer's locale, and most of it is invisible until a second locale ships.

**Every finding cites the site `<file:line>` (or the catalog set, key and locale) + the class + the route or screen that renders it + the oracle that failed, or the test that would settle it + the fix in the project's i18n library.** A grep hit, a lint message or a script row is a candidate, never a finding by itself. "No i18n defects" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution.** The static half is the pre-flight below plus a catalog script that diffs every locale's keys, placeholders and plural forms. The proof is a render or a unit test under a second locale: a pseudo-locale walk, a missing-key run, a plural matrix, an RTL mirror check ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Pseudo-locale and RTL mirror", variants V111 and V112). A candidate with no harness is **Unconfirmed**, carrying the test that would settle it. It is never dropped as "speculative" and never promoted on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The locale-count gate

Decide the gate before any class runs, and print it in the header. It comes from the catalog script's `GATE:` line plus pre-flight greps 0a–0d.

| Gate | When | What runs |
|---|---|---|
| **ON** | more than one locale declared (catalog files, `supportedLngs`, `locales: [...]`), or a non-`en` `lang` or `dir="rtl"` shipped, or the brief names a second market | every class; RTL classes (§5, §7 `dir`, §11) only when an RTL locale (`ar`, `he`, `fa`, `ur`, …) is declared or shipped |
| **CATALOG-ONLY** | one locale, but the project has an i18n layer: a library from 0a, or an in-house `t()` from 0c | §1, §2 (keys used but undefined), §3, §4, §10 at one severity step lower: the code is committed to externalising copy, and a bypass is convention drift. §5, §6, §7, §8, §11 print `N/A (single locale, no RTL)` |
| **OFF** | one locale and no i18n layer | every row `N/A (single-locale product, no i18n library)`. Not findings ([`precedents/ui.md`](../../../../snippets/precedents/ui.md) § 47–48 cover the RTL and expansion cases) |

The gate never downgrades a class silently. A row it turns off prints its `N/A` reason.

## The rule

A candidate is a finding when all four hold:

1. **It renders for a user.** A route or screen shows the string, the format or the layout. Dead components, Storybook-only files, design-system documentation pages the product declares single-language, and admin or dev routes declared untranslated fail here.
2. **The locale that breaks it ships.** The gate is ON for the class, and the locale the defect hurts is declared: an RTL locale for §5, a locale with more plural categories than English for §3.
3. **No existing control handles it.** A `<Trans>` child, an Angular `i18n`-marked element, a project `formatDate()` wrapper that injects the active locale, a server that already localizes its messages by `Accept-Language`, a `[dir]`-scoped override.
4. **The oracle fires, or would.** A failing test or render is a finding. A static fact passes with its two-ended trace: a key missing from a shipped locale's catalog, a hard-coded `lang="en"` on a multi-locale shell. Everything else without a harness is Unconfirmed, with the test written out.

## Boundaries

- **Clock and time-zone arithmetic** (a date off by a day, DST, `new Date()` in a range filter) → code-quality `correctness-smell-scan` §6, when the code-quality pack is installed. §4 here owns presentation: which locale, calendar, digits and currency format the user sees. Without that pack, report the arithmetic here tagged `correctness-class (owner pack not installed)`.
- **Locale-dependent output during SSR** (a hydration mismatch from `toLocaleDateString()` on server and client) → `ssr-audit` §1 (this pack). Server-side `i18next.changeLanguage()` on a shared instance, which serves one user's language to another, → `ssr-audit` §4. §4 here still reports the missing locale argument once.
- **The leak in raw server text** (a stack, SQL or internal detail) → security `data-exposure-scan` §1, when the security pack is installed. §10 here owns only the language: English server text in a localized UI. Without it, report the leak here tagged `security-class (owner pack not installed)`.
- **A cache key that omits the active locale**, which serves the previous language after a switch → `client-data-scan` §6 (this pack).
- **`<html lang>` as accessibility** (SC 3.1.1, axe `html-has-lang`) → `a11y-code-scan` grep 0d and `a11y-scan` (this pack). §7 here owns whether `lang` and `dir` follow the active locale. A site both report is one finding, credited to both.
- **`hreflang` reciprocity** → `seo-audit` and `@technical-seo` (this pack).
- **How an RTL layout should look** (mirrored motion, icon semantics, the visual language) → the ui-ux pack's `rtl.md` and `visual-check`'s RTL matrix row, when ui-ux is installed. §5 here owns whether the code can mirror at all.
- **Native screens** (Android, iOS, Flutter, Compose) → the mobile pack owns their layout and lifecycle. This skill owns their **catalogs** (§9) and carries a native lane for hard-coded text (grep 1f) and physical layout (grep 5e) until a mobile i18n detector ships.

## Adapt to the codebase — the i18n lanes

Read the library, the lint plugins **and their versions** from the lockfile, and print the lanes in the header. The rule ids and options below were read from the npm registry and package sources on 2026-10-05.

| Lane | Catalogs | Lint lane (keep only these `ruleId`s) | Missing-key hook for the oracle |
|---|---|---|---|
| **React / Next / RN** — i18next, react-i18next, next-intl | JSON namespaces | eslint-plugin-i18next **6.1.5** `i18next/no-literal-string`. The default mode `jsx-text-only` ignores attributes: run `{ mode: 'jsx-only', 'jsx-attributes': { include: ['alt','title','placeholder','aria-label'] } }` | `saveMissing: true` + a `missingKeyHandler` that throws in the test run; `i18next.exists(key, { lng })` |
| **formatjs / react-intl** | ICU JSON | eslint-plugin-formatjs **8.1.0**: `no-literal-string-in-jsx`, `prefer-full-sentence`, `enforce-plural-rules`, `no-invalid-icu`, `no-missing-icu-plural-one-placeholders`; `@formatjs/cli` 6.16.32 `compile` fails on bad ICU | the compile step |
| **Lingui** | PO / JSON | eslint-plugin-lingui **0.16.0**: `no-unlocalized-strings` (noisy until `ignoreFunctions` lists loggers), `no-single-variables-to-translate`, `no-expression-in-message`, `consistent-plural-format` | `lingui extract` + the catalog script |
| **Vue 3 / Nuxt** — vue-i18n, @nuxtjs/i18n | JSON / YAML / TS | @intlify/eslint-plugin-vue-i18n **4.5.1**: `no-raw-text`, `no-missing-keys`, `no-missing-keys-in-other-locales`, `no-unused-keys`, `no-dynamic-keys`, `valid-message-syntax`, `valid-plural-forms` (needs `settings['vue-i18n'].localeDir`); eslint-plugin-vue **10.11.1** `vue/no-bare-strings-in-template` (its default allow-list is punctuation only) | `missingWarn` + `fallbackWarn` turned into test failures |
| **Angular** — @angular/localize | XLIFF from `ng extract-i18n --format=xlf2` | @angular-eslint/eslint-plugin-template **22.5.0** `@angular-eslint/template/i18n` with `{ checkId: false, checkText: true, checkAttributes: true }`. Extraction sees only marked text, so unmarked text is invisible to it | the catalog script reads the XLIFF |
| **Svelte / Solid / Astro** — Paraglide, svelte-i18n | inlang messages / JSON | none mapped: rg only | Paraglide's typed `m.key()` makes a missing key a type error |
| **Styles** | — | stylelint 17.16.0 with stylelint-use-logical **2.1.3** `csstools/use-logical`, or stylelint-plugin-logical-css **2.1.0** `logical-css/require-logical-properties`, `-keywords`, `-units` (the 1.x `plugin/use-logical-*` names are gone); eslint-plugin-better-tailwindcss **4.8.0** `better-tailwindcss/enforce-logical-properties` (not in its recommended set) | — |
| **Native catalogs** | `strings.xml`, `.xcstrings`, `.strings`, ARB, PO | Android Lint `MissingTranslation`, `ExtraTranslation`, `StringFormatMatches`, `HardcodedText`, `RtlHardcoded`, `MissingQuantity`; Flutter `flutter gen-l10n --untranslated-messages-file` (flag unverified here: check `--help`) | the catalog script |

**`better-tailwindcss/enforce-logical-properties` rewrites more than direction.** Version 4.8.0 also maps vertical and size utilities (`mt-` → `mbs-`, `w-` → `inline-`, `h-` → `block-`, `top-` → `inset-bs-`). Those are writing-mode changes, irrelevant to RTL. Run it with the ignore list, or it buries the RTL rows:

```bash
# ROOTS as computed by the first line of § Pre-flight greps. Run only when the project's ESLint config loads the plugin;
# otherwise the lane is `blocked (plugin not installed)` — never install into the target repo, use a throwaway worktree.
npx --no eslint -f json --rule '{"i18next/no-literal-string":["error",{"mode":"jsx-only","jsx-attributes":{"include":["alt","title","placeholder","aria-label"]}}],"better-tailwindcss/enforce-logical-properties":["warn",{"ignore":["^(?:h|w|min-h|min-w|max-h|max-w|size|mt|mb|pt|pb|top|bottom|scroll-[mp][tb]|border-[tb])(?:-|$)"]}]}' "${ROOTS[@]}" > "${TMPDIR:-/tmp}/i18n-lint.json"
jq -r '.[] | .filePath as $f | .messages[] | select((.ruleId // "") | test("^(i18next/|formatjs/|lingui/|@intlify/vue-i18n/|vue/no-bare-strings|@angular-eslint/template/i18n|better-tailwindcss/enforce-logical)")) | "\($f):\(.line) \(.ruleId)"' "${TMPDIR:-/tmp}/i18n-lint.json" | sort | uniq -c | sort -rn | head -40
```

A lint lane that did not run is not a clean lane: §1 reads `checked (rg only; lint blocked: <reason>)`.

## The catalog script (§2, §9)

`scripts/catalog-parity.py`, beside this file (installed as `.claude/skills/i18n-scan/scripts/catalog-parity.py`). Python 3 standard library, read-only. Run it from the repo root:

```bash
python3 .claude/skills/i18n-scan/scripts/catalog-parity.py . --used="$(IFS=,; echo "${ROOTS[*]}")" --max=60
python3 .claude/skills/i18n-scan/scripts/catalog-parity.py --self-test
```

It finds every catalog whose path carries a locale token (JSON, YAML, TS/JS object catalogs, ARB, Android `values-*/strings.xml`, iOS `.lproj/*.strings` and `.xcstrings`, gettext PO, Angular XLIFF), groups the files that differ only by that token into **sets**, and prints the locales, the RTL locales, the base and the **gate**. Per set it reports `missing-file`, `missing-key`, `placeholder` (`{{n}}` vs `{n}`, `%1$s` vs `%s`, ICU arguments parsed so branch text is not mistaken for an argument), `plural-forms` (the categories `Intl.PluralRules` says each locale needs, via `node`), and `untranslated` (an empty value where another locale has one, a fuzzy or empty `msgstr`, an XLIFF target that is missing or `new`, an `.xcstrings` state other than `translated`). With `--used` it also reports `used-undefined` (a literal key that no catalog defines under any plausible namespace), and three candidate lists that each need a read: `dynamic-prefix` (including keys built on a string constant, `` `${KEY}.jt.${code}` ``, and `<fully dynamic>` heads), `unused-key` and `same-as-base`. Two finding shapes print as candidates instead: `placeholder-token` (a value that is one placeholder token in every locale, or a key read with `skipInterpolation`) and `untranslated-slot` (an empty value whose siblings share its stem — a word-order slot). Exit 1 on any finding row; candidates never set it.

**Cross-tree mode (`--v1=<laravel-root>`).** During a port from Laravel, `--v1` also reads V1's `lang/` and `resources/lang/` (`<locale>/**/*.php` arrays, `<locale>.json`; never written) and matches each V1 key to the V2 key of the same name, or the same name under the V2 file's stem, per locale. Findings: `v1-plural-forms` (a V1 pipe plural whose V2 key lacks a CLDR category the locale needs), `v1-plural-lost`, `v1-placeholder` (`:name` vs `{{name}}`); candidates: `v1-plural-range`, `v1-pipe-text`, `v1-unmapped`. The migration pack routes MG-I18N-1 (catalog and plural drift in a port) here, when the frontend pack is installed; its rows are graded under §2 (keys, placeholders) and §3 (plurals). A `--v1` with no `lang/` prints `v1 cross-tree: blocked`, never 0 rows.

i18next plural keys (`key_one` … `key_other`) fold into their base only when a locale has `<base>_other` **and** a second form or a `{{count}}`, so `errors.too_many` stays a key. A token that never shares a set with another locale (`team-hr.json` read as Croatian) is dropped with a note. Pass `--locales=` to keep one on purpose.

**The prefix × union sweep** (§2, dynamic keys). For each `dynamic-prefix` row: the prefix is the *supplied* set (catalog keys under it, which the script counts). Find what bounds the variable at its declaration — a TS union or enum, a `const` array, a DTO field, the API schema — and cite it as the *demanded* set. Supplied − demanded is **dead (dynamic)**, safe to propose for deletion now that the bound is cited. Demanded − supplied is **missing (dynamic)**: a key that exists in *no* locale, so parity is silent about it, and production renders the raw key for one value nobody clicked in QA. An unbounded variable (raw API text, tenant-supplied values) is `unresolvable: <prefix>` and needs a `defaultValue` or fallback at the call site. An unresolvable prefix with no fallback is a high finding. Report dynamic rows in their own block, never folded into the grep-complete ones.

**Measured** (2026-10-05) on a real bilingual SPA (React 19, Vite, i18next 26, Arabic default with English, about 4,700 web source files, plus a NestJS API with its own catalogs; read-only): 518 catalog files in 259 sets, locales `ar` and `en`, 0.4 s. The first version printed 262 `missing-file` rows from one false token (`team-hr.json` → `hr`) and 18 false `plural-forms` rows from key names ending `_many`, `_one` or `_other`. The directory-before-suffix order, the never-paired drop and the second-form rule removed all of them. The run then reports four `plural-forms` candidates, the shared catalog's `ar` count keys missing `zero` (read whether a count of 0 renders), one `untranslated` (an `en` value empty where `ar` has text), and nine `same-as-base` (provider and API terms). With `--used` over the web sources (13,332 literal and 1,351 dynamic calls, 2.5 s): `used-undefined` 4 → 0 once comment lines were skipped (all four were comments), 336 dynamic prefixes, and `unused-key` 1,707 → 276 once namespace mounts (`docs/<id>.json` mounted at `docs.<id>`), template prefixes and `` `${ns}:key` `` keys counted as references. A sample of 11 of the 276 had no reference outside comments. Re-measured 2026-10-15 on a real NestJS + React monorepo (React 19.2, i18next 26, Arabic default): the same command printed 509 `unused-key`, 41 % of them keys built on a string constant — `const KEY = 'ns:carrierReason'` then `` `${KEY}.jt.${code}` ``, and `` `ns:carrierCode.${family}.${code}` `` whose literal head carries a namespace — so `unused-key` was not "mostly real". The script now resolves both: 509 → 314 (195 credited, 0 newly reported, no change on the 20 benchmark fixtures), and a template whose head is a variable (`` `${group}.${key}.label` ``, 22 keys under a `'rules' | 'workflow'` union) prints as a `<fully dynamic>` `dynamic-prefix` row for the sweep instead of hiding. Its two finding rows became candidates: a `{{variable}}` / `{{متغير}}` display token read with `skipInterpolation` (`placeholder-token`) and an empty English middle slot between two hero-title halves (`untranslated-slot`); the exit code now comes only from four Arabic `zero` plural gaps. On a synthetic tree with one catalog per format, every planted row was reported and `values-night/`, `translatable="false"` and `shouldTranslate: false` were skipped.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 decides the gate. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. Files-without-match is `--files-without-match`, **never `-L`** (that is `--follow`). Any `rg` error on stderr (exit 2) is a failed grep, not zero hits. Run them only for the classes the gate turned on.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|react-native|vue|svelte|@angular/core|solid-js|preact|astro|next|nuxt|@builder\.io/qwik)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static,DerivedData,Pods,.dart_tool}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,fixtures,stories,playwright,cypress,scripts,tools,generated,__generated__}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!**/*.{test-data,fixture,fixtures}.*' -g '!ai/**' -g '!docs/**')
C=(-g '!**/{locales,locale,i18n,l10n,lang,translations}/**')      # catalogs and i18n plumbing: never a hard-coded-string site
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,html,astro}'); CSS=(-g '*.{css,scss,sass,less,vue,svelte,astro}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/?\*|<!--|#)')            # drop comment-only lines
# 0. The gate: 0a i18n libraries and lint plugins, 0b declared locales, 0c an in-house t() layer, 0d RTL shipped anywhere.
rg -n --no-heading '"(i18next|react-i18next|next-intl|next-i18next|vue-i18n|@nuxtjs/i18n|@angular/localize|@ngx-translate/core|@jsverse/transloco|@lingui/core|react-intl|@formatjs/intl|svelte-i18n|@inlang/paraglide-js|typesafe-i18n|i18n-js|expo-localization|react-native-localize|eslint-plugin-i18next|@intlify/eslint-plugin-vue-i18n|eslint-plugin-lingui|eslint-plugin-formatjs|@angular-eslint/eslint-plugin-template|eslint-plugin-vue|eslint-plugin-better-tailwindcss|stylelint-use-logical|stylelint-plugin-logical-css|pseudo-localization|tailwindcss)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --pcre2 '\b(?:supportedLngs|supportedLocales|SUPPORTED_(?:LANGS|LOCALES)|availableLocales|locales)\s*[:=]\s*\[|\b(?:defaultLocale|fallbackLng|sourceLocale)\s*:|createI18n\(|\bi18n\s*:\s*\{' "${UI[@]}" -g '*.json' -g '!**/package*.json' "${X[@]}" "${ROOTS[@]}" | head -20
rg -l --pcre2 '^\s*(?:export\s+)?(?:function\s+(?:t|translate|__)\s*\(|const\s+(?:t|translate)\s*=\s*(?:\(|function))' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\bdir\s*=\s*["\x27]rtl|\bdir\s*[:=]\s*["\x27]rtl|\bisRTL\b|forceRTL|supportsRtl|\brtl:' "${UI[@]}" -g '*.xml' "${X[@]}" "${ROOTS[@]}" | head -5
# 1. Hard-coded copy: 1a a text node on one line, text beside interpolations included (skips <Trans>-family children,
#    Angular i18n, and the code-like tags in the skip list — append the project's own code/LTR wrappers to it after the
#    first read), 1b a text node on its own line, 1c a user-facing attribute (skips alt="", Angular i18n-<attr> and
#    example formats: emails, URLs, values with digits), 1d a toast / alert / confirm / document.title literal with words
#    outside its ${…}, 1e a validation-schema message, 1f native text (Android XML, Compose, Flutter; SwiftUI Text("…") is a key),
#    1g an English label in a TS/JS label map (`{ value: 'manual', label: 'Manual' }`; bilingual rows with labelAr/nameAr skipped).
rg -n --pcre2 '^(?!.*<(?:Trans|T|FormattedMessage|i18n-t|Plural|Select)\b).*?<(?!(?:code|pre|kbd|samp|script|style|Code|CodeBlock|Kbd)\b)([A-Za-z][\w.-]*)(?![^>]*\bi18n\b)(?:\s[^<>]*)?>(?=(?:[^<>{}]|\{(?:[^{}]|\{[^{}]*\})*\})*?\p{L}{2})(?:[^<>{}]|\{(?:[^{}]|\{[^{}]*\})*\})+</\1>' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '(?<![=>-])>[ \t]*\n[ \t]*\K(?=[^<>{}\n]*\p{L}{2})(?![ \t]*(?://|/?\*|\}|\)|return\b|import\b|export\b|const\b|let\b|if\b|else\b))[^<>{}\n;=()]+(?=\n[ \t]*</?[A-Za-z{])' -g '*.{jsx,tsx,vue,svelte,html,astro}' "${X[@]}" "${C[@]}" "${ROOTS[@]}"
rg -n --pcre2 '(?<![:\[\w.-])(alt|title|placeholder|aria-label|aria-description|aria-placeholder|label)=(["\x27])(?![\w.+-]*@|https?:|[^"\x27\s]*\d[^"\x27\s]*\2)(?=[^"\x27{}]*\p{L}{2})[^"\x27{}]+\2(?![^>]*\bi18n-\1\b)' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:toast|notify|notification|enqueueSnackbar|snackbar|Swal\.fire|alert|confirm|prompt)(?:\s*\.\s*(?:success|error|info|warn(?:ing)?|show|open|loading|promise|message))?\s*\(\s*(["\x27\x60])(?=(?:[^"\x27\x60$]|\$(?!\{)|\$\{[^}]*\})*?\p{L}{2})|\bdocument\.title\s*=\s*(["\x27\x60])(?=[^"\x27\x60]*\p{L}{2})' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:message|required_error|invalid_type_error)\s*:\s*(["\x27\x60])(?=[^"\x27\x60]*\p{L}{2}[^"\x27\x60]*\s)|\.(?:min|max|length|email|url|uuid|regex|nonempty|required|matches|oneOf|typeError|refine)\((?:[^()"\x27\x60]*,\s*)?(["\x27\x60])(?=[^"\x27\x60]*\p{L}{2}[^"\x27\x60]*\s)' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'android:(?:text|hint|contentDescription)="(?!@)[^"]*\p{L}{2}|\bText\(\s*"(?=[^"]*\p{L}{2})[^"]*"\s*[,)]|\bText\(\s*\x27(?=[^\x27]*\p{L}{2})' -g '*.{xml,kt,dart}' "${X[@]}" .
rg -n --pcre2 '\b(?:label|title|header|heading|placeholder|description|hint|tooltip|emptyText)\s*:\s*(["\x27\x60])[A-Z][a-z]+(?:[ -][A-Za-z]+)*[.:!?]?\1' -g '*.{ts,tsx,js,jsx,mjs}' "${X[@]}" "${C[@]}" "${ROOTS[@]}" | rg -v --pcre2 '\b(?:labelAr|nameAr|titleAr|_ar)\b|@Api\w*\(' | "${NC[@]}"
# 3. Plurals and concatenation: 3a a plural comparison picking words or t() calls, 3b a plural `s` suffix, 3c translated
#    fragments joined with + or two t() calls in one template literal.
rg -n --pcre2 '\b(?:count|length|total|n|num\w*|qty|quantity|size|\w+Count)\s*(?:[!=]==?\s*1|>\s*1|<=\s*1|>=\s*2)\s*\?\s*(?:(["\x27\x60])(?=[^"\x27\x60]*\p{L}{2})|(?:t|\$t)\()' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\?\s*(["\x27\x60])s\1\s*:\s*(["\x27\x60])\2|\?\s*(["\x27\x60])\3\s*:\s*(["\x27\x60])s\4|\}\s*\+\s*["\x27\x60]s["\x27\x60]' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:t|\$t|i18n\.t|translate|intl\.formatMessage)\([^()]*\)\s*\+\s*(?:["\x27\x60]|\w)|(?:["\x27\x60]|\w)\s*\+\s*(?:t|\$t|i18n\.t)\(\s*["\x27\x60]|\$\{\s*(?:t|\$t)\([^}]*\}[^\x60]*\$\{\s*(?:t|\$t)\(' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. Presentation formatting: 4a locale-less or hard-locale date and number formatting (skips machine dates: padStart,
#    toISOString, YYYY-MM- templates, date arithmetic), 4b manual money and currency symbols.
rg -n --pcre2 '^(?!.*(?:padStart|toISOString|getFullYear\(\)\}-|getMonth\(\)\s*\+\s*1\s*,))(?:.*?)(?:\.toLocale(?:Date|Time)?String\(\s*\)|\.toLocale(?:Date|Time)?String\(\s*(?:undefined|["\x27][a-z]{2}(?:-[A-Z]{2})?["\x27])|new\s+Intl\.(?:DateTimeFormat|NumberFormat|RelativeTimeFormat|PluralRules|ListFormat|Collator|DisplayNames)\(\s*(?:\)|["\x27][a-z]{2}(?:-[A-Z]{2})?["\x27])|\.get(?:UTC)?Month\(\)\s*\+\s*1|\bformat\([^,()]+,\s*["\x27][dDMyYHhms/.: -]+["\x27]\s*\)|\bdayjs\([^)]*\)\.format\()' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '(?<![\w$])[$€£¥₹]\$\{|(["\x27\x60])[$€£¥₹]\1\s*\+|\.toFixed\(2\)|\$\{[^}]+\}\s*(?:USD|EUR|SAR|AED|EGP|GBP|KWD)\b' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. RTL: 5a physical CSS (skips [dir]/:dir() lines, rules whose selector — the nearest `{` line above — is under
#    [dir]/:dir(), and left/right pairs), 5a' a 4-value margin/padding/inset whose right
#    and left differ, 5b physical inline-style keys (skips four-sided box objects such as chart margins), 5c Tailwind
#    physical utilities in class contexts (skips rtl:/ltr:), 5d directional icons with no flip (skips two-way swap icons),
#    5e native layout (Android XML, Compose, Flutter, UIKit).
rg -n --pcre2 '^(?!.*(?:\[dir|:dir\(|\bleft\s*:[^;]*;\s*right\s*:|\bright\s*:[^;]*;\s*left\s*:))[^\n]*?(?:(?<![\w-])(?:margin|padding|border)-(?:left|right)(?:-\w+)?\s*:|(?<![\w-])(?:left|right)\s*:\s*(?!auto\b)|(?<![\w-])(?:text-align|float|clear)\s*:\s*(?:left|right)\b|(?<![\w-])border-(?:top|bottom)-(?:left|right)-radius\s*:|background-position\s*:\s*(?:left|right)\b)' "${CSS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | while IFS=: read -r f n rest; do awk -v n="$n" 'NR<=n && /[{]/ {s=$0} NR>=n {exit (s ~ /\[dir|:dir\(/)}' "$f" && printf '%s:%s:%s\n' "$f" "$n" "$rest"; done
rg -n --pcre2 '^(?!.*(?:\[dir|:dir\())[^\n]*\b(?:margin|padding|inset)\s*:\s*(\S+)\s+(\S+)\s+(\S+)\s+(?!\2\s*[;!}])\S+\s*[;!}]' "${CSS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^(?!.*\btop\s*:.*\bbottom\s*:|.*\bleft\s*:[^;,]*[;,]\s*right\s*:)(?:.*?)(?:\b(?:margin|padding|border)(?:Left|Right)\w*\s*:|\b(?:textAlign|float)\s*:\s*["\x27](?:left|right)|\b(?:left|right)\s*:\s*-?\d)' -g '*.{jsx,tsx,js,ts}' "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '(?:\bclass(?:Name)?\s*=\s*\{?\s*["\x27\x60]|\b(?:clsx|cn|cva|twMerge|twJoin|classnames|tw)\s*\((?:[^()"\x27\x60]|["\x27\x60][^"\x27\x60]*["\x27\x60])*?["\x27\x60]|\btw\x60)[^"\x27\x60]*?(?<![\w-])(?<!rtl:)(?<!ltr:)-?(?:m[lr]|p[lr]|left|right|scroll-[mp][lr]|border-[lr]|rounded-(?:[lr]|[tb][lr])|text-(?:left|right)|float-(?:left|right)|clear-(?:left|right))(?:-[\w./\[\]#%()-]+)?(?![\w-])' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}"
rg -n --pcre2 '<(?!\w*(?:RightLeft|LeftRight))(?:\w*(?:Chevron|Arrow|Caret)(?:Right|Left|Forward|Back)\w*|\w*(?:Right|Left)Arrow\w*)\b(?![^>]*(?:rtl:|scale-x-|rotate-180|mirror|flip))' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}"
rg -n --pcre2 'android:(?:layout_)?(?:margin|padding)(?:Left|Right)\b|android:(?:layout_)?gravity="(?:left|right)|absolute(?:Padding|Offset)\(|AbsoluteAlignment|Arrangement\.Absolute|TextAlign\.(?:Left|Right)\b|EdgeInsets\.(?:only|fromLTRB)\(|Alignment\.(?:centerLeft|centerRight|topLeft|topRight|bottomLeft|bottomRight)\b|Positioned\(\s*(?:left|right)\s*:|NSTextAlignment\.(?:left|right)|\.textAlignment\s*=\s*\.(?:left|right)|\.(?:left|right)Anchor\b' -g '*.{xml,kt,dart,swift}' "${X[@]}" .
# 6. Expansion: a fixed pixel width, and truncation or no-wrap on a line that renders a translated label with no title.
rg -n --pcre2 '\b(?:w|min-w|max-w)-\[\d{2,}px\]|(?<![\w-])(?:width|max-width)\s*:\s*\d{2,}px|^(?=.*(?:\{\s*t\(|\$t\(|\|\s*translate\b))(?!.*\btitle=)(?=.*\b(?:truncate|line-clamp-\d|whitespace-nowrap|text-ellipsis)\b)' "${UI[@]}" "${CSS[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7. <html lang>/dir: 7a a hard-coded lang, 7b the sites that sync lang/dir (no output with an RTL locale declared is the finding).
rg -n --pcre2 '<html\b(?![^>]*\blang=\{)[^>]*\blang=["\x27][a-z]{2}|htmlAttrs\s*:\s*\{[^}]*lang\s*:\s*["\x27]' -g '*.{html,tsx,jsx,vue,svelte,astro,ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'documentElement\.(?:dir|lang)\b|documentElement\.setAttribute\(\s*["\x27](?:dir|lang)|<html[^>]*\bdir=\{|:dir=|\[dir\]=|htmlAttrs[^}]*\bdir\b|useHead\([^)]*\bdir\b|<Html[^>]*\bdir=' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
# 8. Collation and casing on display text: a string sort with < or >, localeCompare with no locale (in a sort callback or
#    on a name-like field), locale-less case mapping, case-folded equality on a name-like field.
rg -n --pcre2 '\.sort\(\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*=>\s*\1(?:\.\w+)+\s*[<>]|\.sort\(\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*=>\s*\3(?:\??\.\w+)*\.localeCompare\(\s*\4(?:\??\.\w+)*\s*\)|\.(?:\w*[Nn]ame|title|label|city|country|description)\??\.localeCompare\(\s*[^,()]+\)|\.toLocale(?:Lower|Upper)Case\(\s*\)|\.(?:\w*[Nn]ame|title|label|city)(?:\.trim\(\))?\.toLowerCase\(\)\s*===' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 10. Raw server or exception text rendered: 10a JSX, Vue/Angular interpolation, a toast fed the message; 10b the project's
#     error→text helpers (`notifyError(e, fallback)` → `apiErrorMessage` → `error.message`): read each once — one helper is
#     the app-wide surface the inline grep never sees.
rg -n --pcre2 '(?:\{\{?\s*|\(\s*)(?:e|err|error|ex|exception)\??\.(?:message|response\??\.data\??\.(?:message|error|detail))\s*\}|toast\.error\(\s*(?:e|err|error)\??\.message' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '(?:export\s+)?(?:async\s+)?(?:function\s+\w*(?:[Ee]rror[Mm]essage|[Nn]otify[Ee]rror|[Tt]oast[Ee]rror|[Ss]how[Ee]rror|[Ee]rror[Tt]ext)\w*\s*[(<]|const\s+\w*(?:[Ee]rror[Mm]essage|[Nn]otify[Ee]rror|[Tt]oast[Ee]rror|[Ss]how[Ee]rror|[Ee]rror[Tt]ext)\w*\s*=\s*(?:async\s*)?\()' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 11. Bidi isolation: BW = the project's isolation wrappers (an exported component that renders {children} inside <bdi> or
#     dir="auto", e.g. `<Ltr>`), counted as isolation in 11a and 11c; 11a a user field beside other text on one line
#     (alone in its element it is isolated already), 11b a user field passed into a translated sentence, 11c the
#     isolation sites per file (no output = 0).
BW=$(rg -o -U --no-filename --pcre2 'export\s+(?:default\s+)?(?:function\s+([A-Z]\w*)|const\s+([A-Z]\w*)\s*=)[^\n]*\n(?:(?![ \t]*export\s)[^\n]*\n){0,30}?[^\n]*<(?:bdi\b|\w+\b[^>]*\bdir=["\x27{]+auto)[^>]*>\s*\{\s*(?:props\.)?children\s*\}' -r '$1$2' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | paste -sd'|' -); echo "11 isolation wrappers: ${BW:-none}"
rg -n --pcre2 '(?:\p{L}[^<>{}\n=]*|\}\s*)\{\{?\s*\w+\??\.(?:name|fullName|firstName|lastName|title|comment|description|username|email|displayName|phone)\s*\}\}?|\{\{?\s*\w+\??\.(?:name|fullName|firstName|lastName|title|comment|description|username|email|displayName|phone)\s*\}\}?(?:\s*\{|[^<>{}\n]*\p{L})' -g '*.{jsx,tsx,vue,svelte,html,astro}' "${X[@]}" "${C[@]}" "${ROOTS[@]}" | rg -v --pcre2 '<bdi|dir="auto"|unicode-bidi|\b(?:key|alt|src|href|value|id)=\{'"${BW:+|<(?:$BW)\\b}" | "${NC[@]}"
rg -n --pcre2 '\b(?:t|\$t|i18n\.t)\(\s*["\x27\x60][^"\x27\x60]+["\x27\x60]\s*,\s*\{[^}]*\b\w+\s*:\s*\w+\??\.(?:name|fullName|firstName|lastName|title|username|displayName)\b' "${UI[@]}" "${X[@]}" "${C[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -c --pcre2 '<bdi\b|dir="auto"|dir=\{["\x27]auto|unicode-bidi\s*:\s*isolate'"${BW:+|<(?:$BW)\\b}" "${UI[@]}" "${CSS[@]}" "${X[@]}" "${ROOTS[@]}"
```

Grep 2 and grep 9 are the catalog script. A finding is a hit **plus** a read of the component **plus** the route that renders it **plus** the oracle. Four blind spots are structural:

- **A label map hides the copy.** `const LABELS = { open: 'Open' }` rendered three files away is what 1g lists (one capitalised English word or phrase as a `label` / `title` / `hint` value); a lower-case value, a default prop `label = 'Submit'` and an `<option>` list built from an array stay invisible. The pseudo-locale walk sees all of them, and so does the i18next lint in `mode: 'all'`, at the price of noise.
- **A wrapper decides the direction.** A design-system `Stack` with a physical `gap`/`margin` prop, or a chart library's internal layout, is invisible to 5a–5c. Only the RTL mirror render sees it.
- **A dynamic key is invisible to parity.** Every `dynamic-prefix` row needs the prefix × union sweep, or §2 reads `checked (static keys only)`.
- **Text built outside the component** (an email or push template, a PDF or print template string, `confirm()` built in a hook) reaches the user with no JSX around it. Read the print and notification modules by name.

**Measured** (2026-10-05). On this batch's research fixtures (positives and decoys in React, Vue, Svelte and Angular): 1a 5/5 and 0/9 decoys (`<Trans>` children, `<code>`, Angular `i18n`, `{t('x')}` alone), 1c 5/5 (`alt=""`, `:placeholder`, `alt={m.x()}`, `i18n-title` skipped), 1d 2/2 (`console.error`, `logger.warn` skipped), 3a 2/2, 3c 2/2, 4a 4/4 (`toLocaleDateString(locale)`, `Intl.NumberFormat(locale, …)` skipped), 4b 1/1, 5a 6/6 (`[dir="rtl"]`, `margin-inline-start`, `text-align: start`, `margin: 0 auto`, `top: 0` skipped), 5b 1/1, 5c 6/6 (`rtl:mr-4 ltr:ml-4`, `ms-4 pe-2` skipped), 5d 1/1 (`rtl:rotate-180` skipped), 7a 1/1, 8 2/2, 10 4/4; on a second fixture 1b 2/2 (an Arabic line included), 1e 2/2 (a `t()` message skipped), 3b 1/1, 5a′ 2/2 (`4px 8px 4px 8px` skipped), 11a 1/1 (`<bdi>` skipped), 1f 3/3 and 5e 5/5 across Android XML, Compose, Flutter and UIKit (`@string/`, `EdgeInsets.symmetric`, `TextAlign.Start` skipped). `benchmarks/fixtures/web-dashboard`: 0c finds the in-house `t()` (gate CATALOG-ONLY), 1a returns WEB-I18N-01, 4b returns WEB-I18N-02, 5b returns the six inline `textAlign` sites. On the real bilingual SPA above the script runs in about 1 s. 1a returned 103 lines: 52 inside the project's own LTR wrapper on design-system documentation pages (append it to the skip list), 16 in print templates (read whether the print is locale-bound), and the rest mostly English labels in an Arabic-default UI (`Client ID`, `POS Serial`, `Type:`, `SKU:`) plus six brand or standard names. 1c 45 (example-format placeholders were the noise until the digit/email/URL exclusion), 1d 7 (three English toasts), 3a 4 (2 true: a binary plural in code), 3c 28 (labels assembled from two `t()` calls), 4a 2, 4b 9, 5a 1 (a centering `left: 50%`), 5b 2, 5c 2, 5d 0 after the swap-icon exclusion (it was 18, every one an `ArrowRightLeft` or `ArrowLeftRight`), 7a 1 and 7b 2 (`lang`/`dir` synced on switch), 8 23 (names sorted with no locale, beside ISO-date and code sorts), 10 9 (`error.message || t(…)`: read whether the API localizes by `Accept-Language`), 11a 13, 11b 27, 11c 27 files. Re-measured 2026-10-15 on a real NestJS + React monorepo (the same Arabic-default i18next 26 web app family): 1b 9 → 8 (a `*.test-data.tsx` builder, now excluded), new 1g 28 lines → three real groups (an English label map on a POS order card, `'Manual'` / `'Other'` in a geography source list, the WhatsApp template-variable labels) beside brand and theme names, 5a 2 → 1 (a `text-align: right` whose `[dir='rtl']` selector sits on the line above), new 10b 5 helpers — `notifyError(error, fallback)` → `apiErrorMessage` → `error.message` is the app-wide surface that 10a's single inline hit never showed, 11c 24 → 268 files once the project's `<Ltr>` isolation wrapper (a `<bdi dir="ltr">`) counts; 11a 17 → 17.

## The 3,000-hit path

1. **Intersect with the route table.** A component no route imports is dismissed with one read. Design-system documentation, Storybook-only and admin/dev routes the product declares single-language form their own group.
2. **Group.** One group = (component or shared wrapper, class) for code hits, and (catalog set, class) for script rows. A wrapper that hard-codes its label, or a namespace missing one locale, is one group however many call sites or keys it has. Fixing it there closes them all.
3. **Rank** by route traffic: RUM or analytics when present, else landing, auth, checkout-class, list and form routes. Rank error and empty states up: they surface when the user is already stuck.
4. **Read the top 30 groups.**
5. **Prefer the runtime bulk oracle at scale.** One pseudo-locale walk across the route matrix confirms or refutes every §1 group at once: a hit that never renders is dead code (Refuted), and a rendered unaccented string the greps missed is a new finding. One missing-key run over the e2e suite does the same for §2. One RTL mirror pass over the top routes does it for §5.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes the gate is ON and the route ships to the affected locale. Under CATALOG-ONLY, drop one step.

| § | Class | Research id | Default severity |
|---|---|---|---|
| 1 | Hard-coded copy: text nodes, user-facing attributes, toasts, confirms, titles, validation messages, native text | I-01, I-02, I-03 | high in new code on a translated route, and for an accessible name; medium in existing code |
| 2 | Catalog defects: missing file or key, key used but undefined, dynamic key with no bound, placeholder mismatch, invalid ICU, unused key | I-07, I-16 | high for a key missing in a shipped locale or a placeholder mismatch (a runtime error or a raw key); medium for an unbounded dynamic key; low for unused |
| 3 | Plural logic in code, concatenated fragments, a plural message missing a CLDR category | I-05, I-06 | high when Arabic or a Slavic locale ships; medium otherwise |
| 4 | Presentation formatting with no locale or a hard-coded one; manual money and currency symbols | I-08, I-09 | medium; high when it also renders during SSR (cross-link `ssr-audit` §1) |
| 5 | Physical CSS, inline styles, Tailwind utilities and native layout; directional icons that do not mirror | I-11, I-12, I-13 | medium; high on an RTL-primary product; low for icons |
| 6 | Text expansion clipped: fixed widths, truncation with no full value | I-17 | medium |
| 7 | `<html lang>` / `dir` hard-coded or not switched with the locale | I-14 | high when multi-locale |
| 8 | Locale-insensitive collation and case mapping on display text | I-10 | low; medium on a list users scan by name |
| 9 | Native catalogs: Android `strings.xml`, iOS String Catalog and `.strings`, Flutter ARB | — | as §2 |
| 10 | Raw server or exception text rendered to the user | I-04 | high |
| 11 | User content with no bidi isolation | I-15 | low; medium when names, phone numbers or amounts sit inside RTL sentences |

### 1. Hard-coded copy

```
BAD:   <Label>Client ID</Label>   ·   <input placeholder="Search orders" />   ·   toast.success('Marked as paid')
       z.string().email('Enter a valid email')   ·   <h2>Order summary</h2> (Vue)   ·   Text("Order summary") (Compose)
GOOD:  <Label>{t('integrations.clientId')}</Label>   ·   placeholder={t('orders.search')}   ·   toast.success(t('referrals.paid'))
       z.string().email({ message: t('validation.email') }), or the library's i18n error map   ·   {{ $t('order.summary') }}
       stringResource(R.string.summary)   ·   SwiftUI Text("order.summary") is already a localized key
```
**Read the code:** Is the string copy, or data (a SKU, a code, a user value, an API enum shown as a badge)? Is it a brand, product or standard name the project lists as untranslated? Does a `<Trans>` or `i18n` attribute wrap it a level up? Is the route translated, or declared single-language? For an attribute: is it the accessible name (`aria-label`, `alt`, an icon button's `title`)? Then a screen-reader user in the other locale hears the wrong language. **Finding when** the copy renders on a translated route. **Proof:** the pseudo-locale walk: the string renders with no pseudo marks ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Pseudo-locale and RTL mirror", V111). A toast or validation message needs its failure injected first (`page.route` → 500, an invalid submit).

### 2. Catalog defects

```
BAD:   locales/ar.json lacks products.form.name_placeholder   ·   en "{{count}} items" vs ar "{count} عناصر"
       t(`status.${s}`) with no bound on s   ·   t('orders.card.invalid_status') defined in no catalog
GOOD:  every shipped locale has every key (fallback to the base only where the product declares it)
       the placeholder spelled the same in every locale   ·   a typed key map: satisfies Record<Status, Key>
```
**Read the code:** For `missing-key`: does the library fall back (`fallbackLng`), and does the product declare that fallback acceptable for this namespace? A fallback to another language is still the wrong language. For `placeholder`: does the library throw on a missing variable or print the raw token? For `used-undefined`: is the key built at runtime under a namespace the script could not see (`addResourceBundle`, a glob loader)? Read the loader once. For each `dynamic-prefix`, run the prefix × union sweep (§ The catalog script). **Finding when** a shipped locale renders a raw key, a raw placeholder or the base language. **Proof:** a missing-key run: the e2e or component suite under each locale with a missing-key handler that throws ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Pseudo-locale and RTL mirror"); for a single key, `i18next.exists(key, { lng })` or the library's equivalent in a unit test, red before the catalog fix.

### 3. Plurals and concatenation

```
BAD:   {count === 1 ? t('order') : t('orders')}   ·   `${n} item${n === 1 ? '' : 's'}`   ·   t('hello') + ' ' + user.name
       `${t('store')} (${t('optional')})`        ·   ar plural with only one/other
GOOD:  t('orders', { count })  with  orders_zero … orders_other  (i18next)  or  {count, plural, …}  (ICU)
       t('greeting', { name })  — one message, the translator orders the words   ·   Intl.ListFormat for joined lists
```
**Read the code:** Does the ternary pick words or a visual state (`count === 0 ? <Empty/> : <List/>` is an empty state, not a plural)? Is the concatenation joining sentence fragments, or two separate UI elements laid out by CSS? Does the target locale's catalog carry every category `Intl.PluralRules(locale).resolvedOptions().pluralCategories` names (Arabic: zero, one, two, few, many, other)? Can the count be 0 on this screen? **Finding when** a shipped locale renders a wrong form or a reordered sentence. **Proof:** the plural matrix: render with n ∈ {0, 1, 2, 3, 11, 100, 101} under `ar`, one assertion per CLDR category; for concatenation, the pseudo-locale `bidi` strategy plus an `ar` screenshot.

### 4. Presentation formatting

```
BAD:   new Date(d).toLocaleDateString()  ·  amount.toLocaleString('en-US')  ·  `$${price.toFixed(2)}`  ·  `${x} USD`
       format(d, 'MM/dd/yyyy') (date-fns, no locale)  ·  new Intl.NumberFormat()
GOOD:  new Intl.DateTimeFormat(locale, opts)  ·  new Intl.NumberFormat(locale, { style: 'currency', currency })
       a project formatDate()/formatMoney() that injects the active locale — read it once; its call sites are then clean
```
**Read the code:** Is the output shown to a user, or sent to an API, a log, a file name or an `<input type="date">` (machine format: not a finding)? Is the hard-coded locale a product decision (a WhatsApp message in one market's format)? Is the currency fixed by the product (single-currency, single-locale)? Does the code run during SSR? Then the server's locale and zone differ from the browser's: cross-link `ssr-audit` §1. **Finding when** a user in a shipped locale sees another locale's format, digits or currency placement. **Proof:** the locale format matrix: the same fixture value under `test.use({ locale: 'ar-SA', timezoneId })` and `en-US`, asserted against `Intl` output for that locale; money across three locales × three currencies including JPY (0 decimals) and KWD (3).

### 5. RTL: physical layout and directional icons

```
BAD:   .title { margin-left: 12px }  ·  style={{ textAlign: 'left' }}  ·  className="ml-4 text-left rounded-l-lg"
       margin: 0 8px 0 0  ·  <ChevronRight />  ·  android:layout_marginLeft  ·  EdgeInsets.only(left: 8)
GOOD:  margin-inline-start  ·  textAlign: 'start'  ·  ms-4 text-start rounded-s-lg  ·  margin-inline-end: 8px
       <ChevronRight className="rtl:rotate-180" />  ·  layout_marginStart  ·  EdgeInsetsDirectional.only(start: 8)
```
**Read the code:** Is the pair symmetric (`left: 0; right: 0`, `mx-`, `left-1/2 -translate-x-1/2` centering)? Is it inside a `[dir]`, `:dir()`, `rtl:` or `ltr:` override — that is the mirroring? Must the content stay LTR (code, phone numbers, charts, maps, media timelines)? Is the property vertical (`top`, `mt-`, `h-`)? On React Native, `marginLeft` auto-swaps under RTL by default, so it is low at most; transforms, `textAlign: 'left'` and icons do not swap. On Tailwind v3, `space-x-*` emits physical margins; check the major before reporting it. Is the icon directional (back, forward, next), or one that must not mirror (play, clock, check, a two-way swap)? **Finding when** the RTL render puts the element on the wrong side. **Proof:** the RTL mirror: switch to the RTL locale through the app's own switcher, assert `html[dir="rtl"]`, and compare bounding boxes with the LTR render: the x-order of the pair inverts (V112).

### 6. Text expansion

```
BAD:   <Button className="w-[110px]">{t('save')}</Button>   ·   <span className="truncate">{t('roles.auditor')}</span>
GOOD:  min-w-* with padding  ·  truncation with the full value in a title or tooltip  ·  wrapping allowed
```
**Read the code:** Does the element hold translated text, or a number or a code? Is the truncation intentional, with the full value reachable? **Finding when** a translated label clips at the product's smallest viewport. **Proof:** the pseudo-locale `accented` strategy (about +35–40 % length) at 320 px: no labelled element has `scrollWidth > clientWidth + 1` under hidden overflow (V111). A brand mark or a code-like value that clips only there is not a finding (`precedents/ui.md` § 47).

### 7. `<html lang>` and `dir`

```
BAD:   <html lang="en"> in index.html of a bilingual app, never updated   ·   an RTL locale declared and no dir binding anywhere
GOOD:  document.documentElement.lang = lang; document.documentElement.dir = dir on every switch   ·   <html lang={locale} dir={dir}>
```
**Read the code:** Does the static `index.html` value match the default locale, and does a switch update both attributes (7b)? Is the SPA switch covered as well as the first load? A per-subtree `lang` or `dir` on a quote or a code block is correct. **Finding when** the active locale and the document attributes disagree after load or after a switch. **Proof:** the locale switch: switch through the app's own control; `expect(page.locator('html')).toHaveAttribute('lang', /^ar/)` and `dir="rtl"`, on first load and after a client-side switch.

### 8. Collation and casing

```
BAD:   cities.sort((a, b) => a.localeCompare(b))   ·   rows.sort((a, b) => a.name > b.name ? 1 : -1)   ·   name.toLowerCase() === q
GOOD:  new Intl.Collator(locale).compare  ·  a.localeCompare(b, locale)  ·  toLocaleLowerCase(locale) on user text
```
**Read the code:** Is the sorted value display text (names, cities, product titles), or an id, an enum code, an ISO date (sorting those by code unit is correct)? Is the case-folded value user text or an ASCII protocol token (an HTTP header, a file extension, a status code)? **Finding when** a list users scan by name orders wrongly in a shipped locale, or a Turkish dotted/dotless `i` breaks a match. **Proof:** a unit test: `['Ä', 'Z', 'A']` sorted under `de` and `sv` compared with `new Intl.Collator(locale).compare`; for Arabic, a list with and without diacritics.

### 9. Native catalogs

```
BAD:   res/values-ar/strings.xml lacks a key of res/values/strings.xml   ·   a plurals entry with only one/other for ar
       an .xcstrings entry `needs_review` or `new` for a shipped language   ·   app_ar.arb missing a message of app_en.arb
GOOD:  every shipped locale complete; translatable="false" or shouldTranslate: false on what must not be translated
```
**Read the code:** Is the language listed as shipped (Android `localeConfig` / `resConfigs`, Xcode `knownRegions`, Flutter `supportedLocales`)? Is the entry marked non-translatable? **Finding when** a shipped language falls back to the source for a string a user sees. **Proof:** the catalog script row is the static fact; Android Lint `MissingTranslation` / `MissingQuantity` at error level, or a Flutter build whose untranslated-messages report is empty, is the gate.

### 10. Raw server or exception text

```
BAD:   <p>{err.message}</p>   ·   toast.error(error.message || t('saveFailed'))   ·   {{ error.message }}
GOOD:  t(`errors.${code}`, { defaultValue: t('errors.generic') }) with the code list enumerated from the API contract
```
**Read the code:** Start with the helpers 10b lists: a `notifyError(error, fallback)` that shows `apiErrorMessage(error)` — the server's `message` when there is one — is one root cause with every call site behind it. Does the API localize its messages by `Accept-Language`, and does the client send it? Then the text is already in the user's language: read one handler to confirm, and the row is Hardening. Is the message a code the client maps? **Finding when** a localized UI shows server or runtime text in another language. **Proof:** the server-text sentinel: `page.route` answers 4xx/5xx with the message `ZZ_SERVER_TEXT`; under `ar` the sentinel must not be visible.

### 11. Bidi isolation

```
BAD:   <span>{t('by')} {user.name} (2)</span>   ·   t('revokeDesc', { name: user.username }) shown in an Arabic sentence
GOOD:  <bdi>{user.name}</bdi>  ·  <span dir="auto">{comment}</span>  ·  unicode-bidi: isolate on the interpolation's element
```
**Read the code:** Does user-supplied or API-supplied text sit inside a sentence or beside numbers and punctuation in another direction? Does the library isolate interpolations already? ICU MessageFormat and `Intl` do not by default. **Finding when** the mixed-direction render reorders the punctuation or digits. **Proof:** the bidi isolation fixture: render the user name `"Ali (CEO) 2"` inside the Arabic sentence; assert the visual order of the parenthesis and digit with `Range.getClientRects()` or a screenshot.

## Proof

The oracle per class, failing first and green after the fix ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states):

1. **Pseudo-locale walk** (§1, §3 concatenation, §6) — § "Pseudo-locale and RTL mirror", V111 and V132. Wrap every catalog **value** with `pseudoLocalizeString(v, { strategy: 'accented' | 'bidi' })` (pseudo-localization 3.1.3), skipping ICU placeholders and tags. Never `PseudoLocalizeDom.start()`: it rewrites hard-coded text too, so it cannot tell the two apart. Walk the visible text nodes and `[alt], [title], [placeholder], [aria-label]` values: a node with two or more Latin letters and no pseudo marks is hard-coded unless it is seeded data.
2. **RTL mirror** (§5, §7) — same section, V112 and V136.
3. **Missing-key run** (§2, §9) — the suite under every shipped locale with `missingKeyHandler` (i18next), `missingWarn`/`fallbackWarn` (vue-i18n) or the compile step (formatjs, Angular) turned into a failure — *Missing-key run* under `### i18n oracles`, V133.
4. **Plural matrix** (§3, V134), **locale format matrix** (§4, V135), **locale switch** (§7, V137), **collation order** (§8, V138), **server-text sentinel** (§10, V139), **bidi isolation** (§11, V140) — `### i18n oracles` in the same section; the per-§ shape above names the fixture.

A static fact needs no runtime oracle only when the source is the whole claim: a key absent from a shipped locale's catalog, a placeholder spelled differently, `<html lang="en">` never updated on a bilingual shell. Every other class needs its oracle to fire. Without a harness the candidate is Unconfirmed with the test written out.

## Output

```
i18n-scan — gate ON: ar, en (ar RTL, default ar); i18next 26.4 + react-i18next 17.0 (apps/web/package.json);
lint lane: blocked (eslint-plugin-i18next not installed) — §1 is rg + pseudo-locale only; catalogs: 518 JSON in 259 sets

Findings: 2 · Unconfirmed: 3

1. src/features/integrations/components/CredentialsDialog.tsx:100                  [report-with-fix]   high
   §1 hard-coded label — <Label>Client ID</Label> and <Label>Client Secret</Label> on /settings/integrations,
   an Arabic-default route. Proof: pseudo-locale walk — both labels render with no pseudo marks (fails).
   Fix: t('integrations.clientId') / t('integrations.clientSecret'); keys added to ar and en.
2. src/shared/i18n/locales/{L}.json :: common.bulkActionBar.selected               [report-with-fix]   high
   §3 plural category missing — ar has one, two, few, many, other; Intl.PluralRules('ar') also needs zero, and the
   bar renders at count 0 after a deselect-all. Proof: plural matrix n=0 under ar renders the raw key (fails).
   Fix: add selected_zero to ar.
3. src/features/delivery/model/use-delivery-settings.ts:121                          [report-flagged]    high
   §10 server text — toast.error(error.message || t('settings.saveFailed')). Unproven: whether the API localizes by
   Accept-Language. Settling probe: 500 with ZZ_SERVER_TEXT under ar; the sentinel must not show.

Verification: 41 candidates → 2 findings · 3 unconfirmed · 9 hardening · 27 refuted

Class coverage:
  §1  hard-coded copy          checked (rg only; lint blocked) (162 hits / 38 groups → 1 finding; 52 in an LTR docs wrapper refuted by one read) · Live, unreviewed (24 groups / 61 hits — continue with grep 1a on src/features/finance)
  §2  catalog defects          checked (script: 0 missing, 0 placeholder; 336 dynamic prefixes → top 30 swept, 0 missing (dynamic)) · Live, unreviewed (306 prefixes — continue with the prefix × union sweep)
  §3  plurals / concatenation  checked (32 hits + 4 script rows → 1 finding, 1 unconfirmed)
  §4  formatting               checked (11 hits → 0 findings; 9 machine or value-only toFixed)
  §5  RTL layout               checked (5 hits → 0 findings; 1 centering, 2 print-only)
  §6  expansion                blocked (no harness for the pseudo-locale render) (40 hits)
  §7  lang / dir               checked (static lang="ar" matches the default; dir and lang synced on switch)
  §8  collation                checked (23 hits → 1 unconfirmed: city names sorted with no locale)
  §9  native catalogs          N/A (no Android, iOS or Flutter catalogs)
  §10 server text              checked (9 hits / 1 group → 1 unconfirmed)
  §11 bidi isolation           checked (40 hits → 0 findings, 4 hardening)
```

`[report-with-fix]`: the site renders on a cited route in a shipped locale, the oracle failed, and the fix is a local change in the project's i18n library. `[report-flagged]`: one link is unproven (no harness, a loader not read, a server contract not checked), and the row names that link and the settling test. The coverage block lists **all eleven** classes on every run: `checked (k hits → m findings)` only when the greps or the script ran; `N/A (<reason>)` when the gate or the stack has no such surface; `blocked (<reason>)` when a grep, the lint lane or the render failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (§ 47–48 and i18n § 76–83 for this skill) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this skill meets most:

- **A single-locale product with no i18n library**: every row `N/A`, unless the brief names a second market (§ 76).
- **Not copy:** text in `<code>`, `<pre>`, `<kbd>` and the project's code or LTR wrappers; `<Trans>`-family children; Angular `i18n`-marked elements; `alt=""` on a decorative image; brand, product and standard names on a documented allow-list; units and symbols; data (user content, API values, SKUs); example-format placeholders (`john@example.com`, `https://…`, `01xxxxxxxxx`); developer text (`console.*`, logger calls, `throw new Error` that never renders); routes the product declares single-language (§ 77).
- **Machine formats:** `toISOString()`, `YYYY-MM-DD` built for an input or an API, `toFixed` on a non-money value, sorting ids, enum codes or ISO dates, `toLowerCase()` on ASCII protocol tokens (§ 78).
- **A project wrapper owns the locale:** a `formatDate()`, `formatMoney()` or `Trans` wrapper that injects the active locale. Read it once; its call sites are clean (§ 79).
- **RTL:** symmetric pairs; `[dir]`, `:dir()`, `rtl:` and `ltr:` overrides (`precedents/ui.md` § 48); content that must stay LTR (code, phone numbers, charts, maps, media timelines); vertical properties; React Native `marginLeft` under the default auto-swap; icons that must not mirror (play, clock, check, two-way swap) (§ 80, 83).
- **A server that localizes** its messages by `Accept-Language`, with the client sending the header: §10 is Hardening (§ 81).
- **SwiftUI `Text("literal")`** is a `LocalizedStringKey`; only `Text(verbatim:)` and `Text(stringVariable)` are hard-coded (§ 82).
- **Pseudo-locale-only clipping** of a brand mark or a code-like value (`precedents/ui.md` § 47).
- **A word-order slot:** an empty value in one locale whose siblings form one sentence (`heroTitleA` / `heroTitleMid` / `heroTitleB`) — `untranslated-slot` (`precedents/ui.md` § 106).
- **A display token:** a value that is one placeholder token in every locale, or a key read with `skipInterpolation` — `placeholder-token` (`precedents/ui.md` § 107).

## When to run

- On a diff that adds or changes user-visible text, a catalog, a format call, a sort over display text, a style with a horizontal property, an icon, or the document shell: the `/frontend-audit` dispatch signal when that command is present.
- On every whole-repo `/frontend-audit` and `/i18n-audit` (its preset), reporting all eleven classes.
- When a translator delivers a locale, before a new locale is promoted, and when a second market is first named in a brief (the gate turns ON).

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/frontend-audit` or `/i18n-audit` that happens in their verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the site `<file:line>` (or set, key and locale), the route or screen that renders it, the oracle, and the fix in the project's library.
- Do not mark a finding `[report-with-fix]` without an oracle that failed first; a static-fact row needs its two-ended trace.
- Do not print the gate as OFF while 0a or 0c returned an i18n layer, and do not print "no i18n defects" without the class-coverage block. A class whose grep, script or render did not run is `blocked`, never `checked`.
- Do not propose a fix that hides the symptom: a machine translation shipped as copy (copy the base value with a `TODO: translate` marker instead), a plural collapsed to `one`/`other` for a locale that needs more, an `eslint-disable` line, `dir="ltr"` forced on a whole screen, a key deleted because a grep found no literal use while a dynamic prefix covers it.
- Do not use `rg -L` for files-without-match; it is `--follow`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `@i18n-auditor` (this pack) — the lens over this skill: judges its rows, ranks them and runs the catalog script on a diff. `/i18n-audit` — the preset of `/frontend-audit --classes=i18n` that dispatches this skill.
- `ssr-audit` (this pack) — locale-dependent hydration and per-request language on the server. `a11y-code-scan` and `a11y-scan` (this pack) — `lang` as accessibility. `client-data-scan` §6 (this pack) — the locale in a cache key. `seo-audit` and `@technical-seo` (this pack) — `hreflang`.
- code-quality `correctness-smell-scan` §6 (when installed) — clock and zone arithmetic. Security `data-exposure-scan` §1 (when installed) — the leak in raw server text.
- `visual-check` (this pack) — the RTL row of the visual matrix. ui-ux `rtl.md` (when installed) — the RTL vocabulary.
- `rules/i18n.md` — how many locales the code assumes; `ai/patterns/i18n.md` — key architecture, ICU plurals, `Intl` formatting and namespace loading, the shapes the fixes take.
