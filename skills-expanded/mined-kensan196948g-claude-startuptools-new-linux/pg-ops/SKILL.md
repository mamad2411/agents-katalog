---
name: pg-ops
description: Local PostgreSQL の運用手順 (health / init / backup / verify / restore drill / freshness / migration-risk / systemd unit 生成)。DB を持つプロジェクトの初期化、migration 前、リリース前後、定期点検で使う。
when_to_use: 新規 DB の作成、migration 適用前のスナップショット、backup の鮮度確認、復元可能性の証明、Mission Control の DB 警告対応。
allowed-tools: Bash(bash bin/pg-ops.sh *), Bash(bash libexec/diag-postgres.sh*), Read
---

# PostgreSQL Ops (ClaudeOS v10)

## Purpose
「バックアップが存在する」ではなく「復元できる」ことを定期的に証明し、破壊的操作を Human Approval Gate へ導く。

## Procedure
- 初期化: `bash bin/pg-ops.sh init <project> [--password-file <0600 file>]` → 専用 role / database。DATABASE_URL は `~/.config/<app>/db.env` (0600) へ (値を出力しない)
- 健全性: `bash bin/pg-ops.sh health <db>` (pg_isready + disk)。`bash libexec/diag-postgres.sh` で全 DB の一覧
- backup: `bash bin/pg-ops.sh backup <db>` (pg_dump -Fc + sha256 + retention 14d + 即時検証)
- 復元検証: `bash bin/pg-ops.sh restore-drill <db>` (`<db>_recovery` へ実復元しテーブル数・行数照合)。週次 timer は `bash bin/pg-ops.sh units <project> <db>` で生成 (`--install` は運用者判断)
- migration 前: `bash bin/pg-ops.sh migration-risk <sql-dir>` → HUMAN_APPROVAL なら `/approval-pr`。additive なら `backup` を取ってからホスト側で適用
- 監視: `bash bin/pg-ops.sh status <db> --json` (health / size / backup 鮮度 / drill 結果)

## Validation
restore drill が PASS、freshness が 26h 以内、Mission Control の DB 警告なし。

## Failure Handling
drill FAIL → 復元手順とバックアップ世代を確認し、原因 (欠損 / 破損 / 版不一致 PG_BIN) を特定。backup 失敗 → disk / 権限 / socket を確認。DROP / TRUNCATE / 条件なし DELETE / 本番 `pg_restore --clean` は実行せず停止。

## Output
各コマンドの PASS / FAIL と `~/.claudeos/pg/drill-<db>.json`。
