---
name: git-cherry-pick-squash
description: 当用户需要在当前仓库里按作者筛选跨分支提交、生成 `commits-[YYYYMMDD].md` 清单，并按 STORY 号分组 cherry-pick 到目标分支时使用。默认读取同级 `references/config.json`，同一 STORY 会合并提交，没有 STORY 号的提交保持独立。
---

# 按 STORY 分组 Cherry-pick

这个 skill 用于重复性较高的跨分支 cherry-pick 场景，适合先整理提交清单、再分组应用到当前分支的流程。

先读 [references/usage.md](references/usage.md) 了解命令，再直接修改 [references/config.json](references/config.json)。

## 适用场景

- 用户给出了源分支、起始提交和作者过滤条件。
- 用户要求先生成一份提交清单，再决定如何 pick。
- 用户要求同一个 STORY 下的提交合并为一条提交。
- 用户要求没有 STORY 号的提交保持独立。
- 用户需要在清单里为部分历史提交写入不同的来源分支名。

## 不适用场景

- 用户只需要临时 cherry-pick 一两条提交，不需要生成清单或分组。
- 用户希望 AI 自动解决 cherry-pick 冲突并自行决定保留哪一侧代码。
- 用户的提交信息没有稳定的 STORY 号约定，且也不打算提供自定义 `story_pattern`。

## 快速参考

| 事项 | 默认行为 |
| --- | --- |
| 配置文件 | 读取同级 `references/config.json` |
| 入口脚本 | `bash scripts/init-config.sh` |
| 清单文件 | 默认输出 `commits-[YYYYMMDD].md` |
| STORY 提交 | 合并为 `feat: [STORY#需求号]需求内容` |
| 非 STORY 提交 | 保持独立并沿用原始 commit message |
| 冲突处理 | 脚本立即停止，交给开发人员人工处理 |

## 核心规则

- 生成的清单文件默认命名为 `commits-[YYYYMMDD].md`。
- 同一个 STORY 的提交会并到同一组，组内 cherry-pick 顺序仍然是从旧到新。
- STORY 组的提交标题固定为 `feat: [STORY#{需求号}]{需求内容}`。
- 需求内容优先从该 STORY 组里“带 STORY 号且不是 bug 修复”的标题提取。
- 如果当前清单里找不到可用的需求内容，则标题里的需求内容回退为 `往期需求缺陷修复`。
- 没有识别到 STORY 号的提交不会并组，会保持为独立提交。
- 独立提交默认沿用原始 commit message。

## 工作流

1. 确认目标仓库路径和当前分支。
2. 直接修改同级的 `references/config.json`。
3. 运行 `bash scripts/init-config.sh collect` 生成清单。
4. 检查生成的 `commits-[YYYYMMDD].md` 文件、STORY 分组结果和预览标题。
5. 如果部分历史提交实际属于其他分支链路，把对应 hash 填进 `branch_overrides`。
6. 运行 `bash scripts/init-config.sh apply`。
7. 如果中途出现冲突，脚本必须立即停止，并交给开发人员人工判断和解决；不要让 AI 自行决定保留哪一侧代码。
8. 只有开发人员手工解决冲突并执行 `git cherry-pick --continue` 之后，才可以继续运行：
   `bash scripts/init-config.sh apply --resume`
9. 完成后检查 `git status --short` 和 `git log --oneline --stat -n 5`。

## 常见错误

- 只改了 `source_branch`，但忘了同步更新 `start_commit` 或 `author`，导致清单范围不对。
- 在 `collect` 之后改了 `branch_overrides`，却没有重新执行一次 `collect` 核对清单。
- 冲突发生后没有先执行 `git cherry-pick --continue`，就直接运行 `--resume`。
- 期待脚本自动替开发人员做冲突取舍；这个 skill 不承担这类判断。

## 注意事项

- 脚本会先写清单文件，再执行 cherry-pick。
- 默认会把清单文件排除在最终提交之外。
- 如果同一个 STORY 在时间线上被其他 STORY 的提交穿插，脚本会按“该 STORY 首次出现的位置”建组，并把后续同 STORY 的提交继续并入该组。
- 如果出现冲突，优先由开发人员人工介入；AI 只负责停下来、说明冲突发生了、以及提示后续可选的 `--resume` 流程。

## References

| 文件 | 用途 |
| --- | --- |
| [references/usage.md](references/usage.md) | 命令入口、配置字段和输出说明 |
| [references/config.json](references/config.json) | 默认任务配置模板 |
