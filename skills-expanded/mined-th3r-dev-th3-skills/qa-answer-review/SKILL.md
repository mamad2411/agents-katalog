---
name: qa-answer-review
description: >-
  Review the prepared answers in a "Q&A" sheet before a customer / go-live / integration meeting:
  pull the tab (No · Question · Prepared answer · Remark), run every answer through four review
  lenses in parallel — business, program, data, operation (lenses/<lens>/SKILL.md) — merge the verdicts into
  one plain note per row and write it into the Remark column. Use WHENEVER the work is "review the
  Q&A before the meeting", "are these prepared answers safe to say", "ตรวจคำตอบก่อนประชุม",
  "ลง remark ให้ Q&A", "business review / program review of an answer", or a spreadsheet link that
  names a Q&A tab. Read-only on source code and databases; writes only the Remark column.
---

# Review a prepared Q&A tab

**In** a sheet export (`.xlsx`) with one tab per meeting · **Out** one Remark per question saying
whether the prepared answer is safe to say, what to change, and what is still open — plus the
evidence trail in `<out>/<tab-key>/<DDMMYYYY>/`.

The answers are what *we* will tell a customer or partner in a meeting. The review question is not
"is this nice prose" but **"if we say this, is it true, is it ours to promise, and can the system
back it up today?"**

```bash
S=skills/qa/answer-review/scripts
# 1. pull: export the sheet as .xlsx (Drive: File → Download → .xlsx, or an MCP download that spills JSON with base64 content)
uv run $S/qa.py pull <sheet.xlsx | download.json> --out work/qa-review \
    [--tab 'Q&A List (\S+)'] [--headers "No,Question,Answer,Remark"]   # -> work/qa-review/<key>/qa.json
# 2. lenses write work/qa-review/<key>/<DDMMYYYY>/lens-<lens>.json (one agent per lens, in parallel)
# 3. condense the lens notes into final.json by hand, then merge
uv run $S/qa.py merge <key> --out work/qa-review                       # -> plan.json (old / new per row)
uv run $S/qa.py selfcheck
```

## 0. The tab

- Header **row 1** holds the four columns. The default is `No · Question · Answer · Remark`;
  pass `--headers` with the sheet's exact labels (any language). `qa.py pull` asserts them and
  stops if a column was renamed.
- `--tab` is a regex with one capture group: the group becomes the folder key (`TOP`, `ACME`, …).
  Default `Q&A\s*(?:List)?\s*(\S+)` matches `Q&A List ACME`, `Q&A ACME`.
- Remark may already hold team comments on some rows. **Those are review input, not noise** — every
  lens reads them, and they stay in the cell.
- Never edit the Question or Answer columns. A better answer goes into Remark as a suggestion; the
  team owns the wording.

## 1. Lenses — one agent each, in parallel

| Lens | Asks | Skill |
|---|---|---|
| business | Is it ours to say? Process, roles, scope, commitments, consistency with the other answers | `lenses/business/SKILL.md` |
| program | Does the system do this today? Endpoint · screen · released tag | `lenses/program/SKILL.md` |
| data | Do the fields, keys and units named exist, with those meanings, and do they join? | `lenses/data/SKILL.md` |
| operation | Network, file transfer, sandbox, auth, monitoring, support — can we run it? | `lenses/operation/SKILL.md` |

Spawn four read-only agents, each over **all rows** of `qa.json`, each told to read its lens
`SKILL.md` and follow it. Every brief carries, verbatim:

> Read-only: no repo edits, no DB writes, no logins, no sheet edits. Repos: `<list them>` — report
> `git log -1` of each. Database: `<read-only command>`. Input: `<out>/<key>/qa.json`.
> Output: `<out>/<key>/<DDMMYYYY>/lens-<lens>.json` = `[{No, row, verdict, evidence, note}]`,
> one item per row, `verdict` one of `OK · ADJUST · WRONG · OPEN · N/A`. `evidence` is for us
> (file:line, tag, query + result, doc path). `note` is for the meeting team: 1–2 short lines in
> the team's language, lead with what was found ("checked: …" · "from what we found, … likely …"
> · "need more info on …"), never "cannot prove" / "no conclusion", never name a tool, script,
> skill or agent. `N/A` when the row is outside the lens — leave `note` empty then.

For Thai notes follow the `kien-thai` rules (technical terms stay English, no middle dot `·`).

| Verdict | Means | Remark shows |
|---|---|---|
| `OK` | true, ours to say, backed by the system today | one line, the evidence in words |
| `ADJUST` | right direction, but overclaims, underclaims or is vague | what to change, a better phrase |
| `WRONG` | contradicts the system or the process | what is actually true |
| `OPEN` | depends on a decision not yet made | who decides, and a holding answer |
| `N/A` | outside this lens | nothing |

## 2. Merge, propose

1. **Condense by hand into `final.json`** = `{No: "- …\n- …"}`. The Remark reads like the team's
   own notes — 1–3 plain `- ` bullets, sorted (what is true → what to say instead → what to ask),
   **no lens labels, no verdicts, no date header**. Merge the four lenses into one view; where they
   disagree, write it as a thing to check, not two answers.
2. `qa.py merge <key>` writes `plan.json`: the team's text kept on top, a blank line, our bullets.
   Our bullets from any earlier `final.json` of that key are stripped first, so a re-review
   replaces them instead of stacking.
3. Show the owner a short table: No · verdicts per lens · the one-line gist. Rows with `WRONG`
   first. Once shown, write — unless they stop it.

## 3. Write Remark (the fourth column)

Whatever drives the sheet (browser automation, Sheets API, a CSV re-import), keep these checks:

- Re-export the tab, parse it quote-aware, assert the Remark header and that every `plan.json`
  row's `old` still equals the live cell. A mismatch means a teammate edited meanwhile: re-pull and
  re-merge, don't overwrite.
- Write the whole Remark column in one paste / one batch update built from the live column with
  `plan.json` applied; never cell by cell by hand.
- Verify by re-export: the Remark column equals the plan, every other cell equals the pre-write copy.
- `plan.json` (`old` / `new` per row) is the before/after record — no separate CSV needed.
- A large plan does not fit in a script argument: load it from a file.

## Traps

- **The meeting is about the partner's integration, not our UI.** "API" in a question can mean
  their current push, our external API, or a webhook. Say which one in the note.
- **"Already available" needs a tag.** Merged on `develop` is not available to a customer; quote
  the release that carries it, or say it is not released yet.
- **Answers lean on each other.** A row that offers "3 options: SFTP, Excel, manual" is contradicted
  by a Remark saying there is no SFTP — the business lens checks the set, not just the row.
