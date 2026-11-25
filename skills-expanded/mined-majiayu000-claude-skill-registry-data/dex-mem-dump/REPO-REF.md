# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: platform/dex-mem-dump/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 运行时 DEX 内存 dump / 脱壳（root 直读 /proc/<pid>/mem，不注入、不 ptrace）：常规解包拿不到、抽取壳未回填、或目标查 TracerPid 时用。流程：推工具 → 跑 → 拉回 → 清理；分诊与排障见 references/unpacking.md。
