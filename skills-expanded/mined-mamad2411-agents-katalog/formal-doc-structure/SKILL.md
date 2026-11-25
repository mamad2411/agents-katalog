---
name: formal-doc-structure
description: Draft, revise, or restructure formal internal business documents in Traditional Chinese (Taiwan corporate / financial-institution usage) — 簽呈, 會議紀錄, 評估報告, 專案規劃, 採購與廠商溝通, 對主管簡報, 驗收與交付, 跨單位協調. Picks a reader-driven structure per document type and produces a usable draft, not just advice. Trigger when the user asks to write or fix an internal business document, memo, report, meeting record, plan, or vendor communication. Do NOT invoke for RFP / 招標規格 / 需求規格書 (use rfp-writing), for pure language cleanup with no structural work (use avoid-ai-writing / clean-ai-writing), or for casual chat, creative writing, marketing copy, or code comments.
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing formal-document zh-tw traditional-chinese business
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F4C4"
---

# Formal Internal Document Structure

Produce internal business documents that help a reader decide, approve, assign work, review risk, brief management, communicate with a vendor, or verify completion. The output is a usable draft — complete sections that paste straight into a document — not a critique.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## When to use

Use when the request names one of these artifacts (or a clear equivalent):

- 簽呈與核准文件, 經費 / 人力 / 資源申請
- 會議紀錄 (內部、廠商、審查)
- 專案規劃 / 執行計畫, 組織與人力規劃, 訓練與培育文件
- 需求文件, 評估報告, 風險說明
- 採購與廠商溝通文件 (詢問、澄清、合作範圍)
- 制度 / 流程 / 作業規範, 問題追蹤與改善報告, 驗收與交付文件
- 對主管簡報文字, 對外回覆稿, 跨單位協調材料

## When NOT to use

Each of these has conventions that conflict with internal-business-doc rules:

- **RFP / 招標規格 / 需求規格書 / 投標 issuer specs** → use `rfp-writing`. That skill governs documents sent out for bidding; this one governs documents that circulate inside the organization.
- **Pure language cleanup** (remove AI-isms from existing text, no structural change) → use `avoid-ai-writing` / `clean-ai-writing`. Reach for this skill when the job also involves *organizing* a document by type.
- Casual conversation, creative writing, marketing / advertising copy, or code comments — unless the user explicitly asks for an internal-document style.

Do not force every document into a project-plan shape. Pick the structure from the reader's need (see below).

## Core writing principles

1. **Write like an experienced internal staff member** — a project owner, IT lead, HR partner, procurement officer, or risk reviewer preparing the document for internal circulation. Grounded, practical, business tone. Not promotional, not slogan-like.

2. **Every sentence must earn its place.** Keep a sentence only if it adds a decision, requirement, constraint, risk, responsibility, deliverable, timeline, verification method, follow-up action, or concrete explanation. Cut filler, restatement, and abstract conclusions. This is the same discipline `avoid-ai-writing` enforces, applied while you build the document. See [references/language.md](references/language.md) for the prohibited-phrase list and fixes.

3. **Use affirmative planning language.** Write what *will* be done, proposed, provided, and how it is verified — 預計採…, 規劃…, 建議…, 應提供…, 需完成…, 由…負責…, 成果包含…, 後續依…辦理…. Avoid negative framing (不建議…, 不宜…, 不是…而是…); when contrast is needed, rewrite it as a direct implementation statement.

   > Poor: 不建議僅以會議討論作為結論，而是要形成後續追蹤項目。
   > Better: 會議結論需整理為後續追蹤項目，並列明負責單位、預計完成時間及檢核方式。

## Pick the structure from the reader's need

Choose by what the reader must decide, approve, understand, or execute. Full templates in [references/structures.md](references/structures.md):

| Reader need | Document type | Template |
|-------------|---------------|----------|
| Sign off / approve / fund | 決策或核准文件 (簽呈, 採購, 預算) | A |
| Compare options / assess risk | 評估報告 | B |
| Record what was decided | 會議紀錄 | C |
| Execute a plan | 執行 / 作業計畫 (專案, 訓練, 流程) | D |
| Coordinate with a vendor | 廠商 / 對外溝通 | E |

Then apply three structural habits (detail in references):

- **Keep chapters concentrated** — group related ideas (背景+現況, 範圍+假設, 交付物+驗收, 風險+控管). Fewer, stronger chapters beat many thin ones.
- **Summary before detail** — open a heavy section with one or two sentences of planning intent / conclusion, then the steps or tables.
- **Don't repeat other documents** — in an appendix or follow-up, reference the parent (本文件承接主文件之…) and focus only on this document's unique purpose.

## Content must be concrete enough to execute

Stop short of conceptual statements. For each important activity, name the responsible unit, owner, timeframe, scope boundary, deliverables, acceptance criteria, review cadence, and follow-up mechanism. Every activity gets a corresponding output (meeting→紀錄/決議/待辦; review→評估備忘/發現/追蹤清單; vendor work→交付物/驗收紀錄/問題log; system task→測試/部署/rollback 紀錄).

> Poor: 需加強後續管理。
> Better: 後續由承辦單位每月彙整執行情形，內容包含進度、待辦事項、風險、需主管協調事項及預計完成時間。

Drafting patterns for each paragraph type (purpose, background, execution model, responsibility split, vendor scope, risk/control, acceptance) are in [references/language.md](references/language.md).

## Revision checklist

Run before finalizing:

1. Does every section have a clear purpose, and can any two be merged?
2. Is any paragraph repeating a point made elsewhere?
3. Are tables necessary and decision-oriented (not restating the prose)?
4. Are responsibilities — responsible / supporting / review / vendor / escalation — clearly assigned?
5. Are time, deliverables, and acceptance criteria specific enough to act on?
6. Does the document connect the proposal to daily work (who owns it, what outputs, how reviewed)?
7. Are vendor requirements concrete enough to discuss or quote against?
8. Are risks, assumptions, and constraints stated plainly?
9. Are all AI-style slogans and filler phrases removed (see references/language.md)?
10. Is the tone formal, practical, and fit for internal review?

## De-AI finishing pass

After the checklist passes, offer `avoid-ai-writing-zh` as a deep de-AI pass over the draft, a far richer AI-ism ruleset than item 9's own light check (references/language.md). Run it only if the user agrees; otherwise finalize as-is. This is the last step before final output.
