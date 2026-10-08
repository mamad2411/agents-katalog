# CLAUDE.md

## What this is

`sumo-linter` — a linter and opinionated formatter for SUMO (support.mozilla.org)
Knowledge Base wiki markup, scoped to **MZLA Thunderbird** content.

- **Phase 1:** detect and fix genuine formatting errors.
- **Phase 2:** apply opinionated house style (Black/Ruff-style), as a *named preset*.
- **Phase 3+:** non-English locales.

Firefox and other non-MZLA products are deliberately out of scope for style — they keep
their own conventions. This is why the style layer must be a configurable preset
(`style = "thunderbird"`) on top of a product-neutral correctness core, never hardcoded.

Scope: products `thunderbird` + `thunderbird-android` on **production**
(`support.mozilla.org`). Locale-aware architecture from day one, but **only en-US is
implemented**. The corpus is 203 articles; 196 public ones are committed under `corpus/`,
refreshed 2026-09-09. `corpus/README.md` records how the public/non-public split is decided
and why it cannot be inferred from the API.

## Current state

Phases 1 and 2 are implemented and tested. `cargo test` runs 34 tests, including property
tests over every corpus article.

The corpus is no longer Thunderbird-only: `corpus-other/` holds 475 public Firefox
articles, 207 other-product templates and the 3 markup-documentation articles — 895
documents of en-US source in total, all round-tripped in CI. It exists for lexer coverage
*and* for the markup-aware search in issue #6. Thunderbird **style** still applies only to
`corpus/`.

Linting the committed corpus reports **4 errors, all verified by hand** and all filed:
issues #223, #224, #225 (unbalanced `'''`) and #228 (two `{for}` bugs in
`keyboard-shortcuts-thunderbird` that the earlier regex audit could not detect, because the
file's 294/294 tag totals balance). It was 5 until the 2026-09-09 refresh: the SW004 in
`thunderbird-desktop-and-thundermail` has since been fixed upstream — so **re-lint after a
rescrape and treat a change in that count as a real signal**, about either the articles or
the linter.

The WASM build and web app are **verified working in a real browser**: all six exports load,
diagnostics render with correct line/column, both buttons behave, and a 124 KB input with
Arabic, Japanese and em-dashes lints in 4 ms and styles in 11 ms while still round-tripping.

Toolchain: **rustup-managed rustc/cargo 1.97.1** plus the `wasm32-unknown-unknown` target,
Node 22, Playwright + Chromium 1234. Homebrew's `rust` formula was removed — having both
meant a stray `/opt/homebrew/bin/cargo` would silently lack the WASM target.

Build and serve the web app:

```sh
tools/build-web.sh                        # writes web/sumo_lint_wasm.wasm (~116 KB)
python3 -m http.server -d web 8412        # pick a free port; 8099 is often taken
```

## Where to pick up

Phases 1 and 2 are done, pushed, and CI is green. The web app is live at
<https://thunderbird.github.io/sumo-linter/>.

**Open, on Roland's side (no deadline):**
- Post the heading-convention consultation: `docs/heading-convention-discussion.md` plus
  the data gist <https://gist.github.com/rtanglao/2708f762f5a4ec71c699827d8bc4071f>.
  **This blocks nothing** — the per-article default needs no decision.
- Fix the four filed markup bugs: knowledgebase-issues **#223, #224, #225, #228**.
- Triage the 8 non-public drafts: knowledgebase-issues **#227** (has a checklist). Two of
  the eight are not drafts at all — `invalid-certificates` is a misfiled support question,
  and `troubleshoot-pdf-and-email-issues-thunderbird` reads like machine-generated filler.

**Open, for a future session:**
- sumo-linter **#1 is answered** (2026-09-09), and the answers are in
  `corpus-other/README.md`: `{{{n}}}` does not exist but `{{{name}}}` does (31 uses, all
  named); `REDIRECT` is real but appears once, bare, with no leading `#`; and
  `[[Include:]]` occurs **nowhere** in 895 documents, so that path has no production markup
  to test against — a finding, not a gap. The same sweep found 21 real unbalanced-`{for}`
  errors in Firefox articles (correctness rules are product-neutral, now with evidence) and
  the SW007 false positive fixed in #7.
- Phase 3: non-English locales. Locale is already threaded through; no en-US assumptions
  live in rule logic.
- A **markup-aware search engine** over the KB — Roland's stated goal, 2026-09-09. SUMO's
  search indexes *rendered* text, so it cannot answer "which articles reference
  `[[Template:X]]`" or "which use this construct". Nothing is built; the point for now is
  that it makes corpus scrapes **complete sets, not samples** — `corpus-other/` exists for
  round-trip coverage *and* for this — and that the lossless token stream is already the
  right substrate: queries over token kinds rather than regexes over text.

**Do not redo:** the corpus is already scraped and committed (rescraping is cheap to *ask*
for and expensive to *run* — a full pass is ~200 signed-in page fetches and reliably earns
a 429 for the rest of the hour); the heading data is already measured; the four bugs are
already filed with rendered-output evidence. **Every test now runs in CI** — `rust`,
`vscode` (34 grammar + 51 link assertions), `emacs`
(63 mode assertions, against the real CLI), `vim` (61 plugin assertions, run under
both Vim and Neovim) and `web` (31 assertions on the fix arithmetic) — so there is no
by-hand test suite left.
LSP quick fixes (`textDocument/codeAction`) are implemented, tested, pushed and
CI-green as of 2026-08-17;
the VS Code `SUMO: Insert Link` command (`Cmd+K Cmd+L`) was added 2026-08-19, and
paste-a-URL-over-a-selection (sumo-linter #2) on 2026-08-28, and insert-link in Emacs and
Vim the same day, which brought the three editors to parity;
the editor-side setup they need is in `editors/README.md`, including the GhostText
`fileExtension` setting without which the extension never activates on a SUMO textarea.

## Hard-won facts about SUMO (verified live — do not re-derive)

**The markup is not Markdown.** It's Kitsune's own wiki dialect. A Markdown parser is the
wrong tool. Authoritative sources:
- `kitsune/wiki/parser.py` and `kitsune/sumo/parser.py` in mozilla/kitsune
- KB articles `markup-chart`, `markup-cheat-sheet`, `how-to-use-for`, `using-templates`

**Both prod and staging sit behind a Fastly client challenge.** Every plain HTTP request —
including `/api/1/kb/` — gets a 3038-byte JS interstitial titled `Client Challenge`. `curl`
cannot be used. A real browser is mandatory.

**`--disable-blink-features=AutomationControlled` is load-bearing.** The challenge gates on
`navigator.webdriver`. Measured, and counterintuitive: bundled Chromium *with* the flag
clears the challenge; `channel:'chrome'` *without* it stays blocked forever. Do not "clean
up" that launch arg.

**The public API never exposes raw wiki source.** `/api/1/kb/<slug>` returns
`id, title, slug, url, locale, products, topics, summary, html` — `html` is rendered.
`/kb/<slug>/history` and `/revision/<id>` are public but also rendered. Raw source lives
only in `<textarea name="content">` on `/<locale>/kb/<slug>/edit`, which **requires login**
on prod and staging alike.

**`?product=` is singular.** `?products=thunderbird` is silently ignored and returns the
entire 1493-article KB. A silent, easy-to-miss trap.

**SUMO rate-limits aggressively (429), including top-level navigation.** A 429 on a
navigation surfaces as `net::ERR_HTTP_RESPONSE_CODE_FAILURE`, not a status code. Backoff is
required in both the in-page fetches and `page.goto`. Bans persist for minutes; retrying
early may prolong them. Keep `--delay` high and prefer cached corpus files.

**Articles cannot be deleted on SUMO.** The available action is marking an article
**obsolete** (previously called "Archive"). Never recommend or describe deletion of a KB
article — the platform does not support it. Spam and misfiled content get marked obsolete.

**A template's slug cannot be derived from its title, and the API does not list templates
at all.** A `# COMPLETE` anonymous enumeration of `/api/1/kb/` returns 1325 public en-US
articles and zero templates. The KB contains `templatesharearticle` (colon dropped,
lowercased), `templateopenProfileFolderTB` (case kept) and `Template:optionspreferences`
(colon kept) — three conventions, so 44 guessed candidates all 404ed. Kitsune resolves
`[[Template:X]]` by *title*, so fetching one needs a title→slug map, and `/en-US/kb/all`
(`--all-docs`, 5299 documents, 221 templates) is the only index with both.

**A 404 to anonymous requests does not mean "unpublished draft."** Obsolete/archived, no
approved revision, and otherwise restricted all look identical from outside. Distinguishing
them requires the authenticated edit page or the SUMO admin UI.

**Free oracle:** the API's rendered `html` plus scraped source gives ~156
`(source → Kitsune's own HTML)` pairs. Useful for validating grammar assumptions without
running Kitsune in Docker. Opt in with `--rendered` (doubles request count).

## Scraper runbook

```sh
cd tools/scrape
npm install                 # once
npx playwright install chromium
npm run login               # you sign in by hand; session persists to .auth/
npm run scrape              # resumable; skips cached files
npm run scrape -- --limit 3 # trial
npm run report              # writes corpus/report.md
```

Read-only by construction: GETs only, never submits a form, defaults to staging
(`--base https://support.mozilla.org` to switch). `.auth/` is gitignored; **public** en-US
source is committed (see `corpus/README.md` and `corpus-other/README.md` for the rule and
the exclusions) — never commit an authenticated session or a non-public article.

Other modes, each added because nothing else could answer the question: `--force`
(re-fetch cached), `--list-only` (enumerate without a login), `--profile <dir>` (a throwaway
profile, i.e. what an *anonymous* visitor sees), `--only <listing>` (fetch nothing outside
an allow-list), `--slugs <file>` (`slug<TAB>name`, for documents no listing exposes),
`--all-docs` (page `/en-US/kb/all`, the only index containing templates), `--probe <file>`
(which slugs exist, by status code, no login, never fetches a body), `--path <p>` (one
arbitrary path through the same challenge/429/5xx handling), `--out <dir>`.
`batch.sh <product|--slugs FILE> <outdir> [batch] [allow-list]` paces a long scrape.

**Two tooling lessons, each of which cost a run on 2026-09-09:**

- **"Nothing left to do" and "nothing was done" are opposite outcomes that look identical
  from inside a loop.** This bit three times in one session: a two-file `awk` whose empty
  first file made every slug read as already-done (and reported success having probed
  nothing); `batch.sh` stopping because a pass *fetched* nothing when on a resume its whole
  batch was merely cached — it announced "firefox is complete" at 180 of 475 and deleted the
  state file that would have shown otherwise; and a truncated listing that would have filed
  every unreached article as an unpublished draft. Every such loop now compares what it
  recorded against what it asked for, and says which case it hit — hence the `# COMPLETE` /
  `# INCOMPLETE` marker that `public-index.mjs` refuses to run without.
- **Review the recovery path as carefully as the main one.** The resume line `batch.sh`
  wrote on failure omitted the allow-list, so following its own instructions would have
  dropped `--only` and started fetching drafts — the recovery path reintroducing exactly the
  hazard the flag exists to prevent.

## Architecture

Cargo workspace with **zero dependencies**. The core does no I/O so it compiles to WASM.

| Crate | Role |
|---|---|
| `crates/sumo-wiki-core` | lossless lexer → rules → formatter. No fs, no network, no deps. |
| `crates/sumo-lint-cli` | `sumo-lint` binary: hand-rolled args, `--fix`, `--style`, `--diff`, JSON |
| `crates/sumo-lint-lsp` | LSP over stdio: diagnostics, `textDocument/formatting`, `codeAction` quick fixes |
| `crates/sumo-lint-wasm` | four C-ABI exports (`lint`, `fix`, `style`, `is_lossless`) — no wasm-bindgen |
| `editors/` | VS Code extension (LSP client + TextMate grammar + `SUMO: Insert Link` + URL-paste handler); Emacs mode; `editors/vim/` Vim-script plugin (Vim 8+ and Neovim); LSP wiring for Neovim and ALE |
| `tools/scrape/` | dev-only Node corpus fetcher (not a runtime dependency) |
| `web/` | static Pages app — **paste-in only** (can't fetch source: needs auth + CORS); byte↔UTF-16 arithmetic isolated in `fixes.js` and tested under Node |

**Losslessness is non-negotiable.** Tokens tile the input exactly, so reprinting an
unmodified parse is byte-identical. This is asserted in the lexer, property-tested over
every corpus article, and re-checked before `--fix` writes a file — a lexer bug would
otherwise corrupt articles silently.

It is a **token stream**, not a full CST. That is enough for phase-1 rules and phase-2
formatting; do not describe it as a tree.

Diagnostics carry a stable code (`SW001`), severity, byte span, message, and an optional
fix marked `Safe` or `Unsafe`; only `Safe` fixes apply without `--unsafe-fixes`. **`Safe`
means the author's intent is unambiguous, not that rendering is unchanged** — SW009 and
SW010 turn inert Markdown into a real link and real bold, and `=h1` → `=h1=` turns a
literal line into a heading. What makes a fix `Unsafe` is a real choice between plausible
repairs: `==H ===` could have meant either level, and picking one silently changes what the
article says. Apply that test to every new rule. In the LSP
both kinds are offered as quick fixes (`Unsafe` titled *(needs review)*), because accepting
a code action is a deliberate, undoable choice, unlike a CLI writing files unattended. The
web app follows the same rule with a **Fix** button on each diagnostic, and earns the
"undoable" half of that claim: it edits the textarea through `execCommand('insertText')`,
deprecated but still the only way to keep a textarea's native undo stack — assigning
`.value` throws the history away. It also refuses to splice if the text changed since the
lint that produced the offsets, because linting is debounced and a click can arrive first.

**Pages caches `app.js` and the `.wasm` independently** (`max-age=600`), so for ten minutes
after a deploy a returning visitor can run new JS against the previous module. Measured on
the live site, where it presented as a Fix button that threw. Two guards, both needed: the
module is fetched with `cache: 'no-cache'` so it revalidates, and a fix without a span is
rendered as description-only rather than as a button. Test a change to the JSON shape by
building the previous module and serving it under the new page — the failure is invisible
otherwise, because a local build always ships both halves at once.

**Paste-a-URL-over-a-selection hooks paste, never rebinds it.** In all three editors the
gesture is "select words, paste a URL, get `[url words]`", and in all three the paste key
must keep pasting: VS Code uses a `DocumentPasteEditProvider` (not a `Cmd+V` binding, which
would replace paste in `.sumo` files with input boxes), Emacs remaps `yank` (so it follows
`C-y` *and* `s-v`), Vim maps visual-mode `p`/`P` buffer-locally. Each falls through to the
ordinary paste unless the gesture is unambiguous — single non-empty single-line selection,
register/clipboard is one whitespace-free URL, selection isn't itself a URL or bracketed —
because a paste handler that guesses silently mangles the clipboard. External form only:
internal links go by article *title*, which a `/kb/<slug>` URL does not carry.

Per-editor traps, all measured: VS Code needs **1.97+** (`engines.vscode` was bumped),
guarded so an older host loses the handler rather than failing to activate. Emacs
`delete-selection-mode` deletes the region in `pre-command-hook`, so the command needs a
function-valued `delete-selection` property to keep its link text — and `transient-mark-mode`
is **nil under `--batch`**, so a region test must bind it or pass vacuously. Vim must not
read the selection by yanking it: under `clipboard=unnamed` that overwrites the very URL
being pasted, so the plugin slices the line with `setline` instead; `:echo` prints nothing
under `-es`, so the test writes to `/dev/stdout`.

**A quick-fix provider is not optional.** Without one, `Cmd+.` on a SUMO diagnostic falls
through to whatever else the editor has installed, and an AI assistant asked to fix SW009
rewrites the markup into a *Markdown* link — the very syntax the rule flags. Measured in
Roland's VS Code, Aug 2026.

## Editor parity is a requirement, not a nice-to-have

Roland's instruction, 2026-08-28: keep the VS Code, Emacs and Vim SUMO markup modes
**synchronised — the same features in all three, as far as each editor allows.** They are
peers, not a primary plus two ports. He uses more than one himself, and these features are
about muscle memory, which does not survive being available in one editor only.

| Feature | VS Code | Emacs | Vim / Neovim |
|---|---|---|---|
| Diagnostics | LSP client | Eglot / lsp-mode / Flymake | native LSP / ALE |
| Quick fixes | `Cmd+.` | `M-x eglot-code-actions` | `vim.lsp.buf.code_action()` |
| Fix / style whole buffer | code action, `codeActionsOnSave` | `C-c C-f` / `C-c C-s` | CLI |
| Syntax highlighting | TextMate grammar | font-lock | *(none yet)* |
| Insert link (prompts) | `Cmd+K Cmd+L` | `C-c C-l` | `<LocalLeader>l` |
| Paste URL over selection | `Cmd+V` | `C-y` | visual `p`/`P` |

Idiom per editor, gesture in common: a VS Code paste provider, an Emacs `yank` remap and a
Vim visual mapping are the *same* feature even though the keystrokes differ. Do not chase
identical keybindings.

Keep each editor's decision logic a **pure function** — `link.js`,
`sumo-wiki--build-link` / `--link-from-paste`, `sumo_wiki#build_link` /
`#link_from_paste` — so it is testable headlessly and lands in CI. Linting itself lives
once in `sumo-lint-lsp` and is never duplicated; only editing gestures are. The remaining
gap is **syntax highlighting in Vim**: VS Code has a TextMate grammar and Emacs has
font-lock, Vim has no syntax file yet.

Headless-test traps, all measured, one per editor:
- **Emacs** — `transient-mark-mode` is nil under `--batch` but t interactively, so a region
  test must bind it or pass vacuously. Stub prompts by `cl-letf`-ing `read-string`.
- **Vim** — `:echo` prints nothing under `-es`, so write to `/dev/stdout`. `feedkeys(...,
  'x')` is the only way to answer `input()`, which is why `insert_link` must **not** call
  `inputsave()`/`inputrestore()`: they clear the typeahead buffer the answers live in and
  the prompt blocks forever. `plugin/` is not sourced when the runtimepath is set after
  startup — `runtime!` it by hand. `maparg()` never finds a `<Plug>` lhs; ask `:nmap`
  through `execute()`.
- **VS Code** — grammar and link logic are tested under plain Node; nothing needs a VS Code
  harness, and it should stay that way.

## Conventions

- Scaffold with `cargo init`; keep `cargo fmt` and `cargo clippy --all-targets` clean.
- MPL-2.0 header on every new source file (see `tools/scrape/*.mjs`).
- Write tests alongside code — `cargo mutants` is planned and needs real assertions.
- Required properties: **round-trip** (parse→print of unmodified input is byte-identical)
  and **idempotence** (`format(format(x)) == format(x)`).
- `tests/fixtures/selftest-known-bad.wiki` holds deliberately broken markup with 15 planted
  errors; keep it passing as a regression fixture.

## Phase 2: implemented, with churn as the governing constraint

`sumo-wiki-core::style` implements phase-2 formatting. The default is the least
invasive setting that still removes real inconsistency, because **every source change is
reviewed by volunteer localizers** — a diff with no rendered difference costs their time
for nothing.

Measured on the 203-article corpus:

| Setting | Articles changed |
|---|---|
| Default (per-article heading normalisation) | **30 / 203 (15%)** |
| `--strip-trailing-whitespace` | 129 / 203 (64%) |

- **`HeadingSpacing::PreserveDominant` is the default.** Each article is normalised to
  whichever style *it* already uses most; already-consistent articles come back
  byte-identical, and ties are left alone. This means the `= H =` vs `=H=` question
  **does not block phase 2** — when the community decides, set `Style::heading_spacing`
  to `Spaced` or `Tight` and the same code enforces it.
- **`trailing_whitespace` defaults to false.** It quadruples churn for zero rendered
  benefit. Opt in per invocation with `--strip-trailing-whitespace`.
- Asymmetric headings are **skipped** by the formatter: which level the author meant is a
  guess, so it stays a phase-1 error (SW005) with an *Unsafe* fix for a human to resolve.
  A heading with **no** closing run (`=h1`) is a different case — the opening run is the
  only evidence, so that fix is *Safe* and closes with a run mirroring the opening
  spacing (`=h1` → `=h1=`, `= h1` → `= h1 =`), taking no side in the spacing question.
- Properties enforced over the whole corpus: formatting is **idempotent**, output still
  **round-trips**, and the **line count never changes** (localizers diff by line).

## Phase-2 candidate rules (not yet implemented)

- **Heading spacing as a global convention** — still awaiting community consultation, but
  no longer blocking; see the table above.
- **Make leading-space preformatting explicit.** A line beginning with a space is
  rendered preformatted by wiki markup, which is invisible in source and easy to
  create by accident. `switching-thunderbird` relies on it for a `.reg` sample.
  Proposed: rewrite such blocks as an explicit `<pre>` so the intent is obvious,
  and flag lone space-indented lines that were probably accidental. Needs care —
  the rewrite must not change rendering, so verify against the `--rendered` oracle.
- **Whitespace hygiene** — trailing whitespace (382 occurrences) and tab characters
  (98). Uncontroversial, safe to autofix.
- **Within-article heading consistency** — 20 articles mix both heading styles;
  normalising each to its own dominant style needs no community decision.

## Style rollout: opportunistic, never a bulk sweep

Decided 2026-08-04: once a house style is settled, apply it **going forward, as articles are
edited for other reasons**. Do not mass-reformat the KB.

Why this constrains the design: a bulk sweep would rewrite ~500+ headings with *zero*
rendered difference, bury substantive edits in revision history, and hand localisers a pile
of source changes with no user-visible payoff. So the formatter must be useful on a single
article at a time, and there is no migration script to write. The same applies to the 20
internally-inconsistent articles — fix them when touched.

Heading style is genuinely undecided and awaiting community consultation: the corpus splits
53.9% `= H =` vs 44.7% `=H=` across 1149 headings, and `=H=` is the *newer* trend. Neither
form may be treated as correct in the meantime. See `docs/heading-convention-discussion.md`.

## Rule-selection principle

Phase-1 rules are ranked by **measured frequency in the real corpus** (`corpus/report.md`),
not by guesswork. Every regex hit in that report is a *candidate* for human review, not a
verdict — the audit's heuristics are deliberately crude and do produce false positives.

Cautionary example: `# Text` looks like a stray Markdown heading but `#` is SUMO's
ordered-list marker, so the two are indistinguishable and no such rule can exist. Likewise
`*` is a list marker, not emphasis.

## Commands

```sh
cargo build && cargo test        # once Cargo.toml exists
cargo fmt && cargo clippy --all-targets
```
