---
name: production-config-sync
description: >
  生产配置关联检查——代码变更后自动检查是否需要同步更新关联的配置文件
  （nginx、docker-compose、CI/CD、环境变量等），防止"改了代码忘了改配置"
  导致的生产事故。触发词：配置同步、改完代码改配置、nginx 配置、路由配置、
  docker 配置、生产配置、config sync、关联配置检查。
---

# 生产配置关联检查

代码变更时，有些关联的配置文件必须同步更新。如果只改代码不改配置，部署后必崩。
本 skill 提供一套系统化的关联检查方法。

## 核心原则

**代码和配置是耦合的**，但耦合点往往只存在于开发者脑子里，没有被显式文档化。
结果就是："我代码写好了，部署吧" → 线上 502 / CORS 报错 / 路由 404 / 构建失败。

**规则**：任何涉及以下变更的 PR，合并前必须检查对应的配置文件是否需要同步修改。

## 变更类型 → 关联配置速查

### 1. API 路由变更

| 变更内容 | 需检查的配置 |
|----------|-------------|
| 新增/修改/删除 API 路径 | nginx 反向代理规则、API Gateway 路由表 |
| 修改 API 前缀（如 `/api/v1` → `/api/v2`） | nginx `location` 块、前端 `baseURL`、环境变量 `VITE_API_BASE` |
| 新增 WebSocket 端点 | nginx `Upgrade`/`Connection` 头、超时配置 |
| 修改请求体大小限制 | nginx `client_max_body_size`、网关限制 |

### 2. 认证/鉴权变更

| 变更内容 | 需检查的配置 |
|----------|-------------|
| 新增认证方式（OAuth/JWT/SSO） | nginx CORS 头、`proxy_set_header Authorization`、Cookie domain |
| 修改 Token 有效期 | 前端刷新逻辑、网关超时、session 配置 |
| 新增公开端点（无需认证） | 确认该端点确实不在认证中间件覆盖范围内 |

### 3. 前端路由/构建变更

| 变更内容 | 需检查的配置 |
|----------|-------------|
| 修改前端路由模式（hash → history） | nginx `try_files` fallback 配置 |
| 修改 `base` 路径（如 `/app/` → `/`） | `vite.config.ts` 的 `base`、nginx `location`、CI 构建脚本 |
| 修改静态资源路径 | nginx `root`/`alias`、CDN 配置、`assetPrefix` |
| 新增环境变量（`VITE_*`） | `.env.example`、CI/CD 构建参数、Docker `ARG`/`ENV` |

### 4. 后端配置变更

| 变更内容 | 需检查的配置 |
|----------|-------------|
| 新增/修改环境变量 | `.env.example`、docker-compose `environment`/`env_file`、K8s ConfigMap、CI/CD secrets |
| 修改数据库连接参数 | docker-compose `DATABASE_URL`、连接池配置、SSL 证书路径 |
| 修改第三方 API 地址 | `.env` 的 `*_ENDPOINT`、nginx 代理白名单 |
| 新增文件上传/存储 | nginx `client_max_body_size`、存储卷挂载、云存储配置 |
| 修改日志级别/格式 | 日志采集器配置、ELK/Loki 过滤规则 |

### 5. 容器/部署变更

| 变更内容 | 需检查的配置 |
|----------|-------------|
| 新增服务依赖（Redis/Kafka/MinIO） | docker-compose `depends_on`、healthcheck、网络配置 |
| 修改端口 | docker-compose `ports`、nginx `upstream`、防火墙规则 |
| 修改健康检查端点 | docker-compose `healthcheck`、K8s `livenessProbe` |
| 新增构建步骤 | Dockerfile、CI/CD pipeline、`.dockerignore` |
| 修改资源限制需求 | docker-compose `deploy.resources`、K8s `limits` |

### 6. 中间件/拦截器变更

| 变更内容 | 需检查的配置 |
|----------|-------------|
| 修改 CORS 策略 | nginx `add_header`、代码中 CORS 中间件、CDN 配置 |
| 新增/修改限流规则 | nginx `limit_req`、网关限流 |
| 修改超时配置 | nginx `proxy_read_timeout`、网关超时、客户端超时 |

## 工作流程

### 1. 识别变更类型

合并前，运行 `git diff main...HEAD --stat` 获取变更文件列表，按文件路径识别变更类型：

```bash
# 后端路由变更
git diff main...HEAD --name-only | grep -E "(routes|controllers|handlers|endpoints)"

# 前端路由变更
git diff main...HEAD --name-only | grep -E "(router|routes\.)"

# 认证变更
git diff main...HEAD --name-only | grep -E "(auth|login|jwt|token|session|oauth)"

# 配置变更（反向：如果改了配置文件，代码里有没有对应的使用？）
git diff main...HEAD --name-only | grep -E "(nginx|docker-compose|Dockerfile|\.env|config\.)"
```

### 2. 按上表逐项比对

根据识别到的变更类型，对照上文的速查表，逐项确认关联配置文件是否需要同步修改。

### 3. 判定与输出

对每项关联检查，输出以下三种状态之一：

| 状态 | 含义 |
|------|------|
| ✅ 无需修改 | 配置已在正确状态，或本次变更不涉及该关联 |
| ⚠️ 需确认 | 关联文件存在，但无法自动判断是否需要修改——需人工 review |
| ❌ 需同步 | 代码已变更但关联配置文件未更新，部署后会出问题 |

## 输出格式

```markdown
## 生产配置关联检查报告

**分支**: feat/xxx → main
**变更文件**: 5 个

### API 路由变更
- ✅ nginx 路由表无需修改（本次未涉及路由变更）

### 环境变量变更
- ❌ `src/config.py` 新增 `REDIS_URL` 环境变量引用，但 `.env.example` 未更新
- ⚠️ docker-compose.yml 的 `environment` 段需确认是否需要追加

### 前端构建变更
- ✅ vite.config.ts base 路径未变更
```

## 自动化提示

可以将变更类型 → 关联配置的映射维护在项目根目录 `.agents/config-correlation.json` 中，格式：

```json
{
  "correlations": [
    {
      "pattern": "src/api/routes/.*",
      "description": "API 路由变更",
      "checkFiles": ["nginx/nginx.conf", "frontend/.env.production"],
      "checkRationale": "路由变更需同步 nginx 代理规则和前端 API baseURL"
    },
    {
      "pattern": "src/auth/.*",
      "description": "认证模块变更",
      "checkFiles": ["nginx/conf.d/cors.conf", "docker-compose.yml"],
      "checkRationale": "认证变更需检查 CORS 配置和容器环境变量"
    }
  ]
}
```

存在此文件时，可自动化执行关联检查，无需手动 grep。

## 注意事项

1. **即使 CI 通过也不代表配置正确**——CI 环境变量通常不同于生产环境
2. **反向检查同样重要**：如果改了 nginx 配置，也要确认代码中的对应逻辑（如超时时间、路由前缀）是否匹配
3. **多环境差异**：staging 和 production 的配置可能不同，检查时需明确目标环境
4. **不替代 `project-compliance-check`**：本 skill 聚焦"变更关联性"，`project-compliance-check` 是上线前 28 项全面审计，两者互补
