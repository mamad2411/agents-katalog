# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-one-step-beh1nd-skillbank/findscripter-everything-skills-content-hash-cache-pattern-02/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当为高成本、可重复的文件处理（PDF 解析、OCR、文本/图像抽取）加缓存、需要 --cache/--no-cache 开关、且不想改动现有纯函数时使用；用文件内容的 SHA-256 作缓存键、按 {hash}.json 落盘、以独立服务层包裹纯处理函数，产出路径无关、内容变即自动失效、损坏即视为未命中的缓存方案；不适用于必须实时最新的数据、超大缓存条目（改用流式）、或结果还依赖内容之外参数（如抽
