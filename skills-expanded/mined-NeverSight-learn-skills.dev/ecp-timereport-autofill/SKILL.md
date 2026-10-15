---
name: ecp-timereport-autofill
description: 从 release 分支的当日 Git 提交自动生成并可提交 ECP 工时日志。用于“每天自动填工时”“按提交描述回填工时”“定时自动写入 ECP 工时日志”等场景。
---

# ECP Timereport 自动填报

从 `springcloud-aile` 与 `AuthServer\authserver` 的 release 分支提取当天提交描述，自动生成并可提交到 ECP 工时日志。

## 安装后先配置

1. 双击 `configure-ecp-timereport.cmd`（快捷方式）或运行 `python scripts/configure_timereport.py --interactive`。
2. 将以下变量写入 `config/timereport-config.json`（不再强依赖环境变量）：
   - 本地项目映射（`name + path`，支持多个）
   - ECP 账号/密码
   - 可选的 timereport 扩展项（总工时、Git 作者过滤、输出目录等）
3. 首次保存配置时，会自动记录当前设备指纹到 `device_binding`。
4. 后续可重复运行快捷脚本随时更新。

## 对话式补配置流程

当用户说“填写今日工时”“提交今天工时”“补工时”等，需要按下面流程强制执行：

1. 先运行 `python scripts/configure_timereport.py --show-required-status` 检查必填配置状态。
2. 如果 `ready=true`，再继续执行填报脚本。
3. 如果 `ready=false` 且 `binding_issue` 为 `missing_fingerprint` 或 `fingerprint_mismatch`，则不要询问“恢复还是重配”，必须直接进入“重新配置”流程。
4. 如果 `ready=false` 且没有 `binding_issue`，不要直接结束，也不要立刻自动恢复配置。
5. 只有在“没有 binding_issue、只是缺少必填字段”时，才先向用户确认：是“从最近一次工时报告恢复可恢复的配置”，还是“重新配置”。
6. 如果用户选择“从最近报告恢复”：
   - 先从最近一次成功的 timereport 报告中恢复可推断的项目路径配置。
   - 恢复后重新运行 `python scripts/configure_timereport.py --show-required-status`。
   - 对仍缺失的字段，再在当前对话里继续索取，只问仍缺失的用户可理解信息项。
7. 如果进入“重新配置”：
   - 必须在当前对话里主动向用户索取缺失字段，只问仍缺失的用户可理解信息项。
   - 本地仓库的项目地址：格式为 `name=path;name=path`
   - ECP 账号
   - ECP 密码
8. 收到用户输入后，立即运行 `python scripts/configure_timereport.py` 把值写回 `config/timereport-config.json`。
9. 写回后再次运行 `python scripts/configure_timereport.py --show-required-status`。
10. 只有当 `ready=true` 时，才能继续执行 `python scripts/fill_timereport.py --submit ...`。

对话约束：

- 优先用当前对话补配置，不把责任推回给用户手动执行脚本。
- 如果存在 `binding_issue`，直接走重新配置，不再询问“从最近报告恢复”还是“重新配置”。
- 只有在没有 `binding_issue` 且只是缺少普通字段时，才先问用户“从最近报告恢复”还是“重新配置”。
- 每次只问缺失项，不重复索取已有值。
- 如果能从最近一次 timereport 报告或当前工作区推断出项目路径，可先复用，再只向用户问剩余缺项。
- 写入配置后，在继续填报前要向用户简短说明“配置已补齐，继续提交工时”。
- 对用户提问时，不直接使用 `projects`、`ecp.username`、`ecp.password` 这类配置 key，而是用自然话术表达。

推荐对话顺序：

1. 先明确告知用户当前一共缺少几项配置。
2. 列出缺失信息的自然语言名称，让用户知道接下来会补哪些内容。
3. 如果存在 `binding_issue`，直接说明“检测到当前设备标识变化，需要重新配置”，然后进入逐项提问。
4. 如果不存在 `binding_issue`，再询问用户是“从最近报告恢复”还是“重新配置”。
5. 如果进入重新配置流程，必须一项一项单独提问并等待用户回复，不要把所有字段一次性抛给用户。
6. 每拿到一项值后，先简短确认这一项已记录，再继续问下一项。
7. 所有缺失项收集完成后，再统一写入配置并继续提交流程。

推荐话术：

- 开场先说：`当前检测到 3 项配置缺失，需要补齐后才能继续填工时。`
- 然后说：`目前缺少的信息是：本地仓库的项目地址、ECP 账号、ECP 密码。`
- 如果存在指纹问题，直接说：`检测到当前设备标识发生变化，需要重新配置这些信息后才能继续填工时。`
- 只有在没有指纹问题时，才问选择：`你希望我从最近报告恢复可恢复配置，还是重新配置？`
- 如果用户选择重新配置，逐项提问：
  - `第 1 项是本地仓库的项目地址，请发我项目路径映射，格式为 name=path;name=path。`
  - `第 2 项是 ECP 账号，请发我登录账号。`
  - `第 3 项是 ECP 密码，请发我登录密码。`
- 每项收到后给简短确认：
  - `本地仓库的项目地址已记录。`
  - `ECP 账号已记录。`
  - `ECP 密码已记录。`

## 填报规则（已内置）

1. 仅对中国大陆法定工作日（含调休）执行填报，节假日/休息日不填。
2. 当天有多条提交时，仅取最早的一条提交描述作为当日工时描述。
3. 当天无提交时，自动在临近日期中查找“多条提交”的日期，并优先选取尚未被填写过的那条提交记录。
4. 若临近日期不存在“多条提交”或这些记录都已被填写过，则当天先不填，等下一次执行时再重新判断；仅在月末补齐时才使用模糊话术自动填报（如：优化相关代码、调整相关业务逻辑、配合前端调整接口）。
5. 当天执行 `--submit` 时，会自动检查当月过去工作日是否缺失并补齐；如果使用了 `--activity-detail` 手动指定休假/会议，则只处理目标日期，不触发整月补齐。
6. `--activity-type 休假 --activity-detail 特休假` 会生成 `休假-特休假` 描述，且不关联任务。
7. `--activity-type 会议 --activity-detail 顾问会议` 会生成 `会议-顾问会议` 描述，且保持任务关联。
8. 工时明细进度百分比统一写入 `100%`（当月首个工作日及后续工作日均一致）。
9. 触发 skill 时会先校验 `device_binding.fingerprint`；若缺失或与当前设备不一致，会自动清空配置文件中的业务变量，只保留当前设备指纹和空白必填项，然后必须按“对话式补配置流程”直接进入“重新配置”分支，不再先询问“从最近报告恢复”还是“重新配置”。

## 工作流程

1. 读取 `config/timereport-config.json` 中的本地项目映射与 ECP 参数。
2. 登录 ECP 后先调用 `Ecp.Aile.getOnlineUser` 获取当前 `userId`。
3. 再调用 `Ecp.TimeReport.getAllRelevantObjs` 自动匹配当月任务 `taskId`。
4. 若必填配置缺失，先按“对话式补配置流程”补齐配置，再继续。
5. 运行 `scripts/fill_timereport.py`，从 release 分支提取当天提交并生成工时内容。
6. 检查 `timereport-reports/` 下生成的 JSON 报告。
7. 使用 `--submit` 写入 ECP 工时日志。

## 跨设备保护流程

1. skill 首次配置成功后，会把当前设备指纹写入 `config/timereport-config.json` 的 `device_binding`。
2. 每次运行 `scripts/fill_timereport.py` 前，都会校验该指纹。
3. 若发现指纹缺失或与当前设备不一致，脚本会自动清空配置中的业务变量。
4. 此时不能直接终止，也不要再询问“从最近报告恢复”还是“重新配置”。
5. 必须直接通过当前对话重新补全本地仓库的项目地址、ECP 账号、ECP 密码。
6. 收到用户输入后，运行 `python scripts/configure_timereport.py` 把新值写回配置，脚本会把新设备指纹重新写入配置。

## 命令示例

```bash
# 仅生成，不提交
python scripts/fill_timereport.py

# 指定日期
python scripts/fill_timereport.py --date 2026-03-11 --branch release

# 指定休假（不关联任务）
python scripts/fill_timereport.py --date 2026-03-13 --activity-type 休假 --activity-detail 特休假 --submit

# 指定会议（关联任务）
python scripts/fill_timereport.py --date 2026-03-16 --activity-type 会议 --activity-detail 顾问会议 --submit

# 提交到 ECP（默认 8 小时）
python scripts/fill_timereport.py --submit

# 指定配置文件
python scripts/fill_timereport.py --config .\config\timereport-config.json --submit

# 快速修改配置（命令行）
python scripts/configure_timereport.py --projects "project-a=/path/to/project-a;project-b=/path/to/project-b" --username "your-username" --password "your-password"
```

## 配置来源优先级

- 首选：`config/timereport-config.json`
- 兼容：命令行参数（最高优先级）和历史环境变量（兜底）

## 失败处理

- 指定日期无提交时，会尝试“临近多提交”或“月末模糊补齐”策略。
- 当天已有工时明细时，默认终止；加 `--allow-overwrite` 才继续。
- ECP 接口报错时保留 JSON 报告并返回非 0 退出码。

## 参考

- 见 `references/setup.md`（环境配置与自动化模板）。
