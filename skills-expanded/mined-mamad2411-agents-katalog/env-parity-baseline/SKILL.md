---
name: env-parity-baseline
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
description: >-
  Cross-environment parity baseline and deployment-risk router. Detects dev/CI/staging/prod consistency gaps, injects a minimum baseline file set (.gitattributes, .editorconfig, env validator, CI matrix, env contract, runtime manifest, deploy parity checklist), and routes deploy-layer concerns (Docker, Compose, k8s, systemd, Nginx, Terraform, Ansible) to downstream specialists instead of over-generating templates. Scoped to detect, minimum contract and handoff — not a full deploy generator. Triggers: "环境一致性 / dev-prod parity / CRLF/LF / works on my machine / runtime version pin / .env.example / k8s configmap mismatch / 跨平台 / 部署环境".
---

# env-parity-baseline — 跨环境一致性基线 + 部署风险路由器

## 0. 重要定位（不要误解）

**这个 skill 不是"全栈部署配置生成器"。**

它不直接产出完整的 Dockerfile / Kubernetes manifests / Terraform / Ansible / Nginx 配置。如果它做这些，会变成一个不可靠的巨型模板仓库。

**它是三件事的合体**：

1. **环境差异检测器** — 扫描 dev / CI / staging / prod 之间的缺口
2. **最小一致性契约注入器** — 只写最小必要的基线文件（行尾符 / env validator / CI matrix / contract docs）
3. **部署/运行时风险路由器** — 把容器、k8s、systemd、Nginx、Terraform 等深水区路由给后续 specialist skill 或人工 review

输出三件事：**detected risks / minimum baseline / safe next action**。

---

## 1. Mission

- 缩小 dev / CI / staging / prod 之间的差异（Twelve-Factor X）
- 让"在我机器上能跑"变成"在所有目标平台都能跑"
- 在 baseline 注入前必须 PROPOSE，绝不静默覆盖现有文件
- 检测到深水区（k8s schema 不齐 / Dockerfile secret 泄露 / Nginx 错配）→ handoff，不在本 skill 内修复

---

## 2. 激活条件

### 强激活（任一即装）

- 项目含语言 manifest：`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `pom.xml` / `build.gradle` / `CMakeLists.txt`
- 项目含运行 / 部署信号：`Dockerfile` / `compose.yaml` / `docker-compose.yml` / `.devcontainer/` / `k8s/` / `kubernetes/` / `helm/` / `Chart.yaml` / `terraform/` / `*.tf` / `ansible/` / `systemd/` / `*.service` / `nginx.conf` / `Caddyfile` / `.github/workflows/*deploy*`
- 部署目标含 Linux 服务器但开发机器含 Windows / macOS（混合 OS 团队）

### 跳过条件

- 纯文档 / 咨询项目（只有 `.md`）
- 单文件实验 / prototype 早期阶段且明确不部署
- 用户在 ASK 阶段明确选择"unknown / 无 / 否" 且无其他强信号

---

## 3. 检测信号矩阵（DETECT — 只读，不改文件）

### 3.1 工具链版本锁定信号

| 语言 | 应有版本锁文件 | 缺失 severity |
|---|---|---|
| Node | `.nvmrc` / `.node-version` / `package.json#volta` / `mise.toml` / `.tool-versions`（asdf） | MEDIUM |
| Python | `.python-version` / `mise.toml` / `.tool-versions` / `uv.lock` 含 `requires-python` | HIGH（Python 版本差异破坏性大） |
| Rust | `rust-toolchain.toml` | MEDIUM |
| Go | `go.mod` 含 `go 1.x` + `toolchain` directive | MEDIUM |
| Java | Maven Wrapper（`mvnw`）/ Gradle Wrapper（`gradlew`）/ `.java-version` / `.sdkmanrc` | HIGH |
| C/C++ | `CMakePresets.json` / vcpkg manifest / Conan `profile.lock` | HIGH（toolchain drift 致命） |

### 3.2 依赖锁定信号

| 语言 | clean install 命令 | 必备 lockfile |
|---|---|---|
| Node | `npm ci` / `pnpm install --frozen-lockfile` / `yarn install --frozen-lockfile` | `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` |
| Python | `pip install --require-hashes -r requirements.txt` / `poetry install --no-update` / `uv sync --frozen` | `requirements.txt` + hash / `poetry.lock` / `uv.lock` |
| Rust | `cargo build --locked` | `Cargo.lock` |
| Go | `GOFLAGS=-mod=readonly go build ./...` | `go.sum` |
| Java | `./mvnw -B verify` / `./gradlew check --refresh-dependencies` | `dependency-lock.json`（Gradle）/ Maven 内置 |

**npm 关键事实**：`npm ci` 要求已有 `package-lock.json` 或 `npm-shrinkwrap.json`，且 lockfile 与 `package.json` 不一致时直接失败（不会自动更新 lockfile）。这是 CI 必备的属性。

**pip 关键事实**：`pip install --require-hashes` 会强制对每个依赖校验 hash，是部署脚本可重复安装的基础。

### 3.3 `.env` 契约信号

| 检测项 | 怎么检测 | 缺失 severity |
|---|---|---|
| `.env.example` commit 到仓库 | `Read` | HIGH（若代码访问 `process.env` / `os.environ`） |
| `.env*` 在 `.gitignore` | `Grep` | CRITICAL（若不在） |
| env validator 在 app 启动期 throw | `Grep` 找 `zod` / `pydantic` / `envalid` / `@t3-oss/env-core` | MEDIUM |
| CI 校验 `.env.example` 与 schema 一致 | 检查 workflow yml | LOW |
| `.env.example` 不含真实 secret | `Grep` 找 `=sk_` / `=ghp_` / `=AKIA` 等高熵 prefix | CRITICAL（若发现）|

### 3.4 容器 / 部署信号（深水区 — 检测但不修复）

| 信号 | 检测的 risk | severity |
|---|---|---|
| `Dockerfile` 含 `ARG SECRET_*` / `ENV SECRET_*` / `ENV *_TOKEN` / `ENV *_PASSWORD` | secret 泄露到镜像 layer | CRITICAL |
| `compose.yaml` / `docker-compose.yml` 服务用 `:latest` tag | dev/prod 版本漂移 | HIGH |
| k8s manifests `ConfigMap` / `Secret` keys vs app env schema | 不一致 → 启动期 panic 或 silent default | HIGH |
| Helm `values.yaml` 默认值在 schema 之外 | 部署后变量未生效 | MEDIUM |
| `systemd` unit `Environment=` / `EnvironmentFile=` vs `.env.example` | systemd 启动用错变量 | HIGH |
| `nginx.conf` / `Caddyfile`：`client_max_body_size` / `proxy_read_timeout` / CORS headers | 与 app 期望不一致 | MEDIUM |
| `terraform/` 存在但缺 `terraform fmt -check` / `tflint` 在 CI | IaC drift | MEDIUM |
| `ansible/` 存在但缺 `ansible-lint` 在 CI | 部署脚本回归 | MEDIUM |
| CI deploy workflow 只跑 ubuntu 但目标 OS 含 Windows | 上线在 Windows 才炸 | HIGH |

### 3.5 健康 / 可观测信号

| 信号 | 缺失 risk | severity |
|---|---|---|
| `/healthz` / `/readyz` endpoint | k8s / compose 没法做健康检查 | HIGH（部署用 k8s/compose 时） |
| structured JSON logging | 跨环境 grep / 聚合困难 | MEDIUM |
| migration tool（drizzle / alembic / flyway / liquibase）| 部署后 schema drift | HIGH（项目有 DB 时） |
| rollback 策略文档 | 上线失败无 safe path | HIGH |
| graceful shutdown（SIGTERM 处理） | 滚动更新丢请求 | MEDIUM |

---

## 4. 标准基线（INJECT — 最小集合，仅 6 个核心文件）

仅注入以下文件，**不生成完整部署模板**：

| 文件 | 何时注入 | 模板路径 |
|---|---|---|
| `.gitattributes` | 缺失即注入 | `templates/gitattributes` |
| `.editorconfig` | 缺失即注入 | `templates/editorconfig` |
| `.env.example`（占位） | 缺失且检测到 `process.env` / `os.environ` 访问 | 生成空白模板 |
| env-validator（Node 或 Python） | 检测到对应语言 | `templates/env-validator-node.ts` / `templates/env-validator-python.py` |
| `.github/workflows/ci-matrix.yml` | 缺 CI matrix 或只跑 Linux | `templates/ci-matrix-github-actions.yml` |
| `docs/env-contract.md` | 缺 | `templates/env-contract.md` |

**额外的契约文件（PRESENT 但不执行）**：

| 文件 | 作用 |
|---|---|
| `docs/runtime-manifest.yml` | 记录语言版本 / 包管理器 / lockfile / 服务依赖 / OS target — single source of truth |
| `docs/deploy-parity-checklist.md` | 每次 deploy 前过一遍的清单（不强制执行，但作为 release gate 参考）|

---

## 5. Workflow（5 步）

```
Step 1 — DETECT     扫 §3 信号矩阵，输出 risks 表（按 severity 分级）
Step 2 — ASK        如有多义性，用 AskUserQuestion 问（见 §5.1）
Step 3 — PROPOSE    输出 risks + minimum baseline diff + 推荐 next action
Step 4 — EXECUTE    用户确认后，注入 §4 基线文件（绝不覆盖现有，diff 给用户看）
Step 5 — HANDOFF    深水区路由出去：
                    - Dockerfile secret / SAST → appsec-security-orchestrator
                    - CI cross-platform parity → enterprise-qa-testing
                    - k8s / compose / nginx / terraform 完整配置 → 人工 review 或 future deploy-specialist skill
```

### 5.1 关键多义性问题（ASK 阶段）

不是每个项目都问全。看 DETECT 结果按需：

| 维度 | 选项 | 何时问 |
|---|---|---|
| 目标运行环境 | `local only` / `Docker Compose` / `VM + systemd` / `Kubernetes` / `serverless` / `unknown` | 总是 |
| 目标 OS | `Linux` / `Windows` / `macOS` / `mixed` | 总是 |
| 服务依赖（多选） | `数据库` / `缓存` / `队列` / `对象存储` / `邮件` / `无` | 总是 |
| Secrets 来源 | `local .env` / `GitHub Secrets` / `cloud secret manager` / `k8s Secret` / `unknown` | 部署目标 ≠ `local only` 时 |
| Devcontainer 需要 | `是` / `否` / `不确定` | 检测到 multi-language monorepo 或 native deps 时 |

### 5.2 PROPOSE 输出格式（用户必须看到）

```markdown
## env-parity-baseline 报告

### Detected Risks
| Severity | 类别 | 信号 | 影响 |
|---|---|---|---|
| CRITICAL | secret | Dockerfile L12 含 `ARG STRIPE_SECRET_KEY` | secret 会进 image layer，handoff appsec |
| HIGH | runtime pin | 无 .nvmrc + 无 mise.toml | dev/CI/prod Node 版本可能漂移 |
| HIGH | CI parity | workflow 只跑 ubuntu，开发机器含 Windows | 上线在 Windows 才发现 path / shell 问题 |
| MEDIUM | repo hygiene | 无 .gitattributes | 行尾符不锁 |

### Minimum Baseline 将注入（diff）
- 新建 `.gitattributes`（55 行）
- 新建 `.editorconfig`（24 行）
- 新建 `.github/workflows/ci-matrix.yml`（50 行，ubuntu + windows 双跑）
- 新建 `docs/env-contract.md`
- 新建 `docs/runtime-manifest.yml`
- 新建 `docs/deploy-parity-checklist.md`
- 不动 `.env.example`（已存在，仅 diff 提示 schema 缺 `LOG_LEVEL`）

### Safe Next Action
1. 立即修：Dockerfile L12 secret 泄露 → 改用 BuildKit `--mount=type=secret`（handoff appsec-security-orchestrator）
2. 中期修：补 `.nvmrc` 锁 Node 版本（v20.11.x）
3. 中期修：CI matrix 加 `windows-latest` job
4. 走 `docs/deploy-parity-checklist.md` 一遍

确认注入 baseline? [Y/n/修改清单]
```

---

## 6. 跨语言模板表

### 6.1 完整模板（templates/ 已附）

| 语言 | 模板 |
|---|---|
| Node / TypeScript | `templates/env-validator-node.ts`（Zod） |
| Python | `templates/env-validator-python.py`（pydantic-settings） |

### 6.2 仅规范，不附完整模板（用户按语言生态生成）

| 语言 | 版本锁文件 | clean install 命令 | env validator 推荐 |
|---|---|---|---|
| Rust | `rust-toolchain.toml` | `cargo build --locked` | `envy` / `clap` derive |
| Go | `go.mod` 含 `toolchain go1.x` | `GOFLAGS=-mod=readonly go build` | `github.com/caarlos0/env` |
| Java | Maven/Gradle Wrapper + `.java-version` | `./mvnw -B verify` / `./gradlew check` | Spring `@ConfigurationProperties` + Bean Validation |
| Kotlin | Gradle Wrapper + `.tool-versions` | `./gradlew check` | 同 Java |
| C/C++ | `CMakePresets.json` + vcpkg / Conan lock | preset 驱动 build | header-only env reader（自写） |

---

## 7. Devcontainer（optional trigger + handoff，不默认生成）

**默认不生成 Devcontainer 模板**。但在以下信号出现时**主动建议用户启用**：

| 触发信号 | 建议 |
|---|---|
| 检测到 `Dockerfile` + 多语言 monorepo（≥ 2 种语言 manifest） | 建议 Devcontainer 统一开发镜像 |
| 检测到 native dependency（`node-gyp` / `gcc` / `openssl-sys` / `libpq-dev`） | 建议 Devcontainer 避免本地环境 hell |
| 用户在 ASK 阶段报告 onboarding pain（"新人装环境要花一天"） | 强烈建议 Devcontainer |
| 团队 OS 混合（Windows + Linux + macOS）| 建议 Devcontainer 作为统一开发面 |

启用时的 handoff 路径：
- 让用户按 [Dev Containers spec](https://containers.dev/) 起草 `.devcontainer/devcontainer.json`
- 或建议未来由 `claude-env-bootstrap --update` 注入（标记 `devcontainer_pending = true` 到 manifest）
- **本 skill 不直接生成 `.devcontainer/devcontainer.json`**（避免做"半个 deploy 模板"）

---

## 8. 反模式

| 反模式 | 正确做法 |
|---|---|
| 在本 skill 里直接生成完整 Dockerfile / k8s / terraform / ansible 配置 | 只检测 + 路由出去（HANDOFF） |
| 默认强塞 Devcontainer | 仅在 §7 触发信号出现时建议 |
| 锁太死的版本（如 Node `20.11.0` 而不是 `20.11.x`） | 默认 minor pin，patch 不锁；安全更新自由 |
| 把真实 secret 写进 `.env.example` | `.env.example` 只放 `KEY=` 空值或 placeholder（如 `DATABASE_URL=postgres://user:pass@localhost:5432/db`，用户改本地）|
| 覆盖用户已有 `.gitattributes` / `.editorconfig` / `.env.example` | 检测到则 diff 给用户看，等用户决定 merge / skip |
| 用 `ARG` / `ENV` 传 build-time secret | 用 BuildKit `RUN --mount=type=secret,id=xxx,target=/tmp/xxx` |
| 假设 `.env` 自动同步到 CI / 生产 | 必须有 secret store 桥接，不能依赖 `.env` |
| 检测到 k8s manifests 后顺手帮用户写 `Deployment` / `Service` | 不写，只检测和 handoff |
| `.env.example` 只列 keys 但 docs 不说哪个是 secret / required | 必须配 `docs/env-contract.md` |

---

## 9. Hard Rules（不可违反）

1. ❌ **不生成完整部署配置**（Dockerfile / k8s manifests / terraform / ansible / systemd unit / nginx.conf）
2. ❌ **不覆盖现有 baseline 文件**（`.gitattributes` / `.editorconfig` / `.env.example` / CI workflow 任一已存在 → diff + user confirm，不直接 Write）
3. ❌ **不把 secret 值写进任何 commit 文件**（包括 `.env.example`、CI workflow、Dockerfile）
4. ❌ **不假设单一 OS / 单一部署目标**（多义时必须 ASK，不能猜）
5. ❌ **DETECT 阶段绝对不改文件**（只读、报告、路由）
6. ❌ **不静默执行 EXECUTE**（必须 PROPOSE → user confirm → EXECUTE）
7. ❌ **不假设"项目小所以不用部署一致性"**（即使是 prototype，CRLF / env validator / lockfile 也必须有；只有纯 .md 项目才完全跳过）

---

## 10. 与其他 skill 的接口

### 10.1 来向（谁触发本 skill）

| 来源 | 触发时机 |
|---|---|
| `claude-env-bootstrap` | SCAN 检测到 §2 激活条件，在 §5.5c 追加规则中触发 |
| `enterprise-qa-testing` | QA Static 层发现 CI 只跑 Linux 但目标 OS 含 Windows 时触发本 skill 补 matrix |
| `gsd-spec-phase` / `gsd-plan-phase` | spec 含 "跨平台" / "Windows 部署" / "Docker 部署" 等关键词时建议引入 |
| 用户主动调用 | 报告 "works on my machine" / "Windows 跟服务器不一致" / "Docker build 出来跟本地行为不同" |

### 10.2 去向（本 skill 路由到哪）

| 风险类别 | 路由目标 |
|---|---|
| Dockerfile / ENV secret 泄露 | `appsec-security-orchestrator`（CRITICAL） |
| compose / k8s ConfigMap-Secret 与 app schema 不一致 | `appsec-security-orchestrator` + 人工 review |
| CI smoke parity（cross-platform 测试缺失）| `enterprise-qa-testing`（Static + Smoke 层） |
| migration 工具缺失 / rollback 策略缺失 | `gsd-plan-phase`（作为 phase deliverable） |
| 完整 Dockerfile / k8s / terraform / nginx 配置 | 暂无 deploy-specialist skill → 人工 review，建议按 `templates/deploy-parity-checklist.md` 走 |
| Devcontainer 注入 | `claude-env-bootstrap --update` 未来扩展（标记 `devcontainer_pending`）|

### 10.3 与 GSD 主线

- 在 `gsd-plan-phase` 阶段：PLAN.md 应含 env parity 作为 phase deliverable（如果 §3 有 HIGH+ risk）
- 在 `gsd-verify-work` 阶段：走 `templates/deploy-parity-checklist.md` 作为 verify 子清单
- 在 `gsd-ship` 阶段：本 skill 的 Detected Risks 必须全部 RESOLVED / RISK-ACCEPTED 才能 ship

---

## 11. 参考

- Twelve-Factor App X. Dev/prod parity: <https://12factor.net/dev-prod-parity>
- Twelve-Factor App III. Config: <https://12factor.net/config>
- Twelve-Factor App IV. Backing services: <https://12factor.net/backing-services>
- npm-ci: <https://docs.npmjs.com/cli/v10/commands/npm-ci/>
- pip secure installs (`--require-hashes`): <https://pip.pypa.io/en/stable/topics/secure-installs/>
- Docker build secrets warning: <https://docs.docker.com/build/building/variables/>
- Docker build secrets (correct usage): <https://docs.docker.com/build/building/secrets/>
- Kubernetes Container env vars: <https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/>
- Dev Containers spec: <https://devcontainers.github.io/implementors/spec/>
- GitHub Actions matrix: <https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow>
- EditorConfig spec: <https://editorconfig.org/>

---

## 12. 一句话总结

> 不是"装一套部署模板"，而是"扫一下、说清差异、补最小契约、把深水区交给该接的人"。
> 本 skill 是"风险检测器 + 最小契约工 + 路由员"，不是"全栈部署生成器"。
