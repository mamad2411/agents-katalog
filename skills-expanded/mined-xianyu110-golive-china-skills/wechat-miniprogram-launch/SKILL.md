---
name: wechat-miniprogram-launch
description: "微信小程序上线与审核：主体与类目选择、小程序备案（2023-09-01 起新小程序上架前必须备案）、用户隐私保护指引配置、提审前自查（对照《微信小程序平台常见拒绝情形》）、测试账号、AI/UGC 等特殊类目资质。Use when publishing a WeChat Mini Program, when a submission was rejected, or when the user mentions 小程序审核 / 小程序备案 / 隐私保护指引 / 类目 / 提审."
---

# 微信小程序上线审核 · WeChat Mini Program Launch & Review

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** Get a Mini Program from "code done" to "published": choose subject & category, complete the mandatory Mini Program filing (required before listing for new apps since 2023-09-01), configure the user-privacy guideline to match the APIs you actually call, pre-check against WeChat's official common-rejection list, provide a test account, and resubmit fast when rejected.

## 关键规则（已核对）

- **小程序备案**：2023 年 9 月 1 日起，新的微信小程序须先完成备案方可上架；流程为填写备案信息 → 平台初审 → 工信部短信核验 → 通信管理局审核。[^record][^record-notice]
- **用户隐私保护指引**：涉及处理用户个人信息的接口须在后台"用户隐私保护指引"中如实声明用途，审核会核验声明与代码实际收集行为是否一致。[^privacy]
- **常见拒绝情形**以官方文档为准：[^reject] 下表为摘录，非全部。
- 个人主体小程序不能开通普通微信支付（见 `wechat-pay`）。[^mp-pay]

## 前置条件

- [ ] 主体决定能力范围：个人主体可开放的类目与能力有限（支付、部分类目需企业/个体）
- [ ] 服务类目：按实际业务选择，并准备类目要求的资质（如需要）
- [ ] 小程序备案材料（与 ICP 备案相似：主体证件、负责人身份证、手机号）
- [ ] 服务器域名已在后台配置（request 合法域名需 HTTPS，且通常要求域名已备案——以后台提示为准）
- [ ] 如有账号体系：一个可体验全部功能的测试账号

## 步骤

1. **类目映射（agent）**：读取产品功能，列出每个功能对应的类目和是否需要资质；涉及 AI 生成内容、UGC、直播、医疗、金融、教育等的单独标红，让 human 去后台确认当前要求。
2. **小程序备案（human 提交，agent 起草）**：后台首页"去备案"；agent 起草小程序名称/简介一致性检查。[^record]
3. **隐私保护指引（agent 生成，human 粘贴）**：扫描代码中的 `wx.getLocation`、`wx.chooseImage/chooseMedia`、`getPhoneNumber`、剪贴板、蓝牙、通讯录等调用，生成"信息类型 → 用途"清单，用途写具体（例："相册（仅写入）：用于保存用户生成的海报"）。[^privacy] 涉及需要用户同意时使用官方隐私授权弹窗机制。[^privacy-dev]
4. **提审前自查（agent）**：对照下方清单逐条跑一遍；名称、简介、头像、首页功能一致；所有类目页面从首页 2 次点击内可达。[^reject]
5. **提交审核（human）**：填写测试账号、功能页面路径、补充说明（例如 AI 内容由哪个已备案模型生成、如何过滤不当内容）。
6. **被拒 → 修复 → 重提（agent + human）**：把拒绝理由原文贴给 agent，对照官方条款编号定位修复。
7. **发布 & 灰度（human）**：审核通过后发布；关注"小程序评测/投诉"消息。

## 提审自查清单（摘自官方常见拒绝情形，非全部）

- [ ] 名称/简介/头像：不侵犯他人商标、不含"国家级""最高级"等广告法禁用词，简介写明具体功能，名称与简介一致（1.1、1.2）
- [ ] 类目：页面核心内容与所选类目一致，从首页可直达或 2 次点击内到达（2.1、3.1.2）
- [ ] 功能有使用价值，不是只有一个页面/按钮；不是测试版（3.1.5、3.3.1）
- [ ] 无诱导分享/关注/下载，无强制分享解锁（3.2.1）
- [ ] 广告不遮挡功能、不超过页面一半（3.2.2）
- [ ] 不含算命、星座运势等"测试类内容"（3.2.4）
- [ ] UGC 有过滤不当内容的措施（3.2.11）
- [ ] 有账号体系时提供测试号；有易于发现的"退出"账户选项（3.3.4、3.5.5）
- [ ] 收集数据前明确告知用途并取得同意；注销后删除数据；位置追踪可退出（3.4.1、3.4.7）
- [ ] 不在页面请求用户输入微信账号密码（3.4.2）
- [ ] 多媒体不自动播放；浮层弹窗可关闭（3.5.2、3.6.2）
- [ ] 隐私保护指引声明与代码调用一致

## 常见拒绝原因与修复

| 拒绝原因（官方条款） | 修复 |
|---|---|
| 简介模糊、与功能不符（1.2.1） | 简介列出 2–3 个具体功能点，名称与简介呼应 |
| 类目与内容不符 / 类目页面打不开（2.1、2.2） | 改类目或补功能；确保路径可达 |
| 功能过于简单（3.1.5） | 补齐核心流程后再提 |
| 诱导分享（3.2.1） | 删除"分享后解锁"等文案与逻辑 |
| 需要登录但未提供测试号（3.3.4） | 在提审信息里填写测试账号 |
| 隐私保护指引与实际收集不一致 | 重新生成清单，删掉未使用的接口或补声明[^privacy] |
| 未备案无法上架 | 先完成小程序备案[^record] |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 类目映射、隐私接口扫描、生成隐私指引文案 | 注册小程序、选择主体、认证 |
| 对照官方拒绝情形做提审前自查 | 小程序备案提交、短信核验 |
| 修复被拒问题、写补充说明 | 提交审核、发布、处理投诉 |
| 用 miniprogram-ci 上传代码（需用户提供的上传密钥） | 保管上传密钥与 AppSecret |

## 官方来源

[^record]: 小程序备案操作指引 https://developers.weixin.qq.com/miniprogram/product/record/record_guidelines.html ；常见问答 https://developers.weixin.qq.com/miniprogram/product/record/record_faq.html
[^record-notice]: 微信公众平台《关于开展微信小程序备案的通知》 https://mp.weixin.qq.com/s/E4zAI5Y--nqRcRdPgSe-cw
[^privacy]: 用户隐私保护指引填写说明 https://developers.weixin.qq.com/miniprogram/dev/framework/user-privacy/
[^privacy-dev]: 小程序隐私协议开发指南 https://developers.weixin.qq.com/miniprogram/dev/framework/user-privacy/PrivacyAuthorize.html
[^reject]: 微信小程序平台常见拒绝情形 https://developers.weixin.qq.com/miniprogram/product/reject.html
[^mp-pay]: 微信支付·小程序支付开发接入准备 https://pay.weixin.qq.com/doc/v3/merchant/4015459512

> ⚠️ 免责声明：本文不是法律意见；审核尺度与类目资质随时调整，审核时长官方未承诺固定天数，以微信公众平台当时规则与审核反馈为准。
