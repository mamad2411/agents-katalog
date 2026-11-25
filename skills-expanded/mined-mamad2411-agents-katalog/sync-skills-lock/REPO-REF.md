# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-fandhe-ai-agent-cli-skills/sync-skills-lock/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: ルート直下の `skills-lock.json` の `computedHash` を upstream リポジトリの最新状態と照合して更新する。`source` が `Fandhe-AI/<repo>` に完全一致しないエントリは clone せず skip (安全弁)。submodule 配下の `skills-lock.json` は触らない。contribute-skill のマージ後や
