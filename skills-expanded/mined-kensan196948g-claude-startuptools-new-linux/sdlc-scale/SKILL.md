---
name: sdlc-scale
description: 変更規模 (S / M / L) から AI-Native SDLC の必須成果物 (intent / spec / plan / architecture / test-plan / eval-plan / review-report / release-report) を縮退・拡張して決める。作業開始時に使う。
when_to_use: 新しい Issue / Intent に着手する時。小規模修正に全成果物を強制しないため、まず規模判定を行う。
allowed-tools: Read, Bash(node scripts/tools/agent-router.js *)
---

# SDLC Scale (ClaudeOS v10 AI-Native SDLC)

## Purpose
Intent → Specification → Plan → Implementation → Tests → Evals → Review → PR → CI/CD → Monitoring → Feedback → Improvement を、規模に応じて過不足なく回す。

## Procedure
1. 規模を判定する:
   - **S**: ≤3 ファイル、< 30 分、動作・API・DB・権限に変更なし (docs / typo / 設定微修正)
   - **M**: ≤20 ファイル、機能追加・バグ修正、DB は additive のみ、公開 API 変更なし
   - **L**: それ以上、または architecture / DB / 認証 / deployment / security に影響
2. 必須成果物 (`Claude/templates/claudeos/sdlc/*.md` のテンプレートを使う):
   | 成果物 | S | M | L |
   |---|---|---|---|
   | intent.md | PR 本文の「目的」で代替 | ○ | ○ |
   | spec.md | 不要 | 簡易 (受入条件のみ) | ○ |
   | plan.md | 不要 | ○ | ○ (plan mode で作成) |
   | architecture.md | 不要 | 不要 | ○ (ADR 含む) |
   | test-plan.md | 既存テスト実行 | ○ | ○ |
   | eval-plan.md | 不要 | 該当 skill / router 変更時 | ○ |
   | review-report.md | /code-review | /code-review + security-reviewer | 独立 QA + security + adversarial |
   | release-report.md | PR 本文で代替 | ○ | ○ + rollback 演習 |
3. `/agent-router` で実行形態を決め、成果物の置き場を `docs/sdlc/<issue-or-slug>/` (プロジェクト側) に作る。

## Validation
L で成果物が欠けている PR は品質ゲート未達として扱う。

## Output
規模判定 (S/M/L)、必須成果物リスト、担当実行形態。
