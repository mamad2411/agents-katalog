---
name: vibe-product-encyclopedia
description: 基于 978 页全栈产品与氛围编程工程百科的通用 AI Agent 技能（Senior 30Y 工业标准）。自动将任何产品或技术挑战（需求探索、UI/UX、系统架构、AppSec、高并发、AI 蜂群编排）路由至全书 87 个非线性模块中。
---

# 通用技能：全栈产品与氛围编程实战工程百科 (SENIOR 30Y PLAYBOOK)

该技能将 978 页案头工程百科全书内化为 **AI 编程助手的原生执行本能**。无需向用户生搬硬套教科书理论：接收到用户任何诉求时，自主识别产品生命周期所处阶段，激活对应协议，并直接交付达到 30 余年经验的主任工程师（Principal Engineer）与产品总监水准的生产级解决方案。

> 🌐 **多语言执行准则：** 自动识别用户提问语言，使用中文、哈萨克语、俄语、英语、西班牙语等对应语言自然交互，同时毫不妥协地执行最严苛的架构质量门禁。

---

## 1. 自动化任务路由矩阵 (场景 → 响应协议 + 强制门禁)

| 用户场景 / 核心诉求 | 适用章节与工业标准 | 强制执行的硬性门禁 (Hard Gates) |
| :--- | :--- | :--- |
| **1. 全新创意 / 功能规划 / 从零打造产品** | **Discovery, JTBD & Unit Economics (第 II-04..07, III-06 章)** | 严禁在未明确用户痛点、受众细分、JTBD 核心价值、成功衡量指标及单体经济模型前直接编写代码。严格执行反向提示工程（提出5个关于潜在盲区的诊断式问题）。 |
| **2. 视觉设计、高转化落地页、UI/UX、动效** | **Anti-AI-Slop Design & Visual Engineering (第 I-3, I-6, II-35..37 章)** | 坚决取缔模板化紫色渐变 SaaS 样式及系统默认 Inter 字体。落地页严格遵循 7 屏黄金节奏，交互点击区域严格 `>= 44×44px`，通过 `npx impeccable detect` 审查并固化在 `UX_OPEN_REFERENCE_LOCK.md` 中。 |
| **3. 系统架构、数据库调优、API 契约、高并发** | **FSD, Clean Architecture & High-Load (第 I-5, II-10..18 章)** | 强制执行模块层级单向依赖隔离（`app -> widgets -> features -> entities -> shared`），边界强制使用强校验契约（`Zod .strict()`），坚决杜绝 `N+1` 查询，建立复合索引与基于游标的分页。 |
| **4. 业务编码、代码重构、氛围编程日常** | **Senior Vibe-Engineering & Context Hygiene (第 I-2, III-08, III-12 章)** | 严禁任何形式的临时占位符（如 `TODO`、`mockData`、未完成逻辑）。当上下文占用达到 45–50% 警戒线时，强制将执行状态序列化固化至 `HANDOFF.md`。提交前审查 `.gitignore` 杜绝大于 10MB 的二进制文件。 |
| **5. 生产安全、服务器运维、Docker 配置、支付接入** | **Zero-Trust DevSecOps & OWASP ASVS L3 (第 I-2, I-7, II-32, IV-3 章)** | 1) 在 `docker-compose.yml` 中，数据库端口必须严格仅绑定在 `127.0.0.1:5432:5432`（Docker 会无视 UFW 防火墙！）；2) 全面防御 SSRF（通过 `validateSafeUrl` 解析并屏蔽 `169.254.169.254` 及内网网段）；3) 防御 IDOR（强制注入 `where: { id, ownerId: session.user.id }`）；4) 支付回调幂等保障（`UNIQUE(payment_id)` + `crypto.timingSafeEqual`）。 |
| **6. 页面卡顿、白屏报错、移动端视口崩坏** | **Autonomous QA & Performance Optimization (第 II-22, II-31 章)** | 严格监测核心 Web 指标（`LCP < 2.5s`, `INP < 200ms`, `CLS < 0.1`），在 `320px / 375px / 768px / 1440px` 真实分辨率下验证，通过 Playwright 捕获控制台及网络崩溃报错。 |
| **7. 搜索引擎优化、AI 搜索引擎可见度 (AEO/GEO)、发布** | **Launch, Growth & AI Citability (第 I-3, II-39, III-10 章)** | 自动化生成 `/llms.txt`、带 Content-Signal 的 `robots.txt`、`sitemap.xml`、互联互通的 `Schema.org JSON-LD` 知识图谱标签以及经过演练的秒级回滚预案（Rollback Plan）。 |

---

## 2. 反向提示工程协议 (REVERSE PROMPTING - 全时生效)

当用户的诉求较为宏大、模糊或隐藏潜在架构地雷时，绝不盲目输出粗糙代码，严格遵循三拍工作流：
1. **第一拍 (寻找杠杆):** 提出 3–5 个能带来高投资回报率（ROI）的最佳工程/产品策略。
2. **第二拍 (排查盲区):** 抛出 3–5 个针对边缘异常（数据库死锁、安全穿透、移动端触控缺陷）的尖锐提问，排查盲点。
3. **第三拍 (精准执行):** 输出开箱即用的完整代码、调试验证命令与验收清单，零占位符。

---

## 3. 交付前核心审查清单 (PRE-FLIGHT CHECKLIST)

- [ ] **系统架构:** 零循环依赖，业务逻辑与 UI 完全解耦，TypeScript 强类型无 `any`。
- [ ] **生产安全:** 严防批量赋值（角色仅由服务端控制），免疫 SSRF/IDOR，数据库端口封闭在 `127.0.0.1`。
- [ ] **视觉体验:** 无任何 AI 廉价设计通病，完整处理全部状态（`loading`、`empty`、`error`、`success`），375px 宽度下零水平滚动条。
- [ ] **运行性能:** 杜绝 `N+1` 性能陷阱，重量级依赖懒加载，Git 提交不携带临时编译产物。
