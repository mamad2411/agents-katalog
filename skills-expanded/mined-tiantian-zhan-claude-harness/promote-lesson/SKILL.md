---
name: promote-lesson
description: Find lessons in docs/lessons.md that have been referenced ≥2 times, then promote them into CLAUDE.md boundary rules via a single delta edit. Implements the ACE paper's structured-bullet + delta-edit pattern, so your harness evolves without full rewrites. The mechanism that makes the harness self-improving.
allowed-tools: Read, Glob, Grep, Edit, Bash(grep:*), Bash(git log:*), AskUserQuestion
---

# promote-lesson

The harness is supposed to learn from its mistakes. This skill is the **learning mechanism** — it scans `docs/lessons.md` for repeated pain, then turns the worst-offender lessons into hard rules in `CLAUDE.md`.

## When to use

- After a `/review-harness` flagged "promote candidates"
- Monthly hygiene (alongside `/review-harness`)
- Whenever you find yourself thinking "we just hit this *again*"

## When NOT to use

- Right after seeding `docs/lessons.md` — give it 2-4 weeks of real use first
- When `docs/lessons.md` has fewer than ~5 entries — sample too small
- For one-time observations — wait for a second occurrence before promoting

---

## Why this exists (the research backbone)

The **ACE paper (arxiv 2510.04618)** demonstrates that an evolving rulebook works best when:

1. Rules are stored as **structured bullets with IDs** (so individual rules can be targeted)
2. Updates happen via **delta edits**, not full rewrites (so the rulebook accumulates without churn)
3. Promotion is gated by a **helpful/harmful counter** (so noise doesn't pollute the rulebook)

Concretely: when the same lesson keeps being referenced — by you, by `/review-harness`, by past PRs — that lesson has earned a place in the always-loaded section. Otherwise it stays in `docs/lessons.md` where it's only consulted on demand.

Industry data on why this matters: **45% of AI-generated code contains security flaws** (Veracode 2025), and the bulk of those flaws cluster around the same handful of patterns (input validation, secret handling, schema mutation). Once you've seen a class of mistake twice, it belongs in the boundary list, not in a footnote.

---

## Workflow — 5 steps

### Step 1 — Scan lessons.md

```bash
cat docs/lessons.md
```

If the file doesn't exist or has < 5 entries: report "lessons.md is too sparse to promote from; come back after 2-4 more weeks of use." Stop.

### Step 2 — Count references per lesson

For each lesson entry (typically lines starting with `` `YYYY-MM-DD` ·`` or similar bullet pattern), grep the whole `docs/` tree (excluding `lessons.md` itself) for references:

```bash
# pseudo:
for each lesson keyword/topic:
    grep -ric '<keyword>' docs/ --exclude=lessons.md
```

A reference can be:
- An inline link from another doc (`see docs/lessons.md#YYYY-MM-DD`)
- A topic mention in `docs/exec-plans/completed/*.md` (post-mortem references)
- A `/review-harness` output that flagged the lesson previously (if cached)

Build a sorted list: lesson → reference count, descending.

### Step 3 — Filter promotion candidates

Keep only lessons where **reference count ≥ 2**. Show this short list to the user:

```
Promotion candidates (referenced ≥2 times):

1. `2026-03-15` · Schema mutations without backfill cause silent prod breakage (3 refs)
2. `2026-04-02` · Test files should never import from src/internal/ (2 refs)
3. ...
```

If list is empty: tell the user and stop. **Do not invent candidates.**

### Step 4 — Draft the delta edit

For each candidate the user wants to promote, draft a one-line CLAUDE.md boundary rule:

- Pick the right tier: ✅ Always / ⚠️ Ask first / 🚫 Never
- Phrase as imperative, ≤ 1 line, ≤ 100 characters
- No long explanation in CLAUDE.md — the *why* stays in `lessons.md`

Example transformation:

| `lessons.md` entry | Promoted CLAUDE.md rule |
|---|---|
| `2026-03-15` · Schema mutations without backfill cause silent prod breakage. We migrated `users.email` to NOT NULL without backfill and the staging migration looked clean because staging had no NULL rows. | 🚫 Never add NOT NULL constraints without writing the backfill migration in the same PR |

Show each draft to the user via AskUserQuestion. Each promotion is a separate confirmation — promote one rule at a time.

### Step 5 — Apply, then mark

After the user confirms a promotion:

1. **Edit CLAUDE.md** — add the new rule to the appropriate boundary section. Keep CLAUDE.md ≤ 150 lines; if the new rule pushes it over, propose what to trim (usually a stale `⚠️ Ask first` item that's now obvious).

2. **Mark the lesson** — append a tag to the lesson entry in `lessons.md`:
   ```
   `2026-03-15` · ...original lesson text... · **[promoted YYYY-MM-DD → CLAUDE.md §🚫 Never]**
   ```

Do NOT delete the original lesson — promoted lessons are still searchable history. The tag just stops `/review-harness` from re-flagging them.

---

## Anti-patterns

- ❌ **Promoting on first observation** — the whole point of the ≥2 rule is to avoid pattern-matching on coincidence
- ❌ **Multi-rule batch edits** — ACE paper shows delta edits work; bulk rewrites cause CLAUDE.md churn and break the agent's learned attention to it
- ❌ **Pushing CLAUDE.md over 150 lines** — if you can't fit the new rule without breaking the limit, the promotion should also trim something obsolete
- ❌ **Restating the lesson's full backstory in CLAUDE.md** — the boundary is one imperative line; the backstory stays in `lessons.md` (linked from the boundary if needed)
- ❌ **Deleting the original lesson after promoting** — kills the audit trail; future devs can't see "why does this rule exist?"
- ❌ **Promoting style preferences** — those belong to a linter or formatter, not to CLAUDE.md. (Pocock's `humanlayer` guidance: "never send an LLM to do a linter's job.")
- ❌ **Auto-applying promotions in batch without user confirmation per rule** — promoted rules become always-loaded context; the user is the only person who can vouch that the rule is worth that cost

---

## Sources

- [ACE paper (arxiv 2510.04618)](https://arxiv.org/abs/2510.04618) — structured-bullets, delta-edits, helpful/harmful counters
- [Agent drift analysis](https://prassanna.io/blog/agent-drift/) — why fully-autonomous self-improvement fails; promote-lesson is the human-in-loop alternative
- [Veracode 2025 GenAI Code Security Report](https://www.veracode.com/) — the 45% security-flaw data point that motivates promoting recurring lessons
- [Writing a good CLAUDE.md — HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — "treat CLAUDE.md like code: prune regularly"
