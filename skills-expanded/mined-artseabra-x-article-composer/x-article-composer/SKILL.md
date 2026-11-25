---
name: x-article-composer
description: Reliably compose and verify unpublished X Articles with native formatting, checkpoint-aware continuation, semantic-first post insertion, bounded execution, and a strict never-publish boundary.
---

# X Article Composer

Use this skill when the user wants an agent to create, reconstruct, format, test, or verify an X Article in the native composer.

Read this file completely before browser interaction. For a first run, also read `docs/ONBOARDING.md`, `docs/DEMO_ARTICLE.md`, and `docs/COMPOSER_MECHANICS.md`.

## Outcome

Produce a correctly structured, autosaved **draft**, prove the native structures in X's rendered Preview, and hand control back to the user. Never publish.

## Non-negotiable boundaries

1. Use only a browser surface the user explicitly authorizes for this task.
2. Do not inspect unrelated tabs, drafts, profiles, windows, local storage, cookies, or credentials.
3. If authentication is required, ask the user to sign in directly in the browser. Do not operate password, passkey, recovery, or multi-factor fields.
4. Identify the exact new or existing Article draft before changing content.
5. Treat availability of a browser or tool as separate from the user's authorization to use it.
6. Never click **Publish**. A request to publish is outside this skill; leave publication to the user.
7. Do not upload a local file unless the user selects it or explicitly identifies it for this exact draft.
8. Do not claim success from typed text, autosave, word count, or a screenshot alone. Verify the native result in Preview.
9. Preserve every verified checkpoint. A failure in a later block or insert never authorizes selecting or deleting previously verified Body content.
10. Give the exact browser-composer actor a declared token ceiling and reserve enough of it for autosave, Preview, recovery, and handoff. Do not put that ceiling on a controller agent or create a product goal unless the user explicitly requests one.
11. If a controller delegates browser work to a composer sub-agent, bind browser and mutation authority only to that composer. The controller may supervise and relay evidence but must not become a second browser operator.

If any boundary becomes ambiguous, stop before mutation and ask one concise question.

## First-run flow

Follow `docs/ONBOARDING.md` exactly.

The short form is:

1. Open `https://x.com/compose/articles` in the authorized browser surface.
2. If X presents authentication, pause for the user to sign in manually.
3. State the exact draft-only scope and optional inputs.
4. Ask the single execution gate from the onboarding document, including the exact composer token ceiling and any conditional exact clipboard write for a supplied post URL.
5. After `ready`, create one new blank unpublished demonstration draft in the active X account named in the gate. First-run onboarding never reuses an existing draft.
6. Compose `docs/DEMO_ARTICLE.md` using the mechanics below.
7. Confirm autosave, then open Preview, verify every required element, and stop there.

## Operating procedure

### 1. Establish the surface

- Confirm that the visible page is the X Articles area or the exact authorized Article editor.
- Confirm that the intended surface is a draft.
- If an existing draft is in scope, record its visible title and preserve all content outside the user's requested edit region.
- For the capability demonstration, prefer a new draft so no existing writing can be damaged.

### 2. Bind the composer and execution budget

Before the first browser mutation, identify the one browser-composer actor and declare one hard token ceiling for that actor in the run contract, delegated instruction, or working plan. The ceiling belongs to the composer doing the browser work, not to a supervising controller.

Do not use a runtime's goal API merely to enforce the ceiling. Create or update a product goal only when the user explicitly requests goal use for this run. A normal execution plan or authorization contract is sufficient.

Allocate the ceiling before composing:

- `10%` for surface, source, and checkpoint preflight;
- `60%` for forward composition;
- `20%` for autosave and Preview reconciliation; and
- `10%` for bounded recovery and the completion report.

At each phase boundary, record only the amount used and remaining when trustworthy telemetry exists. Never invent token usage. When the remaining budget reaches the reserved autosave, Preview, recovery, and report allocation, stop starting new content. Preserve the last verified checkpoint, confirm persistence when possible, release the browser cleanly, and report the incomplete remainder.

Do not spend the budget repeating a passed canary, replaying an unchanged paragraph, or emitting the same full-state proof after every action. One compact checkpoint proof replaces repeated reconstruction.

### 3. Freeze or resume a checkpoint

A checkpoint is a compact record bound to the exact Article ID, source digest or exact payload, and last verified native block. It records:

- the ordered block texts and native classifiers already present;
- the exact inline marks and embeds inside those blocks;
- the protected title and banner state;
- the last usable empty Body insertion point; and
- whether autosave was explicitly observed.

When continuing an existing draft:

1. Reconcile the live draft against the checkpoint in one bounded semantic read.
2. If it matches, reuse it. Do not retype, reformat, or rerun method canaries for unchanged content.
3. Treat content and caret focus as separate state. If the content matches but focus moved elsewhere, restore only a collapsed caret at the exact empty Body insertion block, then prove Body focus and inactive styles. Do not replay content.
4. If the content differs, stop before mutation and report the first divergence.
5. Extend the checkpoint only after the new block or insert has been semantically proved.

A previously proved method remains admitted on the same composer surface while the exact checkpoint remains intact. Re-run a method canary only when the relevant UI or method has changed, the proof was incomplete, or the user explicitly requests a retest.

### 4. Prefer Focus mode while writing

When creating, drafting, composing, reconstructing, formatting, or editing an Article, prefer X's Focus mode when it is available. Enter it in either of these ways:

- choose the visible **Focus** control; or
- append `/focus` to the exact authorized Article editor URL, for example `https://x.com/compose/articles/edit/<ARTICLE_ID>/focus`.

After entering Focus mode, confirm that the URL still contains the exact authorized Article ID and that the same draft remains open. Focus mode changes the editor view, not the authorization scope. If it is unavailable, continue in the standard authorized editor rather than navigating to another surface.

### 5. Choose a clean insertion point

- Native classifier prefixes work reliably only on a genuinely empty **Body** block.
- Do not append `#`, `##`, `>`, `-`, or `1.` directly to existing text.
- If the current empty line inherited a heading, quote, or list classifier, reset that empty line to Body before continuing.

### 6. Activate, observe, then type

For every classifier prefix:

1. Send the prefix as discrete keystrokes.
2. Send Space.
3. Wait for the block to visibly or semantically change type.
4. Only then enter its text.

If the automation surface exposes block roles or semantic tags, poll at short intervals and begin as soon as the expected type appears. If semantic polling is unavailable, use a conservative pause of about one second after Space.

Do not batch the prefix, Space, and content into one fast insertion.

### 7. Preserve focus through inline styles

For forward composition of styled text, keep the exact Draft.js Body block continuously focused from style activation through span completion:

1. Prove the caret, block, focus, and current active styles.
2. If the styled span has a leading boundary space, send one discrete native Space while styles are inactive and prove the U+0020 space and caret advance.
3. Activate Bold or Italic with the native toolbar or platform shortcut already proved on this surface.
4. Do not refocus through a locator while the style is active.
5. Enter each exact ASCII character in the styled span with one acknowledged native keypress. Do not use bulk type while Bold or Italic is active.
6. After each character, prove the exact prefix, caret advance, focus, active style, and the new character's semantic inline mark.
7. Deactivate the style and prove it inactive before continuing with unstyled text.
8. If the styled span has a trailing boundary space, send one discrete native Space and prove the U+0020 space and caret advance before unstyled text resumes.

Bulk type is reserved for unstyled interior text with no leading or trailing boundary space and only while Bold and Italic are proved inactive.

Toolbar chrome is not the formatting truth. If an outer Bold or Italic button looks inactive while its nested icon or Draft.js state shows active, inspect the semantic inline range and nested control state. Correct the read-only checker; do not refocus, toggle, retype, or roll back content that already passed.

For applying a mark to text that already exists, use an exact selection:

For bold, italic, strikethrough, or link text:

1. Focus the exact text block.
2. Move to the beginning of the block.
3. Advance to the exact start position.
4. Extend the selection by the exact target length.
5. Apply one command.
6. Verify that only the intended span changed.

Use visible substring boundaries when the automation surface supports them. When counting cursor positions, account for emoji and other characters represented by more than one UTF-16 code unit. Do not infer an inline Bold mark from computed font weight alone: headings can be natively heavy without containing a semantic Bold span.

Current native commands:

- Bold: Command-B on macOS or Control-B on Windows/Linux.
- Italic: Command-I on macOS or Control-I on Windows/Linux.
- Strikethrough: Command-Shift-X on macOS or Control-Shift-X on Windows/Linux.
- Link: Command-K on macOS or Control-K on Windows/Linux, then fill the URL and visible text in the native dialog.

Do not attempt underline as a required native Article mark.

### 8. Serialize menu actions

Never click **Insert** and a submenu item in the same unobserved burst.

1. Open **Insert**.
2. Wait until the menu is visible.
3. Choose exactly one item.
4. Wait for its dialog or block editor.
5. Fill it.
6. Use its own Preview when offered.
7. Insert or update it.
8. Wait until the native block appears in the Article before proceeding.

Follow the element-specific flows in `docs/COMPOSER_MECHANICS.md`.

For a supplied public post URL, use the checkpoint-safe Posts flow in `docs/COMPOSER_MECHANICS.md`: one native paste, one exact-value proof, an event-first wait, exact semantic proof of the outer post and its unique visible containing non-anchor control, then one immediate click. Do not type a post URL character by character and do not require a pre-click screenshot.

Visually inspect the native embed only after insertion. A repost or quote-post can contain nested media and another post card, making the inserted embed taller than the viewport. When capture is authorized, emit only a crop bounded to that embed, never the full viewport or display. The outer author row may be hidden by the sticky editor toolbar; exact outer semantic identity plus the expected visible post content is sufficient and need not coexist in one image.

### 9. Adapt to the composer, not the clock

Serialize every X action and prove its resulting state before the next action. Use state transitions wherever possible:

- classifier changed to the expected native block;
- dialog became visible;
- action button became enabled;
- media processing disappeared and a media block appeared;
- autosave was explicitly confirmed, then Preview became available; and
- the Preview route loaded.

Poll ordinary semantic transitions at short intervals for up to about five seconds. The Posts candidate is a network-rendered exception: wait event-first for up to about thirty seconds, treating five seconds as a heartbeat rather than a terminal mismatch. Do not paste, type, press Enter, or otherwise submit a second input while waiting. If the composer exposes no readiness signal for another action, wait at least one second before continuing. Fixed waits are fallback guards, not proof.

### 10. Recover locally

If a prefix remains literal or a block has the wrong type:

1. Stop typing immediately.
2. Undo only the current block or remove only the literal prefix.
3. Restore one empty Body block.
4. Retry once with observed activation or a longer pause.
5. If the second attempt fails, leave the surrounding draft intact and report the element as unverified.

For a failed insert, close only its transient dialog and preserve the last verified checkpoint. If a post was already clicked and the resulting native embed fails semantic or visual verification, remove only that isolated new embed when its exact containment is proved and removal cannot touch verified content. If safe local removal cannot be proved, stop without mutation and leave the verified checkpoint intact.

Never use Select All on the Body to recover a later-block failure. Do not rebuild the whole article to repair one block or insert.

### 11. Verify in Preview

Autosave is necessary but insufficient. Open the unpublished Preview and verify:

- each required H1 and H2 is rendered as a heading;
- Body blocks remain Body blocks;
- bold, italic, and strikethrough cover the exact intended text;
- links have the intended visible text and destination;
- quote and list structures are native and list items remain separate;
- dividers render as separators;
- tables preserve rows, columns, and cell text;
- code preserves language and exact code;
- optional posts and media render as embeds with any intended caption;
- emoji is present; and
- LaTeX renders as mathematics rather than literal source.

Also prove the Preview route, non-editable state, visible Draft or unpublished state, and absence of Publish controls. Count inline marks from semantic ranges, not native block typography. A responsive X media delivery URL may have different pixel dimensions or query parameters from the editor's original banner; accept it only when the stable media identity and aspect ratio match and the editor's protected original asset remains unchanged. A Preview screenshot is not required when the complete semantic reconciliation is available. Leave the unpublished Preview open, finalize the exact tab as a handoff when the browser runtime supports it, release browser control, and make no later browser call.

## Completion report

Report:

- the draft title;
- which core elements passed Preview;
- which optional elements were included or skipped;
- any bounded repair performed;
- any unverified element; and
- the explicit statement: **Publish was not invoked.**

Do not describe the draft as public, posted, released, or published.
