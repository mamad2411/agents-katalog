---
name: publicist-china-pipl
description: Apply China's PIPL rules to journalist data, WeChat IDs, email addresses, and cross-border transfers. Use when media-contact data leaves China or enters an overseas CRM or model.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# PIPL cross-border compliance, China market

**Scope**. Mandatory when journalist/contact data (personal information) crosses China border. Pair with `publicist-china` + platform skills + `publicist-china-ai-compliance`.

## Legal basis
- **《个人信息保护法》** (PIPL), 2021-11-01 生效
- **《个人信息出境标准合同办法》**, 2023-06 生效
- **《个人信息出境安全评估办法》**, 2022-09 生效
- **网信部门备案指南**, 2023-05 更新

## What constitutes personal information (PIPL Art.4)
在媒体关系场景下，以下均为个人信息：
- 记者/编辑/运营：姓名、手机、邮箱、微信号、头像、职业履历、过往署名、联系偏好
- 媒体账号：公众号认证主体、运营者实名、后台登录记录
- 互动记录：微信聊天、邮件往来、通话录音、会面笔记
- **关键判断**. "已识别或可识别的自然人相关信息", 单条不识别，组合可识别 = 个人信息

## Cross-border triggers (PIPL Art.38-40)
以下场景触发出境合规义务：
1. **境外 CRM** (Salesforce/HubSpot/Pipedrive/Notion/Airtable) 存储记者联系方式
2. **境外邮件平台** (Gmail/Outlook/ProtonMail) 收发记者邮件
3. **境外模型输入** (OpenAI/Claude/Gemini API) 分析记者画像/过往稿件
4. **境外云文档** (Google Docs/Notion/Confluence) 协作媒体名单
5. **境外监测工具** (Meltwater/Cision/Muck Rack) 存储中国记者数据
6. **团队协作** (Slack/Teams/Discord) 讨论中国媒体名单

## Three legal pathways (任选一)
| Pathway | 适用条件 | 核心要求 |
|---|---|---|
| **安全评估** | 关键信息基础设施运营者 / 100万+人信息 / 敏感个人信息 | 网信部门评估通过 |
| **专业机构认证** | 非关键基础设施、<100万、非敏感 | 专业机构(如北京中证天下/中认联科)认证 "符合标准合同" |
| **标准合同备案** | 最常用路径 | 签署《标准合同》+ 网信部门备案 (省级/国家级) |

## Standard contract filing flow (标准合同备案)
1. **数据出境影响评估 (DPIA)**, 内部自查：数据类型、目的、接收方、安全措施、风险
2. **签署标准合同**, 与境外接收方 (CRM/邮件/模型提供商) 签《个人信息出境标准合同》
3. **单独告知 + 单独同意**, 每位记者/联系人：**单独**告知出境目的/方式/接收方/保留期限/权利，**单独**获得明示同意
4. **网信部门备案**, 省级网信办 (非关键/非敏感) 或 国家网信办 (关键/敏感), 15个工作日审核
5. **持续合规**, 记录留存 ≥3年；变更重新评估/备案；数据主体权利响应机制

## Practical compliance for publicist workflow

### Scenario A: 记者名单存入境外 CRM
- ❌ 直接导入 → 违法
- ✅ 路径: DPIA → 标准合同 + 备案 → 单独告知每位记者 → 获得同意 → 导入
- **替代**. 用本地加密表格/本地数据库 (不出境) → 无合规负担

### Scenario B: 记者过往稿件喂给境外 LLM 分析
- ❌ 直接粘贴到 ChatGPT/Claude → 违法 (稿件含姓名/单位/联系方式 = 个人信息)
- ✅ 路径: 脱敏处理 (姓名→代号、单位→行业、邮箱/微信→哈希) → 仅输入脱敏文本
- **替代**. 用本地模型 (llama.cpp/Qwen) 离线分析 → 无出境

### Scenario C: Meltwater/Cision 等境外监测平台
- 这些平台通常已完成标准合同备案或认证, **但需核实当前状态**
- 使用前：确认提供商《标准合同》版本、备案编号、数据处理附录 (DPA)
- 记录：`provider=Meltwater, cross_border_path=标准合同备案, filing_date=2024-xx, records_retention=3y`

### Scenario D: 团队 Slack/Notion 讨论中国媒体名单
- ❌ 直接粘贴明文名单 → 违法
- ✅ 路径: 仅分享脱敏索引 (ID+行业+地域)；明文名单留本地加密存储
- **替代**. 飞书/钉钉/企业微信 (国内合规协作工具)

## Minimal compliance checklist (per project)
- [ ] **数据映射**. 列出所有记者/联系人字段、存储位置、处理目的、跨境去向
- [ ] **路径选择**. 安全评估 / 认证 / 标准合同备案, 选一条
- [ ] **单独告知**. 每位数据主体收到独立告知 (目的/方式/接收方/期限/权利)
- [ ] **单独同意**. 明示同意记录 (签名/勾选/录音/邮件回复), 留存
- [ ] **备案完成**. 网信部门受理/通过证明, 留存
- [ ] **合同/DPA**. 与境外接收方签署最新版标准合同 + DPA, 留存
- [ ] **权利响应**. 15个工作日内响应查阅/更正/删除/撤回同意请求
- [ ] **记录留存**. 所有上述文档 ≥3年

## Negative patterns (避坑)
- ❌ "我们公司有隐私政策" ≠ 单独告知+单独同意
- ❌ "CRM供应商说合规" ≠ 你完成备案
- ❌ "只是临时分析" ≠ 豁免 (处理即触发)
- ❌ "数据量很小" ≠ 豁免 (无最低量豁免)
- ❌ 批量导入联系人 → 无单独同意记录
- ❌ 微信号/邮箱哈希后仍可反查 → 仍属个人信息

## Emergency simplification (ponytail: 本地化优先)
> **最省力合规路径**. 所有中国记者/联系人数据 **不出境**，用本地加密文件/本地数据库/飞书/钉钉/企业微信。仅在必须用境外工具时，走标准合同备案。

## References
- `http://www.gov.cn/gongbao/content/2023/content_5752224.htm`, 标准合同办法
- `https://www.cac.gov.cn/2023-05/30/c_1687090906222927.htm`, 备案指南
- `skills/publicist-china/references/law-and-ethics.md`
- `skills/publicist-china/references/sources.md` (CAC/网信办链接)
- 普华永道/金诚同达 PIPL 合规实务解析

## What this skill does not do
- ❌ No legal advice (escalate to China-qualified counsel)
- ❌ No automated filing tool
- ❌ No MCP/CLI tools (reference only)
