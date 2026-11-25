---
name: icp-beian
description: "ICP 备案（工信部互联网信息服务备案）全流程向导：判断是否需要备案、经营性 ICP 许可证 vs 非经营性备案、材料清单、云厂商代备案、工信部短信核验、管局审核、备案号展示。Use when a website/App/小程序 will be served from a mainland China server or China CDN, when the user asks about 备案 / ICP / beian.miit.gov.cn / 备案号 / 管局, or before buying a domestic server for a launch."
---

# ICP 备案 · ICP Filing

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见**，以工信部备案管理系统、所在省通信管理局和你的云服务商最新页面为准。

**English summary:** Walks the agent and developer through China's MIIT ICP filing: decide whether you need it (mainland server/CDN ⇒ yes), filing (非经营性) vs licence (经营性 ICP 许可证), required materials, filing via your cloud provider, the MIIT SMS verification within 24 h, provincial review, and displaying the filing number in the site footer.

## 什么时候需要

- 依据《互联网信息服务管理办法》第四条：**经营性**互联网信息服务实行**许可**制度，**非经营性**实行**备案**制度；未取得许可或未履行备案手续，不得从事互联网信息服务。[^292]
- 实务触发条件：网站解析到**中国内地节点**服务器，或域名接入**中国内地 CDN**（见 `china-cloud-cdn-deploy`）。服务器全部在境外（含香港）一般不走 ICP 备案，但也就无法使用内地节点。
- App、小程序、快应用同样有备案要求（App 备案见 `app-store-ruanzhu`，小程序备案见 `wechat-miniprogram-launch`）。[^app]
- ⚠️ "收费 SaaS 是否属于经营性、要不要办 ICP 许可证（增值电信业务经营许可证）"因业务形态和省份口径不同而不同——**本 skill 不下结论**，请咨询当地通信管理局或专业律师。

## 前置条件（Prerequisites）

- [ ] 备案主体：个人（身份证）或单位（营业执照等）。证件剩余有效期 ≥ 3 个月（阿里云规则）。[^ali-mat]
- [ ] 域名：已在**工信部批复的注册商**注册、后缀在批复名单内、**已实名**且实名主体与备案主体一致（见 `domain-realname-dns`）。[^domain]
- [ ] 内地服务器：以阿里云为例，需中国内地节点、**包年包月且累计购买时长满 3 个月**，免费试用 ECS 不能备案；用服务器生成"备案服务码"。[^ali-server]
- [ ] 负责人手机号（能收工信部 12381 短信）、邮箱。
- [ ] 涉及新闻、出版、药品和医疗器械、文化、广播电影电视节目等的，需先办**前置审批**。[^ali-flow]

## 步骤（Step by step）

1. **判定（agent）**：扫描项目——部署目标是否在内地？是否接 CDN？是否有付费功能、用户发布内容（UGC）、AI 生成？输出"需要/不需要备案 + 可能需要的前置审批/许可"的判定表，标注不确定项。
2. **准备材料（human 为主）**：按云厂商页面上传。阿里云要求证件照片为原件拍摄（不能翻拍）、JPG/PNG 等格式、每张 200 KB–4 MB；部分省份另需域名证书、授权书、手持证件照等。[^ali-mat][^ali-upload]
3. **填写备案信息（agent 起草，human 提交）**：主办者信息、网站名称、网站服务内容、负责人信息。agent 可帮你起草"网站名称/网站简介"，避免使用与业务不符的名称、不使用"中国""国家""最高"等词（具体以管局规则为准）。
4. **真实性核验（human）**：用云厂商 App 完成人脸核验与证件拍摄。[^ali-upload]
5. **云厂商初审（human 接电话）**：阿里云初审约 1–2 个工作日，审核专员会打电话核对备案信息，请熟记自己填写的内容。[^ali-trial]
6. **工信部短信核验（human，24 小时内）**：提交管局后，负责人收到 12381 短信，须在 **24 小时内**登录工信部备案管理系统核验；逾期需重新提交。首次网站备案需"主体负责人 + 网站负责人"核验。[^ali-sms]
7. **管局审核（等待）**：一般 1–20 个工作日，无法加急（阿里云页面口径）。[^ali-flow]
8. **展示备案号（agent）**：在网站首页底部展示备案号并链接到 `https://beian.miit.gov.cn/`。agent 可直接改 footer：

```html
<a href="https://beian.miit.gov.cn/" target="_blank" rel="noreferrer">京ICP备XXXXXXXX号-1</a>
```

9. **30 日内做公安联网备案** → 转 `gongan-beian`。

## 检查清单（Checklist）

- [ ] 备案主体 = 域名实名主体 = （后续）支付商户主体，三者一致
- [ ] 服务器满足云厂商"可备案"条件，已拿到备案服务码
- [ ] 网站名称与网站内容一致，不含夸大/敏感词
- [ ] 审核期间网站状态符合所在管局要求（有的管局要求备案期间不开放访问——以初审客服告知为准）
- [ ] 12381 短信 24 小时内完成核验
- [ ] 备案通过后 footer 展示备案号并链接 beian.miit.gov.cn
- [ ] 日历提醒：30 日内办公安联网备案

## 常见驳回原因与修复

| 驳回原因 | 修复 |
|---|---|
| 证件不清晰/不完整/非最新证件 | 用云厂商 App 现场拍摄原件，上传最后一次办理的证件[^ali-upload] |
| 域名实名信息与备案主体不一致、域名后缀或注册商未获批复 | 先在注册商处修正实名或转入合规注册商[^domain] |
| 初审电话未接通或回答与提交信息不符 | 保持电话畅通，熟记填写内容[^ali-trial] |
| 短信核验超时/连续 5 次失败 | 24 小时内核验；失败需重新提交[^ali-sms] |
| 网站名称与内容不符、涉及需前置审批的内容 | 改名称或先办前置审批 |
| 证件有效期不足 3 个月、授权书超过 3 个月 | 更新证件/重新开具授权书[^ali-mat] |

## Agent 能做 vs 人必须做

| Agent 可以自动化 | 必须由人完成 |
|---|---|
| 判断是否需要备案、列出前置审批风险 | 选择备案主体、承担法律责任 |
| 生成材料清单、起草网站名称/简介 | 人脸核验、拍摄证件原件 |
| 检查域名实名/解析、服务器地域（读取 IaC/配置） | 接初审电话、24 小时内完成短信核验 |
| 修改 footer 加入备案号链接 | 在云厂商控制台提交订单 |
| 设置 30 日公安备案提醒 | 与管局/律师确认是否需要 ICP 许可证 |

## 官方来源（Sources）

[^292]: 《互联网信息服务管理办法》（国务院令第 292 号）https://www.gov.cn/gongbao/content/2000/content_60531.htm
[^app]: 工业和信息化部关于开展移动互联网应用程序备案工作的通知 https://www.gov.cn/zhengce/zhengceku/202308/content_6897341.htm
[^domain]: 《互联网域名管理办法》（工信部令第 43 号）https://www.miit.gov.cn/zwgk/zcwj/flfg/art/2017/art_43ec3819b2d04a31ad2c1c81c3f6100b.html
[^ali-flow]: 阿里云 ICP 备案流程概述 https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-application-overview
[^ali-mat]: 阿里云 备案所需资料 https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/required-materials
[^ali-upload]: 阿里云 资料上传和真实性核验 https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/upload-data-and-authenticity-verification
[^ali-trial]: 阿里云 备案审核全流程及注意事项 https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-to-the-board-audit-notice-before-trial
[^ali-sms]: 阿里云 工信部短信核验 https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/sms-check
[^ali-server]: 阿里云 备案前服务器及接入信息确认 https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-server-access-information-check

工信部备案管理系统：https://beian.miit.gov.cn/ 。腾讯云、华为云等其他接入商的流程类似但细节（服务器条件、初审时效）不同，以各自文档为准。

> ⚠️ 免责声明：政策与各省管局规则随时调整，本文仅为开发者整理的流程参考，不构成法律意见。时效数字均引用自上述页面，实际以审核为准。
