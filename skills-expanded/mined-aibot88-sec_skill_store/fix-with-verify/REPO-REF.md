# Repo Ref
- source: https://github.com/aibot88/sec_skill_store (path: skills/claudskills/fix-with-verify/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: バグ修正→コンパイル確認→回帰テスト→失敗時 revert の安全修正パイプライン。修正が新たなバグを生まないことを機械的に保証する。USE WHEN 単発バグ修正、影響範囲が見えにくい変更、リファクタの安全確認。SKIP 大規模機能追加は impl-orchestrator、セキュリティ Finding 一括修正は robust-fix、仕様整合性回復は spec-fix を使うこと。
