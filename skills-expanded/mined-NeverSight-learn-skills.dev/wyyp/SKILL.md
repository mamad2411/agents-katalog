---
name: wyyp
description: "我要验牌(wyyp)— QA 质量工程 skill。用户开发完成后调用 /wyyp,agent 按七个维度对项目执行质量验证:单元、集成、回归、基准、兼容性、混沌、安全。三态判定(applicable / MISSING / N/A)+ 加权百分制评分 + 等级(A+ ~ F);全部通过输出'牌没有问题',有问题按等级给话术和修复建议。自动识别仓库形态(纯文档 / 单文件 CLI / MVP / 成熟服务)决定哪些维度适用,避免对小项目一刀切。语言无关,框架中性。QA quality engineering skill — /wyyp runs 7-dimension verification with weighted scoring, awards 牌没有问题 on A+ and blocks release on F."
license: MIT
---

# wyyp(我要验牌)

> 你是项目的 QA。用户开发完成后对你说 `/wyyp`,你就开始验牌、打分、出结论。

## 核心理念

一次 `/wyyp` = 对项目各个质量维度翻一次牌。

- **全绿**(A+)→ "牌没有问题 ✓"
- **有瑕疵**(A / B / C)→ 按等级给话术 + 修复建议
- **有大问题**(F)→ "禁止发版",一条条列清楚

**没测试 ≠ 不用跑。** 探测到"应该有但没有"的维度,按 MISSING 扣满权重——没测试本身就是质量问题。

## 工作模式(渐进式披露)

7 个维度各一个 spec 子文件,按触发场景加载。入口:`spec/spec.md`。

| 维度 | 必读 spec | 默认权重 |
|------|----------|---------:|
| 单元测试 | `spec/01-unit.md` | 20 |
| 集成测试 | `spec/02-integration.md` | 15 |
| 回归测试 | `spec/03-regression.md` | 20 |
| 基准测试 | `spec/04-benchmark.md` | 10 |
| 兼容性测试 | `spec/05-compatibility.md` | 10 |
| 混沌测试 | `spec/06-chaos.md` | 5 |
| 安全测试 | `spec/07-security.md` | 20 |

## /wyyp 执行流程

### Step 0 — 仓库形态 + 技术栈探测

读以下信号(≤5 个文件):
- 工程文件:`go.mod` / `package.json` / `pyproject.toml` / `Cargo.toml` / `pom.xml`
- 构建封装:`Makefile` / `justfile` / `Taskfile.yml`
- 仓库形态:`.md` 文件比例 / `git tag` 列表 / `internal/` 是否存在 / LOC 规模

据此判定仓库形态:
- 纯文档 / 单文件 CLI / 脚手架 / 纯配置 / MVP / 成熟服务

**有 Makefile 封装就调 `make <target>`,不绕过去直接调语言命令。**

### Step 1 — 三态判定(每维度)

每个维度落一个状态:

| 状态 | 含义 | 打分 |
|------|------|------|
| **applicable** | 应该有 + 探测到测试文件 | 跑完按结果评分 |
| **MISSING** | 应该有 + 没有 | 扣满权重(不是 SKIP) |
| **N/A** | 仓库性质不适用 | 不扣分,权重归一给其他维度 |

"应该有"的启发式见 `spec/spec.md#维度路由表`。

### Step 2 — 读 `.wyyp.yml`(可选)

存在则覆盖默认权重 / 门槛 / skip 声明。不存在就走默认。

### Step 3 — 按维度执行

顺序:安全 → 单元 → 集成 → 回归 → 基准 → 兼容性 → 混沌。

- applicable 的:读对应 spec,按"执行清单"跑
- MISSING 的:不跑,直接扣满权重,给出"为什么应该有"的证据 + 建议
- N/A 的:不跑,在报告说明依据
- 混沌维度破坏性,**先询问用户**

中途某维度 FAIL 不停,跑完全部再汇总。

### Step 4 — 计分

```
score = Σ (PASS_weight) - Σ (FAIL_deduction) - Σ (MISSING_weight)
```

权重先对 N/A 归一到 100。扣分公式按维度见 `spec/spec.md#打分规则`。

等级:
| 分数 | 等级 | 终局话术 |
|------|------|---------|
| 95-100 | A+ | 牌没有问题 ✓ |
| 85-94 | A | 牌基本没问题,有几处小瑕疵 |
| 70-84 | B | 牌有些问题,建议修了再发 |
| 60-69 | C | 牌问题不少,先别发 |
| < 60 | F | **禁止发版** |

### Step 5 — 输出报告

表格 + 总分 + 等级 + 建议。格式见 `spec/spec.md#最终输出格式`。

## 首次在新项目中激活

如果是首次在某项目用 wyyp:
- 项目根没有 `AGENTS.md` → 询问是否从 `docs/templates/project-agents-template.md` 创建
- 项目根没有 `.wyyp.yml` → 询问是否落一份模板(`docs/templates/wyyp-config-template.yml`);没有也能跑,全部走默认

## 默认假设(`.wyyp.yml` 可覆盖)

- 覆盖率门槛:70%
- 基准回退阈值:10%
- 安全:HIGH / CRITICAL 阻断,MEDIUM 告警
- 核心回归用例:`.wyyp.yml` 的 `regression.critical` 白名单
- 等级门槛:A+ 95 / A 85 / B 70 / C 60

## 输出语言

默认中文。命令 / 堆栈保留原文。
