---
name: design-token-audit
description: "Design-system drift detector: raw colour, spacing, type and z-index literals, Tailwind arbitrary values, re-built or deprecated DS components, per token-source lane, proved by computed-style conformance."
kind: skill
pack: ui-ux
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: design-token-audit

## Premise

Hardcoded design values are how design systems silently die: one `#3b82f6` here, one `padding: 13px` there, three different button styles within a year. Each literal is invisible on the day it lands. It stays the same colour when the theme flips to dark, when the brand changes, when the token it should have named is retuned for contrast. This skill finds them across every way a project declares tokens — Tailwind 4 `@theme`, a v3 config, CSS custom properties, DTCG JSON, a CSS-in-JS theme, a native theme — and the components that rebuild what the design system already exports.

**This skill DETECTS; it does not apply.** It produces the finding set `ui-design-sweep`'s verbs 1–2 close: `consolidate-tokens` when a token exists, `extract-token` when none does. This skill owns *resolution*: which token is right, and is the swap safe? The verb owns the edit and its visual verify. A run that starts editing components is out of contract.

**Existing tokens are the truth. Mirror; never invent.** Every "literal → token" proposal names a token from the project's resolved catalog (§ Adapt to the codebase), with its definition `<file:line>`. When no token matches, the finding is "designer decision required: the closest existing token, or a new token through the design-system process". Inventing `text-accent-orange` because it would have been nice is the failure this skill exists to prevent.

**Every finding cites the literal's `<file:line>` + the token it should be (definition `<file:line>`) or `no token` + the route that renders it + the proof + the fix.** A grep hit is never a finding by itself. "No drift found" is never printed without the class-coverage block (§ Output).

Below, `ui § n` means [`precedents/ui.md`](../../../../snippets/precedents/ui.md) § n; a bare `§n` is a detector in this skill. §1–§10 are the research classes D-01…D-10, in order.

## The rule

A candidate is a finding when all four hold:

1. **A catalog exists.** The project declares the token set this value bypasses (or exports the component this markup rebuilds). With no catalog, §1–§5 and §8–§10 are `[report-flagged] (no token catalog — extract-token)`, never Findings.
2. **It renders.** A route, screen or layout reaches the file. Scripts, mocks, seeds, Storybook-only and design-system-internal files fail here.
3. **It is not a definition or an exempt context** (§ False positives): token files, `@theme`, DTCG JSON, the DS's own primitives, SVG illustrations, email and print templates, third-party overrides, `var(--…)` through arbitrary syntax, layout `calc()`, dynamic geometry, CSS-variable injection.
4. **The proof holds.** A literal on a rendered path with its token named is a static fact (`precedents/ui.md`, the proof rule): the two-ended trace passes. Rendered drift at scale, a themed miss, and every §6 behavioural claim need their oracle (§ Proof).

## Boundaries

- **Contrast as a WCAG failure** (1.4.3, 1.4.11) is `a11y-scan` §3 (frontend pack, when installed). This skill computes a token **pair's** ratio only to decide whether a swap is safe (§ The swap trap). Without the frontend pack, a pair below its ratio is reported here, tagged `owner: a11y-scan (frontend pack not installed)`.
- **Motion durations and easing** → `motion-audit` (this pack). **Chart data ramps** and series colour → `chart-encoding-audit` (this pack). **Dark-mode parity of a whole theme** → `@theme-specialist` (this pack).
- **The fix, by remedy.** A literal whose value **equals** an existing token (`scripts/token-map.py` class `EXACT` with `eq=yes`, § The swap trap) is a documented token applied in place → `/align`, which closes it as an EQ row (`_orchestration-sync.md` § Command boundary table: snapping to a token that already exists is `/align`'s). A nearest-only or cross-family literal, or a value no token holds → verb 2 `extract-token` or a designer decision, through `/polish` or `/enhance-ui`. Every instance of one surface type behind one wrapper (§6 at scale) → `/unify-surfaces`. A deprecated export (§7) whose replacement is a version bump → `/upgrade-dep`. This skill names the route; it never edits.
- **Raw primitive at build time** (a feature PR writing `<button>` beside the DS `Button`) is also caught by the delivery lane's sibling-shape halt when the delivery pack is installed; this skill is the sweep.
- **Native token sources** (Flutter `ThemeData`, Compose `MaterialTheme`, SwiftUI asset catalogs) run grep-only here; the platform fix belongs to the mobile pack's references when it is installed.

## Adapt to the codebase — the token-source lanes

Resolve the catalog **once**, before any grep is judged: the token set, the semantic layer, the DS component export set, and the `@deprecated` exports. Print the lanes found, with versions read from the lockfile, in the output header. More than one live source for the same axis is itself a finding (drift between sources); pick the one the DS docs name.

| Lane | Where tokens live (grep 0b/0c) | How feature code consumes them | Literal that bypasses them |
|---|---|---|---|
| **Tailwind 4** | `@theme { --color-*: …; --spacing: …; }` and `@theme inline { … }` in CSS; runtime values in `:root` / `.dark` / `[data-theme]` | utilities derived from the namespace (`--color-brand` → `bg-brand`; `p-4` = 4 × `--spacing`) | `bg-[#1e40af]`, `p-[13px]`, `text-[14px]`; default-palette `text-blue-500` when the theme is semantic |
| **Tailwind 3** | `tailwind.config.*` `theme` / `theme.extend` | utilities | the same arbitrary values; a literal in the config's consumers |
| **CSS custom properties** | `:root { --x: … }`, theme blocks, a tokens partial | `var(--x)` | hex / `rgb()` / `oklch()` / px in rules |
| **SCSS / Less variables** | a `_tokens.scss` / `variables.less` partial | `$x` / `@x` | a literal, or a `$local: #…` defined outside the partial |
| **DTCG 2025.10 / Style Dictionary** | `*.tokens.json` with `$value` / `$type`; the Style Dictionary build output | the generated CSS / JS | as the output's lane |
| **CSS-in-JS** (styled-components, Emotion, vanilla-extract, Panda, UnoCSS) | a `ThemeProvider` theme object; `createTheme` / `createGlobalTheme`; `defineTokens` / `defineSemanticTokens`; a `theme` key in the config | `${p => p.theme.x}`, `vars.x`, token utilities | literals in template literals and style objects |
| **Component-library theme** (MUI, Chakra, Mantine, Vuetify, PrimeVue, Angular Material) | `createTheme`, `createSystem`, `extendTheme`, the library's theme file | `sx` / style props with theme keys | `sx={{ color: '#…' }}`; raw-scale access (`theme.palette.blue[500]`) where a semantic role exists |
| **React Native / NativeWind** | a `theme.ts`; NativeWind's Tailwind config | `StyleSheet` reading the theme; utilities | `StyleSheet.create({ color: '#…' })` |
| **Flutter · Compose · SwiftUI** | `ThemeData` / `ColorScheme`; `MaterialTheme(colorScheme = …)`; `*.xcassets` colour sets | `Theme.of(context)`, `MaterialTheme.colorScheme`, `Color("name")` | `Color(0xFF…)`, `Color.fromARGB`, `Color(red:…)` outside the theme files |

**The design-system component set.** The DS root is the directory the DS docs name (`components/ui`, `shared/ui`, `packages/ui/src`, `design-system`); grep 0d lists candidates. Its file names are the export set (`button.tsx` → `Button`). A shadcn-style project's DS root is `components/ui`; its primitives wrap Radix, and the native elements inside them are the DS, not drift.

## Lint lanes

Where the project already runs a rule, use its config and keep only these rule ids; where it does not, run them from a scratch directory with the project's files as input, never committing the config. A lane that cannot install prints `blocked (<reason>)` for its column; the greps still run. **Cite only a tool this repo installs or this run installed in scratch** — a halt cleared by a plugin absent from both is a fabricated pass.

| Rule (version read 2026-10-05) | Classes |
|---|---|
| stylelint 17.16.0 core `color-no-hex`, `function-disallowed-list` (`rgb`, `rgba`, `hsl`, `hsla`, `oklch`), `declaration-no-important` | §1, §5 |
| `scale-unlimited/declaration-strict-value` 1.12.1 (peer stylelint ≥ 16 ≤ 17) on `/color$/`, `fill`, `stroke`, `z-index`, `font-size`, spacing and radius properties, `ignoreValues: currentColor, transparent, inherit, initial, unset` | §1, §4, §10 |
| `eslint-plugin-tailwindcss` 4.4.0 `no-arbitrary-value`; `eslint-plugin-better-tailwindcss` 4.8.0 `no-unknown-classes` (closed theme), `no-restricted-classes`, `no-deprecated-classes` | §2, §5, §7, §8 |
| `vue/no-static-inline-styles`; `@angular-eslint/template/no-inline-styles` | §3 |
| `@typescript-eslint/no-deprecated` 8.71.0 — typed lint, needs `parserOptions.projectService`; flags uses of `@deprecated`-tagged exports | §7 |
| `@ast-grep/cli` 0.45.3 — one rule per (native element, DS export) pair (grep 6 builds them) | §6 |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`"${ROOTS[@]}"`): given none, rg reads stdin under an agent's shell and reports a silent zero. Any rg error (exit 2) is a failed grep, never zero hits. A pattern that begins with `-` goes behind `-e`, or rg reads it as a flag.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|lit|react-native)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,coverage,storybook-static,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,__fixtures__,playwright,cypress,scripts,tools}/**' -g '!**/*.{test,spec,stories,story,e2e,cy,mock}.*' -g '!**/*.{test-data,fixture,fixtures}.*'
   -g '!*.{md,mdx,snap,map,lock,json,yml,yaml,svg}' -g '!**/{locales,locale,i18n,translations,docs,illustrations,emails,email,vendor}/**' -g '!/ai/**' -g '!**/*.min.*')
S=(-g '*.{css,scss,sass,less,pcss,styl}'); M=(-g '*.{jsx,tsx,vue,svelte,astro,html}'); K=(-g '*.{jsx,tsx,js,ts,vue,svelte,astro,html}')
U=(-g '*.{css,scss,sass,less,pcss,js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--)')   # drops comment-only lines
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'                                  # JSX-aware tag body
# 0a lanes and versions. 0b CSS token sources (handled per line by the §1 lookbehinds). 0c whole-file token sources
#    (JS/TS/JSON — dropped from every literal grep). 0d the DS root(s). 0e is the theme semantic (gates §8)?
rg -n --no-heading --pcre2 '"(?:tailwindcss|@tailwindcss/(?:vite|postcss)|style-dictionary|styled-components|@emotion/react|@vanilla-extract/css|@pandacss/dev|unocss|@mui/material|@chakra-ui/react|@mantine/core|vuetify|primevue|nativewind|stylelint|stylelint-declaration-strict-value|eslint-plugin-better-tailwindcss|eslint-plugin-tailwindcss|typescript-eslint|@ast-grep/cli)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --no-heading --pcre2 '^\s*@theme\b|^\s*:root\s*(?:,[^{]*)?\{|^\s*(?:\.dark|html\.dark|\[data-theme[^\]]*\])\s*[,{]' "${S[@]}" "${X[@]}" "${ROOTS[@]}"
TOKF=( $( { rg --files -g '**/tailwind.config.*' -g '**/*.tokens.json' -g '**/{tokens,design-tokens}.json' -g '!**/node_modules/**' "${ROOTS[@]}"
  rg -l --pcre2 '"\$value"\s*:' -g '*.json' -g '!**/node_modules/**' "${ROOTS[@]}"
  rg -l --pcre2 '\b(?:createTheme|createGlobalTheme|createThemeContract|defineTokens|defineSemanticTokens|createSystem|extendTheme)\s*\(' -g '*.{js,ts,mjs,tsx}' "${X[@]}" "${ROOTS[@]}"; } | sort -u ) ); printf 'token file: %s\n' "${TOKF[@]}"
TF=(-e '^$^'); for f in "${TOKF[@]}"; do TF+=(-e "^${f}:"); done; DROP=(grep -v "${TF[@]}")
DSR=( $(rg --files "${X[@]}" "${ROOTS[@]}" | rg --pcre2 -o '^.*?/(?:components/ui|shared/ui|ui-kit|design-system|packages/ui/src)(?=/)' | sort -u) ); printf 'DS root: %s\n' "${DSR[@]}"
rg -l --pcre2 -e '--color-(?:primary|secondary|accent|brand|surface|muted|destructive|success|danger|warning|info|foreground|background)\b|^\s*--(?:primary|brand|surface|destructive|accent)\s*:' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l
# 1. Colour literal outside a token definition (D-01). The two `--` lookbehinds need PCRE2 >= 10.43 (rg 15.2.0 ships 10.45);
#    older builds run the fallback, which drops them and filters custom-property lines after. 1b: native colour constructors.
P1='(?<!--[\w-]{1,60}:\s{0,3})(?<!--[\w-]{1,60}:\s{0,3}[^;{}]{1,80})(?<!href=["\x27])(?<!to=["\x27])(?<![&\w])(?:#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])(?!\s*\{)|(?<![\w-])(?:rgba?|hsla?|oklch|oklab|hwb)\((?!\s*(?:var\(|from\s+var\()))'
if rg --pcre2-version | awk 'NR==1{split($2,v,".");exit !(v[1]>10||(v[1]==10&&v[2]>=43))}'; then rg -n --pcre2 "$P1" "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}"
else rg -n --pcre2 "${P1#*\{1,80\})}" "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}" | rg -v --pcre2 '^[^:]+:\d+:.*--[\w-]+\s*:\s*[^;]*(?:#|rgb|hsl|okl|hwb)'; fi
rg -n --pcre2 '\bColor\(\s*0x[0-9A-Fa-f]{6,8}\s*\)|\bColor\.from(?:ARGB|RGBO)\(|\b(?:UI|NS)?Color\(\s*red\s*:|\bColor\(\s*red\s*=' -g '*.{dart,kt,swift}' "${X[@]}" -g '!**/{theme,themes}/**' -g '!**/*{Theme,Colors,Tokens}*.{dart,kt,swift}' "${ROOTS[@]}" | "${NC[@]}"
# 2. Tailwind arbitrary value on a token axis (D-02): colour, spacing, type, radius, shadow, z. Layout sizes (w/h/min/max/inset)
#    and `var(` / `calc(` / `theme(` / `--` bodies are not this class.
rg -n --pcre2 '(?<![\w-])(?:[\w-]+:)*!?-?(?:bg|text|border(?:-[xytrblse])?|ring|ring-offset|fill|stroke|from|via|to|shadow|outline|decoration|accent|caret|divide|placeholder|p[xytrblse]?|m[xytrblse]?|gap(?:-[xy])?|space-[xy]|rounded(?:-[a-z]+)?|z|leading|tracking|font)-\[(?!var\(|calc\(|theme\(|--)(?:#|rgba?\(|hsla?\(|oklch\(|-?\d)' "${K[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}"
# 3. Inline style literal (D-03): React style objects, Vue :style and static style, Angular [style.x] / [ngStyle]. 0 and % skipped.
rg -n --pcre2 'style=\{\{[^}]*\b(?:color|background\w*|border\w*Color|margin\w*|padding\w*|fontSize|fontWeight|lineHeight|letterSpacing|gap|borderRadius|boxShadow|zIndex)\s*:\s*["\x27\x60]?(?:#|-?(?!0(?![.\d]))(?!\d+(?:\.\d+)?%)\d|rgb|hsl|oklch)|:style="\{[^"]*\b(?:color|background\w*|margin\w*|padding\w*|fontSize|fontWeight|lineHeight|gap|borderRadius|boxShadow|zIndex)\s*:\s*\x27?(?:#|-?(?!0(?![.\d]))(?!\d+(?:\.\d+)?%)\d|rgb|hsl)|(?<![:\w.-])style="[^"]*\b(?:color|background(?:-color)?|border(?:-\w+)?-color|margin(?:-\w+)?|padding(?:-\w+)?|font-size|font-weight|line-height|gap|border-radius|box-shadow|z-index)\s*:\s*(?:#|-?(?!0(?![.\d]))(?!\d+(?:\.\d+)?%)\d|rgb|hsl)|\[style\.(?:color|background(?:-color)?|margin[\w-]*|padding[\w-]*|font-size|z-index)(?:\.px)?\]="[^"]*(?:#|\d)|\[ngStyle\]="\{[^"]*\x27(?:color|background[\w-]*|margin[\w.-]*|padding[\w.-]*|font-size[\w.-]*|z-index)\x27\s*:\s*\x27?(?:#|\d|rgb)' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. z-index magic numbers (D-04): two or more digits, any syntax.
rg -n --pcre2 '(?<![\w-])z-index\s*:\s*-?\d{2,}|\bzIndex\s*:\s*-?\d{2,}|(?<![\w-])-?z-\[-?\d+\]' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}"
# 5. !important and the Tailwind important modifier (D-05): v3 prefix `!mt-2`, v4 suffix `mt-2!`. Only inside a class
#    string: a bound `:class="{ a: !b }"` or `className={!open && …}` is JS, where `!` is negation.
rg -n --pcre2 '!important\b|(?:(?<![:\w.-])class(?:Name)?=\{?["\x27\x60][^"\x27\x60]*?(?<![\w-]))![a-z][\w:-]*|(?:(?<![:\w.-])class(?:Name)?=\{?["\x27\x60][^"\x27\x60]*?)[a-z0-9\]]!(?=[\s"\x27\x60])' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6. A native element styled outside the DS root, in a file that does not import the DS equivalent (D-06; rg fallback —
#    the ast-grep lane below is primary). Per app root: a root is paired only with the DS roots inside it or in a
#    workspace package its package.json names (owner = longest ROOTS prefix), and a pair runs only when that DS exports it.
own() { printf '%s\n' "${ROOTS[@]}" | awk -v d="$1/" 'index(d, $0 "/")==1 {print length($0) "\t" $0}' | sort -n | tail -1 | cut -f2; }
for root in "${ROOTS[@]}"; do RDIR=(); for d in "${DSR[@]}"; do o=$(own "$d"); nm=$(rg -o -m1 --pcre2 '"name"\s*:\s*"\K[^"]+' "$o/package.json" | head -1)
  { [ "$o" = "$root" ] || { [ -n "$nm" ] && rg -q -F "\"$nm\"" "$root/package.json"; }; } && RDIR+=("$d"); done; [ ${#RDIR[@]} -eq 0 ] && continue
  NEST=( $(printf '%s\n' "${ROOTS[@]}" | awk -v r="$root" '$0!=r && index($0, r "/")==1 {sub(/^\.\//, ""); print "-g\n!" $0 "/**"}') )
  for pair in 'button:Button:<button\b(?='"$TB"'\bclass(?:Name)?\s*=)' 'dialog:Dialog:<(?:div|section)\b(?='"$TB"'(?:\brole=["\x27](?:dialog|alertdialog)["\x27]|\baria-modal\s*=|\bfixed inset-0\b))' 'select:Select:<select\b' 'checkbox:Checkbox:<input\b(?='"$TB"'\btype=["\x27]checkbox["\x27])' 'tabs:Tabs:\brole=["\x27]tablist["\x27]'; do
    f=${pair%%:*}; r=${pair#*:}; n=${r%%:*}; p=${r#*:}
    rg --files "${RDIR[@]}" | rg -q -i "/${f}s?\.(?:tsx|jsx|vue|svelte)$" || continue
    rg -l0 -U --pcre2 "$p" "${M[@]}" "${X[@]}" $(printf -- "-g !%s/** " "${RDIR[@]#./}") "${NEST[@]}" "$root" | xargs -0 -r rg --files-without-match -U --pcre2 "import\s*(?:type\s+)?\{[^}]*\b${n}\b[^}]*\}|import\s+${n}\b" | sed "s/^/§6 ${f} → ${n}: /"
  done; done
# 7. Deprecated DS exports: the names (read), then their consumers (the typed lint lane is primary).
[ ${#DSR[@]} -gt 0 ] && rg -n -U --pcre2 -o '@deprecated\b[^\n]*\n(?:\s*\*[^\n]*\n)*?\s*\*/\s*\n\s*export\s+(?:declare\s+)?(?:const|function|class|let|type|interface)\s+(\w+)' -r '$1' "${DSR[@]}"
# 8. Default-palette utility on a semantic theme (D-08) — only when 0e > 0.
rg -n --pcre2 '(?<![\w-])(?:[\w-]+:)*!?(?:bg|text|border(?:-[xytrblse])?|ring|ring-offset|fill|stroke|from|via|to|outline|decoration|divide|placeholder|accent|caret|shadow)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(?:50|[1-9]00|950)\b' "${K[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}"
# 8b. Primitive tier used where a semantic tier aliases it (AL-08). 8p counts declared palette ramps; 0 → 8b is N/A.
#     Definitions (`--color-primary: var(--blue-500)`) are the semantic layer itself and are dropped by the last filter.
PRIM='(?:slate|gray|grey|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose|brand)-(?:50|[1-9]00|950)'
echo "8p primitive ramps: $(rg -c --pcre2 -e "^\s*--(?:color-)?${PRIM}\s*:" "${S[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF}END{print s+0}')"
rg -n --pcre2 -e "var\(\s*--(?:color-)?${PRIM}\s*[,)]|(?<![\w-])(?:[\w-]+:)*!?(?:bg|text|border(?:-[xytrblse])?|ring|fill|stroke|outline|from|via|to|decoration|shadow)-\(--(?:color-)?${PRIM}\)" "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}" | rg -v --pcre2 '^[^:]+:\d+:\s*--[\w-]+\s*:'
# 9. Declared CSS tokens no `var()`, no v4 `(--x)` shorthand and no Tailwind 4 utility references (D-09). Candidates, read
#    before reporting. NS lists the v4 theme namespaces a utility reads: `--z-index-chrome` is `z-chrome`.
T="${TMPDIR:-/tmp}"; NS='color|font|text|font-weight|tracking|leading|breakpoint|container|spacing|radius|shadow|inset-shadow|drop-shadow|blur|perspective|aspect|ease|animate|z-index|transition-duration|default-transition-duration|animation-duration'
rg -o -N --no-filename --pcre2 '^\s*\K--[\w-]+(?=\s*:)' "${S[@]}" -g '!**/node_modules/**' "${ROOTS[@]}" | sort -u > "$T/dta-decl"
rg -o -N --no-filename --pcre2 '\(\s*\K--[\w-]+' "${U[@]}" -g '!**/node_modules/**' "${ROOTS[@]}" | sort -u | comm -23 "$T/dta-decl" - > "$T/dta-unref"
sed -nE "s/^--($NS)-(.+)$/\2/p" "$T/dta-unref" | sort -u | sed 's/.*/(?<=[-:])&(?![\\w-])/' > "$T/dta-ns"
[ -s "$T/dta-ns" ] && rg -o -N --no-filename --pcre2 -f "$T/dta-ns" "${K[@]}" -g '*.css' -g '!**/node_modules/**' "${ROOTS[@]}" | sort -u > "$T/dta-nsused" || : > "$T/dta-nsused"
grep -v -E -x -e "--($NS)-($(paste -sd'|' "$T/dta-nsused"))" "$T/dta-unref"
# 10. Off-scale spacing, type, radius or shadow literal in stylesheets and CSS-in-JS (D-10). 0, 1px, var()/calc()/clamp() skipped.
rg -n --pcre2 '(?<![\w-])(?:(?:margin|padding|inset)(?:-(?:top|right|bottom|left|inline|block)(?:-(?:start|end))?)?|gap|row-gap|column-gap|font-size|line-height|letter-spacing|border(?:-(?:top|bottom)-(?:left|right))?-radius)\s*:\s*(?![^;{}]*(?:var|calc|clamp|min|max|env|theme)\()[^;{},]*?(?<![\w.#-])(?!0(?:\.0+)?(?:px|rem|em)?\b)(?!1px\b)\d+(?:\.\d+)?(?:px|rem|em)\b|(?<![\w-])box-shadow\s*:\s*(?!\s*(?:none|var\(|inherit|initial|unset))[^;{}]*\d+px' "${S[@]}" -g '*.{vue,svelte,astro,js,jsx,ts,tsx}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DROP[@]}"
```

**The ast-grep lane (§6, primary for TSX).** One rule per pair the DS exports, generated from grep 0d; the `not` block keeps a file that imports the DS component. It is structural, so it sees multi-line JSX the rg fallback reads line by line. Run it with the installed `ast-grep` binary — the audit never downloads it; absent, the lane prints NOT-RUN and grep 6 is the lane (the `sg` alias prints a deprecation warning in 0.45.3), excluding the DS root. In a monorepo, scan each app root only with the rules of the DS roots grep 6 paired it with (`RDIR`), not `"${ROOTS[@]}"` at once:

```bash
AG="$( { [ -x node_modules/.bin/ast-grep ] && echo node_modules/.bin/ast-grep; } || command -v ast-grep || true)"
[ -n "$AG" ] || echo "§6 ast-grep NOT-RUN (ast-grep not installed — to enable: npm i -D @ast-grep/cli@0.45.3, or brew install ast-grep) → grep 6 is the lane"
[ -n "$AG" ] && "$AG" scan --globs '!**/components/ui/**' --globs '!**/shared/ui/**' --json=compact "${ROOTS[@]}" --inline-rules '
id: ds-native-button
language: tsx
rule:
  kind: jsx_opening_element
  all:
    - has: { field: name, regex: "^button$" }
    - has: { kind: jsx_attribute, regex: "^className=", stopBy: end }
  not:
    inside: { kind: program, stopBy: end, has: { kind: import_statement, regex: "\\bButton\\b", stopBy: end } }'
```

Repeat with `select`/`Select`, `input` + `type="checkbox"`/`Checkbox`. Known gap: a file that imports the DS `Button` **and** styles a native one is skipped; drop the `not` block for a stricter, noisier pass.

**Measured** (2026-10-05). On the research fixture set (`pos`/`neg` in CSS, TSX, Vue, an Angular template and styled-components), grep 1 hits 9/9 positive lines and 0 decoys: `:root { --x: #… }`, `@theme`, the `#bad {` ID selector, `href="#add"`, `&#123;` and `var(--…)` are skipped. The hex regex the earlier version of this skill printed, `#[0-9a-fA-F]{3,8}\b`, matches all three of ID selectors, `href="#…"` and HTML entities. On `benchmarks/fixtures/web-dashboard`, grep 1 returns 3 lines, including the seeded WEB-TOKEN-01 (a hex literal byte-identical to a token), and grep 3 returns 2, including WEB-TOKEN-02 (an off-scale padding); the other 4 UI fixtures return 0–2. On a read-only real React 19 + Vite + Tailwind 4 (`@theme inline`) + Radix application, the script runs in under a second: grep 1 gives 117 lines after the `scripts/` and `*.mock.*` exclusions (340 before). Most of the 117 are print and receipt templates, brand-colour defaults stored as data, web-manifest `theme_color`, prose in multi-line JSX comments whose continuation lines carry no `*`, and order numbers such as `'#1234'`, which are valid 4-digit hex. Grep 2 gives 23 lines; it gave 281 before the layout sizes were dropped, and 249 of those were `max-h-[88vh]`, `min-w-[11rem]` and similar. Grep 6 flags 17 files for `button` and 15 for `tablist`; the ast-grep rule flags 19 `button` files, and one sampled `role="tablist"` strip's own comment calls it a hand-rolled strip that never became the DS tab hub. Grep 9 finds 36 unreferenced of 252 declared tokens, among them a whole `--chart-1…5` set superseded by `--series-*`. Grep 10 gives 140, of which 125 are in print templates. Grep 8 gives 32 (custom-card colour pickers and comments). Grep 8b (added 2026-10-18 for AL-08) returns 0 on all 23 `benchmarks/fixtures` roots: none declares a primitive ramp (8p = 0), so the lane prints `N/A (no primitive tier)` there. On a scratch tree with `--blue-500` / `--color-red-600` aliased by `--color-primary` / `--color-danger`, it printed 3 lines carrying the 4 primitive uses (a CSS `var()`, a TSX style `var()`, a `var()` with a fallback, a Tailwind 4 `bg-(--color-red-600)` shorthand) and skipped the 2 alias definitions, the semantic `var(--color-danger)` and a commented use. **Re-measured 2026-10-15** on the same app inside a real NestJS + React monorepo: grep 9 fell from 36 to 23 once the Tailwind 4 namespaces `--z-index-*` (6 tokens, used as `z-chrome` and kin), `--transition-duration-*` and `--animation-duration-*` (3 each) joined `NS` and the v4 shorthand `w-(--sidebar-width-collapsed)` counted as a reference; 13 of the 36 were those false positives and the 23 left were all real (22 unread tokens plus one alias). Grep 1 fell from 98 to 96 once `*.test-data.*` fixture files left the scan. The fixture counts are unchanged.

## The 3,000-hit path

1. **Intersect** with the route table and drop the exempt contexts by **group**, one read each: a print, receipt or label template (an HTML string written into a print window or PDF); an email template; a web-manifest or brand-default data file; a DS primitive. Name each dismissed group in the coverage block.
2. **Group** by (value, file family). One literal repeated in 40 files is one `consolidate-tokens` group with 40 sites; a shared wrapper with a literal is one finding with N call sites (`ui § 9`).
3. **Rank:** colour on themed surfaces first (a literal does not follow the dark theme), then primary routes (landing, auth, checkout-class, list, form), then legacy.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** One computed-style conformance run per route × theme (§ Proof) confirms or refutes whole groups: a literal that never renders is dead, and a value that renders in both themes unchanged while its neighbours change is the themed miss.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity: **medium** by default. **High** when the literal is a colour on a surface the project themes (≥ 2 themes shipped), or when it lands in a diff (new drift is cheaper to stop than to sweep). One step lower in legacy code nobody is changing. Never critical.

| § | Class (research id) | Default |
|---|---|---|
| 1 | Raw colour literal outside a token definition (D-01) | medium; high on a themed surface or a diff |
| 2 | Tailwind arbitrary value on a token axis (D-02) | medium |
| 3 | Inline style literal (D-03) | medium |
| 4 | z-index magic number (D-04) | low; medium when an overlay renders under another |
| 5 | `!important` / the Tailwind important modifier (D-05) | low |
| 6 | DS component re-implemented beside its export (D-06) | high when the DS equivalent exists and differs in behaviour |
| 7 | Deprecated DS component or token still used (D-07) | medium |
| 8 | Default-palette utility on a semantic theme (D-08); a primitive-tier token where a semantic one aliases it (AL-08) | medium |
| 9 | Declared token nothing references (D-09) | low |
| 10 | Off-scale spacing, type, radius or shadow literal (D-10) | medium |

### 1. Raw colour literal

```
BAD:   <span style={{ color: failed ? '#d92d20' : 'var(--color-text-muted)' }}>   ·   .card { background: rgba(16,24,40,.6) }
GOOD:  color: failed ? 'var(--color-danger)' : 'var(--color-text-muted)'          ·   background: var(--overlay)
```
**Read the code:** Does a token hold this value exactly (`rg -n -F '<value>'` over the token files), or nearly? Is the line a definition, a comment continuation, an ID or an order number? Is it a canvas chart or a library control that cannot read a CSS var (`ui-design-sweep` verb 1 carve-out)? Does the surface theme? **Finding when** a rendered literal bypasses an existing token, or no token exists and the value repeats ≥ 3 times (an `extract-token` group). **Proof:** the trace (literal, token definition, route); for themed surfaces the theme-flip variant of the conformance oracle.

### 2. Tailwind arbitrary value on a token axis

```
BAD:   className="bg-[#1e40af] p-[13px] text-[14px] rounded-[6px]"
GOOD:  className="bg-primary p-3 text-sm rounded-md"   ·   bg-[var(--brand)] / bg-(--brand) is a token through arbitrary syntax
```
**Read the code:** Which theme value is nearest (v4: `--spacing` × n, the `--text-*` scale, `--radius-*`)? Is the class inside a DS primitive defining its own one-off? **Finding when** the value is on a token axis and the theme has a step for it, or it repeats ≥ 3 times. **Proof:** the trace; the conformance oracle for a rendered off-scale value.

### 3. Inline style literal

```
BAD:   style={{ padding: '13px' }}   ·   :style="{ color: '#fff' }"   ·   [style.color]="'#ff0000'"
GOOD:  a class from the scale  ·  style={{ '--progress': pct }} (the token bridge)  ·  width: `${pct}%` (dynamic geometry)
```
**Read the code:** Is the value dynamic (geometry, a virtualised row's `top`) or a constant? **Finding when** a constant design value is set inline where a token or class exists. **Proof:** the trace.

### 4. z-index magic number

```
BAD:   z-index: 9999  ·  className="z-[9999]"  ·  zIndex: 1000
GOOD:  z-index: var(--z-modal)  ·  z-50 from the scale  ·  z-index: 0 / 1 / -1 inside a local stacking context
```
**Read the code:** Does the project define a layer scale (`--z-*`)? Which overlay families (dialog, menu, toast, tooltip, sticky header) does this element compete with? **Finding when** a magic number stands where a layer token exists, or two overlays order wrongly. **Proof:** open each overlay on each layout; `document.elementFromPoint` at the overlay's centre is inside it.

### 5. `!important`

```
BAD:   .btn { color: #fff !important }  ·  className="!mt-2" (v3)  ·  className="mt-2!" (v4)
GOOD:  fix the specificity at the source  ·  the reduced-motion reset (`animation: none !important`) and `.sr-only` are the documented exceptions
```
**Finding when** it overrides a token or a theme. **Proof:** static; read each (no oracle adds evidence).

### 6. DS component re-implemented

```
BAD:   <button className="rounded bg-blue-600 px-4 py-2 text-white">Buy</button>   in a file that never imports Button
       <div className="fixed inset-0 z-50" role="dialog" aria-modal="true">…</div>  beside the DS Dialog
GOOD:  <Button>Buy</Button>  ·  <Dialog>  ·  a native element inside the DS source  ·  Radix asChild / Slot composition
```
**Read the code:** Does the DS export this component, and does its API cover this use (a variant, a size, `asChild`)? Is the native element unstyled inside a DS wrapper that styles it? What behaviour does the DS version encode that this one lacks (focus trap, Escape, focus return, `aria-*`, the busy state)? **Finding when** the DS equivalent exists and the local copy differs in behaviour or look. **Proof:** the behavioural diff — the same keyboard path and axe run on the DS component and on the local copy, opened; the DS version passes and the copy fails. The a11y half is `a11y-scan`'s oracle when the frontend pack is installed; without it the row is `[report-flagged]` with that test written out. At scale, route the remedy to `/unify-surfaces`.

### 7. Deprecated DS component or token

```
BAD:   import { OldModal } from '@acme/ds'   where OldModal carries @deprecated   ·   a v3 utility v4 renamed
GOOD:  the replacement the @deprecated note names
```
**Read the code:** Does the deprecation name a replacement, or is none available yet (then it is Hardening)? **Finding when** a rendered path uses a deprecated export or class with a replacement available. **Proof:** `@typescript-eslint/no-deprecated` on the line, or upgrade the DS in scratch and `tsc --noEmit` lists the removed export.

### 8. Default-palette utility, or a primitive-tier token, on a semantic theme

```
BAD:   text-blue-500 · bg-emerald-500   when the theme defines primary / success
BAD:   color: var(--blue-500) · bg-(--color-red-600)   when --color-primary / --color-danger alias those ramps (8b, AL-08)
GOOD:  text-primary · bg-success · var(--color-danger)   ·   a project whose documented DS IS the default palette (a neutral scale)
```
**Read the code:** Is it a user-chosen colour stored as data (a picker's swatch list)? Does the theme close the palette (`--color-*: initial`)? For 8b: does a declaration mandate the semantic tier (an ADR, a design-system doc line, a lint rule banning primitive names — the align oracle's T1/T2 rows), or is the primitive ramp the documented API? Which semantic tokens alias this primitive (`token-map.py <root> --resolve=<semantic>` per candidate), and do they hold its value in every theme? **Finding when** a fixed UI role is painted from the default palette or from a primitive ramp while a semantic token for that role exists. With no declaration that mandates the semantic tier, an 8b hit is a split for `convention-oracle` § 2 (AL-02), not a finding. **Proof:** the trace; the theme-flip variant (a default-palette class or a primitive token does not move with the theme). **Route:** exactly one semantic candidate, equal in every theme → an EQ row `/align` closes (AL-08); several candidates (`--color-danger` and `--color-error` both alias `--red-600`) → `[report-flagged]`, the role decides, a human picks.

### 9. Declared token nothing references

**Read the code:** Map token → utility first (v4 `--color-brand` is used as `bg-brand`; a `--breakpoint-md` is used as `md:`; `--z-index-chrome` as `z-chrome`; `--transition-duration-base` as `duration-base`; any token as the v4 shorthand `w-(--x)`). Is it exported for a native app, an email build or a third-party widget? **Finding when** no var, utility, script or downstream build reads it. **Proof:** the empty reference search, printed. Fix: delete, or document the external consumer.

### 10. Off-scale spacing, type, radius or shadow literal

```
BAD:   padding: 13px  ·  font-size: 15px  ·  styled.div` margin: 13px `  ·  box-shadow: 0 1px 2px …
GOOD:  var(--space-3)  ·  var(--text-sm)  ·  shadow-md  ·  0, auto, 1px hairlines, 100%, layout calc()
```
**Read the code:** Is the value on the scale under another name? Is it inside a DS primitive that defines the scale? **Finding when** a rendered spacing, type, radius or shadow value is off the scale. **Proof:** the trace; the conformance oracle reports rendered px values not in the scale.

## The swap trap — why "nearest token" is not "safe swap"

For each literal, classify it with **`scripts/token-map.py`** (this skill's folder; stdlib, `python3 -I`, reads the root and writes nothing into it). It resolves every token source of § Adapt to the codebase per theme (`:root`, `.dark`, `[data-theme]`, `@theme`, DTCG `{alias}` chains, TS theme objects) and the property family of both sides. `token-map.py <root> --lookup=<value> --prop=<css prop> [--site=<relpath>]` prints one of four classes:
- **`EXACT`**: the value equals a token of the **same family**. `eq=yes` only when there is exactly one candidate **and** it holds that value in every shipped theme. Only an `EXACT eq=yes` row is a mechanical swap, and it is `/align`'s to close (V397 round-trip, V394 zero computed-style diff).
- **`NEAREST`**: no same-family match, but the family has tokens. It prints the nearest token and its distance (px, ms, weight steps, or ΔE × 100 in OKLab for colours). Snapping changes pixels: report-flagged, never auto-fixed.
- **`NONE`**: the family has no tokens (fixed layout geometry without a size scale), or the value cannot be compared.
- **`EXEMPT`**: values tokens do not cover by design (`0`, `auto`, `%`, a `1px` hairline, `currentColor`, `calc()` bodies).

Border, outline and text-decoration lengths form their own `width` family, so `border-[1.5px]` is never matched against an icon-size or spacing token (measured on a real NestJS + React monorepo, 2026-10-18: 13 width sites that had read NEAREST `--icon-xs` or as a colour now read `width` NONE). Every row also carries **`xfam=<token>`** when the value matches a token of **another** family. A cross-family match is never exact. Measured on `benchmarks/fixtures/web-dashboard` (2026-10-18): `padding: '13px'` looks up `NEAREST --space-3=12px (1px)` with `xfam=--font-size-sm`, while `'#d92d20'` looks up `EXACT --color-danger eq=yes`. `--scan` classifies every literal site in the root, including ternary, `??` and `||` branches of a style value, and `--names` lists every declared token (the emitted-name check, V398). Without Python, fall back to the manual reading below: colour by ΔE, spacing by the nearest scale step, type by the nearest type step, radius from the radii table.

**Nearest-by-ΔE is a proximity measure, not a safety proof.** Two colours a human calls "the same grey" can sit on opposite sides of a contrast threshold. Computed from the WCAG relative-luminance formula: **`#767676` on `#ffffff` is 4.54:1** (passes AA body text, 4.5:1) and **`#7a7a7a` on `#ffffff` is 4.29:1** (fails). They are four steps apart per channel, a CIE L\* difference of about 1.6, well inside any tolerance a "nearest match" heuristic uses. It will swap one for the other without comment. So for every **colour** swap:

1. Resolve the token's actual value and the **role** it plays at that site — body text, large text, a non-text UI boundary, decoration — because the threshold differs (4.5:1, 3:1, 3:1, none; WCAG 2.2 SC 1.4.3 and 1.4.11).
2. **Compute** the ratio against the resolved background at that site, in every theme the project ships.
3. Only a swap that stays at or above its role's threshold in every theme is `auto-fixable`. Anything else is `manual review required`, with the computed before/after ratios printed.

A spacing or radius swap is visually safe but can change a hit area: a swap on an interactive element re-checks target size (`a11y-scan` §5 when the frontend pack is installed) before it is called mechanical. If no token exists for the value, the design system is missing it: route the addition through `extract-token` with the architect's approval, never through this skill.

## Proof — computed-style token conformance

The oracle for §1–§4, §8 and §10 at scale. Run on a production build at each route × theme, after the route's own content marker is visible (the `reach()` step of `a11y-scan`'s recipe when the frontend pack is installed). It is framework-free: whatever styling technique produced a colour, the browser computed it.

```ts
// Resolve the palette from the tokens, normalise every colour through a 1×1 canvas so hex, rgb() and oklch() compare equal,
// then sample what actually rendered. Run once per theme; diff the two runs for the theme-flip variant.
export const offToken = (page: Page, tokens: string[], scale: number[]) => page.evaluate(({ tokens, scale }) => {
  const cx = document.createElement('canvas').getContext('2d', { willReadFrequently: true })!;
  const norm = (c: string) => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); return cx.getImageData(0, 0, 1, 1).data.join(','); };
  const root = getComputedStyle(document.documentElement);
  const palette = new Set(tokens.map((t) => root.getPropertyValue(t).trim()).filter(Boolean).map(norm));
  const out = new Map<string, { n: number; sel: string }>();
  const add = (k: string, el: Element) => { const r = out.get(k); if (r) r.n++; else out.set(k, { n: 1, sel: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + '.' + [...el.classList].slice(0, 3).join('.') }); };
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height || el.closest('svg, iframe')) continue;
    const s = getComputedStyle(el);
    for (const p of ['color', 'background-color', 'border-top-color', 'outline-color'] as const) {
      const v = s.getPropertyValue(p); if (!v || /^rgba\(0, 0, 0, 0\)$|transparent/.test(v) || (p !== 'color' && v === s.color)) continue;
      if (!palette.has(norm(v))) add(`${p}: ${v}`, el);
    }
    for (const p of ['padding-top', 'padding-left', 'margin-top', 'gap', 'font-size', 'border-top-left-radius'] as const) {
      const px = parseFloat(s.getPropertyValue(p)); if (px > 1 && !scale.includes(px)) add(`${p}: ${px}px`, el);
    }
  }
  return [...out].map(([value, r]) => ({ value, ...r })).sort((a, b) => b.n - a.n);
}, { tokens, scale });
```

**Fails first:** before the fix the literal's value (or the off-scale px) is in the list with the candidate's selector. After it, the value is gone and nothing new appeared. **Theme flip:** run in light and dark; an element whose colour is identical in both while the tokens it should use differ is the themed miss — the strongest §1 and §8 evidence. Translucent tokens (`color-mix`, alpha) normalise to their composited value on the canvas's black ground; compare like with like and treat a near-miss within ±1 channel as rounding. The §6 oracle is the behavioural diff in § 6. Both are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states: *Token conformance* (V141; this skill carries the full `offToken` helper) and *Behavioural diff vs the DS component* (V142).

**Whole-class variants** a fix must survive: CSS, a locally defined SCSS variable, styled-components / Emotion, an inline style, a Tailwind arbitrary value, the default palette, a component SVG `fill`, raw-scale theme access (`theme.colors.blue[500]`), the dark-theme variant of the swapped token, and the hover / focus / disabled states of the same control.

## Output

```
design-token-audit — lanes: tailwind 4.3 (@theme inline, src/shared/theme/theme.css:37), CSS custom properties
  (src/index.css :root/.dark, src/shared/theme/tokens.css); DS root src/shared/ui; ast-grep 0.45.3 (scratch); stylelint absent
Catalog: 252 tokens · semantic colours yes (--primary, --danger, --success …) · themes light, dark, aurora

Findings: 2 · Unconfirmed: 1

1. src/components/billing/InvoiceList.tsx:42                     [report-with-fix]   high
   §1 colour literal — `'#d92d20'` in the failed-status branch; byte-identical to --color-danger
   (src/styles/tokens.css:9). Route /orders. Proof: conformance run, dark theme — the cell stays #d92d20
   while --color-danger resolves to #f97066. Fix: verb 1 consolidate-tokens → var(--color-danger);
   contrast at this role (text on --color-surface): light 4.9:1, dark 5.6:1 → auto-fixable.

2. src/features/orders/list/components/OrderStatusTabs.tsx:80     [report-with-fix]   high
   §6 DS component re-implemented — a role="tablist" strip of styled <button>s beside the DS Tabs
   (src/shared/ui/tabs.tsx); 14 sibling screens use Tabs. Proof: keyboard path — ArrowRight on the selected
   tab moves nothing; the DS Tabs moves selection. Fix: /unify-surfaces (tabs) onto the DS Tabs.

3. src/index.css:1284                                              [report-flagged]    medium
   §1 colour literal — `rgba(79, 158, 255, 0.28)` in the dark block, no token holds it. Unproven link:
   whether it is the selection highlight the theme should own. Settling probe: conformance run, dark,
   on /orders with a row selected. Fix: designer decision — extract-token or the closest existing tint.

Verification: 61 candidates → 2 findings · 1 unconfirmed · 9 hardening · 0 pre-existing · 49 refuted
Swap safety: 1 colour swap computed (both themes) · 0 manual-review

Class coverage:
  §1  colour literal            checked (117 hits / 22 groups → 1 finding, 1 unconfirmed; print templates, brand data, comments dismissed by group)
  §2  arbitrary value           checked (23 hits → 0 findings; 9 × border-[1.5px] in the DS input, Hardening)
  §3  inline style              checked (0 hits)
  §4  z-index                   checked (2 hits → 0 findings; DS data-table sticky cells)
  §5  !important                checked (29 hits → 0 findings; 19 in the reduced-motion reset)
  §6  re-implemented component  checked (ast-grep 19 files + rg 15 tablist files → 1 finding) · Live, unreviewed (12 groups / 17 files — continue with the ast-grep button rule)
  §7  deprecated                checked (1 @deprecated export, not in the DS root → N/A)
  §8  default palette           checked (32 hits → 0 findings; a colour picker's swatch list is user data)
  §9  unreferenced token        checked (36 of 252 → 0 findings, 1 Hardening group: --chart-1…5 superseded by --series-*)
  §10 off-scale literal         checked (140 hits → 0 findings; 125 in print templates)
```

`[report-with-fix]`: the literal, the token (or `no token`), the route and the proof are all present, and the fix is a verb or route named above. `[report-flagged]`: one link is unproven (no catalog, a value no token holds, a render not run), and the row names that link and the settling probe. The coverage block lists **all ten** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the surface is absent (no Tailwind for §2, no DS root for §6–§7, no semantic theme for §8); `blocked (<reason>)` when a grep or lint lane failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`. **Auto-fixable** rows are itemised, each with its `<file:line>`, token and computed contrast per theme, before any total is printed.

Write the report to `ai/audits/design-tokens-<date>.md`. A previous report gives the trend line (literals per class, last run → this run).

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (posting rules § 1–10, contrast exemptions § 19, design system § 84–90) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The design-system precedents, in short:

- **Definitions, not uses** (§ 84): token files, `@theme` / `@theme inline`, DTCG JSON, a Tailwind config, the DS's own primitives defining the scale.
- **Contexts that must carry literals** (§ 85): SVG illustrations and brand logos, email templates (inline styles are required), print / receipt / label templates written into another document, web-manifest `theme_color`, third-party widget overrides.
- **Data, not design** (§ 86): a user- or merchant-chosen colour stored with its default, a colour picker's swatch list, an order or ticket number such as `#1234`.
- **Token through arbitrary syntax** (§ 87): `bg-[var(--brand)]`, v4 `bg-(--brand)`, `style={{ '--progress': x }}`.
- **Layout and dynamic geometry** (§ 88): `w-[calc(100%-2rem)]`, `grid-cols-[1fr_auto]`, `max-h-[88vh]`, `width: ${pct}%`, a virtualised row's `top`.
- **Native elements inside the DS, Radix `asChild` / `Slot`, headless-library hosts** are not §6 (§ 12, § 89).
- **The reduced-motion reset and `.sr-only`** are the documented `!important` exceptions (§ 90).

## When to run

- On any diff touching `components/`, `views/`, `pages/`, `screens/`, a stylesheet, a theme or token file: the `/frontend-audit` dispatch signal "a style, token or animation change" when the frontend pack is installed.
- On every whole-repo `/frontend-audit` (its Design tokens row), `/polish` and `/align` on `frontend-*`, reporting all ten classes.
- Before a design-system version bump (§7 lists what would break), after a designer hands off a screen, and quarterly.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any proposed replacement that names a token absent from the resolved catalog, and on a `<file:line>` whose line does not contain the flagged value.
- Halt on an aggregate auto-fix claim ("18 colours → exact token match") without the itemised rows behind it.
- Halt on listing a **colour** swap as auto-fixable before its contrast at the rendered role is computed in every theme (§ The swap trap).
- Do not report a grep hit as a finding, or dismiss a group without reading one member. A class whose grep did not run is `blocked`, never `checked`.
- Do not cite a lint plugin the repo does not install and this run did not install in scratch.
- Do not apply the fix. Do not re-derive a class another skill owns (§ Boundaries); cross-link it.

## Related

- `ui-design-sweep` (this pack) — **the applier.** Verbs 1 `consolidate-tokens` and 2 `extract-token` consume this skill's findings and own the edit, the visual baseline and the a11y re-check. Detection and resolution here; transformation and verification there.
- `@design-system-guardian` — full governance; this skill is its token and component-drift dimension. `@design-system-architect` codifies the tokens this skill measures against.
- `motion-audit` (this pack) — motion tokens. `chart-encoding-audit` (this pack) — data ramps. `@theme-specialist` — theme parity.
- `a11y-scan` §3 and §5, `a11y-code-scan` (frontend pack, when installed) — contrast and target size as WCAG findings; `/frontend-audit` folds this skill's coverage block into its Design tokens row.
- [`design-systems.md`](../../ai-patterns/design-systems.md) — the consumer rule this skill measures against and its § Enforcement list of rules that are real.
- `/polish` · `/enhance-ui` — apply verbs 1–2; `/align` — enforce a token once it exists; `/unify-surfaces` — §6 at scale.
