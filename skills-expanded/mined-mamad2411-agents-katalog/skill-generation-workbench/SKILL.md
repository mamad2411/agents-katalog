---
name: skill-generation-workbench
description: "设计、生成和验证 Codex Skill 包。用于用户提出创建 Skill、开发 Skill、把流程或专家能力封装成 Skill、把外部专家卡片或提示词转换为 Skill，或需要升级已有 Skill 时；写入前先用 find-skills 再查 SkillHub，核对可复用能力，然后澄清触发场景、输入输出、边界和副作用，最后生成符合约定的 SKILL.md、agents/openai.yaml、引用文件和可选脚本。"
---

# skill生成器 / Skill Generator

## Overview

将模糊的“帮我做一个 Skill”请求整理成可执行的 Skill 蓝图，并生成一个可验证、可维护、不会默认安装或发布的 Skill 包。写入文件前先查找可复用能力，避免重复造 Skill。保持 Skill 是能力与工作流，不把人格、身份或专家灵魂写进 `SKILL.md`。

## Operating Modes

识别用户要做的模式：

- **create**：从想法、流程、文档、截图或外部专家卡片创建新 Skill。
- **upgrade**：分析并改进已有 Skill 的触发条件、流程、资源或验证。
- **convert**：把已有 agent、prompt 或专家卡片转成 Skill；剥离 persona，只保留能力和工作流。
- **review**：只审查 Skill 的触发、结构、重复能力、安全和验证，不修改文件，除非用户要求修复。

## Intake

当需求已经包含目标能力、触发方式、输入输出和目标位置时，直接进入设计；不要为了形式重复提问。信息不足且会影响实现时，一次只问最少的阻塞问题：

1. 这个 Skill 解决什么任务，用户会用哪些自然语言请求触发它？至少收集 2 个真实例句。
2. 它接收哪些输入，应该产出什么结果或文件？哪些结果算完成？
3. 目标位置是当前仓库、某个项目，还是用户的 Skill 目录？是否只生成仓库包，不安装？
4. 是否会执行提交、推送、安装、删除、部署或其他外部副作用？没有明确授权时一律只生成和验证。

保留用户的原始术语和约束。不要凭空补充组织规则、私有 API、凭据、远程地址或“自动发布”行为。

## Workflow

### 0. Capability Discovery Before Writing (MANDATORY)

For **create**, **upgrade**, and **convert** modes, complete this discovery phase before creating,
editing, or scaffolding any package file. Review-only mode may skip it when no files will be written.
The order is mandatory: **find-skills first, then SkillHub**.

1. Build a focused query from the domain, user task, stack, inputs, outputs, and risk terms. Keep it
   short enough to search, for example `react form validation`, `harmonyos app release`, or
   `api contract testing`.
2. Use the `find-skills` discovery workflow first:

   ```bash
   npx --yes skills find "<domain> <task> <stack>"
   ```

   Read the candidate name, repository, `skills.sh` URL, install count, and source. This is search
   only; do not run `npx skills add` or install a candidate.
3. Query SkillHub second, using the local CLI when available:

   ```bash
   skillhub --skip-self-upgrade search "<domain> <task> <stack>" --json --search-limit 20
   ```

   The CLI searches `https://skillhub.cn/`. If the CLI is unavailable, read the public search API at
   `https://api.skillhub.cn/api/v1/search` with `q` and `limit`; do not infer results from the home page.
4. Compare both result sets with the repository registries and installed local roots. For every
   serious candidate, inspect its visible `SKILL.md` or package metadata when reachable, and record
   name, source, capability overlap, input/output compatibility, version or install evidence, and
   verification status. Search metadata alone is not proof that a Skill is usable.
5. Make one explicit decision before writing:
   - **reuse** an existing local or verified external capability when it already owns the task;
   - **upgrade** the existing package when the request is an extension of its scope;
   - **convert** an external package when the user supplied a visible expert/prompt package;
   - **create** a new package only when no verified candidate owns the required workflow or the
     boundary is materially different.
6. Record the query, both source results, rejected candidates, and the reuse/upgrade/convert/create
   decision in the blueprint. A failed or unavailable search must be reported as an evidence gap,
   not silently treated as “no matching Skill”.

### 1. Inspect

先完成第 0 阶段的能力发现，再确认当前工作区和目标目录，检查是否存在同名或功能重叠的 Skill：

- 查看 `git status --short --branch -uall`，不要覆盖用户已有改动。
- 用 `rg` 搜索现有 `SKILL.md` 的 `name`、描述和触发词；在 `tiny-agents` 中优先查看 `indexes/skill-registry.md`，若要看本地扫描库存再看 `indexes/agent-skill-index.md`。
- 将第 0 阶段的 `find-skills` 和 SkillHub 结果与本地 registry 一起比较，不因远端搜索结果存在就覆盖本地 Skill。
- 若输入来自截图或外部专家卡片，只把可见的名称、摘要、标签和流程当作来源；缺失的隐藏 prompt 不得臆造。
- 选择短的、动词导向的 hyphen-case 名称；已存在相同能力时优先升级或复用，而不是创建重复包。

### 2. Design The Blueprint

在写文件前形成一份内部蓝图，至少包含：

- `name`：不超过 64 个字符，只用小写字母、数字和连字符。
- `description`：明确能力和触发场景；把所有触发条件放在 frontmatter 中。
- `inputs` / `outputs`：输入材料、交付物、成功判定和不确定性处理。
- `workflow`：按顺序列出发现、执行、验证和交付步骤；为高风险操作设置确认点。
- `resources`：只有反复需要或适合确定性执行的内容才放入 `scripts/`、`references/` 或 `assets/`。
- `validation`：列出结构校验、脚本测试、项目测试和安全扫描。

把长篇领域知识放入一层 `references/` 文件，并在 `SKILL.md` 中说明何时读取。不要创建 README、安装指南、变更日志或仅用于叙述的附属文件。

### 3. Scaffold

创建新包时，使用本 Skill 的脚本生成稳定骨架：

```bash
python3 scripts/scaffold_skill.py <skill-name> \
  --path <parent-directory> \
  --description "<what it does and when to use it>" \
  --resources references
```

脚本会拒绝覆盖已有目录，并生成 `SKILL.md`、`agents/openai.yaml`、安全的 `source.json` 和请求的资源目录。它只生成骨架，不会替代具体能力内容；随后补全 `SKILL.md`，并删除未使用的资源目录。

更新已有 Skill 时直接编辑现有文件，保留有效的来源元数据和用户改动；不要重新初始化或整包覆盖。

### 4. Implement

把蓝图转成目标包：

- `SKILL.md` 只写另一个 Codex 实例执行任务所需的非显然规则，使用祈使式步骤和具体决策点。
- frontmatter 只包含允许的 `name`、`description`、`metadata` 等字段；默认不要增加工具依赖。
- `agents/openai.yaml` 的 `display_name`、`short_description` 和 `default_prompt` 必须与 Skill 一致，`default_prompt` 必须显式包含 `$skill-name`。
- 脚本必须使用参数而不是硬编码本机路径；任何写入、网络、安装、提交或推送动作都要有清晰的边界和失败处理。
- `source.json` 只能写公开的相对来源标识，例如 `repo-local/generated` 或 `~/.codex/...`，不得写本机绝对路径、token、凭据或运行缓存。
- 如果是外部专家卡片转换，声明是卡片或可见资料派生；不要声称拥有未提供的内部专家详情。

### 5. Validate

按风险执行验证，至少运行：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" <skill-directory>
python3 -m json.tool <skill-directory>/agents/openai.yaml
git diff --check
```

注意：`agents/openai.yaml` 是 YAML，不是 JSON；如果 `json.tool` 不适用，使用仓库已有 YAML 解析器或针对 YAML 的结构检查，并验证关键字段。脚本资源必须实际运行，新增 Python 测试必须纳入 `python3 -m unittest`。

发布前扫描本机路径和敏感信息，确认没有机器专属 home 路径、临时目录、私有运行目录、token、密钥或临时报告进入 Skill。检查 `git status --short -uall`，确认只有预期文件变化。

### 6. Deliver

交付时说明：生成或更新的绝对文件路径、Skill 名称、典型触发例句、资源文件、验证命令和结果。把未解决的假设与风险单独列出。

默认只生成并验证仓库 Skill 包。安装到 `~/.codex/skills`、提交、推送、部署或删除旧 Skill 都必须等用户明确授权。

## Output Contract

一个完成的生成任务至少交付：

1. 可触发的 `SKILL.md`，frontmatter 完整且没有 TODO 占位内容。
2. 与内容一致的 `agents/openai.yaml`。
3. 必要时提供引用文件或确定性脚本；没有实际用途的目录不保留。
4. 能力发现记录：查询词、find-skills 结果、SkillHub 结果、候选验证、拒绝原因和最终复用/升级/转换/新建决策。
5. 结构校验、安全扫描和相关测试的真实结果。

详细字段、蓝图和检查表见：

- [references/guide.md](references/guide.md)
- [references/skill-contract.md](references/skill-contract.md)
- [references/generation-checklist.md](references/generation-checklist.md)
