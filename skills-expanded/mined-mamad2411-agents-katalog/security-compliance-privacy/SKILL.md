---
name: security-compliance-privacy
canonical_id: security.compliance.privacy
aliases: [gdpr, ccpa, cpra, privacy-compliance, data-protection]
version: 1.0.0
status: stable
created_date: 2026-06-10
updated_date: 2026-06-10
allowed-tools: Read, Grep, Glob, Bash
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - EU GDPR (Regulation 2016/679): in force
  - UK GDPR + DPA 2018: in force (post-Brexit UK regime)
  - California CCPA (as amended by CPRA): in force; CPRA fully operative 2023
  - CPRA regs (CPPA): consult current CPPA rulemaking text
  - EU-U.S. Data Privacy Framework (DPF): 2023 adequacy (status under litigation — verify)
  - EU SCCs (Implementing Decision 2021/914): in force
  - ISO/IEC 27701: 2019 (optional PIMS overlay)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key"]
  never_write: ["real EU/UK PII", "real California consumer PII", "actual names", "actual emails", "actual government IDs"]
  redact_on_output: ["email → mask local-part", "name → first char only", "national ID → mask middle", "IP address → truncate last octet/segment"]
upstream:
  - appsec-security-orchestrator
downstream:
  - security-remediation
  - security-response-incident-response  # breach clock (GDPR 72h / CCPA notice)
description: >-
  Privacy overlay for jurisdictions OUTSIDE China - EU/UK GDPR and CCPA/CPRA: lawful basis, data-subject rights and DSAR, consent, DPIA, Art 30 records, 72h breach notification, controller-processor DPAs, cross-border transfer (SCCs / TIA), privacy-by-design, retention, opt-out and Global Privacy Control. Engineering baseline, not legal counsel - verify time-sensitive claims against current regulation.
trigger_phrases:
  - GDPR / CCPA / CPRA / privacy compliance / data protection / 隐私合规 / 数据保护
  - DSAR / data subject rights / right to erasure / right to access / portability
  - consent / consent management / lawful basis / legitimate interest
  - DPIA / data protection impact assessment / records of processing / Art 30
  - cross-border transfer / adequacy / SCC / standard contractual clauses / TIA / Schrems II
  - Global Privacy Control / GPC / Do Not Sell or Share / opt-out of sale
  - controller vs processor / DPA contract / data processing agreement
  - special-category data / sensitive personal information / privacy by design
---

# Security Compliance — Privacy (GDPR + CCPA/CPRA, ex-China)

## 1. Mission

隐私合规在中国以外主要是 **两套互补但不等价的体系**：EU/UK **GDPR**（rights-based、全生命周期、域外效力）+ California **CCPA/CPRA**（consumer-rights + 商业行为约束，外加 GPC 信号义务）。本 skill 帮工程团队判断适用法域、把法规义务落到代码/架构、准备 DSAR / DPIA / RoPA / breach 证据，**不**替代法务。

**职责边界**：
- **owns**: 工程层 privacy baseline + scope（哪法域适用）决策 + 法规→代码映射 + DSAR/DPIA/RoPA/breach evidence prep
- **不做**: 替代律师正式意见；不替你做 controller↔processor 商业谈判；不出具 settled legal advice
- **不做**: 处理真实欧盟/英国/加州个人数据（hard rule，见 §sensitive_data_rules）
- **不做 China**：PIPL / DSL / CSL / 数据出境 → 路由 `security-compliance-cn-data`（见 §11 边界）
- **不做 payment**：PCI DSS / cardholder data → 路由 `security-compliance-payment`（见 §11 边界）

> **Honest disclaimer（贯穿全文）**：privacy law 持续变动——adequacy 决定可被法院推翻（Schrems I/II 已两次推翻 transfer 机制），CPRA 实施细则仍在 rulemaking，州级隐私法逐年新增。本 skill 给的是 **工程基线 + 当前理解**，任何 time-sensitive 结论（阈值、生效日期、adequacy 状态、罚款额、新法域）**必须 verify against current regulation / counsel**，不要把本文当成 settled fact。

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 处理 EU/EEA 境内自然人个人数据 | 强制激活（GDPR 适用，含域外效力 Art 3(2)）|
| 向 EU/EEA / UK 居民提供商品/服务 或 监测其行为 | 强制激活（GDPR 域外效力，即使公司在境外）|
| 处理英国居民个人数据 | 激活 UK GDPR + DPA 2018（与 EU 体系并行，独立 adequacy）|
| 处理 California 居民个人信息 且 满足 CCPA 业务门槛 | 激活 CCPA/CPRA（门槛见 §3，**verify current 阈值**）|
| "卖" 或 "分享" 个人信息（含定向广告 cookie）| 激活 CCPA opt-out + GPC 信号义务（§6）|
| 收到 data-subject / consumer 请求（access / delete / opt-out）| 走 §5 DSAR workflow |
| 新增 high-risk processing（profiling / 大规模特殊类别 / 系统性监控）| 触发 DPIA 评估（§7）|
| 个人数据 breach（confidentiality / integrity / availability）| 启动 72h 时钟 → 路由 `security-response-incident-response`（§9）|
| 个人数据离开 EU/EEA / UK 到第三国 | 触发 transfer 机制决策（§8 adequacy / SCC / TIA）|
| 引入第三方处理方（SaaS / analytics / 子处理方）| 触发 controller/processor + DPA 评估（§4.3）|
| 处理特殊类别 / sensitive PI（健康/生物识别/性取向/政治等）| 升级保护 + 额外 lawful basis（§4.2 / §6）|
| 上线前 privacy readiness | 走 §10 evidence package |

> 注：**中国相关触发词不在此表**（PIPL / 数据出境 / 网信办 / 关键信息基础设施 等）—— 那些一律由 `security-compliance-cn-data` 触发，本 skill 不抢工（§11）。

---

## 3. 适用法域速查（哪套规则管你）

| 体系 | 适用范围 | 核心义务摘要 |
|---|---|---|
| **EU GDPR** | EU/EEA 境内 controller/processor；**或** 向 EU/EEA 居民提供商品服务 / 监测行为的境外主体（Art 3）| lawful basis / data-subject rights / consent / DPIA / RoPA / 72h breach / transfer 机制 / privacy-by-design |
| **UK GDPR + DPA 2018** | 英国居民数据；与 EU 平行但独立（独立 adequacy 名单、独立 ICO 监管、独立 UK IDTA/Addendum transfer 工具）| 同 GDPR 结构，工具/名单需单独确认 |
| **California CCPA/CPRA** | for-profit 实体处理 CA 居民 PI **且** 满足门槛之一（**verify current**：年营收阈值 / 处理 PI 的消费者+家庭数量阈值 / 营收来自"卖/分享"PI 比例阈值）| consumer rights（know/delete/correct/opt-out）/ 卖&分享 opt-out + GPC / SPI 限制 / notice-at-collection / 不歧视 / service-provider 合同 |
| **其他美国州法**（多州陆续生效）| 各州门槛/口径不同 | ⚠️ **超出本 skill v1.0 详规范围**；命中时标 "verify against that state's statute + counsel" 并按 GDPR/CCPA 最严就高对齐 |

**Iron rule（适用判断）**：
1. GDPR 的触发**不看公司注册地**——只看"是否面向 EU/EEA 居民提供服务 / 监测行为"。"我们公司在美国/亚洲" **不是** 豁免理由。
2. CCPA 业务门槛是 time-sensitive 数字——**绝不**把记忆里的阈值当 settled，每次都标 "verify current CCPA thresholds with counsel"。
3. UK 与 EU 是 **两套**：adequacy 名单、transfer 工具（EU SCC vs UK IDTA/Addendum）、监管机构都各自独立，不可混用。

---

## 4. GDPR 核心义务

### 4.1 Lawful basis（六大合法性基础，Art 6）

每个 processing activity **必须**绑定且仅绑定恰当的一个（或多个）基础，并文档化：

| Basis (Art 6(1)) | 适用 | 工程含义 |
|---|---|---|
| **(a) Consent** | 用户自愿、具体、知情、明确的同意 | 需 consent management（可撤回、与服务不捆绑、默认不勾选）|
| **(b) Contract** | 履行与数据主体的合同所必需 | 仅限"必需"——不能借此塞营销 |
| **(c) Legal obligation** | 法定义务（如税务留存）| 文档化对应法条 |
| **(d) Vital interests** | 保护生命所必需 | 罕见（医疗急救）|
| **(e) Public task** | 公共利益 / 公权力行使 | 多为公共机构 |
| **(f) Legitimate interests** | 控制者/第三方正当利益，且不被数据主体权利覆盖 | **必须做 LIA（legitimate interests assessment）三步：purpose / necessity / balancing**；不可用于 special category |

**Iron rule（lawful basis）**：
1. **Consent 不是默认万能钥匙**——能用 contract/legal-obligation 的不要硬套 consent（同意可撤回会让你被动）；反之该 consent 的（如非必要 cookie / 营销）**绝不**伪装成 legitimate interest。
2. **每个 purpose 单独绑 basis**——一个 basis 不能笼统覆盖所有处理；purpose creep（拿登录数据去做广告）= 违 purpose limitation。
3. Special-category data（§4.2）**额外**需要 Art 9 例外，Art 6 basis 单独不够。

### 4.2 Special-category data（Art 9）

种族/民族、政治观点、宗教、工会、**基因、生物识别（用于唯一识别）、健康、性生活/性取向**。默认**禁止**处理，除非满足 Art 9(2) 例外（最常见：explicit consent / 雇佣与社保法定 / 重大公共健康 / 已由数据主体公开）。工程上要单独标记、单独 access control、单独 retention。

### 4.3 Controller vs Processor + DPA 合同

| 角色 | 定义 | 主要义务 |
|---|---|---|
| **Controller** | 决定处理的目的与方式 | 全责：lawful basis / rights / DPIA / breach 通知 DPA / 选合规 processor |
| **Processor** | 仅代表 controller 处理 | 按 controller 指令；Art 28 义务；sub-processor 需授权；协助 controller 履行 rights/breach |
| **Joint controllers** | 共同决定目的与方式 | Art 26 透明安排，划分责任 |

**Iron rule（DPA 合同）**：任何把个人数据交给第三方处理方（含 SaaS analytics / 云 / 客服工具 / AI API）**必须**有 **Art 28 DPA**（data processing agreement），含：处理范围/期限/目的、保密、安全措施、sub-processor 授权、协助 rights & breach、终止后删除/返还、审计权。**没有 DPA 就把个人数据塞进第三方 = 默认违规**。

### 4.4 Records of Processing Activities（RoPA，Art 30）

Controller（及 processor 各自）维护处理活动记录。最小字段：
- controller/processor 身份 + DPO 联系方式（如有）
- 处理目的
- 数据主体类别 + 个人数据类别
- 接收方类别（含第三国接收方）
- 第三国传输 + 适用 safeguard
- 计划的删除期限（per category）
- 技术与组织安全措施概述（TOMs）

工程上可由 data-flow inventory + 数据字典自动派生——**让 RoPA 成为 data inventory 的渲染视图，不要手维护两份**。

### 4.5 Privacy by Design & by Default（Art 25）

- **by Design**：处理设计阶段即内建保护（pseudonymisation / 最小化 / 加密 / access control）
- **by Default**：默认只处理 **每个具体目的所必需** 的个人数据——默认收集面最小、默认共享面最小、默认保留期最短、默认不公开。
- 工程落点：默认关闭非必要 telemetry、默认不勾选营销、默认 private 可见性、默认短 TTL。

### 4.6 Data minimization & retention

- 只收 **adequate / relevant / limited to necessary** 的数据（Art 5(1)(c)）。
- Storage limitation（Art 5(1)(e)）：不超过目的所需期限——需 **retention schedule per data class** + 自动清理 job（§5.3 工程清单）。

---

## 5. Data-subject rights + DSAR workflow（GDPR Ch.3，并 map 到 CCPA）

### 5.1 权利清单

| GDPR 权利 | Art | CCPA/CPRA 对应 | 工程含义 |
|---|---|---|---|
| **Access**（含 RoPA-style 信息）| 15 | Right to Know | 聚合该主体全部个人数据 + 处理信息，结构化导出 |
| **Rectification**（更正）| 16 | Right to Correct | 可编辑 + 传播更正给下游接收方 |
| **Erasure**（"被遗忘权"）| 17 | Right to Delete | 删除 pipeline，含 backups / logs / 第三方（§5.2）|
| **Portability**（可携带）| 20 | （CCPA 含于 Know 的可携格式）| 机器可读、commonly-used 格式（JSON/CSV）导出 |
| **Restriction**（限制处理）| 18 | — | 标记 "frozen"，停止处理但不删 |
| **Objection**（反对，尤其直销/legit-interest）| 21 | Opt-out of sale/share（部分重叠）| 可拒绝；直销反对为绝对权 |
| **Automated-decision 解释/人工介入** | 22 | — | profiling/自动决策需人工介入通道 |

### 5.2 DSAR 标准工作流（机器可执行骨架）

```
Step 1  Intake + 鉴权（identity verification）
        → 多渠道收口（email/in-app/web form）→ 统一 case
        → 验证请求者身份（防"假冒他人行使他人权利"——over-collection 也违规，验证适度）
        → 记录 received_at（启动 SLA 时钟）

Step 2  Scope + 定位（discovery）
        → 用 data inventory / data-flow map 定位该主体在所有系统的数据
        → 含：主库 / 副本 / 分析库 / 日志 / 缓存 / 第三方 processor / 备份
        → 区分 controller-held vs processor-held（processor 协助 controller）

Step 3  按请求类型执行
        → Access/Portability：聚合 + 结构化导出（JSON/CSV）+ 处理信息说明
        → Erasure：§5.3 删除 pipeline（含 backups 策略 + 通知下游接收方 Art 17(2)）
        → Rectification：更新 + 向已接收方传播
        → Restriction/Objection：标记停止处理（不必删）
        → 评估例外（法定留存 / 法律主张 / 言论自由 等）→ 文档化拒绝理由

Step 4  响应 SLA（**verify current 法定期限**）
        → GDPR：原则上"无不当延迟，且最迟一个月"（可在复杂时按法定延长，需告知）
        → CCPA：法定回应期限（**verify current**）；通常 45 天可延长
        → 注：具体天数随法规/指南变动，**以现行条文为准**，本文不锁死数字

Step 5  审计留痕
        → 记录 case 全过程（who/what/when/decision/rationale）作为 accountability 证据
        → Erasure 完成出"deletion certificate"（含范围 + backup 滞后说明）
```

### 5.3 Erasure pipeline 工程要点（最容易漏 backups）

- **主存储**：硬删除或不可逆匿名化（pseudonymisation 不等于 erasure——可重识别就不算删）。
- **派生/副本**：分析库、search index、cache、event log 同步删除/匿名化。
- **Backups**：备份通常不可逐条编辑——可接受做法是 **文档化 backup retention 周期 + 恢复时排除已删主体（suppression list / re-deletion on restore）**，并向数据主体说明 backup 滞后。**绝不**声称"已彻底删除"却把人留在可恢复备份里不加抑制。
- **第三方 processor**：通过 DPA 触发其删除（Art 17(2) 通知接收方）。
- **不可删的合法例外**：法定留存（税务/反洗钱）、法律主张所需——**保留例外部分，删其余**，并文档化。

---

## 6. CCPA/CPRA 专项（California）

| 主题 | 要求 | 工程落点 |
|---|---|---|
| **Consumer rights** | know / delete / correct / opt-out（of sale & sharing）/ limit use of SPI | 对应端点 + 鉴权 + SLA（§5）|
| **Sale & Sharing opt-out** | 提供 "Do Not Sell or Share My Personal Information" 链接/机制 | 注意 "sharing" 涵盖 **cross-context behavioral advertising**（很多广告/分析 cookie 即属此类）|
| **Global Privacy Control (GPC)** | **必须把浏览器/扩展发出的 GPC 信号当作有效 opt-out 请求 honor** | 服务端/前端读取 `Sec-GPC: 1` header（及对应 JS 信号）→ 自动置该用户/会话为 opt-out，无需用户再点 |
| **Sensitive Personal Information (SPI)** | 消费者可 "limit the use and disclosure of SPI" to 必要用途 | SPI 单独标记 + "Limit the Use of My SPI" 机制 |
| **Notice at collection** | 收集点告知类别 + 目的 + 是否卖/分享 + 保留期 | 收集表单/SDK 初始化处的 just-in-time notice |
| **Non-discrimination** | 不得因消费者行使权利而歧视（拒服务/差别定价）——financial incentive 须合规披露 | 行权不降级核心功能 |
| **Service provider / contractor 合同** | 与 CCPA 下的 service provider/contractor 需有合规合同条款（限制其用途）| 类比 GDPR DPA，但口径是 CCPA 术语 |

**Iron rule（GPC）**：GPC 是 **强制 honor** 的 opt-out 信号，不是可选优化。命中 `Sec-GPC: 1` 却继续"卖/分享"= 直接违 CPRA。服务端要在广告/分析数据外发**之前**检查 GPC/opt-out 状态。

> **Honest disclaimer**：CCPA/CPRA 的具体阈值、SPI 清单、SLA 天数、service-provider 合同必备条款随 CPPA rulemaking 与执法指南演进——**verify against current CPPA regulations / counsel**，本文是工程理解非 settled legal text。

---

## 7. DPIA（Data Protection Impact Assessment，GDPR Art 35）

**何时强制**：处理"可能对自然人权利自由造成高风险"时，尤其：
- 系统性、广泛的 **自动化决策 / profiling** 且产生法律或类似重大影响；
- **大规模** 处理 special-category data（§4.2）或刑事定罪数据；
- **系统性大规模监控** 公共可达区域。
- （并参考监管机构发布的 "DPIA 必做清单"——**verify current DPA list**。）

**怎么做（最小结构）**：
1. 系统描述 + 处理目的 + data flows；
2. 必要性 & 相称性评估（lawful basis / 最小化 / retention）；
3. 风险识别（对数据主体的风险，非仅对公司）；
4. 缓解措施（TOMs / pseudonymisation / 限权 / 透明度）；
5. 残余风险评估 → 若高风险无法降低 → **prior consultation with DPA**。

工程产物：`DPIA-<feature>.md`，与 threat-model / risk-register 并行（reliability/cost lens 不替代 DPIA 的 rights lens）。

---

## 8. Cross-border transfer（GDPR Ch.5，post-Schrems II）

把个人数据传出 EU/EEA（及 UK GDPR 下传出 UK）到第三国，必须有合法 transfer 机制：

| 机制 | 适用 | 注意 |
|---|---|---|
| **Adequacy decision**（Art 45）| 接收国/框架在欧委会 adequacy 名单（如 EU-U.S. DPF 认证企业）| ⚠️ adequacy **可被推翻**（Schrems I/II 先例）；DPF 当前正受司法挑战——**verify current status** |
| **SCCs**（Art 46，2021/914 模块化）| 无 adequacy 时主力工具 | 需选对 module（C2C/C2P/P2P/P2C）+ 填附录 + 配套 **TIA** |
| **BCRs**（Art 47）| 跨国集团内部 | 需监管批准，周期长 |
| **Derogations**（Art 49）| 例外（explicit consent / 合同必需 等）| 仅限偶发、有限，不可作常态机制 |

**Iron rule（transfer，post-Schrems II）**：
1. 用 SCC **不够**——必须做 **Transfer Impact Assessment (TIA)**：评估接收国法律（尤其政府 access / surveillance）是否削弱 SCC 保护，必要时加 **supplementary measures**（端到端加密 / pseudonymisation / split processing）。
2. **adequacy 状态是 time-sensitive**——上线前 verify 接收国/框架当前是否仍在名单，**绝不**把历史 adequacy 当永久有效（Privacy Shield 已被推翻是前车之鉴）。
3. UK 传输用 **UK IDTA / EU SCC + UK Addendum**，不是裸 EU SCC；EU 与 UK 名单各自独立。
4. 注意"传输"含 **隐性外流**：SaaS analytics 默认回传美国、日志 shipping、CDN、备份异地、第三方 AI API 调用——都算 transfer，需机制覆盖。

---

## 9. Breach notification（GDPR Art 33/34；CCPA 私诉风险）

| 维度 | GDPR | 工程动作 |
|---|---|---|
| **通知 DPA** | personal-data breach **risk to rights/freedoms** → "无不当延迟，且在 **知悉后 72 小时内**" 通知监管（除非不太可能造成风险）| 启动 72h 时钟（自"知悉"起）；准备 Art 33(3) 字段 |
| **通知数据主体** | 若 **high risk to rights/freedoms** → 还须 **无不当延迟** 直接通知受影响个人（除非已加密等使风险消解 / 不成比例努力则公告）| 受影响主体清单 + 通知模板 |
| **CCPA** | 加州有数据泄露通知法（civil code）+ CCPA 对特定个人信息泄露给予 **私人诉权 / 法定赔偿**——安全措施不足后果重 | 保留安全控制证据 |

**Iron rule（breach clock）**：
1. **72 小时从"知悉 (awareness)"起算，不是从"调查清楚"起算**——证据不全也要按时初报，后续补充（Art 33(4) 允许分阶段）。
2. Breach 处置 **必须** 路由 `security-response-incident-response` 跑取证/遏制/恢复，本 skill 只 **叠加** GDPR/CCPA 特定的 notification 义务 + 时钟 + 模板，不重复实现 IR pipeline。
3. **绝不**把"内部默默修掉、不上报"当选项——漏报本身是独立违规。

---

## 10. Standard Workflow（engineering checklist：法规→代码/架构）

```
Step 1  Scope determination
        → 列处理个人数据的所有系统 + 数据流（含第三方 processor、第三国流向）
        → 判定适用法域：GDPR? UK GDPR? CCPA/CPRA?（按 §3；其他州法标 verify）
        → 标记角色：controller / processor / joint（per processing activity）

Step 2  Data inventory + classification
        → 个人数据 / special-category（Art 9）/ CCPA SPI 分类标记
        → 派生 RoPA（Art 30）字段（让 RoPA = inventory 的视图）

Step 3  Lawful basis / purpose mapping
        → 每个 processing activity 绑 Art 6 basis（+ Art 9 例外 if special-category）
        → legitimate interest → 附 LIA；consent → 接 consent management
        → 防 purpose creep（一份数据被偷偷复用到新目的）

Step 4  Consent & notice（工程）
        → consent management：自愿/具体/知情/明确、可撤回、不与服务捆绑、默认不勾选
        → cookie/tracker：非必要默认 off；接入前先取 consent
        → notice-at-collection（CCPA）+ 透明度信息（GDPR Art 13/14）
        → record consent（时间/版本/范围）作为证据

Step 5  Rights / DSAR endpoints（工程）
        → access/export 端点（结构化导出 JSON/CSV）
        → deletion pipeline（§5.3：主库 + 派生 + cache + log + 第三方 + backup suppression）
        → rectification + 传播下游；restriction/objection 标记
        → identity verification（适度，不 over-collect）
        → SLA 计时 + case 审计留痕

Step 6  GPC / opt-out（CCPA，工程）
        → 读 `Sec-GPC: 1` header / JS 信号 → 自动 opt-out 该用户/会话
        → "Do Not Sell or Share" 机制；SPI use-limit 机制
        → 广告/分析数据外发前检查 opt-out 状态（拦截点）

Step 7  Retention & minimization（工程）
        → retention schedule per data class + 自动清理 job（cron/TTL）
        → privacy-by-default：默认最小收集 / 最小共享 / 最短保留 / 私有可见

Step 8  Cross-border transfer
        → 列所有出 EU/EEA(/UK) 的数据流（含隐性：SaaS/日志/CDN/备份/AI API）
        → 选机制（adequacy / SCC + TIA / BCR）→ verify adequacy 当前状态
        → 必要时加 supplementary measures（加密/pseudonymisation）

Step 9  Vendor / processor governance
        → 每个第三方 processor 有 Art 28 DPA（CCPA 下 service-provider 合同条款）
        → sub-processor 清单 + 授权链；终止后删除/返还约定

Step 10 DPIA（if high-risk per §7）
        → 出 DPIA-<feature>.md；残余高风险 → prior consultation 标记

Step 11 Audit logging
        → 记录 access to personal data / DSAR 处理 / consent 变更 / opt-out 状态变更
        → 作为 accountability（Art 5(2)）证据；日志本身遵守最小化（别把 PII 灌进日志）

Step 12 Breach readiness
        → IR plan 含 personal-data breach 分支（72h 时钟 + 受影响主体识别）
        → 模板 + 路由 security-response-incident-response（§9）

Step 13 输出 + 路由
        → Scope + 适用法域报告 + 角色矩阵
        → Lawful basis matrix / RoPA 草稿 / DSAR design / DPIA（如适用）/ transfer 决策 + TIA
        → Findings（schema v1.0）→ appsec-sdk finding.add → security-remediation
        → SECURITY.md privacy section + AppSec Release Evidence §12 叠加层
        → 与 cn-data / payment 叠加层并列（不互相覆盖，§11）
```

---

## 11. 边界 / 不重叠声明（Iron rule — 组合而非吞并）

本 skill 是 **ex-China 隐私法规合规 overlay**，与以下相邻能力 **并列组合**，不互相替代：

| 相邻能力 | 谁拥有 | 本 skill 的动作 |
|---|---|---|
| **China 数据合规**（PIPL / DSL / CSL / 数据出境 / 网信办 / CIIO / 算法备案）| `security-compliance-cn-data` | **不碰**。命中中国相关触发词 → 路由 cn-data。中国主体的隐私走 cn-data，本 skill 只管 EU/UK/CA。两者可在一个项目里并存（如全球产品）|
| **Payment / 卡数据**（PCI DSS / PAN / CVV / SAQ / tokenization）| `security-compliance-payment` | **不碰**。支付卡合规 → 路由 payment。注：支付场景里的**持卡人个人数据**（姓名/地址）仍受 GDPR/CCPA——payment 管 PCI，本 skill 管该数据的 privacy rights，两者叠加 |
| **`operations.privacy` capability**（orchestrator §5.4，operational data-handling）| AppSec orchestrator operations 层 | **区分**：`operations.privacy` 是 **运营层数据处置**（怎么安全地搬运/留存/最小化数据的工程操作）；本 skill 是 **regulatory-compliance overlay**（GDPR/CCPA 法定义务映射）。本 skill 产出"法规要求什么"，operations 层执行"工程上怎么稳妥处置"——本 skill 是合规叠加层，不是 operations 的实现 |

**Iron rule（de-conflict with cn-data）**：触发路由按"**地域 / 数据主体所在地**"切分——
- 数据主体是 **EU/EEA / UK / California 居民** 或出现 GDPR/CCPA/DSAR/GPC/SCC 等 ex-China 术语 → **本 skill**；
- 数据主体是 **中国大陆境内自然人** 或出现 PIPL / 数据出境 / 网信办 / 关键信息基础设施 / 算法备案 等术语 → **cn-data**；
- 全球产品两边都触发 → **两个 skill 都激活、各管各法域、证据各自落盘并列**，谁都不覆盖谁。

---

## 12. Hard Rules（不可违反）

- ❌ **不读** `.env*` / `secrets/**` / `*.pem` / `*.key` 文件内容（PreToolUse hook 物理拦截）
- ❌ **不处理 / 不写入** 真实 EU/UK/CA 个人数据到 test fixture / dev DB / chat / report（hard rule）
- ❌ **不在** chat / log / report / SECURITY.md 输出 raw PII（email / name / 国民 ID / 精确 IP）——先走 redact
- ❌ **不把** "公司在境外" 当 GDPR 豁免理由（Art 3 域外效力看的是面向谁提供服务）
- ❌ **不把** 个人数据交给没有 Art 28 DPA 的第三方 processor（含 SaaS/analytics/AI API）
- ❌ **不把** 非必要 cookie / 营销处理伪装成 legitimate interest 来跳过 consent
- ❌ **不用** 一个 lawful basis 笼统覆盖多个 purpose（purpose creep = 违 purpose limitation）
- ❌ **不忽略** `Sec-GPC: 1` opt-out 信号继续卖/分享（直接违 CPRA）
- ❌ **不声称** "已彻底删除" 却把人留在可恢复 backup 里且无 suppression（§5.3）
- ❌ **不把** 历史 adequacy 当永久有效——transfer 前 verify 当前 adequacy 状态（Schrems 前车之鉴）
- ❌ **不用** 裸 EU SCC 覆盖 UK transfer（需 UK IDTA / Addendum）
- ❌ **不超** 72h breach 通知时钟（从"知悉"起算，证据不全也先初报）
- ❌ **不把** breach "内部默默修掉不上报" 当选项（漏报是独立违规）
- ❌ **不替代** 法务——任何 time-sensitive / 法定结论标 "verify against current regulation / counsel"
- ❌ **不碰** China（→ cn-data）/ payment-PCI（→ payment）—— 越界即违反 §11 边界

---

## 13. Anti-patterns

- ❌ "我们是 GDPR compliant，所以中国/加州也没问题" — GDPR ≠ PIPL ≠ CCPA，三套不等价
- ❌ "公司注册在境外，GDPR 管不到我们" — Art 3 域外效力（面向 EU 居民提供服务即触发）
- ❌ "用 Google Analytics / Sentry 直连，能用就用" — 默认含跨境 transfer + 缺 DPA + 可能违 GDPR
- ❌ "Cookie banner 弹一下、默认全勾选" — 非自愿/默认勾选不构成有效 consent
- ❌ "Legitimate interest 是万能基础" — 营销/非必要 tracker 套 LI 跳过 consent = 违规
- ❌ "删除就是把 status 改成 deleted" — soft-delete 可重识别 ≠ erasure；还漏 backup/log/第三方
- ❌ "GPC 信号是可选优化,先不做" — CPRA 下强制 honor，无视即违法
- ❌ "SCC 签了就能随便传美国" — post-Schrems II 必须配 TIA + 可能 supplementary measures
- ❌ "Privacy Shield 之前能用,现在应该也行" — 已被推翻；adequacy 是 time-sensitive
- ❌ "DPIA 是 legal 的纸面活" — 是 high-risk processing 的法定前置 + 工程缓解依据
- ❌ "Breach 先查清楚再报" — 72h 从知悉起算，必须按时初报后补充
- ❌ "把所有用户数据塞进日志方便 debug" — 违最小化 + 日志成 PII 泄露面
- ❌ "处理 China 用户的隐私也在这个 skill 里一起做" — 错，China → cn-data（§11）

---

## 14. Output Contract

每次 review 产出：

1. Scope determination（适用法域：GDPR / UK GDPR / CCPA-CPRA / 其他州标 verify）+ 角色矩阵（controller/processor/joint per activity）
2. Data inventory + classification（个人数据 / special-category / CCPA SPI）
3. RoPA（Art 30）草稿（inventory 的视图）
4. Lawful basis matrix per processing activity（+ LIA / Art 9 例外 如适用）
5. Consent & notice design（consent management + notice-at-collection + 透明度）
6. Data-subject / consumer rights 实现 mapping + DSAR workflow design（含 erasure pipeline + backup suppression）
7. GPC / opt-out / SPI-limit 工程设计（CCPA）
8. Retention schedule + minimization + privacy-by-default 落点
9. Cross-border transfer 决策 + TIA（如适用，含 adequacy 状态 verify 注记）
10. Vendor / processor governance（Art 28 DPA / CCPA service-provider 合同清单 + sub-processor 链）
11. DPIA（如 high-risk，§7）
12. Breach readiness（72h 时钟 + 受影响主体识别 + 模板）→ 与 security-response-incident-response 协同
13. Findings（schema v1.0，severity lower-case，redact-first）→ `appsec-sdk finding.add` → security-remediation
14. SECURITY.md privacy section + AppSec Release Evidence §12 叠加层（与 cn-data / payment 并列）
15. **Disclaimer 注记**：所有 time-sensitive 结论标 "verify against current regulation / counsel"

> **Finding 落盘契约**：所有 finding 必须符合 `appsec-security-orchestrator §9 Standardized Finding Schema v1.0`，`source: manual_review`（或 `threat_model`），`severity` 取 lower-case（critical|high|medium|low），写入只能走 `appsec-sdk finding.add`（PostToolUse/PreToolUse hook 校 schema + 拦直接 Write）。输出前所有 PII 走 redact。breach-related timeline 与 `security-response-incident-response` 协调（72h / CCPA 通知），不重复实现 IR。

---

## 15. References

> Privacy law evolves — 以下为定位入口，具体条文/阈值/adequacy 状态 **以官方现行版本为准**，verify before relying.

- [EU GDPR (Regulation 2016/679) — EUR-Lex consolidated](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [UK GDPR + Data Protection Act 2018 — ICO guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/)
- [EDPB guidelines (DSAR / DPIA / transfers / consent)](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en)
- [EU SCCs — Implementing Decision (EU) 2021/914](https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj)
- [EDPB Recommendations 01/2020 on supplementary measures (Schrems II / TIA)](https://www.edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en)
- [California CCPA/CPRA — California Privacy Protection Agency (CPPA)](https://cppa.ca.gov/regulations/)
- [California Civil Code §1798.100 et seq. (CCPA text)](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5)
- [Global Privacy Control (GPC) spec](https://globalprivacycontrol.org/)
- [ISO/IEC 27701:2019 (PIMS, optional overlay)](https://www.iso.org/standard/71670.html)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §9 finding schema + §5.6 compliance map
- [security-remediation](../security-remediation/SKILL.md) — finding → fix → regression
- [security-response-incident-response](../security-response-incident-response/SKILL.md) — breach clock (GDPR 72h / CCPA notice)
- [security-compliance-cn-data](../security-compliance-cn-data/SKILL.md) — China (NOT covered here; §11 boundary)
- [security-compliance-payment](../security-compliance-payment/SKILL.md) — PCI/payment (NOT covered here; §11 boundary)
