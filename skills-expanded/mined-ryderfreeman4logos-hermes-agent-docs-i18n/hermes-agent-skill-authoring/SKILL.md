---
name: hermes-agent-skill-authoring
description: "Author in-repo SKILL.md files: frontmatter and structure."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, authoring, hermes-agent, conventions, skill-md]
    related_skills: [requesting-code-review]
---

# 编写 Hermes-Agent 技能（在代码仓库中）

## 概述

SKILL.md 文件可以存放在两个位置：

1. **用户本地**：`~/.hermes/skills/<可选分类>/<名称>/SKILL.md` —— 仅个人使用，不会被共享。可通过 `skill_manage(action='create')` 创建。
2. **在代码仓库中（针对当前项目）**：位于 hermes-agent 代码仓库内的 `skills/<分类>/<名称>/SKILL.md` 或 `optional-skills/<分类>/<名称>/SKILL.md` —— 会被提交并随软件包一起发布。需使用 `write_file` 加上 `git add` 操作完成。`skill_manage(action='create')` 不适用于此路径下的文件。

代码仓库中的技能必须符合该仓库的**严格编写标准**（详见 AGENTS.md 中的“技能编写标准（HARDLINE）”——该部分为权威依据，本文档仅为操作指南）。审核人员会拒绝违反这些标准的 Pull Request，因此提前满足标准比后期补救更为高效。

## 适用场景

- 用户要求你在“当前分支/代码仓库/提交版本”中添加某项技能。
- 你要提交的流程可复用，且应随 hermes-agent 一同发布。
- 你需要编辑 `skills/` 或 `optional-skills/` 目录下的现有技能（细微修改可使用 `patch`，全面重写则使用 `write_file`；对于代码仓库中的技能，`skill_manage` 仍可用于执行 patch 操作，但不支持创建新技能）。
- **不适用于**：`~/.hermes/skills/` 中的个人技能（此类情况直接使用 `skill_manage` 即可）。

## 先确定技能类型：内置型还是可选型

- **内置技能（`skills/<category>/`）**——适用于日常高频使用，对各类用户都极具通用性，占用资源少。其判定标准极为严格：必须能够确信“该用户每月会在5次及以上会话中加载此技能”。
- **可选技能（`optional-skills/<category>/`）**——针对特定细分领域（如区块链、游戏、金融或某款特定应用）、重复性任务所需的技能，或是资源占用较大的技能。可通过命令 `hermes skills install official/<category>/<skill>` 进行安装。

**遇到不确定的情况时，优先选择可选技能。**后续再将其升级为内置技能很容易，但降级则可能导致用户流失。“任何需要此技能的人都会受益”这类理由仅适用于可选技能，而不适合内置技能。

分类时应根据工具的实际功能来选择，而非其给人的感觉（即便某个AI智能体CLI工具能提升工作效率，也应归类到 `autonomous-ai-agents/` 中）。可通过命令 `search_files(pattern='*', target='files', path='skills')` 查阅现有分类，切勿随意创建新的顶级分类。

**禁止创建路由/索引/中枢类技能。**那些核心内容仅为指向其他相关技能的路由表的技能，只会增加额外的间接调用环节，并重复这些关联技能本身的“使用场景”说明。如果该技能在没有“加载技能X替代”的指引下内容就会为空，那就无需编写——目录结构及各关联技能的触发条件已能完成相同功能。

## 必需的前置信息

验证规则的具体来源：`tools/skill_manager_tool.py::_validate_frontmatter`。验证时的硬性要求包括：

- 第一个字节为 `---`，且前面没有空行。
- 内容之前以 `\n---\n` 作为结尾。
- 被解析为 YAML 映射格式。
- 必须包含 `name` 字段。
- 必须包含 `description` 字段（验证规则要求长度不超过 1024 字符——但请注意下方的仓库硬性限制，其要求更为严格）。
- 结尾的 `---` 之后必须有非空内容。

遵循仓库标准格式（即使验证规则未作强制要求，也必须包含所有字段）：

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)
description: Concise capability statement, under sixty chars.
version: 0.1.0                    # semver; new skills start at 0.1.0
author: Real Name (github-handle), Hermes Agent
license: MIT
platforms: [linux, macos, windows]   # audit, don't guess — see Platform Gating
metadata:
  hermes:
    tags: [Short, Descriptive, Tags]
    related_skills: [other-in-repo-skill]
---
```

### `description` 规则（重要提示——验证工具允许的长度为1024字符，并非标准限制）

- **长度不超过60个字符**，且需为单句，以句号结尾。
- 应描述功能而非实现方式，同时不得重复技能名称。
- 禁止使用营销性词汇，如“强大”“全面”“无缝”“先进”等。
- 系统提示中的技能索引显示长度最多为57个字符，超出部分会显示“...”——因此触发条件或功能描述必须完整包含在该范围内。
- 若描述中包含冒号`:`，需用双引号将其括起来；否则YAML解析器会将其视为映射结构，导致文档生成工具崩溃。双引号不计入60字符的限制内。

**正确示例**：`Track named companies for material news with cited digests.`
**错误示例**：`Use when a user asks to monitor named competitors or companies for product launches, pricing changes, funding, ...`（长度达240字符，审核时被拒绝）

### `author` 规则

- 首先注明**人类作者**，其次标注“Hermes Agent”作为协作方，格式为：`Ben Barclay (benbarclay), Hermes Agent`。
- 对于由他人贡献的技能，绝不能仅写`author: Hermes Agent`——即便内容是由智能体撰写的，也需注明人类作者，而非工具本身。
- 由维护者自行编写的技能，格式为：`Teknium (teknium1), Hermes Agent`。

### `related_skills` 规则

- 每个条目都必须对应您PR所在分支树结构中已存在的技能。不得引用仅处于规划阶段、位于其他PR中，或仅存在于`~/.hermes/skills/`目录下的技能。
- 需逐一验证每个条目，可使用命令 `search_files(pattern='<name>', target='files', path='skills')`（以及 `optional-skills/` 目录）进行检查。
## 平台限制策略：审核优先，绝不盲目信任

`platforms:` 用于根据主机操作系统来控制功能的加载。其值应依据该技能的代码及脚本实际调用的环境来确定：

| 技能仅使用…… | `platforms:` |
|---|---|
| Hermes 工具 + 标准库 Python + 跨平台 CLI 工具 | `[linux, macos, windows]` |
| bash 流水线、`grep`/`awk`/`sed` 处理命令、heredoc 文件 | `[linux, macos]` |
| `osascript`、`defaults`、`pmset` 命令 | `[macos]` |
| `apt`/`systemctl`/`/proc` 接口 | `[linux]` |

在 `scripts/` 目录中应查找仅适用于 POSIX 系统的信号，例如：`fcntl`、`termios`、`pty`、`os.fork`、`os.killpg`、`signal.SIGKILL`、`os.kill(pid, 0)` 等用于检测程序是否存活的信号，以及硬编码的 `/tmp`、`/proc`、`/etc` 路径。推荐做法是首先确保代码具备跨平台兼容性（如使用 `tempfile.gettempdir()`、`pathlib.Path`、`psutil.pid_exists` 等函数）；只有在某项功能确实受特定平台限制时，才设置更严格的平台限制，并在 `## 潜在问题` 部分说明原因。

## 文件大小限制

- 完整的 SKILL.md 文件长度不得超过 100,000 个字符（受 `MAX_SKILL_CONTENT_CHARS` 参数约束），但建议简单技能的文件控制在 **约 100 行**，复杂技能则控制在 **约 200 行**。同类技能的文件长度通常在 8,000 至 14,000 字符之间。
- 体积较大或仅适用于特定分支的内容应存放在 `references/*.md`、`templates/` 或 `scripts/` 目录中，通过引用方式在 SKILL.md 中提及，而非直接嵌入代码。
- 不要期望模型能在每次调用时都自动嵌入解析器或复杂的逻辑代码——建议将相关辅助脚本放入 `scripts/` 目录，并通过路径进行调用。

## 文档结构（现代章节顺序）

```
# <Skill> Skill
2-3 sentence intro: what it does, what it doesn't do, dependency stance.

## When to Use          — bulleted triggers (+ "Don't use for:" counter-triggers)
## Prerequisites        — exact env vars, installs, API key sourcing
## How to Run           — canonical invocation through the `terminal` tool
## Quick Reference      — flat command list, no narration
## Procedure            — numbered steps, each with a checkable completion criterion
## Pitfalls             — known limits, things that look broken but aren't
## Verification         — how to prove the skill worked
```

并非每个技能都需要包含所有章节（纯流程型任务技能可能无需“快速参考”部分），但“使用场景说明”+“可操作步骤”+“常见陷阱”+“验证方法”是不可或缺的。应删除营销性引言、无实际意义的“设置检查”内容，以及已在“前置条件”中阐述过的环境变量说明。

### 应引用Hermes内置工具，而非原始shell命令

当技能需要某种功能时，需用反引号标明对应的Hermes工具名称：`terminal`、`read_file`、`write_file`、`patch`、`search_files`、`web_search`、`web_extract`、`browser_navigate`、`vision_analyze`、`delegate_task`、`cronjob`。切勿使用Agent已封装好的shell工具名称（例如将`grep`替换为`search_files`，`cat`替换为`read_file`，`sed`/`awk`替换为`patch`，`find`/`ls`替换为`search_files target='files'`）。基于CLI的技能应采用`terminal(command="<tool> ...", timeout=...)`的格式来组织指令调用——直接使用原始shell语句（如“run `foo --version`”）属于会阻碍审核的违规行为。若该技能依赖MCP服务器，也需在“前置条件”中明确说明其名称并记录相关设置方法。

### 绝对禁止使用本地机器路径

应使用相对于代码仓库的路径（如`skills/...`、`tools/skill_manager_tool.py`）。如果在已提交的技能代码中硬编码了`/home/<you>/...`这类本地路径，将会影响其他所有用户的使用，且会立即成为审核时的问题点。

## 编写优质技能的原则

技能存在的意义在于提升Agent执行流程的可预测性——让Agent始终遵循一致且高效的运作规范。

1. **提升流程的可预测性。** 若某条指令不会改变处理结果，应将其删除。  
2. **合理控制上下文信息量。** 每次交互都会产生费用，详细内容应放在正文或链接参考中。  
3. **为每一步设定明确的完成标准。** 这些标准需具备可验证性，且在关键情况下应做到全面覆盖——例如使用“确保所有修改过的文件都被处理”而非“总结更改内容”。  
4. **将规则与其所管理的概念放在一起。**  
5. **使用简洁有力的词汇**（如“闭环机制”“根本原因”“回归测试”），而非冗长的重复解释。  
6. **去除重复内容和无用操作。** “请谨慎操作”和“遵循最佳实践”无法改变模型行为——应将其替换为可验证的标准或直接删除。  

## 测试与文档（仓库管理技能的必备项）

1. **测试代码**位于`tests/skills/test_<skill>_skill.py`中——仅允许使用标准库、pytest以及`unittest.mock`，禁止使用网络连接。可通过`scripts/run_tests.sh tests/skills/test_<skill>_skill.py -q`命令运行。（通用的`tests/tools/test_skill_manager_tool.py`测试通过并不能证明你的技能也符合要求。）
2. **文档重新生成**：运行`python website/scripts/generate-skill-docs.py`，随后需严格控制文件范围——该工具会重写所有自动生成的页面。请使用`git checkout --`移除所有非你负责的文件；最终的差异对比结果中应仅显示你的SKILL.md文件、每个技能对应的独立文档页、一条简短的目录条目，以及`website/sidebars.ts`文件中的一行插入内容（可通过`search_files(pattern='<your-slug>', path='website/sidebars.ts')`进行验证——必须恰好返回一条匹配结果，否则该页面即为孤立文件）。
3. **`.env.example`文件**（仅当该技能需要新的环境变量时使用）：需用注释清晰地标出相关内容；请勿修改该文件中的其他任何部分。

## 工作流程

1. 使用`search_files(target='files')`查找目标类别中的同类技能，阅读2-3个同类技能的SKILL.md文件，以此确定文档的风格与结构。建议优先扩展现有技能，而非创建功能单一的新技能。
2. 确定技能的层级与类别（参见上文）。如有疑问，可自行选择，但提交前务必征得他人意见，切勿直接默认设置。
3. 使用`write_file`命令将内容写入`skills/<category>/<name>/SKILL.md`文件中（或`optional-skills/...`目录下）。
4. 在本地进行验证：
   ```python
   import yaml, re, pathlib
   content = pathlib.Path("skills/<category>/<name>/SKILL.md").read_text()
   assert content.startswith("---")
   m = re.search(r'\n---\s*\n', content[3:])
   fm = yaml.safe_load(content[3:m.start()+3])
   assert "name" in fm and "description" in fm
   assert len(fm["description"]) <= 60, f"description {len(fm['description'])} chars — hardline is 60"
   assert fm["description"].endswith(".")
   assert "platforms" in fm
   assert len(content) <= 100_000
   ```
同时，请确认仓库中确实存在每一个`related_skills`条目。
5. **添加测试用例并重新生成文档**（见上一节）。
6. 在当前分支上执行`Git add + commit`操作，然后创建一个Pull Request。
7. **注意：**当前会话的技能加载器处于缓存状态——因此直到开启新会话后，`skill_view`/`skills_list`才会显示新增的技能。这是正常现象，并非错误。

## 编辑仓库中的现有技能

- **小型修复：**对于仓库中的技能，可使用`skill_manage(action='patch', ...)`函数，或者直接使用`patch`命令。
- **大规模重写：**需要将整个SKILL.md文件的内容通过`write_file`函数写入。
- **辅助文件：**也可以通过`write_file`函数向技能目录下的`references/`、`templates/`或`scripts/`文件夹中添加文件。
- **务必执行提交操作**——仓库中的技能属于代码源，而非运行时状态。一旦前置数据发生变化，就需要重新运行文档生成工具。

## 常见问题与陷阱

1. **使用 `skill_manage(action='create')` 创建仓库内的技能时**。该命令会将内容写入 `~/.hermes/skills/` 目录，而非仓库目录结构中，请改用 `write_file` 命令。

2. **以验证工具的限制作为标准**。验证工具允许描述长度为1024字符，而审核流程会拒绝长度超过60字符的描述。验证工具不会检查 `platforms:`、作者格式、测试用例或文档内容，这些需由审核流程来处理。

3. **贡献的技能需标注 `author: Hermes Agent`**。应首先注明具体贡献者。

4. **`---` 前不能有前置空格**。若存在前置空行或BOM字符，验证将会失败。

5. **描述过于笼统，或触发词位于57字符之后**。

6. **`related_skills` 指向仓库中不存在的技能**（如用户本地保存的、计划添加的，或位于其他分支中的技能）。

7. **重复创建同类技能**。应先查看该类别中已有的技能，选择扩展而非重复创建。

8. **跳过文档生成工具，或推送与其无关的变更内容**。这两种做法都是错误的：不生成文档会导致技能孤立且没有文档页面；盲目生成文档则会使得差异文件因包含其他技能的变更内容而变得臃肿。

9. **认为新技能会立即在当前会话中显示**。实际上，加载器是在会话启动时才被初始化的。

10. **任由技能相关内容逐渐积压**。添加规则时，应同时删除被替代的旧内容。

## 验证检查清单

- [ ] 级别需明确指定（套餐标准：每月5次及以上使用；否则归类至`optional-skills/`）
- [ ] 文件应存放于`skills/<类别>/<名称>/SKILL.md`或`optional-skills/<类别>/<名称>/SKILL.md`路径下
- [ ] 前置信息需以字节0处的`---`开始，以`\n---\n`结束
- [ ] 必须包含`name`、`description`、`version`、`author`、`license`、`platforms`以及`metadata.hermes.{tags, related_skills}`字段
- [ ] 描述内容长度不得超过60个字符，需为单句结构，以句号结尾，不得包含任何营销用语
- [ ] `author`字段需首先注明实际贡献者姓名
- [ ] `platforms:`字段的内容需根据实际代码/脚本核实，不可复制自其他相关文件
- [ ] 所有的`related_skills`条目都必须在代码仓库内部可找到对应内容
- [ ] 正文需遵循现代文档结构规范，所有指令均需通过Hermes工具呈现
- [ ] 文件中严禁出现任何基于本地机器的路径
- [ ] 每个有序步骤都需设定可验证的完成标准
- [ ] 通过`scripts/run_tests.sh`运行后，`tests/skills/test_<skill>_skill.py`中的测试用例必须全部通过
- [ ] 文档生成时需严格遵循结构规范，侧边栏中对应slug的条目数量必须为1个
- [ ] 需在指定分支上执行`git add`并提交代码，随后创建PR
