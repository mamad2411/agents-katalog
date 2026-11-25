---
name: gongan-beian
description: "公安联网备案（全国互联网安全管理服务平台 beian.mps.gov.cn）向导：ICP 备案通过后 30 日内办理、填报项、网站服务类型、备案号与图标放到页面底部。Use when ICP filing has just been approved, when the user mentions 公安备案 / 网安备案 / 公网安备 / beian.mps.gov.cn, or when auditing a site footer before launch."
---

# 公安联网备案 · Public Security Network Filing

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** After the MIIT ICP filing is approved, mainland sites must also file with the Ministry of Public Security platform (beian.mps.gov.cn) within 30 days of going live, then display the "公网安备" number + icon in the footer. The agent prepares the form data and footer code; the human logs in, verifies identity and submits.

## 依据与时限

- 《计算机信息网络国际联网安全保护管理办法》（公安部令第 33 号）第十二条：使用国际联网的法人和其他组织，应当**自网络正式联通之日起三十日内**办理备案手续。[^33]
- 不履行备案职责的，由公安机关给予警告或者停机整顿不超过六个月（第二十三条）。[^33]
- 办理平台：全国互联网安全管理服务平台 https://beian.mps.gov.cn/ ，可全程在线办理。[^xa]
- ⚠️ 个人网站是否必须办理、各地网安审核周期，各地口径不一，以平台和当地网安部门告知为准。

## 前置条件

- [ ] ICP 备案已通过，拿到"京ICP备XXXX号"（见 `icp-beian`）
- [ ] 网站可正常访问（审核期间网安人员需要能打开网站）[^ali]
- [ ] 主体证件、负责人身份证、手机号；部分地区要求上传域名证书
- [ ] 服务器公网 IP、接入服务商、域名注册服务商信息

## 步骤

1. **收集填报数据（agent）**：从工信部备案系统查询 ICP 备案号与审核通过日期（多数指南建议"网站开通日期"填 ICP 备案通过日）；从 DNS/云控制台读出公网 IP、接入商、域名注册商；整理成一张填报表。[^ali]
2. **登录与实名（human）**：在 beian.mps.gov.cn 注册/登录，完成实名认证。
3. **新办主体 → 新办网站（human 提交，agent 给填写内容）**：填写网站名称（与 ICP 备案一致）、主域名、IP、接入商、服务类型；如提供交互式服务（论坛、评论、用户上传、即时通讯等）需如实勾选，可能需要额外安全评估或材料。
4. **等待网安审核**：留意短信/平台消息，按要求补充材料。
5. **展示备案号（agent）**：备案成功后按平台要求放到网页底部（阿里云指南示例如下，图标与链接以平台"获取代码"为准）：[^ali]

```html
<a href="https://beian.mps.gov.cn/#/query/webSearch?code=11010502000000" target="_blank" rel="noreferrer">
  <img src="/assets/beian-gongan.png" width="16" alt=""> 京公网安备11010502000000号
</a>
```

## 检查清单

- [ ] 在 ICP 备案通过/网站开通后 **30 日内**提交
- [ ] 网站名称、域名与 ICP 备案一致
- [ ] IP 为公网 IP（不是内网 IP），接入商与实际一致
- [ ] 交互式服务如实勾选
- [ ] footer 同时展示 ICP 备案号与公网安备号，均可点击跳转查询

## 常见驳回原因与修复

| 原因 | 修复 |
|---|---|
| 审核期间网站打不开 | 保持网站可访问，或按要求提供说明[^ali] |
| 网站名称/域名与 ICP 信息不一致 | 以工信部查询结果为准逐字填写 |
| IP 填成内网 IP 或 CDN 节点 IP 不一致 | 填源站公网 IP，必要时说明 CDN 情况 |
| 服务类型漏报（实际有评论/上传） | 如实勾选交互式服务并补材料 |
| 未在页面展示备案号 | 按平台代码放到页面底部 |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 查 ICP 号、通过日期、IP、接入商，生成填报表 | 平台注册登录、实名认证、提交 |
| 判断是否属于交互式服务（扫描代码里的评论/上传/IM 功能） | 接听网安电话、补充材料 |
| 生成 footer 代码、PR | 对填报内容真实性负责 |

## 官方来源

[^33]: 《计算机信息网络国际联网安全保护管理办法》（公安部令第 33 号），网信办转载 https://www.cac.gov.cn/2014-10/08/c_1112737294.htm
[^xa]: 西安市公安局《带你一文看懂公安联网备案》 http://police.xa.gov.cn/jwzq/blfj/jwdt/1983007005389910017.html
[^ali]: 阿里云 公安联网备案信息填写指南 https://help.aliyun.com/zh/icp-filing/basic-icp-service/the-public-security-network-for-the-record-information-fill-in-the-guide

> ⚠️ 免责声明：本文不是法律意见；各地网安审核要求和周期不同，以全国互联网安全管理服务平台与当地公安机关要求为准。
