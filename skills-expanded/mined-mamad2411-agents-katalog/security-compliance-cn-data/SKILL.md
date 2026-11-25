---
name: security-compliance-cn-data
canonical_id: security.compliance.cn_data
aliases: [pipl, china-data, cn-data-export, china-privacy]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Grep, Glob
forbidden-tools: Bash, WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - 中华人民共和国个人信息保护法 (PIPL): 2021
  - 中华人民共和国数据安全法 (DSL): 2021
  - 中华人民共和国网络安全法 (CSL): 2017, amended 2025 (NPCSC decision), effective 2026-01-01
  - 数据出境安全评估办法 (CAC 2022): 2022
  - 个人信息出境标准合同办法 (CAC 2023): 2023
  - 促进和规范数据跨境流动规定 (CAC 2024): 2024
  - 网络数据安全管理条例 (CAC 2024): 2024
  - 生成式人工智能服务管理暂行办法 (CAC 2023): 2023
sensitive_data_rules:
  never_read: ["real_chinese_user_data/**", ".env*", "secrets/**", "*.pem", "*.key"]
  never_write: ["actual Chinese PII", "真实身份证号", "actual phone numbers"]
  redact_on_output: ["身份证号 → mask 中间", "手机号 → mask 中间 4 位", "real name → 仅 first char"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling
downstream:
  - security-remediation
  - compliance.audit (planned)
  - appsec-security-orchestrator (back with findings)
description: >-
  China data protection overlay - PIPL, Data Security Law, Cybersecurity Law, cross-border transfer security assessment and the personal-information export standard contract, network data regulations, GenAI service rules. For projects processing Chinese personal information or exporting data from China. Engineering baseline and evidence prep, not legal counsel.
trigger_phrases:
  - PIPL / 个人信息保护法 / 中国数据合规
  - 数据出境 / 跨境数据 / data export from China
  - 数据本地化 / data localization / 网信办
  - 关键信息基础设施 / CIIO / critical information infrastructure
  - 个人信息处理 / sensitive personal information / 敏感个人信息
  - 算法备案 / 大模型备案 / GenAI 服务备案
  - 标准合同 / SCC / CAC 安全评估
---

# Security Compliance — China Data Protection

## 1. Mission

中国数据合规是 **多法叠加**：PIPL（隐私）+ DSL（数据安全）+ CSL（网络安全）+ 跨境出境多条规章 + 行业规则。本 skill 帮工程团队判断适用规章、做最小化设计、准备出境评估材料，**不**替代法务。

**职责边界**：
- **owns**: 工程层合规 baseline + scope 决策 + 出境流程触发 + evidence prep
- **不做**: 替代法务正式意见；行政许可申请代办
- **不做**: 处理真实中国 PII（hard rule）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 处理中国大陆境内自然人个人信息 | 强制激活（PIPL 全境内适用 + 域外效力）|
| 处理中国大陆 IP 访问的用户 | 评估是否触发境外提供 PI 给境内主体（PIPL 第 3 条域外）|
| 数据离开中国大陆边境（出境）| 强制激活 + 出境路径决策 |
| 关键信息基础设施运营者 (CIIO) | 强制激活 + 数据本地化要求 |
| 处理超过 100 万条 PI / 1 万条敏感 PI | 关注 CAC 安全评估申报阈值 |
| 提供 GenAI 服务给中国境内用户 | 激活 + 算法备案 + 大模型备案 |
| 自动化决策（评分 / 推荐 / 招聘）| 激活 + PIPL 24 条算法解释权 + 拒绝权 |
| 处理 14 岁以下 minor 数据 | 升 敏感个人信息 + 监护人同意 |
| 上线前合规 readiness | 走 §10 evidence package |

---

## 3. 中国数据合规法律体系速查

| 法律 / 规章 | 范围 | 关键义务 |
|---|---|---|
| **网络安全法 (CSL) 2017（2025 修订，2026-01-01 生效）** | 网络运营者 / CIIO | 等级保护 / CIIO 本地化 / 安全审查 / **2025 修订加强 AI 治理 + 强化处罚 + 数据保护责任** |
| **数据安全法 (DSL) 2021** | 所有数据处理（不限 PI）| 数据分类分级 / 重要数据出境管制 |
| **个人信息保护法 (PIPL) 2021** | 处理境内自然人 PI | 全生命周期保护 / 域外效力 / 算法 / 跨境 |
| **CAC 数据出境安全评估办法 2022** | 出境敏感 PI / 重要数据 | 安全评估申报（不是备案）|
| **CAC 个人信息出境标准合同办法 2023** | 出境非敏感 PI 一般场景 | SCC 签订 + 备案 |
| **CAC 促进和规范数据跨境流动规定 2024** | 大幅放宽中等规模出境豁免 | 自贸区清单 / 豁免情形 |
| **网络数据安全管理条例 2024** | 落地 PIPL/DSL/CSL 具体执行 | 各类合规细则 |
| **生成式 AI 服务管理办法 2023** | 提供 GenAI 给境内 | 算法备案 + 大模型备案 + 内容标识 |
| **行业（金融 / 医疗 / 汽车）** | 各行业额外要求 | 单独评估 |

---

## 4. 数据出境路径决策（核心）

2024 新规后，出境路径如下：

| 路径 | 适用 | 流程 |
|---|---|---|
| **A. 安全评估**（最严）| 1) CIIO 出境任意 PI；2) 一年内累计向境外提供 >100 万人 PI 或 >1 万人敏感 PI；3) 重要数据出境 | 向省级网信办申报 + CAC 审批 |
| **B. 标准合同 (SCC)**（中等）| 非 CIIO，一年内累计 ≥10 万人 PI 但 <100 万；或 <1 万人敏感 PI | 签 CAC 标准合同 + 个人信息保护影响评估 (PIPIA) + 备案 |
| **C. 认证**（少用）| 跨国集团内部 | 取得专业机构认证 |
| **D. 豁免**（2024 新规放宽）| 1) 履行合同必需（跨境购物 / 国际邮寄 / 跨境酒店）；2) HR 必需；3) 自贸区清单；4) **<10 万人非敏感 PI 出境（不含敏感 PI、不含重要数据）** | 无需评估 / SCC / 认证 |

### 敏感 PI 出境特殊规则（**核心铁律 — 不可绕过**）

**任意数量的敏感 PI 出境都不享受非敏感 PI 的豁免阈值**。具体：

| 敏感 PI 出境规模 | 路径 |
|---|---|
| 任意敏感 PI 出境，且年累计 <1 万人 | **B. SCC + PIPIA + 备案** 或 **C. 认证**（不能走 D 豁免）|
| 年累计 ≥1 万人敏感 PI 出境 | **A. CAC 安全评估**（强制）|
| CIIO 出境任意敏感 PI | **A. CAC 安全评估**（强制，无最低门槛）|

**敏感 PI 定义**（PIPL 第 28 条）：生物识别 / 宗教 / 特定身份 / 医疗健康 / 金融账户 / 行踪轨迹 / 14 岁以下儿童信息。任一即触发上表强化路径。

**Iron rule**: 
1. 出境前必须做 **个人信息保护影响评估 (PIPIA)**，记录归档至少 3 年。
2. 敏感 PI 出境**永不**走"<10 万人豁免"路径——豁免明文排除敏感 PI 与重要数据。
3. 重要数据出境**永远**走 A 安全评估，无例外。

---

## 5. Standard Workflow

```
Step 1  Scope determination
        → 列所有 system 处理中国 PI 的位置（境内 vs 境外）
        → 评估是否 CIIO（行业 + 关键性）
        → 列数据流（含数据出境路径 + 第三方接收方）
        → 统计：年度出境 PI 人数、含敏感 PI 人数

Step 2  Data classification (DSL + PIPL)
        → 一般数据 / 重要数据 / 核心数据（DSL 分级）
        → 一般 PI / 敏感 PI（PIPL 28 条）
        → 敏感 PI 含：生物识别 / 宗教 / 特定身份 / 医疗健康 / 金融账户 / 行踪轨迹 / 14 岁以下儿童

Step 3  Lawful basis (PIPL 13 条)
        → 同意 / 履行合同必需 / 法定职责 / 应急 / 公共利益 / 已公开
        → 文档化每个 processing activity 的 basis

Step 4  Notice + consent (PIPL 17 / 14 条)
        → 隐私政策中文版 + 易于理解
        → 单独同意（敏感 PI / 出境 / 自动化决策 / 公开）
        → Withdraw 同意机制易于使用

Step 5  Minimization + storage
        → 收集最小化（只收必要）
        → 存储期限明确 + 自动清理
        → 中国境内存储优先（特别 CIIO / 重要数据）

Step 6  Rights of data subject (PIPL 44-50 条)
        → 查阅 / 复制（结构化导出）
        → 更正
        → 删除（含 retention 满足后 / 同意撤回）
        → 限制 / 拒绝处理
        → 解释（自动化决策）
        → 申诉机制
        → 注：未成年 / 死者特殊条款

Step 7  Cross-border transfer assessment
        → 按 §4 决定路径
        → 准备 PIPIA 文档（必备字段）：
           - 数据接收方信息 + 所在国地区
           - 出境必要性 + 目的
           - 出境数据范围 + 敏感性
           - 接收方安全保护能力
           - 数据主体权利保障措施
           - 风险评估 + 应对措施
        → 申报 / 签订 SCC / 备案 / 验证豁免条件

Step 8  CIIO obligations (CSL)
        → 等级保护 2.0 测评（按级别 1-5）
        → 本地化存储（数据 + 个人信息）
        → 重要采购走安全审查（关键 IT 产品）
        → 内部安全部门 + 人员 + 演练

Step 9  GenAI specific (if applicable)
        → 训练数据合规（来源 + 处理 + 标注）
        → 算法备案（提供舆论属性 / 社会动员能力服务）
        → 大模型备案（基础模型）
        → 生成内容标识（深度合成）
        → 安全评估 + 用户实名

Step 10 Algorithmic accountability (PIPL 24)
        → 自动化决策透明度
        → 用户拒绝权
        → 重大影响决策（不利后果）提供解释 + 拒绝

Step 11 Incident response (PIPL 57)
        → Breach 立即通知监管 + 个人
        → 影响评估 + 补救措施
        → 走 security-response-incident-response + 补 PIPL-specific notification

Step 12 输出 + 路由
        → Scope + 适用路径报告
        → PIPIA 文档草稿（出境项目）
        → CIIO 评估（如适用）
        → 算法 / 大模型备案 readiness（如适用）
        → Findings → security-remediation
        → SECURITY.md cn-data section + AppSec Release Evidence §12 叠加层
        → Evidence package for CAC 申报 / 备案
```

---

## 6. 关键阈值速查

| 阈值 | 法律 | 后果 |
|---|---|---|
| 100 万人 PI（基础规模运营者认定） | 网络数据安全管理条例 | 增加 DPO / 评估义务 |
| 1000 万人 PI（大型运营者认定） | 网络数据安全管理条例 | 增加 风险评估 / 应急 / 审计 |
| 累计 >100 万人 PI 出境（含非敏感）| CAC 出境评估办法 | 必须申报安全评估 |
| 累计 ≥1 万人敏感 PI 出境 | CAC 出境评估办法 | 必须申报安全评估（敏感 PI 阈值，与非敏感不同）|
| 累计 ≥10 万人 PI 出境（非敏感）| CAC SCC 办法 | 签 SCC + 备案 |
| **<1 万人敏感 PI 出境** | 2024 新规 + CAC SCC 办法 | **必须走 SCC 或 认证（不享豁免）**|
| **<10 万人非敏感 PI 出境**（明确不含敏感 PI 与重要数据） | 2024 新规 | 豁免（验证条件）|
| 重要数据出境（任意量）| CAC 出境评估办法 | **永远走安全评估** |
| CIIO | CSL + CAC 评估 | 数据本地化 + 出境评估 + 等保 + 安全审查 |

---

## 7. Hard Rules

- ❌ **永不**未经同意收集敏感 PI（PIPL 29 条单独同意）
- ❌ **永不**未走出境路径就把中国 PI 传境外（含 backup / log shipping / SaaS analytics）
- ❌ **永不**让 SaaS provider（如 Datadog / Mixpanel / Sentry）默认采集 → 直接传美国 / 欧洲 服务器
- ❌ **永不**忽略 PIPIA 文档（出境前强制）
- ❌ **永不**用境外服务器处理 CIIO 数据（违反 CSL 本地化）
- ❌ **永不**用 disabled 用户拒绝自动化决策的接口（PIPL 24 强制权利）
- ❌ **永不**未备案就提供 GenAI 给境内用户（如有"舆论属性"）
- ❌ **永不**delete 个人请求处理超过 15 个工作日（PIPL 50）
- ❌ **永不**breach 后超 immediate 通知监管和个人（PIPL 57）
- ❌ **永不**把"国际化 / 跨境"等同于"可以传出境"
- ❌ **永不**把敏感 PI 出境塞进"<10 万人豁免"路径（豁免明文排除敏感 PI）
- ❌ **永不**忽略 CSL 2025 修订（AI 治理 + 强化处罚 + 数据保护责任新增）
- ❌ **永不**把"重要数据"按"一般数据"处理出境（重要数据出境永远走安全评估）

---

## 8. Anti-patterns

- ❌ "我们用 Google Analytics / Sentry 直接连境外，能用就用" — 默认违 PIPL + DSL 出境规
- ❌ "GDPR compliant 就够中国合规" — GDPR ≠ PIPL，多处不同
- ❌ "数据本地化是 CIIO 才要" — 一般运营者也有出境管制
- ❌ "标准合同签了就万事大吉" — SCC + PIPIA + 备案 + 持续监督
- ❌ "用户没勾敏感 PI 同意但不影响功能就允许" — PIPL 28 单独同意硬要求
- ❌ "10 万人阈值不到，随便出境" — 仍要 lawful basis + 安全措施
- ❌ "GenAI 大模型用境外开源就够" — 提供服务给境内 = 备案 + 标识
- ❌ "Breach 内部修一下不报" — PIPL 57 强制通知，违法成本高
- ❌ "我们公司在境外，不适用 PIPL" — PIPL 3 条域外效力（向境内提供产品 / 服务）
- ❌ "翻译一下英文 privacy policy 就行" — 内容 + 同意机制 + 易于理解都要重做

---

## 9. Output Contract

每次 review 产出：

1. Scope determination（中国 PI / CIIO / 出境路径）
2. 数据分类分级表
3. Lawful basis matrix per processing activity
4. Notice + consent 设计（隐私政策 + 单独同意）
5. Minimization + retention + 本地化策略
6. Data subject rights 实现 mapping
7. 出境路径决策 + PIPIA 文档草稿
8. CIIO obligations 评估（如适用）
9. GenAI 备案 readiness（如适用）
10. Algorithmic accountability design (PIPL 24)
11. IR plan PIPL addendum（57 条 + 通知模板）
12. Findings → security-remediation
13. SECURITY.md cn-data section + AppSec Release Evidence §12 叠加层
14. Evidence package for CAC 申报 / SCC 备案 / 算法备案

---

## 10. References

- [中国个人信息保护法](http://www.npc.gov.cn/npc/c30834/202108/a8c4e3672c74491a80b53a172bb753fe.shtml)
- [数据安全法](http://www.npc.gov.cn/npc/c30834/202106/7c9af12f51334a73b56d7938f99a788a.shtml)
- [网络安全法（2017 原文）](http://www.cac.gov.cn/2016-11/07/c_1119867116.htm)
- [**网络安全法 2025 修订（2026-01-01 生效）**](https://www.cac.gov.cn/2025-12/29/c_1768735112911946.htm)
- [数据出境安全评估办法 2022](https://www.cac.gov.cn/2022-07/07/c_1658811536396503.htm)
- [个人信息出境标准合同办法 2023](https://www.cac.gov.cn/2023-02/24/c_1678884830036813.htm)
- [促进和规范数据跨境流动规定 2024](https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm)
- [网络数据安全管理条例 2024](https://www.gov.cn/zhengce/zhengceku/202409/content_6976163.htm)
- [生成式 AI 服务管理办法 2023](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md)
- [security-response-incident-response](../security-response-incident-response/SKILL.md) — PIPL 57 通知
