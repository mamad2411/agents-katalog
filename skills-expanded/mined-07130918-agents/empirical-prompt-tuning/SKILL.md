---
name: empirical-prompt-tuning
description: agent 向けテキスト指示(skill / slash command / task プロンプト / AGENTS.md 節 / コード生成プロンプト)を、バイアスを排した実行者に動かしてもらい、両面(実行者の自己申告 + 指示側メトリクス)で評価して反復改善する手法。改善が頭打ちになるまで回す。プロンプトや skill を新規作成・大幅改訂した直後、またはエージェントの挙動が期待通りにならない原因を指示側の曖昧さに求めたいときに使う。
---

# empirical-prompt-tuning

この skill の詳細手順は `~/.agents/references/empirical-prompt-tuning.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
