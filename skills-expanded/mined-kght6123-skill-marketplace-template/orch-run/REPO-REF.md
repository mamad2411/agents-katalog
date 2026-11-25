# Repo Ref
- source: https://github.com/kght6123/skill-marketplace-template (path: plugins/ai-dev-orchestration/skills/orch-run/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: AI開発オーケストレーションの1周（tick / build）をマネージャとして回す司令塔スキル。ユーザーが「AI開発を1周進めて」「orchのtickを回して」「buildを実行して」「今やることを教えて」「orchを回して」「次のタスクは？」などと言ったら使う。自分では実装せず、orch CLI で対象を決め、実装は各リポジトリの worktree でワーカーを起動して任せる。state.js
