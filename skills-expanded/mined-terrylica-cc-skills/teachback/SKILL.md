---
name: teachback
description: Build or deepen a single-file interactive HTML explainer that teaches back difficult material already established in the conversation (or a named subject/source). Use when someone wants a durable, self-contained lesson with rendered mathematics, an exploratory multiple-choice assessment, and a terminology loop that lets the reader push unfamiliar terms back for deeper coverage.
---

# teachback — teach the material back as a self-contained interactive page

> **Self-Evolving Skill**: this file improves through use. If an instruction here is wrong, a gate
> rejected a page it should have accepted, or you needed a workaround — fix this file immediately,
> don't defer. Only for real, reproducible issues. And when you add a check to a gate, add the
> mutation that proves it can fail: an unexercised check is not yet a check.

Produces **one HTML file** that explains hard material to an intelligent reader with no assumed
specialist background. The page runs from `file://` with no server, no tracking and no framework.

The defining behaviour: **teachback reads what is already in the working context.** Do not ask the
reader to restate material the conversation already contains. Infer the subject, scope, prerequisites,
title, filename and technical depth.

> **This copy is canonical.** teachback was built in `Eon-Labs/alpha-forge` and merged there as
> [#527](https://github.com/Eon-Labs/alpha-forge/pull/527) after eleven review rounds; it was promoted
> to [terrylica/cc-skills](https://github.com/terrylica/cc-skills) on 2026-08-20 to make it available
> in every project rather than one repository. **Edit it here.** The alpha-forge path
> `.claude/skills/teachback/` is being reduced to a redirect stub carrying no gate scripts; until
> that lands, two full copies exist and only this one is authoritative. If you find yourself editing
> the alpha-forge copy, stop and edit this one.

---

## Options

Every option is optional. `/teachback` with no arguments is the common case.

| Option                          | Effect                                                                                                                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _(none)_                        | Explain the most recent coherent discussion in the working context.                                                                                                                                           |
| `<subject>`                     | Explain a named subject instead, e.g. `/teachback the spanning admission result`.                                                                                                                             |
| `--source <path\|issue\|url>`   | Explain designated material rather than the conversation: a file, `#123`, a doc path, a URL.                                                                                                                  |
| `--out <path>`                  | Write the page here. **Default: `~/Documents/explainers/<slug>.html`, outside the repository** — generated pages are artefacts, not source. Pass an in-repo path only when the page is meant to be committed. |
| `--update <path>`               | Revise an existing page in place instead of creating one. Implied by `--terms` and `--revise`.                                                                                                                |
| `--terms "a, b, c"`             | **The terminology loop.** Add or substantially deepen coverage of these terms in an existing page. This is what the page's own footer form emits.                                                             |
| `--revise "<instruction>"`      | Any other change to an existing page, in plain language.                                                                                                                                                      |
| `--depth intro\|standard\|deep` | How much advanced qualification to carry. Default `standard`. `deep` keeps every limitation, objection and open question.                                                                                     |
| `--questions <n>`               | Assessment size. Default 3–8, chosen to cover the objectives.                                                                                                                                                 |
| `--open` / `--no-open`          | Launch the default browser on completion. Default `--open`.                                                                                                                                                   |
| `--dark` / `--light`            | Force a colour scheme. Default: follow the operating system.                                                                                                                                                  |

**Composition:** `--terms`, `--revise` and `--update` operate on an existing page and always append a
revision-ledger entry. Everything else builds a new page.

---

## What the page must contain

Include a section only when it materially improves understanding. Do not pad to fill a structure.

1. Orientation and explicit learning objectives
2. A concise 101-level account
3. Prerequisites and terminology
4. Canonical definitions
5. Components, variables, actors, stages or layers
6. The literal mechanism or logical sequence
7. Conditions, boundaries, exclusions, common confusions
8. A real example, a non-example, and a near-miss
9. A justified worked application
10. Advanced qualifications, limitations, exceptions, open questions
11. The diagnostic assessment
12. The terminology request form and the revision ledger

### Provenance marking is mandatory

Distinguish three kinds of statement, visibly, with the `.prov` spans:

- `SOURCE-ESTABLISHED` — measured or stated in the underlying material
- `INFERENCE` — explanatory reasoning added by the explainer
- `OPEN` — unresolved, contradictory, or missing evidence

**Mark contradictions and uncertainty; never invent a resolution.** Where a later correction
supersedes an earlier statement in the source material, the correction wins and the supersession is
stated.

### Pedagogy constraints

Reduce prerequisite burden and linguistic complexity **without** reducing technical precision.
Preserve accepted terminology, definitions, mechanisms, causal relationships, boundary conditions and
qualifications.

**Do not use analogies, metaphors, fictional comparisons, or approximate substitutions that alter the
concept.** Explain the thing itself.

---

## Mathematics

Render with **MathJax 3**, from a version-pinned CDN URL carrying a **subresource-integrity hash**:

```html
<script
  id="mj"
  async
  src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"
  integrity="sha384-Wuix6BuhrWbjDBs24bXrjf4ZQ5aFeFWBuKkFekO2t8xFU0iNaLQfp2K6/1Nxveei"
  crossorigin="anonymous"
  referrerpolicy="no-referrer"
></script>
```

**Never point the primary source at a local absolute path.** An earlier version of this skill
prescribed `file:///Users/<name>/node_modules/mathjax/...` with a JavaScript `error` fallback to the
CDN. Measured, that fallback does fire and the page does render — but the pattern is wrong twice
over: the path cannot travel with the artifact, and served over http(s) a browser refuses `file://`
subresources outright, logging `Not allowed to load local resource` and leaving the generating
machine's home directory in the DOM for anyone who receives the file.

`integrity` pins the bytes, not merely the URL: a swapped or compromised CDN object fails to execute
rather than running silently. Recompute it if the pinned version changes —
`curl -sSL <url> | openssl dgst -sha384 -binary | openssl base64 -A`.

If a page must render with no network at all, pre-render the mathematics to **SVG** at generation
time rather than adding a local script source; SVG output inlines glyph paths, so it needs no font
requests. Do not add a `file:` source to a page that will be shared.

- Preserve every material equation, variable, operator, constraint, domain, assumption and subscript.
- Give consequential equations **stable numeric identifiers** and keep them stable across revisions.
- Put the **raw LaTeX in a `<details>` panel** beneath each numbered equation so it is recoverable.
- Define symbols, units, assumptions and validity conditions near first use.
- Explain what each equation asserts and how its terms relate; show consequential intermediate steps.
- Distinguish source equations from added derivations.
- If an expression looks wrong or ambiguous, **preserve it and add a marked note** — never silently
  correct or simplify it away.
- Never render mathematics as images, canvas, or Unicode approximations.

Rendering the equation correctly is the floor, not the goal. Every equation must additionally satisfy
**Notation accessibility** below.

---

## Notation accessibility (release-blocking)

The reader is assumed to be **symbolically illiterate but not unintelligent**: fluent in the subject
matter, unpractised at decoding notation. An equation printed bare forces them to hold a symbol in
memory, hunt for its definition in surrounding prose, carry the meaning back, and repeat — the
_split-attention effect_, and it is the single largest avoidable cost on a page like this.

Every numbered equation carries **four** things. Fewer is a defect, not a style choice.

### 1. Systematic colour encoding

Colour symbols by the **kind of thing they are**, with one fixed vocabulary reused across the whole
page. The same colour must mean the same role in every equation; a symbol must never change colour.

| Role       | Meaning                                     | Typical symbols |
| ---------- | ------------------------------------------- | --------------- |
| `sym-out`  | the quantity the equation exists to define  | Δ, α, IR        |
| `sym-pos`  | positions, weights, loadings — what is held | w, w⋆, β        |
| `sym-ret`  | returns; what an instrument or book earned  | r, g, y, e      |
| `sym-time` | time indices, counts, block labels          | t, i, T         |
| `sym-cost` | costs, turnover, penalties                  | c, κ, λ         |
| `sym-disp` | dispersion, covariance, risk aversion       | σ, Σ, γ         |

Adapt the _roles_ to the subject; keep the _discipline_. Six is near the ceiling — beyond that the key
itself becomes the thing to memorise.

Implementation is fixed, because the obvious version silently fails:

```js
// Listing the package is NOT enough. tex-mml-chtml does not bundle the html extension, so without
// this loader entry \class renders as literal red "\class" text in the output.
loader: { load: ['[tex]/html'] },
tex: { packages: { '[+]': ['html'] } }
```

Then `$\class{sym-out}{\Delta} = \class{sym-pos}{w}\,\class{sym-ret}{r}$`, with colour defined **once**
per role as a CSS custom property. Use a colourblind-safe palette (Okabe–Ito) and give every role a
distinct dark-mode value; a hue that reads well on white can vanish on near-black.

Two properties make the code trustworthy, and both are checked:

- **One role per symbol, everywhere.** A symbol that is `sym-out` in one equation and `sym-disp` in
  another teaches the reader that the colour is arbitrary.
- **The code extends into prose.** A symbol mentioned in a paragraph carries the colour it was given
  in the equation that defined it. An encoding applied only inside the equation boxes reads as
  decoration. Colour _role-bearing symbols_ only — a bare statistic such as `p = 0.027` has no role,
  and colouring it dilutes the vocabulary.

**Verify by inspecting the emitted DOM, never by assuming.** Count `mjx-container .sym-*` occurrences
and read back `getComputedStyle().color` in both schemes. A silent `\class` failure looks like
ordinary red text and is easy to scroll past.

### 2. Colour is redundant, never load-bearing

Every coloured symbol also carries a **chip** beneath its equation: the symbol, what it means in
ordinary words, and its shape or value. Nothing on the page may require distinguishing two hues.

Chips sit **directly under the equation they annotate** — spatial contiguity. A legend elsewhere on
the page reintroduces exactly the hunting the colours were meant to remove.

**Every chip declares which symbols it explains, in `data-symbol`, verbatim as they appear inside
`\class{…}{…}`, separated by `|`:**

```html
<span class="chip sym-time" data-symbol="t|t-1"
  ><b>t, t−1</b><span>the bar being scored, and the bar before it</span
  ><i
    >the weight is fixed at t−1, so it cannot use anything observed at t</i
  ></span
>
```

Declared rather than inferred, because the chip renders `μ_p` as glyphs while the source says
`\mu_{p}`; matching them would be a normalisation guess, and a guess that fails reads as coverage.
The gate requires every `(role, symbol)` pair an equation colours to be declared by one of its chips.
Comparing role **sets** is not enough — an equation colouring both `g` and `n` as `sym-out` with one
chip has identical sets on each side, which is how `t`, `t−1`, `g` and `R` stayed coloured and unnamed
in the reference page through several rounds of review.

### 3. A notation key before the first equation (pre-training)

Introduce the role vocabulary and the typographic conventions — bold means a collection, a subscript
is a label and not a multiplication, a star means "chosen to be best" — **before** the first equation,
never inline with it. Learning six categories once is cheaper than decoding forty symbols later.

The key must survive the expert switch below: it is the only place the encoding is decoded, so hiding
it strands the reader with an undocumented code.

### 4. Equation as a sentence, then as numbers

Each equation gets:

- a **`Reads as`** block — the equation restated as one plain-language sentence, subject and verb, no
  symbols. Not a gloss of the notation; a statement of what it asserts.
- a **`With numbers`** block — the equation instantiated with the actual figures from the material,
  including what the result was and why. Where a real figure is unavailable, say so; never invent one.

Both blocks contain mathematics, and **mathematics cannot line-break**. Give `.eq`, `.reads` and
`.numbers` `overflow-x:auto` so a long expression scrolls inside its own block. Omitting this was
measured at 120px of _page-level_ horizontal scroll on a 390px viewport, caused by one inline
arithmetic line — a local formatting choice turning into a whole-document defect.

Use `\underbrace{...}_{\text{...}}` to name multi-term groups **inside** the equation. This is
_signalling_: it partitions a wall of symbols into two or three named chunks that can be read
independently, and it is the one annotation the reader cannot fail to associate with the right terms.

### 5. Expertise reversal — all of it must be switchable

The same annotation that measurably helps a first reading measurably **hinders** a reader who has
internalised the notation, because reconciling redundant explanation is itself work. Provide one
page-level control that hides the readings, chips and worked numbers; keep the colour encoding and the
notation key, since neither costs vertical space. Persist the choice in `localStorage` inside a
`try`/`catch` — private-browsing mode must degrade to "not remembered", not to a thrown error.

### 6. Do not claim accessibility features you have not verified

Recorded negative, so it is not re-attempted blind: the **MathJax a11y explorer is not usable in a
portable single file.** Measured on 2026-08-18 —

1. `loader.load: ['[a11y]/explorer']` resolves the unregistered `[a11y]` prefix against the _document_,
   404s, and **aborts MathJax startup**: container count 8 → 0. An optional extra took every equation.
2. Loading it after startup with the path repaired throws `EnrichedMathItemMixin`, because the bundle
   registers no dependency metadata for `[a11y]` either.
3. Loading the whole chain in order (`sre`, `semantic-enrich`, `complexity`, `explorer`) succeeds and
   sets `explorer = true`, but **no `aria-label` and no `data-semantic-speech` is ever attached**, even
   after a forced `rerender()`. The module is present and inert.

Hard-coding the `a11y` path at config time works locally, but the artifact is meant to travel and a
stale absolute path then takes the equations down with it. The `Reads as` sentence is the substitute,
and it is purpose-written prose rather than machine-generated speech. If a future revision does enable
speech, gate the on-page claim on the capability actually being present, not on the module loading.

---

## Layout

- Page shell occupies **92–100%** of desktop width; no globally narrow container.
- **Body text fills the content column.** Operator decision 2026-08-18: a 65–80ch cap beside a wide
  shell leaves a large void to the right of every paragraph, which reads as hard-wrapped text. Prose,
  cards, tables, equations and the assessment all use the same width. Do not reintroduce a prose cap
  or a marginalia rail without being asked.
- **Contents is a collapsed sticky `<details>` disclosure, not a sidebar rail.** Operator decision
  2026-08-18: a permanent rail spends horizontal space on navigation that is consulted occasionally.
  Closed it costs one ~40px bar; open it expands to a multi-column list. Native `<details>` keeps it
  keyboard-accessible and working with JavaScript disabled.
- **Do not make `.shell` a grid.** If it ever becomes one, every direct child (`header`, `nav`,
  `main`, `footer`) needs an explicit `grid-column`. A child without one auto-flows into the next
  free cell — which is column 1 — and that is how the revision ledger once rendered inside the
  narrow contents column.

**These are RENDERED invariants, and only `verify_rendered.py` may assert them.** Do not add a
layout check to the static gate. Whitespace and declaration order are insignificant in CSS, so
matching source text is unsound in principle, and it was unsound in practice: the pattern
`.shell{display:grid` matched, while the exactly equivalent `.shell { display: grid; }` bypassed the
grid-child check entirely — the check silently enforced nothing on any page whose CSS happened to be
formatted (Eon-Labs/alpha-forge#527 review, finding 4). The rendered gate reads these back from `getComputedStyle`
and from measured geometry, where formatting cannot change the answer.

- Keyboard navigation, visible focus, sufficient contrast, dark mode, print, and full intelligibility
  with JavaScript disabled (JS is required only for assessment validation and the terminology form).
- Keep all explanatory content in the DOM. No decorative clutter, gratuitous animation, oversized
  hero, marketing language, or dashboard elements.

---

## Assessment — exploratory, not an examination

3–8 questions covering the major objectives, including definition/boundary recognition, mechanism or
reasoning, and transfer to a new closely related case.

One best answer, three purposeful distractors. **Every distractor encodes a different plausible
misconception arising from the material.** No filler, trivia, deceptive wording, test-taking tricks,
"all of the above" or "none of the above".

**The reader is never locked out. This is the point.**

- Selecting the correct answer marks it correct — and **every other option stays selectable**.
- After the answer is found, clicking a distractor shows what that option assumes and why it is
  wrong, presented as exploration rather than failure.
- Before the answer is found, an incorrect selection names the misconception and gives a targeted
  hint **without revealing which option is correct**, and another attempt is permitted.
- Per-question reset, reset-all, and a live summary of objectives demonstrated versus needing review.
- Track and report **misconceptions explored**, not just correctness. A reader who has read every
  distractor's explanation has learned more than one who guessed right first time.
- Never transmit, store or track responses. No `localStorage`, no `fetch`, no cookies.

### Emit the assessment as JSON, not as a JavaScript literal

The questions live in a **`<script type="application/json" id="assessment-data">`** block **inside
`<main>`**, and the page's own script does `JSON.parse(...)` on that block. One source of truth: the
gate reads exactly what the page reads.

This is structural, not stylistic. A per-question contract cannot be soundly verified by regexing a
JS object literal, and the attempt failed in the favourable direction: counting document-wide
`ok: true` occurrences certified a page where one question had two correct answers and another had
none, because the totals matched (Eon-Labs/alpha-forge#527 review, finding 1). Parsing makes "one correct and three
distractors **in every question**" checkable, and makes duplicate question ids detectable.

Placing the block inside `<main>` also fixes the ledger: question text is teaching content, but in a
`<script>` after `</main>` it sat outside the revision hash, so editing a question changed nothing in
the revision id.

---

## Privacy: deny by default with a Content Security Policy (release-blocking)

The page is generated **from private working context**. An exfiltration channel is therefore a real
risk, not a theoretical one, and a blacklist of JavaScript APIs cannot close it: a remote `<img>`, a
`<script>`, a `<link>`, a `<form action>`, a `WebSocket` and an `EventSource` are all requests, and
none of them calls `fetch` (Eon-Labs/alpha-forge#527 review, finding 7).

Every page carries this as the **first element after `<meta charset>`**, before any content it must
govern — a policy in `<meta>` does not apply to markup the parser has already seen:

```html
<meta
  http-equiv="Content-Security-Policy"
  content="default-src 'none'; script-src 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'unsafe-inline'; font-src https://cdn.jsdelivr.net; form-action 'none'; base-uri 'none'"
/>
```

`connect-src`, `img-src` and `frame-src` are deliberately absent: they fall back to
`default-src 'none'`. `'unsafe-inline'` is required because the page's own `<style>` and `<script>`
are inline and MathJax injects styles at runtime; it is not a weakness here, because
`default-src 'none'` still denies every _destination_.

**Measured, not assumed.** Against a local sink on a separate origin, a page without this policy
delivered five requests — image beacon, remote script, remote stylesheet, WebSocket handshake, SSE
stream. With it, **zero arrived**, and all equations still rendered. Re-run that comparison if the
policy changes; a CSP that blocks nothing is not a control.

Three properties of that policy are contractual, not incidental:

- **It precedes every element that can issue a request.** A policy in `<meta>` does not govern markup
  the parser has already seen, so a _late_ policy leaves everything above it ungoverned — including
  a beacon on the allowed origin, which both gates would otherwise wave through.
- **The single remote reference is an exact URL, not an origin.** An origin allowlist is not enough:
  any path on that origin can carry page content in its query string.
- **That reference carries the expected `integrity` value**, not merely some integrity attribute.

`localStorage` is permitted for exactly one key, `teachback:annotations`, holding the annotation
preference. Reader responses are never stored. Every access sits inside its own `try`/`catch`, so
private-browsing mode degrades to "not remembered" rather than throwing.

**Enumerate storage references, then subtract the permitted ones — never the reverse.** Scanning for
`localStorage.setItem(` is an allowlist with an open back door: `localStorage["setItem"](…)` is
ordinary JavaScript that produced zero detected accesses _and_ zero unguarded offsets, so a page
persisting reader answers passed both storage checks at once.

**Then stop arguing about syntax and observe the storage.** The static rules ban computed global
access and runtime-built property keys, but that is a constraint on _shape_ — it closes the spellings
someone thought of, and `document.defaultView`, `Reflect.get(document, "defaultView")` and whatever
comes next are not among them. `verify_rendered.py` therefore exercises the page — every question
answered, the annotation toggle flipped — and then reads `Object.keys(localStorage)`, asserting the
set is exactly `{teachback:annotations}`, with `sessionStorage` and `document.cookie` empty.

Keep both. The static rules fail fast and say _why_ at the point of authorship; the observation is
the one that actually holds, because it does not care how the code was written.

---

## Terminology loop

The page ends with a form where the reader lists terms they did not understand.

The form **cannot call a model**; it composes a ready-to-paste instruction and copies it to the
clipboard, naming the page path and current revision id:

```
/teachback --update <abs-path> --terms "portfolio admission, certainty equivalent"
```

When invoked with `--terms`, expand those terms substantively in the terminology section — a real
definition, why it matters here, and how it differs from the nearest thing it is confused with. A
one-line gloss is not sufficient. Add a `<dfn>`-style anchor so the term can be linked from the body.

---

## Revision ledger

Every page carries a ledger as the **last element before the closing footer text**. Each update
appends one row; earlier rows are never rewritten.

| Field         | Meaning                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------ |
| `#`           | Monotonic revision number, starting at 1                                                         |
| UTC timestamp | When the revision was produced                                                                   |
| Revision id   | **First 12 hex of `sha256` over the exact bytes from `<main id="main">` to `</main>` inclusive** |
| Change        | One line describing what this revision altered                                                   |
| Commit        | The git commit that carried it, when the page lives in a repository; `—` otherwise               |

Hashing `<main>` only is deliberate: the ledger lives in the `<footer>`, so recording a revision id
cannot change the value being recorded. Recompute and verify with:

```bash
uv run --no-project --script "$(cc-plugin-root doc-tools)/skills/teachback/verify_explainer.py" <page.html> --revision
```

---

## Zero hard-wrapping invariant (release-blocking)

**Every `<p>` element must occupy exactly one physical line in the saved source.** Browsers soft-wrap
responsively; the source must contain no newline, `<br>`, `<wbr>` or newline entity between `<p...>`
and `</p>`. Do not use `white-space: nowrap`.

Apply the check **after every generation, formatting or build step**, and make it the **last
file-content operation** before opening the browser.

> **The naive whole-document regex `<p\b[^>]*>[\s\S]*?[\r\n][\s\S]*?</p>` is unsatisfiable and must
> not be used as the gate.** Being non-greedy across the whole document, it opens in one `<p>`,
> crosses that element's `</p>` and the following newline, and closes at a _later_ `</p>` — so it
> fires on any document containing two well-formed adjacent paragraphs on separate source lines. The
> correct test pairs each `<p ...>` with its own nearest `</p>` and requires that body to be
> newline-free. `verify_explainer.py` implements the correct test and reports the naive count
> separately so the distinction stays visible.

---

## Verification

Three tools, all Python. PEP 723 inline metadata makes each file self-contained: uv resolves each
gate's dependency into an ephemeral environment, so nothing has to be installed first and the gates
run against any project, in any language, on a machine with only uv present.

**Resolve the skill directory first, then invoke with `--no-project --script`:**

```bash
TB="$(cc-plugin-root doc-tools)/skills/teachback"

uv run --no-project --script "$TB/verify_explainer.py" <page.html>             # static gate
uv run --no-project --script "$TB/verify_explainer.py" <page.html> --revision  # print the revision id
uv run --no-project --script "$TB/verify_rendered.py"  <page.html>             # rendered gate (headless browser)
uv run --no-project --script "$TB/mutate_gate.py"      <page.html>             # negative fixtures
uv run --no-project --script "$TB/tests/test_check_discovery.py"               # the gates' own tests
```

The last line takes no page: it is the regression guard for the coverage audit below, and like the
gates it carries its own PEP 723 metadata, so it resolves pytest for itself.

`cc-plugin-root doc-tools` prints the live install path from
`~/.claude/plugins/installed_plugins.json`. The CLAUDE_PLUGIN_ROOT placeholder is **not** a shell
variable — Claude Code substitutes it only inside plugin manifests and injects it only into hook and
MCP subprocesses, never into the Bash tool. Spelled in a skill body it reaches the shell unset,
expands to empty, and yields an absolute-looking `/skills/teachback/...` that reads like a missing
file instead of a missing variable. Globbing the version cache is not the fallback either: that
directory retains orphaned versions and the highest semver is routinely not the live one.

`--no-project` states the isolation the gate depends on, rather than relying on it. **It is not
currently load-bearing, and this paragraph says so deliberately** — the first draft of it claimed
that plain `uv run` adopts the surrounding workspace and that the gates therefore had to be run from
`$HOME`. That claim was inferred from a `DEBUG Found workspace root:` line, which reports workspace
_discovery_, not workspace _adoption_, and it is false. Measured on uv 0.11.28 from a directory whose
`pyproject.toml` declares an unresolvable dependency — a fixture first checked to be genuinely
hostile, by confirming a plain `uv run python -c ...` there fails to resolve — all three of
`uv run <gate>`, `uv run --script <gate>` and `uv run --no-project --script <gate>` reached the
gate's own argparse. uv says as much itself: `--no-project is a no-op for Python scripts with inline
metadata; ignoring`.

Keep the flag anyway. It costs nothing, it is correct for any invocation that is _not_ a PEP 723
script (`uv run pytest ...` inside a project genuinely does resolve that project), and it keeps the
documented command correct if a gate ever loses its inline metadata block. What it must not do is
carry a mechanism story nobody re-measured.

### What each one owns, and why the split is not arbitrary

| Tool                  | Owns                                                                                                                           | Never touches                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| `verify_explainer.py` | source-text and structural invariants: hard wrapping, per-equation annotations, per-question assessment shape, CSP, the ledger | layout — see below               |
| `verify_rendered.py`  | anything only a browser can answer: computed colours, measured geometry, overflow, toggle behaviour, outbound requests         | source text                      |
| `mutate_gate.py`      | proving the static gate is not blind                                                                                           | the page itself (it restores it) |

Layout lives exclusively in the rendered gate. Asserting a rendered property against CSS source text
is unsound in principle and was unsound here: `.shell{display:grid` matched, `.shell { display: grid; }`
did not, and the check enforced nothing on formatted CSS.

The static gate **parses** the page with BeautifulSoup rather than pattern-matching it, because the
contracts are per-item. A document-wide count cannot see a per-item failure and fails in the
favourable direction — extras on one equation mask a total absence on another. Where the gate must
still look at text (the hard-wrap invariant, which is _about_ whitespace, and the scripted-network
check) it says so and scopes itself: the network check reads script bodies with comments stripped,
after whole-file matching flagged a page's own prose sentence "none of them calls `fetch()`".

### Every check must have been seen to fail

`mutate_gate.py` carries twelve mutations, one per defect class, and **asserts the unmutated baseline
is clean before counting any kill** — a harness that always reports non-zero looks identical to one
that works. Add a mutation whenever you add a check. A mutation that changes nothing, or cannot find
its target, is reported as BROKEN rather than counted as a survivor: two mutations here first looked
like blind gates and were in fact selecting a fragment with a non-greedy regex instead of the element
with a parser.

### A gate that cannot run is not a gate

`verify_rendered.py` bootstraps its own browser. PEP 723 resolves the Playwright _package_; it does
not download the _browser_, so the documented command failed in a clean checkout with
`Executable doesn't exist` — the same class of problem as the Bun dependency it replaced, one layer
down. It now runs `playwright install chromium` once on first use rather than documenting a
prerequisite nobody reads. Only a missing-browser failure triggers that; any other launch error
surfaces.

### Assertions must observe the state they are about

The lock-out check **solves a question first**, then clicks a distractor and confirms it still
explains itself. Reading the initial disabled count proved nothing: code that disables the other
options only _after_ the correct answer is chosen is invisible before the question is answered.

The same principle killed the width-based grid check. Inferring "explicitly placed" from a child's
width was vacuous in the common case — in a single-column grid every auto-flowed child is full width,
so the check passed while nothing was placed — and wrong in the uncommon one, since a deliberately
narrow but correctly placed child was reported as a fault. It now reads computed `grid-column-start`.

### Six rules that generalise every gate defect found in review

Eight review rounds and an adversarial self-review found the same few confusions repeatedly. They
are worth stating as rules, because each one closes a class that instance patches only delay.

**1. Presence is not content.** `select_one(".reads") is not None` is satisfied by
`<div class="reads"></div>`, and `.chips .chip` by `<span class="chip"></span>`. A generator that
emits the right skeleton with nothing in it was certified complete. Every annotation check therefore
asserts a minimum of actual visible text, and absent collapses to the same answer as empty.

**2. A source pattern is not a rendered property.** Scanning for `\class{sym-` proves the markup was
written; it does not prove the reader sees colour. One CSS rule — `color: inherit !important` — makes
every symbol black while the string is still in the file. Colour is therefore read per equation from
`getComputedStyle` in the rendered gate, and the static check is explicitly the weaker of the two.

**3. A curated list is not enumeration.** Watching `localStorage`, `sessionStorage` and
`document.cookie` left IndexedDB, the Cache API and the Origin Private File System unexamined — the
same losing game as naming Window aliases one at a time. Ask the browser what actually persists:
`indexedDB.databases()`, `caches.keys()`, `navigator.storage.getDirectory()`.

**4. A minimum count is not coverage.** "At least one non-empty chip" was satisfied by an equation
using six colour roles and explaining one, and "at least three key chips" by a page using six. The
contract is _every role the equation actually uses is documented_, so the check now compares the set
of roles **used** against the set **explained** and names the difference. Enforcing this immediately
found a real gap in the reference page: equation (6) coloured `sym-time` and never said what it was.

**5. A kill is only evidence for the check it targets.** A mutation that removed one `sym-disp` chip
was reported KILLED — but equation (8) documents that role twice, so coverage never broke; the only
failure was the **revision id**, which any edit changes. The mutation was a no-op for its own purpose
and looked identical to a working one. So every mutation now declares the check it must trip, and a
red run that misses it is reported `MISDIRECTED` and counted as a failure, not a kill.

**6. An unexercised check is not yet a check.** `mutate_gate.py --audit-coverage` lists every check no
mutation targets. The first run said 56 of 71 — and every vacuous check found in review up to that
point had been in that set, so that is where the rest were. Probing seven of them found six real
defects, the worst being an ordering check that located elements with `str.find` and read the −1
"not found" sentinel as "earlier", so it passed for **any** ordering. Report the remaining count
rather than "all mutations killed": a suite that says it is partial is honest.

The generalisation behind the first three: **verify the property the contract is about, at the layer
it lives on.** Source text, DOM structure and rendered appearance are three different layers, and a
check on the wrong one passes for the wrong reason. Rules 4 and 5 extend it one step further — a
check can also read the right layer and still ask a weaker question than the contract, and a test
suite can be green for a reason that has nothing to do with what it claims to prove.

### Still do a human browser pass

The rendered gate does not cover print presentation, dark-mode legibility as a human judges it, or
intelligibility with JavaScript disabled. Check those by looking.

**Do not claim a check passed unless it was performed successfully.**

---

## Completion

Resolve the file to an absolute path and open **that exact file** in the default browser
(`open <abs-path>` on macOS). Confirm the launch succeeded by querying the browser, not by trusting
the launcher's exit code — `open` returns 0 whether or not the page loaded. If no graphical session
is available, say so and give the exact manual command.

Then report: whether it opened, the path, one sentence on what it explains, and any unresolved
source, mathematical, verification or environmental limitation.

---

## Post-Execution Reflection

If a gate rejected a page that was in fact correct, accepted one that was in fact wrong, or you had
to work around an instruction above — update this file and the gate together, now, not "next time".
Two specific cases are worth the edit every time:

- **A check fired for the wrong reason.** Record which layer the contract actually lives on (source
  text, DOM structure, rendered appearance) and move the check there. Most defects found in review
  were checks reading the wrong layer and passing for an unrelated reason.
- **A mutation was reported KILLED without tripping its own target.** That is a `MISDIRECTED` result,
  not a kill; state which check the mutation is supposed to trip and fix the mutation, not the count.

When you add a check, add its mutation in the same edit, and re-run `--audit-coverage` so the
remaining unexercised count stays honest rather than quietly growing.
