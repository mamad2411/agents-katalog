---
name: roadmap
description: >
  Roadmap ledger: promote scratch ideas into docs/ROADMAP.md, update entry
  status (Done/advanced/superseded), ensure the document header, or publish a
  roadmap entry to GitHub / Fizzy on explicit ask. Use when the user says add
  this to the roadmap, promote this idea, mark roadmap done, update roadmap
  status, this belongs on the roadmap, capture as a roadmap item, make this a
  future capability, publish to Fizzy, or open a GitHub issue for a roadmap
  idea — and when commit detects ledger impact or passes release context.
disable-model-invocation: true
---

# roadmap

Durable **idea ledger** in `docs/ROADMAP.md` — unordered, undated, not a
sprint plan. Commitment levels:

| Level | Signal | Destination |
|-------|--------|-------------|
| Thought | capture / brain dump / ambiguous | **`idea`** → `.scratch/ideas/` |
| Durable intent | promote / add to roadmap | `docs/ROADMAP.md` |
| Status update | mark done / advanced / superseded / shipped | existing entry Status |
| Tracked work | publish / open issue / Fizzy card | GitHub or Fizzy |

When intent is ambiguous, capture via **`idea`**. Never infer publication from
capture or promotion.

## Boundaries

- Do **not** promote or publish without explicit user intent for that level.
- Do **not** invent detail merely to fill optional fields.
- Do **not** emit filler like `Open Questions` / `Notes` with “None.” — omit
  empty optional sections.
- Do **not** delete scratch files after promotion (mark provenance only).
- Do **not** treat roadmap order as priority or assign dates/estimates/sprints.
- Do **not** expand status updates into sprint planning or issue creation.
- Do **not** put author or agent instructions into `docs/ROADMAP.md` or the
  public header in [references/roadmap-template.md](references/roadmap-template.md)
  — that file is a public idea display; process rules live in this skill and
  [references/promotion.md](references/promotion.md).
- Do **not** create Fizzy/GitHub artifacts during promote or status — publish is
  a **separate** explicit step after an entry exists.

## Workflow

### 1. Classify action

| User / caller intent | Action |
|----------------------|--------|
| Capture / brain dump / ambiguous | Hand off to **`idea`**; stop |
| Promote / add to roadmap / future capability | Continue → promote |
| Mark done / advanced / superseded / shipped-in / ledger impact from **`commit`** | Continue → status |
| Publish to Fizzy / open GitHub issue | Continue → publish (entry must already exist or promote first) |
| Ensure / init ROADMAP.md only | Run ensure header; stop |

**Done when:** action chosen; capture routed away if needed.

### 2. Ensure ledger

If `docs/ROADMAP.md` is missing or lacks the standard header, copy the header
from [references/roadmap-template.md](references/roadmap-template.md) (through
the entries-append comment only — not the blank entry shape below it).

```bash
python3 skills/roadmap/scripts/ensure_header.py
```

**Done when:** `docs/ROADMAP.md` exists with conventions header.

### 3. Promote (normalize)

Read the scratch source (user path, or search `.scratch/ideas/` + OKF
`knowledge/index.md` / `CONTEXT.md` for related terms). Promotion is
**classification** into the public entry shape — see
[references/promotion.md](references/promotion.md) and the blank entry in
[references/roadmap-template.md](references/roadmap-template.md).

Required fields: **Domain**, **Intent**, **Scope**, **Boundaries**. Include
**Constraints**, **Open Questions**, **Interfaces**, **Notes** only when they
carry public signal. Set **Interfaces → Scratch** to the source path when
promoting from `.scratch/ideas/`.

Write the entry markdown to a temp fragment, then:

```bash
python3 skills/roadmap/scripts/append_entry.py --entry /path/to/fragment.md
python3 skills/roadmap/scripts/mark_promoted.py \
  --scratch .scratch/ideas/<slug>.md \
  --anchor <anchor-from-append>
```

Report the ROADMAP path + anchor. Leave scratch in place with the promotion
marker.

**Done when:** entry appended; scratch marked; paths reported.

### 4. Status

Update an **existing** entry only. Grammar:
[references/status.md](references/status.md).

1. Identify the entry (title/anchor from user, commit ledger-impact hint, or
   release context).
2. Set **Status** to Done / Advanced / Superseded; optional shipped-in-version.
3. Do not rewrite Scope into a sprint plan; keep edits to Status (+ short note).

If no matching entry and the user wants durable intent → promote first (step 3),
then status. If ambiguous which entry → ask once.

**Done when:** Status line updated (or skipped with reason); path reported.

### 5. Publish (explicit only)

Only when the user separately asks to publish or open tracked work:

| Target | Behavior (current) |
|--------|--------------------|
| GitHub | Draft issue title/body from the entry; create with `gh` only if user confirms |
| Fizzy | Stub: report that self-hosted Fizzy sync is not automated yet; give card title + body the user can paste, or note webhook/API follow-up on the roadmap |

Never create external artifacts during promote or status.

**Done when:** publish skipped with reason, or external artifact URL/path reported.
