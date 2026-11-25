---
name: handoff-prompt
description: 次の Codex/Claude セッションが目的、文脈、判断基準、作業状態を理解して自律再開できる handoff prompt を生成する。現在の作業ディレクトリを検査し、repo 全体像、ユーザーの実現したいこと、これまでの対話と実施内容、git/PR/検証状態、次の指示、注意点、期待する動きを次セッションへ貼れる Markdown として出力する。「引き継ぎ」「handoff」「次セッションに渡す」「引き継ぎ用に作業まとめて」などで使う。設定へ恒久的な学びを反映する場合は session-retrospective、新規 skill 作成は create-skill を使う。
argument-hint: [current-session | branch | pr-number]
allowed-tools: Read Write Edit Glob Grep Bash(git *) Bash(gh *) Bash(docker *) Bash(find *) Bash(rg *) Bash(head *) Bash(ls *) Bash(test *) Bash(pwd) Bash(wc *)
---

# handoff-prompt

この skill の詳細手順は `~/.agents/references/handoff-prompt.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
