---
name: agent-baton
description: 多角色 AI 团队接力协作框架（BA / Arch / Dev / TechLead），通过 Markdown 文档在角色之间传递上下文，适用于需要结构化协作的中大型项目。当用户明确说"用 AgentBaton 初始化项目"/"启动 AgentBaton 框架"，或提到任一角色名（"BA 角色"/"Arch 角色"/"Dev 角色"/"TechLead 角色"/"TechLead Review"），或当前项目根目录已存在 `config/roles/` 或 `config/TEAM_GUIDE.md` 时，使用本 skill。不要用于：简单代码修改、bug 修复、单文件改动、代码探索、纯重构、与多角色协作无关的常规开发任务。
---

# AgentBaton — 多角色 AI 接力协作框架

本 skill 把"BA → Arch → Dev → TechLead"的人机混合团队工作流封装为可触发的协作框架。核心机制：**4 个角色通过 Markdown 文档接力，状态沉淀在项目内 `config/` 和 `docs/` 目录，跨会话/跨 Agent/跨模型可断点续接**。

---

## 第一步：自检触发条件

在做任何动作之前，先判断当前到底属于哪种场景：

1. **场景 A — 初始化新项目**：用户明确说"用 AgentBaton 初始化新项目"或类似表述，且当前目录**没有** `config/roles/` 和 `config/TEAM_GUIDE.md`。
2. **场景 B — 初始化二期接入项目**：用户明确说"用 AgentBaton 初始化二期接入项目"，且当前目录**没有** `config/roles/`。
3. **场景 C — 已有 AgentBaton 项目中启动角色**：当前目录已有 `config/roles/` 和 `config/TEAM_GUIDE.md`，用户提到任一角色名。
4. **场景 D — 不适用**：用户没明确说初始化、没有提到角色，且当前目录不是 AgentBaton 项目。**立即停止本 skill**，告知用户"当前不符合 AgentBaton 触发条件，将按普通方式回答"，然后让对话回到主流程。

---

## 场景 A：初始化新项目（全新开发）

执行以下步骤：

1. **拷贝模板到当前项目**。Skill 模板位置：`${CLAUDE_PLUGIN_ROOT:-~/.claude/skills/agent-baton}/assets/templates/`。要拷贝的内容：
   - `CLAUDE.md` → 项目根
   - `config/TEAM_GUIDE.md`、`config/PROJECT_STATUS.md`、`config/TECH_STATUS.md` → `config/`
   - `config/roles/{BA,ARCH,DEV,TECHLEAD}.md` → `config/roles/`
   - `docs/{INIT_REQ,PRD,ARCH,TASKS}.md` → `docs/`
   - `docs/prototypes/.gitkeep` → `docs/prototypes/`
   - 不拷贝 `docs/phase1/`（仅二期接入模式需要）

   定位 skill 路径，再 `cp` 各文件。注意 `find` 必须用 `-L` 才能跟随软链：

   ```bash
   # 优先用环境变量；否则按常见路径搜索；最后回退到 find -L
   SKILL_DIR="${CLAUDE_PLUGIN_ROOT:-}"
   [ -z "$SKILL_DIR" ] && [ -d ~/.claude/skills/agent-baton ] && SKILL_DIR=~/.claude/skills/agent-baton
   [ -z "$SKILL_DIR" ] && SKILL_DIR=$(find -L ~/.claude/skills ~/.claude/plugins -maxdepth 4 -name "agent-baton" 2>/dev/null | head -1)
   [ -z "$SKILL_DIR" ] && { echo "未找到 AgentBaton skill 安装目录"; exit 1; }

   mkdir -p config/roles docs/prototypes
   cp "$SKILL_DIR/assets/templates/CLAUDE.md" ./CLAUDE.md
   cp "$SKILL_DIR/assets/templates/config/"{TEAM_GUIDE,PROJECT_STATUS,TECH_STATUS}.md config/
   cp "$SKILL_DIR/assets/templates/config/roles/"{BA,ARCH,DEV,TECHLEAD}.md config/roles/
   cp "$SKILL_DIR/assets/templates/docs/"{INIT_REQ,PRD,ARCH,TASKS}.md docs/
   touch docs/prototypes/.gitkeep
   ```

2. **写一份基础 `.gitignore`**（若不存在）：覆盖 macOS / IDE / 构建产物 / 密钥。

3. **引导用户填写**：告诉用户接下来要做的事：
   - 编辑 `CLAUDE.md`：填写技术栈、开发规范、Git 团队配置（"项目阶段"字段保持默认"全新开发"）
   - 在项目目录执行 `git init && git add -A && git commit -m "init: AgentBaton 项目初始化"`
   - 让产品经理填写 `docs/INIT_REQ.md`

4. **不要继续做需求分析、不要启动 BA 角色**。初始化完成后停下来等用户。

---

## 场景 B：初始化二期接入项目

与场景 A 类似，但额外动作：

1. 额外拷贝 `assets/templates/docs/phase1/{INIT_REQ,CODEBASE}.md` 到 `docs/phase1/`：

   ```bash
   mkdir -p docs/phase1
   cp "$SKILL_DIR/assets/templates/docs/phase1/"{INIT_REQ,CODEBASE}.md docs/phase1/
   ```

2. 修改新拷贝的 `CLAUDE.md` 和 `config/PROJECT_STATUS.md`（注意 macOS 与 Linux 的 `sed -i` 语法不同，下面是 macOS 版）：

   ```bash
   sed -i '' 's/- \*\*当前模式\*\*：全新开发/- **当前模式**：二期接入/' CLAUDE.md
   sed -i '' 's|- \*\*基线文档\*\*：无|- **基线文档**：docs/phase1/|' CLAUDE.md
   sed -i '' 's/\*\*项目模式\*\*：全新开发/**项目模式**：二期接入/' config/PROJECT_STATUS.md
   ```

   Linux 上把 `sed -i ''` 替换为 `sed -i`。

3. 引导用户额外填写：
   - 一期代码仓库路径（写入 `CLAUDE.md` 的"一期代码仓库"字段）
   - `docs/phase1/INIT_REQ.md` 中的一期功能描述

4. 提示接下来要走"基线重建"流程：产品经理启动 BA 角色，告诉它"请重建一期基线 PRD"

---

## 场景 C：已有项目中启动角色

用户提到某个角色（"BA 角色"/"Arch 角色"/"Dev 角色"/"TechLead 角色"/"TechLead Review"）时：

1. **加载该角色文件**：读 `config/roles/<ROLE>.md`（项目根相对路径，因为模板已经拷贝过去了）
2. **按文件中"第一步：了解背景"开始执行**：读 `config/TEAM_GUIDE.md`、`config/PROJECT_STATUS.md`、`CLAUDE.md` 等
3. **严格遵守角色的自主权边界**（见 `config/TEAM_GUIDE.md` 第 2.3 节）和"⏸️ 停下来"节点：每个角色在完成自己阶段的工作后必须停止，等待下一个角色或人工接手，**不要跨角色自动推进**

特殊触发词识别：

| 用户表述 | 加载文件 |
|---------|---------|
| "BA 角色"/"业务分析"/"启动 BA" | `config/roles/BA.md` |
| "Arch 角色"/"架构师"/"启动 Arch" | `config/roles/ARCH.md` |
| "Dev 角色"/"开发者"/"启动 Dev"/"开始编码" | `config/roles/DEV.md` |
| "TechLead 角色"/"技术负责人"/"TechLead Review"/"代码审查"（在 AgentBaton 项目中） | `config/roles/TECHLEAD.md` |

---

## 通用纪律（所有场景共享）

- **不要把 4 个角色合并执行**：每个角色完成自己阶段就停，等用户手动启动下一个角色
- **Git 策略**：本 skill 借用当前用户的 git 账号做**本地 commit**，**不主动 push**。`push` 由用户手动执行
- **不要修改 `docs/INIT_REQ.md` 的原始需求部分**：迭代需求只在末尾"迭代需求"区域追加
- **二期接入项目的 `docs/phase1/` 是只读基线**：基线一旦由开发负责人校验通过即冻结，不再修改
- **如果用户在场景 C 下提的具体诉求与当前角色职责不符**（例如让 Dev 做架构决策），按角色边界拒绝并建议切换到合适角色

---

## 协议主体

详细的协作流程、文档体系、阶段交接、二期接入逆向重建、迭代变更路径 A/B 等，在项目内的 `config/TEAM_GUIDE.md` 中。**Skill 触发后第一件实事必须是读它**（场景 A/B 拷贝完成后读项目内的，场景 C 直接读项目内的）。

各角色的详细指令（包含 Git 提交话术、交接 Checklist、停留点）在 `config/roles/<ROLE>.md`。

---

## 触发疑似边界情况

下列情形**不要触发**本 skill，让 Claude 按普通方式回应：

- 用户在非 AgentBaton 项目里说"写个 PRD 文档" → 这是普通文档写作，不是启动框架
- 用户在 AgentBaton 项目里说"帮我改 main.go 的一个 bug" → 这是常规 Dev 任务，按普通方式做就行
- 用户问"AgentBaton 是什么"/"这个框架怎么用" → 直接简要解释，不要进入初始化流程
- 用户提到"团队"/"协作"/"PRD"/"架构"/"Review" 这些词但没有上下文表明在用 AgentBaton → 不要触发
