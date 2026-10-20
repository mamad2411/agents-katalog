---
name: friction-review
description: Read docs/quality/FRICTION-LOG.md, cluster entries by skill and type, surface the top patterns, and scaffold a week-summary doc plus draft eval cases for the top 3 patterns. Usage — /friction-review [--week N] [--since YYYY-MM-DD]
argument-hint: "[--week N] [--since YYYY-MM-DD]"
arguments:
  - name: flags
    description: "Optional — --week <N> sets the week number for the output file; --since <date> filters entries"
user-invocable: true
effort: medium
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(date *)
  - Bash(ls *)
  - Bash(grep *)
  - Bash(awk *)
  - Bash(sort *)
  - Bash(wc *)
  - Bash(find *)
---

# /friction-review — cluster the log and propose fixes

Reduces a week of friction entries to a one-page action plan. The user reads the cluster, picks what to fix, runs `/forge` on the chosen items.

The user does the deciding. This skill does the counting.

---

## Step 1 — Load the log

```bash
test -f docs/quality/FRICTION-LOG.md || { echo "No friction log found. Run /friction first."; exit 0; }
```

Parse `$ARGUMENTS` for `--week <N>` and `--since <date>`. Defaults:
- `--week` → infer from existing `DOGFOOD-WEEK-*.md` files (next number)
- `--since` → 7 days ago

Read the whole `FRICTION-LOG.md`. Extract all entries matching `^## F-` headings. Filter by date if `--since` was given.

---

## Step 2 — Cluster

For each entry, parse the structured fields (`**What happened:**`, `**Expected:**`, `**Skill/agent:**`, `**Type:**`, `**Severity:**`, `**Status:**`).

Build two clusters:

**By skill/agent path:**
| Path | Count | High-severity count |
| --- | --- | --- |
| `layers/backend/node-express/nodejs-standards` | 8 | 3 |
| `layers/frontend/react` | 5 | 1 |
| ... | | |

Skip entries with `Status: resolved`.

**By type:**
| Type | Count |
| --- | --- |
| skill-gap | 11 |
| hook-fp | 6 |
| pipeline | 4 |
| ... | |

---

## Step 3 — Identify top 3 patterns

A "pattern" is a (skill/agent, type) tuple with ≥2 entries.

Rank by:
1. Number of entries (more = higher priority)
2. Tie-break: total severity weight (high=3, medium=2, low=1)

Pick the top 3. For each, also pick a representative entry (the most recent one) to anchor the pattern.

---

## Step 4 — Draft fix recommendations

For each of the top 3 patterns, propose a concrete fix and write a draft eval case (if applicable):

| Pattern type | Recommended action |
|---|---|
| `skill-gap` | Add a draft `.eval.yaml` case under `docs/quality/draft-evals/<skill-slug>-<short-name>.eval.yaml` with a `must_contain` assertion derived from the "Expected" field. Note: run `/forge fix <skill>` after the draft is accepted. |
| `hook-fp` | Note which regex needs tightening; point at the hook script. Recommend: add the false-positive content as a regression test in `tests/hooks/<hook>.test.sh` (once that suite exists) so it stays fixed. |
| `hook-fn` | Recommend extending the regex to catch the missed pattern. Reference the relevant entry's "Expected" field. |
| `pipeline` | Point at the orchestrating skill (`skills/<name>/SKILL.md`). Recommend a clarifying instruction or an explicit step. |
| `ux` | Recommend a copy / default / phrasing change. Reference the friction's "Expected" field. |
| `other` | Surface the entries; defer to user judgement. |

For `skill-gap` patterns, write the draft eval file. Format:

```yaml
skill: <skill-name>
skill_files:
  - <path-to-skill-md>
version: 1

cases:
  - id: <skill>-<draft-N>
    name: "<short description from the friction>"
    scenario: |
      <one-paragraph scenario derived from the friction's What/Expected fields>
      Use the <skill-name> skill rules.
    must_contain:
      - "<one-or-more terms from the Expected field>"
    must_not_contain: []
    rationale: |
      Derived from friction <ID>: <one-line summary>.
      Captures the pattern that <N> entries reported missing.
```

The user reviews the draft before merging it into the canonical `.eval.yaml`.

---

## Step 5 — Write the week summary

Output: `docs/quality/DOGFOOD-WEEK-N.md`

Template:

```markdown
# Dogfood Week N — <YYYY-MM-DD>

**Window:** <since-date> → <today>
**Total entries:** <N>  **Resolved last week:** <N>

## Cluster — by skill/agent

| Skill/agent | Total | High | Medium | Low |
| ... | | | | |

## Cluster — by type

| Type | Count |
| ... | |

## Top 3 patterns to fix

### 1. <skill> — <type> (<N> entries)
**Representative entry:** F-YYYY-MM-DD-NN — <title>
**Recommendation:** <action>
**Draft eval:** `docs/quality/draft-evals/<file>.eval.yaml`
**Next:** `/forge fix <skill>`

### 2. <pattern 2>
### 3. <pattern 3>

## Unresolved entries by severity

| ID | Title | Severity | Type | Skill |
| ... | | | | |

## Notes / open questions
- <anything the cluster surfaced that doesn't fit a pattern>
```

---

## Step 6 — Tell the user what to do next

Print a compact summary:

```
✓ Reviewed N entries
✓ Wrote docs/quality/DOGFOOD-WEEK-<N>.md
✓ Drafted M eval cases under docs/quality/draft-evals/

Top 3 patterns:
  1. <skill> — <type> (X entries)  →  /forge fix <skill>
  2. <pattern 2>                    →  <action>
  3. <pattern 3>                    →  <action>

Review the week summary, then run the suggested fixes.
```

Do NOT auto-apply fixes. Do NOT mark entries as resolved. The user reviews the doc, makes their own calls, commits the fixes manually. The skill's job ends at the recommendation.

---

## Hard rules

- Never modify existing FRICTION-LOG entries. Read-only.
- Never invent entries to inflate counts. If there are <3 patterns with ≥2 entries each, report fewer top-N.
- Draft eval files are clearly named `draft-` so they aren't auto-picked up by `/eval all`.
- If the log has 0 entries since `--since`, print "No new entries to review" and exit. Don't write an empty week doc.
