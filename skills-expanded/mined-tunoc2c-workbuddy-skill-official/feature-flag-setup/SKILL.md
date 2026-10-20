---
name: feature-flag-setup
pack: universal
description: 给一个新功能加一个完整的特性开关——更新 @app/flags 的 FLAGS 登记表、设保守默认值、配 .env.*.example 灰度规则、文档化 kill switch 操作。每个新功能上线前必走。
when_to_use: implementer agent 收到带 "FLAGS.<KEY>" 约束的任务时;架构师任务模板第 5 段提到新 flag 时;或 review 阶段发现 PR 没把功能藏在开关后时。
when_NOT_to_use: 改的是已有 flag 的灰度参数(那是 ops 动作,不走 PR)。
---

# Skill: Feature Flag Setup

每个新功能**必须**藏在特性开关后——这是 harness 的"可反悔权"。

## 步骤(原子动作,不可省略)

### 1. 登记 flag(`packages/flags/src/index.ts` 或 kit 的 `flags/feature-flags.ts`)

```ts
export const FLAGS = {
  // ... 已有 ...
  NEW_GREETING: 'new_greeting',   // ← 新增,key 用 snake_case,字符串
} as const;

const FLAG_DEFAULTS: Record<FlagKey, boolean> = {
  // ...
  [FLAGS.NEW_GREETING]: false,    // ← 默认务必 false(fail-safe)
};
```

### 2. 业务代码用依赖注入,不要直接吃 flag 单例

❌ `if (await flags.isEnabled(FLAGS.X)) ...`(测试时无法覆盖)
✅ 服务接收 `getVariant`/`isEnabled` 注入,生产由 main.ts 注入真 flags(见 services/api/src/server.ts 范式)

### 3. 配灰度规则(`config/.env.dev.example` 与 `.env.prod.example`)

**两份 KEY 集合必须一致**(CI 的 env-parity 会拦):

```
# .env.dev.example
FLAG_new_greeting={"enabled":true,"rolloutPct":100}

# .env.prod.example
FLAG_new_greeting={"enabled":true,"rolloutPct":5}
```

### 4. 在 PR 描述里写明灰度计划

```
## Feature flag
- Key: NEW_GREETING
- Default: false (fail-safe)
- 灰度: teamOnly → 5% → 25% → 100%(每档观察 24h)
- Kill switch: FLAG_new_greeting='{"enabled":false}'
- 观测指标: <CTR 或转化等>
```

### 5. 验收(PR 合之前):写一行测试证明 kill 起作用

```ts
test('kill switch turns the feature off', async () => {
  const provider = new LocalProvider({ NEW_GREETING: { enabled: false } });
  expect(await provider.isEnabled('new_greeting', {}, false)).toBe(false);
});
```

## Statsig 升级(Day 0 用本地 provider 就够,这部分可选)

到团队 > 10 人或需要可视化看板时,在 `flags/feature-flags.ts` 已有的 `StatsigProvider` 上接 `STATSIG_SERVER_SECRET`,业务代码零改动。

## 反模式

- ❌ flag 默认 `true`——失去 fail-safe
- ❌ flag 直接吃单例不注入——测试覆不到
- ❌ kill 步骤写"redeploy"——失去"无需部署即时关闭"的能力
- ❌ 两份 env 模板的 FLAG_ key 数不一致——CI 拦你
