# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/r/release-gate-audit/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 发布前放行门禁：判定一个产物能否公开发布。与常规密钥扫描器的根本区别是判定对象——它以 git 已追踪内容 + 全部提交历史构成的「公开面」为准，而不是 ls 看到的工作目录，因此既不会把本地文件误报成泄露，也不会漏掉当前已删除但仍存在于旧 commit 中的凭证。四类威胁分离处置（凭证需吊销 / 雇主内部信息需泛化 / PII 兼可移植性缺陷 / 本地专属产物需停止追踪），并提供整改闭环的机器验
