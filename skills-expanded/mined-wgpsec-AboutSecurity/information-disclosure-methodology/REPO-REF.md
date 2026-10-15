# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/exploit/web-method/information-disclosure-methodology/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: Web 应用敏感信息泄露检测与利用。当发现 .git/.svn 目录、备份文件路径(.bak/.zip/.tar.gz)、.env 配置文件、Swagger/OpenAPI 文档、debug 页面等信息泄露点时使用。也适用于发现源码泄露后的深入利用：git 历史审计（git log -p -S 搜索已删除的密码和 flag）、svn wc.db 文件列表提取、.DS_Store 目录枚举。优先于漏
