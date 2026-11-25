---
name: domain-realname-dns
description: "域名实名认证与解析：选可备案后缀与工信部批复注册商、实名信息与备案主体一致、DNS 记录（A/CNAME/TXT/CAA）、CDN CNAME、HTTPS 证书验证。Use when buying a domain for a China launch, when ICP filing fails on 域名核验, when configuring DNS for a domestic server/CDN, or when the user mentions 域名实名 / 域名证书 / 解析."
---

# 域名实名与解析 · Domain Real-name & DNS

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** Picks a domain that can actually be ICP-filed (MIIT-approved TLD + MIIT-approved registrar), completes real-name verification with the same identity as the ICP filer, then configures DNS (A/CNAME for CDN, TXT for verification, CAA) and HTTPS. Most DNS work is automatable; real-name verification is human-only.

## 依据

- 《互联网域名管理办法》（工信部令第 43 号）第三十条：域名注册服务机构应要求申请者提供真实、准确、完整的身份信息并核验。[^43]
- ICP 备案"域名核验"：域名后缀须获工信部批复、注册商须获批复、域名已实名且在有效期内，实名信息须与备案主体名称、证件类型、证件号码一致（百度智能云、华为云备案文档口径）。[^bd][^hw]
- ⚠️ 许多新潮后缀（如部分 `.ai`、`.io` 等）**可能不在批复名单内**，无法备案。购买前去工信部/注册商页面查询当前批复后缀，不要凭印象。

## 前置条件

- [ ] 确定备案主体（个人 or 公司）——域名实名必须用**同一主体**
- [ ] 注册商：选择工信部批复的境内注册商（阿里云万网、腾讯云 DNSPod、华为云等），境外注册商域名通常需先转入
- [ ] 能接收实名审核结果的邮箱/手机号

## 步骤

1. **选后缀（agent 查询，human 决定）**：列出候选域名；对每个后缀检查是否可备案（查注册商"可备案后缀"页面），给出风险标注。
2. **实名认证（human）**：在注册商控制台创建"信息模板"，上传证件，等待实名审核通过。实名主体 = 备案主体。部分省份备案要求上传域名证书，实名通过后在注册商处下载。[^ali-mat]
3. **DNS 记录（agent 生成，可自动执行若有 API Key）**：

| 记录 | 用途 | 示例 |
|---|---|---|
| A / AAAA | 根域或 www 指向源站 | `@ A 1.2.3.4` |
| CNAME | 接入 CDN | `www CNAME www.example.com.w.cdngslb.com` |
| TXT | 域名归属验证、SPF | `_dnsauth TXT "..."` |
| CAA | 限制可签发证书的 CA | `@ CAA 0 issue "letsencrypt.org"` |

4. **HTTPS（agent）**：用云厂商免费/付费证书或 ACME（Let's Encrypt）签发；CDN 场景证书配置在 CDN 上。
5. **验证（agent）**：`dig +short www.example.com`、`curl -I https://www.example.com` 检查解析与证书链。

## 检查清单

- [ ] 后缀与注册商均在工信部批复范围内
- [ ] 实名主体 = 备案主体 = 后续支付商户主体
- [ ] 域名到期时间远离备案周期（避免备案期间到期）
- [ ] 根域、www 都解析且跳转一致
- [ ] HTTPS 证书覆盖所有子域名，自动续期已配置
- [ ] 备案通过前不要把域名解析到"未备案"的内地服务器上对外提供服务

## 常见驳回原因与修复

| 原因 | 修复 |
|---|---|
| 域名核验不通过：实名信息与主体不一致 | 修改域名实名或改用一致的主体[^hw] |
| 后缀/注册商未获批复 | 换后缀，或转入批复注册商[^bd] |
| 域名实名审核中 | 等实名完成后再提交备案 |
| CDN 添加域名失败：未备案 | 内地加速必须先备案（见 `china-cloud-cdn-deploy`） |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 查询后缀可备案性、比价 | 付款购买、实名认证上传证件 |
| 生成/通过 DNS API 写入记录（需用户授权的 Key） | 决定主体、保管账号 |
| 签发与续期证书、验证解析 | 处理注册商的人工审核 |

## 官方来源

[^43]: 《互联网域名管理办法》（工信部令第 43 号）https://www.miit.gov.cn/zwgk/zcwj/flfg/art/2017/art_43ec3819b2d04a31ad2c1c81c3f6100b.html
[^bd]: 百度智能云 ICP 备案·域名核验 https://cloud.baidu.com/doc/BeiAn/s/5jx4t46v1
[^hw]: 华为云 域名核验说明 https://support.huaweicloud.com/topic/264861-1-G
[^ali-mat]: 阿里云 备案所需资料（域名证书说明）https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/required-materials

> ⚠️ 免责声明：本文不是法律意见；可备案后缀名单与注册商资质会变化，购买前请以工信部与注册商当时页面为准。
