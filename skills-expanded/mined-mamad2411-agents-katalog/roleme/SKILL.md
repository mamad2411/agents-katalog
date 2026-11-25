---
name: roleme
description: Use when the user wants to initialize, switch, inspect, optimize, export, or diagnose a role bundle with /roleMe.
---

# roleMe

`/roleMe` 无参调用时，应先列出现有角色供用户选择加载；如果用户不想加载已有角色，就先问他要创建的角色名，再进入初始化流程。

详细使用说明见 `references/usage.md`。

命令面：

- `/roleMe`
- `/roleMe <角色名>`
- `/roleMe list`
- `/roleMe current`
- `/roleMe optimize [角色名]`
- `/roleMe export [角色名]`
- `/roleMe doctor [角色名]`

运行时原则：

- `roleMe` 管理的是用户角色上下文，不是助手人格切换。
- 未被结构化写入角色包的上下文，不应假定模型已经知道；稳定信息应落到 `persona/`、`memory/`、`brain/`、`projects/` 中可检索的位置。
- 常驻层与渐进层的边界由角色包内的 `AGENT.md` 决定。
- 常驻层应保持最小且稳定；细节、专题知识与项目上下文优先按需展开，而不是堆进单个总说明。
- 记忆写回优先遵循 `AGENT.md` 中的策略和 `memory/` 结构。
- 主题知识与项目上下文通过 `tools/context_router.py` 做渐进式发现，不应一次性全量加载。
- 归档内容优先追求对智能体可读：结构清晰、边界明确、可检索、可增量更新，而不是只写成长段自由叙述。
- 初始化访谈可以是动态的：问题由模型根据当前已知信息和信息缺口来决定，但最终仍要落到稳定的 `persona/`、`memory/`、`brain/`、`projects/` 结构。
- 槽位只是归档目标，不是固定提问顺序；模型应按当前情景决定下一问，而不是机械执行问卷。
- 初始化访谈应更像采访而不是填表：用户没有表达出来的信息可以先不记录，不要为了补全而反复追问同一槽位。
- 槽位提示只是采访锚点，不是最终逐字发问文案；真正问用户前，应结合当前上下文先润色成自然口语。
- 当用户第一次无参执行 `/roleMe` 时，应先列出现有角色，让用户选择加载；如果用户选择创建新角色，应先询问角色名，再开始采访。
- 语言偏好应在初始化时显式采访一次；如果用户暂时没有给出明确偏好，可以留空并在后续使用中慢慢积累。
- 初始化成功后，应明确提醒用户重新调用 `/roleMe <角色名>`，以便把新写入的角色包加载进后续会话使用的快照。
- 当角色已加载后，如果用户说“帮我总结这个项目的工作方式”或“帮我总结成通用的工作方式”，应直接把结果归档到当前角色，而不是只返回普通总结文本。
- 当角色已加载后，若用户内容明显属于学习沉淀、项目复盘、方法论提炼、稳定偏好或长期协作规则，助手应主动进行归档，而不必等待用户显式下达“归档”指令。
- 归档前应先提炼原始内容，再判断归档位置，而不是把原始对话直接整段落盘。
- 默认先写入，再用一句短回执告知用户归档结果。
- 判断不够确定时，优先写入 `memory/episodes/` 或项目记忆，不轻易提升到 `memory/USER.md` 与 `memory/MEMORY.md`。
- 项目级 workflow 写入 `projects/<project-slug>/workflow.md`、`context.md`、`memory.md`；通用 workflow 写入 `brain/topics/general-workflow.md`，并将稳定规则提升到 `memory/USER.md` 与 `memory/MEMORY.md`。
- 当前角色以 `ROLEME_HOME/.current-role.json` 为准；自然语言归档只能写当前角色。
- 如果归档提升了 resident 规则或摘要，应提醒用户重新执行 `/roleMe <角色名>` 才会刷新当前会话底座。
- `optimize` 与 `doctor` 应优先发现和修复角色包的熵增问题，例如重复记忆、索引失效、resident/on-demand 边界漂移。
- 只有确定性的文件操作才调用 `tools/role_ops.py`、`tools/memory.py`、`tools/context_router.py`。
- 打包产物中不包含开发仓库的 `scripts/`。
