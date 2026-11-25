---
name: e2e-live-docker
description: 実 Claude API + Docker サンドボックスを叩く docker カテゴリの総合テストを実行する。`DISABLE_SANDBOX` を unset した状態で `yarn dev` が起動済みであることが前提（サンドボックス off だと全 test が `test.skip` で抜ける）。
---

## 前提

- `yarn dev` を別ターミナルで起動済み（`http://localhost:5173` が応答する）
- **`DISABLE_SANDBOX` を unset** で起動していること。`/api/sandbox` の payload は enabled 時 `{ sshAgent, mounts }`、 disabled 時 空オブジェクト `{}` を返す（`server/api/sandboxStatus.ts` 参照）。spec 側の `getSandboxStatus(page)` helper はこの `{}` を `null` に正規化するので、 sandbox off だと spec の gate が `null === null` で hit して全 test が `test.skip` で抜ける
- Docker daemon が起動しており、 `mulmoclaude-sandbox` image が build 済（`yarn dev` 初回起動時に自動 build）
- Claude 認証済み（`claude login` 済み or `ANTHROPIC_API_KEY` 設定済み）
- 各シナリオ固有の前提（unmet なら spec が `test.skip` で抜ける、 ログにスキップ理由が出る）:
  - **L-23**: `X_BEARER_TOKEN` が host の env に設定されていること
  - **L-28**: `SANDBOX_MOUNT_CONFIGS=gh` または `SANDBOX_SSH_AGENT_FORWARD=1` のいずれかが設定されていること

## 実行

```bash
yarn test:e2e:live:docker
```

## デバッグ時

```bash
HEADED=1 yarn test:e2e:live:docker
```

## カバーするシナリオ

- **L-23**: X MCP tools (`readXPost` / `searchX`) が Docker サンドボックス on 状態で host の `X_BEARER_TOKEN` を見て enabled になる（B-01 回帰）
- **L-26**: サンドボックス on 状態で開始したセッションが reload で「No conversation found」 を出さず履歴復元される（B-04 回帰、 in-container workspace path 整合）
- **L-28**: agent が container 内で `gh auth status` を Bash 実行し、 host の gh credential が container に届いていることを確認する（B-06 回帰）

## 結果の確認

- 詳細: `playwright-report-live/docker/index.html`（このカテゴリ専用サブディレクトリに出力されるので、 親 `/e2e-live` の総合レポートは上書きされない）
- 動画リプレイ: `npx playwright show-trace test-results-live/docker/<spec>/trace.zip`

## fake-echo / CI matrix について

このカテゴリは fake-echo backend (`MULMOCLAUDE_FAKE_AGENT=1`) で再現できない（実 Docker サンドボックス起動が必要）ので、 `.github/workflows/e2e_live_no_llm.yaml` の matrix には **意図的に登録していない**。 同等の理由で各 test も `E2E_LIVE_NO_LLM=1` が立っていると skip する。 routine な CI 検証ではなく **開発者が手元で Docker on モードを切り替えて回す** ことを想定したスイート。

## Docker on/off の検証も必要な場合

このカテゴリは Docker on 必須で、 off では全 test が `test.skip` するだけ。 「両モード巡回」 を取りたい時は 1) 現在モード (`/api/sandbox` の payload で確認) で `yarn test:e2e:live:docker` を回す、 2) もう一方のモードに dev を再起動して `yarn test:e2e:live` を回して他カテゴリの両モード健全性を見る、 の併用が想定。
