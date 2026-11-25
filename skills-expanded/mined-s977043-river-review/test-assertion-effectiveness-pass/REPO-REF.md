# Repo Ref
- source: https://github.com/s977043/river-review (path: plugin-dist/river-review/skills/downstream/test-assertion-effectiveness/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: テストは存在するがアサーションが実質何も検証しておらず、実装が壊れても落ちない（常に PASS する）構造を diff-time で検出する。Check 1 missing assertion（テスト本体にアサーションが無い）、Check 2 tautological assertion（定数同士・入力自身・mock の戻り値自身を assert し SUT に依存しない）、Check 3 non
