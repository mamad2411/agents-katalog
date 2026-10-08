# Repo Ref
- source: https://github.com/fandhe-ai/agent-cli-skills (path: skills/create-commit/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: Conventional Commits 形式で git コミットを作成する。staged 差分から type/scope を推定し、breaking change やシークレット混入 (.env 等) を検出。pre-commit フックを必ず通す (`--no-verify` 不可)。「コミットして」「git commit」「変更を記録して」などで使用。
