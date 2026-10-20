---
name: trellis-flower-update
description: "手动检查和执行单项目或父目录下多个已安装 Flower/Trellis 强化包升级。用于用户明确要求更新或升级 flower-trellis、Flower、Trellis 强化包、skill-garden 快照、项目 flower 版本追平，或自动更新提示被稍后/跳过后仍想在对话里升级时。不要用于用户说想发版、发布版本、release、打 tag、npm publish 或修改 package 版本号；这些属于项目发版流程。"
---

# Trellis Flower Update

用于用户主动要求升级已安装的 Flower/Trellis 强化层时。自动 SessionStart 提示的 snooze、skip 和 cooldown 只是不主动打扰，不能阻止用户显式要求升级。

本 skill 不是发版入口。用户说“我想发版了”、release、打 tag、npm publish、更新 package 版本号或准备发布包时，不使用本 skill；按当前项目的 release SOP 或发布规范处理。

## Workflow

1. 确认范围。单个 Flower 项目使用该项目路径；用户给出父目录并要求批量升级时，先用 `flower-trellis update-all --root <dir> --dry-run` 清点已安装项目，再逐项目核对。批量命令目前会整项目跳过脏 Git、活动任务和非 Git 目录；这些 `skipped` 只是待复核目标，不能直接作为无法升级的结论。
2. 检查 `flower-trellis` 是否可执行。缺失或入口异常且目标项目存在 `.trellis/scripts/flower_update_hook.py` 时，先运行目标项目的检测脚本：`python3 <target>/.trellis/scripts/flower_update_hook.py --bootstrap-only --target <target>`（路径按当前 shell 引用，Python 命令沿用项目配置）。遵循返回的 `<flower-cli-bootstrap>`：先征得当前成员确认，再安装锁定版本并验证；当前对话已授权这次安装时不重复确认。脚本不存在时说明项目缺少安装引导入口，不猜版本安装。未安装成功则停止依赖 CLI 的步骤，不循环追问或安装。
3. CLI 可用后，对每个目标运行人工检查，默认强制刷新远端版本证据：

```bash
flower-trellis self-check --json --manual --force-remote --target <target>
```

4. 解析 JSON：
   - `update_available`：展示当前版本、推荐版本、release notes 摘要和 `commands.recommended`。
   - `project_out_of_sync`：展示当前 Flower/Trellis 与项目记录的差异，并展示 `commands.recommended`。
   - `up_to_date`：说明 CLI 与项目版本记录一致；版本记录不等于受管内容完整性验证。
   - `project_unknown`：说明 CLI 未发现新版，但项目 Flower 版本无法确认。linked worktree 进入 `trellis-worktree` 的 Flower Preparation，通过 `prepare --inherit-flower --source <source>` 补齐可验证记录后重新检查；来源缺失或冲突时如实报告，不推定需要重装。
   - `disabled` / `offline` / `skipped`：说明原因；不要靠重置缓存伪造可执行状态。
5. 写入前遵守确认和安全门槛：
   - 用户已明确要求执行升级时，该授权覆盖所指定范围内的项目，不因每个项目的 `safety.reasons` 重复询问；用户只是询问、查看或比较版本时，只展示结果并等待确认。
   - `safety.reasons` 是自动更新的保守门槛，不等于人工升级的最终结论。`dirty_worktree`、`active_task` 和 `not_git_repo` 均需核对实际影响，不单独阻断升级。批量命令跳过的项目也按此规则逐项处理。
   - 对脏 Git 项目读取精确 dirty 路径，对活动任务定位其任务文件；预演 Trellis 与 Plugin 更新，必要时用 Plugin JSON dry-run 获取目标路径。比较计划写入、删除的文件及目录范围与现有改动的交集。`self-update` 默认向 Trellis 传 `--force`，精确提交和失败备份都不能挽回已被覆盖的本地内容。确认无交集后执行推荐命令，保留原有业务和任务文件；活动任务的存在本身不要求另一次确认。
   - 非 Git 项目若属于用户指定范围，预演并核对升级器备份与恢复能力后可升级；不能用 Git 精确提交验证其结果。有交集、预演失败或内容归属不明时，只停受影响项目，查明具体路径及能否无损保留；无法证明安全则报告真实冲突，不以 `--force` 绕过。
   - CLI 或推荐命令缺失、版本证据不足、Git 状态读取失败等原因仍需按实际原因解决。不要把 `update-all --yes` 的整项目跳过当成全部已处理。
6. 升级后逐项目核对版本与原有改动，分别报告完成项和实际冲突，再处理本地提交：
   - 单项目 `self-update` 返回 `post_action: run_trellis_push_confirmation` 时，按原单项目流程进入 `trellis-push`，展示精确文件与 message 并等待确认。
   - 用户明确要求执行父目录或多个目标的批量升级且未排除提交时，同次授权覆盖升级产物的本地精确提交；`update-all` 的 `post_action: run_flower_batch_commit` 及逐项目补齐的成功结果均由 Flower 批量流程处理，不进入 `trellis-push`，不逐仓重复询问。只检查版本或 dry-run 时不提交。
   - 按所属 Git 仓库收集升级器实际写入的精确路径，结合安装记录、预演结果与升级前状态核对归属；仅提交已证明属于本次升级的路径。逐仓重新核对分支、HEAD、冲突、staged 与文件内容，使用精确路径提交并核对提交文件集；保留其余 staged、未暂存和未跟踪变更，不借升级完成活动任务。无变更、非 Git、detached HEAD、真实路径交集或归属不明的仓库单独待处理，其它独立仓库继续。
   - 批量结果只汇总成功提交数、文件数与待处理原因；用户要求时再展开路径。提交失败不改变升级状态。除非用户另有明确授权，不推送。

## Rules

- 不直接读写 `.flower/update-check.tmp`。
- 无论远端查询结果如何，都单独说明 `project.flowerVersionStatus=unknown`；不得用本机 CLI 版本替代项目安装证据。
- 不使用 `update-check reset`、`snooze` 或 `skip` 作为升级绕过手段。
- 不运行 `npm run release`、不打 tag、不 publish，也不修改 `package.json` 版本号。
- 不把 `self-check --manual` 用在 SessionStart 自动 hook；自动路径必须继续尊重提示节流。
- 只在将覆盖现有内容、实际授权不足或证据无法核实时停下受影响项目；不得因为整个工作区脏或存在活动任务而跳过其它可安全升级的项目。
