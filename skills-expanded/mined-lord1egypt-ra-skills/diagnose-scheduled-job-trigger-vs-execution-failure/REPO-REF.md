# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/d/diagnose-scheduled-job-trigger-vs-execution-failure/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 用于排查“定时任务没执行”这类问题，并区分到底是未触发、已触发但执行失败，还是运行环境/授权失效导致的假象。遇到 cron 异常、任务未跑、自动任务失灵、网关重启后要验证恢复、怀疑是模型导致任务失败、需要查看日志作证、需要给出证据口径、要确认 `deactivated_workspace` / OAuth token 失效 / timeout 是否为根因时，都应触发本技能。也适用于“任务其实有 r
