# Repo Ref
- source: https://github.com/zhaoxinghua09-cell/agent-skills (path: skills/env-var-audit/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 环境变量审计器 — 代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
