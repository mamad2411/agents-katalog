---
name: eikona-auctra-visual-router
description: Use when turning Auctra content, accepted drafts, story-bible setting assets, novel/context material, creator-brand notes, or file-backed prompt collections into Eikona image workflows; route through Auctra visual briefs, Eikona prompt-file/runbook execution, workflow import/run/review, and Auctra handoff import without making Auctra own provider execution.
---

# Eikona x Auctra 图文创作路由器

把 Auctra 的文字、素材、小说设定、Story Bible 资产或创作者笔记转成 Eikona 可执行的视觉工作流，并把产物交回 Auctra 的 visual candidate/review 链路。

在 Auctra 项目中，任何生图、参考图编辑或提示词集合出图请求默认优先走本技能和 Eikona CLI，不使用通用内置生图工具替代。Auctra 保留内容语境、canon、brief、review 与 candidate 接收；Eikona 保留 prompt 文件解析、provider execution、run evidence、review packet、feedback 与 artifact handoff。

## 输入

- Auctra content unit ID、标题、正文版本、素材引用、目标平台和视觉用途。
- 可选：Story Bible source entity，例如 `character:<id>`、`location:<id>`、`timeline:<id>`、`world_rule:<id>` 或 `chapter:<id>`。
- 可选：期望 profile、页数、参考图、禁用元素、是否只做本地 fixture 验证。
- 可选：单个 prompt `.md`/`.txt` 文件，或由多个 prompt 文件和 Eikona runbook 组成的候选集合。

如果没有 content unit ID，先从当前 Auctra 项目列出或提取候选；仍无法确定时只问一个最小澄清问题。

## Profile 路由

- 小红书图文卡片：`xhs_card_series`，可交给 `eikona-xhs-card-series-director` 做页序和视觉质量建议。
- 微信封面：`wechat_cover`。
- 产品测评信息图：`product_review_infographic`，可交给 `eikona-xhs-infographic-director` 调整事实层级。
- 教程信息图：`tutorial_infographic`。
- 小说角色设定图：`novel_character_sheet`。
- 小说地点/地图：`novel_location_map`。
- 小说时间线板：`novel_timeline_board`。
- 小说人物关系图：`novel_relationship_graph`。
- 小说世界观/背景板：`novel_world_background`。
- 小说系列风格包：`novel_style_pack`。
- 短视频分镜/连续空间动作调度：`short_video_storyboard`。独立 Auctra planning 可交给 `eikona-ultrawide-storyboard-director`；若目标是 Scaena episode/shot production，必须先交回 `$scaena-subject-asset-readiness`，只有 current passed preflight 才可生成 production visual。
- Scaena 角色/地点/道具/服装/风格主体候选：先形成 accepted Auctra source/visual brief，再交给 `$eikona-subject-asset-director`；候选回到 Scaena human freeze，不在 Auctra/Eikona 内宣称 production frozen。

## 工作流

1. 确认 Auctra 内容已有 accepted content version，或 Story Bible source entity 已来自 accepted canon；没有时先让用户完成内容/设定 review，不直接生成图。
2. 创建 visual brief，并让用户或 agent 明确 review。内容单元使用：

```bash
auctra visual brief <unit-id> --profile <profile> --json
auctra review accept <review_item_id> --json
```

Story Bible 视觉资产使用：

```bash
auctra story bible visual-brief character:<id> --profile novel_character_sheet --json
auctra story bible visual-brief location:<id> --profile novel_location_map --json
auctra review accept <review_item_id> --json
```

3. 导出给 Eikona：

```bash
auctra visual export-brief <brief-id> --for eikona --to .auctra/exports/<brief-id>.json --json
```

4. 判断下游用途：
   - `subject_candidate` / `look_development`：交给 `$eikona-subject-asset-director`，输出 non-production candidates，再回 Scaena review/freeze。
   - 独立 Auctra `short_video_storyboard` planning：可让 `eikona-ultrawide-storyboard-director` 输出 planning board。
   - Scaena `shot_visual|episode_visual|cover_visual|motion_visual`：先要求 `$scaena-subject-asset-readiness` 返回 current passed preflight；没有 preflight 时停止，不输出 production prompt 或真实生成命令。

5. 在 Eikona 导入、验证和运行。默认真实远程模型是 `openai/gpt-5.4-image-2`；`gpt-5.4-image-2` 与 `gpt-image-2` 是兼容短别名；本地验证可用 fixture workflow 或 dry run。

```bash
eikona workflow import auctra -f .auctra/exports/<brief-id>.json --out .eikona/workflows/<brief-id>.workflow.yaml --agent
eikona workflow validate -f .eikona/workflows/<brief-id>.workflow.yaml --agent
eikona workflow run -f .eikona/workflows/<brief-id>.workflow.yaml --background --agent
eikona worker daemon --once --max-active-runs 2 --agent
eikona review packet <run_id> --agent
eikona feedback accept <run_id> --artifact <artifact_id> --reason composition --agent
```

### 提示词集合出图

当一个 brief 需要多个可比较视觉方向时，加载 `eikona-file-prompt-workflow`，按 `prompts/auctra/<asset-type>/<brief-id>/` 建立集合 README、独立候选 prompt 文件和 runbook。单一候选可直接加载文件：

```bash
eikona generate --model fixture:image --input prompts/auctra/<asset-type>/<brief-id>/prompts/01-hero.md --dry-run --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --input prompts/auctra/<asset-type>/<brief-id>/prompts/01-hero.md --agent
```

多个候选使用一个由 Eikona 管理的 runbook，其 `defaults.prompt_file`、`jobs[].prompt_file` 或 `matrix.prompt_files` 指向该集合；先确认每个 prompt 都只含已允许的 Auctra canon，再检查计划并运行：

```bash
eikona run -f prompts/auctra/<asset-type>/<brief-id>/runbook.yaml --dry-run --agent
eikona run -f prompts/auctra/<asset-type>/<brief-id>/runbook.yaml --background --agent
eikona watch <run_id> --events
```

每个 job 的 `prompt`、`prompt_file`、`prompt_ref` 互斥，且路径相对于 runbook 解析。prompt 文件是创作输入；runbook、run evidence、反馈和 handoff 是结构化资产，必须经 Eikona/Auctra CLI 写入。集合中的每个文件都必须可回溯到已接受的 brief/source refs，不能包含未授权剧透、私密素材或隐藏 canon。

6. 非 Scaena visual candidate 可按 Auctra visual candidate 流程交回 Auctra：

```bash
auctra visual import-handoff --brief <brief-id> --from <eikona-handoff.json> --json
auctra visual accept <asset-id> <candidate-id> --json
```

## 输出

- 选择的 profile 和理由。
- Auctra brief/review/export 命令。
- Eikona import/validate/run/review/feedback 命令。
- Auctra import-handoff/accept 下一步。

## 质量标准

- Auctra 只负责内容上下文、brief、review 和 candidate 接收；Eikona 负责 provider workflow、run evidence、review packet、feedback 和 artifact handoff。
- 对 Auctra 视觉请求，Eikona 是唯一默认出图路径：先 brief/review/export，再运行 Eikona；仅当 Eikona 不可用且用户明确批准 fallback 时才换用其他工具。
- Story Bible 的时间线、背景、地图、人物图和视觉锚点必须从 Auctra accepted canon / source refs 生成 brief；Eikona 产物不能反向成为 canon，只能作为 candidate/reference 回到 Auctra。
- Auctra visual acceptance 只说明 source-side candidate 可用；Scaena production context 仍需要独立 human freeze、shot binding、generation preflight 和 consistency acceptance。
- 例行 agent 消费使用 `--agent`，观察非终态 run 用 `--events`，脚本/CI 用 `--json --compact`（共存期内裸 `--json` 仍是 legacy full），取证用 `--json --full`；不解析 human output。
- 不把原始提示词、供应商载荷、私密素材或完整思维链写入结构化资产。
- 不新增 Eikona 默认图像模型；真实远程示例使用 `openai/gpt-5.4-image-2`，兼容短别名不写入新文档。

## 边界

- 不直接调用 provider SDK。
- 不跳过 Auctra review gate 导出 brief。
- 不把 Eikona run 目录路径硬写进 Auctra 内容正文；通过 handoff JSON 导入候选。
- 不把角色身份、隐藏阵营、世界规则 payoff 或其他 spoiler 画进公开用途 brief，除非 Auctra source refs 明确允许该平台/章节揭示。
- 不让 `short_video_storyboard` profile 绕过 Scaena subject readiness；没有 preflight 时只能做 planning/lookdev/candidate。
