---
name: postready
description: >
  Run the full publish-ready pipeline on source content — generate LinkedIn posts, fact-check them, tighten them, and HR-screen them — all in one shot, end-to-end. Trigger this skill whenever the user types /postready, says "make this publish-ready", "run the full pipeline", "give me final posts from this", or shares source material (PDF, email, newsletter, URL, pasted text) and signals they want finished, ready-to-publish posts rather than rough drafts.
---

# Post-Ready Pipeline

End-to-end content pipeline. Source material in → publish-ready LinkedIn posts out.

Runs four skills in sequence, automatically. No checkpoints. No menu. No asking which steps to run.

1. **content** — draft 3–4 posts from the source
2. **factcheck** — verify factual claims (Standard tier, no tier picker)
3. **hatchet** — tighten each post
4. **ask-hr** — HR-screen each post and apply rewrites for anything flagged

> **Setup note:** This skill orchestrates four other skills (`content`, `factcheck`, `hatchet`, `ask-hr`). All four must be installed. The path references below assume they live under your skills directory (e.g. `~/.claude/skills/content/SKILL.md`) — adjust if yours are different.

---

## Step 1: Generate the drafts (content)

Read the `content` SKILL.md and follow its instructions to:
- Identify and ingest the source content (pasted text, PDF, URL, email, newsletter, etc.)
- Find the best 3–4 angles
- Draft full-length posts in the user's voice (using the `post` skill)

**Two important deviations from `content`'s normal flow:**

- **Skip `content`'s internal factcheck step.** This pipeline runs factcheck centrally in Step 2 — don't double up.
- **Do not "present" the posts yet.** `content` normally ends by presenting finished drafts to the user. Here, treat the drafts as intermediate output and pass them to Step 2.

---

## Step 2: Fact-check the drafts (factcheck — Standard tier)

Read the `factcheck` SKILL.md and run the **Standard tier** on every post that contains:
- Statistics or numbers
- Named figures, organizations, or surveys
- Specific historical, scientific, or attributed claims

**Skip the tier picker entirely.** Don't ask which tier — always Standard.

For each ❌ Incorrect or ⚠️ Partially correct finding, apply the suggested fix directly into the draft. Keep a one-line note per fix for the final summary (e.g. *"Post 2: corrected '85% of jobs in 2030' → 'a widely cited but unsourced claim removed'"*).

If a post has no checkable claims, skip the search and note *"no claims to check"* in the pipeline notes.

---

## Step 3: Tighten each post (hatchet)

Read the `hatchet` SKILL.md and run hatchet on each (now factchecked) post.

- Default target: roughly 50% reduction
- If a post is already tight, just clean it up — don't over-cut
- Preserve the user's voice and the sharp opening line
- Do not collapse the post into a single paragraph if the original used line breaks for rhythm

The hatchet output is intermediate — feed it into Step 4, don't present it yet.

---

## Step 4: HR-screen each post (ask-hr)

Read the `ask-hr` SKILL.md and run an HR review on each tightened post.

For each post, decide based on the verdict:

| Verdict | Action |
|---|---|
| ✅ Clear or 🟢 Low Risk | Keep the post as-is from Step 3 |
| 🟡 Moderate Risk | Use the **Full Rewrite** from `ask-hr` as the final version |
| 🔴 High Risk | Use the **Full Rewrite** from `ask-hr` as the final version, flag prominently in pipeline notes |

Keep HR notes brief — name the issue and severity, one or two lines per flagged post. Don't include the full risk-score table in the final output.

---

## Step 5: Present the final posts

Format the response exactly like this:

---

### 📦 Post-Ready: [N] posts

**Post 1 — [angle type]**

[Final post text — factchecked, tightened, HR-cleared]

---

**Post 2 — [angle type]**

[Final post text]

---

*(repeat for each post)*

---

### 🔧 Pipeline notes

**Factcheck:** [one line per fix applied, or "All claims verified" / "No checkable claims"]

**Hatchet:** [rough reduction summary, e.g. "Posts trimmed ~40–55%" or "All posts already tight, light cleanup only"]

**HR:** [any flags caught and the rewrite applied, or "All posts cleared"]

---

End by asking which (if any) the user wants to adjust further.

---

## What NOT to do

- Do NOT pause for approval between steps — the whole point of `postready` is end-to-end automation
- Do NOT show intermediate drafts (raw, factchecked-but-not-trimmed, etc.) — only the final versions
- Do NOT skip any of the four steps on any post, even ones that look "obviously fine"
- Do NOT use a different factcheck tier — always Standard
- Do NOT over-cut tight posts in the hatchet step
- Do NOT open posts with newsletter meta-framing ("This week's newsletter…", "I read a PDF that…") — same rule as `content`
- Do NOT include the full `ask-hr` risk-score table or the full `factcheck` per-claim report in the final output — keep pipeline notes brief
