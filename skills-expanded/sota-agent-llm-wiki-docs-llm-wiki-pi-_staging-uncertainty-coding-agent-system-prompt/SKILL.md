# uncertainty: subsys.coding-agent.system-prompt

本轮 L2 复核 `subsys.coding-agent.system-prompt` 未新增 `[U]`。

降级为 `[I]` 的点:

- `BuildSystemPromptOptions` 只消费已准备好的资源、不负责磁盘加载:由 options 字段与 `AgentSession._rebuildSystemPrompt`/`DefaultResourceLoader` 调用关系推出。
- bash-only file operation guideline 是能力替代 guideline、不是 tool registry 注册逻辑:由 `buildSystemPrompt` 中 guideline 条件推出。
- CLI prompt 参数“具体内容仍由 resource loader 解析后交给 builder”:由 `parseArgs`、`DefaultResourceLoader` 和 `AgentSession._rebuildSystemPrompt` 串联推出。
- `pi-agent-core` 消费 prompt、`pi-coding-agent` 负责产品 prompt 内容:由 `AgentHarness` systemPrompt 输入与 coding-agent builder 的跨包关系推出。
- prompt templates 展开 user prompt text,不等同于 system prompt append source:由 `expandPromptTemplate` 调用位置推出。

L2 复核中修正了一批落在注释行或承载不足行的 `[E]` 引用,并补强 `DefaultResourceLoader` prompt source / append source 解析的代码行。没有需要上卷到 `reference/uncertainty.md` 的 unknown。节点已置 `status: verified`。
