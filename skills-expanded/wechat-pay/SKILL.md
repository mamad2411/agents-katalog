---
name: wechat-pay
description: "微信支付接入（直连普通商户，APIv3）：商户号申请材料、AppID 绑定、选择支付产品（JSAPI/Native/H5/App/小程序）、下单、回调验签与 AES-256-GCM 解密、幂等与对账、常见驳回。Use when adding WeChat Pay to a website, H5, App or 小程序, when the user mentions 微信支付 / 商户号 / mchid / APIv3 / notify_url, or when payment callbacks fail verification."
---

# 微信支付接入 · WeChat Pay Integration (APIv3)

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律或财务意见。**

**English summary:** End-to-end WeChat Pay for a direct (普通) merchant on APIv3: what you need to apply (business licence — individuals without one go through a different 小微 path), binding AppID↔mchid, choosing JSAPI/Native/H5/App/Mini-Program, creating orders, verifying callback signatures (WeChat Pay public key or platform certificate), decrypting the resource with AES-256-GCM, idempotency and reconciliation. Code is automatable; applying, signing and key custody are human.

## 前置条件

- [ ] **主体**：普通商户入驻需营业执照（个体工商户 / 企业 / 机关事业单位等）。PC 网站接入页面列出的材料：营业执照、法人身份证、对公银行账户（个体户可用法人对私账户）。[^web]
- [ ] **网站场景需 ICP 备案**："微信支付支持完成域名 ICP 备案的网站接入支付功能"。[^web]
- [ ] **小程序场景**：小程序需为企业/个体工商户等可开通支付的主体，个人主体小程序不能接入普通小程序支付。[^mp-pay]
- [ ] 回调地址 `notify_url`：外网可访问的 HTTPS 地址。[^notify]
- [ ] 费用：微信支付页面写明"申请接入不收取申请费用"，交易服务费率"一般与经营类目有关，0.6%–1% 不等"——以你签约类目页面为准。[^web]

## 步骤

1. **选择产品（agent）**：

| 场景 | 产品 |
|---|---|
| PC 网站扫码 | Native 支付（生成二维码） |
| 微信内打开的网页（公众号 H5） | JSAPI 支付 |
| 手机浏览器（非微信内） | H5 支付（需单独申请开通） |
| 小程序 | 小程序支付（JSAPI 同源接口） |
| 原生 App | App 支付 |

2. **入驻（human）**：在商户平台 https://pay.weixin.qq.com 提交资料并完成账户验证；页面写明审核一般 1–2 个工作日，通过后在线签约。[^web]
3. **绑定 AppID（human）**：商户号与公众号/小程序/App 的 AppID 绑定（主体一致或按平台规则授权）。
4. **配置 API 密钥（human 生成，agent 只读环境变量）**：设置 APIv3 密钥、下载商户 API 证书；获取**微信支付公钥**（或平台证书）。密钥只放服务端 secret 管理，绝不进前端与 git。
5. **下单（agent）**：服务端调用对应下单接口，金额以"分"为单位、`out_trade_no` 由自己生成且唯一；建议使用官方 SDK（Java/Go/PHP/Node 等）。[^jsapi]
6. **回调处理（agent）**——官方要求的顺序：[^notify][^pubkey]
   1. 取**原始 body** 与请求头 `Wechatpay-Timestamp`、`Wechatpay-Nonce`、`Wechatpay-Signature`、`Wechatpay-Serial`；
   2. 构造验签串 `时间戳\n随机串\n原始body\n`，用 `Wechatpay-Serial` 对应的公钥做 SHA256-RSA 验签：序列号以 `PUB_KEY_ID_` 开头用**微信支付公钥**，否则用**平台证书**；
   3. 用 APIv3 密钥 + `resource.nonce` + `resource.associated_data` 对 `resource.ciphertext` 做 AES-256-GCM 解密；
   4. 校验 `mchid`、`appid`、`out_trade_no`、金额与本地订单一致，**幂等**更新订单状态；
   5. 成功返回 200/204；失败返回 4xx/5xx（微信会重试）。

```js
// Node.js 18+ 回调验签与解密示意（以官方文档为准）
import crypto from "node:crypto";
export function verifyAndDecrypt({ headers, rawBody, wechatpayPublicKeyPem, apiV3Key }) {
  const msg = `${headers["wechatpay-timestamp"]}\n${headers["wechatpay-nonce"]}\n${rawBody}\n`;
  const ok = crypto.verify("RSA-SHA256", Buffer.from(msg), wechatpayPublicKeyPem,
                           Buffer.from(headers["wechatpay-signature"], "base64"));
  if (!ok) throw new Error("bad signature");
  const { resource } = JSON.parse(rawBody);
  const buf = Buffer.from(resource.ciphertext, "base64");
  const decipher = crypto.createDecipheriv("aes-256-gcm", Buffer.from(apiV3Key), Buffer.from(resource.nonce));
  decipher.setAuthTag(buf.subarray(buf.length - 16));
  decipher.setAAD(Buffer.from(resource.associated_data || ""));
  return JSON.parse(Buffer.concat([decipher.update(buf.subarray(0, buf.length - 16)), decipher.final()]).toString());
}
```

7. **兜底（agent）**：回调丢失时用"查询订单"接口主动查单；定时下载对账单核对；退款走退款接口并处理退款回调。
8. **上线前测试（human + agent）**：用真实小额订单完整走一遍下单→支付→回调→退款。

## 检查清单

- [ ] 商户主体 = ICP 备案主体 = AppID 主体（或已按规则授权）
- [ ] 网站域名已 ICP 备案、HTTPS
- [ ] 密钥/证书只在服务端，日志不打印密钥与完整回调明文中的敏感信息
- [ ] 回调使用原始 body 验签（不要先 JSON.parse 再 stringify）
- [ ] 订单状态更新幂等；金额以分为单位且与本地订单比对
- [ ] 有主动查单与对账任务
- [ ] 商品/服务页面信息完整（价格、说明、客服方式、退款规则）
- [ ] 经营内容与签约类目一致

## 常见驳回 / 故障原因与修复

| 原因 | 修复 |
|---|---|
| 主体/证照信息不一致或过期、统一社会信用代码填错 | 核对营业执照逐字填写[^faq] |
| 网站无法访问、页面不完整、无商品与价格 | 上线完整的商品页、价格、联系方式后再提交 |
| 网站域名未备案 | 先完成 `icp-beian`[^web] |
| 经营类目选错（与实际业务不符） | 重新选择对应类目并补资质 |
| 回调验签失败 | 使用原始 body；序列号对应正确的公钥/证书；检查换行符[^pubkey] |
| 个人主体小程序无法开通支付 | 变更为企业/个体工商户主体[^mp-pay] |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 选择产品、写下单/回调/查单/退款/对账代码与测试 | 入驻、账户验证、签约、选择类目 |
| 准备商品页、退款规则、客服入口 | 生成并保管 APIv3 密钥、证书 |
| 检查网站是否满足"完整可访问"要求 | 绑定 AppID、真实支付测试 |
| 回调验签单元测试（用官方示例数据） | 对资金与税务合规负责 |

## 官方来源

[^web]: 微信支付接入指引·PC 网站（材料、费率、流程） https://pay.weixin.qq.com/static/applyment_guide/applyment_detail_website.shtml
[^mp-pay]: 微信支付·小程序支付开发接入准备 https://pay.weixin.qq.com/doc/v3/merchant/4015459512 ；小程序接入指引 https://pay.weixin.qq.com/static/applyment_guide/applyment_detail_miniapp.shtml
[^jsapi]: JSAPI 支付开发指引 https://pay.weixin.qq.com/doc/v3/merchant/4012791870
[^notify]: Native 支付·支付成功回调通知 https://pay.weixin.qq.com/doc/v3/merchant/4012791882
[^pubkey]: 如何使用微信支付公钥验签 https://pay.weixin.qq.com/doc/v3/merchant/4013053249 ；平台证书验签 https://pay.weixin.qq.com/doc/v3/merchant/4013053420
[^faq]: 微信支付·商户进件常见问题 https://pay.weixin.qq.com/doc/v3/partner/4012713017

> ⚠️ 免责声明：本文不是法律、财务或税务意见。申请材料、费率、类目资质随时调整，以微信支付商户平台当时页面为准。
