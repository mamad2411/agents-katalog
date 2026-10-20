# auth 模块知识

> 包路径：`com.bookcollector.auth` · 最后更新：2026-09-23

## 1. 这个模块是干什么的

**登录鉴权**（FR-A1 ~ FR-A4）：账号密码来自 `sys_user` 集合（密码存 MD5 摘要），
校验通过由 **Sa-Token** 签发 token 并建立会话（落 Redis）。
`roles` 只是给前端菜单渲染的占位，**不参与任何鉴权判断**（FR-A5）。

> ⚠️ **历史说明**：第一期的实现是「账号密码写死在 `application.yml` + 固定 token」，
> 即所谓的「写死登录」。那个版本有两个绕不过去的问题 —— **改密码要重启**、
> **登出是假的**（token 永不变化，服务端没有可撤销的东西）。
> 现在两件事都变成真的：改密码改库即生效；`logout` 会真的删掉 Redis 里的会话。
> 本文档描述的是**现状**，`docs/01-需求分析与分步执行方案.md` 等阶段文档里
> 的「写死登录」是当时的记录，不再代表当前实现。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `controller/AuthController` | Controller | 3 个端点（login / logout / me），**极薄转发** |
| `service/AuthService` | Service 接口 | 3 个方法 |
| `service/impl/AuthServiceImpl` | Service 实现 | 查 `sys_user` → MD5 比对 → Sa-Token 登录 → 会话存 `LoginUser` |
| `entity/SysUser` | 实体 | 登录用户（集合 `sys_user`），**密码存 MD5 摘要** |
| `repository/SysUserRepository` | 仓储 | 按 `username` 查 / 幂等判断 / 刷新 `lastLoginAt` |
| `dto/LoginUser` | DTO | 会话里的登录用户，**刻意不含 password 字段** |
| `stp/AuthStpUtil` | Sa-Token 门面 | `loginType="bookcollector-admin"` 的 `StpLogic` 封装，登录态唯一入口 |
| `interceptor/AuthInterceptor` | `HandlerInterceptor` | 校验 `/api/**` 登录态，失败写 `code=4100` |
| `extract/ExtractLoginUser` | 注解 | 在 Controller 方法参数上注入当前登录用户 |
| `extract/ExtractLoginUserHandlerResolver` | `HandlerMethodArgumentResolver` | 校验登录态 + 注入用户 + **身份一致性校验** |
| `req/LoginRequest` | req | 登录请求体（`username` / `password`） |

模块外的相关类：

- `config/AuthProperties`（`bookcollector.auth.*`）—— **只是初始管理员的播种参数**，
  不是登录校验的来源。见 `common/AGENTS.md`。
- `config/WebMvcConfig` —— 注册 `AuthInterceptor` 与 `ExtractLoginUserHandlerResolver`。
- `util/Md5Util` —— 密码摘要。
- `config/SeedRunner` —— 首次启动播种初始管理员（**不是 upsert，库里已有同名用户就跳过**）。
- `config/MongoIndexInitializer` —— 建 `sys_user` 的 `uk_username` 唯一索引。

## 3. 调用关系（图谱）

```
【登录】
前端 ──POST /api/auth/login──► AuthController ──► AuthServiceImpl
                                                      │ ① SysUserRepository.findByUsername
                                                      │ ② Md5Util.matches(明文, 库里摘要)
                                                      │ ③ AuthStpUtil.login(id)      → token 落 Redis
                                                      │ ④ 会话存 LoginUser（脱敏投影）
                                                      │ ⑤ touchLastLogin(id)
                                                      ▼
                                          返回 { token, username }

【鉴权】其余 /api/** 请求
      │
      ▼
AuthInterceptor.preHandle     ← WebMvcConfig 注册，拦截 /api/**
      │  放行：/api/auth/login、/api/ping、/api/ping/**
      │  OPTIONS 预检直接放行
      │
      ├─ AuthStpUtil.checkLogin() 通过 ──► 继续
      └─ 抛 NotLoginException ──► 写 HTTP 200 + body { code: 4100 }，return false

【注入当前用户】需要「谁在调用」的接口
      │
      ▼
ExtractLoginUserHandlerResolver
      │  ① checkLogin()                → 未登录抛 NotLoginException → 4100
      │  ② getSessionLoginUser()       → 从会话取 LoginUser
      │  ③ 校验 LoginUser.id == token 归属的 loginId
      └─ 不一致 / 取不到 ──► throw BizException.sessionInvalid → 4100
```

**两条通道的分工（重要）**：

| | 拦截器 | 参数解析器 |
|---|---|---|
| 管什么 | **授权**：能不能进 | **注入**：进来的是谁 |
| 覆盖面 | 所有 `/api/**`（默认拒绝） | 只覆盖带 `@ExtractLoginUser` 的参数 |
| 缺了会怎样 | 新增接口默认不设防 | Controller 里塞满「校验 + 取用户 + 判空」样板 |

类比 Spring Security 的 filter chain + `@AuthenticationPrincipal`。**两者都要**，
不是一个替代另一个。

## 4. 数据集合与索引

| 集合 | 实体 | 索引 |
|---|---|---|
| `sys_user` | `auth.entity.SysUser` | `uk_username`（`username` ASC，**唯一**） |

`uk_username` **不是性能优化，是正确性依赖**：`SeedRunner.seedSysUser` 的幂等策略是
「先 `existsByUsername` 再插入」，没有唯一索引兜底时并发/重复启动会插出两条同名账号，
之后 `findByUsername` 的 `findOne` 返回哪一条**不确定** ——
症状是「密码改了却登不上，刷新几次又能登」。

集合本身由 `MongoIndexInitializer` 顺带建出来（在**不存在的集合上建索引**时
MongoDB 会先把集合建出来），`sys_user` 没有别的建表入口。

## 5. 对外接口

| 方法 | 路由 | 说明 |
|---|---|---|
| POST | `/api/auth/login` | 校验 `sys_user` 账号密码（MD5），成功返回 `{ token, username }` |
| POST | `/api/auth/logout` | **真的删掉服务端会话**，token 立即失效；返回 `{ message: "已退出登录" }` |
| GET | `/api/auth/me` | 返回 `{ username, roles, nickname }`，**不含 token** |

三个端点的**响应键与改造前完全一致**，所以前端零改动。

**token 的唯一入口**：请求头 `Authorization: Bearer <token>`。

- 由 `sa-token.token-name=Authorization` + `token-prefix=Bearer` 配置。
  Sa-Token 的裁剪条件是 `tokenValue.startsWith(prefix + " ")`，
  **`Bearer` 后面那个空格是必须的**（前端发的正好是这个格式）。
- 改造前还支持 `X-Token: xxx` 和 `?token=xxx` 两种备用传法，**现在都不支持了**
  （`sa-token.is-read-body=false`、`is-read-cookie=false`）。这是刻意的：
  token 只有一个入口，排障和审计都不用猜「这次是哪个位置带的」。
  curl 调试要用 `-H "Authorization: Bearer xxx"`。

## 6. 不变量与铁律 ← 改这个模块前必读

1. **🔴 鉴权失败返回 HTTP 200 + `code=4100`，不是 401。**
   前端 axios 拦截器（`frontend/src/api/request.ts`）**只看 body 里的 `code`，不看 HTTP 状态码**。
   返 401 会让前端走「HTTP 层错误」分支，弹「请求异常：HTTP 401」而不是
   「身份已失效，请重新登录」。改这里之前先确认前端拦截器的行为没变。

2. **拦截点用 `HandlerInterceptor`，不用 `Filter`。**
   - Filter 只能按 `urlPatterns` 做前缀匹配，而 `/api/auth/login`、`/api/ping`
     与其余 `/api/**` **混在同一前缀下**，前缀匹配表达不了
   - Interceptor 的 `excludePathPatterns` 表达力正好够用
   - 副产品：`/v3/api-docs` 与 `/swagger-ui/**` 不在 `/api/**` 下，天然不被拦，
     不用手工维护静态资源白名单

   （`TraceIdFilter` 与 Sa-Token 自己的 `SaTokenContextFilterForServlet` 仍然是 Filter ——
   它们需要覆盖所有请求，那里 Filter 才是对的工具。）

3. **`preHandle` 返回 `false` 后异常处理器根本不会介入**，所以 4100 的 JSON
   必须拦截器**自己写**（`writeSessionInvalid`）。**不要**指望 `GlobalExceptionHandler`。
   （`ResultBean.err(...)` 内部会带出 MDC 里的 traceId，所以自写响应并不缺信息。
   `GlobalExceptionHandler` 里的 `NotLoginException` 分支兜的是**另一条路**：
   服务层直接调 `AuthStpUtil.checkLogin()` 时。两者不重复。）

4. **`OPTIONS` 预检直接放行。** 浏览器的 CORS 预检不带自定义头。

5. **刻意不区分「用户名错」和「密码错」。** 统一提示「用户名或密码错误」。
   本地服务其实没这个必要，但这条习惯成本为零，且能避免以后加审计时泄漏有效用户名。

6. **登出现在是「真的」。** `logout` 会删掉 Redis 里的会话，token 立即失效。
   —— 这与改造前的「不做 token 黑名单、logout 只是清前端 localStorage」是**相反的**，
   别再按老结论改代码。`AuthStpUtil.logout()` 对未登录是幂等的，重复登出安全。

7. **`/me` 不返回 token。** 前端已经在 localStorage 里有了，回传没有收益。

8. **`/api/ping` 必须在白名单里。** 它同时是 S0 的验收点
   （「不带任何头就能拿到 code:200」），也是前端探测「后端到底起来没有」的手段。
   要求它带 token 会让排障变难：连不上时分不清是后端没起还是 token 不对。

9. **🔴 业务代码不要直接 `import cn.dev33.satoken.stp.StpUtil`。**
   本模块用的是自定义 `StpLogic`（`AuthStpUtil.LOGIN_TYPE = "bookcollector-admin"`），
   而 `StpUtil` 用的是默认的 `loginType="login"`。两者**登录态完全不相干**：
   `StpUtil.checkLogin()` 永远抛未登录，`StpUtil.login(id)` 登录的用户 `AuthStpUtil` 也认不出来。
   编译器不会报错，症状是「登录了但所有接口 4100」。
   需要登录态一律走 `AuthStpUtil`。

   > 为什么要自定义 loginType：本机 Redis 是 `database: 0`，多个本地项目共用。
   > 都用默认 `StpUtil` 时 token 会落在同一批 key（`satoken:login:...`）上，
   > 表现为「登录了 A 项目，B 项目也变成已登录」。带上项目名前缀就天然隔离了。

10. **`LoginUser` 里绝不能出现 `password` 字段。**
    它会被写进 Redis 里的会话，也会进 `/api/auth/me` 的响应体。
    一旦带了密码摘要，就等于「登录一次之后，密码摘要长期停在 Redis 和前端内存里」。
    所以 `LoginUser` **刻意不复用** `SysUser` 而是重新声明字段 —— 多写 20 行换掉一个坑。
    `AuthIT.responsesNeverLeakPassword` 是这个决定的守卫。

11. **新增 `/api/**` 接口默认就被鉴权保护。** 这是拦截器方案的核心价值。
    确实需要匿名访问的，必须**显式**加进 `WebMvcConfig` 的 `excludePathPatterns`，
    并在本文件第 5 节登记 —— 白名单是「需要被审视的例外」，不是随手能加的东西。

12. **`roles` 不参与鉴权。** 后端没有任何 `hasRole` / `checkRole` 判断，
    所有登录用户能看到的、能调的都一样。前端菜单按 `roles` 渲染只是占位。

13. **`AuthProperties` 只影响「库为空时的第一次播种」。** 改它对已存在的账号没有任何影响
    （`SeedRunner.seedSysUser` 的语义是「库里有同名用户就跳过」，不是 upsert）。
    要改密码，改库。

## 7. 依赖与耦合

- **依赖**：`config.AuthProperties`、`common.{BizException,ResultBean}`、
  `util.Md5Util`、`config.WebMvcConfig`、`cn.dev33.satoken.*`、`spring-data-mongodb`。
- **被依赖**：`config.SeedRunner`（播种管理员）、`config.MongoIndexInitializer`（建索引）、
  前端（所有请求都带 token）。
- **业务模块之间没有依赖** —— 这是刻意的（认证不该被业务模块反向依赖）。
- ⚠️ **`config → auth` 是一条新的依赖方向**（改造前 `config` 只依赖 `auth` 的
  `TokenInterceptor` 一个类，现在是 `AuthProperties` + `SysUser` + `SysUserRepository`）。
  它没有引入新的环：`auth` 不依赖 `config` 的任何业务语义，
  只依赖 `AuthProperties` 这个配置载体，而 `AuthProperties` 是纯 POJO。

## 8. 测试与验收

| 测试类 | 覆盖 |
|---|---|
| `ApiContractTest` | 路由契约、4100 契约、**登出后 token 立即失效**、错误 token / 少前缀 / 其它 header 一律 4100 |
| `ApiCrudIT` | 真实登录拿 token 后跑写路径 |
| `AuthIT` | **三处「不报错的失败」**：Redis DAO 是否真生效、会话 DTO 类型是否被 Jackson 退化、密码是否明文落库；外加「不区分用户名/密码错」与「响应不泄漏密码」 |

```bash
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=ApiContractTest
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=AuthIT
```

> ⚠️ 这两个测试类**都需要 Mongo 和 Redis 在跑**（登录要写会话）。
> 测试用 `@Value("${bookcollector.auth.initial-*")` 拿初始凭据后**真实登录**，
> 不再从配置里读 token（token 已不是配置项）。

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 前端弹「请求异常：HTTP 401」而不是「身份已失效，请重新登录」

- **现象**：token 失效后，前端提示文案不对。
- **根因**：拦截器写了 HTTP 401，而前端只看 body 的 `code`。
- **修法**：HTTP 状态码保持 200，body 里 `code = 4100`（`ResultBean.code_session_invalid`）。

### 9.2 Swagger 页面打不开

- **现象**：加了拦截器后 `/swagger-ui.html` 报 4100。
- **根因**：拦截路径写成了 `/` 或 `/**`。
- **修法**：只拦 `/api/**`。Swagger 的路径不在这个前缀下，天然放行。

### 9.3 改了 `application.yml` 的密码但登录还是老的

- **现象**：改了 `bookcollector.auth.initial-password`，用新密码登录失败。
- **根因**：**这段配置现在完全不参与登录校验**，它只在「库里还没有同名用户」时用一次。
  库里已有账号时它被 `SeedRunner.seedSysUser` 直接跳过（这是刻意的 ——
  否则「改密码」又退化成「改 yml + 重启」）。
- **修法**：直接改库：
  ```
  db.sys_user.updateOne({username:"admin"}, {$set:{password:"<新密码的 MD5>"}})
  ```
  摘要可以用 `Md5Util.md5(...)` 算，或 `echo -n '新密码' | md5sum`。
  ⚠️ 不要为了「省事」把它改成 upsert —— 那会让用户改过的密码被重启冲掉。

### 9.4 登录成功，但下一个请求就 4100

- **现象**：`POST /api/auth/login` 返回 200 且有 token，但带着它调任何接口都
  `code=4100`「登录信息已失效」。
- **根因**：会话里的 `LoginUser` 被 Jackson **反序列化成了 `LinkedHashMap`**，
  于是 `ExtractLoginUserHandlerResolver` 的 `instanceof LoginUser` 判断失败。
  Sa-Token 的会话是序列化成 JSON 存 Redis 的，默认不带类型信息。
- **修法**：确认两件事 ——
  1. `sa-token-jackson` 在依赖树里（`sa-token-spring-boot-starter` 已带）。
     它的 `SaJsonTemplateForJackson` 会执行
     `activateDefaultTyping(..., DefaultType.NON_FINAL, As.PROPERTY)`，
     非 final 类型会带 `@class` 往返。
  2. **`LoginUser` 必须有无参构造器**（`@NoArgsConstructor`）。删掉它，这个坑立刻复现。
- **守卫**：`AuthIT.sessionHoldsTypedLoginUser` —— 它返回 200 这件事本身就证明类型没丢。

### 9.5 服务一重启，登录态就没了（但没有任何报错）

- **现象**：每次重启后端都要重新登录；`logout` 看起来也「只对当前进程有效」。
  登录、鉴权功能本身**完全正常**，没有任何异常或 WARN。
- **根因**：Sa-Token **静默退回了内存 DAO** —— `sa-token-redis-jackson` 的自动配置
  没被加载（例如 Boot 版本与 `spring.factories` / `.imports` 的读取方式不匹配）。
  Sa-Token 不会为此打任何日志。
- **修法**：确认 `SaManager.getSaTokenDao()` 是 `SaTokenDaoForRedisTemplate`。
  本项目已核实：`sa-token-spring-boot-starter` 与 `sa-token-redis-template` 的 jar 里
  **同时**有 `META-INF/spring.factories`（Boot 2.3 读这个）和
  `META-INF/spring/...AutoConfiguration.imports`，所以 Boot 2.3.12 能正常加载。
- **守卫**：`AuthIT.saTokenDaoIsRedisBacked`。

### 9.6 curl 调试时带 token 报 4100

- **现象**：改造前能用的 `curl 'http://127.0.0.1:8080/api/books?token=xxx'` 现在返回 4100。
- **根因**：token 现在**只从请求头读**（`is-read-body=false`、`is-read-cookie=false`），
  而且必须是 `Bearer ` 前缀格式。
- **修法**：`curl -H "Authorization: Bearer <token>" http://127.0.0.1:8080/api/books`。
  token 从登录响应体的 `data.token` 拿。
