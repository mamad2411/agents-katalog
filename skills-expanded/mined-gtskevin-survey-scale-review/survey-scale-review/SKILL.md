---
name: survey-scale-review
description: Use when reviewing research survey scales, for organizational behavior, management, marketing, psychology, and social science research questionnaires with English source items, Chinese translations, adapted scales, reverse-coded items, paired leader-employee surveys, multi-wave surveys, or pre-launch questionnaire quality checks.
---

# Survey Scale Review

Use this skill to review OB/management research questionnaires and scale translation/adaptation files. Default language is Chinese unless the user asks otherwise.

## Default stance

- Default mode is **修改建议模式**: produce a concise Chinese chat summary plus a user-facing **custom dashboard HTML review page**. The HTML should contain the executive summary, issue list, and modification suggestions in one copy-friendly page.
- For `formal_review`, the default user-facing artifact must be the **v4 精简仪表盘版** style: card-based layout, visual executive dashboard, prominent disclaimer card, compact update panel with buttons, 10-minute decision section, top action table, researcher decision cards, scale diagnosis cards, and a concise key revision table. Do not rely on plain `pretty-doc` Markdown rendering as the primary formal-review output unless custom HTML generation is unavailable.
- Do not output a long Markdown report by default. Use Markdown only as an internal/source format when needed to render HTML, or when the user explicitly asks for Markdown.
- The substantive review must be done by the language model's item-by-item judgment. Rules and scripts only focus attention and extract structure; they do not replace the model's semantic review.
- By default, include a suggested revised version for problematic items and instructions in the HTML report. Preserve the original wording beside `建议修改版`, `修改理由`, `审稿解释`, `建议采纳级别`, and `研究者确认`.
- Do not automatically create a separate rewritten questionnaire file unless the user asks for one. The default HTML report should already contain the recommended revised wording needed for review.
- Formal reports should be usable by early-stage doctoral students without forcing them to read a long report. Use a **progressive disclosure** structure and dashboard UI: a short decision-focused front section first, then optional details/appendix later.
- Keep the main report concise by default. Put only the launch decision, top risks, researcher decisions, minimal action checklist, and highest-value suggested wording in the front section. Move comprehensive row-by-row notes to an appendix or separate file unless the user explicitly asks for exhaustive review.
- Explain key scale-review concepts with `{{术语|解释}}` hover glossary syntax and short `> 📖` learning callouts, but only where they help users understand a decision. Avoid turning every issue into a lesson.
- Put a visual executive dashboard near the top: launch recommendation, P0/P1/P2/P3 counts, RA-action count, researcher-confirmation count, expert-review count, and the first 5-8 actions to take. This should be rendered as visual metric cards, not only as a Markdown table.
- For every P0/P1 issue, include `为什么重要` and `谁来处理` so users understand the methodological consequence and ownership.
- Distinguish `资料确认`, `模型推断`, and `需源文核验` when the judgment depends on source-text limits.
- Put a visually prominent disclaimer at both the beginning and end of every formal report: AI helps identify risks but does not replace expert human review, back-translation, pretesting, or validity evidence.
- Include a non-technical update panel in formal HTML reports: local commit short SHA and commit date when available, a visible `检查新版本` link to GitHub, and a copyable prompt that users can paste into Codex/Claude Code/WorkBuddy to update the skill. If the local SHA is known, prefer a GitHub compare link from that SHA to `main`; otherwise link to the repository's commits page.
- Treat reverse-coded source items according to the Skill Creator's default review stance: reverse items are usually rewritten into positive wording to reduce respondent confusion. Check whether positive wording is accurate and whether scoring notes are updated; do not mark positive wording as an error by itself.
- For mature non-adapted scales, do not re-evaluate whether items cover the construct. Check translation equivalence, clarity, response options, respondent experience, and file consistency.
- For adapted, self-developed, or highly adapted scales, focus on whether the adaptation is defensible to reviewers and whether items have common scale-design problems.

## Modes

Choose the mode from the user's request; when unclear, use `formal_review`.

| Mode | When to use | Output focus |
|---|---|---|
| `quick_check` | RA has just prepared a scale file | Blocking issues: item counts, respondent/time mismatch, placeholders, missing fields |
| `formal_review` | Researcher wants a full review | Report + issue list + modification suggestions |
| `pre_launch_check` | Survey is nearly ready to distribute | Launch readiness: instructions, referents, pairing IDs, time windows, response options |

## Workflow

1. Inspect the source file structure. For Excel, prefer `scripts/inspect_workbook.py` to summarize sheets, columns, variable blocks, items, sources, placeholders, reverse-coded markers, and obvious consistency issues when the local environment can run Python with `pandas` and `openpyxl`.
   - The user does not need to run this script manually.
   - If the script dependencies are unavailable, do not fail the review. Use the agent's available spreadsheet/file-reading tools to inspect the workbook, or tell the user what dependency is missing only if no fallback is available.
   - If the file is not in the template format, first infer its structure and report missing information before judging translation or adaptation quality.
   - The script output is only a **structure pre-check**. Never treat the script-generated `issues.html` as the final review for a formal review, because it cannot judge translation equivalence, adaptation quality, instruction contamination, double-barreled wording, or level-of-analysis problems.
   - Use script outputs as evidence and navigation aids, then perform the actual review directly with the language model.
2. Build a variable-item index: variable name, Chinese name, respondent, wave, item count, source, original item, current Chinese item, notes.
3. Classify each scale as mature direct translation, explicitly adapted mature scale, implicitly adapted mature scale, self-developed scale, highly adapted scale, or mixed scale.
   - Do not depend on the user's labels. Infer implicit adaptation when the current variable name, instruction, or Chinese wording changes the source construct, object, context, actor, referent, response perspective, or level of analysis.
   - Example: a source item about `AI training` or learning from AI training used under `AI self-efficacy` should be treated as likely adapted from an AI training efficacy/training-learning context, even if the user did not label it as an adaptation.
4. Run blocking checks first: item-count mismatch, respondent mismatch, wave mismatch, missing original/current item text, missing source, placeholders, unresolved internal notes, reverse-scoring conflicts.
5. Run a **row-by-row semantic audit** before writing the final report:
   - For every item with English source text, compare the English and Chinese item directly. Identify added concepts, omitted concepts, changed intensity, changed actor, changed object, changed time frame, changed valence, and changed observability.
   - For every adapted item, separate reasonable object/context replacement from meaning-changing adaptation. If the Chinese item measures a different behavior, cognition, emotion, outcome, or causal mechanism, flag it even when the Chinese reads fluently.
   - For every instruction block, check whether it defines the construct, reveals the intended variable, explains what the scale is "really" measuring, or tells respondents what not to consider. Such instructions can contaminate responses and should be flagged.
   - For every self-developed or highly adapted item, check double-barreled wording, social desirability, moralized/accusatory wording, construct contamination, causal wording, unsupported premises, and response-option fit.
   - For leadership, team, and paired designs, explicitly check referent and level of analysis: `我的领导/领导层`, `我/我们`, `团队/部门/组织`, `员工/下属/团队成员`, and whether the respondent can observe the target.
6. Generate suggested revised wording for each substantive problem unless a revision would require a theory decision the researcher must make first.
   - If researcher judgment is needed, provide 2-3 wording options tied to alternative theoretical choices, such as individual-level `我` vs team-level `我们`.
   - Keep original source items visible so users can compare English, current Chinese, and suggested Chinese.
   - Split theory-dependent alternatives into separate options, not a single slash-form sentence, so RA does not accidentally combine incompatible referents.
7. Review scales using the appropriate standard:
   - Direct mature scales: translation equivalence and respondent clarity.
   - Adapted mature scales: adaptation logic and reviewer defensibility.
   - Self-developed/highly adapted scales: common item-writing errors and psychometric design risks.
8. Review respondent experience: ambiguity, referents, team/leader/AI definitions, time windows, sensitive wording, response-option fit.
9. Produce concise Chinese outputs. For formal reviews, make a custom v4-style dashboard HTML the primary user-facing artifact and keep the chat response short. If maintaining Markdown, save it only as an editable source or content draft; do not make plain `pretty-doc` output the main formal-review deliverable unless custom HTML generation is blocked. If using the user's Pretty Doc workflow, satisfy the "HTML not chat" principle with the custom dashboard HTML first; optionally also keep/render a Markdown source for editability.
10. Add an update panel and report footer with `Survey Scale Review 本地版本`, `commit 日期`, `检查新版本`, and `复制更新提示词` when possible. Do not interrupt normal review work to browse GitHub for updates unless the user asks for an update check.

## When to load references

- Load `references/evaluation-rubric.md` for severity levels, core criteria, reverse-item handling, and scale-type-specific standards.
- Load `references/translation-equivalence.md` when English source items and Chinese translations are both present.
- Load `references/adaptation-review.md` when a file includes adapted scales or AI/context replacement.
- Load `references/respondent-experience.md` for ambiguity, instructions, response options, and paired survey checks.
- Load `references/report-template.md` before writing a full review report.
- Load `references/output-formats.md` when creating an issue list, suggestion table, or optimized questionnaire comparison.

## Output requirements

Default formal review outputs:

1. One user-facing **custom dashboard HTML** review page in Chinese, using the v4 精简仪表盘版 layout: prominent opening disclaimer, non-technical update panel with `检查新版本` and `复制更新提示词` buttons, visual dashboard metric cards, brief beginner guide, top P0/P1 action list, researcher decision cards, minimal suggested revised wording table, short scale-level notes, optional appendix, and prominent closing disclaimer.
2. The HTML issue and suggestion tables must be copy-friendly. Use Chinese column headers, priority colors or badges, a top summary, top P0/P1 issues, a `变量/量表` column, `为什么重要`, concrete suggested wording, evidence status (`资料确认` / `模型推断` / `需源文核验`), and clear action ownership (`RA 可直接处理`, `研究者确认`, `建议专家复核`, `仅提示`) whenever available.
3. Default formal report length target: enough for a researcher to understand the main decisions in 10 minutes. Prefer 5-8 top issues and 10-20 suggested revisions in the main body; put extra item-level details in an appendix.
4. Optional formatted Excel workbook only when the user explicitly wants spreadsheet processing.
5. Avoid plain long-document HTML for formal review. A generic Markdown-to-HTML page is acceptable only for quick notes, source drafts, or fallback. If both files exist, link/open the dashboard HTML as the main report and identify the Markdown/plain HTML as secondary source material.

For install/update requests, prefer these local checks:

- Codex path: `~/.codex/skills/survey-scale-review`
- Claude Code/WorkBuddy path: `~/.claude/skills/survey-scale-review`
- If the directory is a git clone, update with `git -C <path> pull --ff-only`.
- If it is not a git repository, back up the old directory and reinstall from `https://github.com/gtskevin/survey-scale-review`.
- After updating, report the local commit short SHA and commit date.

For report update panels:

- Use the button label `检查新版本`.
- If local commit SHA is known, link to `https://github.com/gtskevin/survey-scale-review/compare/<local-sha>...main`.
- If local commit SHA is unknown, link to `https://github.com/gtskevin/survey-scale-review/commits/main`.
- Include a second button or compact text area labeled `复制更新提示词`, containing a plain-language update request for the user's current agent.
- Make clear that clicking the link only checks whether a newer GitHub version exists; updating local files still needs the user's Agent to perform the update.

Avoid long Markdown, CSV, and Excel as the default user-facing output because long questionnaire text is easier to review in the cleaner HTML page. CSV/JSON can be kept as machine-readable support files.

## Boundaries

- Do not claim to have verified original journal scale wording unless the source document or article text was provided or explicitly looked up.
- Do not replace researcher judgment on construct boundaries, high adaptation, or self-developed scale validity.
- Do not silently overwrite original questionnaire content.
- Do not treat all item wording changes as final. Label high-adaptation suggestions as needing researcher confirmation.
