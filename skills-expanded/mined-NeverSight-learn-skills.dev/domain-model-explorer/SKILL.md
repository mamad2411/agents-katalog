---
name: domain-model-explorer
description: Use this skill whenever the user wants to understand business flows, event chains, bounded-context boundaries, or directly create, update, or delete event-storming nodes and relations in this project. Trigger for natural requests like "帮我看下这个流程怎么走", "用户做某个动作后会发生什么", "新增一个事件节点", "修改这条关系", "直接帮我在事件风暴里补节点/关系", or "先按领域模型解释，再直接改模型".
metadata:
  requires:
    bins: ["node"]
---

# Domain Model Explorer

Use the project's domain-model API as the default path for both exploration and model mutation.
This skill is for understanding system chain, context boundaries, and design structure, and for directly editing the event-storming model without manually clicking through the page.

## Trigger guidance

Prefer triggering this skill when the user's intent is to:

- 理解一个业务动作会带来哪些后续流程
- 查看一个事件或命令的上游、下游、整体链路
- 了解某个能力横跨哪些上下文
- 新增、编辑、删除一个节点
- 新增、编辑、删除一条关系
- 先理解模型，再直接改模型

High-signal natural prompts include:

- “帮我看下这个功能的整体流程”
- “用户创建订单后会发生什么”
- “在 OrderContext 里加一个支付超时事件”
- “把这条关系改成 triggers”
- “直接帮我把这个节点删掉并确认结果”
- “先别读代码，先按领域模型给我讲讲，然后直接改模型”

## API surface rule

Always treat `/api/v1` as the only skill-facing API surface.

- Read operations use `/api/v1` query routes.
- Write operations also use `/api/v1` mutation routes.
- Do not default to legacy `/api/nodes` or `/api/relations` routes.
- If you discover a needed capability is still missing from `/api/v1`, call that out explicitly instead of silently falling back to legacy APIs.

## Script path rule

All bundled script paths in this skill are relative to the current skill directory.
When executing them, set the working directory to `@.codex/skills/domain-model-explorer` first, then run `node scripts/...`.
Do not prepend repo-relative paths like `.codex/skills/...`, and do not search the repository to rediscover script locations.

## Authentication

Default mode is user-first:

- configure `DOMAIN_MODEL_PROJECT_ID`
- obtain `DOMAIN_MODEL_ACCESS_TOKEN`
- the bundled script sends `Authorization: Bearer <token>` plus `X-Project-Id`

### Auth init

Default base URL is `https://ddd.hixqz.com/api/v1`. Only pass a base URL when you need to override it explicitly. Project can also be chosen later in the browser flow:

```bash
node scripts/domain-model-query.mjs auth-init --base-url "http://localhost:3000/api/v1"
node scripts/domain-model-query.mjs auth-init --project-id "<project-id>" --base-url "http://localhost:3000/api/v1"
```

Explicit override examples:

```bash
DOMAIN_MODEL_API_BASE_URL="http://localhost:3000/api/v1" node scripts/domain-model-query.mjs auth-status
DOMAIN_MODEL_API_BASE_URL="http://localhost:3000/api/v1" node scripts/domain-model-query.mjs auth-login-browser --project-id "<project-id>" --base-url "http://localhost:3000/api/v1"
```

Resolution order:

```text
DOMAIN_MODEL_API_BASE_URL
-> local config baseUrl (~/.config/domain-model-explorer/auth.json)
-> https://ddd.hixqz.com/api/v1
```

### Auth login

Manual token flow:

```text
<app-origin>/api/auth/access-token?projectId=<project-id>&permission=write&expiresIn=86400
<app-origin>/api/auth/access-token?projectId=<project-id>&permission=read&expiresIn=3600  # only for temporary read-only access
```

Then save the returned `access_token`:

```bash
node scripts/domain-model-query.mjs auth-login --access-token "<query-access-token>" --project-id "<project-id>"
```

Prefer the browser automation flow when possible:

```bash
node scripts/domain-model-query.mjs auth-login-browser
node scripts/domain-model-query.mjs auth-login-browser --project-id "<project-id>" --base-url "http://localhost:3000/api/v1" --permission write
node scripts/domain-model-query.mjs auth-login-browser --project-id "<project-id>" --base-url "http://localhost:3000/api/v1" --permission read --expires-in 3600  # temporary read-only only
```

`auth-login-browser` 默认申请 `write` 权限，默认有效期为 `86400` 秒。只有确实需要临时只读令牌时，才显式传 `read`。
认证命令只接受显式参数，不再使用位置参数；例如用 `--project-id`、`--base-url`、`--permission`、`--expires-in` 表达含义。

### Auth status

Before querying or mutating, check current auth state:

```bash
node scripts/domain-model-query.mjs auth-status
```

### Token reuse rule

Within one conversation, prefer reusing the current token instead of reissuing a new one.

- default behavior: one conversation reuses one token
- only re-auth when the token is missing, expired, project-mismatched, or permission-mismatched
- read tasks should reuse the current token when it is still valid; a `write` token satisfies read operations
- only switch to a new `write` token when the current token cannot satisfy a write operation
- calling `auth-login-browser` with the same project and sufficient permission should reuse the existing token and avoid reopening the browser

### Write permission rule

- Read-only exploration can use a `read` token.
- Any node or relation mutation requires a `write` token.
- Default browser authentication should request a `write` token so exploration can naturally continue into confirmed mutations.
- If a write command returns a permission error and the current token is only `read`, request a new `write` token.
- Do not reissue a token just because another command in the same conversation starts. Reuse first, re-auth only when required.

### Security rules

- never print `DOMAIN_MODEL_ACCESS_TOKEN` in terminal output or user-facing answers
- prefer `write` by default; use `read` only when a short-lived read-only token is explicitly desired
- after switching projects, request a new token to avoid scope mismatch
- avoid repeated `auth-login-browser` calls in one conversation when the current token is still valid for the same project and permission

## Bundled script

Use the bundled client instead of hand-writing HTTP requests:

```bash
node scripts/domain-model-query.mjs auth-status
node scripts/domain-model-query.mjs list-contexts
node scripts/domain-model-query.mjs summarize-context "OrderContext"
node scripts/domain-model-query.mjs node-detail "PurchaseOrderCreatedEvent"
node scripts/domain-model-query.mjs summarize-relations "UserLockedEvent" outgoing context Event,Command
node scripts/domain-model-query.mjs create-node '{"boundedContextName":"OrderContext","name":"PaymentTimedOutEvent","type":"Event","displayName":"支付超时","properties":[{"name":"orderId","type":"string"},{"name":"timedOutAt","type":"datetime"},{"name":"reason","type":"string"}]}'
node scripts/domain-model-query.mjs update-node "PaymentTimedOutEvent" '{"displayName":"支付已超时"}'
node scripts/domain-model-query.mjs move-node "PaymentTimedOutEvent" "PaymentContext"
node scripts/domain-model-query.mjs delete-node "PaymentTimedOutEvent"
node scripts/domain-model-query.mjs list-relations '{"source":"PlaceOrderCommand","target":"OrderPlacedEvent","relationType":"triggers"}'
node scripts/domain-model-query.mjs create-relation '{"source":"PlaceOrderCommand","target":"OrderPlacedEvent","relationType":"triggers","label":"订单已创建"}'
node scripts/domain-model-query.mjs create-relation '{"source":"BindResourceCommand","middle":"ResourceRelationAgg","target":"ResourceBoundEvent","relationType":"triggers","middleLabel":"绑定资源","label":"资源已绑定"}'
node scripts/domain-model-query.mjs update-relation "<relation-id>" '{"middleLabel":"绑定资源","label":"资源已绑定"}'
node scripts/domain-model-query.mjs delete-relation "<relation-id>"
```

For node create/update payloads, the bundled client will normalize enum-like property types into value-object types when possible, so `enum(...)` should still be treated as input smell rather than the target model shape. If the payload only implies a generic type name such as `Status` or `Type`, the client should reject it and require an explicit business-specific value object name. The normalized result should keep only the value-object type name on the parameter itself, and move candidate values into rules.

## Mutation workflow

Default to this order for write operations:

1. Clarify the exact target context, node, or relation.
2. Ensure auth is ready; if mutating, ensure the token has `write` permission.
3. Resolve the target by context name, node name, node id, or relation id.
4. Before any create, update, or delete, present a compact Markdown table that lists the planned impact.
5. Wait for explicit user confirmation after showing the table.
6. Execute the mutation through `/api/v1` only after the user confirms.
7. Read back the result or rely on the returned payload to confirm what changed.
8. Tell the user the final model state, not the terminal steps.

## Mutation confirmation gate

Never execute a write immediately after inferring the user's intent.
For every create, update, or delete operation, first show the planned impact in a Markdown table and ask the user to confirm.

The table should cover at least:

- operation: create, update, or delete
- target: context, node, or relation that will be changed
- affected nodes: nodes that will be created, modified, deleted, or indirectly impacted
- parameters: fields that will be written, removed, or kept unchanged
- rules: business rules, duplicate checks, cascade deletes, or ambiguity handling that matter for this mutation

Use a compact shape like:

| 操作 | 目标 | 影响节点 | 参数/字段 | 规则/注意事项 |
| --- | --- | --- | --- | --- |
| 新增节点 | `OrderContext` | `PaymentTimedOutEvent` | `type=Event`, `displayName=支付超时` | 非 `Person` 节点必须归属上下文 |
| 删除节点 | `PaymentTimedOutEvent` | 该节点及其关联关系 | 无 | 删除节点会级联删除挂在它上的关系 |

After the table:

- ask for explicit confirmation
- do not execute the mutation in the same turn unless the user already explicitly said to skip confirmation
- if the target is ambiguous, use the table to surface candidates instead of guessing

## Event Storming modeling flow

Hard rule: unless the user explicitly asks to land the model, stay in Event Storming and do not create, update, or delete any stored node, relation, or context.

Hard rule: Event Storming has only three phases and must move in order:

1. event
2. command
3. aggregate

Do not enter the next phase until:

- the current phase is finished
- the user explicitly agrees to enter the next phase

When the user wants to build or refine a domain model from business language, use this order:

### 1. Identify domain events

- Hard rule: Event Storming must start from events. Do not output commands, aggregates, or policies before the user confirms the event phase is complete.
- Start from business facts that have already happened and matter to the domain.
- Name events in past tense and keep them objective.
- **Hard rule: Every event must have parameters that describe the domain facts it carries. Never create an event without parameters.**
- For each event, identify parameters first: business identity, status, time, amount, operator, resource, and other domain facts carried by the event.
- Examples: `订单已创建(orderId, userId, items, totalAmount)`, `支付已成功(orderId, paymentId, paidAt)`, `订单已发货(orderId, shippedAt, trackingNo)`, `主机已释放(hostId, releasedAt, operator)`

### 2. Identify commands

- Only after the user confirms the event phase, derive commands.
- Find the user actions or external behaviors that trigger those events.
- Default modeling rule: one event should map back to one primary command. Do not converge multiple different commands into the same event unless the user explicitly confirms they are the same business intent.
- A command may lead to one event or a chain of events.
- Keep command names action-oriented and explicit.
- **Hard rule: Every command must have parameters that describe the input it accepts. Never create a command without parameters.**
- For each command, identify parameters first: input fields, target identity, preconditions, and the fields that may change.
- Examples: `提交订单(orderId, userId, items)` -> `订单已创建(orderId, userId, items, totalAmount)`, `确认支付(orderId, paymentMethod)` -> `支付已成功(orderId, paymentId, paidAt)`

### 3. Derive aggregates

- Only after the user confirms the command phase, derive aggregates.
- Compare commands and events to find stable business identities and shared key attributes.
- Treat those business entities as aggregate candidates, then check whether their boundaries and invariants are coherent.
- **Hard rule: Every aggregate must have parameters that describe its core attributes and identity. Never create an aggregate without parameters.**
- For each aggregate, identify key parameters, core attributes, invariants, and the command/event set it owns.
- Do not derive aggregates from UI shape or temporary process wording.
- Examples: `Order(orderId, status, totalAmount, items)`, `Payment(orderId, paymentId, status, paidAt)`, `Disk(diskId, size, status, attachedHostId)`

After aggregate phase, continue discussing ordering, dependencies, constraints, and optimization points inside the current conversation. Do not treat them as a separate phase.

Keep the modeling output aligned with DDD:

- event = domain fact
- command = intent or action
- aggregate = consistency boundary
- policy = event-driven routing rule that turns one or more events into follow-up commands
- relation = explicit trigger, dependency, or policy link
- bounded context = business language and model boundary

Policy usually appears as `Event -> Policy -> Command`.

## Enum-like attribute modeling rule

Hard rule: when a parameter or attribute looks like an enum, do not model its type directly as `enum`.

- Model it as a `ValueObject` instead.
- Do not expand the value object into inner attributes like `code` / `name` on the parameter or property definition.
- The concrete selectable values belong in business rules, not in the parameter type itself.
- In other words: parameter type should be `OrderStatus`, `PaymentMethod`, `DiskType` and similar value object names, not `enum<OrderStatus>` or inline enum literals.
- Hard rule: do not settle for generic value object names such as `Status`, `Type`, `State`, `Kind`. Prefer business-specific names like `OrderStatus`, `PaymentStatus`, `RefundType`.

Use this pattern:

| Scenario | Wrong | Correct |
| --- | --- | --- |
| 订单状态 | `status: enum(CREATED, PAID, CANCELED)` | `status: OrderStatus` and put candidates in rules |
| 支付方式 | `paymentMethod: enum(ALIPAY, WECHAT)` | `paymentMethod: PaymentMethod` and put candidates in rules |
| 磁盘类型 | `diskType: enum(SSD, ESSD)` | `diskType: DiskType` and put candidates in rules |

When explaining or landing the model:

- If a field is enum-like, explicitly mention the corresponding value object.
- Do not add inner attributes like `code` / `name` to that value object just because it comes from enum semantics.
- Put the allowed values in rules such as “`OrderStatus` 可选值：`CREATED/已创建`、`PAID/已支付`、`CANCELED/已取消`”.
- If the value object node itself has not been listed yet, add it into the current modeling draft before landing.

## Modeling completion gate

Event Storming output is the domain model draft.

- Only land the model when the user explicitly asks to do so.
- Before the user confirms the model is complete, keep storming with the user instead of rushing into node or relation mutation.
- Before the user confirms one phase is complete, stay in that phase and do not jump ahead.
- Keep refining events, commands, aggregates, policies, parameters, constraints, and dependencies until the user agrees the model is complete enough to land.
- Do not create, update, or delete nodes and relations while the model is still obviously incomplete or ambiguous.
- If the user asks to land the model after finishing the current phase, landing is allowed, but only after showing the confirmation table and getting explicit confirmation.

Before landing the model, first present a compact table that covers:

| 类型 | 名称 | 参数 | 关系 | 说明 |
| --- | --- | --- | --- | --- |
| Command | `CreateOrderCommand` | `orderId, userId, items, totalAmount` | triggers `OrderCreatedEvent` via `OrderAgg` | 用户提交订单 |
| Event | `OrderCreatedEvent` | `orderId, userId, items, totalAmount, createdAt` | emitted by `OrderAgg` | 订单已创建 |
| Aggregate | `OrderAgg` | `orderId, status, totalAmount, items` | handles `CreateOrderCommand`, emits `OrderCreatedEvent` | 订单一致性边界 |
| Policy | `PaymentTimeoutPolicy` | `orderId, deadlineAt` | `OrderCreatedEvent -> PaymentTimeoutPolicy -> ExpireOrderCommand` | 订单超时自动取消 |

**Parameter checklist before landing:**
- Every node must have at least one parameter that describes its identity or core data.
- Events carry domain facts: identity + status + timestamp + business data.
- Commands carry inputs: target identity + operation fields.
- Aggregates carry state: identity + core attributes + invariants.
- Enum-like attributes must be modeled as value objects, not direct `enum` types.
- Enum-like value objects should stay as type names and should not be展开成 `code`、`name` 这类内部属性。
- Concrete enum candidates must be written in rules/notes, not embedded in parameter type declarations.

After the user confirms that table, then enter node and relation landing flow.

## Node naming rule

Hard rule: except `ValueObject`, node names must end with the suffix defined by node type. Do not invent free-form endings.

- `Command` / `FacadeCommand` -> `Command`
- `DomainEvent` / `Event` -> `Event`
- `IntegrationEvent` -> `IntegrationEvent`
- `Query` -> `Query`
- `Aggregate` -> `Agg`
- `Entity` -> `Entity`
- `ValueObject` -> no forced suffix
- `ReadModel` -> `ReadModel`
- `UserInterface` -> `UserInterface`
- `Service` -> `Service`
- `Policy` -> `Policy`
- `Saga` -> `Saga`
- `Process` -> `Process`
- `Result` -> `Result`
- `Timer` -> `Timer`
- `Person` -> `Person`
- `System` -> `System`
- `Comment` -> `Comment`

Examples:

- command name: `ReleaseDiskCommand`
- event name: `DiskReleasedEvent`
- aggregate name: `DiskAgg`
- value object name: `Money`, `DiskSpec`

## Node operation rules

### Create node

- Prefer `boundedContextName` in payload when the user speaks in business language.
- Convert it to `boundedContextId` before sending the request.
- For non-`Person` nodes, a bounded context is required.
- Before execution, check whether the node name already follows the required type suffix. If not, correct it before landing.
- **Hard rule: Every node must have parameters. Before execution, ask the user for parameters if not provided. Never create a node with empty parameters.**
- **Hard rule: If a node parameter is enum-like, replace the direct enum type with a value object type, and do not expand that value object into `code` / `name` or similar internal attributes.**
- Before execution, list the node name, type, displayName, bounded context, **parameters**, and any initial properties or rules in the confirmation table.
- Example confirmation table for node creation:

| 操作 | 目标 | 节点名称 | 类型 | 显示名称 | 参数 | 规则/注意事项 |
| --- | --- | --- | --- | --- | --- | --- |
| 新增节点 | `OrderContext` | `PaymentTimedOutEvent` | Event | 支付超时 | `orderId, timedOutAt, reason` | 非 `Person` 节点必须归属上下文；事件参数必填 |

When parameters include enum-like semantics, prefer confirmation lines like:

| 操作 | 目标 | 节点名称 | 类型 | 显示名称 | 参数 | 规则/注意事项 |
| --- | --- | --- | --- | --- | --- | --- |
| 新增节点 | `OrderContext` | `OrderCreatedEvent` | Event | 订单已创建 | `orderId, status: OrderStatus, createdAt` | `OrderStatus` 为值对象类型，不展开内部属性；枚举值写入规则 |

### Update node

- Resolve the node first.
- Only send fields that should change.
- Do not silently rename the wrong node if the name is ambiguous.
- Before execution, list which fields change, which fields stay untouched, and which rules or constraints may reject the update.

### Delete node

- Resolve the node first.
- Tell the user when the deletion also removes attached relations.
- Confirm the deleted node id in the final answer when helpful.
- Before execution, include cascade impact in the confirmation table, especially attached relations and any directly affected downstream modeling elements.

## Relation operation rules

Hard rule: relation labels must follow business time semantics.

### Label semantics (critical)

For three-part relations `Command -> Aggregate -> Event`:

- **Aggregate-side label (middleLabel)**: describes the **in-flight action** or **processing intent** — what the aggregate is doing right now. Use verb-object form like "绑定资源"、"释放磁盘"、"创建订单".
- **Event-side label (label)**: describes the **final fact** that has **already happened** — the completed state. Use "已" prefix or past-tense form like "资源已绑定"、"磁盘已释放"、"订单已创建".

Memory aid: Aggregate is "doing", Event is "done".

### Common mistakes

| Scenario | Wrong | Correct |
| --- | --- | --- |
| 绑定资源 | `ResourceRelationAgg:"资源已绑定"`, `ResourceBoundEvent:"绑定资源"` | `ResourceRelationAgg:"绑定资源"`, `ResourceBoundEvent:"资源已绑定"` |
| 释放磁盘 | `DiskAgg:"磁盘已释放"`, `DiskReleasedEvent:"释放磁盘"` | `DiskAgg:"释放磁盘"`, `DiskReleasedEvent:"磁盘已释放"` |
| 创建订单 | `OrderAgg:"订单已创建"`, `OrderCreatedEvent:"创建订单"` | `OrderAgg:"创建订单"`, `OrderCreatedEvent:"订单已创建"` |
| 公网IP到期 | `IpAgg:"公网IP已过期"`, `IpExpiredEvent:"公网IP到期"` | `IpAgg:"公网IP到期"`, `IpExpiredEvent:"公网IP已过期"` |

### Create relation

- Accept `source` / `target` / `middle` names in payload and resolve them before sending the request.
- Prefer `relationType` over vague prose when constructing the mutation payload.
- If `middle` or `middleId` is provided and `middleLabel` is omitted, default `middleLabel` to `label` and send both so three-part relations can pass server validation.
- Both two-part and three-part relations must carry explicit labels, and those labels must describe the real business action or result.
- Do not use the aggregate name as the relation label. Aggregate is the node identity, not the explanation text.
- For two-part relations, `label` should describe the command intent or event result.
- For three-part relations:
  - `middleLabel` (aggregate side) = in-flight action = verb-object form
  - `label` (event side) = completed fact = "已" prefix or past-tense form
- Before execution, list `source`, `target`, optional `middle`, `relationType`, `label`, `middleLabel`, and duplicate-check implications in the confirmation table.

### Update relation

- Prefer relation id for updates.
- If the user only describes endpoints, use `list-relations` first to narrow the candidate set.
- `list-relations` may also use `relationType`, `label`, and `middleLabel` to further narrow the candidate set.
- If multiple relations still match, ask for clarification instead of guessing.
- If `middleId` is being set and `middleLabel` is omitted, default `middleLabel` to `label` before sending the update.
- Before execution, list the exact relation id and all fields that will change in the confirmation table.
- Example confirmation table for relation creation:

| 操作 | Source | Middle (聚合) | Target | middleLabel (聚合端) | label (事件端) | 规则/注意事项 |
| --- | --- | --- | --- | --- | --- | --- |
| 新增关系 | `BindResourceCommand` | `ResourceRelationAgg` | `ResourceBoundEvent` | 绑定资源 | 资源已绑定 | 聚合端=进行中动作；事件端=已完成事实 |

### Delete relation

- Delete by relation id.
- Use `list-relations` first when the user describes the relation by endpoints or label only.
- Before execution, list the exact relation id and the source/target pair in the confirmation table.

## Query order

Default to this order unless the user already gave a precise target:

1. Clarify the target context or node.
2. If auth is not ready, run `auth-status`.
3. If unknown, run `list-contexts`.
4. If the user is exploring one context, run `context-nodes` or `summarize-context`.
5. If they care about one node, run `node-detail`.
6. If they care about flow or impact, run `node-relations` or `summarize-relations`.
7. If they want to mutate a relation but lack relation id, run `list-relations` before update/delete.

## Response style

When answering the user:

- answer the result first
- prefer business-language conclusions over route or command names
- keep the language concise and pointed
- for mutation tasks, explicitly say what was created, updated, or deleted
- when useful, include the final node id or relation id in the confirmation
- default to concise output: 1 short conclusion + 2-4 flat bullets is enough
- do not narrate your investigation process unless the user asked how you checked it
- do not paste tokens, command history, or terminal progress into the main answer

Before a mutation is confirmed, prefer this answer shape:

```text
计划如下，请确认后我再执行：

| 操作 | 目标 | 影响节点 | 参数/字段 | 规则/注意事项 |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |
```

For write confirmations, prefer shapes like:

```text
结果：
已在 OrderContext 新增 PaymentTimedOutEvent。

补充说明：
- 节点类型：Event
- 显示名称：支付超时
- 节点ID：...
```

## Common workflows

### Understand one bounded context

1. `list-contexts`
2. `summarize-context <contextName>`
3. If needed, `context-nodes <contextName> "" true true`

### Inspect one node

1. `node-detail <nodeNameOrId>`
2. `summarize-relations <nodeNameOrId> outgoing context Event`
3. `summarize-relations <nodeNameOrId> incoming context Event`

### Create one node

1. `auth-status`
2. If needed, `auth-login-browser --project-id <projectId> --base-url <baseUrl> --permission write`
3. `create-node <jsonPayload>`

### Edit or delete one relation

1. `list-relations <jsonFilters>`
2. confirm the exact relation id
3. `update-relation <relationId> <jsonPayload>` or `delete-relation <relationId>`

## References

Read these only when needed:

- Query patterns: `references/query-patterns.md`

## Re-run evals

To generate a new iteration workspace for this skill:

```bash
DOMAIN_MODEL_API_BASE_URL="http://localhost:3000/api/v1" DOMAIN_MODEL_PROJECT_ID="<project-id>" DOMAIN_MODEL_ACCESS_TOKEN="<query-access-token>" node scripts/run-domain-model-iteration.mjs   --previous-workspace .codex/skills/domain-model-explorer-workspace/iteration-5
```
