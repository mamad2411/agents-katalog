---
name: kb-gray-market
description: CVE/PoC 知识库 · 博彩包网 / 黑灰产站点面（29 条）：源码与备份泄露、前端签名可逆、接口越权(BOLA)、后台管理 API 未授权、代登录越权、代理层级越权、会员隐私枚举、Mass Assignment、支付回调伪造、提现审核越权、余额并发与负数、下注赔率篡改、彩金幂等缺失、三方游戏回调伪造、开奖算法可预测、客服 IM/WS 未鉴权、存储型 XSS 打后台、短信验证码回显/复用/爆破、密码重置 token 越权、上传 getshell、短信轰炸、报表接口未授权、若依后台、Actuator、JWT、公开 OSS 桶、导出任意读、业务 SQLi、SSRF。每条都有可直接执行的请求与判定标准；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（业务逻辑 / 实现缺陷类，无 CVE；出处见各条「参考」）
---

# 博彩 / 黑灰产站点面（59 条）
> 条目为公开资料整理（出处见各条「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

这类目标（博彩包网、代理后台、跑分/代付、发卡、接码）共同点：**成套买同一套系统换皮上线**，所以指纹一致、缺陷一致；很少靠"新 CVE"，几乎全是：

1. 部署残留（备份、`.git`、`.env`、sourcemap、swagger、Druid、Actuator）；
2. 权限只写在前端（接口越权读他人订单/流水/提现/会员资料）；
3. 资金面逻辑不严（回调不验签、金额取自信使请求、状态机可重放、并发、幂等缺失、开奖可预测）；
4. 前端即信任边界（签名算法与密钥在 JS 里、供应商 key 打进 H5 包）；
5. 上传与验证码（头像/KYC getshell、短信轰炸、账号枚举）。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `admin-api-unauthenticated.md` | 后台管理 API 未授权（只在前端隐藏菜单） | critical | 普通 token 直接打 /api/admin/* |
| `admin-ip-whitelist-bypass.md` | 后台 IP 白名单绕过（X-Forwarded-For 伪造内网来源） | high | 403 页面 + 只允许 127.0.0.1/内网段 |
| `admin-reset-any-user.md` | 后台“重置任意用户密码”接口越权（直接接管会员/管理员） | critical | /api/admin/user/resetPassword  /api/agent/resetPwd |
| `agent-hierarchy-privilege.md` | 代理层级越权（读全站下级 / 改佣金比例） | critical | 改 agentId 读他人下级，改 rate 提佣金 |
| `api-idor-bola.md` | 接口越权 / BOLA（读他人订单、流水、提现） | high | - |
| `api-replay-nonce-missing.md` | 接口无 nonce / 时间戳 → 请求重放（充值、领奖、下注） | high | 充值/领奖/下注接口缺 nonce 校验 |
| `bet-history-idor.md` | 注单 / 流水接口越权批量拉取（全站会员数据） | high | /api/bet/list?uid=  /api/report/bet |
| `bet-odds-tampering.md` | 下注/结算赔率与倍数篡改（资金面） | critical | 下注体里改 odds/multiple |
| `callback-url-ssrf.md` | 支付 / 回调地址可控 → 内网 SSRF（含云元数据） | high | 支付配置/回调 URL/代理推广链接检测 |
| `client-side-signature-forgery.md` | 前端签名 / 加密可逆（伪造请求绕过风控） | high | app.js 里抄出算法与 key，重算 sign |
| `cors-misconfig-credential.md` | CORS 配置错误（带凭据读他人接口数据） | high | 反射 Origin 且 Allow-Credentials: true |
| `coupon-code-enumeration.md` | 券码 / 彩金码可枚举（批量领取与套现） | high | /api/coupon/redeem  /api/promo/exchange |
| `cs-chat-export-unauth.md` | 客服聊天记录导出未鉴权（全站会话与身份材料） | high | /api/cs/history/export  /api/im/sessions |
| `csrf-transfer.md` | CSRF（无 token 的提现/改密/绑卡） | high | 关键操作缺 CSRF token 且 SameSite 未设 |
| `daily-reward-farming.md` | 签到 / 任务奖励批量刷取（缺幂等与频率控制） | high | /api/activity/sign、/api/task/claim |
| `db-admin-tool-exposed.md` | phpMyAdmin / Adminer 暴露（弱口令直进数据库） | critical | /phpmyadmin/  /pma/  /adminer.php |
| `druid-monitor-unauth.md` | Druid 监控未授权 → session 泄露/后台接管（若依系必备） | critical | /druid/index.html  /druid/websession.html |
| `export-file-read.md` | 导出 / 下载接口任意文件读取 | high | /api/report/export?file=../../../../etc/passwd |
| `finance-export-pii.md` | 财务导出接口越权（银行卡 + 身份证批量导出） | critical | /api/finance/export  /api/withdraw/export |
| `game-vendor-api-forgery.md` | 三方游戏 / 视讯接口 key 泄露与回调伪造 | critical | 前端拿 vendor key，伪造 /api/game/callback 上分 |
| `host-header-poisoning.md` | Host 头投毒（密码重置链接被劫持 → 任意账号接管） | critical | POST /api/user/findpwd 的 Host / X-Forwarded-Host |
| `impersonate-switch-user.md` | 后台"切换用户/代登录"接口越权（任意账号接管） | critical | /api/admin/user/loginAs?uid=1 |
| `im-websocket-unauth.md` | 客服 IM / WebSocket 未鉴权（订阅他人会话） | high | ws://host/ws 无 token 直接订阅 room |
| `invite-referral-selfdealing.md` | 邀请返水自邀循环（小号矩阵刷返水） | high | /api/user/invite 或注册时的 inviteCode |
| `jwt-none-and-weak-key.md` | JWT 实现缺陷（alg:none / 弱密钥 / 可预测 / kid 注入） | high | - |
| `lottery-prng-predictable.md` | 开奖结果可预测（弱 PRNG / 客户端算法 / 固定种子） | critical | 历史期号统计 + 前端 JS 算法复现 |
| `mass-assignment-role.md` | Mass Assignment（注册/资料接口注入 role / vip / balance / agentId） | high | 注册体里多带一个 role=admin |
| `member-data-enumeration.md` | 会员隐私批量查询 / 账号枚举（手机号、银行卡） | high | /api/member/info?phone= 逐个返回他人资料 |
| `multi-tenant-cross-site.md` | 包网多租户越权（tenantId/siteId 遍历，横穿几十个站点） | critical | 请求体或 Header 里的 tenantId / siteId / merchantId |
| `notification-template-ssti.md` | 通知模板注入（标题/正文模板未转义 → SSTI / 存储型 XSS） | critical | 后台模板编辑 / 会员自定义通知标题 |
| `oauth-redirect-uri.md` | OAuth redirect_uri 劫持 / state 缺失（账号接管） | high | /oauth/authorize?redirect_uri= 可篡改 |
| `object-storage-datastore-exposure.md` | 对象存储与数据存储裸露（OSS / S3 / MinIO / MySQL / MongoDB） | high | - |
| `operator-backend-weak-login.md` | 运营后台弱口令 + 验证码复用（博彩站点最常见入口） | critical | /admin /manage /agent 的登录接口 |
| `order-status-tamper.md` | 订单状态机篡改（未支付改成已支付 / 已取消再入账） | critical | /api/order/status  /api/recharge/confirm |
| `origin-ip-leak-waf-bypass.md` | 源站 IP 泄露 → 绕过 WAF 直打（博彩站必看） | critical | 子域/邮件头/证书历史/SSRF 泄露的 origin |
| `panel-bt-1panel.md` | 宝塔 / 1Panel 面板弱口令与未授权（黑灰站最常见后台） | critical | :8888/<随机入口> 或 :8888/login |
| `password-reset-token-abuse.md` | 密码重置 token 可预测 / 未绑定用户（任意用户改密） | critical | token = md5(uid) / 响应回显 / 不校验 uid |
| `payment-channel-swap.md` | 支付通道 / 商户号篡改（充值进攻击者账户） | critical | /api/pay/create 的 channelId / merchantId / notifyUrl |
| `payment-notify-forgery.md` | 支付回调伪造与金额篡改（资金面） | critical | - |
| `promotion-abuse.md` | 活动 / 彩金 / 返水无限领取（幂等缺失） | high | /api/promotion/receive 重复或并发领取 |
| `race-condition-balance.md` | 余额并发与负数（竞态 / 金额符号） | critical | 同一请求并发 20 次 / amount=-100 |
| `redis-session-forgery.md` | Redis 未授权 → 偷后台 session / token 直接进后台 | critical | Redis 里的 login/session/token 键 |
| `repo-config-backup-leak.md` | 源码 / 备份 / 配置泄露 | high | - |
| `report-api-unauth.md` | 报表/财务接口未授权（全站流水与代理佣金） | high | /api/report/* 免认证或普通 token |
| `ruoyi-admin-unauth.md` | 若依（RuoYi）系后台默认口令 / Druid / 定时任务 RCE | critical | - |
| `scheduled-task-injection.md` | 后台定时任务 / 计划任务注入（Quartz、XXL-JOB、若依） | critical | 任务执行内容 / cron 表达式可写 |
| `sms-bomb-and-enum.md` | 短信轰炸与账号枚举（验证码面） | medium | - |
| `sms-code-reuse-and-bruteforce.md` | 短信验证码回显 / 复用 / 爆破（任意账号接管） | critical | 响应里带 code / 同码复用 / 4 位爆破 |
| `sourcemap-js-secret-leak.md` | sourcemap / 前端 JS 泄露接口与密钥（SPA 包网站第一入口） | high | /static/js/*.js.map 与打包进 bundle 的 AK/secret |
| `spring-actuator-exposure.md` | Spring Boot Actuator 未授权（heapdump / Jolokia / Gateway） | critical | - |
| `sql-injection-business-api.md` | 业务接口 SQL 注入（报表 / 订单 / 代理查询） | critical | orderNo=1' AND SLEEP(5)-- |
| `ssrf-to-internal.md` | SSRF（图片抓取 / 回调校验 / 推广链接检测）打内网与云元数据 | high | url=http://169.254.169.254/latest/meta-data/ |
| `stored-xss-to-admin.md` | 会员资料存储型 XSS 打后台审核（管理员会话劫持） | high | 昵称/备注/工单里插 <img onerror> |
| `support-ticket-attachment-idor.md` | 客服工单附件越权下载（证件照 / KYC 材料） | high | /api/support/attachment?fileId= |
| `swagger-knife4j-unauth.md` | Swagger / Knife4j 接口文档暴露 → 未授权接口直打 | high | /v2/api-docs  /doc.html  /swagger-ui/index.html |
| `upload-getshell.md` | 上传点 getshell（头像 / KYC 证件 / 客服附件） | critical | - |
| `vip-level-escalation.md` | VIP/等级接口参数篡改（免费拿高等级权益） | high | /api/user/level 或资料更新里的 vipLevel/levelId |
| `withdraw-approval-idor.md` | 提现审核接口越权（读他人银行卡 / 改审核状态） | critical | 两形态二选一（Query/JSON），抓包为准 |
| `withdraw-bankcard-swap.md` | 提现银行卡越权替换（把别人提现收进自己卡） | critical | /api/withdraw/apply 的 bankId / cardNo / memberId |

## 打法顺序（别从上传硬啃）

```
1. 源站定位（CDN 后面的真实 IP）              → kb-triage/fingerprint-workflow.md
2. 部署残留（.git / 备份 / .env / sourcemap） → 一步拿到全站逻辑与密钥
3. 前端签名与供应商 key（可逆 ⇒ 后面全部可伪造）→ client-side-signature-forgery / game-vendor-api-forgery
4. 接口越权（BOLA / 代理层级 / 会员隐私）      → api-idor-bola / agent-hierarchy-privilege / member-data-enumeration
5. 资金面（回调 / 提现审核 / 并发 / 彩金 / 开奖）→ payment-notify-forgery / withdraw-approval-idor / race-condition-balance / promotion-abuse / lottery-prng-predictable
6. 落地与提权（上传 / JWT / 后台残留）          → upload-getshell / jwt-none-and-weak-key / ruoyi-admin-unauth / spring-actuator-exposure
7. 数据面（公开桶 / 裸露 DB / 导出 / SQLi / SSRF）→ object-storage-datastore-exposure / export-file-read / sql-injection-business-api / ssrf-to-internal
```

## 硬规则

- 条目是**公开资料整理**，不是实测报告；`利用步骤` 属待验证假设，出报告前按目标版本自验并把 `verified` 置为 true。
- 资金面只用自己的账号与测试订单；越权只取 1-2 条记录做证据；报告里别贴会员库、证件、卡号。
- 这类站点普遍有设备指纹、IP 频控、日志留存差；枚举/爆破类动作先限速、选低峰窗口。并发测试是**一次性突发**（例如 20 并发打一次），不是持续压测。
- **资金面结论要分级写**：能改状态 ≠ 能出款。提现是否真正落地还取决于二级复核、出款风控、渠道对账——这部分语料未覆盖，报告里必须标"未验证"。
