# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/ctf/ctf-source-audit/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: CTF 挑战中的源码审计方法。当发现 .git 目录、.bak/.zip 备份、/proc/self/environ 泄露源码时使用。与真实代码审计不同——CTF 源码中的漏洞是故意设置的，通常只有 1-2 个关键点。先找危险函数（sink），再追溯输入（source）到该函数的路径。覆盖 PHP/Python/Node.js/Java 四种语言的危险函数和漏洞模式"
