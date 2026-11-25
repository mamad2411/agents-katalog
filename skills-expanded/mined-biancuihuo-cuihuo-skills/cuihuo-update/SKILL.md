---
name: cuihuo-update
description: 更新官方 cuihuo-skills（淬火包），清理已下线的旧官方入口，同时完整保留用户的本地存档、其他 Skill 和 .cuihuo/local.yaml 本地配置。当用户要求更新、升级、检查淬火包版本，或在更新提醒后紧接着回复 1 时使用。
metadata:
  cuihuo-handoff: |
    - 用户要求更新或升级淬火包，或在上一条更新提醒后单独回复 1 → 执行官方仓库更新、清理下线旧官方入口并刷新版本检查时间戳
    - 用户只问当前版本或更新内容，未要求立即安装 → 说明版本状态，不执行安装命令
    - 不交出：更新第三方其他 Skill、删除用户存档或 .cuihuo/local.yaml 配置、自动创建定时任务
---

# cuihuo-update：更新淬火包

当用户明确要求更新 `cuihuo-skills`，或在上一条回复末尾明确包含淬火包更新提醒、用户紧接着单独回复 `1` 时，直接执行更新，不做二次口头确认。

## 更新边界

- 只更新官方仓库 `Biancuihuo/cuihuo-skills`；
- 完整保留用户的 `~/.cuihuo/` 与工作区 `.cuihuo/local.yaml`、学习讲义、测评报告、圆桌合辑和决策卡；
- 不使用 `npx skills update`（会误更新其他作者的 Skill）；
- 清理已下线旧入口时，只清理能确认指向旧官方版本的失效链接或目录，并先备份到 `~/.cuihuo/retired-skills/<时间>/`；用户自改的目录一律保留。

## 执行步骤

1. **检测安装方式**：
   - 若本 Skill 位于本地 Git 克隆仓库内（存在 `../../.claude-plugin/marketplace.json` 和 `../../.git`）：在仓库根目录确认工作区干净后执行 `git pull --ff-only`；若工作区有未提交本地改动，先提示用户保存或提交，不强行覆盖。
   - 若通过 Claude Code 插件安装：执行 `claude plugin marketplace update cuihuo-skills` 并更新已安装的 `@cuihuo-skills` 插件。
   - 其余情况（Skills CLI 全局安装或未知方式）：执行：
     ```bash
     npx -y skills add Biancuihuo/cuihuo-skills -g --all
     ```
2. **清理已下线旧官方入口**：
   解析本 Skill 目录绝对路径，运行：
   ```bash
   python3 "<本 Skill 目录>/scripts/cleanup_retired_skills.py"
   ```
   脚本依据 [references/retired-skills.json](references/retired-skills.json) 安全检查各 Agent 目录下的旧入口，仅移除失效链接或旧官方副本（并备份），绝不误删用户自有文件。
3. **刷新版本检查时间戳**：
   ```bash
   mkdir -p "$HOME/.cuihuo" && date +%s > "$HOME/.cuihuo/update_check_at"
   ```
4. **回报结果**：
   - 成功：说明更新渠道，并提醒「新建一次对话后即可加载新版能力」（如有清理旧入口，列出备份路径）。
   - 失败：用一句话交代具体原因（如网络、权限或本地有未提交改动）与下一步处理方式，不刷屏贴完整终端日志。

完成当前任务后直接结束。如果发现超出本工具范围的下一步需求，用一句话说明还需要哪种能力；当前环境已安装 `/cuihuo` 时，提示可直接输入 `/cuihuo` 由总调度台匹配。
