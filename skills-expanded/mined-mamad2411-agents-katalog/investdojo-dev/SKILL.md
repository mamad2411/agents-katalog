---
name: investdojo-dev
description: >-
  InvestDojo 量化投资平台开发辅助 Skill。提供项目架构知识、全栈启动/重启自动化、
  数据种子脚本执行、新页面/因子脚手架生成、项目进度同步、常见问题排障指南。
  当用户涉及 InvestDojo 项目的开发、调试、部署、数据维护等任务时，
  此 Skill 应被触发。关键触发词包括：启动服务、重启、健康检查、种子数据、
  创建页面、创建因子、K线、回测、因子库、Docker、Supabase、微服务、
  更新进度、同步进展、项目进度。
---

# InvestDojo 开发辅助

## 项目概述

InvestDojo 是一个量化交易模拟平台，采用 pnpm + Turborepo monorepo 架构：
- **前端**: Next.js 15 + React 19 + Tailwind CSS 4（`:3000`）
- **Python 微服务**: 6 个 FastAPI 服务（`:8001`~`:8006`）
- **基础设施**: PostgreSQL + PostgREST + GoTrue + Kong（Supabase Lite）+ Redis + MinIO（**全部合并在 `infra/supabase-lite/docker-compose.yml` 单一文件**，一条 `docker compose up -d` 拉起 6 个容器）。Python 微服务已改为**直连 PostgreSQL**（localhost:5432），rest/auth/kong 三个容器仅前端使用。

项目根目录：当前工作区下的 `investdojo/` 子目录。

## 开发-测试协作工作流（核心）

**每次开发任务完成后，必须自动执行以下测试流程。**

### 流程总览

```
用户需求 → 需求拆解 → 多角色并行开发（Team 模式） → 自动化测试 → E2E 浏览器测试 → 报告
```

### 角色体系

#### 开发角色

| 角色 ID | 角色名 | 职责范围 | 涉及目录 |
|---------|--------|----------|----------|
| `fe-dev` | 前端开发 | React 页面/组件、Tailwind 样式、Next.js 路由、SDK 调用 | `apps/web/src/`, `packages/ui/` |
| `api-dev` | API / 后端开发 | FastAPI 路由、业务逻辑、Pydantic 模型、SDK 客户端 | `python-services/*-svc/routers/`, `packages/api/src/` |
| `auth-dev` | 鉴权专员 | Supabase Auth 集成、GoTrue 配置、RLS 策略、JWT、用户权限校验 | `infra/supabase-lite/config/`, `infra/supabase-lite/init/`, `apps/web/src/lib/supabase/`, `apps/web/src/lib/sdk.ts`(userId 部分) |
| `data-eng` | 数据工程师 | 数据采集脚本、种子数据、爬虫、数据库 Schema、数据迁移、BaoStock/AKShare | `scripts/`, `python-services/data-svc/`, `infra/supabase-lite/init/*.sql` |
| `infra-ops` | 基础设施 | Docker Compose、Kong 配置、Redis/MinIO、服务编排、端口管理 | `infra/`, `python-services/Procfile`, `python-services/Makefile` |

#### 测试角色

| 角色 ID | 角色名 | 职责范围 |
|---------|--------|----------|
| `tester-unit` | 单元测试 | pytest 单元测试、vitest 组件测试 |
| `tester-e2e` | E2E 测试 | agent-browser 浏览器自动化、API 冒烟测试 |

### 第零阶段：需求 / 任务登记（强制）⭐

**每当你新增一个需求或拆解出一个任务，必须同时做两件事**（避免排单和进度滞后）：

1. **登记排单（backlog）**：把需求/任务写入 `progress-data.json` 的 `backlog` 数组，
   含 `id` / `title` / `epic` / `priority`(P0|P1|P2) / `status`(todo|doing|done) / `owner` / `created`。
2. **登记进度（log）**：调用 `sync_progress.ps1 -Backlog "..."` 一步完成上述两件事
   （脚本同时往 `backlog` 追加条目、并写入当天 `log` 进展）。

示例：
```powershell
powershell -File "<skill_base>/scripts/sync_progress.ps1" `
  -Backlog "因子批量导出 Excel" -BacklogEpic 3 -BacklogPriority P1 -BacklogOwner api-dev
```

> 禁止「只开发不登记」：backlog 是排期与分工的单一事实来源，进度文档是对外展示来源。

### 第一阶段：需求拆解与角色分配

收到用户需求后，先分析涉及哪些层：

**示例 — "添加因子发布/撤销功能"**：
- `api-dev`：后端添加 publish/unpublish 接口
- `fe-dev`：前端添加发布/撤销按钮
- `auth-dev`：确保 owner 权限校验、X-User-Id header 传递
- → 三个角色需要并行工作

**示例 — "采集日 K 线数据"**：
- `data-eng`：编写/运行种子脚本
- `infra-ops`：确保 DB 连接和存储
- → 两个角色，`data-eng` 主导

**示例 — "修复 CORS 问题"**：
- `infra-ops`：修改 Kong 配置
- → 单角色

### 第二阶段：多角色并行开发（Team 模式）

当需求涉及 2 个以上角色时，使用 Team 模式并行开发：

```
1. 创建 Team（如 "feature-xyz"）
2. 为每个角色 spawn 一个 Team Member
3. 角色之间通过 send_message 共享信息
4. 所有角色完成后进入测试阶段
```

#### 角色间通信场景

| 场景 | 发送方 | 接收方 | 通信内容 |
|------|--------|--------|----------|
| 新增 API 接口 | `api-dev` | `fe-dev` | 接口路径、参数、返回格式 |
| 需要新 DB 字段 | `api-dev` | `data-eng` | 表名、字段名、类型 |
| 权限模型变更 | `auth-dev` | `api-dev` + `fe-dev` | RLS 策略、header 约定、userId 获取方式 |
| 新增 Docker 服务 | `infra-ops` | 全员广播 | 端口、环境变量 |
| 数据格式变更 | `data-eng` | `api-dev` | 表结构、字段类型、数据范围 |
| 前端需要新接口 | `fe-dev` | `api-dev` | 需要的数据结构和查询参数 |

#### Team 协作示例

```
# 全栈需求："为因子添加评分功能"

Team: factor-rating
├── fe-dev:    "在因子详情页添加评分 UI（星级组件 + 平均分显示）"
├── api-dev:   "在 feature-svc 添加 POST/GET /factors/{id}/ratings 接口"
├── auth-dev:  "确保只有登录用户可以评分，每人只能评一次"
├── data-eng:  "创建 factor_ratings 表，添加 RLS 策略"
│
│ 通信流:
│   data-eng → api-dev:  "factor_ratings 表已创建，字段: id, factor_id, user_id, score(1-5), created_at"
│   api-dev → fe-dev:    "接口已完成: POST /factors/{id}/ratings {score:int}, GET 返回 {avg, count, user_rating}"
│   auth-dev → api-dev:  "权限用 X-User-Id header，记得调 ensureUserId()"
│   auth-dev → fe-dev:   "未登录时评分按钮要禁用，提示登录"
```

### 第三阶段：自动化测试（开发完成后立即执行）

开发完成后，**不等用户指示**，立即执行以下测试：

#### Step 1: 判断测试范围

根据本次开发变更的文件，确定测试范围：

| 变更目录 | 测试动作 |
|----------|----------|
| `python-services/` | 运行 `pytest tests/ -v` |
| `apps/web/src/` | 运行 `pnpm --filter @investdojo/web test -- --run` |
| `packages/api/` | 两者都运行 |
| `infra/` | 运行 `scripts/health_check.ps1` |
| `scripts/` | 运行对应脚本 + DB 验证 |
| 任何改动 | 运行 API 冒烟测试 |

#### Step 2: 运行自动化测试

```powershell
cd investdojo/python-services
$env:PYTHONPATH = "."
python -m pytest tests/ -v --tb=short
```

```powershell
cd investdojo
pnpm --filter @investdojo/web test -- --run
```

#### Step 3: API 冒烟测试

用 curl 或 Invoke-WebRequest 验证相关 API 端点返回 200。
参见 `references/testing.md` 中的端点列表。

#### Step 4: 数据验证（如涉及数据变更）

```powershell
docker exec -it investdojo-db psql -U postgres -d postgres -c "SELECT count(*) FROM <table>;"
```

### 第四阶段：E2E 浏览器测试（涉及前端变更时）

当变更涉及前端页面时，使用 `agent-browser` Skill 执行浏览器测试：

1. **确认前端服务运行中**（http://localhost:3000 可达）
2. **打开变更涉及的页面**
3. **截图验证**关键 UI 元素
4. **交互测试**：点击、输入、导航等
5. **录制视频**（如有交互操作）
6. **截图对比**操作前后状态

测试清单参见 `references/testing.md`。

当前环境为 Windows，`agent-browser` 使用 `--headed` 模式。

### 第五阶段：测试报告

测试完成后，向用户汇报：

```
## 测试报告

### 变更摘要
- [描述本次开发了什么]
- [涉及角色: fe-dev / api-dev / auth-dev / data-eng / infra-ops]

### 自动化测试
- Python 单元测试: ✅ 通过 (X/X)
- 前端测试: ✅ 通过 / ⏭ 跳过（无测试文件）
- API 冒烟: ✅ 全部 200

### E2E 浏览器测试
- [页面名] 页面加载: ✅
- [功能名] 交互测试: ✅
- [截图]

### 发现的问题
- （无 / 列出问题及建议修复方案）
```

如果测试发现 bug，**立即修复**（分配给对应角色），修复后重新运行失败的测试直到通过。

### 第六阶段：同步进度文档（强制）

每次开发任务完成并通过测试后，**必须同步项目进度**，保证进度文档不滞后：

1. 更新数据源 `investdojo/apps/web/src/app/admin/progress/progress-data.json`
   - 快速追加：`powershell -File "<skill_base>/scripts/sync_progress.ps1" -Title "..." -Items "项1,项2" -Status "..." -Files "..."`
   - 或直接编辑 Epic/模块进度字段
2. `sync_progress.ps1` 写入 JSON 后会**自动调用 `generate_progress_doc.ps1`**，重新生成可读文档 `investdojo/docs/ops/progress-log.md`
3. 提交时一并提交 `progress-data.json` 与 `progress-log.md`（两者须保持同步）

> 禁止「只改代码不更新进度」：进度文档是对外展示（`/admin/progress`、`/overview`）与团队协作的单一事实来源。

## 核心工作流

### 1. 启动全栈开发环境

执行 `scripts/start_all.ps1` 脚本来一键启动全栈：

```powershell
powershell -File "<skill_base>/scripts/start_all.ps1"
```

可选参数：
- `-SkipDocker`：跳过 Docker 容器（已运行时）
- `-SkipPython`：跳过 Python 微服务
- `-SkipFrontend`：跳过前端

**手动启动顺序**（当脚本不适用时）：

1. Docker 基础设施（单一 compose，含全部 6 容器）：
   ```powershell
   cd investdojo/infra/supabase-lite && docker compose up -d
   ```

2. Python 微服务：
   ```powershell
   cd investdojo/python-services
   $env:PYTHONPATH = "."
   # 每个服务一个终端：
   python -m uvicorn main:app --app-dir data-svc --host 0.0.0.0 --port 8006 --reload
   python -m uvicorn main:app --app-dir feature-svc --host 0.0.0.0 --port 8001 --reload
   # ... 同理 train-svc:8002, infer-svc:8003, backtest-svc:8004, monitor-svc:8005
   ```

3. 前端：
   ```powershell
   cd investdojo && pnpm dev
   ```

### 2. 健康检查

执行 `scripts/health_check.ps1` 检查所有服务状态：

```powershell
powershell -File "<skill_base>/scripts/health_check.ps1"
```

### 3. 运行测试

执行 `scripts/run_tests.ps1`：

```powershell
powershell -File "<skill_base>/scripts/run_tests.ps1"             # 全部
powershell -File "<skill_base>/scripts/run_tests.ps1" -Scope python   # 仅 Python
powershell -File "<skill_base>/scripts/run_tests.ps1" -Scope frontend # 仅前端
powershell -File "<skill_base>/scripts/run_tests.ps1" -Scope api      # 仅 API 冒烟
```

### 4. 数据种子操作

数据脚本位于 `investdojo/scripts/`。详细索引参见 `references/scripts_index.md`。

**常见操作**：

```powershell
cd investdojo/python-services
$env:PYTHONPATH = "."

# 同步股票代码
python ../scripts/seed_symbols_local.py

# 种子 5 分钟 K 线
python ../scripts/seed_5min.py

# 种子因子定义（65 个）
python ../scripts/seed_factors_extended.py

# 回填因子计算值
python ../scripts/backfill_factors.py

# 日常增量更新
python ../scripts/update_daily_klines.py
python ../scripts/update_market_snapshots.py
```

**注意事项**：
- 所有脚本需要 `PYTHONPATH=.`（指向 `python-services/`）
- 脚本读取 `python-services/.env` 中的 Supabase 连接信息
- BaoStock 数据源在非交易时间（周末/节假日/盘后）可能返回空数据

### 5. 创建新页面

参考 `references/page_patterns.md` 获取完整模式。

**步骤**：

1. 创建路由文件 `apps/web/src/app/<name>/page.tsx`
2. 使用 `"use client"` 指令
3. 导入 `MainNav` 组件（全局导航栏）
4. 使用 `sdk` 调用后端 API
5. 写操作前调用 `await ensureUserId()`
6. 遵循 Raycast 设计系统（`rc-` 前缀 CSS 类）

### 6. 创建新因子

**前端入口**: `/factors/new` 页面

**后端 API**: `POST /api/v1/factors`（feature-svc :8001）

**DSL 公式示例**：
- `RSI(14) < 30` — 超卖信号（boolean）
- `SMA(5) cross_up SMA(20)` — 均线金叉（boolean）
- `(close - SMA(20)) / SMA(20)` — 偏离率（scalar）
- `RANK(volume)` — 成交量排名（rank）

**批量种子因子**: 运行 `seed_factors_extended.py`

### 7. 项目架构查询

查阅 `references/architecture.md` 获取：
- 完整目录结构和服务映射
- 端口清单（3000, 5432, 6379, 8000~8006, 9000~9001）
- 凭据信息
- 网络架构（localhost / 局域网，IP 会变动，统一用 localhost）
- 数据库表结构
- SDK 架构和认证流程

### 8. 同步项目进度

每次开发任务完成后，**必须**同步项目进度，保证进度不滞后。

**唯一数据源**: `investdojo/apps/web/src/app/admin/progress/progress-data.json`
（同时驱动 `/admin/progress` 页面与 `/overview` 全景页，请勿直接改页面代码）

**方式 1: 脚本同步（推荐，自动连带生成文档）**

```powershell
powershell -File "<skill_base>/scripts/sync_progress.ps1" `
  -Title "因子库优化" `
  -Items "新增批量删除,修复排序bug,优化搜索性能" `
  -Status "因子库趋于完善" `
  -Files "feature-svc/routers/factors.py,apps/web/src/app/factors/"
```
`sync_progress.ps1` 写入 JSON 后会**自动调用 `generate_progress_doc.ps1`**，重新生成 `investdojo/docs/ops/progress-log.md`。

**方式 2: 仅重新生成文档**（JSON 已手动改好时）

```powershell
powershell -File "<skill_base>/scripts/generate_progress_doc.ps1"
```

**方式 3: 直接编辑 JSON**（更灵活，适合更新 Epic/模块进度）

- `epics[].done` — 更新 Epic 完成任务数
- `modules[].progress` / `modules[].status` — 更新模块进度百分比和状态
- `modules[].details` — 更新子项完成情况（用"完成"/"未开始"后缀标记）
- `log[]` — 在数组头部插入新的每日进展条目

**两文件须同步提交**：`progress-data.json`（数据源）+ `docs/ops/progress-log.md`（可读文档，由脚本从 JSON 生成，勿手改）。

## 常见问题排障

### CORS 错误
Kong 配置文件: `investdojo/infra/supabase-lite/config/kong.yml`
确认 `Access-Control-Allow-Origin` 包含前端地址（如 `http://localhost:3000`）。
修改后重启 Kong: `docker restart investdojo-kong`

### PostgREST 401/403
1. 检查 `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY` 是否一致
2. 检查 RLS 策略是否正确
3. `docker logs investdojo-rest` 查看错误

### Python 服务连接失败
1. 确认 `python-services/.env` 中 `PG_HOST=localhost` / `PG_PORT=5432` / `PG_PASSWORD`（与 supabase-lite db 一致）
2. 确认 Docker 容器 `investdojo-db` 正在运行且 healthy: `docker ps` / `docker inspect investdojo-db`
3. 确认端口 5432 未被占用: `netstat -ano | findstr :5432`

### 前端看不到数据
1. 确认 `apps/web/.env.local` 中 URL 使用 `localhost`（IP 会变动，不要用硬编码局域网 IP）
2. 浏览器控制台检查网络请求
3. 确认 Python 服务正在运行

### userId 不生效（写操作 403）
`sdk.ts` 通过 `getSession()` 缓存用户 ID。写操作前必须 `await ensureUserId()`。
如果仍然失败，检查 Supabase Auth 是否正常: `http://localhost:8000/auth/v1/health`

## 重要约定

- **IP 地址**: 前端与 Python 服务统一使用 `localhost`（本机 IP 为 DHCP 分配会变动，硬编码局域网 IP 会导致连接失败）
- **data-svc 端口**: 8006（非 8000，避免与 Kong 冲突）
- **PYTHONPATH**: Python 脚本运行时必须设置 `$env:PYTHONPATH = "."`
- **pnpm**: 使用 pnpm 9+，不要用 npm/yarn
- **Node.js**: 要求 >= 20
- **Python**: 要求 >= 3.11，用 uv 管理依赖
- **测试**: 每次开发完成后必须运行对应范围的自动化测试和 E2E 验证
- **角色协作**: 多角色开发时使用 Team 模式，通过 send_message 共享接口约定、数据格式、权限要求等关键信息
