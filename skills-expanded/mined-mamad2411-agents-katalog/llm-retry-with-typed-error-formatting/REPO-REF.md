# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-kjuhwa-skills-hub/llm-retry-with-typed-error-formatting/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Wrap LLM calls in a 3-attempt exponential-backoff retry that re-raises auth errors immediately (don't retry 401/403), and on final failure formats a user-actionable message based on error type and HTT
