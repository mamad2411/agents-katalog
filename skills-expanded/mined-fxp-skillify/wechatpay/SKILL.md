---
name: wechatpay
description: 接入微信支付商户 APIv3（pay.weixin.qq.com、api.mch.weixin.qq.com）直连商户模式的开发手册，覆盖 APIv3 请求签名（Authorization WECHATPAY2-SHA256-RSA2048）与应答验签（微信支付公钥 PUB_KEY_ID 或平台证书）、JSAPI / 小程序 / Native / H5 / APP 下单与前端调起支付签名、查单与关单、申请退款与退款查询、支付成功和退款结果回调的验签与 AEAD_AES_256_GCM 解密、交易账单与资金账单下载、HTTP 状态码与错误码。当用户提到"微信支付""WeChat Pay""wechatpay""APIv3""api.mch.weixin.qq.com""prepay_id""code_url""h5_url""wx.requestPayment""WeixinJSBridge""paySign""notify_url 回调""APIv3 密钥""商户 API 证书""微信支付公钥""平台证书""wechatpay-java""wechatpay-go""wechatpay-php"，或要写代码实现微信收款、退款、对账、处理微信支付回调时，应主动使用本技能，不要凭记忆混用 v2 接口（XML、MD5 或 HMAC 签名、/pay/unifiedorder）的写法。
---

# 微信支付（商户 APIv3）接入指南

本 skill 覆盖微信支付面向**直连商户**（普通商户）的 APIv3：五种收款方式的下单、查单与关单、退款、回调、账单。
目标是让 Agent 第一次写代码时，签名、验签、回调解密和金额单位就是对的。**本页只做分流与规则，字段表和示例在 `references/`。**

## ⚠ 验证状态

这是文档版。内容整理自 <https://pay.weixin.qq.com/doc/v3/merchant>（从 `llms.txt` 逐级展开，抓取于 2026-09-11），
**没有用真实凭证调用验证过**，也还没有跑对照实验。

- **无凭证探测（2026-09-11）**：发了 13 个不带凭证、或者带伪造商户号的请求，确认了以下几种情况的真实返回格式：鉴权失败、缺 User-Agent、时间戳过期、请求方法错误、路径不存在、v2 接口。各 reference 里标为「无凭证探测」，原始记录在 `wechatpay-workspace/probe-log.md`。
- **离线复算**：用文档公开的测试私钥复算了签名示例。Body、Path、JSAPI 调起、APP 调起 4 个示例和文档一致；Query 签名示例和微信支付公钥验签示例复算不出来（见 `auth-signing.md` §8）。
- 其余字段、错误码、行为描述，都是**文档原文，未实测**。拿到凭证后，按 `wechatpay-workspace/verification-plan.md` 补测。
- 只覆盖**直连商户**。服务商模式（服务商替子商户收款）不覆盖，文档在 `https://pay.weixin.qq.com/doc/v3/partner/llms.txt`。

## 当前事实

| 项 | 值 |
| :--- | :--- |
| Base URL | `https://api.mch.weixin.qq.com`（备用 `https://api2.mch.weixin.qq.com`，探测可达）。v3 的路径一律以 `/v3/` 开头；**没有沙箱环境** |
| 请求鉴权 | `Authorization: WECHATPAY2-SHA256-RSA2048 mchid="…",nonce_str="…",signature="…",timestamp="…",serial_no="…"`（值用双引号，逗号后不加空格） |
| 签名串 | `METHOD\nURL（去掉域名，带 ?query）\nTIMESTAMP\nNONCE\nBODY\n`，用商户 API 证书私钥做 SHA256withRSA，结果 base64 |
| 必需的请求头 | `Accept: application/json`、`User-Agent`（无凭证探测：`/v3/certificates`、`/v3/refund/*` 缺 UA 直接 400；交易类 `/v3/pay/transactions/*` 缺 UA 仍先报 401 签名错误——一律带上）；有 body 时加 `Content-Type: application/json`；公钥模式加 `Wechatpay-Serial: PUB_KEY_ID_…` |
| 应答 / 回调验签 | 验签串是 `TIMESTAMP\nNONCE\nBODY\n`；根据 `Wechatpay-Serial` 选微信支付公钥或平台证书；时间戳偏差不能超过 ±5 分钟 |
| 回调解密 | `resource` 用 AEAD_AES_256_GCM 加密：key 是 APIv3 密钥（32 字符原串），nonce 和 associated_data 都用原串 |
| 金额 | **整数，单位是分**（`amount.total: 100` 就是 1 元）。账单文件里是「元」，而且是字符串 |
| 有效期 | `prepay_id` / `code_url` 2 小时；`h5_url` 5 分钟；账单 `download_url` 5 分钟；未付款的订单 7 天后自动关闭 |
| 最容易选错的 | `serial_no` 是**商户 API 证书**的序列号；`Wechatpay-Serial` 是微信支付公钥 ID 或平台证书序列号，两者不能互换 |

## 照通用经验写容易错的地方（来自文档，未实测）

1. **签名时用的 body 必须和发出去的字节完全一样，query 也要算进签名串。** 正确顺序是：先 `json.dumps` 成紧凑字符串，用它签名，再用 `data=` 发送。
   用 `requests` 的 `json=` 参数会重新序列化一次，导致 401。GET 查单时的 `?mchid=…` 也必须出现在签名串的第 2 行。
2. **`serial_no` 和 `Wechatpay-Serial` 对应的是两套不同的密钥。** Authorization 里放的是商户 API 证书的序列号；验签和加密用的是微信支付公钥 ID（`PUB_KEY_ID_…`）或平台证书序列号。
   放错会报「商户证书序列号有误」。
3. **调起支付需要后端再签一次名，而且三端的 `package` 格式不一样。** JSAPI 和小程序签的是 `appId\ntimeStamp\nnonceStr\nprepay_id=xxx\n`；
   APP 的第 4 行只放 `prepay_id` 本身，`package` 固定填 `Sign=WXPay`；时间戳单位是秒。前端收到的 `ok` 不能作为支付成功的依据，要以查单或回调为准。
4. **回调的处理顺序：先用原始 body 验签，再用 APIv3 密钥解密，5 秒内回 200 或 204（不带 body）。** 不要回 v2 那种 XML `SUCCESS`。
   验签失败要回 4xx 或 5xx。微信支付会故意发一些签名以 `WECHATPAY/SIGNTEST/` 开头的探测请求（签名是错的），同一条通知最多重发 15 次，所以处理逻辑必须幂等。
5. **金额用整数分；申请退款时三个字段都必须传。** 分别是 `amount.refund`、`amount.total`（原订单金额）和 `currency: "CNY"`（退款时是必填）。账单文件里的金额单位是元，不要混用。
6. **退款遇到超时、429 或 500 时，先查询再重试，而且永远用原来的 `out_refund_no`。** 申请退款成功只表示「已受理」（状态是 `PROCESSING`）；换一个新单号重试可能导致退两次款。
   另外，如果申请退款时没传 `notify_url`、而商户平台上配置了回调地址，收到的会是 v2 格式的 XML 退款通知。
7. **v2 和 v3 的写法不能混用。** v2 的特征：路径是 `/pay/*`，XML 格式，MD5 或 HMAC 签名，失败时也返回 HTTP 200 加 `return_code=FAIL`（已探测）。
   v3 的特征：路径是 `/v3/*`，JSON 格式，RSA 签名，失败返回 HTTP 4xx 加 `code`。FAQ 里出现的 `refund_fee`、`total_fee`、「201 商户订单号重复」都是 v2 的说法。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 构造请求签名、验证应答签名、在微信支付公钥和平台证书之间选择、加密敏感字段 | [`auth-signing.md`](references/auth-signing.md) | `Authorization` 头 · `GET /v3/certificates` |
| 按场景选支付产品、下单、生成前端调起支付的参数 | [`payments.md`](references/payments.md) | `POST /v3/pay/transactions/{jsapi,native,h5,app}` |
| 查订单状态、关单、没收到回调时轮询兜底 | [`orders.md`](references/orders.md) | `GET /v3/pay/transactions/out-trade-no/{out_trade_no}` · `POST …/{out_trade_no}/close` |
| 全额或部分退款、查询退款、处理异常退款、安全地重试 | [`refunds.md`](references/refunds.md) | `POST /v3/refund/domestic/refunds` · `GET /v3/refund/domestic/refunds/{out_refund_no}` |
| 接收支付成功和退款结果回调：验签、解密、应答 | [`notifications.md`](references/notifications.md) | `notify_url`（`TRANSACTION.SUCCESS` · `REFUND.*`） |
| 下载交易账单或资金账单，用来对账 | [`bills.md`](references/bills.md) | `GET /v3/bill/tradebill` · `GET /v3/bill/fundflowbill` · `GET download_url` |
| 看懂 HTTP 状态码和 `code`，判断能否重试，排查签名报错 | [`errors.md`](references/errors.md) | 所有接口的 4xx / 5xx |

## House rules

- **先判断 HTTP 状态码，再判断 `code`；message 只写进日志。** 同一个 `SIGN_ERROR`，探测到了 4 种不同的 message。同一个 code 在不同接口里的 HTTP 状态也可能不同（`MCH_NOT_EXISTS` 在下单接口是 400，在退款接口是 404）。
- **2xx 应答必须验签；4xx 应答不带签名头（已探测），不能验签。** 404 和 405 的 body 是空的（已探测），解析 JSON 之前要先判空。
- **服务器要用 NTP 同步时间。** 请求的时间戳偏差超过 5 分钟会直接返回 401（已探测）。验证应答和回调时，同样要拒绝偏差超过 5 分钟的时间戳。
- **支付结果只认「验签通过的查单结果或回调」。** 前端回调只能用来展示。`NOTPAY` 不等于支付失败，要标记为失败，先调关单接口。T+1 用交易账单对账。
- **`notify_url` 的要求**：`https://` 开头、公网可访问、不能带参数、不能做登录态校验；防火墙要放行微信支付的回调 IP 段（见 `notifications.md` §9）。没设置 APIv3 密钥的话，微信支付不会发回调。
- **优先用微信支付公钥**，它不会过期。如果用平台证书，要定时拉取（间隔小于 12 小时），不能写死在代码里。从平台证书切换到公钥的灰度期间，两种签名的回调都会收到。
- **官方服务端 SDK 只有 Java、PHP、Go 三种**（`wechatpay-java`、`wechatpay/wechatpay`、`wechatpay-go`），会自动处理签名和验签。Python 和 Node 需要按 `auth-signing.md` 自己实现。下载账单时，SDK 的自动验签不适用。
- **密钥和证书只放在环境变量或密钥管理系统里**，不能进代码仓库，也不能出现在前端。`apiclient_key.pem` 只能下载一次；APIv3 密钥设置之后无法再查看。
- **本 skill 不覆盖**：服务商模式、合单支付、付款码支付（V2）、刷脸支付、医保支付、分账、商家转账、微信支付分、代金券与营销、消费者投诉，以及所有 V2 接口。
  这些的文档从 `https://pay.weixin.qq.com/doc/v3/merchant/llms.txt` 进入。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

| 位置 | 问题 |
| :--- | :--- |
| `auth-signing.md` §5 | Gap 标记：文档说所有应答都会签名，但探测到的 4xx 应答没有 `Wechatpay-*` 头 |
| `auth-signing.md` §6 | `/v3/certificates` 的 `effective_time` / `expire_time`：参数表写 integer，说明写 RFC3339，示例是字符串，而且示例里的键名带了尾随空格 |
| `auth-signing.md` §7 | 敏感字段加密的 OAEP 哈希算法：加密指引和官方工具库用 SHA-1，FAQ 却推荐 SHA-256 |
| `auth-signing.md` §8 | Query 签名示例复算不出来；微信支付公钥验签示例里的公钥和签名对不上 |
| `payments.md` §2 | `time_expire` 的上限：Native 页写 7 天，其他页写 15 天。订单号重复时：FAQ 写返回 `201`，API 页写 `403 OUT_TRADE_NO_USED` |
| `payments.md` §7 | 调起支付签名示例里的签名值，末尾多了一个 `%` |
| `orders.md` §7 | 没有写查单、关单的频率上限 |
| `refunds.md` §6–7 | FAQ 里的 `TRADE_OVERDUE` 等错误码没写 HTTP 状态；FAQ 用了 v2 的字段名 `refund_fee` / `total_fee` |
| `notifications.md` §11 | 回调验签时怎么选公钥，两处说法不一；`associated_data` 的取值没写；验签失败时应答要不要带 body，前后表述矛盾 |
| `bills.md` §7 | `download_url` 两处示例的路径不一样；账单里的交易类型是 `FACE`，API 里是 `FACEPAY`，而且账单缺 `MWEB`；资金账单「收支金额」的说明有笔误；`hash_value` 是按压缩前还是压缩后计算的，没写 |
| `errors.md` §1、§9 | 429 的错误码：HTTP 状态码页写 `RATELIMIT_EXCEEDED`，各 API 页写 `FREQUENCY_LIMITED`。Gap 标记：交易类接口的 401 应答里没有 `Request-ID` |
