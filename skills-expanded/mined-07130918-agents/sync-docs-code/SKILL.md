---
name: sync-docs-code
description: |
  PR前に変更差分から実装上の契約とリポジトリ内ドキュメントを照合し、必要な文書更新と検証まで行う。
  Use when: before submitting a PR for feature, bug fix, database, API, UI, configuration, or operational changes; or when asked to "ドキュメントを実装に同期", "README/docsも更新", or "docsの更新漏れを確認".
  Does not trigger on: generic PR creation requests by themselves (create-pr invokes this gate), full-repository audit/report-only requests (defer to docs-code-consistency-audit), or documentation-only copyediting unrelated to implementation.
---

# sync-docs-code

この skill の詳細手順は `~/.agents/references/sync-docs-code.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
