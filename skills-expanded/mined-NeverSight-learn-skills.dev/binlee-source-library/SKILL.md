---
name: binlee-source-library
description: 检索、引用、检查并刷新来自 drli.beaucare.org 的李滨医美文章本地语料。适用于研究语料覆盖的问题、定位原文、检查文章来源或时间，或希望减少重复访问源站时。
---

# Binlee 医美语料库

把本地语料当作可检索、可引用的原始文章集合，而不是当前临床、法律或市场数据的权威库。

## 默认低交互模式

- 用户给出主题时，直接检索并返回最相关的文章，不先询问关键词、分类或输出格式。
- 默认返回少量高相关结果、文章摘要、日期和原文链接；需要完整记录时再展开。
- 查询词不理想时，自动尝试同义词或相邻主题，并说明采用了什么检索假设。
- 刷新语料只有在用户明确要求时执行；明确要求后不再重复确认，失败则保留旧语料并报告原因。

## 检索

1. 读取 [references/corpus-guide.md](references/corpus-guide.md) 和 [references/evidence-policy.md](references/evidence-policy.md)。
2. 用 `node scripts/search-corpus.mjs --query "关键词"` 搜索标题、FAQ、摘要、分类和正文；多个关键词用空格分隔，并根据 `score`、`matchedTerms` 和 `snippet` 判断相关性。
3. 用 `node scripts/search-corpus.mjs --id "文章-id"` 读取选中的完整记录。
4. 每条重要的语料结论都要附文章标题、发布日期和原文链接。

不要一次性加载 `references/articles.json`。先检索，再只打开相关记录。

## 刷新

只有在确实需要更新语料时，才运行 `bash scripts/refresh-corpus.sh --check`。检查模式会下载当前应用 bundle，静态解析文章并报告新增、删除和修改，但不写入文件。

检查结果合理后，才运行 `bash scripts/refresh-corpus.sh --apply`。应用模式会在临时目录生成并校验语料、索引和 manifest，再事务式替换现有产物；下载或提取失败时保留旧语料并报告原因。

## 输出纪律

把源自文章的内容标为：**文章中的观点**、**跨文归纳**或**需另行核验的当前事实**。始终把作者的主张和你的结论分开。
