---
name: ohayo
description: 朝の計画を生成する。全アクティブ案件のWBSを読み込み、今日のタスクとタイムスケジュールを作成する。
---

# /ohayo — 朝の計画生成

## Overview

毎朝の「今日何をやるか」の意思決定を自動化するスキル。

WBS はプロジェクトの全体像を持っているが、そのまま見ても「今日のタスク」は自明ではない。
複数案件を掛け持ちしている中で、期限・遅延・引き継ぎを横断的に見て優先順位を提案するのが目的。

**なぜ Claude が判断するか（機械フィルタでないか）**
単純な日付フィルタでは「今日 From の作業」しか出てこない。
直前に終わらせるべき作業・遅延タスク・引き継ぎ中のものを文脈込みで拾うために、
WBS 全体を読んだうえで Claude が判断する設計にしている。

**なぜ 2 ファイルに書くか**
- `Desktop/task.md`: `/tf` `/bye` が参照する作業ファイル（当日限り上書き）
- `~/claude/daily/YYYY-MM-DD.md`: 翌朝 `/ohayo` が引き継ぎとして読む履歴ファイル

## Step 1: 前回の引き継ぎメモを読む

昨日の日付のファイルを確認する:

```bash
ls ~/claude/daily/ | sort | tail -1
```

ファイルがあれば Read ツールで読み込む。

## Step 2: アクティブ案件の CLAUDE.md を収集

```bash
find ~/claude/dev/active -name "CLAUDE.md" -maxdepth 2
```

各 CLAUDE.md を Read ツールで読み込み、以下を抽出する:
- プロジェクト名
- `## WBS` の `origin:` パス
- `## 役割` の値（manager | member）

## Step 3: WBS を読み込む

各案件の origin パスに対して:

```bash
python3 ~/.claude/scripts/read_wbs.py "{origin_path}"
```

JSON 出力から以下の条件でタスクを抽出（担当 = 松山）:

① 予定 From 〜 予定 To の期間が今日を含む
② 進捗ステータスが「遅延」または「期日未達」
③ 予定 To が今日から 7日以内
④ 引き継ぎメモに記載があるもの

機械的なフィルタではなく、WBS 全体を見た上で判断して提案する。

## Step 4: アウトプットを生成

以下の構成で 2 ファイルに出力する。

**① デスクトップ（毎朝上書き）**
`/mnt/c/Users/kmatuyama/Desktop/task.md`

**② 履歴**
`~/claude/daily/YYYY-MM-DD.md`（今日の日付）

### アウトプット構成

```
# YYYY-MM-DD（曜）今日の計画

## 全体スケジュール
​```mermaid
gantt
    title マスタースケジュール
    dateFormat YYYY-MM-DD
    section {PROJECT_NAME}
        {Lv.1タスク名} :{planned_from}, {planned_to}
​```
※ WBS Lv.1 のみ使用

## 今日のタスク

### {PROJECT_NAME} [manager|member]
- [ ] {タスク名}
- [ ] 管理アクション: {リマインド内容}  ← manager のみ

## タイムスケジュール
| 時間 | 内容 |
|------|------|
| 09:00〜XX:XX | {案件}: {タスク} |
| 12:00〜13:00 | 休憩 |
| 13:00〜17:00 | {案件}: {タスク} |
```

### 制約
- 稼働時間: 7時間（09:00〜17:00）
- 休憩: 12:00〜13:00 固定
- タスクの合計が 7時間を超える場合は優先度を考慮して調整する
