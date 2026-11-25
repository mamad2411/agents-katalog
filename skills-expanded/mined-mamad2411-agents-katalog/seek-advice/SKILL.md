---
name: seek-advice
description: 跨家 LLM 顾问 panel——给一个最小化 scenario，并行 dispatch 给 3-5 个不同 vendor 的模型，每个模型同时跑联网+离线两份，对抗单家族 prior 高度相关导致的 anchoring 偏差。用于复杂诊断、重要技术决策、自己推理 ≥2 小时未收敛兜底。
triggers:
  - 卡住了
  - 拿不准
  - 找别的模型问问
  - 跨家求助
  - 跨家诊断
  - prior anchoring
  - seek_advice
  - second opinion
  - 第二意见
  - 顾问 panel
  - 跨模型咨询
scope: main
---

# Seek Advice Skill

**对抗 prior anchoring 的跨家 LLM 顾问 panel。**

## 为什么存在这个工具

同一模型家族的训练语料高度相关——给同一个模糊症状，Opus 4.7 和 Sonnet 4.6 倾向于走同一条 prior（即使两次独立采样）。当 prior 错时，多次同家族采样只会反复确认错误诊断。

**实证案例（2026-06-02，Max 真实 case）**：服务器 boot 慢，每 30s 刷一条 dmesg。Root cause 是 `console=ttyS0` 让 BMC 虚拟串口 drain 慢，每条 printk 同步阻塞 30s。对照实验结果：

| Model | Prompt | Web Search | 结论 |
|---|---|---|---|
| Gemini 2.5 | 极简纯现象 | ✅ | **第一轮命中**（console 串口 drain） |
| GPT-5.5 | 极简纯现象 | ✅ | ❌ 被搜索结果拉去 SCSI/RAID |
| Opus 4.7 | 极简纯现象 | ❌（禁工具） | ❌ prior anchor 到 SCSI timeout |
| GPT-5.5 | 详细排除 SCSI 后 | ❌ | ✅（被显式排除引导后才跳过去） |
| Opus 4.7 | 详细给完整对照表 | ❌ | ✅（从 pattern 反推机制） |

结论：**单家族 + 单 prompt 容易卡死**。要突破必须 (a) 跨家族 (b) 严格 minimal scenario 不带导向词 (c) 同时看联网/离线两种结果，对照"模型基于训练 prior 的纯推理" vs "模型借助搜索结果的判断"——**两者同等重要，谁都不必然更准**。

## 工具

### `list_models()`

无参数。返回当前 maxclaw LLM 配置里全部 chat-capable provider，按 vendor 归类。

```ts
list_models() returns Array<{
  id: string,       // 完整 provider id, e.g. "anthropic/claude-opus-4-7"
  family: string,   // "anthropic" | "openai" | "google" | "chinese" | "other"
  notes?: string,   // 简短说明（若有）
}>
```

先 call 这个拿可用集合，再挑选传给 `seek_advice`。

### `seek_advice({scenario, models})`

| 参数 | 类型 | 约束 |
|---|---|---|
| `scenario` | string | ≤500 字纯现象陈述；含导向词会被 sanity check reject |
| `models` | string[] | 3-5 个 provider id；都必须在 `list_models()` 返回集合内；强烈建议跨 ≥3 家 vendor |

返回：

```ts
{
  advice: Array<{
    model: string,            // 调用的 provider id
    with_web_search: boolean, // 是否注入了 maxclaw_web_search 工具
    response: string,         // 模型最终回答原文
    elapsed_ms: number,
    error?: string,           // 该 slot 超时/失败时填，response 为空
  }>
  // length = models.length × 2，每 model 出现两次（联网 / 离线）
}
```

行为细节：
- **scenario sanity check**：palette:light 跑一次预检，命中导向词或暗示方向 → tool error，错误信息附 `suggested_rewrite`
- **并行 dispatch**：models × 2 个 slot 同时发请求
- **单 slot 5min 超时**：触发场景是 ≥2 小时未收敛的兜底，panel latency budget 是"几分钟"而不是"几十秒"——超时的 slot 在 `advice` 里以 `error` 字段呈现，不阻塞其他
- **不返回成本**：避免暗示"用得多很贵"——这个工具就是要被频繁用

## 触发场景

| 场景 | 是否该 seek_advice |
|---|---|
| 复杂诊断、病因不明、自己已试错 ≥2 次未命中 | ✅ |
| 架构选型／重大方案抉择（A 还是 B） | ✅ |
| 自己推理 ≥2 小时未收敛 | ✅ 兜底使用 |
| 单点事实查询（"X 命令的参数是什么"） | ❌ 用 maxclaw_web_search 就够 |
| 用户已经给出方向，只是要执行 | ❌ |
| 想找借口推卸判断责任 | ❌ |

## scenario 写法

### 模板

```
[硬件背景一两句]
[软件版本一两句]
[症状定量描述]
[对照实验如有]
请分析潜在原因。
```

### ✅ Good example（Max 2026-06-02 给 Gemini 的原话，第一轮命中真凶）

> 我这边有台服务器，安装了 Ubuntu Server 22.04 系统。无论是使用 RAID 卡 RAID 模式还是 JBOD 模式，无论内核参数，安装时速度正常，启动后 dmesg 内核日志是稳定的每 30s 刷一行，非常缓慢，你去帮我搜搜潜在的原因。

为什么好：
- 纯现象（"每 30s 刷一行"是量化观察，不是猜测）
- 给了对照（RAID/JBOD 都试过，内核参数也试过——告诉模型不是这两个轴）
- 零导向词（没说"我觉得是 SCSI"也没说"可能是磁盘"）
- 自然的"你去搜搜"开放式 framing，不预设答案

### ❌ Bad example（typical agent 添油加醋版）

> 服务器 boot 慢，dmesg 显示 sd 设备 30s timeout，我已经排除了 RAID 模式问题（JBOD 也慢），怀疑是 SCSI subsystem 的 retry 机制有问题，或者可能是某个 udev rule 触发了 device probe 反复重试。需要排查 mpt3sas driver 的 timeout 配置或 systemd 的 udev settle 阶段。请帮我看怎么定位。

为什么烂：
- 把"SCSI"塞进 scenario → 所有模型立即被锚定到 SCSI subsystem 这条死胡同
- "dmesg 显示 sd 设备" 是诊断结论，不是原始观察（实际看到的是 printk 每条 30s 间隔，不是某个 sd device）
- 暗示已知方向，模型只会在用户暗示的范围内细化，丢失 Gemini 那种"问号式"探索的机会
- 读起来像 ongoing debug 的中段而不是问题描述

### 写 scenario 前自检三问

1. **去掉这句话信息会丢吗**？丢不了 → 删
2. **这是观察还是推测**？推测全删
3. **如果是聪明的陌生工程师看到这段，会被引到哪个方向**？被引导 → 改写

## 模型挑选建议

先调 `list_models()` 拿到当前可用列表，每条带 `id` 和 `palettes`。挑 model 走**两个正交的轴**：

### 轴 1：跨 vendor 家族（核心，对抗 prior anchoring）

vendor 直接看 `id` 前缀，不靠工具显式标注（因为 id 本身就携带这个信息）：

| id 前缀 | vendor |
|---|---|
| `anthropic/...` / `oauth:anthropic/...` | Anthropic |
| `ellyecode/...` / `ellyecode-cyber/...` / `openai/...` / `oauth:openai/...` | OpenAI（含中转） |
| `oauth:gemini/...` | Google |
| `xiaomi/...` / `deepseek/...` / `doubao/...` / `kimi/...` 等 | 国产各家 |

**至少 3 家不同 vendor**，例如 anthropic + openai + google。4-5 家加上一个国产 vendor。
避免同家族两个（"opus-4-7 + opus-4-6" 基本是同一 prior 调两次，浪费 panel slot）。

### 轴 2：capability tier（看 palettes 字段）

`palettes` 标识 model 在配置里的 tier 归属。常见 tier：

- **frontier** — 旗舰能力，推理深 reasoning 强（如 opus 系列、gpt-5.5）。**默认 panel 主力。**
- **mid** — 二档能力（sonnet 系列、mimo 旗舰）。frontier 不够用或想验证 frontier 结论时混入。
- **light** — 轻量任务模型（haiku、mimo 普通版、flash 系列）。**不适合 seek_advice**（推理深度不足，会拉低 panel 质量）。
- **vision-ui** / 其他 tier — 跟 capability 正交的特殊用途标签，seek_advice 一般忽略。

**典型 panel 配方**：3 个 frontier + 跨 ≥3 家 vendor。例如：

```
[anthropic/claude-opus-4-7, ellyecode/gpt-5.5, oauth:gemini/default:gemini-2.5-flash]
```

如果 frontier 不足 3 家（比如 google 没有 frontier model），从 mid 补一个跨家的；不要因为凑数把 light model 塞进来。

### 注意

`list_models` 不再返回 hardcoded `family` 字段——之前那个手工分类规则很容易跟新增 provider 不同步。现在 vendor 判断让调用方自己看 id 前缀，capability tier 让调用方自己看 `palettes`，两者都从配置真实数据来，零维护漂移。

## 怎么解读结果

返回 N × 2 条回答，按以下顺序看：

1. **联网命中 vs 离线命中是否一致**：一致 → 高 confidence；不一致 → 看具体歧点是哪一类
   - 联网说 X、离线说 Y → 通常 X 借助实时信息更新过，但也可能 X 被搜索结果带偏（如 2026-06-02 GPT-5.5 联网被拉到 SCSI）
   - 离线全说 X、联网都说 Y → search 显著改变了判断，X 可能是 stale prior
2. **跨家族交集**：3 家不同 vendor 都指向同一原因 → 强信号
3. **唯一异类**：某一家说出别家没说的具体机制 → 不要立刻 discard，反而值得追查（Gemini 第一轮命中就是异类）
4. **never** 把联网当成"权威版本"——联网会引入 search bias

## 自我约束

- 工具结果是输入，不是结论。Claw 自己合成判断后再回 Max
- 不允许把 6 份回答原样贴给 Max——总结分歧 + 你的判断
- 若 6 份全说"信息不足，需要 X"——补 X 再来一轮，不要硬着头皮选一个
