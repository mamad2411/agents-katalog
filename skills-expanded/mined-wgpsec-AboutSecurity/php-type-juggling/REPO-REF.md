# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/exploit/web-method/php-type-juggling/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: PHP 类型杂耍（Type Juggling）和 Magic Hash 攻击方法论。当目标是 PHP 应用且存在密码比较、哈希校验、认证逻辑时使用。当看到 PHP `==` 松散比较、MD5/SHA1 哈希校验、strcmp 比较、JSON 输入处理、is_numeric 检查时必须使用。当错误登录泄露了输入的 MD5 哈希值时，这是 Magic Hash 的强信号，立即使用。CTF/渗透中 PH
