---
name: improve-agent-md
description: 当用户要求改进/瘦身 agent 指令文件（AGENTS.md、CLAUDE.md、QWEN.md、SKILL.md 等）时使用：用 <important if> 条件块标记条件相关指令，对抗"相关性过滤"导致的指令被无视
disable-model-invocation: true
---

# Improve Agent 指令文件

人工手动触发：重写 agent 指令文件（AGENTS.md / CLAUDE.md / QWEN.md / 项目说明 / SKILL.md），提高指令遵循率。不是模型自动调用的常规技能。

## 核心问题

多数 agent 运行时会在每轮会话给指令文件附加一条系统提示：

> "this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task."

这意味着 agent 会自行忽略它判定为"与当前任务无关"的内容。文件越长、与当前任务无关的段落越多，agent 越可能**整体降权**——连真正要紧的硬规则一起忽略。

## 解法：`<important if="触发条件">` 块

把**条件相关**的段落包进 `<important if="条件">` XML 块，给每段指令一个明确的相关性信号，穿过"可能相关可能不相关"的模糊框架，让 agent 只对命中的条件上权重。

这是 Claude Code 自身系统提示在用的 XML 标签模式；对所有注入"相关性过滤"提示的 agent（ZCode / Qwen Code / Claude Code 等）同样有效。

## 原则

### 1. 基础上下文裸放，领域指令包块

不是所有内容都要包。几乎每个任务都相关的（项目定位、目录结构、技术栈）保持纯 markdown 放在文件顶部——那是 agent 的入门必读。

只在特定任务才相关的（测试约定、构建陷阱、发布流程、某工具的使用规则）才包 `<important if>`。经验法则：**90% 以上任务相关 → 裸放；特定工作才相关 → 包块**。

### 2. 条件必须窄而具体

坏——过宽的条件等于没条件：

```xml
<important if="你在写或修改任何代码">
- 使用绝对导入
- 使用函数式组件
</important>
```

好——每条规则有自己窄的触发点：

```xml
<important if="你在新增或修改 import">
- 使用 @/ 绝对导入（路径别名见 tsconfig.json）
- 路由文件外避免 default export
</important>

<important if="你在 Windows 上执行 go build">
- 临时目录指向项目内普通目录（如 `GOTMPDIR=<项目本地目录>/.gtmp`），防杀软锁 %TEMP% 链接产物
- 判断真实结果看退出码/产物文件，不看改写后的 "Success" 输出
</important>

<important if="需要架构概览/复杂度排行/commit 影响半径">
- 用 cbm skill（codegraph 无架构视图、impact 只能符号驱动）
</important>
```

### 3. 保持短小，少拆文件

一切内联、按条件加权——agent 全都看得见，但只对命中条件的上注意力。除非内容极长极复杂，不要为省上下文拆成需要额外工具调用才能发现的子文件。

### 4. Less is more

模型能可靠遵循的指令总量有限，每一条都在挤占预算。删：

- **linter / formatter / pre-commit 能强制的**（写进配置，不写进提示词）
- **agent 从现有代码模式能学到的**（代码库一致的模式，几次搜索就会跟随）
- **代码片段**（会过时，改用文件路径引用，如"模式见 `src/utils/example.ts`"）
- 与其他指令重复或矛盾的

## 工作流程

1. **定位文件**：用户指定了文件就用它；否则按 `AGENTS.md` → `CLAUDE.md` → `QWEN.md` → 项目内 `SKILL.md` 顺序探测，多份存在时先问用户改哪份
2. **通读分类**：逐段判定——基础上下文（裸放）/ 条件相关（包块，提炼窄触发条件）/ 可删（linter 可强制、可从代码推断、重复过时）
3. **重写**：输出完整新文件；`<important if>` 条件用一句话描述触发场景，宁窄勿宽
4. **收尾报告**：向用户列出 ① 包块段落及各自触发条件 ② 删除段落及删除理由，**删除有争议的内容前先问**，不要静默删
