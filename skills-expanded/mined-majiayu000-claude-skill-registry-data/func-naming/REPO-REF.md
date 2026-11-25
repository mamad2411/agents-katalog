# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: security/func-naming/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 已知地址判断函数用途/算法（无符号函数命名）：先查 .dynsym，再取字符串/魔数/成对调用特征，最后回填命名。SO 层深挖的单步能力，入口仍在 frida-mobile-security；恢复结构体用 rev-struct，判漏洞用 native-audit。
