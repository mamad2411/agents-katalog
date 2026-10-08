---
name: sentence-gap
description: >-
  Always put a visibly wider gap between sentences in every human-readable reply and file. Applies on every turn — Cursor desktop, Cursor cloud, CLI, Grok, chat, commits, PRs, and docs. Follows Monet's portable protocol: two ASCII spaces in files; backend NBSP in HTML. Never display the six characters &nbsp; in cloud/owner-visible text. Use whenever writing any prose a human will read.
---

# Sentence gap (portable — always on)

> **This install is for Grok Bot roles.** Slack tag is `[GB-<NAME>]` — `[GB-CONDUCTOR]`, `[GB-MONITOR]`, `[GB-FIXER]`, `[GB-DEPLOYER]`, `[GB-COMPILER]` (Compiler), `[GB-NURSE]`, `[GB-HOUSEKEEPER]`, `[GB-ACCOUNTANT]`, `[GB-ORACLE]`.  Notes name is the role in Title Case (`Conductor`, `Monitor`, …).  Cloud branches are often `cursor/`.  Never `[GROK-BOT]`, `[CURSOR]`, `[GROK]`, or `[MONET]`.


Source of truth: `/Users/jay/Code/AI-Fleet-Coordinator/docs/SENTENCE-GAP-PORTABLE-SKILL.md`

The block below is Monet's protocol, pasted verbatim. Follow it exactly. Do not weaken it. Cloud agents without the Mac filesystem still have the full protocol in this file.

### Rule: two visible spaces between sentences

Put a **visibly wider gap** between sentences — after `.` `!` `?` when a new sentence
follows — in every piece of prose a human reads.  Not just product copy: chat replies,
commit messages, PR titles and bodies, code comments, docs, tickets, Slack posts, release
notes, design docs.

Do **not** add a gap after a non-terminal abbreviation (`e.g.`, `i.e.`, `Dr.`, `v1.2.3`),
inside a URL, email, filename, or a brand name containing a period.

### The catch that wastes everyone's time

**Typing two literal spaces usually does nothing visible.**  HTML and most Markdown
renderers collapse runs of whitespace to a single space.  So the assistant "complies,"
the raw text really does contain two spaces, and the human still sees one.  Both sides
then argue about whether the instruction was followed.

**The gap must survive the renderer between you and the reader.**  Which mechanism works
depends on the surface, so pick by destination:

| Destination | Use | Why |
|---|---|---|
| **Cloud / BotFleet / OpenMausBot chat** | two literal ASCII spaces | Owner 2026-09-03: never display the six characters `&nbsp;` in cloud text.  The backend maps doubles (or the entity) to a real U+00A0 before paint. |
| **Claude Code — desktop app (Code tab)** | two literal ASCII spaces | Owner-verified 2026-09-04.  Supersedes the 2026-08-19 entity finding below for this surface — see History. |
| **A surface where the owner has confirmed the renderer expands the entity** | the literal entity text `&nbsp;` then a normal space → `End.&nbsp; Next.` | Name no product here.  Only use this row on a surface the owner has confirmed — do not assume, and do not re-test a surface this table already answers. |
| **Plain-text chat (no Markdown rendering)** | two literal ASCII spaces | Nothing collapses them; an entity would show as the ugly text `&nbsp;` |
| **Files read as source** — repo docs, commit messages, code comments, config, diffs | two literal ASCII spaces | Read in an editor/terminal/`git diff`, which preserve them verbatim; an entity would appear literally |
| **HTML / JSX / SwiftUI / any rendered product copy** | a real U+00A0 plus a space, or a shared `SENTENCE_GAP` constant | Raw double spaces collapse in HTML.  Source may use the entity only when the renderer expands it.  The owner must never see `&nbsp;` as text. |
| **Markdown source** | two literal spaces *between* sentences | ⚠️ Two spaces at the **end of a line** is the unrelated hard-line-break syntax — don't confuse the two |

### Verify, don't assume — run this self-test only on a NEW, unlisted surface

The table above already answers every surface listed in it — follow the row, don't re-test
it.  For a surface the table does **not** cover, test it and ask the human what they
actually see before relying on either mechanism.

> Output these two lines verbatim, then ask which shows a wider gap:
>
> A. `Sentence one.&nbsp; Sentence two.`
> B. `Sentence one.  Sentence two.`
>
> If A looks wider → confirm the result with the owner before relying on the `&nbsp;`
>   entity on this surface.  Do not assume from one look.
> If B looks wider, or they look identical → use two literal spaces.
> If neither shows a gap → say so plainly and ask how they want it handled.
> Then keep using whichever won, for that surface, for the rest of the session — and add
> the surface to the table above so nobody re-tests it.

### History — 2026-08-19/20 findings on Claude Code (terminal + desktop), do NOT re-run these tests

**2026-09-04 update — desktop app superseded.**  The entity finding below for the desktop
app (Code tab) was superseded by an owner-verified ruling on 2026-09-04: use **two literal
ASCII spaces** there now (see the table above).  The 2026-08-19 entity advice for the
desktop app is withdrawn.

**Terminal CLI — no newer ruling.**  Last checked 2026-08-19/20; not re-verified since.
Default to two literal ASCII spaces there, and confirm with the owner before relying on the
`&nbsp;` entity on the terminal CLI.

What was found 2026-08-19/20:

- ❌ **Two literal ASCII spaces in chat** — collapsed by the Markdown renderer.  Invisible.
- ❌ **A raw U+00A0 character typed directly into chat** — normalized away in the
  transcript view.  **Especially deceptive: copy-pasting the reply out can still show two
  spaces, so it looks fixed when the human still sees one.**  Do not trust copy-paste as
  proof.
- ❌ **App/output settings** — no toggle governs inter-sentence spacing.  Output-style
  settings change tone only; headless output-format flags don't apply to interactive chat;
  screen-reader modes only drop borders.
- ❌ **Patching the client** — compiled and signed; breaks code signing and is wiped by
  auto-update.  Never attempt.
- The literal entity text `&nbsp;` + a space rendered as a visibly wider gap at the time —
  now superseded on the desktop app (2026-09-04, see above); not re-verified on the
  terminal CLI since, so confirm with the owner before relying on it there.
- ✅ **Two literal ASCII spaces in files** — correct and simplest; leave file content alone.

### The transferable lesson

When an instruction *appears* not to take effect, **stop repeating the promise and
diagnose the rendering layer between you and the reader** — then ask them what is on their
screen.  Four rounds of "fixed it!" were spent here before anyone checked whether the
change could be seen at all.  Intent is not output; output is not what is displayed.
