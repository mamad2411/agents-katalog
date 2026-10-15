---
name: tapd-testx
description: TAPD TestX 技能，用于查询仓库和目录、创建或更新 TestX 用例，并把 TAPD 需求稳定关联到 TestX 用例。依赖 tapd-base 提供 OAuth 和用户态 API token；涉及需求内容时先串联 tapd-story。
---

# TestX 操作

使用这个 skill 操作 TestX repo、folder、case，以及把 TAPD 需求关联到 TestX 用例。执行前必须先确认相邻目录存在 `tapd-base`，并按 `tapd-base` 完成配置和 token 检查。

## 串联方式

- 只操作 TestX repo/folder/case：`tapd-base` -> `tapd-testx`
- 需要先读取或更新 TAPD 需求，再创建/关联用例：`tapd-base` -> `tapd-story` -> `tapd-testx`
- `tapd-testx` 只负责 TestX 与需求关联结构；需求正文、状态和字段读取交给 `tapd-story`

## 前置检查

命令示例默认已设置 skills 根目录。Codex 全局安装通常是 `~/.codex/skills`，Claude Code 全局安装通常是 `~/.claude/skills`：

```bash
export TAPD_SKILLS_ROOT="${TAPD_SKILLS_ROOT:-$HOME/.codex/skills}"
```

先检查 TAPD 用户态配置：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-base/scripts/tapd_user_oauth_demo.py" check-config
```

如果没有可用 token，先通过 `tapd-base` 完成授权：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-base/scripts/tapd_user_oauth_demo.py" authorize
```

## 已验证规则

- TestX 相关接口里的 `namespace` 使用 TAPD 的 `workspace_id`
- 这个接口已验证可用：

```text
/api/testx/case/v1/namespaces/{workspace_id}/repos
```

- TestX 用例关联 TAPD 需求时，稳定可用的 `Issues` 结构是：
  - `IssueUid=<story_id>`
  - `WorkspaceUid=<workspace_id>`
  - `IssueUrl=<workspace_id>`
  - `Type=STORY`
  - `Source=TAPD`
- 不要把 TAPD 需求详情页 URL 填进 `IssueUrl`

## Repo

列出 TestX repo：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  repo-list \
  --workspace-id 32131908
```

读取单个 TestX repo：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  repo-get \
  --workspace-id 32131908 \
  --repo-uid 17090
```

## Folder

查询目录或目录下的用例：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  folder-list \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --folder-uid 12572042 \
  --item-type CASE
```

可选参数：

```bash
--include-descendants
--story-id 1132131908001006860
```

创建 TestX 目录：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  folder-create \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --name 回归目录
```

创建子目录时加：

```bash
--parent-folder-uid 12572042
```

更新 TestX 目录：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  folder-update \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --folder-uid 12572042 \
  --payload-file /absolute/path/to/folder.json
```

## Case

读取单条 TestX 用例：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  case-get \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --case-uid 12572047
```

确认用例实际保存的 `Issues` 内容时，优先使用 `case-get`，不要只看 `cases/search`。

列出 TestX 用例：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  case-list \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --folder-uid 12572042 \
  --show-mode FLAT
```

给已有 TestX 用例关联 TAPD 需求：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  case-link-story \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --case-uid 12572047 \
  --story-id 1132131908001006860 \
  --story-workspace-id 32131908
```

创建 TestX 用例并同时关联 TAPD 需求：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  case-create \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --payload-file /absolute/path/to/case.json \
  --story-id 1132131908001006860 \
  --story-workspace-id 32131908
```

更新 TestX 用例并可同时关联 TAPD 需求：

```bash
python3 "$TAPD_SKILLS_ROOT/tapd-testx/scripts/tapd_testx.py" \
  case-update \
  --workspace-id 32131908 \
  --repo-uid 17090 \
  --version-uid 18158 \
  --case-uid 12572047 \
  --payload-file /absolute/path/to/case.json \
  --story-id 1132131908001006860 \
  --story-workspace-id 32131908
```

## 维护注意事项

- `cases/search` 适合查列表，`case-get` 适合确认最终落库结构
- 当前 skill 只封装已确认的 repo 查询、folder 查询/创建/更新、case 查询/创建/更新能力，没有额外猜测 `delete` 或 `folder-get` 路径
