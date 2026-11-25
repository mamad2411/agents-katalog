---
name: second-opinion
description: "Call before an irreversible or costly step: a data schema, publishing outward, a teardown, an architecture choice, a release. Trigger words (RU+EN): уверен, точно так, необратимо, миграция, удалить насовсем, выкатываем, а вдруг сломаем / sure, is that right, irreversible, migration, delete for good, we're shipping, what if we break it. Calls ANOTHER model (DeepSeek) for an independent view. COMPLEMENTS code review, does not replace it; the answer is a hypothesis, verify it."
---

# Second opinion

An independent look by **another model** (DeepSeek) at a risky step. Your own Claude subagent would
give **correlated** mistakes — the value is precisely in a different model.

**THIS IS NOT a replacement for code review.** `code-reviewer` stays mandatory and primary. The
second opinion is an **extra** check on top, for the important/contested. It cancels nothing in the
cycle.

## When to call

- before an **irreversible** step (a migration with data loss, a merge into main, a wide refactor);
- on a high-stakes **architectural** decision (a new seam/contract, a choice of approach);
- when the **agent and `code-reviewer` diverge** or you are unsure yourself;
- by the owner's **explicit command** ("take a second opinion on X").

Do NOT call on routine (small edits, low cost of error) — it costs time/money.

## How to call

Two ways — same logic (`second_opinion()`), pick by taste:

**Native MCP tool** (if the MCP server is connected — `.mcp.json` in the plugin): call the
`second_opinion` tool with arguments `question` (required) + `context` (+ optional `model`). No
Bash-command construction — Claude calls it itself.

**CLI** (always works, without MCP):
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/second_opinion.py" "a concrete question" <<< "relevant context (diff/plan/finding)"
# default model: the one picked on the settings page (deepseek-reasoner unless changed); --model overrides
```
- **Question** — concrete ("is this seam drawn correctly?", "what am I missing in this refactor?").
- **Context** — the target chunk (diff, plan, a contested finding), NOT the whole repository.
- No key/an error → it says so gently and does not crash the cycle (it is an extra check) — same in
  CLI and MCP.

The DeepSeek key — env `DEEPSEEK_API_KEY` or `~/.config/retainer/deepseek_key` (chmod 600), outside
git.

## How to accept the answer

An opinion = a **hypothesis, not an authority.** Read → check against the code/reality → weigh →
decide yourself. Not "DeepSeek said so — I do it". [[receiving-review]] applies (verify before
adopting, one at a time, unclear → clarify). The synthesis is yours.

## When NOT to apply
Not on every task — only an important/irreversible step or a hard bug (the cost of error is high). Do
not run routine through a second opinion. And it is an ADDITION to `code-reviewer`, NOT a replacement
(your own reviewer first, then the cross-model one).

Related: [[task-cycle]] (an important/irreversible step), [[diagnosing]] (a second opinion on a hard
bug).
