# XForge — AI 协作入口

> 面向管理系统的 Monorepo 模板。本文件是 AI agent 的持久记忆，每次会话自动加载。**改代码前先读这里。**

---

## 1. 项目结构

```
xforge/
├── admin-web/                      Vue 3 管理端
│   ├── src/components/design-system/   Preset 门面（核心抽象）
│   │   ├── presets/minimal/            极简风预设（默认激活）
│   │   ├── presets/soft-brutal/        柔和新粗野风预设
│   │   ├── generated/                  脚本生成的映射（勿手改）
│   │   └── contracts/                  Preset 无关的 Props/Emits 契约
│   ├── src/components/ui/              shadcn-vue 原语（仅 Preset 内部用）
│   └── src/components/shared/          品牌图标/图表等风格无关设施
├── server/                         Spring Boot Maven 多模块
│   ├── server-common/              纯 JDK（零 Spring），统一响应/错误包络
│   ├── server-core/                 技术底座（security/mybatis-plus/web/flyway）
│   ├── server-system/               业务域（account/tenant/auth/role/menu/dept/...）
│   └── server-admin/                唯一可执行应用（聚合入口）
├── docs/                           架构契约 + 风格规范
└── admin-web/template.config.json  Preset 元数据（contractVersion / activeStyle）
```

## 2. 4A 账号体系（后端核心）

### 设计原则

身份（Account）/ 认证（Authentication）/ 授权（Authorization）/ 审计（Audit）四层职责用独立表拆开。`xf_user` / `xf_user_role` 已彻底废弃——**从未创建**，全链路无引用。

### 身份层表（拦截器白名单，不带 tenant_id 列）

| 表 | 用途 |
| --- | --- |
| `xf_account` | 账号主表。`email_normalized` 全局唯一，不存密码。`lifecycle_status` 0-5 是唯一权威状态 |
| `xf_account_credential` | 认证凭据。`credential_type` 可插拔（PASSWORD / SMS_OTP / WECHAT / LDAP / TOTP）。连续失败写 `locked_until`（临时锁定，区别于账号级冻结） |
| `xf_account_lifecycle_log` | 生命周期审计。append-only，不可变不可删。每次状态/权限变更必须写一条 |
| `xf_tenant` | 租户表 |
| `xf_tenant_member` | 账号-租户多对多关联。一个账号可加入多个租户 = 多 workspace 登录 |
| `xf_tenant_member_role` | 租户内多角色绑定 |
| `xf_role_template` | 角色模板（平台创建租户时复制到 `xf_role`） |
| `xf_platform_user` | 平台超管（独立身份，不与 `xf_account` 混用） |
| `xf_platform_role` / `xf_platform_user_role` / `xf_platform_role_menu` | 平台角色体系 |

### 业务层表（拦截器自动注入 tenant_id）

`xf_role` / `xf_dept` / `xf_menu` / `xf_role_menu` / `xf_role_dept` / `xf_dict_type` / `xf_dict_data` / `xf_config` / `xf_notice` / `xf_notice_read` / `xf_job` / `xf_job_log` / `xf_file` / `xf_file_chunk` / `xf_oper_log` / `xf_login_log` / `xf_login_session` / `xf_logininfor` / `xf_open_app` / `xf_open_app_secret`

### 登录流程

```
POST /api/v1/auth/login  { email, password }

1. email 查 xf_account → 不存在 = 401 通用提示（防枚举）
2. lifecycle_status 检查：冻结(3)/离职(4)/已注销(5) → 明确拒绝
3. xf_account_credential PASSWORD 校验：
   - locked_until 未过期 → 锁定提示
   - BCrypt 失败 → fail_count++ → 达阈值写 locked_until + lifecycle_log
   - 成功 → fail_count 清零
4. xf_tenant_member 列 workspace：
   - 0 个 → "账号未被邀请到任何租户"
   - 1 个 → 直接签发 token(tid=租户)
   - N 个 → 返回 workspace 列表（不签发 token）
5. 待激活(PENDING) → 自动流转为正常(ACTIVE)
6. 更新 last_login_at/ip

POST /api/v1/auth/select-workspace  { accountId, tenantId }  → 换发 token
POST /api/v1/platform/auth/login    { username, password }    → 平台超管独立登录
```

### 账号生命周期状态机

```
[0 待激活] ──(首次登录)──▶ [1 正常] ◀────────────────┐
                               │  │                  │
         (连续失败超限)        │  │ (管理员冻结)      │(管理员解冻)
                               ▼  ▼                  │
                         [2 锁定] [3 冻结]───────────┘

[1/2/3] ──(离职)──▶ [4 离职]
[1/2/3/4] ──(注销)──▶ [5 已注销]（不可逆）
```

### 不可违反的约束

1. 任何写 `xf_account.lifecycle_status` 或 `xf_tenant_member_role` 的操作，**必须**经 `AccountLifecycleService` 写 `lifecycle_log`。
2. 角色授予前**必须**校验 `role.tenant_id == tenant_member.tenant_id`。
3. 平台 token 不能访问租户 API，反之亦然（`PlatformTokenIsolationFilter`）。
4. **禁止使用 `@InterceptorIgnore`**——身份层表走拦截器白名单。

## 3. 后端技术约定

### 模块依赖

```
server-common（零 Spring）→ server-core → server-system → server-admin
```

新业务域与 `server-system` 平级，只依赖 `server-core`。

### 请求生命周期

```
RequestContextFilter (HIGHEST_PRECEDENCE) → traceId/MDC
  → ApiRequestLoggingFilter (HIGHEST_PRECEDENCE+1) → 慢请求 WARN
  → Spring Security (STATELESS, CSRF off)
  → JwtAuthenticationFilter → 解析 Bearer → SecurityContext
  → PlatformTokenIsolationFilter → 平台/租户 token 路由隔离
  → Controller → @PreAuthorize → GlobalExceptionHandler
```

### 多租户拦截器

- 白名单 11 张身份层表：拦截器不注入 `tenant_id`。
- 业务表：拦截器从 `SecurityContext.tenantId()` 自动注入。
- 配置项（`xforge.tenant.*`）：`enabled`(默认 true) / `default-tenant-id`(默认 1) / `lock-fail-threshold`(默认 5) / `lock-duration-minutes`(默认 10)。
- 拦截器注册顺序：多租户 → 数据权限 → 分页。

### 安全姿态

- `permitAll`：`/actuator/health`、`/v3/api-docs/**`、`/swagger-ui/**`、`/api/v1/auth/login`、`/api/v1/auth/select-workspace`、`/api/v1/auth/captcha/**`、`/api/v1/auth/captcha-config`、`/api/v1/platform/auth/**`、`/api/v1/open/call/**`。
- 其余 `anyRequest().authenticated()`。
- 功能权限：`@PreAuthorize("@pms.has('system:user:list')")`。
- 平台权限：`@PreAuthorize("@authService.isPlatform()")`。
- 数据权限：`@DataScope(deptAlias = "d")` AOP 追加 `dept_id IN (...)`。
- `@PreAuthorize` 否决抛 `AuthorizationDeniedException` → `GlobalExceptionHandler` 必须有 `@ExceptionHandler(AccessDeniedException.class)` → 403 包络。

### 实体约定

- **显式** `@TableName("xf_xxx")`（含前缀）。
- 主键 `@TableId(type = ASSIGN_ID)` 雪花。
- 逻辑删除 `@TableLogic(value = "0", delval = "2")`。
- 审计字段（`create_by/create_time/update_by/update_time/del_flag`）由 `BaseEntity` + `AutoFillMetaObjectHandler` 自动填充。
- `xf_account_credential` / `xf_account_lifecycle_log` / `xf_tenant_member_role` **不继承** `BaseEntity`（无 `del_flag` 列）。

### MyBatis-Plus × Boot 4 兼容坑

**禁止设置任何 `mybatis-plus.configuration.*` 属性**（如 `map-underscore-to-camel-case`）。一旦设置会在启动时 `NoSuchMethodError`。命名/ID/逻辑删除走 `mybatis-plus.global-config.db-config.*`。

### Flyway 迁移

| 文件 | 内容 |
| --- | --- |
| `V1__schema.sql` | 全部 31 张表 DDL |
| `V2__seed.sql` | 默认租户 + 部门 + 角色 + 菜单 + 68 按钮权限 + 账号/凭据/成员/角色/审计 + 字典 + 配置 + 定时任务 |
| `V3__platform_seed.sql` | 平台超管 + 平台角色 + 权限点 |

Spring Boot 4.1 已移除 `FlywayAutoConfiguration`，由 `server-core/FlywayConfig` 手动装配（`@Bean(initMethod = "migrate")`，启动时执行 `classpath:db/migration`，装配时调用 `flyway.repair()`）。

### 操作日志

`@Log(title, businessType)` 标注 Controller，`LogAspect`(@Around) 采集 → `AuditSink` 落库 `xf_oper_log`。append-only，写入失败不影响业务。

### 滑块验证码

原图归后端私有。前端松手调用 `POST /api/v1/auth/captcha/slider/verify` 提交换算后的 `sliderX`。登录/改密/重置密码都以 `uuid + code` 消费。`InMemoryCaptchaService` 仅适合单实例。

### 技术栈

Spring Boot 4.1.0 / Java 21 / MyBatis-Plus (spring-boot4-starter + jsqlparser) / Redis / springdoc 3.0.3 / micrometer-otel / H2(MySQL 模式, test) / MySQL(生产)。

## 4. 前端

### Preset 门面（核心抽象）

```
业务页 ──只 import──> @/components/design-system
                          │
                          ├── generated/ (脚本生成当前 Preset 映射)
                          ▼
               presets/minimal/ 或 presets/soft-brutal/
                          │
                          ▼
               components/ui/ (shadcn 基础原语, 无业务色)
```

- 切换预设：`npm run preset -- minimal` 或 `npm run preset -- soft-brutal`。
- 脚本只重写 `generated/{components.ts, themes.ts, tokens.css}`，业务页零改动。
- 组件统一用 `X*` 命名（`XButton` / `XCard` / `XDataTable` 等）。

### Token 级联（一键换肤原理）

```
presets/<name>/tokens.css    定义 --background / --primary / --radius-sm 等原始变量
   → generated/tokens.css     @import 该文件（脚本生成）
   → main.ts 引入后 :root 生效
   → main.css @theme inline   把变量映射成 Tailwind 工具类
```

组件用 `bg-background` / `text-primary` / `rounded-sm` 引用变量，从不写死颜色。

### 登录与多 workspace

- 登录页：`email + password`（不再有 username 字段）。
- 单 workspace：直接签发 token，跳转 `/`。
- 多 workspace：返回 `workspaces[]`，前端跳 `/auth/select-workspace` 让用户选。
- 合成邮箱（`*@migrated.xforge.local`）：`authStore.showEmailBindPrompt = true` 提示绑定（不阻断）。

### 平台控制台

- `/platform/login`：平台超管登录（`platform_admin / admin123`）。
- `/platform/tenants`：租户 CRUD。
- `/platform/accounts`：全局账号冻结/解冻。
- `PlatformLayout`：独立布局（顶部 nav，无 sidebar）。

### 账号安全

`/account/security`：本人资料 + 改密 + 生命周期审计（最近 50 条）。

### 路由刷新

`AdminLayout` 的 `RouterView` 按 `route.fullPath` 作 key，每次切换重新挂载。数据初始化用 `onMounted`。

### 二次确认

`useConfirm()` + `<XConfirmDialog>`。业务层禁止调 `window.confirm()`。

### 栈

Vue 3.5 / Vue Router 4 / Pinia 3 / Vite 6 / Tailwind 4 / reka-ui / cva / @lucide/vue / @vueuse/core。

## 5. 禁止清单

| 禁止 | 原因 |
| --- | --- |
| 业务页直接 import `presets/*` 或 `components/ui/*` | 破坏门面隔离 |
| 手写原生 `<button>` / `<input>` / `<select>` / `<table>` / `<dialog>` | 必须用 `X*` 组件 |
| 硬编码颜色 / 圆角 / 阴影 | 必须引用令牌 |
| 绕过 `AccountLifecycleService` 直接 UPDATE `lifecycle_status` 或 `tenant_member_role` | 破坏审计留痕 |
| 使用 `@InterceptorIgnore` 注解 | 身份层表走白名单 |
| 设置 `mybatis-plus.configuration.*` 属性 | Boot 4 兼容坑，启动 `NoSuchMethodError` |
| 开启 Logback 原生 `scan` 自动重载 | `<springProperty>` 无法解析，误建 `LOG_PATH_IS_UNDEFINED` |
| 业务 Service 手工解析登录态填 `create_by` / `update_by` | 走 `ActorProvider` 自动填充 |
| 前端 SSE URL 用 `VITE_API_TARGET` 直连后端 | 必须用 `VITE_API_BASE_URL` 走 Vite 同源代理 |
| access token 放入 query 参数或加入 `permitAll` | SSE 也要认证保护 |

## 6. 常用命令

```bash
# 前端
cd admin-web && npm run verify                    # format:check → lint → test → build
cd admin-web && npm run dev                       # 开发
cd admin-web && npm run preset -- minimal         # 切换预设

# 后端
cd server && mvn -pl server-admin -am -B clean test   # 全量测试（83 个）
cd server && mvn verify                           # 启动入口: server-admin/XforgeApplication

# 清库重跑（MySQL）
mysql -u root -p -e "DROP DATABASE IF EXISTS xforge; CREATE DATABASE xforge DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 登录
# 租户端：邮箱 admin@migrated.xforge.local / 密码 admin123
# 平台端：POST /api/v1/platform/auth/login { username: "platform_admin", password: "admin123" }
```

## 7. 已知缺口

- 非 Git 仓库（`.gitignore` 存在但未 `git init`）。
- 无 CI（`.github/workflows/` 空目录）。
- 4A"账号核查"定期复核流程未实现——审计日志已完整可支撑后续。
- 短信/OAuth 认证供应商未接入——`credential_type` 扩展点已就绪。
- 合成邮箱绑定弹窗 UI 待完善（`authStore.showEmailBindPrompt` 已就绪）。

## 8. AI 协作约定

- **最小有效改动**：不顺手重构、全仓格式化、升级依赖、改动公共契约。
- **事实 vs 推断**：未跑构建不要声称「能编译」。
- **保护工作区**：不动用户现有改动、生成文件、密钥、未跟踪资源。
- **危险操作**（`git commit`/`push`、部署、删数据）需用户明确指令。
- 阅读优先级：项目规则 > 本文件 > 通用约定。
