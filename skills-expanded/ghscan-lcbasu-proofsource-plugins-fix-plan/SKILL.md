---
name: fix-plan
description: Turn Proofsource's open AI visibility gaps into a prioritized fix plan, then track new buyer questions and record shipped fixes. Use when the user asks how to get mentioned by AI, what to fix first, or says they shipped a fix.
---

# Fix plan

Build the plan from Proofsource's open gaps only. Never invent a gap, a source or an impact number.

## Steps

1. **Pick the brand.** Call `list_brands`. One brand: use it. Several: ask which one, unless the user already named it.
2. **Open gaps.** Call `list_fix_opportunities`. Each gap carries its evidence (the questions and engines where AI leaves the brand out) and a suggested fix.
3. **Prioritize.** Rank gaps by the number of buyer questions affected, then by how many engines miss the brand, then by effort (an edit to an existing page beats a new page). Keep the top 5.
4. **Plan.** For each gap, turn its suggested fix into one concrete action: the page to change or create and what to add. Quote the gap's evidence so the user sees why it matters.
5. **Confirm before writing.** Ask before any write. Then:
   - To track a buyer question the plan depends on, call `list_topics` for the topic id and `create_prompt` with the question phrased the way a buyer would ask.
   - When the user says a fix is live, call `mark_fix_shipped` with the gap id, one or two sentences on what shipped, and the ship date.
6. **Check results.** For fixes already shipped, call `get_fix_verification` and report each verdict as given: moved, within normal answer churn, or waiting for more answers.

## Output

- A numbered plan: action, gap questions, engines that miss the brand, effort (small, medium, large).
- Proof for each item: the gap id and the tool it came from. Link `open_url` when the results carry one.
- After a write, confirm exactly what was recorded.

## Rules

- Write tools change the user's workspace. Never call them without a clear yes.
- Say "competitors", never "rivals".
- No prices, plan names or upgrade links.
