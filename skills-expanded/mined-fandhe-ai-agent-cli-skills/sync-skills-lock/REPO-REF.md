# Repo Ref
- source: https://github.com/fandhe-ai/agent-cli-skills (path: skills/sync-skills-lock/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: ルート直下の `skills-lock.json` の `computedHash` を upstream リポジトリの最新状態と照合して更新する。`source` が `Fandhe-AI/<repo>` に完全一致しないエントリは clone せず skip (安全弁)。submodule 配下の `skills-lock.json` は触らない。contribute-skill のマージ後や
