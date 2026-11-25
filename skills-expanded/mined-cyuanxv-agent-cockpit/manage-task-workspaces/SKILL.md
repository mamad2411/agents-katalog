---
name: manage-task-workspaces
description: 为可能写文件的 Agent 任务创建、检查、提交、收尾、修复和清理 Git Worktree 隔离空间。用户提到并行任务、多个 Agent、任务分支、Worktree、跨仓库修改、恢复失败任务或安全合并时使用。
---

# 管理任务 Worktree

## 适用规则

- 只读盘点不创建 Worktree；第一次写入前创建。
- 使用安装后的 `cockpit` 命令，不手工拼接多仓库 Worktree。
- 每个仓库只提交明确列出的相对路径。
- `finish`、外部推送、PR、合并和 `cleanup` 都保留独立门禁。
- 状态真相在规范仓根的
  `.cockpit-runs/task-workspaces/<task-id>/state.json`。

遇到失败、部分推送、PR 已合并但状态滞后或清理拒绝时，读取
[references/recovery.md](references/recovery.md)。

## 标准流程

1. 检查环境和仓库配置：

   ```bash
   cockpit --root <workspace-root> doctor
   cockpit --root <workspace-root> repos
   ```

2. 创建任务空间；根仓自动加入，其它仓库显式指定：

   ```bash
   cockpit --root <workspace-root> start <task-id> --repo <repo-key>
   ```

   `mount_path` 必须已经被根仓 `.gitignore` 忽略。不要把原 dirty 目录的
   未提交文件搬进任务空间。

3. 在输出的 workspace 内工作。需要切换客户端时，只打印启动命令：

   ```bash
   cockpit --root <workspace-root> launch <task-id> --runtime <runtime-key>
   ```

4. 每个仓库单独检查或提交：

   ```bash
   cockpit --root <workspace-root> prepare <task-id> \
     --repo <repo-key> \
     --path <relative-path> \
     --message "<commit message>"
   ```

   提交语言和格式由 `.cockpit/config.json` 的
   `commit_message_pattern` 决定；未配置时不限制语言。

5. 收尾前先展示无副作用计划：

   ```bash
   cockpit --root <workspace-root> finish <task-id> --dry-run
   ```

6. 只有用户明确授权外部集成后，才传配置中的确认短语：

   ```bash
   cockpit --root <workspace-root> finish <task-id> --confirm <phrase>
   ```

   默认短语是 `integrate`。必须逐仓遵守 `manual`、`local_only`、
   `pull_request` 或 `direct_main` 策略，不能临时降级安全门禁。

7. 清理是单独动作，先预览再确认：

   ```bash
   cockpit --root <workspace-root> cleanup <task-id> --dry-run
   cockpit --root <workspace-root> cleanup <task-id> --confirm cleanup
   ```

   清理只移除符合条件的干净 Worktree，保留任务分支和审计状态；不提供
   `--force`。

## 报告内容

向用户报告任务 workspace、任务分支、各仓库阶段、实际验证、未验证边界和
下一步。没有后续动作时明确写“任务完结”。
