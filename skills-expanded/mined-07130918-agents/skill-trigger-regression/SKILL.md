---
name: skill-trigger-regression
description: skill の発火品質を回帰テストする。新規 skill 作成後や既存 skill の description 変更後に、発火すべき例・発火すべきでない例・既存 skill との競合を検査し、create-skill の検証工程と組み合わせて使う。
argument-hint: skill-name | changed-files | all
allowed-tools: Read Write Edit Glob Grep Bash(find *) Bash(wc *)
---

# skill-trigger-regression

この skill の詳細手順は `~/.agents/references/skill-trigger-regression.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
