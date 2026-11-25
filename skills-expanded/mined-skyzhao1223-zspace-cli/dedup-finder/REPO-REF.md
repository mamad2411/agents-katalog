# Repo Ref
- source: https://github.com/skyzhao1223/zspace-cli (path: skills/dedup-finder/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: Use when 用户想找 NAS 上的重复文件 — "哪些文件重复了"、"帮我找重复照片/视频/文档"、"磁盘被重复文件占满了"、"下载了好几次同一个东西"、"精确去重不要误删"。只读扫描用三级指纹(size → 头部64KB → 全量 sha1)做内容级精确去重,零误报;每组给出「保留哪个/删哪个」的启发式建议,LLM 出删除计划,用户确认后由 Agent 执行(优先 mv 到隔离目录而非直接
