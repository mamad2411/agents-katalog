---
name: draft-park
description: Park a draft message/text in macOS Notes for the operator to review and edit, then read it back before acting (e.g. before sending to a real person). Notes is the source of truth (AppleScript CRUD, iCloud-synced, provenance-stamped with the Claude Code session UUID); Stickies is a best-effort view-only desktop mirror. Use whenever you draft something a human should confirm/edit before it is sent or committed — messages, replies, announcements, anything outbound. TRIGGERS - park this draft, park the message, hold this draft, let me edit first, draft for my approval, save to notes for review, read back the draft.
allowed-tools: Bash, Read
---

<!-- SKILL-PLUGIN-ROOT-OK: explains why this variable must not be used here -->

# draft-park — human-in-the-loop drafts via macOS Notes

> Renamed from `draft-hold` on 2026-08-12. Invoke as `/notes-commander:draft-park`; there is no `draft-hold` alias. Evolution-log entries dated before the rename keep the old name — that is the accurate historical record, not drift.

> **Self-Evolving skill** — if macOS Notes/Stickies behavior drifts from what's below, fix this SKILL.md and the shared engine `scripts/lib/notes-core.ts` (+ a case in `notes-core.test.ts`); see the Post-Execution Reflection at the bottom.

When you compose something a human should confirm or edit before it goes out (a message to a real person, an announcement, a commit body), **don't keep it only in chat** — park it in macOS Notes so the operator can edit it on any device, then read it back and act on the edited version.

**Resolve the entrypoint first** — `$CLAUDE_PLUGIN_ROOT` is NOT a shell variable and expands to empty here (it exists only inside plugin manifests and hook/MCP subprocesses; see the `$CLAUDE_PLUGIN_ROOT` invariant in the plugin CLAUDE.md). Never glob the version cache either — it retains orphaned versions. Use the resolver:

```bash
DP="$(cc-plugin-root notes-commander)/skills/draft-park/draft-park.sh"
```

`draft-park.sh` is a thin shim that `exec`s the **Bun/TypeScript engine** `scripts/draft-park.ts`, built on the plugin's shared `notes-core` engine (which also powers `notes-inventory`/`notes-export`/`notes-organize`).

## Formatting is handled in code — just write naturally

The engine (formatter in `scripts/lib/notes-core.ts`, unit-tested in `notes-core.test.ts`) normalizes your input into Notes HTML, so you never hand-manage line breaks:

- **Prose reflows.** Consecutive non-blank lines join into ONE paragraph that Notes soft-wraps to the reader's screen. Accidental hard-wrapping (text pre-wrapped at ~80/100 cols) is corrected automatically — it can no longer become a permanent mid-sentence break. Blank lines are the only breaks that matter.
- **A blank line = a new paragraph/section.** That is the one authored break.
- **Bullet lists become NATIVE Notes lists, and they nest.** Lines starting `-`, `*`, `+`, `•`, `·` are emitted as real `<ul>`/`<li>`, so Notes draws its own bullet glyph and indents sub-items natively — indent a child by two spaces (a tab counts as one unit) and it nests. The marker is consumed; do not expect to see your own `-`. **Numbered and lettered markers (`1.`, `2)`, `a.`) deliberately keep the literal-marker form**, because Notes' own numbered list renumbers from 1 and would silently rewrite an author's `2)` as `1.`. A wrapped continuation line (indented, no marker) still joins back to its item, and its own indentation does not move the item.
- **Markdown emphasis becomes REAL RICH TEXT — do not hand-strip it.** Notes is a rich-text editor, so `**bold**` → bold, `*italic*` / `_italic_` → italic, `` `code` `` → monospaced, `~~strike~~` → struck, and `#`/`##`/`###` headings → a bold line with the markers consumed. Write in the house markdown style and it arrives formatted. Two deliberate exceptions keep technical prose safe: an **identifier can never open or close emphasis** (`analytics.model_predictions and nan_policy` stays literal, as does `2*3*4`), and anything inside backticks or a fence keeps its markers verbatim.
- **Verbatim / columnar / code blocks** — wrap them in a ` ``` ` fence. Every line inside is preserved exactly and rendered monospace with spaces held (via `&nbsp;`), so columns and IDs line up **in the Notes UI**. (Note: `get --body-only` returns the _sendable_ plain text and collapses inter-column runs to single spaces; if exact alignment must survive to the recipient, send an attachment/screenshot.)

## Hardening (verified failure modes this engine guards)

- **Silent-failure detection** — `new` asserts Notes returned a real note id (`x-coredata://…`); on recent macOS, osascript can exit 0 yet create nothing. If that happens you get a loud `✗ SILENT-FAILURE` instead of a phantom "success".
- **Bounded retry** — transient AppleEvent errors (`-600`/`-1712`/"not running") retry with backoff; permission/syntax errors fail fast.
- **Read-back verify (default ON)** — after `new`, the note is read back and checked for entity leaks and content presence. `--no-verify` skips (rarely needed).

## Workflow

1. **Park the draft** (body on STDIN):

   ```bash
   CLAUDE_SESSION_ID="$CLAUDE_CODE_SESSION_ID" "$DP" new "<title>" --project "<repo-or-context>" <<'EOF'
   Hi <name> — <your drafted message>...
   EOF
   ```

   Creates/replaces a note in the **"Claude Drafts"** folder with a provenance footer (session UUID + project + timestamp). Tell the operator: _"Draft is in Notes → Claude Drafts → <title>; edit it there, then tell me to send."_

2. **(Optional) desktop mirror** — `"$DP" sticky "<title>"` pops a view-only Stickies note (needs Accessibility permission). Notes stays authoritative.

3. **Read it back** before acting — ALWAYS re-read, since the operator may have edited it:

   ```bash
   "$DP" get "<title>"              # full note (heading + message + provenance footer)
   "$DP" get "<title>" --body-only  # JUST the sendable message (no heading, no footer)
   ```

   Use `--body-only` to get exactly the text to send/paste. Add `--for whatsapp` to convert markdown
   into the channel's own syntax, and `--copy` to put the result straight on the clipboard so there is
   no hand-selection step to get wrong:

   ```bash
   "$DP" get "<title>" --for whatsapp --copy   # sendable text → clipboard, warnings on stderr
   ```

   `--for` and `--copy` both imply `--body-only`. stdout is always exactly the sendable bytes;
   warnings go to stderr, so piping stays clean. Show the operator the exact current text, get explicit go-ahead, then send/commit.

4. `"$DP" list` enumerates parked drafts.

## macOS quirks this skill handles for you

- **Quote serialization**: Notes' AppleScript `body` getter re-emits every `"` as the _semicolon-less_ legacy entity `&quot` (verified 2026-06-29). We decode with `textutil` (a real HTML parser) instead of `sed`, so `&quot`/`&amp`/`&lt` etc. round-trip back to literal characters. Never hand-roll entity decoding here. The read-back verify now DETECTS a drift here automatically (`✗ ENTITY-LEAK`). **A real HTML parser is not sufficient on its own** (fixed 2026-07-20): because the stored form is semicolon-LESS, a note holding `Write-Host "x"; $y` comes back raw as `Write-Host &quotx&quot; $y`, and textutil reads the closing `&quot` plus the author's own `;` as one entity — silently eating the semicolon, so it round-tripped as `Write-Host "x" $y`. That corrupts most staged PowerShell/C/Java/JS with no error, which is fatal for a skill whose job is staging text a human will SEND. `terminateLegacyEntities()` in `notes-core.ts` now appends the `;` to every bare entity before decoding, so a following literal `;` stays literal. This is safe unconditionally because Notes escapes every `&` it stores (an author's literal `&amp;` comes back as `&ampamp;`), so a terminated entity in Notes output can only ever be bare-entity + the author's semicolon.
- **UTF-8 decode needs an explicit charset**: `textutil -format html` assumes Latin-1 when the HTML has no charset declaration, mojibaking every non-ASCII character (关于 → `å…³äºŽ`; verified 2026-07-02 with a Chinese draft). `htmlToText` therefore prepends `<meta charset="utf-8">` before piping to textutil — keep that prefix.
- **Note name = first body line, TRUNCATED**: Notes names a note after its first line, ignoring any title you "set". `new` therefore prepends the title as a bold first line so `get`/`list`/replace can find it by title. Pass the message body only on STDIN. **But Notes truncates a long first line** to a capped `name` ending in an ellipsis `…` (verified 2026-07-20: a 66-char title stored as `…(2026-07-20…`), so an exact `whose name is <title>` lookup MISSES long-titled notes. The engine handles this: `new` reads its note back **by id** (not title) for the verify, and `get`/`sticky`/`move-note` resolve a title to a note **truncation-tolerantly** via `noteNameMatchesTitle()` (exact, else the stored name is the title truncated with a trailing `…`). Never rely on exact-name AppleScript matching for a possibly-long title.
- **Links: the SETTER keeps them, the GETTER strips them** (verified 2026-08-05). Write `[label](url)` and the engine emits `<a href>`; Notes stores a genuine link attribute (confirmed by decompressing the note's `ZICNOTEDATA.ZDATA` protobuf in `NoteStore.sqlite` — the href sits in the attribute run while the visible-text run holds only the label). But AppleScript's `body` **getter returns `<u>label</u>` with no href**, for links Notes itself made too. Consequences: (1) `get`/`get --body-only` shows link TEXT and silently loses the URL — never round-trip a linked note through `get` and re-`new` it, the links will be gone; (2) read-back verify is link-blind by construction, so `renderInline`'s unit tests are the only place an href is observable — do not "harden" verify by asserting hrefs, they never appear. Only `http(s)` and `mailto` become anchors; any other scheme (`javascript:`, `file:`, a bare path) renders as literal text.
- **Proportional prose, monospace only in fences**: prose paragraphs render in Notes' normal proportional font (so a long line reflows). Only ` ``` ` fenced blocks are wrapped in `<tt>` (Notes' "Monostyled" face) with spaces held as `&nbsp;`. The mono face is fixed by Notes — it is _not_ the global `NSFixedPitchFont`, which governs TextEdit-style apps, not Notes.

## Getting the session UUID for provenance

**The Bash tool already has it**: Claude Code exports `CLAUDE_CODE_SESSION_ID` (verified 2026-08-05 — matches the `~/.claude/projects/<slug>/<uuid>.jsonl` name). So just forward it, and don't go hunting:

```bash
CLAUDE_SESSION_ID="$CLAUDE_CODE_SESSION_ID" "$DP" new "<title>" …
```

Only if that variable is empty: the `statusline-tools:session-info` skill reports the UUID, or read the newest `*.jsonl` under `~/.claude/projects/<project-slug>/`. If genuinely unavailable, omit it (the footer drops the token — never write a placeholder).

## Rules

- **Never send/commit from memory** — always `get` the note first; the operator may have changed it.
- **Never hand-copy the note out of the Notes UI.** The provenance footer is selectable text sitting
  right underneath the message; on 2026-08-17 it was pasted into a clinic WhatsApp group, disclosing
  `Parked by Claude Code`, a session UUID and a repo path. Use `--body-only` (or `--copy`), which now
  also REFUSES to emit any text still containing the footer.
- **Write URLs inline, never as `[label](url)`, in anything you intend to SEND.** Notes stores the
  href but its AppleScript getter strips it, so the URL cannot come back. `new` refuses such links
  with the inline form to use instead; `--allow-lossy-links` overrides for a note meant to be read in
  Notes rather than sent.
- Notes is the source of truth. Stickies cannot be read back (no AppleScript dictionary), so never treat a sticky as the live draft.
- There is no scriptable deep-link to a specific note (`open x-coredata://…` fails; `applenotes:` links are UI-only) — reference drafts by **folder + title**.
- First run prompts once for Automation permission to control Notes.

## Evolution log

- **2026-09-09 — a rich-text target was being fed escaped markdown, and nobody noticed until a report was read.** _Trigger_: the operator read a parked weekly scrum note and said "`**` marking shouldn't be used but bold them". _Measurement, from the note's own stored bytes rather than the UI_: decompressing `ZICNOTEDATA.ZDATA` for the parked note found **274 literal `**` and 9 literal `#` heading markers**. _Root cause_: `renderInline()` promoted `[label](url)` to an anchor and passed **everything else through `escapeHtml()`**, so every emphasis character survived as a visible glyph. This was never a decision — the formatter grew link support in 2026-08-05 and emphasis was simply never added, while the docs described the escaping as the design. The cost fell on the author, who either hand-stripped markup or shipped it visible; the 2026-08-17 incident log already recorded a real message going out "studded with 20 literal `**`" and the fix then was `--for whatsapp`, i.e. the SEND path, leaving the Notes path untouched. _Fix_: new pure `renderMarkup()` (bold, italic, inline code, strikethrough) applied to already-escaped text so escaping still governs safety, plus `HEADING_RE` promoting ATX headings to bold runs and splitting them into their own paragraph. **Two anchoring decisions are the load-bearing part**, because the naive version corrupts exactly the prose this plugin is used for: `_` emphasis requires a NON-word character before the opener and NO word character after the closer, so `analytics.model_predictions and nan_policy` cannot italicise the span between two identifiers; `*` is anchored the same way so `2*3*4` survives; and code spans are lifted out first (U+E000 placeholder, not a control character — the linter rejects those) so `` `a ** b` `` stays literal. `#600` is an issue reference, not a heading: the ATX rule requires a following space. _Evidence_: **12 new unit tests, 39 → 51 pass, 0 fail**, and each fix **mutation-proven** rather than assumed — removing the `renderMarkup` call kills 7 tests, removing the underscore anchor kills exactly the identifier-corruption test, removing the heading split kills 2, and the restored baseline returns to 51/0. _Not changed_: fences stay verbatim, `get --body-only` still returns plain sendable text, and the link getter is still lossy (Rule 11 unaffected).

- **2026-08-17 — three ways a parked draft reached a recipient WRONG, all found in one afternoon after
  a real clinical message went out damaged.** _Trigger_: a message to a dental clinic's reviewer
  arrived truncated to 38% of its length, carrying internal provenance, and studded with 20 literal
  `**`. _Root causes and fixes_:
  1. **Silent truncation, and it was injection-shaped.** `bodyOnly()` broke at the FIRST line matching
     `/^------\s*$/`, but the footer it strips is always LAST — so an author's dash rule cut the
     message there (1,760 of 4,635 chars). The Notes UI showed the whole note, and the sendable text
     is only ever read by the human pasting it, so nothing looked wrong. The severity is WHOSE text
     can trigger it: drafts quote clinician comments, patient transcripts and Drive comments verbatim,
     so a dash rule written outside this machine could choose the cut point. Now `findFooterStart()`
     scans from the END and requires BOTH signals (the rule AND a following `Parked by Claude Code`
     line), so prose dashes are ignored and a quoted footer cannot pull the cut upwards.
  2. **URLs cannot survive a markdown link, and the existing verify only caught it by luck.** Parking
     `[the rules portal](https://…)` and reading back yields `the rules portal` — URL absent, not
     mangled. `contentPresent()` compares only the first **24 characters** of the first line, so it
     catches a link near the start and passes GREEN on one further in (measured both ways). `new` now
     REFUSES markdown links and prints the inline form to use; `--allow-lossy-links` escapes it and
     relaxes the content check, loudly.
  3. **Markdown is not what the channel speaks.** `--for whatsapp` converts `**bold**` → `*bold*`,
     headings → bold, and flattens `[label](url)` → `label: url`, warning on stderr about anything it
     cannot map (inline code, tables). Fenced blocks are left verbatim. `--copy` writes the sendable
     text to the clipboard, removing the hand-copy step that leaked the footer, and says so rather
     than silently replacing the clipboard.
     _Evidence_: 25 new unit tests (64 total, 0 fail), each proved in both directions, plus a mutation
     check confirming the pre-fix code genuinely exhibits failures 1 and 2 — so the regression tests are
     not vacuous.

- **2026-08-12 — renamed `draft-hold` → `draft-park`.** _Trigger_: operator directive — "park" is the verb the skill's own docs and triggers already used ("park it in macOS Notes", "park the message"), while "hold" read as a queue/blocking state. _Scope_: skill dir `skills/draft-hold/` → `skills/draft-park/`, shim `draft-hold.sh` → `draft-park.sh`, engine `scripts/draft-hold.ts` → `scripts/draft-park.ts`, call-site variable `$DH` → `$DP`, and every live cross-reference (plugin CLAUDE.md/README/plugin.json, marketplace.json, root + plugins CLAUDE.md, `scripts/cc-plugin-root` usage example, macos-font-defaults' Notes-mono cross-reference, and the operator's live `~/.claude` instructions). **No `draft-hold` alias exists** — the slash command is `/notes-commander:draft-park` only. _Deliberately NOT rewritten_: CHANGELOG.md, the entries below this one, and the itp-hooks skill-plugin-root-guard forensics — those describe events that happened under the old name, and back-dating a rename into them would make the incident record wrong. _Behavior_: unchanged — same subcommands, same flags, same "Claude Drafts" Notes folder, so previously parked notes are still found by `get`/`list`. The one content change: the provenance footer now reads `Parked by Claude Code` (was `Held by`). Nothing parses it — `bodyOnly()` cuts at the `------` separator — so notes written under the old wording read back identically.
- **2026-08-05 (b) — the skill could not find its own entrypoint (`exit 127`).** _Trigger_: `/notes-commander:draft-hold` invoked from another repo died on `(eval):1: no such file or directory: /skills/draft-hold/draft-hold.sh`. _Root cause_: this SKILL.md told the caller to use `DH="$CLAUDE_PLUGIN_ROOT/skills/draft-hold/draft-hold.sh"`, but **`CLAUDE_PLUGIN_ROOT` is not a shell variable**. Claude Code substitutes the exact literal `${CLAUDE_PLUGIN_ROOT}` (braces REQUIRED — the helper is `e.replace(/\$\{CLAUDE_PLUGIN_ROOT\}/g, pluginPath)`) inside plugin manifests, and injects the var into hook/MCP subprocess envs — never into the Bash tool. The bare `$…` spelling used here is unsubstitutable on every path, so it reached zsh as an unset var, expanded to empty, and produced an absolute-looking `/skills/…` path — which reads like a missing file, not a missing variable. Two upstream causes made it likely: the repo's own `advanced-topics.md` and `lifecycle-reference.md` documented the rule **exactly backwards** ("available in skill loading, NOT in hooks" — it is the reverse), and the recovery path was equally unsound: globbing the version cache and taking the highest semver picked `23.4.1`, which is marked `.orphaned_at` (live was `23.5.0`). _Fix_: added `scripts/cc-plugin-root` (reads `~/.claude/plugins/installed_plugins.json`, tolerates both registry schemas, jq with a python3 fallback, symlinked into `~/.local/bin/`); this SKILL.md now resolves `DH="$(cc-plugin-root notes-commander)/skills/draft-hold/draft-hold.sh"`; both reference docs corrected; the stale "L3 cache strips `scripts/`" claim retired. Also stopped the sibling waste in this same flow: `CLAUDE_CODE_SESSION_ID` is already exported into the Bash env, so the provenance UUID no longer needs hunting. _Evidence_: resolver returns the live `23.5.0` path via both jq and python3 backends and under both registry shapes; negative cases exit 1/2 with actionable stderr; the resolved `draft-hold.sh` and `scripts/draft-hold.ts` both exist.
- **2026-08-05 (a) — every URL had to be shown naked, because the formatter escaped anchors.** _Trigger_: staging a weekly report whose 16 PR references made the prose unreadable; the operator asked for `#470`-style link text and supplied a screenshot of a working link in Notes, proving Notes supports them. _Root cause_: `escapeHtml()` was applied to every prose and list line, so an `<a href>` could only ever render as literal `&lt;a href…`. _The trap that nearly ended the investigation_: a probe note written with `<a href>` read back as `<u>#470</u>`, which looks exactly like "Notes stripped the link" — I nearly concluded the setter was broken. The operator's OWN hand-made link read back as `<u>link text</u>` too, which is what exposed the real shape: the **getter** is lossy, not the setter. Confirmed by decompressing `ZICNOTEDATA.ZDATA` from `NoteStore.sqlite` — the probe note's visible text was `See #470 and #472.` while the hrefs sat in the attribute run. A read-back-only check would have produced a false negative and no links. _Fix_: added pure, unit-tested `renderInline()` promoting `[label](url)` → `<a href>` at the three prose/list call sites (fences stay verbatim, so a fenced `[x](url)` renders literally); `http(s)`/`mailto` allow-list so a `javascript:` link can never be minted into a document a human will click. _Evidence_: 6 new unit tests (**39 pass, 0 fail**), plus a live round-trip verified against the SQLite protobuf — 16 hrefs stored, zero URLs leaked into visible prose.
- **2026-07-27 — a lead-in line silently ate the list under it.** _Trigger_: staging a real reply draft, `解决办法有两个，你倾向哪个？` immediately followed by two `-` bullets (no blank line) came back from `get --body-only` as ONE run-on line, bullets and all. Hit twice in the same session, in two different notes. _Root cause_: `renderTextBlock()` classified each blank-line-delimited paragraph by testing **`p[0]` only** — so a paragraph whose first line is prose was rendered wholly as prose, and `reflowJoin()` folded the following `-`/`1.` markers into it. The list was destroyed with no error. This contradicted SKILL.md, which promised list markers "each stay on their own line", and left an undocumented "you must leave a blank line before a list" rule that authors could only learn by being bitten. _Fix_: split each paragraph at the FIRST line matching `LIST_RE` — lead-in lines reflow as prose, everything from the first marker on renders per-item via the new extracted `renderListItems()` helper (also removes the duplicated item-grouping loop). All three shapes now work: all-prose, all-list, and lead-in-then-list. _Evidence_: 3 new unit tests (CJK lead-in + bullets, English lead-in + numbered list, multi-line lead-in that must still reflow before splitting); **33 pass, 0 fail**.
- **2026-07-20 (b) — unified the truncation-match rule into one home (DRY).** The 2026-07-20 (a) fix left the exact-then-truncated matching rule in TWO places: `noteNameMatchesTitle()` in `notes-core.ts` (used by draft-hold) AND a hand-copied AppleScript scan inside `notes.ts` `OSA_MOVE`, guarded only by a "keep the two rules in step" comment. _Fix_: added pure `matchNoteIds(index, title)` to `notes-core.ts` (exact ids first, else truncation-tolerant; returns every match so callers can flag ambiguity). `move-note` now indexes the source folder (`OSA_NOTE_INDEX_BY_PATH`), resolves the title in TS via `matchNoteIds`, and moves by **id** (`OSA_MOVE_BY_ID`); the name-matching AppleScript is deleted. draft-hold's own resolver + dedup route through `matchNoteIds` too. One rule, unit-tested (5 new tests, 30 total), impossible to drift. Invariant recorded in the plugin CLAUDE.md (the `matchNoteIds` entry).
- **2026-07-20 (a) — long titles broke read-back verify + `move-note` (name truncation).** _Trigger_: parking a 66-char draft ("CPC Scanners — Procurement Intelligence & Deliverables (2026-07-20)") returned a false `✗ CONTENT-MISMATCH`, and `move-note "<that title>"` then failed with "note not found in source folder", even though the note existed and its body was correct. _Root cause_: macOS Notes stores a long first-line `name` TRUNCATED with a trailing `…`, so `new`'s read-back (`body of note <title> of folder`) and `move-note`'s `whose name is <title>` both looked up a name that no longer equalled the title. _Fix_: added the pure, unit-tested `noteNameMatchesTitle()` + `NOTES_NAME_ELLIPSIS` to `notes-core.ts` (exact, else truncated-prefix match); `new` now verifies **by id** (`OSA_GET_BY_ID`) and dedups older copies via a JS-side folder index; `get`/`sticky` resolve title→id truncation-tolerantly; `move-note` (notes.ts) falls back to a truncated-prefix scan that captures matches **by id** (a live `notes of src` reference held past the loop throws `-1728`). _Evidence_: a 125-char-title probe now creates (clean id, no CONTENT-MISMATCH), `get`s its body, and `move-note`s across folders — all green; 5 new unit tests (25 pass total). Verified live on macOS Notes.
- **2026-07-18 (b) — migrated into notes-commander + hardened.** The standalone draft-hold plugin was folded into the new `notes-commander` plugin as one of its skills; formatting + process wrappers moved to the shared `scripts/lib/notes-core.ts` engine. Added, per a web-researched audit of recent macOS AppleScript failure modes: silent-no-op detection (`isNoteId` on create — osascript can exit 0 yet create nothing on macOS 26), bounded retry on transient AppleEvent errors (`-600`/`-1712`), and a default-on read-back verify (`entityLeaks` + `contentPresent`). All pure helpers unit-tested (16 tests in `notes-core.test.ts`).
- **2026-07-18 (a) — hard-wrapped prose became forced mid-sentence breaks.** A long bilingual briefing was passed with each paragraph pre-wrapped at ~100 chars; because the old bash `new` made each input line its own Notes paragraph (all wrapped in `<tt>`), the reader saw mid-sentence line breaks that did not reflow. _First fix (insufficient)_: a "one line per paragraph" caller contract — but that only works if every caller remembers it. _Real fix_: reimplemented the engine as **Bun/TypeScript**, enforcing the formatting in code so the failure is impossible: prose blocks REFLOW (consecutive lines join; blank line = paragraph), list markers stay per-item, and only ` ``` ` fenced blocks are preserved verbatim/monospace (spaces held as `&nbsp;`). Verified by unit tests + a live Notes round-trip.

## Post-Execution Reflection

After holding or sending a draft, check before closing:

1. **Did read-back match what Notes shows?** — if entities/quotes leaked (e.g. `&quot`), the decode path drifted; the verify step should have caught it — fix the `textutil` step in `notes-core.ts`, never hand-roll sed.
2. **Did `get`/`list` find the note by title?** — if not, the name==title assumption broke; fix the title-prepend in `new`.
3. **Did Notes/Stickies change behavior?** — update the macOS-quirks section so the next run doesn't rediscover it.

Only update if the issue is real and reproducible — not speculative.
