---
name: telegram-rich-messages
version: 2.1.1
description: Use when sending Telegram Bot API rich messages.
platforms:
  - linux
  - macos
metadata:
  hermes:
    tags: [telegram, rich-messages, bot-api, telegram-bot]
    related_skills:
      - [telegram-advanced-config, communities/misc/telegram-advanced-config.md]
---

## When to use

Use when sending, editing, or debugging messages through the Telegram Bot
API, especially when the operator expects native rich rendering (tables,
task lists, dropdowns, LaTeX) rather than plain fallback text. Load before:

- building a message that mixes a markdown table, task list, `<details>`,
  or math block
- reporting a "table won't render" bug (check guard 1, guard 2, latch-off
  below before blaming config)
- choosing `rich_messages` / `rich_drafts` config values

# Telegram Rich Messages (Bot API 10.10)

Verified from code (not docs). Source: `plugins/platforms/telegram/adapter.py` (v0.22.2), tests/gateway/test_telegram_rich_messages.py. Where docs conflict with code, CODE WINS.


## CONFIG

```yaml
platforms:
  telegram:
    extra:
      rich_messages: true   # REQUIRED - enables sendRichMessage path
      rich_drafts: false    # keep false unless need streaming preview rich
```

Set via CLI (safe, auditable; agent cannot write raw config.yaml):

    hermes config set platforms.telegram.extra.rich_messages true
    hermes config set platforms.telegram.extra.rich_drafts false

[PATH CORRECTION] Some docs write "gateway.platforms.telegram.extra". Adapter actually reads `platforms.telegram.extra` (`self.config.extra`). Verify: `hermes config get platforms.telegram.extra`.

Default rich_messages: false is DELIBERATE: native tables harder to copy as plain text. On = trade copy-ease for render beauty. Not a bug.

LIVE CONFIG: rich_messages true, rich_drafts false. Same namespace also has allow_cjk_rich_messages, require_mention - extra knobs.


## WHEN RICH IS USED (TRIGGER)

Rich ONLY for final replies / new messages, and ONLY if content is one of these (`_needs_rich_rendering`):

  - Pipe table      -> has separator row (| :--- | ---: |)
  - GFM task list   -> "- [ ]" / "- [x]" at line start
  - Collapsible     -> "<details>" / "<summary>" at line start
  - Math block      -> contains "$$"

Plain prose, bold/italic, simple lists -> STILL legacy MarkdownV2 path. Deliberate: weight & spacing consistency across clients. Don't be surprised plain text messages don't go "rich".


## SUPPORTED SYNTAX

A. Collapsible / dropdown

  <details>
  <summary>Title (click open/close)</summary>

  Hidden content.
  - Point 1
  - Point 2
  </details>

  Tags at line start so detected.

B. Native grid table

  | Feature | Status | Notes |
  | :------ | :----- | :---- |
  | Gateway | Active | native table |

  Needs separator row. Without it, not a table.

C. Task list

  - [x] done
  - [ ] not yet

D. Math LaTeX

  $$f(x) = \int_{0}^{\infty} \frac{x^3}{e^x - 1}\,dx = \frac{\pi^4}{15}$$


## TWO SILENT CRASH GUARDS (MOST IMPORTANT - absent in old docs)

Adapter DELIBERATELY refuses rich for two shapes. If hit, message SILENTLY falls back to raw text — not a config error, a crash guard. Don't waste time debugging.

Guard 1 - Math INSIDE <details> -> Telegram Desktop crash
  $$, \[ \], \( \), or \sum \frac \alpha \int \sqrt \lim \infty etc
  INSIDE a <details> block triggers Telegram Desktop 6.9.1 crash
  (tdesktop#30808). Bot API accepts it anyway — so Hermes cancels rich
  early. RULE: separate math from <details>. Math OUTSIDE <details> = safe.

Guard 2 - CJK text -> glyph overlap
  CJK text (Hiragana/Katakana, CJK Ext A, CJK Unified, Hangul, CJK Compat,
  astral Han) causes glyph overlap on Telegram Mac/Desktop (#47653).
  Legacy renders clean, so rich is skipped.
  RULE: Chinese/Japanese/Korean content -> don't expect rich, and that's normal.

Other guards:
  - Empty / whitespace only                    -> legacy
  - > 32,768 chars (RICH_MESSAGE_MAX_CHARS)    -> legacy chunking
  - Bot not async-capable                       -> legacy
  - Metadata "expect_edits"                     -> legacy
    (message to be edited while streaming; preview must be born non-rich
     until finalize)


## NEWLINE NORMALIZATION (important, often confuses)

Standard markdown treats single \n as soft break -> lines merge into one paragraph in sendRichMessage. Adapter fixes (`_rich_normalize_linebreaks`):

  - single \n       -> hard break ("  \n", two spaces + newline)
  - \n\n paragraph -> left alone
  - fenced code + pipe-table blocks -> VERBATIM (no space injected, so
    table pipes don't break)

So: multi-line output stays multi-line; tables stay tables.


## FALLBACK BEHAVIOR

Hermes never loses a message:

  Condition                      Action
  -----------------------------  ---------------------------------
  Permanent error (BadRequest)   fallback to MarkdownV2 - message sent
  Endpoint missing (PTB/404)     fallback + LATCH rich off (never retry)
  Transient error (network/timeout) NO legacy resend (prevent dupes)
                                -> success=False

If table won't render as grid despite rich_messages: true, check:
  (1) content actually triggers?
  (2) hit a crash guard?
  (3) hit latch-off from earlier error? Restart gateway clears latch.


## STREAMING DRAFT (rich_drafts)

  false (default): streaming preview PLAIN (legacy), then final reply
                   RICH via sendRichMessage. Recommended.
  true           : preview uses sendRichMessageDraft - but Telegram
                   Desktop/macOS can overlay rich frames until chat
                   redraws (flicker).
  - Draft DM-only; group/topic auto-fallback to edit-based.
  - Capability fail -> draft latch off, that frame falls to legacy.


## MARKDOWNV2 FALLBACK (when rich unavailable)

MarkdownV2 has no tables. Adapter normalizes:

  - Small table (2-4 cols) -> row-group bullets (bold heading + "Col: value")
  - Large/wide table      -> fenced code block with aligned columns


## pretty_tables - DON'T TRUST BLINDLY

Hermes docs mention `telegram.pretty_tables: false` to disable table
normalization. BUT in adapter v0.22.2 key has NO implementation (only in
doc files, not .py). Treat as non-functional until proven otherwise.


## PITFALLS

1. Copy-paste: native tables hard to copy as plain text on old clients.
   If user needs text-copy, turn off rich_messages.
2. Silent guard: math-in-details & CJK kill rich with no warning. Check
   these first before reporting a bug.
3. Strict trigger: plain prose never becomes rich. Don't test with plain
   sentences.
4. Config guard: agent CANNOT write raw config.yaml (blocked). Use
   "hermes config set ..." - official path, safe & auditable.
5. Restart required after config change.


## QUICK TEST (avoids both guards)

  | A | B |
  | :--- | :--- |
  | 1 | 2 |

  - [x] checked

No <details>, no math, no CJK. If table renders as grid -> rich path fully works.


## NON-TRIGGER FEATURES THAT RENDER TOO

Once a message enters rich path (has one of the 4 triggers), other
markdown constructs in the SAME message also render native - even though
not triggers themselves.

  VERIFICATION STATUS: reported passing on client by user in full 9-feature
  test (one message: table + task list + details + math + heading +
  blockquote + nested list + inline formatting + link).
  This is USER REPORT, not independent code verification - adapter only
  has 4 explicit triggers (_needs_rich_rendering), rest delegated to
  Telegram parser.

  Feature                          Own trigger?  Renders along?
  -------------------------------  -------------  -------------
  Heading # / ## / ###             no             yes (reported)
  Blockquote >                     no             yes (reported)
  Nested list (indent)             no             yes (reported)
  Bold / italic / inline code      no             yes (reported)
  Link [text](url)                 no             yes (reported)
  Table / task list / details/math YES            yes

  INFERENCE (not separately tested): message WITH NO trigger falls to
  legacy MarkdownV2 - headings likely appear as raw "##" text. Derived
  from design (_needs_rich_rendering only detects 4 shapes), not directly
  verified.


## TRAP WHEN BUILDING TESTS

Don't mix two guard-hit shapes in one test message if assessing another
feature - guard kills the WHOLE message, not just part:

  - X  Math INSIDE <details>      -> entire message back to legacy
  - X  Any one CJK char anywhere -> entire message back to legacy

Separate tests: details WITHOUT math, and ZERO CJK text.


## CODE MAP (for debug)

  Symbol                                        Location          Function
  --------------------------------------------  ----------------  ----------------------------
  _needs_rich_rendering                          adapter.py ~1248  pick rich vs legacy
  _rich_content_ok                               adapter.py ~1270  guard crash/limit
  _rich_eligible                                 adapter.py ~1280  combined all conditions
  _rich_message_payload                          adapter.py ~1317  payload + NL normalization
  _has_telegram_desktop_details_math_crash_shape adapter.py ~1233  guard math-in-details
  _has_telegram_desktop_cjk_rich_garble_shape    adapter.py ~1238  guard CJK
  RICH_MESSAGE_MAX_CHARS                         adapter.py 376   cap 32,768
  _try_send_rich / _try_edit_rich                adapter.py ~1404 / ~1457  send / edit rich
  convert_table_to_bullets                       gateway/platforms/helpers.py ~174  table fallback


## VERIFICATION RESULTS (this session)

Tested from CODE (deterministic):
  - _needs_rich_rendering + guard -> routing correct
  - sendRichMessage from Bot API -> ok

Reported at CLIENT by user (not independent verification):
  - Pipe table        -> native grid    (PROVEN)
  - Task list - [x]   -> checkbox      (PROVEN)
  - <details> no math -> dropdown     (PROVEN)
  - Math block $$     -> LaTeX render  (PROVEN)
  - Heading          -> rendered      (PROVEN)
  - Blockquote        -> rendered      (PROVEN)
  - Nested list       -> rendered      (PROVEN)
  - Inline formatting -> rendered      (PROVEN)
  - Link              -> rendered    (PROVEN)

Tested from CODE (guard works):
  - Math inside <details> -> forced legacy
  - CJK text              -> forced legacy

Related skill: telegram-advanced-config (all Telegram config knobs).
