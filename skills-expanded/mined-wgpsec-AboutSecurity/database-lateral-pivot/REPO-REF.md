# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/lateral/database-lateral-pivot/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: 数据库横向移动与跨库攻击。当已获取一个数据库权限（PostgreSQL/MySQL/MSSQL）需要横向到其他数据库或内网服务时使用。覆盖 PostgreSQL dblink 跨库连接、MSSQL Linked Server 横向、MySQL 联邦引擎跨库、数据库→SSRF→内网探测。当目标网络隔离但数据库可通信时（数据库通常有比应用服务器更宽松的网络策略），这是突破隔离的关键路径。发现任何数据库
