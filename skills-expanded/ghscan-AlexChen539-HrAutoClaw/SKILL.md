---
name: "email-notification-skill"
description: "Action Agent技能：候选人状态变更邮件通知模板与SMTP配置"
---

# Email Notification Skill

## 概述
Action Agent 负责检测候选人状态变更，并根据变更类型发送标准化邮件通知。
本技能定义了邮件内容模板、SMTP 配置读取方式和通知去重逻辑。

## 邮件配置
- 邮箱地址: 614550317@qq.com
- SMTP 服务器: smtp.qq.com (SSL)
- SMTP 端口: 465
- 授权码: 存储在 email_config.json 或环境变量中
- 找不到授权码时使用 dry-run 模式，只写日志不发送

### 配置读取优先级
1. `data/openclaw/email_config.json` — 结构化配置文件
2. 环境变量 `QQ_SMTP_AUTH_CODE` — 环境变量
3. 上述都不存在 → dry-run 模式，日志记录

`email_config.json` 格式:
```json
{
  "smtp_host": "smtp.qq.com",
  "smtp_port": 465,
  "use_ssl": true,
  "sender_email": "614550317@qq.com",
  "auth_code": "<SMTP授权码>",
  "notify_emails": ["614550317@qq.com"]
}
```

## 邮件模板

### 1. Offer 通知 — 通过面试
**主题**: 🎉 [Testin] 恭喜通过面试 — {姓名}

**正文**:
```
尊敬的 {姓名} 同学/先生/女士：

恭喜您通过 Testin 的{应聘岗位}面试！

经过综合评估，我们很高兴通知您已成功通过所有面试环节。
HR 同事将在近期与您沟通 Offer 详细事宜（薪资、入职时间等）。

如有任何疑问，请随时与我们联系。

Testin 招聘团队
{当前日期}
```

发送条件: 候选人最新状态为 `offer`

### 2. 淘汰通知 — 未通过
**主题**: 💌 [Testin] 面试结果通知 — {姓名}

**正文**:
```
尊敬的 {姓名} 同学/先生/女士：

感谢您参加 Testin 的{应聘岗位}面试。

经过认真评估，我们认为您与该岗位的匹配度暂未达到要求，
本次未能进入下一轮。

您的简历已存入我们的人才库，如有合适的岗位机会，
我们会第一时间与您联系。

再次感谢您的参与，祝您职业发展顺利！

Testin 招聘团队
{当前日期}
```

发送条件: 候选人最新状态为 `rejected`

### 3. 待定通知 — 流程中
**主题**: ⏳ [Testin] 面试进度通知 — {姓名}

**正文**:
```
尊敬的 {姓名} 同学/先生/女士：

感谢您参加 Testin 的{应聘岗位}面试。

您的面试结果目前仍在综合评估中，我们会在
3-5 个工作日内给您最终反馈。

请您耐心等候，感谢您的理解与支持。

Testin 招聘团队
{当前日期}
```

发送条件: 候选人最新状态为 `pending`（可选发送）

## 通知去重逻辑
- 读取 `data/openclaw/runtime/notified_candidates.json`
- 记录格式: `{ "candidate_key": "CAND-0001", "state": "offer", "notified_at": "2026-06-06T09:30:00" }`
- 已通知过的候选人（同 candidate_key + 同 state）跳过
- 状态从 `screening` → `offer` 或 `screening` → `rejected` 才触发通知
- 通知完成后立即更新 notified_candidates.json

## 日志记录
- 每封邮件发送记录写入 `data/openclaw/email_logs/` 目录
- 文件名格式: `emails_YYYYMMDD.jsonl` (JSON Lines)
- 每条记录包含: 时间, 候选人, 类型, 是否发送成功, 错误信息
- dry-run 模式也在日志中标注 `"dry_run": true`

## 执行流程
1. 读取 `state.json` 获取最新候选人状态
2. 读取 `notified_candidates.json` 获取已通知记录
3. 对比找出 status 变更为 offer/rejected 且未通知的候选人
4. 按模板生成邮件内容
5. 尝试通过 SMTP 发送
6. 更新通知记录 + 写日志
