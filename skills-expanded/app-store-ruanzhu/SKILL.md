---
name: app-store-ruanzhu
description: "国内应用商店上架与软著：App 备案（工信部 2023 年起）、App Store 中国大陆区 ICP 备案号、华为/小米/OPPO/vivo/应用宝等安卓商店的软著或电子版权要求、计算机软件著作权登记材料（源程序前后各 30 页、每页 ≥50 行）、隐私合规检测。Use when listing an Android/iOS app in mainland China, when the user mentions 软著 / 软件著作权 / 应用市场上架 / App 备案 / 电子版权证书, or when a store rejects for missing qualification."
---

# 应用商店上架与软著 · App Store Listing & Software Copyright

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** Mainland app distribution needs (1) MIIT App filing — an App without filing may not provide internet information services; (2) for Apple's China mainland storefront, an ICP filing number in App Store Connect; (3) for most Android stores, proof of copyright — typically a Software Copyright Registration Certificate or an accepted e-copyright certificate (e.g. Huawei AppGallery). The agent can generate the copyright source-code & manual documents; the human submits and signs.

## 关键规则（已核对）

- **App 备案**：境内从事互联网信息服务的 App 主办者应履行备案手续，未履行备案手续不得开展 App 互联网信息服务；通过接入服务商或分发平台向省级通信管理局提交，备案号需在 App 显著位置展示。[^app]
- **App Store 中国大陆**：在 App Store Connect 提供 ICP 备案号，且信息需与工信部备案一致；游戏等还需要相应许可（如版号）。[^apple]
- **华为应用市场**：发布范围含中国大陆时，通常需提交版权证明，可选《计算机软件著作权登记证书》《APP 电子版权认证证书》等之一；应用名称需与证书软件名称一致。[^huawei]
- 其他安卓商店（小米、OPPO、vivo、应用宝等）普遍有类似资质要求，**具体以各商店开发者后台当期规则为准**（本 skill 未逐一核对）。
- **软著登记**：向中国版权保护中心申请，提交申请表、软件鉴别材料与证明文件；源程序提交前、后各连续 30 页（每页不少于 50 行），文档前、后各连续 30 页（每页不少于 30 行），不足 60 页的全部提交。[^reg]
- 自 2017 年 4 月 1 日起，中国版权保护中心停止收取软件著作权登记费（新华网报道）。[^free] 《计算机软件著作权登记办法》第二十条：中国版权保护中心应当自受理日起 60 日内审查完成（需补正的另计）。[^reg]

## 前置条件

- [ ] 主体（个人或公司）——软著著作权人、App 备案主体、开发者账号主体保持一致最省事
- [ ] App 名称定稿（软著名称、商店名称、备案名称一致）
- [ ] 隐私政策与用户协议（`pipl-privacy-policy`），App 首次启动弹窗征得同意
- [ ] 游戏：需版号；新闻、视听、出版、医疗等需对应许可

## 步骤

1. **App 备案（human，agent 准备信息）**：通过云服务商或分发平台提交；备案号写入"关于"页与商店信息。[^app]
2. **软著材料（agent 生成，human 核对签章）**：
   - 源程序文档：按"前 30 页 + 后 30 页、每页 ≥ 50 行"从项目中提取，页眉写"软件名称 + 版本号"与页码，名称版本与申请表一致；去掉密钥、个人信息、第三方开源代码大段原文。
   - 用户手册/设计说明书：前后各 30 页、每页 ≥ 30 行，截图配说明。
   - 申请表信息：开发完成日期、首次发表日期、运行环境、编程语言、源程序量、主要功能。
3. **提交软著登记（human）**：中国版权保护中心官网 https://www.ccopyright.com.cn/ 在线填报、签章、提交。
4. **商店上架（human）**：上传安装包、截图、隐私政策链接、软著或电子版权证书、App 备案号；iOS 填写 ICP 备案号。
5. **隐私合规自查（agent）**：对照《App 违法违规收集使用个人信息行为认定方法》：首次运行提示隐私政策、不默认勾选、不强制非必要权限、提供注销渠道。[^rending]

## 检查清单

- [ ] App 名称：软著 = 商店 = 备案 一致
- [ ] App 内显示备案号
- [ ] 源程序 60 页 / 每页 ≥ 50 行；文档 60 页 / 每页 ≥ 30 行；页眉名称版本一致
- [ ] 隐私政策首次启动弹窗 + 设置页可随时查看
- [ ] 权限按需申请，拒绝后不闪退、不反复弹窗
- [ ] 第三方 SDK 清单（名称、目的、收集的信息）写入隐私政策
- [ ] 游戏 / 特殊行业许可已备齐

## 常见驳回原因与修复

| 原因 | 修复 |
|---|---|
| 缺少软著/电子版权证明 | 申请软著或商店认可的电子版权证书[^huawei] |
| 应用名称与证书名称不一致 | 改名或变更登记 |
| 未展示 App 备案号 / 未备案 | 完成备案并在 App 内展示[^app] |
| iOS 中国区缺 ICP 备案号或信息不一致 | 在 App Store Connect 填写与工信部一致的备案号[^apple] |
| 隐私政策缺失、首次启动未提示、超范围收集 | 按 `pipl-privacy-policy` 修复[^rending] |
| 软著补正：页数行数不足、页眉不一致 | 重新生成鉴别材料，30 日内补正（以通知为准） |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 从仓库生成软著源程序 PDF 与操作手册草稿 | 确认著作权归属、签章、提交 |
| 汇总 SDK 清单、权限清单、隐私合规自查 | App 备案、开发者账号注册与付费 |
| 生成商店截图、文案（不含夸大用语） | 上传安装包、应对审核沟通 |

## 官方来源

[^app]: 工业和信息化部关于开展移动互联网应用程序备案工作的通知 https://www.gov.cn/zhengce/zhengceku/202308/content_6897341.htm
[^apple]: Apple App Store Connect Help · App information https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/ ；China mainland compliance information https://developer.apple.com/help/app-store-connect/manage-compliance-information/view-mainland-china-compliance-information
[^huawei]: 华为开发者·计算机软件著作权证书 资质文件说明 https://developer.huawei.com/consumer/cn/doc/App/50111-02
[^reg]: 《计算机软件著作权登记办法》（国家版权局） https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html
[^free]: 新华网《软件著作权登记免费了》 http://www.xinhuanet.com/zgjx/2017-04/01/c_136176406.htm
[^rending]: 《App 违法违规收集使用个人信息行为认定方法》 https://www.cac.gov.cn/2019-12/27/c_1578986455686625.htm

> ⚠️ 免责声明：本文不是法律意见；各应用商店资质要求经常更新，以各开发者后台当期规则为准。软著代理机构收取的服务费不属于官方费用。
