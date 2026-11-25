---
name: kanban-video-orchestrator
description: Plan and run multi-agent video production pipelines.
version: 1.0.0
author: [SHL0MS, alt-glitch]
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, kanban, multi-agent, orchestration, production-pipeline]
    related_skills: [ascii-video, manim-video, p5js, comfyui, touchdesigner-mcp, pixel-art, ascii-art, songwriting-and-ai-music, heartmula, songsee, youtube-content, claude-design, excalidraw, architecture-diagram, concept-diagrams, baoyu-comic, baoyu-infographic, humanizer, gif-search, meme-generation]
    credits: |
      The single-project workspace layout, profile-config patching pattern,
      SOUL.md-per-profile model, TEAM.md task-graph convention, and
      `--workspace dir:/abs/path` discipline are adapted from alt-glitch's
      original multi-agent video pipeline at
      https://github.com/NousResearch/kanban-video-pipeline.
---

# Kanban 视频编排工具

无论您需要处理的是15秒的产品预告片、5分钟的叙事短片、音乐视频，还是ASCII循环动画——均可将其封装在Hermes的Kanban流程中，由相应的专用智能体负责分步处理。

该技能本身并不直接执行任何渲染操作，而是一个元级流程，其功能包括：

1. 通过精准的匹配机制确定任务范围；
2. 根据视频风格自动配置合适的团队架构（包括各角色及其所需工具）；
3. 生成设置脚本，用于创建Hermes智能体配置、项目工作空间以及初始的Kanban任务；
4. 将任务转交给对应的执行智能体，由其通过Kanban流程进行分解处理；
5. 实时监控任务执行进度，在出现卡顿或失败时及时介入干预。

实际的渲染工作会在Kanban流程启动后由合适的现有技能与工具完成，这些工具可能包括：`ascii-video`、`manim-video`、`p5js`、`comfyui`、`touchdesigner-mcp`、`songwriting-and-ai-music`、`heartmula`，或是结合PIL与ffmpeg的普通Python脚本。

## 何时不应使用此技能

- 若视频属于无需专业分工的连续式生成项目，可直接编写代码完成制作；
- 若用户仅需快速转换文件格式（例如“将此MP4转换为GIF”），建议直接使用ffmpeg；
- 若输出结果为静态图片、GIF或纯音频文件，应选用对应的专用技能（如`ascii-art`、`gifs`、`meme-generation`、`songwriting-and-ai-music`）；
- 若任务完全适合某一个现有的技能处理（例如纯ASCII格式的视频），则直接使用`ascii-video`即可。

## 工作流程

```
DISCOVER  →  BRIEF  →  TEAM DESIGN  →  SETUP  →  EXECUTE  →  MONITOR
```

### 第一步 — 信息收集（提出恰当的问题）

信息收集过程是**自适应的**：只需询问实际所需的内容。建议始终从三个问题开始，以便初步明确项目的大致框架：

- **视频内容是什么？**（用一句话简要概括）
- **时长是多少？**（5-30秒的预告片 / 30-90秒的短片 / 90秒-3分钟的讲解视频 / 3-10分钟的电影级作品 / 更长时长）
- **宽高比及目标平台是？**（1:1 / 9:16 / 16:9；X平台、Instagram、YouTube、内部平台等）

根据用户的回答来确定风格类别，不同的风格将决定后续需要询问的问题。**切勿一次性提出所有问题**，建议每次询问2-4个问题，听取回复后再继续。当用户给出暗示性答案时，可进行合理推测。

完整的收集流程及各类风格的对应问题库，请参阅**[references/intake.md](references/intake.md)**。

### 第二步 — 撰写概要

在掌握足够信息后，使用`assets/brief.md.tmpl`中的模板来创建结构化的`brief.md`文件。其内容应包括以下部分：

1. **核心概念**——用一句话概括项目要点，并明确情感基调
2. **项目范围**——时长、宽高比、平台要求、截止日期
3. **风格要求**——视觉参考风格、品牌规范、语调风格
4. **分场景规划**——逐镜头详细说明（包含时长、内容描述及所需工具）
5. **音频元素**——旁白/音乐/音效/无声（如需可按场景分别指定）
6. **交付物要求**——文件格式、分辨率，以及可选的替代版本（竖屏版本、GIF等）

在组建制作团队之前，务必将这份概要展示给用户确认。**概要即项目契约**——后续的所有工作都将以此为依据。

### 第三步 — 团队组建

从角色模板库中挑选适合该视频的角色原型。**应进行组合，而非直接复制**。大多数视频需要4到7个角色配置文件，其中导演角色始终存在，其余角色则根据项目需求来确定。

有关角色模板库及不同风格团队的组成方式，请参阅 **[references/role-archetypes.md](references/role-archetypes.md)**。

若需了解某个角色会加载哪些Hermes技能和工具集，请参阅 **[references/tool-matrix.md](references/tool-matrix.md)**。

### 第4步 — 配置设置

生成一个配置脚本（`setup.sh`）并运行它。该脚本会执行以下操作：

1. 创建项目工作目录（`~/projects/video-pipeline/<slug>/`）
2. 将提供的所有资源文件复制到 `taste/`、`audio/`、`assets/` 目录中
3. 通过 `hermes profile create --clone` 命令创建每个Hermes角色配置文件
4. 为每个角色配置文件编写 `SOUL.md` 文件（用于定义角色性格与职责）
5. 配置对应角色的YAML文件（包括工具集、必加载技能及当前工作目录信息）
6. 编写 `brief.md`、`TEAM.md` 文件以及 `taste/` 目录中的内容
7. 创建初始任务并分配给导演，使用命令 `hermes kanban create` 处理该任务

若需根据项目需求文档和团队配置JSON自动生成 `setup.sh` 脚本，可使用 `scripts/bootstrap_pipeline.py` 工具。关于配置脚本的结构、角色配置规范以及重要的“共享工作目录”规则，请参阅 **[references/kanban-setup.md](references/kanban-setup.md)**。

### 第5步 — 执行运行

先运行 `setup.sh` 脚本，随后向用户提供用于监控项目进展的命令：

```bash
hermes kanban watch --tenant <project-tenant>     # live events
hermes kanban list  --tenant <project-tenant>     # board snapshot
hermes dashboard                                   # visual board UI
```

从这里开始，由负责人配置文件接管工作，它通过看板工具集将任务拆分并分配给相应的专业配置文件。

### 第6步 — 监控与干预

保持关注——虽然看板系统可以自主运行，但遇到卡住的任务或不良输出时，仍需人工（或人工智能）进行判断。

监控方式包括：定期查询 `kanban list`，使用 `kanban show <id>` 检查那些耗时超过预期的“运行中”任务，并查看任务的心跳状态。当某位执行者的输出未通过审核时，可采取的标准干预措施包括：

1. 使用 `kanban_comment` 在该执行者的任务上留下具体反馈；
2. 创建一个新任务并以其原有任务为父任务重新启动处理；
3. 调整任务要求的范围，由负责人重新拆分任务。

有关诊断方法、干预方案以及“任务卡住”时的处理指南，请参阅 **[references/monitoring.md](references/monitoring.md)**。

## 参考：实际案例

这里提供了六个涵盖不同视频风格的典型流程示例——故事电影、产品/营销视频、音乐视频、数学/算法讲解视频、ASCII艺术视频以及实时装置艺术视频——展示了如何通过相同的工作流形成截然不同的团队结构与任务关系图。详情请见 **[references/examples.md](references/examples.md)**。

## 重要规则

1. **先调研，后行动。** 在创建任务要求或组建团队之前，务必至少回答三个基础问题。糟糕的任务要求会影响到整个流程的顺利进行。

2. **为视频匹配合适的团队配置。** 不要每次任务都重复使用相同的四类配置方案。若音乐视频未配置节奏分析相关配置，其处理结果将会失准；而叙事电影若没有编剧相关配置，生成的场景也会显得逻辑混乱。详情请参阅 `references/role-archetypes.md`。

3. **每个项目对应一个工作空间。** 同一视频的所有配置都会使用相同的 `dir:` 工作空间。各项任务通过共享文件系统以及结构化的交接流程来传递处理结果。**每次**执行 `kanban_create` 操作时，都会传入 `workspace_kind="dir"` 以及 `workspace_path="<项目的绝对路径>"` 这两个参数。

4. **为每个项目设置独立租户。** 应使用针对特定项目的租户标识（即 `--tenant <project-slug>`）。这样做既能确保控制台界面仅显示当前项目的相关内容，又能避免与其他正在处理的任务相互干扰。

5. **充分利用现有技能配置。** 当某个场景适合某种现有的技能配置时，相应的处理工具应通过在其任务中添加 `--skill <name>` 参数，或在其配置文件中设置 `always_load` 选项来加载该技能。无需重复实现该技能已具备的功能。

6. **导演不得直接执行任务。** 即便拥有完整的 `kanban + terminal + file` 工具集，根据 `SOUL.md` 中的规则，导演也不得亲自执行任何任务。其职责仅限于对任务进行分解与分配——每个具体的任务都会转化为针对相应专业配置的 `hermes kanban create` 调用。注入到每个任务处理工具系统提示中的看板编排指南也对这一点作出了进一步说明。

7. **避免过度拆分任务。** 一个时长为30秒的产品视频并不需要20个处理步骤。应尽量构建最小的任务图，同时确保其仍能高效并行执行，并设置适当的人工审核节点。

8. **在启动任务前先验证API密钥。** 外部API（如文本转语音、图像生成、图像转视频功能）需要从`${HERMES_HOME:-~/.hermes}/.env`文件或用户的密钥存储中获取相应的密钥。如果工作节点因缺少密钥而出错，就会浪费一个任务处理资源。设置脚本中的`check_key`辅助函数会在检测到缺失必要密钥时立即终止任务执行。

## 文件结构说明

```
SKILL.md                            ← this file (workflow + rules)
references/
  intake.md                         ← discovery question banks per style
  role-archetypes.md                ← role library (writer, designer, animator, …)
  tool-matrix.md                    ← skill + toolset mapping per role
  kanban-setup.md                   ← setup script structure & profile config
  monitoring.md                     ← watch + intervene patterns
  examples.md                       ← six worked pipelines
assets/
  brief.md.tmpl                     ← brief skeleton
  setup.sh.tmpl                     ← setup script skeleton
  soul.md.tmpl                      ← profile personality skeleton
scripts/
  bootstrap_pipeline.py             ← generate setup.sh from brief + team JSON
  monitor.py                        ← polling + intervention helpers
```
