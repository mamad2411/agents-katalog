---
name: webui-health-check
description: Mission Control WebUI の健全性を確認し、問題があれば修正または Issue を起票する検証ループ
---

# WebUI 健全性チェックスキル

Dashboard WebUI (`http://localhost:3737`) の稼働状態と設定を確認し、
問題を検出したら修正 → 再確認まで行う検証ループです。

## 実行手順

```bash
# 1. サーバー稼働確認
curl -s http://localhost:3737/api/health | python -m json.tool

# 2. システム健全性確認
curl -s http://localhost:3737/api/system-health | python -m json.tool

# 3. 認証設定確認
# authEnabled: false の場合は DASHBOARD_PASSWORD 環境変数設定を推奨
```

## 重要チェック項目

| チェック | 状態 | 対応 |
|---|---|---|
| `authEnabled` | ⚠️ false | `DASHBOARD_PASSWORD` または `config.json.dashboardAuth` を設定 |
| `packageJsonMissing` | ⚠️ true | `package.json` を作成 |
| `claudeSkillsMissing` | ⚠️ true | `.claude/skills/` を作成 |
| `dashboardTaskState` | ✅ Ready | タスクスケジューラー登録済み |

## 検証ループ

1. 上記チェックを実行し、⚠️ 項目を列挙する
2. 安全に自動修正できる項目（設定ファイル・ディレクトリ作成）は修正して該当チェックのみ再実行する
3. 自動修正できない項目（認証パスワード設定など人間の決断が必要なもの）は Issue を起票する
4. 全チェックの最終状態を PASS / FAIL / BLOCKED / NOT RUN で報告する
