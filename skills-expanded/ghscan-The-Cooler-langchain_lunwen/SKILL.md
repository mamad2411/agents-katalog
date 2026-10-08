---
name: chapter-spec
description: 撰写智科章节时使用。按结构、段落要求、字数、细则逐项落地。
---

# chapter-spec

## Instructions

1. **优先**调用工具 `read_chapter_spec(章节标题)`；**不要**用 `ls` 盲扫目录。
2. 若必须用 `read_file`，虚拟路径：`/config/<当前模板包名>/chapters/<与标题匹配的>.md`（本包为 `智科`，与系统提示中模板包名一致）。
3. 按顺序执行：`结构 -> 段落要求 -> 字数 -> 细则`。
4. 占位词（如 xx、模块1）必须替换成真实名称，禁止原样写入。
5. 不得跨章节跳写。
