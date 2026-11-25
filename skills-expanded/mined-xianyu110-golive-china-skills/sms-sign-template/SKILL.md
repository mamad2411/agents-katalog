---
name: sms-sign-template
description: "国内短信签名与模板审核：资质 → 签名 → 模板 → 运营商实名报备的顺序、签名来源只认企事业单位名/已注册商标名、验证码/通知/推广模板写法、商业短信需用户同意与退订（2026-05-01 施行的新《通信短信息服务管理规定》）、发送频控与防刷。Use when adding SMS login/verification/notifications for China users, when a 短信签名 or 模板 is rejected, when messages fail to deliver, or when the user mentions 阿里云短信 / 腾讯云短信 / 签名报备 / 验证码短信."
---

# 短信签名与模板审核 · SMS Signature & Template Review

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** China SMS goes qualification → signature → template → carrier real-name registration. Carriers now essentially accept only *company name* or *registered trademark* as signature sources (personal accounts can't self-use). Verification templates must contain "验证码" and no links/marketing; marketing SMS need recipient consent and an opt-out. The agent writes compliant templates, rate limiting and anti-abuse; the human handles qualifications.

## 关键规则（已核对）

- **签名来源**（阿里云口径）：签名需为**企事业单位名**（全称或规范简称；简称须为营业执照全称的连续子集且包含地域信息）或**已注册商标名**；不支持含义模糊的中性签名、个人姓名、"测试"字样；长度 2–18 字符；以"已上线 App（含软著）"为来源的签名运营商已明确不再支持；公众号/小程序、店铺名、已备案网站等来源面临较大发送失败风险。个人认证账号"自用"签名无法通过实名制报备。[^ali-sign]
- **时效**（阿里云口径，未承诺）：签名审核预计 2 小时内（工作时间）；运营商实名报备平均 5–7 个工作日，部分 7–10 个工作日或更长。[^ali-sign]
- **腾讯云**规则相近，变量格式为 `{1}`、`{2}`，以其签名/模板审核标准为准。[^tx-sign][^tx-tpl]
- **商业性短信**：新版《通信短信息服务管理规定》（工信部令第 74 号，2026-05-01 施行）第二十一至二十三条——传输商业性短信须由发送方提供接收方同意或请求接收的承诺或证明材料；须提供便捷有效的拒绝接收方式并随短信告知；接收方明确拒绝后不得再次传输。[^reg74]

## 前置条件

- [ ] 企业实名的云账号（个人账号基本无法申请可用签名）
- [ ] 资质：营业执照、法人与经办人信息；签名涉及第三方时准备委托授权书
- [ ] 签名名称：公司规范简称（含地域）或已注册商标
- [ ] 业务场景截图（登录页、通知场景）

## 步骤

1. **资质申请（human）**：在短信控制台提交企业资质。
2. **签名（agent 建议名称，human 提交）**：agent 根据营业执照全称生成合规简称候选（例：`杭州某某网络科技有限公司` → `杭州某某网络科技`），检查长度与连续性。
3. **模板（agent 起草）**：

| 类型 | 示例（仅示意） | 要点 |
|---|---|---|
| 验证码 | `您的验证码为${code}，5分钟内有效，请勿泄露给他人。` | 含"验证码"；不含链接、营销、联系方式 |
| 通知 | `您的订单${order}已发货，可在App内查看物流。` | 变量含义清晰，不夹带营销 |
| 推广 | `…活动内容…拒收请回复R` | 仅企业可申请；须有退订方式；须取得用户同意 |

4. **等待运营商报备完成（human 跟进）**：报备未完成可能被拦截。
5. **工程防护（agent）**：
   - 图形/滑块验证码 + 同号码 60 秒冷却 + 同 IP/设备日上限；
   - 后端校验验证码（有效期、一次性、错误次数上限）；
   - 发送失败回执落库，监控成功率；
   - 营销短信：记录用户同意的时间与方式、退订即时生效。

## 检查清单

- [ ] 签名来源为企事业单位名或已注册商标名，报备状态为成功
- [ ] 验证码模板不含链接与营销
- [ ] 推广短信有同意证明与"拒收请回复R"类退订方式
- [ ] 频控、防刷、验证码一次性校验
- [ ] 隐私政策写明手机号用途（`pipl-privacy-policy`）

## 常见驳回原因与修复

| 原因 | 修复 |
|---|---|
| 中性签名（"服务通知""温馨提示"） | 改为公司规范简称或商标[^ali-sign] |
| 简称缺地域/跳字/过短 | 从营业执照全称连续截取并含地域[^ali-sign] |
| 个人账号申请自用签名 | 升级企业认证或申请他用（需企业授权）[^ali-sign] |
| 签名来源为 App/小程序/网站 | 改用企事业单位名或商标[^ali-sign] |
| 验证码模板含链接或营销内容 | 拆分为纯验证码模板 |
| 推广短信无退订方式 | 末尾加退订提示[^reg74] |
| 签名"可用-异常"、发送失败 | 查看运营商报备结果，按提示重新报备[^ali-sign] |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 生成签名候选、模板文案、自检规范 | 企业资质提交、委托授权书 |
| 接入 SDK、频控、防刷、回执监控 | 提交签名与模板、跟进报备 |
| 营销同意与退订的数据结构 | 对营销短信合法性负责 |

## 官方来源

[^ali-sign]: 阿里云 短信签名规范 https://help.aliyun.com/zh/sms/user-guide/signature-specifications-1 ；模板规范 https://help.aliyun.com/zh/sms/user-guide/message-template-specifications/
[^tx-sign]: 腾讯云 短信签名审核标准 https://cloud.tencent.com/document/product/382/39022
[^tx-tpl]: 腾讯云 正文模板审核标准 https://cloud.tencent.com/document/product/382/39023
[^reg74]: 《通信短信息服务管理规定》（工信部令第 74 号，2026-05-01 施行） https://www.gov.cn/gongbao/2026/issue_12766/202605/content_7070600.html

> ⚠️ 免责声明：本文不是法律意见；签名与模板规范由运营商与平台随时调整，以控制台审核结果为准。
