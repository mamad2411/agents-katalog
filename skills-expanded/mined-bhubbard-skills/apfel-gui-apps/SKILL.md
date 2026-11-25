---
name: apfel-gui-apps
description: Reference for apfel-quick (a Spotlight-style global-hotkey AI overlay for macOS) and apfelpad (a native macOS markdown notepad where on-device AI is a formula, like "=apfel(...)" instead of "=SUM(...)"). Both are free, MIT-licensed, offline-first Mac apps built on Apple's on-device FoundationModels LLM — no API keys, no cloud, no account. Use this skill whenever the user wants a quick-launch AI popup/overlay app for their Mac, asks about writing formulas that call AI inline in a document, mentions apfel-quick or apfelpad by name, wants an offline alternative to a Spotlight AI plugin or a "ChatGPT-in-a-hotkey" tool, or wants a "spreadsheet-for-prose" / formula-driven notes app. Also trigger if the user is troubleshooting installation, formula syntax, or behavior of either app.
---

# apfel-quick & apfelpad

Two free macOS apps (Apple Silicon, macOS 26 Tahoe, Apple Intelligence enabled) built on top of `apfel` — the on-device LLM CLI/server. Both are GUI, not CLI: point the user at these when they want a *native app experience*, not a terminal tool. (For terminal/scripting use cases, use the `apfel-cli-tools` skill instead — these two apps both launch `apfel --serve` on localhost under the hood, so anything true of the on-device model there — 4,096-token context, no cloud calls, refuses rather than hallucinates — is true here too.)

## apfel-quick — global-hotkey AI overlay

A Spotlight-style popup: press `Ctrl+Space` anywhere on the Mac, type a question, the answer streams in and is automatically copied to the clipboard. Works with Wi-Fi off.

**What it's for:** the "quick answer, back to work" case — translations, unit conversions, facts, rephrasing, grammar fixes, regex, short code snippets, and *local* arithmetic (a built-in parser handles math like `54,34*6-(435353)` or `sqrt(2)*pi` instantly, without invoking the LLM at all — supports `+ − × ÷ ^ %`, parens, unary minus, European decimals, `sqrt sin cos tan log ln abs floor ceil round`, `pi`, `e`).

**What it's explicitly not for:** deep research or long multi-turn conversations — the maker's own positioning is "won't replace ChatGPT for research, but you don't need that most days." Don't oversell it as a full assistant replacement.

**Install:**
```bash
brew install Arthur-Ficial/tap/apfel-quick
# or download the signed/notarised .zip from
# https://github.com/Arthur-Ficial/apfel-quick/releases/latest
```
Unzip → drag to Applications → open. Zero cleanup to uninstall (drag to Trash).

**Requirements:** macOS 26 Tahoe, Apple Silicon (M1+), Apple Intelligence enabled. Free, MIT, 176 tests.

**Troubleshooting pointers:**
- No network calls ever happen — if the user expects it to "look things up" on the live web, that's out of scope (that's what `apfel-mcp` is for, in the CLI ecosystem, not this app).
- If the hotkey doesn't fire, check macOS Privacy & Security → Accessibility/Input Monitoring permissions were granted at first launch.

## apfelpad — formula notepad with inline AI

⚠️ Experimental (v0.3.x+ as of this writing) — expect rough edges, and mention that to the user if they hit something odd. File issues at https://github.com/Arthur-Ficial/apfelpad/issues.

A native macOS markdown notepad where **on-device AI is a first-class formula**, the same way `=SUM(...)` is a formula in a spreadsheet. Type `=apfel("summarize this")` inline in a markdown document, press Return, watch the result stream in as a pale-green span. The document itself stays plain `.md` on disk — open it in any other editor and the formula syntax is just visible text.

### The formula language (21+ functions, Turing-complete, reactive)

Every formula is `=name(args)`, results are cached, and formulas **compose** — any formula's evaluated result can be an argument to another (depth-capped at 10 to guarantee termination). This is enough to express arbitrary computation via `=if` branching + `=ref` document lookup + nesting.

Full function reference, grouped, is in `references/formulas.md` — read it before writing or debugging apfelpad formulas rather than guessing syntax. Categories: on-device AI + math (`=apfel`, `=math`), dates/time, Google-Sheets-style text functions, document references (`=ref`, `=count`), reactive input variables (`=input`/`@name`/`=show`), logical functions, extended text/math/date functions, type-checking.

Two formulas the user will reach for constantly:

```markdown
=apfel("prompt", seed?)     # on-device LLM call; seed → reproducible output
=math(365*24)                # arithmetic with unit/currency-ish annotation support
```

### Document references — the killer feature

Name a heading, then pull its whole section elsewhere in the doc with `=ref(@#anchor)`. Anchors are slugified section titles (`# Project brief` → `@project-brief`), case-insensitive, and stay in sync — edit the source heading's content and every `=ref` pointing at it updates.

```markdown
# Project brief
Build a formula notepad for thinking on macOS.

# Summary
Goal: =ref(@#project-brief)
```

### Reactive variables — spreadsheet semantics in prose

`=input(name, type, default?)` declares a document-level variable; `=show(@name)` echoes its current value; any formula referencing `@name` recomputes live when it changes (e.g. typing into an inline number field updates every downstream `=math(@hours * @rate)`). See the freelance-calculator example in `references/formulas.md` if the user wants a worked template.

**Install:**
```bash
brew install Arthur-Ficial/tap/apfelpad
# or:
curl -fsSL https://raw.githubusercontent.com/Arthur-Ficial/apfelpad/main/scripts/install.sh | zsh
# or download the signed/notarised .zip from
# https://github.com/Arthur-Ficial/apfelpad/releases/latest
```
Requires `apfel` on PATH (apfelpad launches `apfel --serve` on `localhost:11450` at startup) — install `apfel` first if it isn't already there. Note: `=math()` and the non-AI text/date functions all work even without `apfel` installed; only `=apfel(...)` calls need the on-device server running.

**Privacy:** the only network call apfelpad ever makes is an optional, togglable GitHub update check. All AI calls stay on `localhost`.

## Where these two fit in the wider apfel family

Both are consumer-facing surfaces on the same on-device model that the `apfel-cli-tools` skill covers for terminal use. If the user's request is really about scripting, piping, or an HTTP server rather than a native app experience, point them at that skill instead. Sibling GUI apps that exist in the ecosystem but aren't covered here in depth: `apfel-chat` (multi-conversation chat client) and `apfel-clip` (menu-bar clipboard AI actions) — mention them only if the user's need doesn't fit apfel-quick or apfelpad.
