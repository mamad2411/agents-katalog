---
name: local-dev-ops
description: ローカル開発環境の起動、停止、再起動、localhost/ポート確認、Docker Compose、Makefile、`.next` キャッシュ、DB seed、画面/API疎通確認を扱う。ユーザーが「ローカル開発環境を起動して」「localhostを確認」「コンテナを再起動」と依頼したときに使う。Cloud Run/GCP 環境の変更は `gcp-cloud-run-ops` を使う。
allowed-tools: Read Write Edit Glob Grep Bash(find *) Bash(wc *) Bash(mkdir *)
---

# local-dev-ops

この skill の詳細手順は `~/.agents/references/local-dev-ops.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
