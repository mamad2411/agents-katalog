---
name: proofread
description: Proofread the paper into report.md (content, citations, language, AI style, consistency), or apply report items.
disable-model-invocation: true
argument-hint: "[file or section] | apply R3 R7 ..."
---

Review the paper and write findings to `report.md`. The text itself stays untouched until the user asks to apply items.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

Two branches by argument:

- `apply <IDs>` (e.g. `apply R3 R7`, `apply all high`): go to **Apply**.
- anything else: a scope (a `.tex` file, or a section name you resolve to its file and lines), or nothing for the whole paper. Go to **Review**.

## Review

1. **Load the rules.** Load the `writing` skill and read its pattern list `${CLAUDE_PLUGIN_ROOT}/skills/writing/ai-patterns.md`, plus `## Style` and `## Terminology` from `CLAUDE.md`.
2. **Run the scripts.** `PK sync`, then `PK check [files] --json`. The check output is a list of candidates with suggested severity and category.
3. **Read report.md.** Note the highest ID used. Items marked `done` or `wontfix` are settled: do not report them again. Open items whose location lies in the scope are replaced by this run; open items outside the scope stay.
4. **Read the scope in reading order** (main file, then `\input` order) and review every paragraph, caption, footnote and table for:
   - **Content**: unsupported or overstated claims, gaps in the argument, results in the text that differ from the tables, missing baselines or details a reviewer would ask for.
   - **Citations**: each `\cite` against the paper it cites. Use the `literature` skill: the claim must match the notes or the paper body. Papers not `read-full` get read now. A citation that no body passage supports is 🔴. Also: claims that need a citation and have none.
   - **Language**: spelling, grammar, articles, agreement, the English variant from `paper.config.json`.
   - **AI-Style**: the patterns of the `writing` skill.
   - **Consistency**: terminology, abbreviations, notation, capitalization, tense, numbers.
   - **ACL-Compliance**: only what is visible while reading (e.g. no Limitations section; author names in a review version of an `acl-arr` paper, but not for `venue` `semeval`, where papers are not anonymous; check `paper.config.json`). The full check is `/acl-paper:guidelines-check`.
   Where a finding depends on intent you cannot read from the text (is this term deliberately different? is this the claimed contribution?), collect the questions and ask them with AskUserQuestion in one round before writing the items.
5. **Confirm the script candidates** in context. Drop false positives (an abbreviation that is a model name, a quote inside `\texttt`). Several identical low findings become one item listing all places.
6. **Write the items** into `report.md` in the format its header comment defines, under the severity heading, with new IDs counting up from the highest used. Each item quotes the text and proposes a concrete fix.

   Severity: 🔴 high misstates something, breaks a rule that blocks submission, or a citation that its source does not support. 🟠 medium is what a reviewer would flag. 🟢 low is polish.

Done when every paragraph in scope was read, every citation in scope checked against its source, and every script candidate confirmed or dropped. Then report in chat: counts per severity and category, and the three items to fix first.

## Apply

For each requested ID (`all high` = every open 🔴 item):

1. Find the location. Lines may have moved: locate the quoted text.
2. Make the smallest edit that resolves the issue, following the `writing` skill. Citation items follow the `literature` skill.
3. Set the item's status to `done` and move it under `## Closed`.

When an item has several reasonable fixes, or needs the authors' decision (content, results, formatting), ask with AskUserQuestion before editing. When it turns out wrong, leave it open, add a line `- **Note:** ...`, and say so. Report the applied edits as before → after.
