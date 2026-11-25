---
name: alipay
description: "支付宝接入：开放平台创建应用、接口加签方式（公钥/公钥证书）、签约电脑网站支付/手机网站支付/App 支付/当面付的条件、alipay.trade.page.pay 下单、异步通知验签并返回 success、查单与退款、常见签约驳回。Use when adding Alipay to a website, H5 or App, when the user mentions 支付宝 / 开放平台 / APPID / 应用私钥 / notify_url / 电脑网站支付, or when Alipay contract review is rejected."
---

# 支付宝接入 · Alipay Integration

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律或财务意见。**

**English summary:** Create an app on the Alipay Open Platform, configure signing keys (public key or public-key certificate mode), sign the right product (PC website pay, mobile website pay, App pay, face-to-face), call `alipay.trade.page.pay`, verify async notifications and answer with plain-text `success`, plus query/refund and common contract-review rejections. Website products require ICP filing whose subject matches the Alipay account.

## 前置条件（已核对的签约条件）

电脑网站支付 / 手机网站支付签约要求（支付宝文档中心口径）：[^pc-cond][^wap-cond]

- [ ] 网站能正常访问、页面信息完整，有明确经营内容和完整商品信息；
- [ ] 网站**必须完成 ICP 备案**，且备案主体与支付宝账号主体一致；不一致需上传授权函；
- [ ] 个人支付宝账号申请需提交营业执照（如个体工商户），且账号名称与营业执照主体一致。

其他：
- [ ] 支付宝企业账号或已绑定执照的账号，开放平台开发者入驻
- [ ] 服务端 HTTPS 回调地址
- ⚠️ 费率以签约页面为准，本 skill 不列数字。

## 步骤

1. **选产品（agent）**：PC → 电脑网站支付（`alipay.trade.page.pay`，`product_code=FAST_INSTANT_TRADE_PAY`）；手机浏览器 → 手机网站支付；原生 App → App 支付；线下扫码 → 当面付。[^pc-quick]
2. **创建应用（human）**：在 https://open.alipay.com 创建网页/移动应用，配置**接口加签方式**（推荐证书模式时按文档上传 CSR，或公钥模式），设置应用网关、授权回调地址；提交上线审核。[^prep]
3. **签约产品（human）**：在商家平台开通对应支付产品，填写网站地址（与备案一致）。
4. **下单（agent）**：使用官方 SDK；必填 `out_trade_no`、`total_amount`（单位：元，两位小数）、`subject`、`product_code`；配置 `return_url`（同步跳转，仅用于展示）与 `notify_url`（异步通知，**以此或主动查单为准**）。[^pc-quick]
5. **异步通知（agent）**——按官方说明：[^notify]
   1. 用 POST 接收参数；
   2. 除 `sign`、`sign_type` 外参数按规则排序拼接，用**支付宝公钥**（或支付宝公钥证书）RSA2 验签（SDK：`rsaCheckV1` / `certificateCheck` 等）；
   3. 校验 `out_trade_no`、`total_amount`、`seller_id`、`app_id` 与本地一致；
   4. `trade_status` 为 `TRADE_SUCCESS` / `TRADE_FINISHED` 才视为成功；
   5. 处理成功后响应体**只输出纯文本 `success`**（不能有空格、HTML），否则支付宝会重复通知。

```python
# Python 示意（alipay-sdk-python），以官方 SDK 文档为准
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
def handle_notify(form: dict, alipay_public_key: str) -> str:
    sign = form.pop("sign"); form.pop("sign_type", None)
    content = "&".join(f"{k}={form[k]}" for k in sorted(form) if form[k] != "")
    if not verify_with_rsa(alipay_public_key, content.encode("utf-8"), sign):
        return "fail"
    # TODO: 校验 out_trade_no / total_amount / app_id / seller_id 与本地订单一致
    if form.get("trade_status") in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        mark_order_paid_idempotently(form["out_trade_no"])  # 幂等
    return "success"  # 已正确处理（含非成功状态）即回 success，避免重复通知
```

6. **兜底（agent）**：`alipay.trade.query` 主动查单；`alipay.trade.refund` 退款；`alipay.trade.close` 关单；下载对账单。
7. **沙箱 → 生产**：先在开放平台沙箱环境联调，再切生产 APPID 与网关，做真实小额测试。

## 检查清单

- [ ] 网站 ICP 备案主体 = 支付宝账号主体（或已上传授权函）
- [ ] 签约时填写的网站可访问、商品与价格完整
- [ ] 应用私钥只在服务端；支付宝公钥/证书与环境（沙箱/生产）匹配
- [ ] 以异步通知或查单结果为准，不以 return_url 为准
- [ ] 通知处理幂等，返回纯文本 `success`
- [ ] 金额单位为元（与微信支付的"分"不同！）

## 常见驳回 / 故障原因与修复

| 原因 | 修复 |
|---|---|
| 网站无法访问 / 页面不完整 | 确保链接可打开、页面完整后重新提交[^reject] |
| 网站备案主体与账号主体不一致 | 统一主体或上传授权函[^pc-cond] |
| 个人账号无营业执照 | 先办个体工商户执照或用企业账号[^pc-cond] |
| 经营内容不明确/商品信息缺失 | 补全商品、价格、售后与联系方式 |
| 验签失败 | 公钥用错（应用公钥≠支付宝公钥）、沙箱生产混用、参数被 URL 编码处理错误 |
| 重复通知 | 未返回纯文本 `success` |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 写下单/通知/查单/退款代码与单测、沙箱联调 | 开放平台入驻、创建应用、产品签约 |
| 生成 CSR / 密钥对（在用户本地，私钥不外传） | 上传公钥/CSR、保管私钥 |
| 检查网站是否满足签约条件 | 授权函、执照等材料 |

## 官方来源

[^pc-cond]: 电脑网站支付申请条件 https://opendoc.alipay.com/b/03ah5w?pathHash=4542d144
[^wap-cond]: 手机网站支付申请签约的条件 https://opendoc.alipay.com/b/09icjt?pathHash=0ca62d7d
[^pc-quick]: 电脑网站支付快速接入 https://opendoc.alipay.com/open/270/105899?pathHash=d57664bf
[^prep]: 电脑网站支付·接入准备 https://opendoc.alipay.com/open/270/01didh?pathHash=a6ccbe9a
[^notify]: 异步通知说明 https://opendoc.alipay.com/open/0amki1?pathHash=ab0895b0 ；v3 异步通知 https://opendocs.alipay.com/open-v3/05w4ku
[^reject]: 订单为什么会被审核退回 https://opendoc.alipay.com/b/039rtn?pathHash=5b04b222

> ⚠️ 免责声明：本文不是法律、财务意见；支付宝文档页面为前端渲染，内容可能更新，签约条件与费率以开放平台当时页面为准。
