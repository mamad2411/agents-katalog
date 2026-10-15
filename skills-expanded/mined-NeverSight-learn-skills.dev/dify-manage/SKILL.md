---
name: dify-manage
description: >-
  Manages Dify via bundled CLI: pull/export DSL, patch working.yml, deploy,
  cache remote files, upload to Dify, run/chat workflows. Use when the user
  mentions Dify, workflow DSL, pull, deploy, dify-manage, or Dify file inputs.
  当用户需要管理 Dify 工作流 DSL、拉取、编辑、部署、文件缓存、文件上传、运行或调试 Dify 应用时触发。
---

# Dify 管理

## CLI

**SKILL_ROOT** = 本 `SKILL.md` 所在目录（安装后通常在 `~/.cursor/skills/dify-manage/`）。

```bash
# 基命令（后续子命令均接在此后）
python3 "{SKILL_ROOT}/scripts/dify_manage.py" <子命令> [选项]
# 或："{SKILL_ROOT}/scripts/dify" <子命令> [选项]
```

业务项目内可自建 `bin/dify` 包装，启动时 `cd` 到项目根以发现 `.env` / `.dify/`。

## 首次使用（业务项目根目录）

先 `cd` 到含 `.env` 的业务仓库根，再执行：

```bash
# 1. 配置 .env（见 skill 内 .env.example）
# 2. 初始化 .dify/ 骨架（dsl、cache、manifest 等）
python3 "{SKILL_ROOT}/scripts/dify_manage.py" init

# 3. 需要 Console 操作时（须用户确认）
python3 "{SKILL_ROOT}/scripts/dify_manage.py" login

# 4. 列出应用
python3 "{SKILL_ROOT}/scripts/dify_manage.py" apps
```

`login` 也会自动创建 `.dify/` 并写入 `session.json`，但不会建好 `dsl/`、`cache/` 等子目录；**首次务必先 `init`**。

## 项目布局（使用方仓库，非本 skill）

| 路径 | 内容 | Git |
|------|------|-----|
| `.env` | `DIFY_CONSOLE_URL`、`DIFY_BASE_URL` | 真实 ignore |
| `.dify/session.json` | Console token | **ignore** |
| `.dify/manifest.yml` | 应用索引、hash | 建议提交 |
| `.dify/dsl/{app_id}/` | `{ts}-remote.yml`、`working.yml` | remote ignore |
| `.dify/apps/{app_id}.yml` | 业务元数据 | 按需 |
| `.dify/fixtures/{app_id}/` | `smoke.json`、`assets/` | 按需 |
| `.dify/cache/downloads/` | `{md5(url)}-{name}` | **ignore** |

## Token 优先级

`OS env` > `.dify/session.json` > `.env` token。`login`/`refresh` 只写 `session.json`。

## 安全

- 未指定 app → `apps` 确认
- deploy/login 须用户确认
- `--app-id`、`--api-key` 每次传入
- skill 内不固化业务 URL、token、应用名

## DSL 工作流

```bash
python3 "{SKILL_ROOT}/scripts/dify_manage.py" init
python3 "{SKILL_ROOT}/scripts/dify_manage.py" apps
python3 "{SKILL_ROOT}/scripts/dify_manage.py" pull --app-id <id>
# 编辑 .dify/dsl/<id>/working.yml
python3 "{SKILL_ROOT}/scripts/dify_manage.py" dsl diff --app-id <id>
python3 "{SKILL_ROOT}/scripts/dify_manage.py" deploy --app-id <id>
```

维护：`dsl refresh`、`dsl reset`、`dsl prune --keep 3`、`pull --sync-working`。

## 文件工作流

```bash
cache download "https://example.com/a.jpg"
files upload path-or-url --api-key app-xxx
run --api-key app-xxx --file-url product_image=https://...
run --api-key app-xxx --fixtures .dify/fixtures/<id>/smoke.json
```

## DSL 规则

- 改前 `pull`；只 patch 目标节点
- 禁止旧 YAML 整包覆盖
- deploy 前 `dsl diff`；注意 `default` / `file_upload`

## Agent 清单

1. 首次使用：在业务项目根执行 `init`（见上文「首次使用」完整命令）
2. 未指定 app → `apps`
3. 改 DSL 前 `pull`；编辑 `working.yml`
4. 部署前 `dsl diff`；异常用 `dsl status --check-remote`
5. 外链：`cache download` → `files upload` 或 `run --file-url`
6. 敏感操作须确认
7. 无用户要求不 `login`

## 参考

[reference.md](reference.md)
