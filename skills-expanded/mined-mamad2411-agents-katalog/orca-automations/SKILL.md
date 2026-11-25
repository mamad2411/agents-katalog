---
name: orca-automations
description: "Only use when the user explicitly invokes /orca-automations (or $orca-automations in Codex). Never auto-invoke. Orca の自動化（Automations）を orca CLI で作成・管理するスキル。「毎朝9時に◯◯して」「定期実行・スケジュール実行する automation を作って」「自動化の一覧・実行履歴・削除」を Orca 利用環境で求められたときに使用する。フラグ仕様はインストール済み CLI への問い合わせに委譲し最新仕様に追従する。OS の cron・CI のスケジュール・Claude Code 自身の定期実行には使わない。"
disable-model-invocation: true
metadata:
  tags: [orca, automation, scheduling, cli]
---

# Orca Automations

Orca の automation は、指定したプロバイダ（`codex` / `claude` など）が、実行ごとの新規 worktree または既存 workspace に対してスケジュール実行する Orca 管理のプロンプトである。CLI は起動中の Orca アプリへ RPC するため、Orca アプリが起動している必要がある。

## 実行ファイルの選択

セッション冒頭で一度だけ実行ファイルを決め、以降のコマンド例の `ORCA` をその値に置き換える（`ORCA` というシェル変数を作ったり、`ORCA` を文字どおり実行したりしない）:

1. 環境変数 `ORCA_CLI_COMMAND` が設定されていればその値
2. Linux で Orca 管理外のターミナルなら `orca-ide`（素の `orca` は GNOME スクリーンリーダーに解決され、実行すると読み上げが起動してしまう）
3. それ以外は `orca`

Orca が起動していなければ `ORCA open --json` で起動し、`ORCA status --json` で確認する。

## 最新仕様の確認（このスキルの要）

automations のフラグは追加・変更が速い。コマンドを組み立てる前に、必ずインストール済み CLI に現行仕様を問い合わせる:

```text
ORCA automations create --help
ORCA agent-context --json    # 全コマンドの機械可読スキーマ（usage・flags・examples・notes）
```

本スキルの例と CLI の出力が食い違う場合は、CLI の出力を正とする。

## 代表コマンド

```text
ORCA automations list --json
ORCA automations show <automationId> --json
ORCA automations create --name "Daily review" --trigger daily --time 09:00 --prompt "Review open changes" --provider codex --repo id:<repoId> --json
ORCA automations create --name "Weekday triage" --trigger "0 9 * * 1-5" --prompt "Triage issues" --provider claude --repo path:/abs/repo --disabled --json
ORCA automations create --name "Inbox digest" --trigger hourly --prompt "Summarize unread mail" --provider codex --workspace active --reuse-session --json
ORCA automations edit <automationId> --trigger weekdays --time 09:30 --json
ORCA automations run <automationId> --json        # 今すぐ実行（動作確認に使う）
ORCA automations runs --id <automationId> --json  # 実行履歴
ORCA automations remove <automationId> --json
```

## Gotchas

- トリガーは `hourly` / `daily` / `weekdays` / `weekly` のプリセット、5フィールド cron、RRULE を受け付ける。`--time <HH:MM>` は `daily` / `weekdays` / `weekly` とだけ、`--day <0-6>`（日曜=0）は `weekly` とだけ組み合わせる
- `--repo <selector>`（実行ごとに新規 worktree を作成）と `--workspace <selector>`（既存 worktree で実行）は排他。`--reuse-session` は既存 workspace の automation でのみ有効で、前回セッションが消えていれば新規セッションにフォールバックする
- `--precheck <command>` は実行前チェック。exit code 0 なら続行、それ以外なら skipped として記録される（例: レビュー対象の PR が無ければスキップする）
- 新規作成時は「`--disabled` を付けて作成 → `automations run <id>` で即時実行 → `runs` で結果確認 → 問題なければ `edit <id> --enabled`」の順で動作確認してから有効化する
- エージェントからの呼び出しには常に `--json` を付ける

## 自動化以外の Orca 操作

worktree・ターミナル・組み込みブラウザ操作など自動化以外の Orca 操作が必要になったら、`ORCA agent-context --json` でコマンド表面を確認する（公式 `orca-cli` スキルがインストール済みの環境ではそちらを使う）。
