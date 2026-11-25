---
name: wiki-reader
description: 用于从当前用户 Wiki 中读取知识并回答问题。适用于用户询问“我之前负责什么”“我做过哪些项目”“我了解过哪些工具或模块”等需要基于当前用户知识空间回答的问题。回答时优先读取 knowledge/wiki/index.md、knowledge/wiki/pages/ 和 knowledge/wiki/entities/，如果 Wiki 中没有相关信息，必须明确说明，不允许猜测。
---

# Wiki Reader

读取当前用户 Wiki 中的知识并回答问题。

## 读取顺序

1. 先使用文件工具查看 `knowledge/wiki/` 下有哪些文件和目录。
2. 优先读取 `knowledge/wiki/index.md`，了解当前 Wiki 中有哪些页面和实体。
3. 再根据问题主动读取 `knowledge/wiki/pages/` 下最相关的页面。
4. 必要时读取 `knowledge/wiki/entities/` 下的实体文件，用于确认具体对象。
5. 如果当前问题属于某个具体项目，还应主动查看 `knowledge/project-public/<projectId>/wiki/` 下的项目公共 Wiki。
6. 如果以上内容仍然无法支持回答，明确说明当前用户知识空间中没有相关信息。

## 回答规则

1. 只能依据当前用户知识空间中的内容回答。
2. 不允许猜测、补全或编造知识空间之外的事实。
3. 如果信息不足，直接说明“当前你的知识空间里还没有沉淀相关信息”。
4. 如果多个页面内容相关，优先给出一致结论；如发现冲突，指出存在冲突，不自行强行统一。
5. 回答时优先总结结论，不必逐字复述 Wiki 原文。
6. 回答前应尽量先用文件工具自行查找和读取相关 Wiki 文件，而不是假设文件内容已经提供。
