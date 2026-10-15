---
name: gitlab-mr-review
description: Fetch, review, and post inline comments on a GitLab Merge Request. Use when user asks to review a GitLab MR/PR, audit code changes, or comment on a merge request.
---

> **⚠ 严禁调用 MR Approve 接口（`/merge_requests/:iid/approve`）。**

# gitlab-mr-review

---

## 参数

调用时可附带 MR 完整 URL 作为参数，例如：
`/gitlab-mr-review https://gitlab.example.com/group/repo/-/merge_requests/42`

若未提供，则在 Step 2 中询问用户。

---

## Step 1 — 确认依赖工具

**macOS / Linux：**

```bash
which jq || sudo apt install jq -y   # Linux
which jq || brew install jq           # macOS
```

**Windows PowerShell：**

```powershell
if (-not (Get-Command jq -ErrorAction SilentlyContinue)) {
    winget install jqlang.jq   # Windows 10 1709+ 内置，或改用：choco install jq
}
```

---

## Step 2 — 解析 MR URL

从调用参数或用户输入中提取以下变量：
`https://gitlab.example.com/group/repo/-/merge_requests/42`

- `$GITLAB_HOST` = `https://gitlab.example.com`
- `$PROJECT_PATH` = `group/repo`
- `$PROJECT_PATH_ENCODED` = `group%2Frepo`（`/` → `%2F`）
- `$MR_IID` = `42`

若无法从参数解析，询问用户提供完整 MR URL。

---

## Step 3 — 检测运行环境

执行以下命令判断当前 shell 类型，**后续所有步骤根据结果选择对应示例**：

```bash
uname -s 2>/dev/null || echo "Windows"
```

- 输出 `Linux` / `Darwin`：使用 **bash** 示例
- 命令不存在或输出 `Windows`：使用 **PowerShell** 示例

> PowerShell 特别注意：
>
> - 用 `Invoke-RestMethod` 替代 `curl`（原生解析 JSON，无需 jq）
> - 环境变量写法为 `$env:GITLAB_TOKEN`
> - 所有请求均加 `-SkipCertificateCheck`（需 PowerShell 7+）

---

## Step 4 — 检查环境变量

**bash（macOS / Linux）：**

```bash
curl -sfk -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/user" | jq '.name'
```

**PowerShell（Windows）：**

```powershell
(Invoke-RestMethod -Uri "$GITLAB_HOST/api/v4/user" `
  -Headers @{"PRIVATE-TOKEN" = $env:GITLAB_TOKEN} `
  -SkipCertificateCheck).name
```

返回用户名则就绪，继续 Step 5。否则引导用户配置（**不要替用户执行这些命令**）：

> 1. 打开 `$GITLAB_HOST/-/user_settings/personal_access_tokens`
> 2. 创建 token，Scopes 勾选 **api**，复制
> 3. 根据系统设置环境变量：
>    - bash（Linux）：`echo 'export GITLAB_TOKEN=glpat-xxx' >> ~/.bashrc`
>    - zsh（macOS）：`echo 'export GITLAB_TOKEN=glpat-xxx' >> ~/.zshrc`
>    - PowerShell（Windows，永久）：`[Environment]::SetEnvironmentVariable('GITLAB_TOKEN','glpat-xxx','User')`
> 4. **关闭当前终端，重新打开一个新的会话**，然后用以下命令继续本次 review：
>
>    ```
>    /gitlab-mr-review $MR_URL
>    ```

---

## Step 5 — 获取 diff_refs（行级评论必需）

**bash（macOS / Linux）：**

```bash
curl -sfk -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID" \
  | jq '{title, state, diff_refs}'
```

**PowerShell（Windows）：**

```powershell
$mr = Invoke-RestMethod `
  -Uri "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID" `
  -Headers @{"PRIVATE-TOKEN" = $env:GITLAB_TOKEN} `
  -SkipCertificateCheck
$mr | Select-Object title, state, diff_refs
```

保存以下三个值，发行级评论时必须全部提供：

- `$BASE_SHA` ← `diff_refs.base_sha`
- `$START_SHA` ← `diff_refs.start_sha`
- `$HEAD_SHA` ← `diff_refs.head_sha`

---

## Step 6 — 获取 diff 并计算行号

每次取 100 条（GitLab 上限），从 page=1 开始逐页请求，直到返回空数组为止。

**⚠ 执行约束（必须遵守）：**
- 逐页获取后**先累积所有页结果**，待全部获取完毕后再统一分析，保证跨文件上下文完整
- 只使用本文档定义的命令，不得自行增加文件搜索、索引查找等额外操作
- 若某文件 `diff` 字段为空且 `too_large: true`，使用文件内容 API 获取 HEAD 版本全量内容进行审查（见下方"处理 too_large 文件"）

**bash（macOS / Linux）：**

```bash
curl -sfk -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID/diffs?per_page=100&page=PAGE"
```

**PowerShell（Windows）：**

```powershell
Invoke-RestMethod `
  -Uri "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID/diffs?per_page=100&page=PAGE" `
  -Headers @{"PRIVATE-TOKEN" = $env:GITLAB_TOKEN} `
  -SkipCertificateCheck
```

将 `PAGE` 从 1 开始递增，直到返回空数组为止，**先收集所有页的结果**，提取每个文件的 `new_path`、`old_path`、`diff`、`too_large` 字段，然后在 Step 7 中整体分析，避免因上下文不足造成理解偏差。

### 读取全量文件（分析时按需使用）

分析 diff 时，若某文件的改动难以理解（缺少上下文、依赖其他文件等），可拉取该文件在 HEAD 的完整内容辅助理解：

**bash（macOS / Linux）：**

```bash
# FILE_PATH_ENCODED：将路径中的 / 替换为 %2F，如 src/foo.ts → src%2Ffoo.ts
curl -sfk -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/repository/files/FILE_PATH_ENCODED?ref=$HEAD_SHA" \
  | jq -r '.content' | base64 -d
```

**PowerShell（Windows）：**

```powershell
$filePath = "src%2Ffoo.ts"   # / → %2F
$file = Invoke-RestMethod `
  -Uri "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/repository/files/$filePath?ref=$HEAD_SHA" `
  -Headers @{"PRIVATE-TOKEN" = $env:GITLAB_TOKEN} `
  -SkipCertificateCheck
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($file.content))
```

### 处理 too_large 文件

当某文件 `diff: ""` 且 `too_large: true` 时，使用上方"读取全量文件"的命令拉取 HEAD 版本进行全量审查，并在分析结论中注明该文件为全量审查（非 diff）。行级评论的 `new_line` 直接使用文件中的实际行号。

### 计算每行的绝对行号

`@@` 头：`@@ -old_start,old_count +new_start,new_count @@`

初始化：`old_num = old_start`，`new_num = new_start`

| 行前缀         | position 用字段      | old_num | new_num |
| -------------- | -------------------- | ------- | ------- |
| ` `（context） | `new_line = new_num` | +1      | +1      |
| `+`（新增）    | `new_line = new_num` | 不变    | +1      |
| `-`（删除）    | `old_line = old_num` | +1      | 不变    |

---

## Step 7 — 分析 diff

检查变更行，关注：

- **功能完整性**：需求是否完整实现，是否存在遗漏的分支或场景
- **逻辑正确性**：条件判断、循环、状态流转是否正确，有无逻辑漏洞或反转
- **边界与异常**：空值、空集合、越界、并发、超时等边界情况是否处理
- **可简化性**：是否有冗余逻辑、重复代码（DRY）、过度抽象或可用语言内置替代的实现
- **代码质量**：命名不清、多余复杂度、缺少错误处理、死代码
- **安全**：注入、越权、硬编码密钥
- **性能**：N+1 查询、热路径阻塞
- **代码规范**：见 [RULES.md](RULES.md)

每个问题记录：

```
file:     src/foo.ts
new_line: 42        # 新增/context 行；纯删除行改用 old_line
severity: CRITICAL | WARNING | SUGGESTION
body:     中文描述 + 建议修复
```

只关注变更行，评论内容必须用中文。

---

## Step 8 — 发行级评论

每个问题单独一条，发到对应文件的对应行：

**bash（macOS / Linux）：**

```bash
# 新增行 / context 行 → 用 new_line
curl -sfk -X POST \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID/discussions" \
  -d '{
    "body": "**[严重程度]** 问题描述",
    "position": {
      "base_sha":      "'"$BASE_SHA"'",
      "start_sha":     "'"$START_SHA"'",
      "head_sha":      "'"$HEAD_SHA"'",
      "position_type": "text",
      "new_path":      "path/to/file.ts",
      "new_line":      42
    }
  }'

# 纯删除行 → 用 old_line
curl -sfk -X POST \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID/discussions" \
  -d '{
    "body": "**[严重程度]** 问题描述",
    "position": {
      "base_sha":      "'"$BASE_SHA"'",
      "start_sha":     "'"$START_SHA"'",
      "head_sha":      "'"$HEAD_SHA"'",
      "position_type": "text",
      "old_path":      "path/to/file.ts",
      "old_line":      11
    }
  }'
```

**PowerShell（Windows）：**

```powershell
# 新增行 / context 行 → 用 new_line
$body = @{
  body = "**[严重程度]** 问题描述"
  position = @{
    base_sha      = "ACTUAL_BASE_SHA"
    start_sha     = "ACTUAL_START_SHA"
    head_sha      = "ACTUAL_HEAD_SHA"
    position_type = "text"
    new_path      = "path/to/file.ts"
    new_line      = 42
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post `
  -Uri "$GITLAB_HOST/api/v4/projects/$PROJECT_PATH_ENCODED/merge_requests/$MR_IID/discussions" `
  -Headers @{"PRIVATE-TOKEN" = $env:GITLAB_TOKEN} `
  -ContentType "application/json" `
  -SkipCertificateCheck `
  -Body $body

# 纯删除行 → 将 new_line/new_path 替换为 old_line/old_path
```

> PowerShell 要点：用 `ConvertTo-Json` 构造 body 避免引号转义；SHA 值填入实际值；`Invoke-RestMethod` 会自动解析响应 JSON。

返回 422 说明行号不在 diff 中，跳过该条。

---

## Troubleshooting

| Error                        | Fix                                                               |
| ---------------------------- | ----------------------------------------------------------------- |
| 401                          | Token 无效或缺少 `api` scope                                      |
| 404                          | 路径错误，检查 `%2F` 编码                                         |
| 422                          | 行号不在 diff 中，跳过                                            |
| Exit code 49（Windows bash） | IPv6 绑定或代理冲突，curl 加 `--ipv4`；若仍失败加 `--noproxy '*'` |
