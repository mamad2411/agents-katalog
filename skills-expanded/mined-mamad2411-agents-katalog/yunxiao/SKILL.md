---
name: yunxiao
description: >-
  Installs, configures, and calls Alibaba Cloud Yunxiao CLI (aliyun devops) for
  Codeup, Flow, Projex, AppStack, Packages, and TestHub. Use when the user
  mentions 云效, Yunxiao, Apsara DevOps, aliyun devops, Codeup, Flow, Projex, PAT,
  organization-id, or asks to list/create repositories, pipelines, projects, or apps.
disable-model-invocation: true
---

# Yunxiao

通过阿里云 CLI 插件 `aliyun-cli-devops` 调用云效 OpenAPI。不要用 `aliyun configure` / AK/SK；数据面只用个人访问令牌（PAT）。

## Instructions

1. **只做检测**，不要预装：

   ```bash
   aliyun version
   aliyun devops version
   ```

   - 通过：CLI ≥ 3.3.0 且插件返回版本 → 不要重装，继续步骤 2。
   - 失败：`aliyun` 不存在、版本低于 3.3.0、或 `devops` 不可用 → 读并执行 [references/install.md](references/install.md)（装 CLI、装插件，再引导用户拿 PAT / orgId 并填写）。

2. **不确定命令/参数**：`aliyun devops --help` 或 `aliyun devops <command> --help`，不要猜。

3. **调用**：`aliyun devops <command> [flags]`。优先环境变量；用 `--cli-query` 收窄输出。不要先检查凭证。

4. **调用失败后再检查凭证**（只看是否存在，绝不打印令牌）：
   - PowerShell：`[bool]$env:ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN`，以及 `ORGANIZATION_ID` 或 `API_BASE_URL`
   - bash：`[ -n "$ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN" ]`

5. **未配置**：读 [references/install.md](references/install.md) 的「获取并填写凭证」，引导用户去控制台拿 PAT 和 organization-id（或 Region 版 api-base-url），**等用户填写后再写入环境变量**。不要重装 CLI。不要把令牌回显到回复里。写入后再重试刚才失败的调用。

### 组织类型

| | 中心版 | Region 版 |
|---|---|---|
| 接入点 | 内置 `openapi-rdc.aliyuncs.com`，不要设 `api-base-url` | 控制台实例访问域名 → `ALIBABA_CLOUD_YUNXIAO_API_BASE_URL` |
| 组织 ID | 必须 `ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID` | 不要设 |

PAT：云效工作台 → 头像 → 个人设置 → 个人访问令牌。只在创建时显示一次。最小权限，设过期时间。

### 环境变量

中心版：`ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN` + `ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID`

Region 版：`ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN` + `ALIBABA_CLOUD_YUNXIAO_API_BASE_URL`

禁止把令牌写进命令行、回复、日志或 commit。检查时只报 `已设置` / `未设置`。

### 模块前缀

`app-stack-*` AppStack · `base-*` 组织成员 · `codeup-*` Codeup · `flow-*` Flow · `insight-*` Insight · `packages-*` Packages · `projex-*` Projex · `test-hub-*` TestHub

## Examples

列出仓库：

```bash
aliyun devops codeup-list-repositories --page 1 --per-page 20
```

搜索项目：

```bash
aliyun devops projex-search-projects --page 1 --per-page 10
```

更多输入/输出见 [examples.md](examples.md)。

## Additional resources

- 安装与首次填写凭证：[references/install.md](references/install.md)
- 命令与排错：[references/reference.md](references/reference.md)
- 用法示例：[examples.md](examples.md)
