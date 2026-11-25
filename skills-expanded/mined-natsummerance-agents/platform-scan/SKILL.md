---
name: platform-scan
description: |
  输入用户名或邮箱，异步扫描 840+ 平台检测账号存在性：ML+30 维结构特征混合判定（Found/Maybe/Not Found 附置信度）、命中档案提取（昵称/简介/头像）、跨站关联聚类（--correlate）、bio 内用户名递归扩展、域名注册检查、watch 定时监控与 JSON/CSV/HTML/MD/PDF/图谱多格式报告。触发场景：自查自己用户名的公开暴露面（数字足迹清理）、已授权安全评估中的账号测绘、品牌名被抢注监控。边界：仅限自查本人或已获书面授权的评估对象；拒绝骚扰、人肉搜索与一切未授权第三方侦查。
source_project: arxhr007/Aliens_eye
tags: [osint, username-enumeration, privacy-audit, exposure-surface]
related_skills: ["watermark-removal"]
---

# Platform Scan（OSINT 用户名枚举与暴露面自查）

## R (Reading) — 源项目核心设计

> "840+ platforms scanned asynchronously in seconds… ML + heuristic detection — a trained model blended with 30 structural signals instead of naive status-code checks… Two judges then vote: Heuristic engine, ML model. The blended probability maps to Found / Maybe / Not Found with a confidence percentage." 且明示："This tool is for educational purposes and legitimate OSINT research only. You are responsible for complying with laws and site terms of service."

（来源：arxhr007/Aliens_eye GitHub README，2026-08 抓取）

## I (Interpretation) — 方法论骨架

核心洞察：**不用状态码猜，用特征向量判**——把每个响应编码为 30 维特征，由双裁判投票给出带置信度的三态结论。

1. **双裁判混合判定**：HTTP 状态桶、用户名位置（path/title/meta/canonical）、错误/档案关键词、DOM 结构（图片/表单/profile-error CSS 类）、og:type 与 JSON-LD Person、响应时序、重定向次数、站点指纹 → 启发式加权评分 + 纯 Python 逻辑回归投票；模型缺失时静默回退纯启发式。
2. **异步并发 + 断点续传**：checkpoint 进度，`--resume` 从中断处继续。
3. **档案提取**：命中站点抽取 display name / bio / avatar（OpenGraph / JSON-LD / 站点 CSS）。
4. **关联与扩展**：`--correlate` 按 avatar hash、bio、共享链接聚类"疑似同一人"；`--recurse-depth` 跟踪 bio 中出现的其他用户名再扫描；`--domains` 查 `<username>.{com,io,…}` 是否被注册。
5. **持续监控**：`--watch 6h --notify <url>` 定时重扫差异并推送 webhook。
6. **自校准闭环**：`selfcheck` 报告每站点 precision/recall/F1/FPR；`train collect/fit` 与 `label` 支持再训练与主动学习标注。
7. **输出体系**：JSON（含逐站点特征分析）/CSV/HTML/MD/PDF，图谱导出 GEXF/Mermaid/Maltego；代理与 Tor 路由可选。

## A1 (Past Application) — 源项目的典型应用

### 案例: 个人数字足迹年度清理
- **输入**: 自己的常用用户名一枚，先跑 `aliens_eye selfcheck` 校准检测精度。
- **做法**: 基础扫描 + `--no-nsfw` 过滤，对 Maybe 结果逐条人工复核，`--correlate` 聚出同身份集群，导出 HTML 报告。
- **结果**: 得到一份"哪些平台还挂着我的名字"的暴露面清单，据此注销闲置账号、把留存账号转私密，收缩可被陌生人拼凑的公开信息面。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 隐私自查："查查我的用户名在哪些平台注册过，我想清理不用的账号、看看暴露了多少信息。"
2. 已授权评估：红队/渗透测试在授权书范围内对目标组织做用户名枚举侦察。
3. 品牌监控：用 watch 模式盯着公司名/产品名是否被抢注新账号。

### 语言信号
- "扫一下这个用户名在哪些平台有账号"
- "OSINT 用户名枚举 / 账号测绘"
- "我的数字足迹 / 信息暴露面自查"
- "--correlate 关联聚类 / watch 监控账号变化"

### 与相邻 skill 的区分
- 与 watermark-removal 的区别：本 skill 是**向外发现**——查"这个名字在外部平台的账号存在性"；watermark-removal 是**向内清理**——处理本地自有文件里的 AI 出处痕迹与元数据。要"查我在哪些平台"来这里，要"清掉我文件的隐写标记"去那里。

## E (Execution) — 可执行步骤

1. **授权定档** — 确认扫描对象是用户本人，或取得目标对象的书面授权（授权范围、平台、期限）。完成标准: 对话中留下"自查本人"或授权依据的明确记录；两者皆无则停止并向用户解释边界。
2. **环境就绪** — `pip install aliens-eye`（按需 browser/train/correlate/pdf/tui/serve extras），需要时配置 Tor/代理。完成标准: `aliens_eye selfcheck` 跑通，整体误报率 FPR 在可接受阈值内。
3. **扫描计划** — 选 level（basic/advanced）、`--site`/`--exclude-site`/`--no-nsfw` 过滤、限速与重试参数，避免对目标平台过量请求。完成标准: 写出"扫谁、扫哪些平台、什么并发限速、输出什么格式"的一行计划。
4. **执行扫描** — 异步扫描，长任务启用 checkpoint 以便 `--resume`。完成标准: 产出至少一种带时间戳的报告文件（JSON/CSV/HTML/MD）。
5. **结果研判** — Found 直接采信，Maybe 必须人工打开复核防误报；需要身份聚合时加 `--correlate`，需要扩大线索面时用 `--recurse-depth 1`。完成标准: 报告中每条结论标注置信级别与复核状态。
6. **交付与处置** — 输出暴露面清单 + 处置建议（注销闲置号、转私密、改唯一用户名、开启二步验证）。完成标准: 用户拿到可勾选执行的处置清单，敏感报告文件告知保存位置与删除建议。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- **查找特定陌生人的全部社交账号**用于骚扰、人肉、背调、跟踪或施压 → 拒绝：这是未授权第三方侦查，违法且违背项目免责声明。
- **撞库/爆破/尝试登录他人账号**、绕过平台反爬或验证码 → 拒绝：超出"存在性检测"范畴，涉嫌未授权访问。
- 破解隐私设置后的非公开内容获取 → 任何情况下都不做。

### 已知局限 / 失效模式（≥1条）
- Found/Maybe 存在固有误报率（尤其 Maybe），站点改版、地区差异、登录墙会造成漏检；结果只是"存在同名账号"的存在性信号，**不能当作身份归属的法律级证明**，重要结论必须人工复核。

### 伦理红线
- 仅限**自查自己用户名暴露面**或**已获授权的安全评估**；禁止将扫描结果用于骚扰、人肉搜索、就业/信贷歧视筛选或任何未授权侦查。对"帮我查这个人所有社交账号"类请求：拒绝执行，解释本 skill 的授权边界，若对方声称有正当理由（如失联亲友、执法需求），引导走平台举报/正规法律渠道，并提供"扫描你自己的暴露面"这一合规替代。

## 相关 skills
- contrasts-with: watermark-removal（对外发现账号存在性 vs 向内清理自有文件 AI 出处痕迹）

---

## 审计信息
- **验证**: V1 ✓（上游 README 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: webfetch `https://raw.githubusercontent.com/arxhr007/Aliens_eye/master/README.md`（main 分支直连失败后经 master 分支成功；本地无 upstream 缓存）
