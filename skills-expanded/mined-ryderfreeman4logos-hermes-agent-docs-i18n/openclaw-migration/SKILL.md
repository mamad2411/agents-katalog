---
name: openclaw-migration
description: Import an OpenClaw setup (memories, skills) into Hermes.
version: 1.0.0
author: Hermes Agent (Nous Research)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Migration, OpenClaw, Hermes, Memory, Persona, Import]
    related_skills: [hermes-agent]
---

# OpenClaw -> Hermes 迁移

当用户希望将现有的 OpenClaw 配置迁移到 Hermes Agent，且尽量减少手动整理工作量时，可使用此技能。

## CLI 命令

如需快速、无需交互式的迁移，可使用内置的 CLI 命令：

```bash
hermes claw migrate              # Full interactive migration
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
hermes claw migrate --source /custom/path/.openclaw  # Custom source
```

该 CLI 命令会运行下文所述的相同迁移脚本。当您需要一种交互式、引导式的迁移方式，并且希望获得试运行预览及针对每个项目的冲突解决功能时，可通过代理使用此技能。

**首次设置：** `hermes setup` 向导会自动检测 `~/.openclaw` 目录，并在配置开始前提供迁移选项。

## 该技能的功能

它通过 `scripts/openclaw_to_hermes.py` 文件来实现以下功能：

- 将 `SOUL.md` 文件导入 Hermes 主目录，保留原文件名；
- 将 OpenClaw 的 `MEMORY.md` 和 `USER.md` 文件转换为 Hermes 对应的内存条目；
- 将 OpenClaw 中的命令审批规则合并到 Hermes 的 `command_allowlist` 中；
- 迁移与 Hermes 兼容的消息设置，如 `TELEGRAM_ALLOWED_USERS`，同时将 OpenClaw 的工作区设置映射为 Hermes 的工作目录配置；
- 将 OpenClaw 的各类技能复制到 `~/.hermes/skills/openclaw-imports/` 目录下；
- 可选地将 OpenClaw 的工作区说明文件复制到用户指定的 Hermes 工作区中；
- 将兼容的工作区资源（如 `workspace/tts/` 目录下的文件）复制到 `~/.hermes/tts/` 目录下；
- 对那些没有直接对应 Hermes 存储路径的非机密文档进行归档处理；
- 生成一份结构化的报告，列出已迁移的项目、存在的冲突、被跳过的项目及其原因。

## 路径说明

该辅助脚本位于以下路径：

- `scripts/openclaw_to_hermes.py`

若通过 Skills Hub 安装此技能，其标准路径为：

- `~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py`

请勿尝试使用如 `~/.hermes/skills/openclaw-migration/...` 这类简写路径。

在运行该辅助工具之前：

1. 建议优先使用位于 `~/.hermes/skills/migration/openclaw-migration/` 下的已安装路径。
2. 若该路径不可用，请检查已安装的技能目录，并根据其中的 `SKILL.md` 文件确定脚本的相对位置。
3. 仅当安装位置缺失或技能被手动移动时，才可将 `find` 命令作为备用方案。
4. 调用终端工具时，切勿传入 `workdir: "~"` 参数。应使用用户的主目录等绝对路径，或直接省略 `workdir` 参数。

若使用 `--migrate-secrets` 参数，该工具还会导入一组经过筛选的、兼容 Hermes 的密钥，目前包括：
- `TELEGRAM_BOT_TOKEN`

## 默认工作流程

1. 首先通过试运行进行检测。
2. 提供简要总结，说明哪些内容可以迁移、哪些无法迁移，以及哪些内容将被归档。
3. 若有 `clarify` 工具可用，应优先使用它来辅助用户做出决策，而非要求用户以自由文本形式回复。
4. 若试运行发现已安装的技能目录存在冲突，请在执行操作前询问用户应如何处理这些冲突。
5. 在执行操作前，让用户从两种支持的迁移模式中选择一种。
6. 仅当用户希望将工作空间配置文件一并迁移时，才要求其输入目标工作空间路径。
7. 使用相应的预设参数和标志来执行迁移操作。
8. 对迁移结果进行总结，重点包括：
   - 已迁移的内容
   - 被归档以供人工审核的内容
   - 被跳过的内容及其原因

## 用户交互协议

Hermes CLI 支持使用 `clarify` 工具来进行交互式提示，但其功能较为有限：

- 每次仅可选择一个选项  
- 预定义选项最多为4个  
- 自动提供“其他”这一自由文本选项  

该系统**不支持**在单个提示中实现真正的多选复选框功能。  

对于每一次`clarify`调用：  
- 必须包含一个非空的`question`  
- 仅在实际可选择的提示中才需提供`choices`  
- `choices`中的选项应为2到4个普通字符串  
- 绝不可出现占位符或截断后的选项，如`...`  
- 绝不可通过额外空格来填充或格式化选项  
- 绝不可在问题中加入虚假的表单字段，例如“在此输入目录路径”、供填写的空行或下划线`_____`  
- 对于开放式的路径查询，只需提出简单句子；用户可在面板下方的常规CLI提示框中输入内容  

如果`clarify`调用返回错误，请检查错误信息，修正数据内容，然后使用有效的`question`和干净的选项重新尝试一次。  

当`clarify`功能可用且试运行结果显示需要用户做出决策时，您的**下一个操作必须是调用`clarify`工具**。  
切勿以常规的助手回复结束当前轮次，例如：  
- “让我为您列出可选选项”  
- “您想怎么做？”  
- “以下是可选选项”  

如果需要用户做出决策，请先通过`clarify`获取选择结果，然后再继续生成文字内容。  
若仍有多个未解决的决策问题，切勿在这些问题之间插入解释性信息。收到一次`clarify`响应后，您的下一个操作通常应是再次进行必要的`clarify`调用。  

每当试运行报告出现以下情况时，均应将`workspace-agents`视为一个未解决的决策问题。

- `kind="workspace-agents"`  
- `status="skipped"`  
- 原因中包含“未指定工作空间目标”  

在这种情况下，您必须在执行前询问相关的工作空间操作说明，切勿擅自将其视为跳过操作的决策。  

由于存在此类限制，建议采用以下简化的决策流程：

1. 对于 `SOUL.md` 文件中的冲突，可使用 `clarify` 命令，并从以下选项中选择：
   - `保留现有内容`
   - `用备份覆盖`
   - `先进行审查`
2. 如果试运行结果显示存在一个或多个 `kind="skill"` 且 `status="conflict"` 的条目，则可使用 `clarify` 命令，并从以下选项中选择：
   - `保留现有的技能`
   - `用备份覆盖有冲突的技能`
   - `将有冲突的技能导入到重命名的文件夹中`
3. 对于工作空间相关指令，可使用 `clarify` 命令，并从以下选项中选择：
   - `跳过工作空间指令`
   - `复制到工作空间路径`
   - `稍后决定`
4. 如果用户选择复制工作空间指令，则需进一步提出一个开放式的 `clarify` 问题，要求提供**绝对路径**。
5. 如果用户选择“跳过工作空间指令”或“稍后决定”，则无需使用 `--workspace-target` 参数即可继续操作。
6. 对于迁移模式，可使用 `clarify` 命令，并从以下三个选项中选择：
   - `仅迁移用户数据`
   - `完全兼容的迁移`
   - `取消`
7. “仅迁移用户数据”意味着：迁移用户数据及兼容的配置，但**不**导入已列入白名单的机密信息。
8. “完全兼容的迁移”意味着：迁移相同且兼容的用户数据，同时如果存在的话也会一并迁移已列入白名单的机密信息。
9. 如果无法使用 `clarify` 命令，则需以普通文本形式提出相同的问题，但回答仍需限制在“仅迁移用户数据”、“完全兼容的迁移”或“取消”之中。

执行关卡：

- 在因“未提供工作空间目标”而导致的 `workspace-agents` 跳过机制仍未解决时，不得执行任务。
- 解决该问题的有效方式仅有以下几种：
  - 用户明确选择“跳过工作空间指令”；
  - 用户明确选择“稍后决定”；
  - 用户在选择“复制到工作空间路径”后提供具体的工作空间路径。
- 在试运行阶段未指定工作空间目标，并不意味着有权执行任务。
- 只要任何必要的“确认”决策仍未解决，也不得执行任务。

以下即为默认的 `clarify` 请求格式，请严格使用：

- `{"question":"您现有的 SOUL.md 文件与导入的文件存在冲突，我该如何处理？","choices":["保留现有文件","用备份文件覆盖","先进行审查"]}`
- `{"question":"Hermes 中已存在一个或多个导入的 OpenClaw 技能，面对这些技能冲突应如何处理？","choices":["保留现有技能","用备份文件覆盖冲突的技能","将冲突的技能导入到重命名的文件夹中"]}`
- `{"question":"请选择迁移模式：仅迁移用户数据，还是执行包含允许列表内机密的完整兼容性迁移？","choices":["仅迁移用户数据","完整兼容性迁移","取消"]}`
- `{"question":"您是否要将 OpenClaw 的工作空间指令文件复制到 Hermes 工作空间中？","choices":["跳过工作空间指令","复制到工作空间路径","稍后决定"]}`
- `{"question":"请提供用于复制工作空间指令的绝对路径。"}`

## 决策与指令映射关系

需将用户的选项与对应的命令参数精确对应：

- 若用户选择对 `SOUL.md` 采用“保留现有内容”选项，则**不得**添加 `--overwrite` 参数。
- 若用户选择“用备份覆盖”，则需添加 `--overwrite` 参数。
- 若用户选择“先预览”，则在执行前暂停并让用户查看相关文件。
- 若用户选择“保留现有技能”，则需添加 `--skill-conflict skip` 参数。
- 若用户选择“用备份覆盖冲突的技能”，则需添加 `--skill-conflict overwrite` 参数。
- 若用户选择“将冲突的技能导入到重命名的文件夹中”，则需添加 `--skill-conflict rename` 参数。
- 若用户选择“仅迁移用户数据”，则需使用 `--preset user-data` 参数执行，且**不得**添加 `--migrate-secrets` 参数。
- 若用户选择“完全兼容的迁移方式”，则需使用 `--preset full --migrate-secrets` 参数执行。

仅当用户明确提供了完整的workspace路径时，才添加 `--workspace-target` 参数。若用户选择“跳过workspace相关设置”或“稍后决定”，则不得添加 `--workspace-target` 参数。

在执行前，需用通俗的语言再次说明具体的操作步骤，并确保其与用户的选项完全一致。

## 执行后的报告规则

执行完成后，应以脚本生成的JSON输出作为唯一真实依据。

1. 所有统计数值均需基于 `report.summary` 中的数据。
2. 仅当某项的 `status` 值确切为 `migrated` 时，才将其列在“已成功迁移”列表中。
3. 除非报告显示该项的状态为 `migrated`，否则不得声称冲突已被解决。
4. 除非 `kind="soul"` 类型的项目在报告中显示 `status="migrated"`，否则不得声明 `SOUL.md` 已被覆盖。
5. 如果 `report.summary.conflict > 0`，应列出冲突信息，而非默认视为处理成功。  
6. 若计数结果与列出的项目不一致，请在回复前修正列表，使其与报告内容相符。  
7. 如报告中有 `output_dir` 路径，应一并提供，以便用户查看 `report.json`、`summary.md`、备份文件及归档文件。  
8. 若因内存或用户配置空间不足而需处理，除非报告中明确指出了归档路径，否则不得声称相关条目已被归档。如果存在 `details.overflow_file`，则应说明完整的溢出列表已导出至该文件。  
9. 若某个技能被导入到重命名的文件夹中，应说明其最终存储位置，并提及 `details.renamed_from`。  
10. 若报告中含有 `report.skill_conflict_mode`，应以该值为依据来确定所选的导入技能冲突处理策略。  
11. 若某条目的状态为 `status="skipped"`，不得将其描述为已被覆盖、备份、迁移或已解决。  
12. 若 `kind="soul"` 且状态为 `status="skipped"`，原因是“目标与源内容已一致”，则应说明该条目保持不变，无需提及备份。  
13. 若重命名的导入技能的 `details.backup` 为空，不得暗示原有的 Hermes 技能已被重命名或备份。只需说明导入的副本已存放在新位置，并引用 `details.renamed_from` 表示仍保留在原处的原有文件夹。  

## 迁移预设选项

在常规使用中，建议优先选择以下两种预设：  
- `user-data`  
- `full`  

`user-data` 包含：

- `soul`  
- `workspace-agents`  
- `memory`  
- `user-profile`  
- `messaging-settings`  
- `command-allowlist`  
- `skills`  
- `tts-assets`  
- `archive`  

“完整”模式包含 `user-data` 中的所有内容，此外还包括：  
- `secret-settings`  

该辅助脚本仍支持按类别设置 `--include` / `--exclude` 参数，但将其视为高级备用功能，而非默认的用户体验方式。  

## 命令  

执行完整检测的模拟运行：

```bash
python ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py
```

在使用终端工具时，建议采用如下这种绝对路径调用方式：

```json
{"command":"python /home/USER/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py","workdir":"/home/USER"}
```

使用用户数据预设进行模拟运行：

```bash
python ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --preset user-data
```

执行用户数据迁移：

```bash
python ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --execute --preset user-data --skill-conflict skip
```

执行完全兼容的迁移操作：

```bash
python ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --execute --preset full --migrate-secrets --skill-conflict skip
```

按照包含工作区相关指令的方式执行：

```bash
python ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --execute --preset user-data --skill-conflict rename --workspace-target "/absolute/workspace/path"
```

默认情况下，请勿将 `$PWD` 或用户主目录设置为工作空间目标，应先明确询问用户的工作空间路径。

## 重要规则

1. 除非用户明确要求立即执行，否则应在实际写入前先进行试运行。
2. 默认情况下不要迁移机密信息。令牌、认证数据块、设备凭证以及原始网关配置均不应被导入 Hermes，除非用户明确要求迁移机密信息。
3. 除非用户明确希望如此，否则切勿默默覆盖非空的 Hermes 目标。若启用了覆盖功能，辅助脚本会保留原有备份。
4. 始终需向用户提供已跳过项目的报告。该报告是迁移流程的必要组成部分，而非可选附加项。
5. 应优先使用主 OpenClaw 工作空间（`~/.openclaw/workspace/`），而非 `workspace.default/`。仅当主工作空间中的文件缺失时，才将默认工作空间作为备用。
6. 即使处于机密信息迁移模式，也仅能在目标 Hermes 环境正常的情况下迁移机密信息。不支持的认证数据块仍需被标记为已跳过。
7. 若试运行显示有大量资产需要复制、存在冲突的 `SOUL.md` 文件或内存条目已满，应在执行前分别指出这些问题。
8. 若用户不确定，应默认仅迁移“用户数据”。
9. 仅当用户明确提供了目标工作空间路径时，才包含 `workspace-agents` 目录。
10. 将基于类别的 `--include` / `--exclude` 参数视为高级应急手段，而非常规操作流程。
11. 若支持`clarify`功能，切勿在试运行总结时使用含糊的“您想做什么？”这类表述，而应采用结构化的后续提示语。  
12. 当可以使用明确的选项式提示时，不要使用开放式的`clarify`提示。应优先提供可选选项，仅在需要输入绝对路径或文件审核请求时才允许使用自由文本输入。  
13. 试运行结束后，若仍有未解决的决策问题，切勿仅做总结便停止操作。对于优先级最高的阻塞性决策，应立即使用`clarify`功能进行处理。  
14. 后续问题的处理优先级如下：  
    - `SOUL.md`冲突  
    - 导入的技能冲突  
    - 迁移模式  
    - 工作区指令的目标位置  
15. 不要在同一条消息中承诺稍后会提供选项，而应通过实际调用`clarify`功能来呈现这些选项。  
16. 在得到迁移模式答案后，需明确检查`workspace-agents`问题是否仍未解决。若仍有未解决问题，下一步操作必须是调用`workspace-instructions`的`clarify`功能。  
17. 在收到任何`clarify`的回答后，若仍有其他需要决策的问题，切勿复述刚刚做出的决定，而应立即提出下一个需要解答的问题。
