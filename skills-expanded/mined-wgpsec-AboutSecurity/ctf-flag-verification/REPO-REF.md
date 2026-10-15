# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/ctf/ctf-flag-verification/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: CTF/靶场 Flag 强制验证流程。当通过**任何方式**发现疑似 flag 字符串（含 flag{、FLAG{、ctf{ 等格式）时**必须立即**使用此 skill 验证，不要直接提交。防止因字符截断、编码错误、HTML 实体、base64 不完整解码、hex 截断等原因导致提交错误 flag。即使 flag 看起来完整，也可能存在隐藏字符或编码问题。覆盖 SQL 注入分段提取、命令执行输出
