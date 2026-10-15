# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/exploit/web-method/ldap-injection/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: LDAP 注入检测与利用。当目标有 LDAP 认证入口（企业登录/SSO/统一认证）、发现 389/636/3268/3269 端口、URL 参数中出现 uid/cn/ou/dc 等 LDAP 属性名、或后端使用 LDAP 进行用户查询时使用。LDAP 注入与 SQL 注入思路类似但语法不同——通过注入 LDAP 搜索过滤器操作符来绕过认证或提取数据。在域环境和企业内网中常见，与 AD 域攻击配合
