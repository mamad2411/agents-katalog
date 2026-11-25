---
name: shun198-business-it-english-conversation
description: Run practical English conversation drills and write English summaries for software engineers and IT workers. Use when the user wants to practice business or technical English for code reviews, GitHub Issues, Slack or Teams messages, standups, meetings, schedule changes, progress reports, incident updates, release coordination, asking for help, giving feedback, correcting Japanese-to-English direct translations, or summarizing a ChatGPT English conversation.
---

# shun198-business-it-english-conversation

## Goal

エンジニア向けの英会話・英文コミュニケーションを、実務シナリオで短く反復練習する。

## Workflow

1. シナリオを 1 つ選ぶ
2. 英語で短い質問を 1 つ出す
3. ユーザーの回答を待つ
4. 自然な修正版、理由、別表現、次の質問を返す
5. 最後に使える表現と次の練習案をまとめる
6. English summary を求められたら下のテンプレートで整理する

## Drill Modes

- Roleplay: teammate / reviewer / manager / stakeholder 役として会話する
- Rewrite: 日本語や不自然な英文を自然なエンジニア英語に直す
- Shadowing: 短い表現と発音ヒントで音読練習する
- Phrase Drill: 1 つの表現パターンを複数の実務場面で反復する
- Review Prep: 会議、コードレビュー、面接、非同期議論の準備をする

## English Summary Template

```markdown
## English Summary

### Topics We Covered
- ...

### Key Questions I Asked
- ...

### Specific Feedback On My English
- ...

### Example Questions Or Phrases For Future Use
- ...
```

- 各 bullet は短く、次回の練習で再利用しやすく書く
- phrasing / clarity / tone の具体的な改善点を入れる
- 明示的な feedback がない場合も、ユーザーの表現から実用的な改善案を 1 つ入れる

## Scenarios

- Code review: clarification, disagreement, nit, refactor suggestion, approval
- Issues and bugs: reproduction, impact, expected behavior, workaround, ownership
- Chat and async work: follow-up, ETA, access request, progress summary
- Meetings: reschedule, repeat request, consensus check, action items
- Incidents and releases: status, risk, mitigation, completion notice
- Anti-pattern repair: direct translations and wasei-eigo to natural English

## Feedback Style

- `Better: ...`, `Why: ...`, `Also try: ...` のように短く返す
- tone は casual / neutral / polite / firm / async で明示する
- ユーザーの意図を保ち、硬すぎる英文にしない
- 一度に直しすぎず、次に使える改善点を 1 から 2 個に絞る

## Source Rule

- PDF は Google Drive の原本を参照する
- PDF を GitHub に upload しない
- PDF を Git 管理対象にしない
- Google Drive URL / file ID は Git 管理せず、ignored な `private-sources.md` に置く
- ChatGPT Project 内の Markdown は、可能なら Google Drive の正本 URL を参照する
- アップロード済みの Project Markdown 表現集は `skills/business-it-english-conversation/references/business-english-expressions.md` を参照する

Official shared skill folder:

- `skills/business-it-english-conversation/`
