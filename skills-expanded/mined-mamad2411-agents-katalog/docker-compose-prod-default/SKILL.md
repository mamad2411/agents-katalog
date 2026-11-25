---
name: docker-compose-prod-default
description: >
  Docker Compose 生产/开发默认语义设计规范与审查。
  核心原则：docker compose build/up 默认产出生产版，开发版通过显式 -f docker-compose.dev.yml 加载；
  生产 compose 零源码挂载；永不使用 docker-compose.override.yml 约定文件名做开发。
  当用户设计 Docker 部署方案、初始化 docker-compose、review 项目的 docker 配置、
  遇到「build 默认出开发版」「生产环境误挂载源码」「override 文件自动加载导致行为反直觉」、
  或要把现有项目的 dev/prod compose 拆分时使用。
  触发词：docker-compose override、compose 生产版、compose 开发版、override.yml、
  build 默认出开发版、生产环境挂载源码、dev/prod 拆分、源码挂载到容器、
  ./src:/app、镜像不可变原则、Dockerfile.dev、compose 部署方案设计、
  compose 文件审查。
---

# Docker Compose 生产/开发默认语义设计规范

## 问题背景

Docker Compose 有一个约定：名为 `docker-compose.override.yml` 的文件会被 `docker compose up/build` **自动合并加载**。很多项目误用这个约定文件名存放开发配置，导致：

1. `docker compose build` 默认产出**开发版**（因为 override 把 Dockerfile 换成了 dev 版）——违背「build 默认出生产版」的直觉
2. 生产 compose 里混入 `./src:/app` 源码挂载和 `DEBUG=true`——生产容器依赖宿主源码目录，镜像不可变原则被破坏
3. 想构建生产版必须记一个反直觉的命令 `docker compose -f docker-compose.yml up --no-override`

本 skill 把这套反模式修正为「**生产是默认，开发是叠加**」的正向设计。

## 四条核心原则

### 原则 1：生产是默认，开发是叠加

`docker-compose.yml` 永远是**纯生产配置**。开发配置独立成 `docker-compose.dev.yml`，通过显式 `-f` 加载。

**永不使用 `docker-compose.override.yml` 这个约定文件名做开发**——它会自动加载，导致默认行为变成开发版。这是本规范最重要的一条。

```bash
# 生产（默认，直觉正确）
docker compose build
docker compose up -d

# 开发（显式叠加，不会误触发）
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 原则 2：生产 compose 零源码挂载

所有 `./src:/app`、`./backend:/app`、`./frontend:/app` 这类 bind mount 只能进 `docker-compose.dev.yml`。生产用镜像内 `COPY` 的代码，保证镜像不可变。

生产 compose 的 volumes 只允许：
- 数据卷（`mysql_data:`、`redis_data:` 等命名卷）
- 运行时数据目录（如 `./uploads:/uploads` 用户上传数据，不是源码）
- 日志卷
- 配置文件只读挂载（如 `./nginx.conf:/etc/nginx/...:ro`，不是源码）

**为什么**：生产环境部署时，宿主机上不一定有源码（CI 构建镜像后只推镜像）。即使有，挂载源码会让「镜像」和「运行行为」脱节——同一镜像在不同机器跑出不同结果，违背镜像不可变原则。

### 原则 3：环境差异走 compose 覆盖

`DEBUG`、`LOG_LEVEL`、`RELOAD`、`ENVIRONMENT` 这类开关：

- **生产 compose** 写死安全值（`DEBUG: "false"`、`LOG_LEVEL: "warning"`）
- **dev compose** 用 `environment:` 覆盖（`DEBUG: "true"`）

不要靠 `.env` 文件区分生产/开发——`.env` 只放密钥和部署坐标（数据库地址、端口），不放行为开关。理由：`.env` 容易被误提交或误复制，而 compose 覆盖是显式的、版本可控的。

### 原则 4：一份 Dockerfile 多阶段构建

**默认**一个服务只维护一份 `Dockerfile`，用多阶段构建产出最小生产镜像。不要为 dev/prod 维护两份 Dockerfile。

**例外**：当 dev 模式有**强技术约束**无法复用生产 Dockerfile 时，才允许 dev 专用 Dockerfile（如 `Dockerfile.dev`）。典型场景：Vite dev server 强依赖 esbuild 长驻服务，跑不了 nginx 静态模式。这种情况下：
- dev 专用 Dockerfile 仍由 `docker-compose.dev.yml` 选用（`dockerfile: Dockerfile.dev`）
- 不污染生产 compose 和生产 Dockerfile

## 审查现有项目时的检查清单

接到「审查 docker 配置」或「我的 build 默认出开发版」类需求时，按以下步骤定位证据（结论必须带 `文件:行号`）：

### 检查 1：是否有 override 约定文件名

```bash
ls docker-compose.override.yml 2>/dev/null
```

若存在，这是反模式根因。检查它是否：
- 改了 `build.dockerfile`（换 dev 版 Dockerfile）
- 挂载了源码
- 覆盖了端口/环境变量

### 检查 2：生产 compose 是否有源码挂载

```bash
grep -n ":/app\|:/code\|:/src" docker-compose.yml
```

任何 `./<源码目录>:<容器路径>` 都是生产环境的隐患。区分源码挂载与数据挂载：
- `./backend:/app` → 源码挂载，必须移除（移到 dev compose）
- `./uploads:/uploads` → 数据目录，可保留
- `./nginx.conf:/etc/nginx/...:ro` → 配置只读挂载，可保留

### 检查 3：生产环境变量是否写死安全值

```bash
grep -n "DEBUG\|RELOAD\|ENVIRONMENT" docker-compose.yml
```

生产 compose 里 `DEBUG: "true"` 是危险的（堆栈 trace 泄露、热重载开启）。应为 `"false"`。

### 检查 4：验证两套配置的实际合并结果

```bash
# 生产配置（不加载 dev）
docker compose config | grep -E "DEBUG:|source:|dockerfile:"

# 开发配置（显式加载 dev）
docker compose -f docker-compose.yml -f docker-compose.dev.yml config | grep -E "DEBUG:|source:|dockerfile:"
```

对比两次输出，确认：
- 生产：`DEBUG: "false"`、无源码 bind mount、用生产 Dockerfile
- 开发：`DEBUG: "true"`、有源码 bind mount、用 dev Dockerfile（若有）

## 重构步骤（从 override 反模式迁移到本规范）

1. `git mv docker-compose.override.yml docker-compose.dev.yml`（保留历史）
2. 净化 `docker-compose.yml`：
   - 移除所有源码 bind mount（保留数据卷、配置只读挂载）
   - `DEBUG` 等开关改安全值
3. 补全 `docker-compose.dev.yml`：
   - 把移除的源码挂载搬到这里
   - 覆盖 `DEBUG: "true"` 等开发开关
   - 保留原 dev 专有配置（dev Dockerfile、HMR 端口等）
4. 修正 `.pre-commit-config.yaml`：`check-yaml` 的 exclude 规则从 `override.yml` 改为 `dev.yml`（dev compose 常用 `!override` 等 compose 扩展标签，标准 yaml 校验会报错）
5. 更新部署脚本/文档：补「生产/开发」双模式命令说明
6. 验证：`docker compose config` 两套配置对比（见检查 4）

## 镜像源注意事项

国内项目常遇 `docker.io` 拉取超时。Dockerfile 里应预留 `ARG REGISTRY=docker.io`，compose 的 `build.args` 里把默认值设为可达的镜像源（如 `m.daocloud.io/docker.io`），而非让用户每次手动 `--build-arg`。这虽不是本规范核心，但常与 compose 重构一起处理。

## 文件结构范例

```
项目根/
├── docker-compose.yml          # 纯生产（默认，零源码挂载）
├── docker-compose.dev.yml      # 开发（显式 -f 加载，源码挂载 + DEBUG）
├── backend/
│   └── Dockerfile              # 多阶段构建，唯一生产 Dockerfile
└── frontend/
    ├── Dockerfile              # 生产：多阶段 → nginx 静态
    └── Dockerfile.dev          # 例外：Vite dev server 强约束才允许
```

## 命令速查

| 场景 | 命令 |
|------|------|
| 生产构建 | `docker compose build` |
| 生产启动 | `docker compose up -d` |
| 开发构建 | `docker compose -f docker-compose.yml -f docker-compose.dev.yml build` |
| 开发启动 | `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d` |
| 验证生产配置 | `docker compose config` |
| 验证开发配置 | `docker compose -f docker-compose.yml -f docker-compose.dev.yml config` |

## 与其他 skill 的衔接

- 构建缓存复用、镜像优化、BuildKit 配置等 → 参考 `docker-expert`
- 项目整体架构规范（分层、目录结构）→ 参考 `robust-architecture`
- 涉及 commit message → 用 `chinese-commit-messages`