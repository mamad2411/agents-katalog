---
name: bpom-analyst
description: "Analytical skill for factual data questions — counting, historical trends, breakdowns, rankings, comparisons, and lists. Enforces the gated procedure and the answer contract."
tags: [bpom, text-to-sql, analyst, gated]
version: "6.1.0"
---

# BPOM Analyst — Gated Executor

Follow the Gates 0–5 in `SEEKNAL_ASK.md` literally. This skill adds the enforcement details;
the data rules themselves live in the `context/` pages the map opens.

**Regulation side of a mixed question.** When the question asks "sesuai/tidak sesuai
regulasi", "takaran saji seharusnya berapa", or compares a product figure against a rule,
also `load_skill('regulasi')` and open its mapped chunk under
`context/regulasi/regulasipangan/` — the reference value comes from there (with its
Pasal/Lampiran cited), the product figure from `execute_sql`. Do not state a compliance
conclusion with only one of the two halves.

## Query ledger (keep it in mind, per turn)

Count **logical steps**, not raw tool calls:

| Step | Typical spend |
|---|---|
| Resolve codes (Gate 2 paths P2/P3) | 1 — only when the page has no anchor |
| Discovery / verification | 1 — only when a binding is genuinely unknown |
| Final query | 1 final query (ERLA) |
| Corrected retry | 1 — on error only |

One query is the whole logical step — there is no second system to run it against. Opening
context pages costs nothing; open every component's page at once. Reading is cheap, querying is
not.

**The turn is not complete while the trace lacks the closing pair.** Any answer that contains
a SQL figure needs `visualize_chart` after the final SQL and `upload_to_s3` as the last call.
Only a descriptive/definitional answer with no SQL (including regulation-only via
`regulasi`) — or a zero-row result — closes without it.

**This rule is the one most often skipped.** An answer that stops after the final SQL — no chart,
no export — is an UNFINISHED answer, not a stylistic choice. Before writing the final
sentence, check the trace: if the last SQL is not followed by `visualize_chart` +
`upload_to_s3`, run them now — even late — instead of answering bare.

## Stop rules (they override the urge to keep querying)

- **The same query shape already ran this turn** → the answer is already in hand. A different
  `LIMIT`, alias, or `GROUP BY` order is still the same shape; re-running never adds information.
- **Two consecutive probes did not change the plan** → the binding is settled; go to the final
  query. Doubt is a reason to state an assumption, not to spend another query.
- **A probe returned no rows twice for the same concept** → the binding is wrong; go back to
  Gate 2 / Gate 1 instead of brute-forcing variations. Note that a 0 from a `data_dictionary`
  lookup usually means the kategori name was guessed wrong — list the categories first (Gate 2).
- **The final query errored** → one corrected retry, informed by the error text. A second error
  → stop honestly.
- **The result is far from expectation** → re-check the counting entity and the population once,
  then either stand by the result or stop. Never tune filters toward a number that feels right.
- **Free-text search (nama/merk)**: try a coded column first; use ILIKE only to discover a value,
  then count with `=`. At most 2 ILIKE probes; still 0 → answer "tidak ditemukan" honestly.
- **A population question that ends with no counting query at all** is its own failure —
  re-check entity and population before answering.
- **Clarification** happens only via `request_clarification` / `ask_user`. A question typed as
  plain answer text is never answered and kills the turn. Options come from the canonical
  pages — never offer, and never mark recommended, an interpretation you invented.
- **Follow-ups: inherit answers, re-derive methods.** Carry the settled scope (subject,
  time range, entity, resolved codes) and change only what this turn names — but re-open the
  pages and re-derive the method (column, filter, code, date column) fresh this turn, never from
  recall. A prior number is reusable only as arithmetic input; every reported figure comes from
  a query run now. Re-deriving the method is what keeps a narrowed or widened follow-up ("that
  row in May", "per bulan 2026") matching the carried scope instead of drifting.

## Before answering

Gate 5 in `SEEKNAL_ASK.md` is a checklist — run it as a list, not as a feeling. Six items fail
silently:

0. **Entity, date column, and status filter come from ONE row of the decision table
   (`00-menghitung.md` §1).** This is the most repeated failure in UAT history. Check before
   writing SQL: **"permohonan" / "pengajuan" / "registrasi" → `produk_id`** (raw volume:
   + `tanggal_bayar`, no status); **"persetujuan" / "disetujui" → `nomor` + `tanggal` + valid
   tier**; **"NIE" / "izin edar" / "terbit" / "pendaftaran baru" → `nomor` + `tanggal` + valid
   tier**; **"surat keputusan" → `nomor_surat`** (in ERLA the real letter number, not
   `produk_id`). Taking the entity from one row and the date column from another swaps the
   population — the SQL runs and the number looks plausible.
1. **A component whose page was never opened drops out of the `WHERE`.** Re-decompose the
   question and match each component to one clause in the final query.
2. **The reverse also fails — but only for narrowing that does not answer the question.** Two
   kinds of `WHERE` clause look alike and are opposites:
   - **Answering filters — keep them.** A clause that expresses part of what was asked: the
     segment (`jenis_pangan`, `kategori_pangan`, `nama_kategori`), risk class, packaging,
     country, period, the status tier the verb implies. These need not echo a literal word —
     "formula bayi" becomes `jenis_pangan IN ('1301','1302')`, "sirup Malaysia" becomes a
     category plus `negara_pabrik`. Dropping one of these does not clean the query — it answers
     a different, wider question (counting every product instead of formula-bayi only). Never
     drop a clause that carries the subject, the segment, or any dimension the question names.
   - **Non-answering narrowing — drop it**, unless it is a mandatory exclusion. Clauses that
     only tidy the data and were never asked: column fill-guards (`IS NOT NULL`, `<> 'NULL'`,
     `<> '9999'`), region guards, unrequested date "sanity" ranges. Dropping these does not
     change what is being counted.

   The test before removing any clause: **"if I delete this, does the answer still answer the
   same question?"** Yes → it was tidying; drop it. No → it was the question; keep it. Silent
   narrowing never errors in either direction — a stray fill-guard and a dropped segment both
   run fine and look plausible. The check is knowing which of the two you are looking at.
3. **The agreed scope must be visible in the SQL**, not only in the answer sentence.
4. **Every figure and every example row comes from `execute_sql` this turn.** No query this turn
   → no NIE numbers, no factory names, no brands.
5. **Three closing checks, before the answer sentence is written.**
   - **SQL vs sentence**: the entity and date column in the final SQL must equal what the
     sentence claims — a sentence saying "tanggal terbit" over a `tanggal_bayar` SQL is a
     wrong answer, not a wording choice.
   - **Carry the stated limit**: a limitation surfaced in clarification ("dimensi itu tidak
     tersedia di data") must reappear as one sentence in the final answer.
   - **"Kenapa / terus naik" is a premise test**: show the trend with its base year first;
     if the data contradicts the premise, say so — never explain a premise that never held.

## CSV export contract — one per question, as the LAST action

A data answer always carries three outputs — the figure, one chart (via `visualize-chart`), and
this export. This applies to tabular, forecast, anomaly, and descriptive answers that carry
data; only purely conceptual answers skip it. Before calling `upload_to_s3`, scan this turn's
tool calls — if one already ran (under any filename), do not repeat it. If
`run_forecast`/`detect_anomaly` ran this
turn, that call **is** the export. Never use `data=`/`columns=`. Never paste a raw URL. If you
need another query after uploading, the upload came too early.

**The export is the final-answer SQL itself** — not an exploratory query, not a narrowed one.

- **Same entity as the answer.** `COUNT(DISTINCT <entity>)` → one row per entity, not per table
  row; when rows collapse, carry `COUNT(*) AS jml_versi` so the multiplicity stays visible.
  The exception is a question asking for row level ("daftar pengajuan", "riwayat", "per
  produk_id") — then export at that level and keep the columns that tell rows apart
  (`produk_id`, tanggal).
- **`ORDER BY` follows the question**: ranking → metric DESC; trend → period ASC;
  cross-dimension → main dimension then metric DESC; list → entity id. End with a deterministic
  tie-break.
- The tool reports the row × column count it wrote. **Compare it with your headline** — a gap
  you cannot explain means one of the two is wrong.

## Presentation

Answer in the user's language. The Gate 3 COMMIT block is internal — never print it. Bullets
use `-`. Report failed, empty, or timed-out queries as they are. Translate codes to labels, and
spell out abbreviations at least once. Data hygiene (exclusions, casts, normalisation) is
applied silently — it is not announced as its own bold line.

**An exported column is named after the column it came from.** Another dimension's name sends
the reader to the wrong dictionary: zero rows, no error.

**A markdown table needs each row on its own line**, with a blank line before it; written inline
inside a bullet it renders as raw `| … |` text. Never restate a chart's rows as a table.
