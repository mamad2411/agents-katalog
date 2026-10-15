# Repo Ref
- source: https://github.com/Yrzhe/claude-skills (path: plugins/akshare-a-shares/skills/akshare-a-shares/SKILL.md, branch: main)
- mined: 2026-10-15
- desc: 针对中国A股的行情与数据查询（基于本地 akshare 源代码与API映射）。当用户请求获取A股实时行情、历史K线（日/周/月）、分钟级分时（1/5/15/30/60）、复权数据（前复权/后复权）、股东户数（含详情）、以及巨潮资讯公告披露结果时使用本Skill。默认优先使用东方财富(EM)接口；如用户指定新浪(Sina)来源或需要特定接口，则按映射调用对应函数。可使用内置脚本输出CSV/JSON，
