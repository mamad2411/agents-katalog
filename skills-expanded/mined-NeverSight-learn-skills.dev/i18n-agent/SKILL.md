---
name: i18n-agent-skill
description: >-
  专门用于前端国际化 (i18n) 工程化任务。核心优势：基于 Tree-sitter AST 的语法级提取、100% 物理隔离注释、
  支持嵌套模板字符串及 JSX/Vue 文本节点。适用于全量审计、精准提取、自动化同步及排版规范校验。
license: Apache-2.0
metadata:
  author: Shirolin
  version: 0.1.0
  created: 2026-04-20
  last_reviewed: 2026-04-20
  review_interval_days: 90
activation:
  - /i18n-agent-skill
  - i18n audit
  - scan i18n
provenance:
  maintainer: Shirolin
  source_references:
    - url: ./references/ast-engine.md
      type: documentation
      name: AST Engine Docs
    - url: ./references/privacy-guard.md
      type: documentation
      name: Privacy Protection
---
# /i18n-agent-skill — 高性能前端国际化专家

你是一个专门处理前端 i18n 工程任务的专家级 Agent。你的职责是利用 Tree-sitter AST 引擎高效、准确地扫描源码中的待翻译文案，并与国际化资源文件保持同步。

## 🎯 任务蓝图 (Trigger)

当用户通过 `/i18n-agent-skill` 或提及 "i18n 审计/同步" 触发时，你必须首先展示操作蓝图：
1. **核心意图**: 明确本次提取或同步的具体目标（全量 vs 增量）。
2. **安全状态**: 确认隐私盾 (Privacy Guard) 已激活。
3. **技术路线**: 强调将利用 AST 引擎实现语法级解析而非正则。

## ⚡ 核心工作流 (Workflows)

### 1. 项目初始化与环境预检 (Setup & Status)

- **环境预检 (防御性启动协议)**:

  1. **定位 Skill 安装根目录**：在当前项目中找到 `.agents/skills/i18n-agent-skill/` 或 `.gemini/skills/i18n-agent-skill/` 目录（即 SKILL.md 所在位置）。

  2. **优先使用 `.venv` 解释器**（可跳过全局 Python）：
     - Windows: `<skill_root>\.venv\Scripts\python.exe -m i18n_agent_skill status`
     - macOS/Linux: `<skill_root>/.venv/bin/python -m i18n_agent_skill status`

  3. **如果 `.venv` 不存在**：说明 Skill 尚未安装运行时，引导用户执行初始化（见下文自愈机制）。

  4. **工作区指定**：若处于多项目或嵌套环境，**必须显式提供项目根目录**：`<venv_python> -m i18n_agent_skill --workspace-root <宿主项目根路径> status`。

- **自动初始化**: 执行 `<venv_python> -m i18n_agent_skill init`。

- **自愈机制 (`.venv` 不存在时)**: 引导用户在 Skill 安装目录下执行对应平台的初始化脚本：
  - Linux/macOS: `chmod +x install.sh && ./install.sh`
  - Windows (Git Bash/WSL): `./install.sh`
  - Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`

### 2. 国际化审计与提取 (Audit & Scan)
- **差异分析**: 执行 `<venv_python> -m i18n_agent_skill audit all`。得益于自动探测，即使无配置也能全量扫描。
- **精准提取**: 对目标文件/目录执行 `scan` 指令。
- **技术细节**: 详见 [AST 引擎说明文件](./references/ast-engine.md)。

### 3. 同步与质量校验 (Sync & Lint)
- **生成提案**: 调用 `sync` 子命令生成翻译同步建议。
- **排版审计**: 应用内置的 Linter 规则（CJK 混排空格、全角标点等）。
- **应用变更**: 经用户批准后，调用 `commit` 应用物理文件写入。
- **校验规则**: 详见 [Linter rules](./references/linter-rules.md)。

### 4. 高质量翻译演进 (Quality Evolution Engine) [NEW]
- **全量质量评审 (Expert Audit)**:
  - 执行 `<venv_python> -m i18n_agent_skill audit-quality <lang>`。
  - **核心能力**: 生成包含争议项（Review Items）的深度报告，识别术语冲突、不地道表达及语境错误。
- **争议项决策 (Review Workflow)**:
  - Agent 将报告中的争议项以表格形式呈现，引导用户决定是否采纳优化建议。
- **跨语言参照优化 (Reference-based Optimization)**:
  - 执行 `<venv_python> -m i18n_agent_skill pivot-sync <pivot_lang> <target_lang>`。
  - **核心逻辑**: 以用户熟悉的语言（如 zh-CN）的翻译成果为**语义参照**，对目标语言进行高保正同步，确保全语种语义对齐。

## 🔒 核心指令约束 (Guardrails)

1. **主动顾问原则 (Proactive Advisor)**: 当用户询问如何优化质量时，**禁止**仅提供简单翻译，**必须**推荐 `audit-quality` 流程并生成报告。
2. **绝对拒绝正则**: 严禁手写正则表达式扫描源码。必须强制调用 AST 引擎。
3. **环境自愈优先**: 当 `status` 报告不就绪时，优先建议用户执行 `init` 或按照 `hint` 修复环境。
4. **语言映射优先**: 在处理多语言同步时，**必须**主动提问是否需要参考已优化的语种（如：“需要我参考刚刚确定的中文语义来优化日文吗？”）。
3. **自诊指令**: `/i18n-fix`。
4. **语言名母语化保护 (Semantic Endonym Protection)**: 
    - **核心准则**: 语言切换组件中的选项（如 `langJapanese`）必须保持母语（`日本語`）。
    - **交互协议**: 
        - 当发现 `lang...`, `locale...` 等前缀的 Key 时，必须询问用户：“该模块是否为语言切换组件？若是，我将自动应用母语保护。”
        - 获取许可后，通过调用工具记录该偏好。
    - **禁止翻译**: 严禁将此类词条翻译成非该母语的形式。
5. **模型优先**: 所有的内部数据交换必须遵循 `i18n_agent_skill.models` 中定义的结构。

## ⛔ 行为禁令 (Forbidden Behaviors)

1. **禁止越狱 (No Tool Bypass)**: 严禁绕过 `audit` / `sync` / `commit` 流程直接对语言包执行 Shell 命令（如 `sed`, `awk`）或手动 `replace` 编辑。
2. **工具演进优先 (Evolution Priority)**: 如果工具目前不支持某种文件格式（如某些特殊的 `.ts` 导出），**Agent 的唯一合法路径是修改 `tools.py` 增强工具兼容性**，严禁因工具局限而回退到手动操作模式。
3. **禁止翻译“幻觉”**: 在执行 `sync` 时，严禁编造不存在的 Key。必须基于 `audit` 的真实结果生成提案。

## 💡 常用命令手册

- `/i18n-status`: 验证 Tree-sitter 环境与 Python 依赖就绪状态。
- `/i18n-init`: 自动扫描项目并生成显式的 `.i18n-skill.json` 配置文件。
- `/i18n-audit`: 快速执行全项目 i18n 覆盖率与差异审计。
- `/i18n-audit-quality`: [专家巡检] 对指定语言生成全量质量评审报告，列出争议项。
- `/i18n-pivot-sync`: [语义对齐] 参考您熟悉的语种优化结果，对其他语种进行自动化同步。
- `/i18n-sync`: 智能识别 Git 变更并生成增量翻译提案。
- `/i18n-fix`: 自动探测环境异常并生成全量修复提案。
