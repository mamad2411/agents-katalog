---
name: golive-china-checklist
description: "上线前总检查清单与总调度：按『探测 → 计划 → 人工确认 → 执行 → 验证』把产品在中国大陆上线的所有事项串起来（域名、ICP 备案、公安备案、部署与 CDN、支付、小程序/App、隐私政策、短信、生成式 AI 备案/登记、大模型选型），区分 agent 可自动完成与必须由人完成的步骤，并附只读体检脚本。Use when the user says 'launch in China', '国内上线', '上线前检查', 'go live in mainland China', or wants a single plan covering all compliance and deployment steps."
---

# 上线前总检查清单 · China Go-Live Master Checklist

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** The orchestrator. It runs a detect → plan → approve → apply → verify loop across the other 12 skills, produces one ordered launch plan with owners (Agent vs Human) and dependencies, and ships a read-only `scripts/golive_check.py` that verifies HTTPS, ICP/public-security filing numbers in the footer, privacy/terms links, foreign dependencies and AI labelling on a live URL. It never submits forms on the user's behalf.

## 工作方式（agent 必须遵守）

1. **Detect 探测**：读仓库与部署配置，回答：产品形态（网站/H5/小程序/App）、服务器与 CDN 在哪、是否收款、是否发短信、是否收集个人信息、是否有 AI 生成功能、是否有 UGC。
2. **Plan 计划**：输出一张带依赖关系的计划表（见下），每行标 Owner = Agent / Human / Both，未确定的标 ❓。
3. **Approve 确认**：把所有 Human 步骤与需要付费/实名/签约/提交的步骤列给用户确认。**agent 不代替用户实名、签约、提交政府或平台表单，不保管用户密钥。**
4. **Apply 执行**：agent 只执行代码、配置、文档类工作（PR 形式）。
5. **Verify 验证**：运行 `scripts/golive_check.py` + 下面的人工清单；未通过项回到对应 skill。

## 依赖顺序（关键路径）

```text
主体确定（个人/个体户/公司）
  └─ 域名购买+实名 ──┐                    domain-realname-dns
内地服务器（可备案）─┴─ ICP 备案 ── 公安备案（30 日内）   icp-beian → gongan-beian
                          ├─ CDN（内地加速）               china-cloud-cdn-deploy
                          ├─ 微信支付 / 支付宝（网站需备案） wechat-pay / alipay
                          └─ 小程序备案+审核 / App 备案+软著+上架   wechat-miniprogram-launch / app-store-ruanzhu
隐私政策 + 用户协议（所有上架/支付前）                     pipl-privacy-policy
短信：企业资质 → 签名 → 模板 → 运营商报备                  sms-sign-template
AI：模型选型 → 登记/备案 → 标识 + 公示                     llm-api-in-china → genai-algorithm-filing
```

⚠️ 主体一致性是最常见的坑：**域名实名主体 = ICP 备案主体 = 支付商户主体 = 小程序/App 主体 = 短信签名资质主体**。个人主体会在支付、小程序支付、短信签名等环节受限。

## 总清单

### A. 主体与域名
- [ ] 确定主体；需要收款/短信/小程序支付的，评估是否注册个体工商户或公司（`wechat-pay`、`sms-sign-template`）
- [ ] 域名后缀与注册商可备案，实名主体一致（`domain-realname-dns`）

### B. 备案
- [ ] 服务器满足可备案条件（`china-cloud-cdn-deploy`）
- [ ] ICP 备案通过，footer 展示备案号并链接 beian.miit.gov.cn（`icp-beian`）
- [ ] 公安联网备案已提交/通过，footer 展示公网安备号（`gongan-beian`）
- [ ] 经营性业务是否需要 ICP 许可证 / 前置审批 —— 已咨询 ❓（`icp-beian`）

### C. 部署
- [ ] 无境外关键依赖（字体、CDN、统计、验证码、境外 OAuth、境外模型 API）
- [ ] HTTPS、证书自动续期、安全组最小化、备份与监控
- [ ] CDN 仅在备案后添加（`china-cloud-cdn-deploy`）

### D. 收款
- [ ] 商户号/支付宝签约完成，网站内容完整（商品、价格、售后、联系方式）
- [ ] 回调验签、幂等、查单、对账、退款已测试（`wechat-pay`、`alipay`）

### E. 渠道
- [ ] 小程序：备案、隐私保护指引、提审自查（`wechat-miniprogram-launch`）
- [ ] App：App 备案、软著/电子版权、商店资质、iOS ICP 号（`app-store-ruanzhu`）

### F. 个人信息
- [ ] 隐私政策 + 用户协议，与代码实际行为一致；首次同意弹窗；注销功能（`pipl-privacy-policy`）
- [ ] 数据存储位置与出境评估

### G. 短信
- [ ] 签名为企业名/商标且报备成功；模板合规；防刷（`sms-sign-template`）

### H. 生成式 AI（如有）
- [ ] 生产只用已备案模型；登记/备案路径已与属地网信办确认（`llm-api-in-china`、`genai-algorithm-filing`）
- [ ] 显式 + 隐式标识；产品页公示模型名称与备案号/上线编号
- [ ] 内容审核、投诉举报、日志留存

### I. 上线当天
- [ ] `python3 scripts/golive_check.py https://你的域名 [--ai]` 全部 ✅ 或已解释的 ⚠️
- [ ] 真实小额支付 + 退款走通
- [ ] 内地多地区拨测首屏
- [ ] 客服与投诉渠道可用

## 体检脚本

```bash
python3 skills/golive-china-checklist/scripts/golive_check.py https://www.example.com --ai
python3 skills/golive-china-checklist/scripts/golive_check.py https://www.example.com --json > golive-report.json
```

只读、仅标准库；检查 HTTPS 与证书、ICP 备案号及 beian.miit.gov.cn 链接、公网安备号、隐私政策/用户协议入口、境外资源、AI 标识与模型公示关键词。退出码非 0 表示存在 ❌。**脚本结果不代表合规结论。**

## 常见"上线被卡"原因

| 卡点 | 去哪个 skill |
|---|---|
| 备案主体与域名/支付主体不一致 | `domain-realname-dns`、`icp-beian` |
| 个人主体无法开通支付/小程序支付/短信签名 | `wechat-pay`、`sms-sign-template` |
| CDN 加不上域名 | `china-cloud-cdn-deploy` |
| 支付签约"网站无法访问/信息不完整" | `wechat-pay`、`alipay` |
| 小程序隐私指引不一致被拒 | `wechat-miniprogram-launch` |
| 商店要求软著 | `app-store-ruanzhu` |
| AI 产品被要求提供备案/登记信息 | `genai-algorithm-filing` |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 探测、出计划、跑体检脚本、写代码与文档 PR | 选主体、付款、实名、人脸核验、接电话、短信核验 |
| 生成材料清单与文案草稿 | 提交所有政府与平台表单、签约 |
| 每次发布前回归检查 | 律师审阅、与监管沟通、承担主体责任 |

## 官方来源（总表）

- 工信部备案管理系统 https://beian.miit.gov.cn/
- 全国互联网安全管理服务平台 https://beian.mps.gov.cn/
- 《互联网信息服务管理办法》 https://www.gov.cn/gongbao/content/2000/content_60531.htm
- 微信支付商户平台 https://pay.weixin.qq.com/ ；支付宝开放平台 https://open.alipay.com/
- 微信小程序平台常见拒绝情形 https://developers.weixin.qq.com/miniprogram/product/reject.html
- 《个人信息保护法》 http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html
- 《生成式人工智能服务管理暂行办法》 https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm
- 各子 skill 中列出的具体条款与平台文档

> ⚠️ 免责声明：本清单是开发者经验与公开官方资料的整理，不构成法律意见；政策与平台规则随时变化，以官方最新要求为准。
