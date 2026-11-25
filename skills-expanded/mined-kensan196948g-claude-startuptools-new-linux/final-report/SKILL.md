---
name: final-report
description: ClaudeOS v10 の最終報告様式。Phase 完了、リリース後安定化、セッション終了時に、検証結果を PASS / FAIL / BLOCKED / NOT RUN で明示した報告を作る。
when_to_use: 安定化完了時、5 時間到達時、BLOCKED で停止する時、ユーザーが最終報告を求めた時。
user-invocable: true
---

# Final Report (ClaudeOS v10)

## Purpose
推測を排し、根拠付きで状態を伝える。GO / CONDITIONAL GO / NO-GO を明示する。

## Procedure
次の見出しで報告する (該当なしは「該当なし」と書く):
1. Executive Summary (GO / CONDITIONAL GO / NO-GO)
2. 採用した実行方針 (agent-router の決定と理由)
3. Phase 別の変更内容
4. 変更ファイルと主要設計判断 (Decision Log)
5. Subagent / Background Agent / Agent Teams / Workflow の実行内容
6. レビュー結果 (独立レビュー、security-reviewer、outcome-grader)
7. テスト・build・CI 結果 (PASS / FAIL / BLOCKED / NOT RUN)
8. WebUI / API の確認方法
9. Cloudflare および Local PostgreSQL の状態 (health / backup 鮮度 / restore drill)
10. branch / commit / PR / release 状態
11. deployment または未実施理由
12. migration / backup / restore / rollback 結果
13. 障害、修正内容、再発防止策
14. 残課題と残存リスク (Human Decision Required を含む)
15. production-safe 判定
16. design-consistent 判定
17. CTO としての推奨判断

## Validation
数値・URL・commit は実測値のみ。未実施を成功扱いにしない。

## Output
上記様式の日本語レポート。安定化完了後は「一旦終了」を宣言し、セッションは起動したまま次の指示を待つ。
