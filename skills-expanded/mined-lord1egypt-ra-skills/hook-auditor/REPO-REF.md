# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/h/hook-auditor/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 审计并清理 Claude Code 中「你不知道自己装了」的 hook。安装 skill 或 plugin 会自带 hook，它们安装即常驻、每轮对话都跑、持续烧 token 并可能拦截或改写工具调用——即使你从未调用过那个 skill。本 skill 枚举全部真正生效的 hook、标注来源与可信度、量化每轮成本，并在你确认后清理。触发场景：用户说「清理」「提速」「省 token」「变慢了」「to
