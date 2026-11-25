---
name: a11y-code-scan
description: "Static WCAG 2.2 AA detector for UI source: a11y lint lanes per stack plus greps for 14 classes, each proved at a route-state."
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: a11y-code-scan

## Premise

Most accessibility defects are written into source long before anyone renders the page: a `div` that takes clicks, an icon button with no name, a focus ring removed in a stylesheet, a dialog that never moves focus, an error rendered as red text beside its field. This skill finds them in the code, across React, Vue, Svelte, Angular and plain HTML. It runs each stack's own a11y lint rules first, then greps for what lint cannot see — Tailwind classes, cross-file facts, multi-line JSX — and maps every candidate to the WCAG 2.2 success criterion it would fail.

**Every finding cites the source `<file:line>` + the route that renders it + the WCAG 2.2 SC and level + the oracle that proved it (or the test that would settle it) + the fix in the project's own components.** A lint message or a grep hit is never a finding by itself. "No accessibility issues" is never printed: the output is a class-coverage block, and automation finds only part of the problem. Deque's study found 57 % of issues **by volume**; the best single tool in the GDS test caught 41 % of 143 barriers ([`precedents/ui.md`](../../../../snippets/precedents/ui.md) § 58). A clean run is the automated floor. The manual pass — keyboard walk, screen reader, zoom, content judgement — stays, and the report says so.

Below, `ui § n` means [`precedents/ui.md`](../../../../snippets/precedents/ui.md) § n; a bare `§n` is a detector in this skill.

**Detect statically, prove at a route-state.** The proof is an oracle from [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states, run on a production build at the route and state that expose the defect: the axe rule at that route-state, a keyboard path, a role or label query, a focus or geometry probe. A **static-fact** class whose failure is fully visible in source passes with the two-ended trace (`precedents/ui.md`, the proof rule). Every other candidate without a harness is **Unconfirmed**, carrying the settling test. It is never dropped, and never promoted on reading alone.

## The rule

A candidate is a finding when all four hold:

1. **It renders.** A route, screen or layout imports the component and shows it to a user, in a state the user can reach. A story-only, dead or design-system-internal file fails here until a route imports it.
2. **A real user meets it.** Keyboard only, a screen reader, zoom 200 % or 320 px, forced colours, the dark theme.
3. **Nothing already provides it.** No headless primitive (Radix, React Aria, Headless UI, Ark, Reka, Bits UI, Angular CDK / Material), native element or shared field wrapper supplies the role, name, focus or keyboard model (`precedents/ui.md` § 12–14).
4. **The oracle fired, or it is a static fact.** The failure is shown at the route-state, or it is fully visible in source.

## Boundaries

- **Rendered-only classes** belong to `a11y-scan` (this pack): the axe floor per route × state × theme, contrast (1.4.3, 1.4.11), target size (2.5.8), reflow, zoom and text spacing (1.4.4, 1.4.10, 1.4.12), focus obscured (2.4.11), headings, landmarks and `lang` as axe sees them, and the integrity of the project's a11y gate. Their static riders (`user-scalable=no`, `<html>` without `lang`, an orientation lock) are `a11y-scan` grep 6; this skill no longer greps them, so one site is never reported twice.
- **Motion and animation** (2.2.2 auto-moving content, 2.3.3) → `motion-audit` (ui-ux pack), when installed; §12 here keeps media captions and autoplay audio. Without ui-ux, autoplay rows stay here and reduced-motion rows print `N/A (owner pack ui-ux not installed)`.
- **Contrast values and token pairs** → `design-token-audit` (ui-ux pack) computes them; the visual fix is `ui-design-sweep` verbs 12 (lift-contrast), 13 (align-focus-ring), 16 (expand-tap-target) and 18 (clarify-affordance) when ui-ux is installed.
- **Native mobile accessibility** (React Native, Flutter, Compose, SwiftUI) is not this skill's: DOM tooling on a native tree proves nothing. It is `mobile-a11y-scan` (mobile pack, when installed); without it, those files print `N/A (native UI — not a DOM)`.
- **Security in markup** — `dangerouslySetInnerHTML`, `v-html`, `target=_blank` without `noopener` — → `xss-scan` (security pack, when installed).
- **Navigation by `onClick` on a non-link** is reported here as §1 (2.1.1, the keyboard half). The routing and crawl half (no `href`, no new tab, no copy-link) is `routing-scan` §1 (this pack): one element, one finding, credited to both. Hard-coded `aria-label` text is i18n's; the missing name is this skill's.
- **The judge** of an a11y finding is `@ux-reviewer` (ui-ux pack) when installed, else `@accessibility-auditor` (this pack). This skill is the static detector both consume.

## Adapt to the codebase — lane table

Read each framework and lint plugin **with its version** from the lockfile, and print the lanes you ran in the output header. Lint lanes run first; the grep lanes cover what lint cannot see.

| Lane | Lint lane (rule source, version read 2026-10-05) | What lint misses (the greps cover it) | Built-in that is a precedent |
|---|---|---|---|
| **React / Next / React Router 7 / Remix** | eslint-plugin-jsx-a11y 6.10.2. Its peers stop at ESLint 9 while ESLint 10.12.0 is current, so it runs in a scratch ESLint 9 install with `control-has-associated-label` and `no-aria-hidden-on-focusable` turned on and design-system components mapped (`precedents/ui.md` § 52–53). On ESLint 10 projects read the fork `eslint-plugin-jsx-a11y-x` (0.2.0, peers `eslint ^9 \|\| ^10`, lockfile read 2026-10-15): same rules, prefix `jsx-a11y-x/` | icon children it cannot resolve, Tailwind `outline-none`, dialog focus, live regions, error association | Next App Router route announcer (`precedents/ui.md` § 27) |
| **Vue 3 / Nuxt 4** | eslint-plugin-vuejs-accessibility 2.6.0 `flat/recommended` + `no-aria-hidden-on-focusable` + `no-role-presentation-on-focusable` | icon-only buttons (it saw none of the 5 seeded), redundant alt | `<NuxtRouteAnnouncer>` from 3.12, optional — check `app.vue` |
| **Svelte 5 / SvelteKit** | the compiler's `a11y_*` warnings via `svelte-check` (eslint-plugin-svelte 3.23.0 has no a11y rules) | Tailwind, live regions, error association | SvelteKit announcer + focus reset to `body` |
| **Angular 20–22** | @angular-eslint/eslint-plugin-template 22.5.0: the 11 `templateAccessibility` rules + `no-positive-tabindex` | `mat-icon` buttons (it counts the ligature as content), paste blocking, focus | CDK `cdkTrapFocus`, Material dialog |
| **Solid / Qwik / Lit** | none run here (eslint-plugin-lit-a11y 5.1.1 exists for Lit templates) | everything — greps only | — |
| **Plain HTML / SSG output** | html-validate 11.16.2 `--preset a11y` on built HTML (`dist/`, `build/`, `.next/server/app/`) | `lang`, `user-scalable` | — |
| **CSS / SCSS** | @double-great/stylelint-a11y 3.5.4: `a11y/no-outline-none`, `a11y/selector-pseudo-class-focus` | Tailwind classes (grep 3b) | — |

## Lint lanes

Run in a scratch directory, never in the project, and never commit the config. Keep only the a11y rule ids. The audit never installs: the lanes run from a toolchain the user installed once (`$REFRACT_A11Y_LINT`, default `~/.cache/refract/a11y-lint`), and without it they print `NOT-RUN (toolchain not installed — to enable: <the exact npm i>)`. Then the fallback lane is the project's own installed lint (`npx --no-install eslint` from the root, when `node_modules` exists): print which preset and which rules it holds at error, and mark the strict-only rules `blocked (no install)`. Each message is a candidate for the § its rule maps to (§ Scans for). A lint lane that did not run prints `NOT-RUN` or `blocked (<reason>)` for its rule column. The class's greps still run.

```bash
# The toolchain is installed once BY THE USER, never by this audit: T holds it, L is this run's scratch (configs, output).
T="${REFRACT_A11Y_LINT:-$HOME/.cache/refract/a11y-lint}"; L="$(mktemp -d "${TMPDIR:-/tmp}/a11y-lint.XXXXXX")"
if [ -x "$T/node_modules/.bin/eslint" ]; then ln -s "$T/node_modules" "$L/node_modules"
else echo "a11y lint lanes NOT-RUN (toolchain not installed — to enable: mkdir -p \"$T\" && cd \"$T\" && echo '{\"private\":true}' > package.json && npm i --no-audit --no-fund eslint@9 eslint-plugin-jsx-a11y@6.10.2 eslint-plugin-vuejs-accessibility@2.6.0 typescript-eslint @angular-eslint/eslint-plugin-template@22.5.0 @angular-eslint/template-parser@22.5.0 html-validate@11.16.2)"; fi
cat > "$L/react.mjs" <<'EOF'
import jsxA11y from 'eslint-plugin-jsx-a11y'; import tseslint from 'typescript-eslint';
export default [{ ignores: ['**/node_modules/**', '**/dist/**', '**/build/**', '**/.next/**', '**/*.{test,spec,stories}.*', '**/{test,tests,__tests__,e2e}/**'] },
  { files: ['**/*.{jsx,tsx}'], languageOptions: { parser: tseslint.parser, parserOptions: { ecmaFeatures: { jsx: true } } },
    plugins: { 'jsx-a11y': jsxA11y },
    settings: { 'jsx-a11y': { polymorphicPropName: 'as', components: { /* the project's wrappers: Button: 'button', Link: 'a', TextField: 'input' */ } } },
    rules: { ...jsxA11y.flatConfigs.strict.rules, 'jsx-a11y/control-has-associated-label': 'error', 'jsx-a11y/no-aria-hidden-on-focusable': 'error',
      'jsx-a11y/prefer-tag-over-role': 'off', 'jsx-a11y/no-autofocus': 'off' } }];   // advice, not SC failures (precedents/ui.md § 3, ui § 23)
EOF
cat > "$L/vue.mjs" <<'EOF'
import vueA11y from 'eslint-plugin-vuejs-accessibility'; import tseslint from 'typescript-eslint';
export default [{ ignores: ['**/node_modules/**', '**/dist/**', '**/.nuxt/**', '**/.output/**', '**/*.{test,spec,stories}.*'] }, ...vueA11y.configs['flat/recommended'],
  { files: ['**/*.vue'], languageOptions: { parserOptions: { parser: tseslint.parser } },
    rules: { 'vuejs-accessibility/no-aria-hidden-on-focusable': 'error', 'vuejs-accessibility/no-role-presentation-on-focusable': 'error' } }];
EOF
cat > "$L/ng.mjs" <<'EOF'
import tpl from '@angular-eslint/eslint-plugin-template'; import parser from '@angular-eslint/template-parser';
const R = ['alt-text', 'click-events-have-key-events', 'elements-content', 'interactive-supports-focus', 'label-has-associated-control', 'mouse-events-have-key-events',
  'no-autofocus', 'no-distracting-elements', 'role-has-required-aria', 'table-scope', 'valid-aria', 'no-positive-tabindex'];
export default [{ ignores: ['**/node_modules/**', '**/dist/**', '**/.angular/**'] }, { files: ['**/*.html'], languageOptions: { parser }, plugins: { '@angular-eslint/template': tpl },
  rules: Object.fromEntries(R.map((r) => ['@angular-eslint/template/' + r, 'error'])) }];
EOF
# Run from the repo root (with -c, ESLint 9 resolves file globs against the cwd). One lane per stack present.
[ -e "$L/node_modules" ] && "$L/node_modules/.bin/eslint" --no-config-lookup -c "$L/react.mjs" -f json "${ROOTS[@]}" > "$L/react.json"
[ -e "$L/node_modules" ] && "$L/node_modules/.bin/eslint" --no-config-lookup -c "$L/vue.mjs" -f json "${ROOTS[@]}" > "$L/vue.json"
[ -e "$L/node_modules" ] && "$L/node_modules/.bin/eslint" --no-config-lookup -c "$L/ng.mjs" -f json "${ROOTS[@]}" > "$L/ng.json"
for f in "$L"/{react,vue,ng}.json; do [ -s "$f" ] && node -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1]));const c={};for(const f of r)for(const m of f.messages){c[m.ruleId]=(c[m.ruleId]||0)+1;console.log(f.filePath+":"+m.line+"  "+m.ruleId)}console.error(JSON.stringify(c))' "$f"; done
for r in "${ROOTS[@]}"; do (cd "$r" && npx --no-install svelte-check --output machine --threshold warning 2>&1 | grep -o '"[^"]*" [0-9]*:[0-9]* .*svelte.dev/e/a11y_[a-z_]*'); done   # Svelte: the project's own svelte
[ -e "$L/node_modules" ] && "$L/node_modules/.bin/html-validate" --preset a11y --formatter json 'dist/**/*.html'   # plain HTML / SSG output, after a production build
```

**Measured** (2026-10-05, a read-only React 19 + Vite + Radix + Tailwind 4 application, 1,049 `.tsx` files linted in 6 s): the strict preset returned 182 messages in 105 files. `prefer-tag-over-role` (77, all `role="status"` → `<output>`-style advice) and `no-autofocus` (27) are why the config turns both off. The rest are candidates, not findings. A sample of `control-has-associated-label` and `no-static-element-interactions` showed `htmlFor`-labelled range inputs, `stopPropagation`-only wrappers and buttons whose name is an expression — all refuted on read. On the research fixtures (`pos`/`neg`, one file per stack) the Vue and Angular lanes flagged every seeded click, tabindex and label defect, with 0 decoy hits. Neither saw the icon-only buttons; grep 2a did.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`"${ROOTS[@]}"`). Given no path, rg reads stdin under an agent's shell and reports a silent zero. Any rg error (exit 2) is a failed grep, never zero hits. `TB` is a JSX-aware tag body: `[^>]*` stops at the `>` of `onClick={() => x}`, which made the earlier icon-button grep miss a seeded defect. Multi-line greps use `-U`; read the whole printed tag. File-level greps use `--files-without-match` — never `rg -L`, which is `--follow`.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|@builder\.io/qwik|lit)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,coverage,storybook-static}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,__fixtures__,playwright,cypress}/**' -g '!**/*.{test,spec,stories,story,e2e}.*'
   -g '!*.{md,mdx,snap,map,lock,json}' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/docs/**' -g '!/ai/**' -g '!**/*.min.*')
M=(-g '*.{jsx,tsx,vue,svelte,astro,html}'); C=(-g '*.{css,scss,sass,less,pcss,vue,svelte,astro}'); J=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--|#(?!\{))')   # drops comment-only lines
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'
BTN='button|Button|IconButton|a|Link|NavLink|(?!SelectTrigger\b)[A-Z]\w*Trigger'   # + the project's icon-button wrappers (_extracted-idioms.md); SelectTrigger holds a SelectValue
ICON='(?:<(?:[A-Z][\w.]*|svg|i)\b(?!'"$TB"'\b(?:aria-label|alt\s*=\s*(?!["\x27]{2}|\{\s*["\x27]{2}\s*\})))'"$TB"'/>|<(?:svg|i|mat-icon)\b(?!'"$TB"'\baria-label)'"$TB"'>(?:[^<]|<(?!/?(?:button|svg|i|mat-icon|title)\b)[^>]*>)*</(?:svg|i|mat-icon)>)'
# 0a lanes and versions; 0b headless libraries and form wrappers (gate 4); 0c a11y lint suppressions. (The static riders — zoom lock, <html> without lang, orientation lock — are a11y-scan grep 6, run there only.)
rg -n --no-heading --pcre2 '"(?:eslint|eslint-plugin-jsx-a11y|eslint-plugin-vuejs-accessibility|@angular-eslint/template|angular-eslint|svelte|svelte-check|html-validate|@double-great/stylelint-a11y|@axe-core/playwright|@storybook/addon-a11y|react|vue|@angular/core|next|nuxt|@sveltejs/kit|react-router(?:-dom)?|vue-router|tailwindcss)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --no-heading --pcre2 '"(?:@radix-ui/react-[\w-]+|react-aria(?:-components)?|@headlessui/\w+|@ark-ui/\w+|reka-ui|bits-ui|@angular/cdk|@angular/material|vaul|focus-trap(?:-react)?|sonner|react-hot-toast|react-toastify|vue-sonner|ngx-toastr|@dnd-kit/core|react-hook-form|formik|vee-validate)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --pcre2 'svelte-ignore\s+a11y[_-]|eslint-disable(?:-next-line|-line)?\b[^\n]*(?:jsx-a11y|vuejs-accessibility|@angular-eslint/template/(?:alt-text|click-events|elements-content|interactive-supports|label-has|mouse-events|no-autofocus|role-has|valid-aria|table-scope|no-positive-tabindex))' "${J[@]}" "${X[@]}" "${ROOTS[@]}"
# 1. A non-interactive element with a click handler and no role (R01); a stopPropagation-only wrapper is excluded.
rg -n -U --pcre2 '<(?:div|span|li|td|tr|p|img|section|article|label)\b(?='"$TB"'\s(?:onClick|@click|v-on:click|on:click|onclick|\(click\))\s*=)(?!'"$TB"'\srole\s*=)(?!'"$TB"'\s(?:onClick|\(click\))\s*=\s*["{]\s*(?:\(\s*\$?\w*\s*\)\s*=>\s*)?\$?\w+\.stopPropagation\(\)\s*["}])'"$TB"'>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. Names and labels: 2a icon-only button or link (R02; a link under an `asChild` parent that carries aria-label is marked),
#    2b glyph-only button, 2c image with no alt, 2d placeholder-only input, 2e redundant alt (R11), 2f a <label> that neither
#    names a control (no htmlFor/for) nor wraps one, 2g an id built from label text (rows that render it twice collide).
rg -n -U --pcre2 '<('"$BTN"')\b(?!'"$TB"'\b(?:aria-label|aria-labelledby|title|label)\]?\s*=)(?!'"$TB"'\{\s*\.\.\.)'"$TB"'>\s*(?:'"$ICON"'\s*)+</\1>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | awk -F: '{ print } $3 ~ /^[ \t]*<(a|Link|NavLink)([ \t>]|$)/ { c = "sed -n " ($2 > 8 ? $2 - 8 : 1) "," ($2 - 1) "p \"" $1 "\""; s = ""; while ((c | getline x) > 0) s = s " " x; close(c); if (s ~ /asChild/ && s ~ /aria-label/) print "  ^ 2a: child of an asChild parent with aria-label: read the parent (gate 4), it likely names this link" }'
rg -n -U --pcre2 '<button\b(?!'"$TB"'\b(?:aria-label|aria-labelledby|title)\]?\s*=)'"$TB"'>\s*(?:[^\w\s<{}]{1,2}|&\w+;)\s*</button>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '<(?:img|Image|NuxtImg|NuxtPicture)\b(?!'"$TB"'(?:\balt|\{\s*\.\.\.)\]?\s*=?)'"$TB"'/?>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '<(?:input|textarea)\b(?='"$TB"'\bplaceholder\]?\s*=)(?!'"$TB"'\b(?:id|aria-label|aria-labelledby)\]?\s*=)(?!'"$TB"'\{\s*\.\.\.)(?!'"$TB"'\btype=["\x27](?:hidden|submit|button|reset|checkbox|radio|file)["\x27])'"$TB"'/?>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -i --pcre2 '\balt=["\x27](?:(?:an?\s+)?(?:image|picture|photo|graphic|icon)(?:\s+of)?\b[^"\x27]*|[^"\x27]*\.(?:png|jpe?g|svg|webp|gif|avif))["\x27]' "${M[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '<label\b(?!'"$TB"'\b(?:htmlFor|for)\]?\s*=)(?!'"$TB"'\{\s*\.\.\.)'"$TB"'>\s*(?:[^<{]|\{[^{}]*\})*</label>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:id|\w+Id)\s*[=:]\s*\{?\s*`[^`\n]*\$\{\s*(?:props\.)?(?:label|title|heading|text|caption|placeholder)\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3. Focus indicator removed: 3a CSS outline or outline-style none/0 outside :focus:not(:focus-visible) (R17); 3b Tailwind outline-none with no focus replacement on the line (R18).
rg -n -U --pcre2 '(?m)^(?![^{\n]*:not\(:focus-visible\))[^{}\n]*\{[^{}]*\boutline(?:-style)?\s*:\s*(?:none|0)\s*(?:!important\s*)?[;}]' "${C[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^(?!.*\b(?:focus-visible|focus|focus-within):(?:ring|outline-(?!none\b)|shadow|border|underline|bg-)).*(?<![.\w-])(?:focus:)?outline-none\b(?!-)' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. Files that declare a dialog with no focus primitive and no headless library.
rg -n --pcre2 'role=["\x27](?:alert)?dialog["\x27]|aria-modal' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | cut -d: -f1 | sort -u | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\.focus\(|showModal\(|FocusTrap|focus-trap|useFocusTrap|FocusScope|cdkTrapFocus|\binert\b|@radix-ui/react-(?:dialog|alert-dialog)|@headlessui/|react-aria|vaul|@ark-ui/|reka-ui|bits-ui|@angular/cdk|@angular/material'
# 5. Client router with no built-in announcer (5a); title and focus handling on navigation (5b, read).
rg -l --pcre2 'createBrowserRouter|createHashRouter|<BrowserRouter|createRouter\(|provideRouter\(|RouterModule\.forRoot|@tanstack/react-router|from\s+["\x27]wouter' "${J[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'document\.title\s*=|useDocumentTitle|useHead\(|useSeoMeta\(|TitleStrategy|NuxtRouteAnnouncer|RouteAnnouncer|export\s+(?:const|function)\s+meta\b|<title>' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6. Announcements and errors: 6a custom toast with no live region; 6b live region mounted with its content (R14, alert excluded);
#    6c live region created with content (R25); 6d error text rendered with no role; 6e field errors with no association in the file.
#    6a follows one hop: a hit that renders a component exported from a live-region file is marked, not dropped.
LIVE=$(rg -l0 --pcre2 'role=["\x27](?:status|alert|log)|aria-live' -g '*.{jsx,tsx,vue,svelte}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -o -N --no-filename -r '$1' --pcre2 'export\s+(?:default\s+)?(?:function|const|class)\s+([A-Z]\w*)' | sort -u)
rg -l0 --pcre2 '(?:function|const|class)\s+\w*(?:Toast|Toaster|Snackbar|Flash|Notice)\w*\b' -g '*.{jsx,tsx,vue,svelte}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 'role=["\x27](?:status|alert|log)|aria-live|from\s+["\x27](?:sonner|react-hot-toast|react-toastify|vue-sonner|vue-toastification|ngx-toastr|svelte-french-toast|@radix-ui/react-toast)' | while IFS= read -r f; do h=$(rg -o -N --no-filename -r '$1' '<([A-Z]\w*)' "$f" | sort -u | grep -Fx -- "${LIVE:-__none__}" | head -1); [ -n "$h" ] && echo "6a renders <$h>, a live-region component (one hop: read it): $f" || echo "$f"; done
rg -n -U --pcre2 '(?:&&\s*\(?\s*<[^>]*|v-if=[^>]*|\*ngIf=[^>]*|@if\s*\([^)]*\)\s*\{\s*<[^>]*|\{#if[^}]*\}\s*<[^>]*)(?:aria-live=|role=["\x27](?:status|log)["\x27])' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 'setAttribute\(\s*["\x27]aria-live["\x27][^;]*;[^\n]*(?:textContent|innerText|innerHTML)\s*=[^\n]*appendChild' "${J[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\{\s*!?!?\s*(?:\w+\.)*\w*(?:[eE]rror|[pP]roblem)\w*\??\s*&&\s*\(?\s*<[a-z][\w-]*\b(?![^>]*\b(?:role=|aria-live=|id=))' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '(?<![=\w])\{\s*(?:formState\.)?errors(?:\??\.\w+|\[[^\]]+\])+\s*(?:&&|\?\.message\s*\}|\.message\s*\})|v-if="[^"]*errors|@if\s*\([^)]*(?:errors|invalid)|\*ngIf="[^"]*(?:errors|invalid)|\{#if\s+[^}]*errors' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 'aria-invalid|aria-describedby|aria-errormessage|mat-error|FormMessage|FormErrorMessage'
# 7. Status shown by colour alone: a colour chosen by a ternary (read each).
rg -n --pcre2 '\b(?:color|backgroundColor|background|borderColor)\s*:\s*[^,}\n]*\?\s*["\x27](?:#[0-9a-fA-F]{3,8}|rgb|hsl|var\()' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 8. ARIA misuse and focus order: positive tabindex (R03), role=button on a[href] (R04), role=presentation on a focusable (R05),
#    aria-hidden on a focusable (R06), aria-label on a generic element (R12), visual reorder (R19, read).
rg -n --pcre2 '\btab[iI]ndex\]?\s*=\s*(?:\{\s*|"\s*|\x27\s*)?[+]?0*[1-9]\d*\b' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '<a\b(?=[^>]*\bhref=)[^>]*\brole=["\x27]button["\x27]|<(?:button|input|select|textarea|a\b(?=[^>]*\bhref=))[^>]*\brole=["\x27](?:presentation|none)["\x27]|<(?:button|a|input|select|textarea)\b[^>]*\baria-hidden=(?:"true"|\x27true\x27|\{true\})' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '<(?:div|span|p)\b(?![^>]*\brole=)[^>]*\baria-label=' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'flex-direction\s*:\s*(?:row|column)-reverse|(?<![\w-])order\s*:\s*-?\d|\b(?:flex-row-reverse|flex-col-reverse|-?order-(?:first|last|\d+))\b|grid-auto-flow\s*:\s*[^;]*dense|\bgrid-flow-(?:row-|col-)?dense\b' "${C[@]}" "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 9. Composite widgets: files with a composite role and no key handler (9a); a stateful role with no state attribute (R13, JSX-aware, 9b).
rg -n --pcre2 '(?<![\[\w"\x27`-])role=["\x27](?:tablist|menu|menubar|listbox|combobox|grid|treegrid|tree|radiogroup)["\x27]' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | cut -d: -f1 | sort -u | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'onKeyDown|onKeyUp|@keydown|@keyup|\(keydown|\(keyup|on:keydown|onkeydown|addEventListener\(\s*["\x27]key|aria-activedescendant'
rg -n -U --pcre2 '<[\w.-]+\b(?='"$TB"'\srole=["\x27](?:tab|combobox|checkbox|switch|radio|menuitemcheckbox|menuitemradio)["\x27])(?!'"$TB"'\b(?:aria-selected|aria-expanded|aria-checked|aria-pressed)\b)(?!'"$TB"'\{\s*\.\.\.)'"$TB"'>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 10. Dragging: drag libraries in use (10a, read each for a single-pointer alternative); dnd-kit pointer sensor with no keyboard sensor (10b).
rg -l --pcre2 '@dnd-kit/|react-beautiful-dnd|@hello-pangea/dnd|react-dnd\b|vuedraggable|vue-draggable-plus|svelte-dnd-action|cdkDrag|sortablejs|\bdraggable=' "${J[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l0 --pcre2 'useSensor\(\s*PointerSensor' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match 'KeyboardSensor'
# 11. Input purpose and authentication: paste blocked (R07), password with autocomplete off (R08), personal-data input with no autocomplete (R09), CAPTCHA (R24).
rg -n --pcre2 'on[Pp]aste\s*=\s*\{[^}]*preventDefault|@paste\.prevent|\(paste\)\s*=\s*"[^"]*preventDefault|on:paste\|preventDefault|onpaste\s*=\s*["\x27]\s*return\s+false|addEventListener\(\s*["\x27]paste["\x27][^)]*preventDefault' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
PN='e-?mail|phone|tel|username|given-?name|family-?name|first_?name|last_?name|postal|zip|address\w*|organization|company(?:_?name)?|business_?name'
rg -n -U --pcre2 '<[iI]nput\b(?='"$TB"'\btype=["\x27]password["\x27])'"$TB"'\bauto[cC]omplete=["\x27](?:off|false)["\x27]|<[iI]nput\b(?='"$TB"'(?:\btype=["\x27](?:email|tel)["\x27]|\bname=["\x27](?:'"$PN"')["\x27]|\{\s*\.\.\.(?:\w+\.)*register\(\s*["\x27](?:'"$PN"')["\x27]))(?!'"$TB"'\bauto[cC]omplete=)'"$TB"'/?>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '<ReCAPTCHA\b|grecaptcha\.|hcaptcha|<HCaptcha\b|data-sitekey=|recaptcha/api\.js' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 12. Media: files with <video> and no captions track (12a); autoplay without controls (R10, 12b).
rg -l0 --pcre2 '<video\b' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '<track\b[^>]*kind=["\x27](?:captions|subtitles)'
rg -n --pcre2 '<(?:video|audio)\b(?=[^>]*\bauto[pP]lay\b)(?![^>]*\bcontrols\b)[^>]*>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 13. Content shown on hover (a handler that opens or shows something) in a file with no Escape handling and no tooltip library.
rg -l0 --pcre2 '(?:onMouseEnter|onPointerEnter|onMouseOver|@mouseenter|@mouseover|\(mouseenter\)|on:mouseenter|onmouseenter)\s*=\s*["{][^"}]*(?:set\w*(?:Open|Show|Shown|Visible|Hover\w*|Tooltip|Popover|Tip)\w*\(\s*(?:true|!0)|\b(?:show|open)\w*\(|(?:open|show|visible|hovered|isOpen)\w*\s*=\s*true)' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 'Escape|keydown\.esc|@radix-ui/react-(?:tooltip|hover-card|popover)|@floating-ui/|useDismiss|matTooltip|v-tooltip'
# 13b. A tooltip or hover-card trigger `asChild` onto a host that takes no focus: the tip is mouse-only and never reaches AT.
rg -n -U --pcre2 '<(?:TooltipTrigger|HoverCardTrigger)\b(?='"$TB"'\basChild\b)'"$TB"'>\s*<(?!(?:Button|button|a|Link|NavLink|input|select|textarea|summary|Toggletip)\b)[A-Za-z][\w.]*' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 14. Context change on input (A-28); timing: sign-out by timer (R23), idle libraries, meta refresh.
rg -n --pcre2 '(?:onChange|@change|\(change\)|onchange|on:change)\s*=\s*[{"\x27][^}"\x27]*(?:navigate\(|router\.push|\.submit\(\)|requestSubmit\(|location\.(?:href|assign))' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'setTimeout\(\s*(?:\(\)\s*=>|function)[^;]*\b(?:sign[oO]ut|log[oO]ut|logout|endSession|expireSession)\b|react-idle-timer|useIdle\(|@ng-idle/|http-equiv=["\x27]refresh' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a hit **plus** a read of the component **plus** the route that renders it **plus** the oracle. Three blind spots are structural, so work around them rather than trust a quiet grep:

- **Wrappers hide the element.** `<Button>`, `<IconButton>`, `<Clickable>` render the native tag one file away. Add the wrappers to `BTN` and to the jsx-a11y `components` map, and read each wrapper once. A defect in a wrapper is one finding for every call site.
- **Spread props hide attributes.** `{...props}` can supply `role`, `aria-label` or `onClick`. Greps 2 and 9b skip a tag with a spread. Treat a spread tag as `unknown`, settled by the render.
- **Runtime state is invisible.** Focus order, trapping, announcements and state changes exist only when the page runs. §4, §5, §6 and §9 hits are candidates for the keyboard path and the live-region oracle.

**Measured** (2026-10-05, the script above, about 1.5 s per tree):

| Tree | Hits that matter | Verdict |
|---|---|---|
| `benchmarks/fixtures/review-decoys/change/web` | 1 · 2c · 2d · 6d: one hit each | all four seeded RD-A11Y-01..04 caught; 0 hits on decoys RD-DEC-11..14 (labelled `×` button, `alt=""`, `<label htmlFor>`, `role="alert"`) |
| `benchmarks/fixtures/web-dashboard` | 2b, 2c, 2d one each; 1 one; 7 two | WEB-A11Y-01 (glyph `↩` button) and WEB-A11Y-02 (avatar `<img>` with no `alt`) caught. The §1 hit is a backdrop with Escape and a close button (`precedents/ui.md` § 16); the `stopPropagation` wrapper the first version flagged is excluded |
| `review-decoys/base/web` | 4: `Modal.tsx` | the base dialog the change later fixes |
| `slow-marketplace`, `vuln-fullstack`, `quality-mix`, `brittle-suite` | 2d 1 (a search input); 6b 1 (`{status && <p role="status">}`); 8 R12 1 (a rating `span` with `aria-label`) | candidates for the label query, the live-region oracle and axe (`precedents/ui.md` § 24) |
| research fixtures `A-rg/pos` / `neg` | every seeded positive caught (R01 8, R02 5, R03 5, R07 4, …) | 0 decoy hits, except 12a (it lists every `<video>` file; axe `video-caption` is needs-review) |
| real React 19 + Vite app, 1,979 `.tsx` | 0d (the riders, now `a11y-scan` grep 6): 0 · 1: 3 · 2a–2e: 0 · 3: 0 · 4: 0 · 6a: 1 file · 6d: 1 · 6e: 6 files · 8: 1 + 13 reorder · 9a: 19 files · 9b: 1 · 10a: 3 files · 12a: 2 files · 13: 0 · 14: 0 | §1: a click-to-focus tag input (ui § 16), a card row and an inbox row to read. 6e: one root cause — six integration dialogs render `{errors.x && <p>}` beside an unassociated input. 6a: a static notice (refuted on read). 6d: a price error with no role. 8: an image placeholder `div` named by `aria-label` with no role (axe decides). 9a: tab strips with no arrow keys (APG deviation, medium). 10a: two reorder lists are drag-only (native HTML5 DnD, no click or key path: real 2.5.7 candidates); the third has a click path. 12a: user-sent chat media |
| the same app on 2026-10-15, in a real NestJS + React monorepo | **2f: 14 labels, 11 true** (bare `<label>` captions beside `Input`s outside the kit `Field`; 3 refuted by the input's own `aria-label`) · **2g: 1, true** (an editor field's id from its label text, repeated per list row) · **13b: 9, all true** (`TooltipTrigger asChild` onto an icon, a `span` or a `Badge`) · 3a: 0 → 1 (`.focus-ring` sets `outline-style: none` + a shadow) · 2a with the wider `BTN`: 11, the 6 `<a>` under `<Button asChild aria-label>` marked `^` · 6a: 3 files, 2 marked as rendering a live-region component · 11b: 0 → 21 inputs (2 real on sign-up; most are staff entering other people's data, ui § 30) | all four classes were found only by reading before; every fixture count is unchanged |

Before hardening, the same real app returned **R02 26** (icon children mis-anchored by `[^>]*` across prettier-formatted JSX — 0 true), **R13 46** (single-line lookahead on multi-line tags, many in comments — 1 true), **R01 10** (6 `stopPropagation` wrappers, 1 comment), **6e 23** (prop `error={errors.x}` into a wiring `Field` wrapper — `precedents/ui.md` § 14), **13: 3** (prefetch and row-highlight hovers — ui § 33) and **0d: 2** (`<html>` inside comments; the riders grep now lives in `a11y-scan` as grep 6). The versions above are the fixed ones. Small fixtures prove the greps parse and catch seeded rows; precision at scale comes from the real-app row.

## The 3,000-hit path

1. **Intersect** with the route table: a component no route reaches is dismissed with one read. Storybook-only and design-system-internal files form their own group.
2. **Group** by (component or wrapper, pattern). A wrapper with the defect is one group however many call sites it has; fixing the wrapper closes them.
3. **Rank** by route traffic: RUM or analytics when present, else landing, auth, checkout-class, list and form routes first.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** Run `a11y-scan` (axe at every route × state) and the keyboard path across the route matrix once; one run confirms or refutes whole groups.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity is the WCAG impact on a reachable route: drop one step when an equivalent accessible path exists on the same page. Raise to **critical** only when the control is the sole path to a primary or destructive action, or it blocks sign-in or checkout.

| § | Class | WCAG 2.2 SC (level) | Lint rule ids (JSX · Vue · Angular · Svelte) | Default |
|---|---|---|---|---|
| 1 | Non-semantic interactive control | 2.1.1 (A), 4.1.2 (A) | `click-events-have-key-events`, `no-static-element-interactions`, `interactive-supports-focus` · same three · `click-events-have-key-events`, `interactive-supports-focus` · `a11y_click_events_have_key_events`, `a11y_no_static_element_interactions` | high when the sole path |
| 2 | Missing accessible name or label | 1.1.1, 1.3.1, 2.4.4, 3.3.2, 4.1.2 (A); 2.5.3 (A) | `alt-text`, `control-has-associated-label`, `anchor-has-content`, `label-has-associated-control`, `img-redundant-alt` · `alt-text`, `anchor-has-content`, `form-control-has-label` · `alt-text`, `elements-content`, `label-has-associated-control` · `a11y_missing_attribute`, `a11y_consider_explicit_label`, `a11y_label_has_associated_control` | critical on primary / destructive controls and auth inputs; else high |
| 3 | Focus indicator removed | 2.4.7 (AA) | stylelint `a11y/no-outline-none` | high on primary controls |
| 4 | Dialog / overlay focus not managed | 2.1.2 (A), 2.4.3 (A) | — | high; critical when focus is trapped |
| 5 | SPA route change: title, focus, announcement | 2.4.2 (A), 2.4.3 (A), 4.1.3 (AA) | — | medium; high when titles are identical |
| 6 | Status not announced; field error not associated | 4.1.3 (AA), 3.3.1 (A), 1.3.1 (A), 3.3.3 (AA) | — | high on transactional forms |
| 7 | Colour as the only signal | 1.4.1 (A) | — | medium |
| 8 | ARIA misuse, positive tabindex, visual reorder | 4.1.2 (A), 1.3.1 (A), 2.4.3 (A), 1.3.2 (A) | `aria-props`, `aria-proptypes`, `aria-role`, `no-aria-hidden-on-focusable`, `tabindex-no-positive` · `aria-props`, `aria-role`, `no-aria-hidden-on-focusable`, `no-role-presentation-on-focusable`, `tabindex-no-positive` · `valid-aria`, `no-positive-tabindex` · `a11y_positive_tabindex`, `a11y_unknown_role`, `a11y_unknown_aria_attribute` | high for `aria-hidden` on a focusable; medium |
| 9 | Composite widget without its keyboard model or state | 2.1.1 (A), 4.1.2 (A) | `role-has-required-aria-props`, `role-supports-aria-props` · `role-has-required-aria-props` · `role-has-required-aria` · `a11y_role_has_required_aria_props` | high for combobox / menu; medium for tabs reachable by Tab |
| 10 | Dragging with no single-pointer alternative | 2.5.7 (AA) | — | medium; high when reorder is the only way |
| 11 | Input purpose; accessible authentication | 1.3.5 (AA), 3.3.8 (AA), 3.3.7 (A) | `autocomplete-valid` · — · — · `a11y_autocomplete_valid` | high when paste is blocked on sign-in; low–medium for missing tokens |
| 12 | Media: captions, autoplay audio | 1.2.2 (A), 1.4.2 (A) | `media-has-caption` · `media-has-caption` · — · `a11y_media_has_caption` | medium |
| 13 | Hover or focus content not dismissible or hoverable | 1.4.13 (AA) | `mouse-events-have-key-events` (JSX, Vue, Angular) | medium |
| 14 | Context change on input; timing not adjustable | 3.2.1, 3.2.2 (A); 2.2.1 (A) | — (html-validate `meta-refresh`) | medium |

### 1. Non-semantic interactive control

```
BAD:   <div className="close" onClick={onClose}>×</div>          · <li v-on:click="pick(i)">  · <span (click)="go()">
GOOD:  <button type="button" aria-label={t('close')} onClick={onClose}><XIcon aria-hidden /></button>
```
**Read the code:** Is there a real `<button>` / `<a href>` child (delegation, `precedents/ui.md` § 34) or an equivalent control on the page? Is it a backdrop that also closes on Escape (ui § 16)? Does a handler come through spread props? **Finding when** the element is the path to an action and Tab cannot reach it. **Proof:** keyboard path (V87): the control is absent from the Tab sequence, or Enter / Space do nothing. Fix: the native element. `role="button"` + `tabIndex` + key handlers is the fallback, never the first choice.

### 2. Missing accessible name or label

```
BAD:   <button onClick={close}><XIcon /></button>   · <button>↩</button>   · <img src={avatar}>   · <input placeholder="Amount">
GOOD:  <button aria-label={t('close')}>…   · <img src={avatar} alt={name}> (alt="" when decorative)   · <label for="amt">…</label><input id="amt">
```
**Read the code:** Does the icon component render a `<title>` or visually hidden text? Does a wrapper wire `htmlFor` / `aria-labelledby` (ui § 14)? A 2f `<label>` that holds only text sits beside its control instead of naming it: is the control inside the project's `Field` wrapper (which wires the id), or named by its own `aria-label`? A 2g id built from label text collides as soon as a list renders the component twice (axe `duplicate-id-aria`; the fix is `useId`). A 2a link marked `^` sits under a `<Button asChild aria-label>`, which names it. Is the image decorative (ui § 11)? Is the name a translation key that resolves in every locale? **Finding when** the rendered control has no accessible name, or its name omits its visible label (2.5.3). **Proof:** role and label query (V88): `getByRole('button', { name: /close/i })` or `getByLabel('Amount')` finds nothing; axe `button-name` / `image-alt` / `label` at the route-state.

### 3. Focus indicator removed

```
BAD:   .btn:focus { outline: none; }        · className="focus:outline-none"     (no focus-visible ring on the line)
GOOD:  .btn:focus-visible { outline: 2px solid var(--focus-ring); }   · "focus-visible:outline-none focus-visible:ring-2"
```
**Read the code:** Is there a `:focus-visible` rule for the same element elsewhere, a ring from a wrapper class (`focus-ring`), or a `box-shadow` replacement (ui § 18)? Tailwind v4 `outline-none` sets `outline-style: none`; `outline-hidden` is the forced-colours-safe reset (ui § 55). Grep 3a reads `outline-style: none` too: a ring class that pairs it with a `box-shadow` draws nothing under forced colours (ui § 18, Low). **Finding when** a focusable element shows no visible change on keyboard focus. **Proof:** focus-visible delta (V89), normal and `forcedColors: 'active'`.

### 4. Dialog or overlay focus not managed

**Read the code:** Does opening move focus inside, Tab stay inside a modal, Escape close it, and closing return focus to the trigger? Native `<dialog>.showModal()` and headless dialogs provide these (ui § 12, ui § 13); a hand-rolled `role="dialog"` usually does not. **Finding when** any of the four fails. **Proof:** keyboard path (V90). Fix: the project's dialog primitive, or `showModal()`. Not `aria-hidden` on the page behind it.

### 5. SPA route change

**Read the code:** Which router (grep 5a)? Next App Router and SvelteKit announce route changes and Nuxt has an optional announcer (ui § 27). React Router, Vue Router and the Angular Router leave it to the app. Does every route set a distinct title (grep 5b), and does something move focus to the new heading or `main` after navigation? **Finding when** a client-side navigation leaves the title unchanged or focus on a removed element, and nothing announces it. **Proof:** keyboard path + live-region presence (V92), navigating by clicking a link.

### 6. Status not announced; field error not associated

```
BAD:   {error && <span style={{ color: 'red' }}>{error}</span>}          · {saved && <div role="status">Saved</div>}
GOOD:  <p id="amt-err" role="alert">{error}</p> + <input aria-invalid aria-describedby="amt-err">   · an always-mounted <div role="status">{msg}</div>
```
**Read the code:** Does the toast go through a library that owns a live region (ui § 26), or render a project component that does (6a marks the hit `renders <X>, a live-region component`: read X once, and check the region is mounted before the message)? Is the conditional element `role="alert"` (ui § 25, Low)? Does a shared field wrapper wire `aria-invalid` / `aria-describedby` (ui § 14)? Does focus move to the first invalid field or an announced summary? **Finding when** the message is not announced, or the error is not the input's accessible description. **Proof:** live-region presence (V93): `toHaveAccessibleErrorMessage` / `toHaveAccessibleDescription`; the status region exists before the action.

### 7. Colour as the only signal

**Read the code (read lane):** does the colour carry meaning — failed vs paid, a required field, a link in prose — with no text, icon or underline beside it? Most grep 7 hits are variant styling. **Finding when** the state is distinguishable only by hue. **Proof:** axe `link-in-text-block`; a greyscale screenshot (`filter: grayscale(1)` on `html`) attached for the human pass.

### 8. ARIA misuse, positive tabindex, visual reorder

**Read the code:** `aria-hidden` on a focusable, or on a container whose focusables are not also `inert` / `tabindex="-1"`? `role="presentation"` on a focusable? A positive `tabindex` (only positive counts, ui § 22)? `aria-label` on a generic element (trust axe `aria-prohibited-attr`, ui § 24)? A reverse or `order` layout whose focusables then tab out of visual order (not an RTL mirror, ui § 28)? **Finding when** the rendered tree misstates role, name, state or order. **Proof:** axe `aria-hidden-focus`, `aria-allowed-attr`, `tabindex` at the route-state; aria snapshot diff (V94).

### 9. Composite widget without its keyboard model or state

**Read the code:** Is the widget a headless primitive (ui § 12)? For a hand-rolled one, does it follow the APG pattern — arrows, Home / End, roving `tabindex`, `aria-selected` / `aria-expanded` / `aria-checked` that change on interaction? **Finding when** the role promises a model the widget does not implement. Tabs that are plain buttons reachable by Tab are medium (a 4.1.2 promise gap); a combobox or menu with no arrow keys is high. **Proof:** keyboard path + aria snapshot diff (V95).

### 10. Dragging with no single-pointer alternative

**Read the code:** Can the user reach the same result with clicks alone — move buttons, a menu, a position field? A keyboard sensor satisfies 2.1.1, **not** 2.5.7. A file drop zone with a "Browse" button passes. **Finding when** drag is the only pointer path. **Proof:** keyboard path + a click-only path (V96).

### 11. Input purpose and accessible authentication

```
BAD:   <input type="password" onPaste={(e) => e.preventDefault()}>   · <input type="password" autoComplete="off">   · <input type="email" name="email">
GOOD:  paste allowed · autoComplete="current-password" / "new-password" / "one-time-code" · autoComplete="email"
```
**Read the code:** Is the field about the user (ui § 30)? Grep 11b reads the kit `<Input>` and the name a form library registers (`{...register('username')}`) as well as `name=`; on an admin app most hits are staff typing someone else's data, which 1.3.5 does not cover. Is the CAPTCHA an allowed exception (ui § 31)? **Finding when** paste or password managers are blocked on a credential, or a personal-data field has no valid token. **Proof:** paste probe; axe `autocomplete-valid` (V97). Blocked paste and `autocomplete="off"` on a credential are static facts.

### 12. Media

**Read the code:** Is the video prerecorded with speech (captions required, 1.2.2) or decorative (ui § 32)? Does audio autoplay more than three seconds with no control? **Proof:** axe `video-caption` (needs review) and `no-autoplay-audio`; media emulation (V98).

### 13. Hover or focus content

**Read the code:** Does the content also open on focus? Can Escape dismiss it without moving focus, and can the pointer move onto it? Prefetch and row-highlight handlers show nothing (ui § 33). **13b:** a headless `TooltipTrigger asChild` (or `HoverCardTrigger`) merges onto its child, so a `<span>`, an icon or a `Badge` host takes no focus: the tip is reachable by mouse hover only and never exposed to AT (2.1.1 and 1.3.1 when the tip is the only telling; medium). Read whether the same text is on screen elsewhere, and whether the kit ships a focusable variant (a toggletip). **Finding when** shown content fails dismissible, hoverable or persistent, or a 13b tip is the only place the information lives. **Proof:** keyboard path (V99): Tab never reaches the trigger, no `role=tooltip` appears.

### 14. Context change on input; timing

**Read the code:** Does changing a `select` or a field navigate or submit before an explicit action, with no warning beforehand? Does a timer sign the user out with no warning and no way to extend (20-hour and real-time exceptions)? **Finding when** either happens on a reachable route. **Proof:** keyboard path (ArrowDown changes no URL) and clock fast-forward (V100).

## Proof

Each § names its oracle from [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states (variants V87–V100; rendered riders V101–V104 belong to `a11y-scan`). The test runs on a production build, at the route-state, asserts the **one** rule or behaviour the finding names, and **fails before the fix**. A test that passes on the unfixed code proves nothing: rebuild it until it fails. Fixes are accepted only when the same oracle goes green, the class variants pass, and no new axe rule id appears at the route-state. Never accepted as fixes: adding to `disableRules`, `aria-hidden` on the offender, an `outline: none` swapped for another invisible style, a `svelte-ignore` / `eslint-disable`, deleting the test.

## Output

```
a11y-code-scan — lanes: react 19.2 + jsx-a11y 6.10.2 (scratch eslint 9), tailwind 4.3; vue, svelte, angular absent
Context: router react-router 7.18 (no built-in announcer) · headless @radix-ui (13 packages) · field wrapper shared/ui/field.tsx wires aria-invalid/-describedby

Findings: 2 · Unconfirmed: 3

1. src/features/billing/components/AddCardDialog.tsx:62          [report-with-fix]   high
   §6 field error not associated (3.3.1 A, 1.3.1 A) — {errors.card_name && <p>…</p>} beside an <Input> with no
   aria-invalid / aria-describedby; same root cause in 5 sibling dialogs. Route /settings/billing → "Add card".
   Proof: e2e/a11y/add-card.spec.ts — submit empty → toHaveAccessibleErrorMessage(/required/) fails.
   Fix: render through the shared <Field error> wrapper (it wires both); one change per dialog, 6 locations.

2. src/features/orders/components/StatusTabs.tsx:90               [report-with-fix]   medium
   §9 tabs without the APG keyboard model (4.1.2 A) — role="tablist"/"tab" buttons, no arrow keys, every tab in the
   Tab order. Route /orders. Proof: keyboard path — ArrowRight on the selected tab moves nothing (V95).
   Fix: the project's Radix Tabs primitive.

3. src/shared/ui/card-list.tsx:156                                 [report-flagged]    high
   §1 clickable <li> with no role or key handler (2.1.1 A). Unproven link: whether the card holds a real link for
   the same action (ui § 17). Settling test: keyboard path on /customers (cards view) — the row is in the Tab sequence.

Verification: 41 candidates → 2 findings · 3 unconfirmed · 6 hardening · 0 pre-existing · 30 refuted
Automated floor only: the manual pass (screen reader, zoom, content) is not part of this run.

Class coverage (WCAG 2.2 AA):
  §1  non-semantic control        checked (3 hits + 17 lint → 0 findings, 1 unconfirmed; 14 stopPropagation/forwarding)
  §2  names and labels            checked (0 hits + 22 lint → 0 findings; htmlFor-labelled inputs)
  §3  focus indicator             checked (0 hits; every outline-none line carries focus-visible:ring)
  §4  dialog focus                checked (0 files without a focus primitive; Radix dialog)
  §5  route change                checked (react-router: 14 title sites, focus moved in the app shell → read, 0 findings)
  §6  status / error              checked (1 file + 1 hit + 6 files → 1 finding, 6 locations; the custom notice is static)
  §7  colour only                 checked (0 hits)
  §8  ARIA / tabindex / order     checked (14 hits → 0 findings; 13 reorder lines are responsive or RTL layouts; 1 named div → axe decides)
  §9  composite widgets           checked (19 files → 1 finding; Live, unreviewed (17 groups / 17 files — continue with grep 9a))
  §10 dragging                    checked (3 files → 2 unconfirmed: drag-only reorder lists; settle with a click-only path)
  §11 input purpose / auth        checked (0 hits)
  §12 media                       checked (2 files → 0 findings: user-sent chat media, Hardening)
  §13 hover content               checked (0 hits)
  §14 context change / timing     checked (0 hits)
  riders                          not this skill — zoom, lang, orientation are a11y-scan grep 6; contrast, target size, reflow, obscured are a11y-scan
```

`[report-with-fix]`: the source line, the route and a failing oracle are all present, and the fix is a local change in the project's own components. `[report-flagged]`: one link is unproven (no harness, a wrapper not read, a spread prop), and the row names that link and the settling test. The coverage block lists **all fourteen** classes on every run: `checked (k hits → m findings)` only when the grep and lint lane ran on a present stack; `N/A (<reason>)` only when the repo has no such surface (no dialogs, no media, no drag); `blocked (<reason>)` when a grep failed or a lint lane could not install. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (accessibility § 11–34, versions § 49–57, § 102) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10 (the accessibility column). The ones this skill meets most:

- **Headless and native primitives** own role, state and keyboard (ui § 12, ui § 13). A shared field wrapper owns label and error wiring (ui § 14).
- **`stopPropagation`-only and click-to-focus wrappers, backdrops with Escape** (ui § 16), and **cards with an inner link** (ui § 17) are not controls.
- **`alt=""` on decoration** (ui § 11), **`role="alert"` mounted with its text** (ui § 25), **toast libraries** (ui § 26), **built-in route announcers** (ui § 27), **RTL reorder** (ui § 28).
- **Lint advice is not an SC failure**: `prefer-tag-over-role`, `no-autofocus` in a dialog (ui § 3, ui § 23).
- **A link rendered through `<Button asChild aria-label>`** takes the parent's name (ui § 102); grep 2a marks it `^`.

## When to run

- On any diff that adds or changes a component, template, stylesheet, form, dialog, menu, route or a design-system wrapper.
- On every whole-repo `/a11y-audit`, reporting all fourteen classes, before `a11y-scan` renders the routes. The two are complements, never substitutes.
- Before a release with an accessibility claim (EAA, a VPAT, a procurement questionnaire), and after a design-system or lint-plugin upgrade.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the source `<file:line>`, the route that renders it, the WCAG 2.2 SC and level, and the fix in the project's own components.
- Do not mark a finding `[report-with-fix]` without an oracle that failed, unless the class is a static fact (`precedents/ui.md`, the proof rule).
- Do not report a grep hit or a lint message as a finding. Do not report an AAA criterion or a house target as an AA failure (ui § 4).
- Do not print "accessible", "compliant", "WCAG AA ✓" or "no issues found". Print the coverage block and the automated-floor line; a class whose grep or lint lane did not run is `blocked`, never `checked`.
- Do not propose `aria-hidden`, `disableRules`, a suppression comment or a wider `exclude` as a fix.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `a11y-scan` (this pack) — the rendered half: axe per route × state × theme, contrast, target size, reflow, focus obscured. Run it after this skill on the same routes.
- `/frontend-audit` (this pack) — dispatches this skill and folds its coverage block into the A11y static row of the class ledger; `/a11y-audit` is its `--classes=a11y` preset. `/frontend-fix` closes the findings.
- `routing-scan` §1 (this pack) — the routing half of a click-navigation `div`.
- `@ux-reviewer` (ui-ux pack, when installed) — the WCAG judge; `@accessibility-auditor` (this pack) is the judge without ui-ux, and keeps the manual keyboard and screen-reader checklist.
- `ui-design-sweep` verbs 12, 13, 16 and 18, `design-token-audit` and `motion-audit` (ui-ux pack, when installed) — the visual fixes, contrast values and motion. Without ui-ux, those rows print `N/A (owner pack ui-ux not installed)`.
- `xss-scan` (security pack, when installed) — markup sinks; never reported here.
