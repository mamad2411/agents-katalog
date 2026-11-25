---
name: motion-audit
description: "Motion detector: transition-all, layout-triggering animation, missing reduced-motion branches, off-scale durations, auto-moving content, infinite loops — proved by an animated-property census and reduced-motion emulation."
kind: skill
pack: ui-ux
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: motion-audit

## Premise

Animations are where polish lives, and where battery drains, where `prefers-reduced-motion` is ignored, and where 60 fps becomes 30 fps without anyone noticing. A `transition: all` animates a width nobody meant to animate. A progress bar that animates `width` relayouts every frame. A carousel that never stops is a Level-A failure for anyone who cannot read moving text. This skill walks the project's motion surface — CSS, Tailwind, Motion for React, GSAP, Web Animations, Lottie, native drivers — and names each defect by the property that moves and the trigger that moves it.

"Feels janky" is the symptom that prompts the audit, not a finding. **Every finding cites the animation declaration's `<file:line>` + the property and trigger + the route that runs it + the proof + the fix.** A grep hit is never a finding by itself. "No motion issues" is never printed without the class-coverage block (§ Output).

**This skill does NOT own the numbers.** The duration bands, the frequent-action ceiling (> 400 ms is a finding), the absolute ceiling (> 500 ms is forbidden for non-decorative UI motion), the easing classes and the reduced-motion policy come from [`motion.md`](../../ai-patterns/motion.md) § The duration scale. The project's own resolved motion tokens come first when it declares them (grep 0c); `motion.md` is the seed when it does not. A threshold printed here that disagrees with either is drift, and they win. This skill prints no duration or easing value of its own.

Below, `ui § n` means [`precedents/ui.md`](../../../../snippets/precedents/ui.md) § n; a bare `§n` is a detector in this skill.

## The rule

A candidate is a finding when all four hold:

1. **It runs.** A route or screen mounts the element and a real trigger fires the animation: mount, hover, press, scroll, a state change, a timer.
2. **The property or the trigger is the defect.** It animates a layout or paint property, it has no reduced-motion branch for its trigger, its duration is off the scale or over a ceiling, it moves on its own with no pause, or it never stops.
3. **Nothing already handles it.** No global reduced-motion reset covers it, no library-level setting turns it off, no token supplies the value.
4. **The oracle fired, or it is a static fact.** A literal duration or easing with the token named is a static fact. Everything else needs the census, the emulation run or a profile (§ Proof).

## Boundaries

- **Conformance level, stated correctly.** Interaction-triggered motion is **WCAG 2.2 SC 2.3.3 Animation from Interactions — Level AAA**. What binds below AAA is narrower: **SC 2.2.2 Pause, Stop, Hide — Level A**, for content that starts automatically, lasts more than five seconds and is presented in parallel with other content, unless essential. So an auto-playing carousel past 5 s beside other content is a **Level-A failure** (§5), while a parallax hero with no reduced-motion branch is a **house-rule violation with a AAA criterion named** (§3), reported under the rule `motion.md` declares. Reporting the latter as "fails WCAG 2.2 AA" is false and discredits the rest of the report (`ui § 4`). `prefers-reduced-motion` is the mechanism, not the criterion.
- **Autoplay audio and media captions** stay with `a11y-code-scan` §12 (frontend pack, when installed); axe's `blink` and `marquee` rules with `a11y-scan` §1. Moving content (2.2.2) is this skill's §5. Without the frontend pack, those rows print `N/A (owner pack frontend not installed)` and §5 still runs.
- **The cost of an animation** (frames dropped, INP) is the performance pack's when installed (`inp-responsiveness` cites §2 here for the class); this skill proves the property class and points to the profile. A `requestAnimationFrame` loop or animation subscription never cancelled on unmount → `render-correctness-scan` §2 (frontend pack, when installed).
- **Duration and easing tokens as part of the token system** are this skill's; colour, spacing and type tokens are `design-token-audit`'s.
- **Native drivers** (React Native Reanimated / Animated, Flutter, Compose, SwiftUI) run grep-only here. The platform's reduce-motion API and off-main-thread driver belong to the mobile pack's `references/<framework>.md` when it is installed; this skill audits the property class and the trigger, not platform APIs.

## Adapt to the codebase — lane table

Read each animation library **and its version** from the lockfile and print the lanes you ran in the output header. Per animation, record the trigger, the duration, the easing, and **which property animates** — the last decides most findings.

| Lane | Where motion is declared (greps 1–7) | Reduced-motion handling the run looks for (grep 0b) |
|---|---|---|
| **CSS / SCSS** | `transition`, `animation`, `@keyframes`, `will-change`, View Transitions | `@media (prefers-reduced-motion: reduce)` — a global reset covers CSS only |
| **Tailwind** (+ `tw-animate-css` / `tailwindcss-animate`) | `transition-*`, `duration-*`, `ease-*`, `animate-*`, `animate-in` / `slide-in-from-*` | `motion-reduce:` / `motion-safe:` variants, or the global reset |
| **Motion for React** (`motion/react`; formerly Framer Motion) | `animate`, `initial`, `exit`, `whileHover`, `layout`, `transition={{ duration }}`, `useScroll` / `useTransform` | `useReducedMotion()`, `<MotionConfig reducedMotion="user">` — verify what it disables with the emulation oracle, never from memory |
| **GSAP, anime.js, react-spring, Web Animations** | `gsap.to/from/fromTo`, `ScrollTrigger`, `el.animate([...])`, `useSpring` | `gsap.matchMedia()`, a `matchMedia('(prefers-reduced-motion: reduce)')` read |
| **Vue / Svelte / Angular** | `<Transition>`, Svelte `transition:` / `animate:`, Angular animation triggers | the global reset (these compile to CSS or WAAPI); a `matchMedia` read |
| **Lottie, Rive, video, carousels** (Swiper, Embla, Splide, keen-slider, slick) | `loop`, `autoplay`, `Autoplay()` plugin, `<video autoplay>` | a pause control; autoplay off under reduce |
| **Native** (grep-only) | Reanimated / `Animated`, Flutter `AnimationController`, Compose `animate*AsState`, SwiftUI `withAnimation` | the platform's reduce-motion signal named in the mobile pack's references |

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`"${ROOTS[@]}"`); any rg error (exit 2) is a failed grep, never zero hits. File-level greps use `--files-without-match` — never `rg -L`, which is `--follow`.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|lit|react-native)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,coverage,storybook-static,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,__fixtures__,playwright,cypress,scripts,tools}/**' -g '!**/*.{test,spec,stories,story,e2e,cy,mock}.*' -g '!**/*.{test-data,fixture,fixtures}.*'
   -g '!*.{md,mdx,snap,map,lock,json,yml,yaml,svg}' -g '!**/{locales,locale,i18n,translations,docs,vendor}/**' -g '!/ai/**' -g '!**/*.min.*')
U=(-g '*.{css,scss,sass,less,pcss,js,jsx,ts,tsx,mjs,vue,svelte,astro,html}'); S=(-g '*.{css,scss,sass,less,pcss,vue,svelte,astro}'); J=(-g '*.{js,jsx,ts,tsx,vue,svelte,astro}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--)')   # drops comment-only lines
LP='width|height|min-width|max-width|min-height|max-height|top|right|bottom|left|inset[\w-]*|margin[\w-]*|padding[\w-]*|font-size|line-height|letter-spacing|border(?:-[\w-]+)?-width|gap|grid-template[\w-]*|flex-basis'
# 0a lanes and versions; 0b reduced-motion handling (a global CSS reset covers CSS only); 0c the project's motion tokens.
rg -n --no-heading --pcre2 '"(?:motion|framer-motion|@react-spring/\w+|react-spring|gsap|animejs|@formkit/auto-animate|lottie-web|lottie-react|@lottiefiles/[\w-]+|@rive-app/[\w-]+|tw-animate-css|tailwindcss-animate|@angular/animations|react-native-reanimated|moti|swiper|embla-carousel[\w-]*|@splidejs/[\w-]+|keen-slider|react-slick|vue3-carousel|recharts|chart\.js|echarts|@nivo/[\w-]+|victory|apexcharts|highcharts|tailwindcss)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --pcre2 'prefers-reduced-motion|\buseReducedMotion\w*\b|<MotionConfig\b[^>]*reducedMotion|\breducedMotion\s*[:=]|\bmotion-(?:reduce|safe):|gsap\.matchMedia|isReduceMotionEnabled|reduceMotionChanged|disableAnimations|accessibilityReduceMotion|ReduceMotion\.' "${U[@]}" -g '*.{dart,swift,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 -e '^\s*--(?:duration|ease|easing|motion|animate|transition)[\w-]*\s*:' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 1. transition: all, a bare duration (whose property defaults to all), Tailwind transition-all.
rg -n --pcre2 '(?<![\w-])transition\s*:\s*(?:all\b|[\d.]+m?s\b)|\btransition\s*:\s*["\x27\x60](?:all\b|[\d.]+m?s\b)|(?<![\w-])transition-all\b' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. A layout or paint property animated: 2a transitions and permanent will-change; 2b @keyframes that move one; 2c JS libraries.
rg -n --pcre2 '(?<![\w-])transition(?:-property)?\s*:[^;{}]*?(?<![\w-])(?:'"$LP"'|box-shadow|filter|backdrop-filter)\b|(?<![\w-])transition-\[[^\]]*(?:'"$LP"'|box-shadow|filter)|\bwill-change\s*:\s*(?!auto\b)|(?<![\w-])will-change-(?!auto\b)[\w-]+' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '@keyframes\s+[\w-]+\s*\{(?:\s*(?:from|to|[\d.]+%)(?:\s*,\s*(?:from|to|[\d.]+%))*\s*\{[^{}]*\})*?\s*(?:from|to|[\d.]+%)(?:\s*,\s*(?:from|to|[\d.]+%))*\s*\{[^{}]*?(?<![\w-])(?:'"$LP"'|box-shadow|filter|backdrop-filter)\s*:' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '@keyframes'
rg -n --pcre2 '\b(?:animate|initial|exit|whileHover|whileTap|whileInView)\s*=\s*\{\{[^}]*\b(?:width|height|top|left|right|bottom|margin\w*|padding\w*|fontSize|filter|boxShadow)\s*:|\bgsap\.(?:to|from|fromTo)\([^)]*\b(?:width|height|top|left|margin\w*|padding\w*|fontSize|filter)\s*:|\.animate\(\s*\[?\s*\{[^}]*\b(?:width|height|top|left|margin\w*|padding\w*)\s*:' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3. Files that drive motion from JS or scroll and read no reduced-motion signal (a CSS reset does not reach these).
#    Chart libraries animate in JS by default (Recharts on mount and on every data change); an explicit animation switch
#    in the file (`isAnimationActive`, `animation: false`, `animate={false}`) is read as handled.
rg -l0 --pcre2 'from\s+["\x27](?:motion/react|framer-motion|motion|gsap[\w/]*|@react-spring/\w+|react-spring|animejs|lottie-react|lottie-web|@lottiefiles/[\w-]+|@rive-app/[\w-]+|recharts|chart\.js[\w/]*|react-chartjs-2|echarts[\w/-]*|@nivo/[\w-]+|victory[\w-]*|(?:react-)?apexcharts|highcharts[\w/-]*)["\x27]|\.animate\(\s*[\[{]|\bScrollTrigger\b|\buseScroll\b|animation-timeline\s*:|\bscroll-timeline' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 'prefers-reduced-motion|useReducedMotion|reducedMotion|motion-reduce:|motion-safe:|gsap\.matchMedia|\bisAnimationActive\b|\banimation\s*:\s*false\b|\banimate=\{false\}|\banimations\s*:\s*\{\s*enabled\s*:\s*false'
# 4. A literal duration, delay or easing outside a token definition; then the spread of Tailwind durations in use.
rg -n --pcre2 '(?<![\w-])(?:transition|animation)(?:-duration|-delay)?\s*:(?![^;{}]*var\(--)[^;{}]*?(?<![\w.-])(?!0?\.0\d*m?s\b)(?!0m?s\b)\d*\.?\d+m?s\b|cubic-bezier\(|(?<![\w-])(?:duration|delay|ease)-\[[^\]]+\]' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | rg -v --pcre2 '^[^:]+:\d+:.*--[\w-]+\s*:\s*(?:[\d.]+m?s|cubic-bezier)'
rg -o --no-filename --pcre2 '(?<![\w-])duration-(?:\d+|\[[^\]]+\])' -g '*.{jsx,tsx,js,ts,vue,svelte,astro,html}' "${X[@]}" "${ROOTS[@]}" | sort | uniq -c | sort -rn
# 5. Content that moves on its own: autoplay carousels and video, marquee, infinite CSS animation, endless JS repeats;
#    5b a hand-rolled carousel (`setInterval` stepping an index modulo the count) or an AUTOPLAY/AUTO_ADVANCE constant.
rg -n --pcre2 '\bauto[pP]lay\b\s*(?:[:=]\s*(?:\{|true|\d|["\x27])|(?=[\s>/]))|\bAutoplay\(|\bAutoScroll\(|<marquee\b|\banimation(?:-iteration-count)?\s*:[^;{}]*\binfinite\b|\brepeat\s*:\s*(?:Infinity|-1)\b|\banimate-(?:marquee|scroll|ticker)\b' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 'setInterval\(\s*(?:\([^)]*\)\s*=>|function\s*\([^)]*\))\s*\{?\s*\w*\(\s*\(?\s*(\w+)\s*\)?\s*=>\s*\(?\s*\1\s*[+-]\s*1\s*\)?\s*%|\b[A-Z_]*AUTO_?(?:PLAY|ADVANCE|ROTATE|SLIDE)[A-Z_]*\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6. Over the frequent-action ceiling: CSS > 400 ms, Tailwind duration-500 and up, JS durations 0.41–9 s or 401–2999 ms
#    (toast display times of 3 s and more are not animation; read the call).
rg -n --pcre2 '(?<![\w-])(?:transition|animation)(?:-duration)?\s*:[^;{}]*?(?<![\w.-])(?:(?:[5-9]\d\d|4\d[1-9]|4[1-9]\d|\d{4,})ms|(?:0?\.(?:4[1-9]|4\d[1-9]|[5-9]\d*)|[1-9]\d*(?:\.\d+)?)s)\b|(?<![\w-])duration-(?:500|700|1000|\[(?:(?:[5-9]\d\d|4[1-9]\d|\d{4,})ms|[\d.]+s)\])\b|\bduration\s*:\s*(?:0?\.(?:4[1-9]|[5-9])\d*|[1-9](?:\.\d+)?|(?:4[1-9]\d|[5-9]\d\d|[12]\d{3}))\b' "${U[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7. Infinite animation (read: does it stop when its content loads or its view hides?).
rg -n --pcre2 '(?<![\w-])animate-(?:spin|ping|pulse|bounce)\b|\bloop\s*(?:=\s*\{?\s*true|:\s*true)\b|\brepeat\s*:\s*Infinity\b' -g '*.{jsx,tsx,js,ts,vue,svelte,astro,html}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a grep hit **plus** the trigger read **plus** the reduced-motion path read **plus** the route that runs it. Two blind spots are structural: a JS animation driven by `requestAnimationFrame` or a scroll listener names no property a grep can see — read every file grep 3 lists — and a class string assembled in `cn(...)` / `cva(...)` across lines is read, not grepped.

**Measured** (2026-10-05). On a seeded pos/neg set (CSS, TSX with Motion for React, a Swiper carousel, an autoplay video, a toast call) every grep parses and catches each positive; the decoys — `transition: transform 150ms`, an opacity keyframe, `motion-reduce:transition-none`, a `useReducedMotion` file, the `0.01ms` reduced-motion reset, a 5 s toast `duration` — are skipped by greps 1, 2, 3, 6. The 12 `benchmarks/fixtures` trees of that date carry no motion, and every grep returns 0 there. On a read-only real React 19 + Tailwind 4 + `tw-animate-css` application, the script runs in about a second:
- 0b: one global reduced-motion reset in the main stylesheet plus one `matchMedia` read for smooth scroll, so grep 3 is 0.
- 0c: the project's own scale, `--duration-fast/base/slow` = 150/200/300 ms and `--ease-standard`. Its `base` is 200 ms against `motion.md`'s 250 ms token, inside `motion.md`'s 200–300 ms band. The project's scale is the one to cite.
- 1: 8 `transition-all` (progress fills and selectable cards). 2: 8, of which 6 are `transition-[width]` on progress fills and a collapsing sidebar.
- 4: 6, including a 5000 s autofill-background transition, the browser-autofill workaround (a precedent).
- 5: 1, the reset's own spinner exception.
- 6: 8 before reading. A first version counted 3 toast display times (`duration: 5000`, `8000`); the ms range now stops at 2999.
- 7: 20, mostly skeleton `animate-pulse` and spinner `animate-spin` inside loading branches.

**Re-measured 2026-10-15** on the same app inside a real NestJS + React monorepo. Grep 3 went from 0 to 9: the nine Recharts files animate on mount and on every filter change, out of reach of the CSS reset, and none sets `isAnimationActive` (an Unconfirmed until the installed defaults are read). Grep 5b returns the one hand-rolled banner carousel (`setInterval` stepping `(s + 1) % count` every 5 s, no pause), a high 2.2.2 row that grep 5 missed and only reading had found. On `benchmarks/fixtures/a11y-states`, grep 3 goes from 2 to 7 (both seeded rows, a parallax hero and a count-up KPI, still hit; the five additions are its Chart.js and Recharts files), and `quality-mix` and `slow-marketplace` each add their one chart file (Recharts, ECharts).

## The 3,000-hit path

1. **Intersect** with the route table; dismiss in one read each: a DS primitive's own motion (one group per primitive), the reduced-motion reset itself, story-only files.
2. **Group** by (property class, trigger, wrapper). A progress component animating `width` is one finding with N call sites; fixing the primitive closes them (`ui § 9`).
3. **Rank** by trigger frequency: hover and press on list rows and buttons, scroll-linked and parallax, then mount and route transitions, then decorative.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** One census per route (§ Proof) lists every running animation with its real property and duration — a `transition: all` resolves to what actually moves — and one emulation pass under `reducedMotion: 'reduce'` lists everything still moving. One run confirms or refutes whole groups.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity is the class default below; one step higher when the trigger is a frequent action or a primary route, one step lower for decorative motion off the primary flow. A performance severity ("drops to 30 fps") needs a profile artifact (§ Halt conditions); without one the row is medium and `[report-flagged]`.

| § | Class | Standard | Default |
|---|---|---|---|
| 1 | `transition: all` (and a bare duration whose property defaults to all) | — | low; medium when the census shows a layout property moving |
| 2 | Layout- or paint-triggering property animated; shaded `filter` / `backdrop-filter`; permanent `will-change` | — | medium; high on a frequent interaction or a large area, profiled |
| 3 | Interaction- or scroll-triggered motion with no reduced-motion branch | 2.3.3 (AAA) as a house rule | medium; high for vestibular triggers (parallax, zoom, scroll-linked) |
| 4 | Duration, delay or easing literal off the project's scale | — | low |
| 5 | Content that moves on its own > 5 s beside other content, with no pause | 2.2.2 (A) | high |
| 6 | Duration over the frequent-action ceiling (> 400 ms), or non-decorative motion over 500 ms | `motion.md` § The duration scale | medium |
| 7 | Infinite animation that never stops (shimmer over loaded data, a spinner on a hidden view, a looping composition) | — | medium (battery, main thread); low when decorative and paused offscreen |

### 1. `transition: all`

```
BAD:   .card { transition: all .3s }   ·   transition: 300ms   ·   className="transition-all hover:shadow-md"
GOOD:  transition: opacity var(--duration-base) var(--ease-out)  ·  Tailwind `transition` / `transition-colors` (curated lists)
```
`all` animates properties nobody intended, including ones added later, and is the commonest source of accidental layout animation. **Read the code:** what actually changes on this element's trigger — a colour, a shadow, a width? **Finding when** the census shows a property outside the intended set moving, or a layout property moving at all. **Proof:** the census on the trigger.

### 2. Layout- or paint-triggering property animated

```
BAD:   .bar { transition: width 200ms }  ·  @keyframes grow { to { width: 100% } }  ·  <motion.div animate={{ height }}>
       transition: filter 300ms on a full-bleed blur  ·  will-change: transform on every card, permanently
GOOD:  transform: scaleX() with transform-origin  ·  opacity  ·  a stacked shadow layer whose opacity animates
```

| Class | Properties | Verdict |
|---|---|---|
| **Composited** | `transform` (translate, scale, rotate), `opacity` | Cheap — the default target |
| **Composited but shaded per frame** | `filter` (especially `blur()`), `backdrop-filter` | **Measure, never assume.** Cost scales with the animated area; a large animated blur is routinely the most expensive thing on the page. "It's GPU-accelerated" is a hypothesis to profile, not a pass |
| **Triggers layout or paint** | `width`, `height`, `top` / `left` / `right` / `bottom`, `margin`, `padding`, `font-size`, `line-height`, `border-width`, `box-shadow` | Expensive. For `box-shadow`, animate `opacity` on a stacked shadow layer instead of repainting the shadow every frame |

The stack-neutral rule: an animation is cheap when it runs on the compositor without asking the main or UI thread for a new layout each frame. Every platform spells "off the main thread" differently; this skill audits the property class and leaves the mechanism to the platform reference. **Read the code:** does the animation legitimately need layout (a height-auto accordion with no known height)? Flag it for review rather than forcing `transform`. Is `will-change` set only while animating? **Finding when** a layout or paint property animates on a reached trigger. **Proof:** the census names the property; a cost claim adds a trace (§ Proof).

### 3. No reduced-motion branch

```
BAD:   a parallax hero driven by useScroll with no useReducedMotion  ·  gsap ScrollTrigger with no gsap.matchMedia()
GOOD:  @media (prefers-reduced-motion: reduce) { … } covering CSS  ·  useReducedMotion() swapping the move for a cross-fade
```
**Gate on the trigger, not on the duration.** Interaction- and scroll-triggered motion — parallax, zoom, scale, scroll-linked, autoplay — respects reduced motion whatever its duration. A duration threshold applies only to incidental transitions: one longer than the project's `base` token with no reduce branch is a finding. A global CSS reset covers CSS animation and nothing driven from JS, chart libraries included: Recharts, Chart.js, ECharts, Nivo and ApexCharts tween marks in JS by default, on mount and on each data change. Read the installed version's default before claiming it (the `isAnimationActive` / `animation` default and duration). **Read the code:** which trigger runs it? Does the reset or a library-level setting cover it, and does the replacement keep the state change visible (a cross-fade, not a cut to nothing)? **Finding when** a reached interaction- or scroll-triggered animation still moves under `reducedMotion: 'reduce'`. Report it as the house rule `motion.md` declares, naming 2.3.3 (AAA) — never as an AA failure. **Proof:** reduced-motion emulation.

### 4. Off-scale duration or easing literal

```
BAD:   transition: opacity 280ms cubic-bezier(.3,.7,.4,1)  ·  duration-[320ms]  ·  seven distinct durations in use
GOOD:  var(--duration-base) var(--ease-out)  ·  the project's duration-* utilities mapped to its scale
```
**Read the code:** does the project declare a scale (grep 0c)? Then the literal maps to the nearest step. With none, the finding is "no motion token scale" and the proposal is `motion.md` § The duration scale as the seed — never a set of numbers invented in this run. **Finding when** a reached animation hardcodes a value the scale holds, or the distinct-duration spread shows the same trigger timed differently across the app. **Proof:** static (the literal and the scale step, both cited).

### 5. Content that moves on its own

```
BAD:   <Swiper autoplay={{ delay: 3000 }} loop>  with no pause  ·  a news ticker with `animation: scroll 20s linear infinite`
GOOD:  a visible pause / stop control that stops it  ·  autoplay off under reduce  ·  muted video ≤ 5 s, or a video with controls
```
A hand-rolled carousel is a `setInterval` that steps an index (grep 5b); the CSS reset never stops a JS timer, and prev / next / dots that change the slide without clearing the timer are not a pause. **Read the code:** does it start automatically, last more than 5 s, and sit beside other content? Is it essential (a progress indicator)? Is there a pause control, and does it stop the motion? **Finding when** all three conditions hold and no mechanism stops it. 2.2.2 is Level A: this is a conformance failure, not a house rule. **Proof:** under default motion the content is still moving after 6 s and the pause control (if any) does not stop it; under reduce the carousel index is unchanged after 6 s.

### 6. Over the frequent-action ceiling

```
BAD:   duration-700 on a row's hover  ·  a filter chip that animates for 600 ms on every toggle
GOOD:  `fast` / `base` for micro-interactions and UI transitions; `slow` only for page or view changes
```
**Read the code:** is the trigger a frequent action (button, row, filter, toggle) or a page or view transition? Is the motion decorative? **Finding when** a frequent action's motion exceeds the frequent-action ceiling, or non-decorative motion exceeds the absolute ceiling, both from `motion.md` § The duration scale (or the project's scale). **Proof:** static, plus the census's `duration` when the value is computed at run time.

### 7. Infinite animation that never stops

```
BAD:   a shimmer still pulsing over a list that already arrived  ·  a Lottie `loop` mounted on a hidden tab  ·  a spinner on a backgrounded screen
GOOD:  the skeleton unmounts when data arrives  ·  the loop pauses offscreen or when the view hides
```
**Read the code:** is the infinite animation inside the loading branch only? Is a looping composition paused or destroyed when its view leaves the screen? **Finding when** the census shows an infinite animation running on content that has loaded, or on a view the user cannot see. **Proof:** the census after the data arrives (`iterations === Infinity`, `playState === 'running'`). A composition never destroyed on unmount is `render-correctness-scan` §2 when the frontend pack is installed.

## Proof

Run on a production build at the route-state that triggers the animation. Both oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states: reduced motion is *Geometry, reflow and media* (Motion, variant list V98), and the census is *Animation census* (V143) — `document.getAnimations()` mapped to kind, name, the properties that really move, duration, iterations and play state. rAF-driven JS motion is invisible to it: prove those with a trace. Per class:

- **§1 / §2:** trigger the hover, press or state change, then census → a layout property in `props` fails first.
- **§3 / §5:** `page.emulateMedia({ reducedMotion: 'reduce' })`, reload, trigger; the census filtered to running animations longer than 200 ms must be empty; a carousel's index is unchanged after 6 s.
- **§7:** wait for the data marker; the census filtered to `iterations === Infinity && state === 'running'` must be empty.

**Fails first:** the census lists the property, the duration or the still-running loop before the fix, and does not after it, at the same route-state. **A cost claim** (frames dropped, a long task) needs a trace or profile file from the platform's own tool, on a mid-tier device profile (CPU throttled), cited by path. A frame rate nobody recorded is not a measurement.

**Whole-class variants** (V98 plus): CSS transition, CSS keyframes, Tailwind utility, Motion for React, GSAP, Web Animations, Vue / Svelte transitions, View Transitions, Lottie / Rive, an autoplay carousel, parallax and scroll-linked motion, smooth scroll; the same trigger by hover, press, focus and keyboard; light and dark; the mobile width.

## Output

```
motion-audit — lanes: tailwind 4.3 + tw-animate-css 1.4 (apps/web/package.json); motion, gsap, lottie absent
Context: reduced-motion reset src/index.css:2277 (CSS only) · project scale fast 150 / base 200 / slow 300 ms,
  ease-standard (src/shared/theme/theme.css:439–442) — cited instead of motion.md's seed

Findings: 1 · Unconfirmed: 1

1. src/shared/ui/progress-bar.tsx:72                                [report-with-fix]   medium
   §2 layout property animated — the fill transitions `width`; 6 call sites through the primitive.
   Route /orders/import (bulk import). Proof: census on progress 20 → 60 % — CSSTransition `width`, 200 ms.
   Fix: animate transform: scaleX(var(--p)) with origin inline-start; one change in the primitive.

2. src/features/integrations/components/PlatformWebhookInfo.tsx:58  [report-flagged]    medium
   §6 over the ceiling — duration-700 on a card's mount animation. Unproven link: whether the panel opens
   on a frequent action or once per visit. Settling probe: census on /integrations after the second open.

Verification: 23 candidates → 1 finding · 1 unconfirmed · 5 hardening · 0 pre-existing · 16 refuted
Profiled: 0 of 0 cost claims · reduced motion: emulation run on 3 routes (no JS-driven motion to cover)

Class coverage:
  §1  transition: all          checked (8 hits / 4 groups → 0 findings; colour and shadow only in the census)
  §2  layout/paint property    checked (8 hits / 3 groups → 1 finding, 6 locations; sidebar width is a review row)
  §3  no reduced-motion branch checked (0 JS-driven files; CSS covered by the reset)
  §4  off-scale literal        checked (6 hits → 0 findings; autofill workaround and the reset are precedents)
  §5  moves on its own         checked (1 hit → 0 findings: the reset's spinner exception)
  §6  over the ceiling         checked (8 hits → 0 findings, 1 unconfirmed)
  §7  infinite animation       checked (20 hits → 0 findings; skeletons unmount on data)
  human lane                   OS-level reduced-motion toggle on a device: NOT RUN (human lane)
```

`[report-with-fix]`: the declaration, the trigger, the route and a failing census or emulation run are all present, and the fix is local. `[report-flagged]`: one link is unproven (no harness, a JS animation not traced, a trigger whose frequency is unknown), and the row names it and the settling probe. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` when the surface is absent; `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`. Write the report to `ai/audits/motion-<date>.md`.

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (posting rules § 1–10; AAA as a house rule § 4; muted autoplay ≤ 5 s and videos with controls § 32; motion § 90–95) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The motion precedents, in short:

- **The reduced-motion reset itself** (`animation-duration: 0.01ms !important` under `prefers-reduced-motion: reduce`) and its essential-spinner exception (§ 90, 91).
- **The autofill-background workaround** (`transition: background-color 5000s`) is not motion (§ 92).
- **A toast's `duration`** (sonner, react-hot-toast) is display time, not an animation (§ 93).
- **Essential motion** — a progress spinner inside a loading branch — is not §5; it still respects reduce where the reset reaches it (§ 94).
- **Height animations a DS accordion owns** (Radix's measured content-height variable) are one review row at the primitive, not one per consumer (§ 95).

## When to run

- On any diff touching a transition, keyframes, an animation library call, a carousel or a motion token: the `/frontend-audit` dispatch signal when the frontend pack is installed (its A11y motion row).
- On every whole-repo `/frontend-audit`, `/a11y-audit`, `/polish` and `/align` on `frontend-*`, reporting all seven classes.
- Pre-release, when investigating "feels janky", after an animation-library or framework upgrade, and as a quarterly motion-token review.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on a finding without the animation declaration's `<file:line>`, its property and its trigger.
- Halt on a performance claim ("drops to 30 fps") without a profile artifact: name the tool and the file path, or print `fps: SKIPPED (not profiled)`.
- Halt on a duration, easing or token proposed that is not in the project's resolved scale or `motion.md` § The duration scale; this skill prints none of its own.
- Halt on a WCAG criterion at the wrong level: 2.3.3 is AAA, 2.2.2 is A. A house rule is reported as the house rule it is.
- Do not report a grep hit as a finding. A class whose grep did not run is `blocked`, never `checked`. Do not print a reduced-motion pass from source alone: the OS-level toggle on a device is the human lane, printed `NOT RUN (human lane)`.
- Do not propose deleting an animation under reduce in a way that leaves the state change invisible; replace it with a cross-fade.

## Related

- [`motion.md`](../../ai-patterns/motion.md) (this pack) — **owns the duration scale, the easing classes and the reduced-motion policy** this skill audits against. Findings cite it; they never restate a different number.
- `ui-design-sweep` § `normalize-motion` (this pack) — the applier for §1, §2, §4 and §6 findings, through `/polish` or `/enhance-ui` (the `motion-drift` cleanup class).
- `design-token-audit` (this pack) — the colour, spacing and type tokens; this skill is the motion dimension of the token surface.
- `a11y-code-scan` §12, `a11y-scan` §1 and `render-correctness-scan` §2 (frontend pack, when installed) — autoplay audio and captions, axe's `blink` / `marquee`, and animation loops never cancelled. `/frontend-audit` and `/a11y-audit` fold this skill's coverage block into their A11y motion row; `@ux-reviewer` grades 2.2.2 from it.
- `inp-responsiveness` (performance pack, when installed) — the cost of §2 animations on interaction latency.
- Native surfaces — the per-platform reduce-motion APIs, off-main-thread drivers and profilers live in the mobile pack's `references/<framework>.md` when it is installed.
- `/redesign` · `/art-direct` — where motion is a first-class build output, not a consistency fix.
