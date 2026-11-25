---
name: api-endpoint-creator
pack: universal
description: 给一个服务加一个新 HTTP 端点的标准做法——契约/鉴权/结构化日志/错误形态/特性开关/集成测试/Sentry/AGENTS.md 校验全一条龙。implementer agent 写新端点时必走。
when_to_use: implementer agent 看到任务里有"新增 GET/POST/PUT /v1/<resource>"或"加一个 webhook"时。
when_NOT_to_use: 改已有端点的内部逻辑而不动签名时(走 implementer 默认流程即可);RPC/gRPC/GraphQL 走各自专门 skill(暂未提供)。
---

# Skill: API Endpoint Creator

## 强制清单(每一项都不可省)

### 1. 契约(packages/contracts/src/...)
新端点的 request/response 类型先在 contracts 里声明,**任何服务都不可在本地复制类型**。

```ts
// packages/contracts/src/users.ts
export interface MeResponse { id: string; email: string; }
```

### 2. 路由 + 鉴权(默认必须鉴权)

```ts
if (url.pathname === '/v1/users/me' && req.method === 'GET') {
  const user = await deps.authenticate(req);    // ← 没有就 401
  if (!user) { return reply(res, 401, { code: 'unauthorized', requestId }); }
  ...
}
```

**例外**:`/health` `/metrics` 等运维端点;**例外必须在 PR 描述里说明理由**,security 评审会盯。

### 3. 输入校验
- 用 zod / valibot / 手写校验,**绝不**信任 query/body 原值
- 越权(IDOR):任何按 id 取资源的端点,显式校验 `resource.userId === currentUser.id`

### 4. 结构化日志(必须)

```ts
log('info', { requestId, endpoint: '/v1/users/me', userId: user.id, ms: Date.now()-t0 });
```

字段集合:`service` / `level` / `ts` / `requestId` / `endpoint` / `userId?` / `ms?`。
**不要**记 PII(email、phone、token 等)。

### 5. 错误形态(契约 ApiError)

```ts
const err: ApiError = { code: 'not_found', message: 'user not found', requestId };
res.statusCode = 404; res.end(JSON.stringify(err));
```

5xx 必须 throw → 被 Sentry 上报;4xx 不上报。

### 6. 特性开关

新端点默认藏在 flag 后(走 feature-flag-setup skill),除非这是历史端点重构。

### 7. 测试

- **单测**:对纯业务函数(把 IO 隔离)。
- **集成测试**:在 services/<svc>/test/ 用 createServer + fake deps,真起 server fetch,断言状态码 + body + 鉴权拒绝。
- E2E 留给 e2e/ 目录(可选)。

### 8. AGENTS.md 同步

新端点的鉴权要求、限流要求、特殊错误码,要在 AGENTS.md "安全禁区"或"端点列表"里登记一笔。

## 输出检查清单(implementer 在开 PR 前自检)

- [ ] 类型在 contracts,而非本地
- [ ] 默认鉴权,例外有理由
- [ ] 输入校验 + 越权检查
- [ ] 结构化日志,无 PII
- [ ] 错误用 ApiError,5xx 上 Sentry,4xx 不上
- [ ] 藏在特性开关后
- [ ] 集成测试覆盖:成功 / 鉴权失败 / 输入非法 / 资源不存在
- [ ] AGENTS.md 已更新

## 反模式

- ❌ 端点写在 controller 里同时做 IO,业务逻辑无法离线测试
- ❌ 把 user 整对象塞进日志(含 PII)
- ❌ 5xx 用 `res.statusCode = 500` 直接吞,Sentry 看不到
- ❌ 404 写成 200 + `{ok:false}`——破坏前端通用错误处理
