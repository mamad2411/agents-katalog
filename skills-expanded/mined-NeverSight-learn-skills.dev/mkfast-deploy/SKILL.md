---
name: mkfast-deploy
description: 把 mkfast-template / TanStarter 系项目部署到 Cloudflare Workers —— 自动检测实际启用的组件（D1 / R2 / Email / Better Auth / Stripe / Creem / Beehiiv / 通知 / 分析），动态裁剪部署步骤。Use PROACTIVELY whenever 用户提到部署、上线、deploy 到 Cloudflare、wrangler、pnpm deploy、推到生产、发布站点、CF Workers 上线 —— 即使用户没明确说 "mkfast"，只要项目含 `wrangler.jsonc` + `@tanstack/react-start` 或 `drizzle-orm` / `better-auth` 任一，就**优先使用此 skill 而非通用 wrangler / cloudflare skill**（本 skill 更懂 mkfast 的占位符、logpush 默认值陷阱、enable=false 陷阱、tailoring 策略）。SKIP when 项目明显不是 mkfast-template 派生（无 wrangler.jsonc + 无 @tanstack/react-start）→ 改用通用 wrangler skill。触发词：「部署到 Cloudflare」「deploy to Cloudflare」「mkfast 部署」「TanStarter 上线」「wrangler deploy」「准备部署」「上线前要做什么」「deploy 流程」「pnpm deploy」「推到 Cloudflare 生产」「ship to CF」「go live」「发布 CF Workers」「production deploy」「把网站上线」「上线我的 SaaS」。
user-invocable: true
---

# Mkfast Deploy

把 `mkfast-template`（TanStarter 系）项目部署到 Cloudflare Workers。**核心价值：根据项目实际启用的组件动态裁剪部署步骤**，避免照搬完整版文档导致裁剪版项目跑空命令甚至报错。

## 适用范围

**是**：基于 `mkfast-template` 模板派生的项目，包括完整 SaaS 形态、裁剪版博客、或任意中间形态。

**不是**：任意 Cloudflare Workers 项目（这种情况用 `wrangler` skill 就够）。

判断标志（满足任一即可）：
- 根目录有 `wrangler.jsonc` + `package.json`
- `package.json` 含 `wrangler` + `@cloudflare/vite-plugin` + `@tanstack/react-start` 中任一
- 目录里有 mkfast 特征文件：`drizzle.config.ts` / `src/server.ts` / `src/db/auth.schema.ts`

## 重要原则

1. **先评估再执行** — 任何 deploy 命令前必须完成 Phase 1，生成裁剪后的步骤清单。直接 `pnpm run deploy` 不算工作完成
2. **不要照搬官方文档** — mkfast 完整版文档假设了 D1 + R2 + secret bulk，**裁剪版项目跑这些步骤会报错或浪费**（例如无 drizzle 配置时跑 `db:migrate:remote` 会找不到 migrations 目录）
3. **secret bulk 是 gating step** — 项目有服务端 secret（`.env.production` 含非 `VITE_*` 变量）必须在 deploy 前推到 Cloudflare，否则运行时崩溃
4. **生产部署需明确确认** — Phase 3 执行 `pnpm run deploy` 前必须用 AskUserQuestion 让用户最终确认（影响生产域名）
5. **域名状态决定 routes 策略** — 域名未托管 Cloudflare 时不能直接 deploy 含 `routes` 的配置，需先去掉 routes、deploy 拿默认域名、再到 Dashboard 绑定（详见 `references/tailoring.md` Routes 配置策略表）
6. **安全优先** — `.env*` 必须进 `.gitignore`；**对话 / 截图 / Slack / commit message 中出现过的 secret 一律视为已泄漏**，立即 rotate（见 Phase 1.5 安全 baseline + Phase 4 Secret rotation 提醒）
7. **模板占位符必查** — mkfast-template 派生项目的 `wrangler.jsonc` 有 **4 处模板默认值必改**（`name` / `routes.pattern` / `database_id` / `bucket_name`）+ 1 处必关（`logpush: true` 在 Free/Pro plan 必报 code 10023）。见 `references/components.md` §0 占位符识别表；**不查就 deploy 会写到模板原作者的 D1 或 deploy 失败**

## 工作流（4 阶段）

### Phase 1 — 自动评估（只读）

**Step 1.0（必做，block 后续进度）**：对照 `references/components.md` §0 模板默认占位符识别表做 `wrangler.jsonc` + `package.json` diff。**任何未替换的模板默认值**——`name="mkfast-template"` / `routes[0].pattern="demo.tanstarter.dev"` / `database_id="dc34f04a-3445-4b5c-bf61-c4ec2328e239"` / `r2.bucket_name="mkfast-template"` / `logpush: true`——都直接 **block 进 Phase 2**。

这是**本 skill 最重要的前置关**：不查就 deploy 会（a）写到模板原作者的 D1 数据库；（b）deploy 失败报 code 10023（logpush 企业功能）；（c）routes 冲突。所有这些都是 mkfast-template 派生项目首次部署**几乎必踩**的坑。

读取项目状态，识别"项目画像"。**最少读这 5 个文件**：

| 读什么 | 提取什么 |
| --- | --- |
| `wrangler.jsonc` | `name` / `routes` / `d1_databases` / `r2_buckets` / `send_email` / 其他 binding |
| `package.json` | `name` + 依赖中是否含 `drizzle-orm` / `better-auth` / `stripe` / `creem` / `@beehiiv/sdk` |
| `.env.example` | 全部支持的变量分类（参照 `references/components.md` 检测信号表） |
| `.env.production`（若存在） | 已配的变量 vs 未填（空字符串）的变量 |
| `.env.local`（若存在） | `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` 是否就绪 |

按 `references/components.md` 的 12 类组件逐一判断启用与否，生成"项目画像"输出（格式参照 `templates/deploy-checklist.md`）：
- 项目形态：完整 SaaS / 裁剪版博客 / 中间形态
- 启用组件勾选表
- 环境变量缺口表
- 裁剪后的待执行步骤清单（步数）

### Phase 1.5 — 安全 baseline（只读 + 必要时新建 .gitignore）

部署前必查 4 项，缺哪个补哪个，**不让 secret 流出仓库是底线**：

| 项 | 检查命令 | 不通过时的修复 |
| --- | --- | --- |
| `.gitignore` 存在且含 `.env*` | `grep -E "\.env" .gitignore` | 不存在则**立即创建**含 `.env`、`.env.local`、`.env.*.local`、`.env.production`、`.dev.vars` |
| .env.local 不在 git history | `git log --all --full-history -- .env.local` 输出为空 | 已被 commit 过 → 用 `git filter-repo` 清掉 + **立即 rotate** 涉及的所有 secret |
| `wrangler.jsonc` 无硬编码 secret | grep 不应见 `sk_live_` / `re_live_` / `whsec_` 等 | 删硬编码，全走 `wrangler secret put` |
| `.env.production` 无明文 production secret 准备 commit | `cat .gitignore | grep .env.production` | 生产 secret 走 `wrangler secret bulk` 不进 git |

**裁剪版项目无 .gitignore 时**（见过项目还没 git init 但已经写了 `.env.local` 的情况），先建 `.gitignore` 再继续 Phase 2。

### Phase 2 — 决策点（AskUserQuestion）

基于 Phase 1 / 1.5 画像问用户，按情况选 1-5 题：

- **目标用户地域**（强烈推荐先问）：全球 / 仅海外 / **主要面向中国大陆** / 国内+海外都要
  - 若选中国大陆 → ⚠️ 警告：Cloudflare 在中国大陆**没有 PoP 节点**（除非企业版 + 京东云合作），访问体验时通时不通；**建议参考 `references/cn-access.md` 切换方案**（EdgeOne / Vercel + 国内 CDN / 双部署）
- **域名状态**（必问）：`<domain>` 是否托管在 Cloudflare？三选项：已托管 / 未托管（先用默认 *.workers.dev）/ 还没买
- **D1 / R2 资源**（仅完整版）：是否已在 Cloudflare 创建？如未创建，是否同意现在 `wrangler d1 create` / `wrangler r2 bucket create`？
- **可选功能**：Giscus / 分析 / Webhook / Crisp 是否本次启用？
- **CI 自动化**：是否同步配 GitHub Actions auto-deploy？

裁剪决策树详见 `references/tailoring.md`。

### Phase 3 — 执行（按裁剪后清单）

**Step 0 — Sanity（强烈推荐）**：

```bash
# 清掉过往 dev 留下的 dist + .vite 缓存
# 避免 chokidar 在 dev 中 EINTR 报错（曾导致 dev server 起不来）
rm -rf dist .vite node_modules/.vite

# 验证 wrangler 凭证已加载（推荐用 .env.local + 一次 source 而非 wrangler login）
# wrangler 不会自动读 vite 系的 .env.local，必须 export 到当前 shell：
set -a && . ./.env.local && set +a && pnpm wrangler whoami
```

> 推荐在 `package.json` 里加 alias 一次解决：
> ```json
> "deploy:cf": "set -a && . ./.env.local && set +a && pnpm run build && wrangler deploy"
> ```
> 之后用 `pnpm deploy:cf` 即可，避免每条 wrangler 命令都要 export。

**所有项目都要做**：
1. `pnpm wrangler whoami` 验证登录（未登录时检查 `.env.local` 凭证或提示 `wrangler login`）
2. 检查 token 权限：按启用组件查 `references/components.md` 的 §API Token 权限完整矩阵（Workers Scripts / D1 / R2 / Workers Routes / Email / KV 等），缺权限直接到 Dashboard → My Profile → API Tokens 编辑现有 token 加权限（不用重建）
3. **AskUserQuestion 最终确认** → `pnpm run deploy`

**仅当检测到对应组件时做**（按 `references/components.md` 详细步骤）：
- (有 D1) `pnpm wrangler d1 create <name>` → 写回 `wrangler.jsonc` 的 `database_id` → `pnpm db:migrate:remote`
- (有 R2) `pnpm wrangler r2 bucket create <name>` → 写回 `bucket_name`
- (有 send_email) Cloudflare Dashboard 启用 Email Routing + 验证 from 邮箱
- (有 Better Auth) `pnpm dlx @better-auth/cli@latest secret` 生成 → `wrangler secret put BETTER_AUTH_SECRET`
- (有服务端 secret) `pnpm wrangler secret bulk .env.production`
- (有支付) Stripe/Creem live key + price ID + webhook endpoint 配置

**仅当用户在 Phase 2 选了 CI**：
- 创建 `.github/workflows/deploy.yml` + 提示去 GitHub Settings → Secrets 加 `CLOUDFLARE_ACCOUNT_ID` / `CLOUDFLARE_API_TOKEN` / 全部 `VITE_*`

### Phase 4 — 验证

```bash
# 在线验证（首次）
curl -s -o /dev/null -w "HTTP %{http_code} | size %{size_download}B | time %{time_total}s\n" https://<domain>

# 5-10 秒后再跑一次（验证缓存 + 二次访问性能）
curl -s -o /dev/null -w "HTTP %{http_code} | size %{size_download}B | time %{time_total}s\n" https://<domain>
```

预期：

| 指标 | 首次 | 二次（warm） |
| --- | --- | --- |
| HTTP code | 200 | 200 |
| size | > 几 KB（SSR 渲染成功）| 同首次或更小（命中缓存）|
| time | < 3s（含冷启动 + CDN 传播） | < 500ms（PoP 命中）|

附加检查：
- deploy 输出里 `Total Upload: X KiB / gzip: Y KiB` → `Y < 3072`（3 MB 免费计划上限）
- Cloudflare Dashboard → Workers & Pages → `<worker-name>` → Logs → 无 runtime error
- 自定义域名首次访问可能有 30s CDN 传播延迟

**上线后 30 分钟观察清单**：

| 检查项 | 命令 / 位置 | 预期 |
| --- | --- | --- |
| 5xx 响应率 | Dashboard → Workers & Pages → `<worker>` → Logs → 筛 status >= 500 | 0 条 |
| 版本号匹配 | Dashboard → `<worker>` → Deployments | 最新 Version ID 与 deploy 输出一致 |
| Analytics 流量 | Dashboard → `<worker>` → Analytics（或第三方 RUM） | 有正常请求进入 |
| D1 表访问（若启用） | `wrangler d1 execute <name> --remote --command "SELECT COUNT(*) FROM user"` | 返回数字不报错 |
| R2 bucket 访问（若启用） | `wrangler r2 object list <bucket>` | 列表返回不报错 |

**回滚方案**：

```bash
# 列出历史版本
pnpm wrangler deployments list

# 回滚到上一版（不传 id）
pnpm wrangler rollback

# 回滚到指定版本
pnpm wrangler rollback <version-id>
```

注意：
- D1 migrations 是 **forward-only**，schema 回滚需要手动写 down migration 并 `wrangler d1 execute` 应用
- R2 无版本概念，按需从备份恢复（部署前做过 `wrangler r2 object get` 备份才行）
- Secret 回滚：`wrangler secret put <KEY>` 覆盖为旧值，或 `wrangler secret delete <KEY>` 清除

**Secret rotation 提醒（重要）**：
如果本次部署过程中 token / API key / database secret 在以下任一渠道**出现过**：
- Claude / ChatGPT 等对话历史
- Slack / Lark / WeChat 消息
- 截图 / 录屏
- 代码注释 / commit message

→ **立即去 Cloudflare Dashboard / 第三方服务后台 roll**（生成新值替代旧值）。token 字符串变了的，记得更新 `.env.local` 和 GitHub Secrets。

报错排查见 `references/troubleshoot.md`。

## 输出格式

每阶段结束后给用户简洁汇报，例：

### Phase 1 项目画像输出（example）

```markdown
## Phase 1 — 项目画像

**形态**：裁剪版博客
**启用组件**：无（纯 SSR + 博客）
**待执行步骤**：2 步（whoami + deploy）
**跳过**：D1 / R2 / Email / Auth / Pay / Secret bulk / Migrate
```

### 最终 checklist（example）
```
✅ wrangler 登录（账户 zhihui）
✅ pnpm run deploy（gzip 471 KB / 17ms 启动）
✅ HTTP 200 验证通过
⚠️ 可选未启用：Giscus / Plausible
```

## 工具文件

- **`references/components.md`** — mkfast-template 12 类组件检测信号 → 部署步骤映射表
  - §0 模板默认占位符识别表（Phase 1 Step 1.0 必查）
  - §API Token 权限完整矩阵（按启用组件勾权限的速查表）
  - §没 .env.example 时如何反推 secret 列表（读 src/env/*.ts 反推）

- **`references/tailoring.md`** — 完整版 vs 裁剪版 vs 中间形态裁剪决策树 + 决策矩阵速查表
  - §陷阱：`enable=false` 仍需保留 D1 binding（module-load-time 调用 `getDb()`）
  - §澄清：`enable=false` ≠ tree-shake（enable 只控 UX，bundle 仍含 SDK）

- **`references/troubleshoot.md`** — 11 个常见报错 + 排查命令 + 修复（含 #10 Logpush / #11 already exists）

- **`references/cn-access.md`** — 中国大陆访问优化 4 档方案（Cloudflare 设置 / 图床 / EdgeOne 反代 / 双部署）

- **`templates/deploy-checklist.md`** — Phase 1 项目画像输出模板 + 最终汇报模板 + AskUserQuestion 模板

- **`templates/stub-no-d1-r2.md`** — 彻底关闭 D1/R2 的代码 stub 模板（4 文件改动可粘贴版本）
