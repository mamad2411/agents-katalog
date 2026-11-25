# Repo Ref
- source: https://github.com/apokamo/kaji (path: .claude/skills/watch-triage/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: kaji watch が検知した停止 event（aborted / pane_idle / log_stall）の原因を読み、自動復旧の一覧の 5 種類は承認なしで戻し、それ以外は Issue に報告して保守者に回す判断用 skill。kaji watch が Herdr の watch-triage-<issue> タブで自動起動する。一覧の外の復旧は保守者が承認したものだけを実行する。
