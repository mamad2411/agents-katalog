---
name: yonyou
description: 接入用友 YonBIP 开放平台（用友 iuap 开放平台，open.yonyoucloud.com）OpenAPI 的使用手册（文档版）——覆盖用友 YonBIP 公有云（开放平台 API 文档中的「用友 YonBIP」产品线，系统标识 yonsuite，接口路径 /yonbip/…）：按租户查数据中心网关、access_token 的 HmacSHA256 签名、业务单元与部门、客户/供应商/物料档案、采购订单与销售订单的保存提交审核、总账凭证与会计期间、事件订阅回调的验签解密、返回码幂等与限流。不覆盖 YonBIP 高级版、NC Cloud、U8 Cloud、NC、U8（私有部署需网关客户端）及 U8+、畅捷通。当用户提到"用友""YonBIP""YonSuite""用友开放平台""iuap""open.yonyoucloud.com""diwork""getAccessToken""getGatewayAddress""resubmitCheckKey""yonbip-open-api-sdk"，或要写代码把外部系统与用友 BIP 的组织、客户、供应商、物料、采购销售订单、凭证对接、接收用友事件推送时，应主动使用本技能，不要凭记忆编造签名串、网关域名、请求外壳或字段编码。
---

# 用友 YonBIP 开放平台接入指南

用友 iuap 开放平台（open.yonyoucloud.com）把 YonBIP 公有云的业务能力开放成 OpenAPI 与事件推送。
**本 skill 覆盖用友 YonBIP 公有云**——开放平台「API 文档」里的「用友 YonBIP」产品线（系统标识 `yonsuite`，接口路径 `/yonbip/…`）。
**不覆盖** YonBIP 高级版（公开 API 文档里该分类为空）、NC Cloud / U8 Cloud / NC / U8（部署在客户服务器，要装网关客户端），以及 U8+、畅捷通系产品——接口与鉴权都不同，别套用。
**本页只做分流与规则，字段表和示例在 `references/`。**

## ⚠ 验证状态

文档版：内容整理自 <https://open.yonyoucloud.com/> 文档中心（接入文档 236 页、API 详情 40 个、事件详情 7 个，经站点公开 JSON 接口抓取于 2026-09-11）
与官方 gitee 示例仓库（corp-demo / isv-demo）的 README 和源码网页，**未用真实凭证调用验证**。
无凭证探测：对数据中心查询、token 接口、业务网关共发了 25 次伪造参数请求（结果见 `auth-and-gateway.md` §7、`errors-and-limits.md` §2），
业务接口的入参与返回没有测过。拿到凭证后按 `yonyou-workspace/verification-plan.md` 补测；对照实验待凭证到位后进行。

## 当前事实

| 项 | 值 |
| :--- | :--- |
| Base URL | **按租户动态**：先 `GET https://apigateway.yonyoucloud.com/open-auth/dataCenter/getGatewayAddress?tenantId=…`，取 `data.tokenUrl`（形如 `https://…/iuap-api-auth`）和 `data.gatewayUrl`（形如 `https://…/iuap-api-gateway`） |
| 取 token | `GET {tokenUrl}/open-auth/selfAppAuth/base/v1/getAccessToken?appKey=…&timestamp=<毫秒>&signature=…`；ISV 用 `/open-auth/suiteApp/base/v1/getAccessToken`（suiteKey + tenantId） |
| 签名 | 除 signature 外的参数按名排序，「名+值」直接拼接（`appKey<值>timestamp<值>`）→ HmacSHA256（key = appSecret）→ Base64 → URL 编码一次 |
| 调业务接口 | `{gatewayUrl}/yonbip/<路径>?access_token=…`——token 在 **URL query**；POST 带 `Content-Type: application/json`；HTTPS、TLS ≥ 1.2 |
| token 有效期 | 2 小时（`data.expire: 7200` 秒）；token 与网关查询的成功码是字符串 `"00000"` |
| 成功判定 | 业务接口 `str(code) == "200"`；批量 / 提交 / 审核还要 `data.failCount == 0` |
| 最容易选错 | 写接口的外壳：订单、档案保存 `{"data":{…,"_status":"Insert"}}`；批量 `{"data":[…]}`；凭证保存是**顶层字段**；幂等键 `resubmitCheckKey` 放 `data` 里、≤ 32 位 |
| 无凭证探测（2026-09-11） | 不带 token → HTTP 200 `{"code":"310001"}`；假 token → HTTP 200 `{"code":"310036","message":"非法token"}`（code 为字符串）；未注册路径 → **HTTP 404** `310404`，且先于 token 校验；token 接口伪造 appKey → `{"code":"10018","message":"应用不存在或appKey已停用"}` |

## 照通用经验写容易错的地方（来自文档，未实测）

1. **没有固定 API 域名，先按租户查网关。** 每个数据中心有独立的开放平台；`api.diwork.com` 是多数据中心改造前的旧 tokenUrl，别写死。返回的两个域名已带 `/iuap-api-auth`、`/iuap-api-gateway` 前缀。
2. **签名串里没有 `=`、`&`，摘要不是 hex。** `appKey<值>timestamp<值>` 做 HmacSHA256 取二进制再 Base64；timestamp 用毫秒（官方 isv-demo 的 Python 示例用了秒，与参数表矛盾）；用 `requests` 的 `params=` 就别自己先 `quote`，否则编码两次。
3. **access_token 放 URL 参数，不放 Authorization 头。** 新版 token 较长且含特殊字符，拼 URL 时要编码；2 小时有效，缓存复用，别每次调用都重新签名。
4. **保存 ≠ 生效，而且要 `_status`。** 订单保存后还要调 `batchsubmit`、`batchaudit`；表头和每行子表都要 `_status: Insert/Update`；删采购订单还要带 `pubts`。
5. **`code: "200"` 不代表批量全部成功。** 批量保存、提交、审核、删除部分失败时仍返回 200，要看 `data.failCount` / `messages`（官方拼写 `sucessCount`）。
6. **同名概念的字段写法因接口而异。** 多语言 `{"simplifiedName"}` 与 `{"zh_CN"}` 两套；采购订单用 `vendor_code`、`product_cCode` 等 `_code` 字段，销售订单一个字段接受 ID 或编码，且有 `"orderPrices!currency"` 这种带 `!` 的扁平键。
7. **事件回调的验签有三种互相矛盾的写法。** 官方 demo 源码是对 timestamp、nonce、encrypt 三个值排序拼接后以 appSecret 做 HmacSHA256 再 Base64；用 CHECK_URL 测试事件核对，推送超时 5 秒，失败重推 24 小时。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 查租户网关、签名取 token、调用任意业务接口、用官方 SDK | [`auth-and-gateway.md`](references/auth-and-gateway.md) | `GET /open-auth/dataCenter/getGatewayAddress`、`GET /open-auth/selfAppAuth/base/v1/getAccessToken` |
| 同步业务单元与部门 | [`organization.md`](references/organization.md) | `POST /yonbip/digitalModel/orgunit/querytree`、`POST /yonbip/digitalModel/admindept/tree`、`POST /yonbip/digitalModel/orgunit/save` |
| 同步客户、供应商、物料、计量单位，分配使用组织 | [`master-data.md`](references/master-data.md) | `POST /yonbip/digitalModel/merchant/newlist`、`POST /yonbip/digitalModel/vendor/batchSaveV2`、`POST /yonbip/digitalModel/product/idempotent/save` |
| 创建 / 提交 / 审核 / 删除采购订单与销售订单 | [`purchase-sales-orders.md`](references/purchase-sales-orders.md) | `POST /yonbip/scm/purchaseorder/singleSave_v1`、`POST /yonbip/sd/voucherorder/singleSave`、`POST …/batchaudit` |
| 生成、查询、删除总账凭证，查会计期间 | [`gl-voucher.md`](references/gl-voucher.md) | `POST /yonbip/fi/ficloud/openapi/voucher/addVoucher`、`POST /yonbip/fi/ficloud/openapi/voucher/queryVouchers` |
| 接收事件推送：订阅、验签、解密、事件体、事件编码 | [`events.md`](references/events.md) | 回调 `POST {signature,timestamp,nonce,encrypt}` |
| 看懂返回码、幂等重试、限流与平台变更公告 | [`errors-and-limits.md`](references/errors-and-limits.md) | 平台码 `310xxx`、`resubmitCheckKey` |

本 skill 不覆盖：应用免登（`getBaseInfoByCode`）、移动端 JSAPI、待办 / 工作通知 / 服务号 / 群消息、审批中心、库存出入库与发货 / 发票单据、
应收应付、人力 / 制造 / 资产 / 项目云、ISV 上架与订单开通、NC Cloud / U8 Cloud / NC / U8 网关客户端接入。
这些文档在 open.yonyoucloud.com 文档中心的「接入文档」和「API 文档」对应分类下（API 分类树共 1305 个分类节点）。

## House rules

- 凭证只走环境变量：`YONBIP_TENANT_ID`、`YONBIP_APP_KEY`、`YONBIP_APP_SECRET`；缓存 `tokenUrl` / `gatewayUrl` 与 token（过期前刷新）。
- **路径以 API 详情的「请求地址」为准**，文档里的请求示例 URL 多处写错（`/yonsuite/` 前缀、`_copy` 后缀、双斜杠、租户前缀）。拿不准时用假 token 调一次：返回 `310404` 就是路径不存在。
- 解析响应先容错：`code` 可能是字符串或数字，个别接口鉴权失败返回纯文本；按 `code` 判断，不匹配 `message` 文案。
- 组织、客户、供应商、物料、税目、交易类型、账簿、科目、凭证类型的**编码因租户而异**，先用列表接口查，不要写死示例值。
- MDD 幂等接口（订单保存、客户 / 物料保存、凭证保存）传稳定的 `resubmitCheckKey`；非幂等接口（提交、审核、批量保存）超时后先查状态再重发。
- 不要用 `null` 表示「不修改」：2025-03-15 起 null 入参会透传到后台处理。新接入用最新版本接口，避开标为已废弃的。
- 事件只当「某 ID 变了」的信号：收到后调详情接口取完整数据，按 `eventId` 去重，另用 `pubts` 定时增量兜底。
- 限流码 `310032` / `310039` / `310042` / `310046` 指数退避；销售订单列表 / 详情 / 保存自 2026-03-31 起免费 60 次/分钟。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

**探测证实的文档错误（reference 里用 `<!-- Gap: … -->` 标记，共 3 处）**
- 会计期间查询示例 URL `/yonsuite/fi/fipub/basedoc/querybd/accperiod` 未注册（`310404`），应为 `/yonbip/…` → `gl-voucher.md` §6
- 客户档案保存示例 URL `/yonbip/digitalModel/merchant/newinsert_copy` 未注册，应为 `…/merchant/idempotent/newinsert` → `master-data.md` §4
- 文档称接口统一返回 `{code,message,data}` JSON；会计期间查询在假 token 时返回 `text/plain` 纯文本 `非法token` → `errors-and-limits.md` §2

**自相矛盾**
- timestamp 毫秒（参数表）vs 秒（isv-demo Python 示例）；ISV token 路径旧 / 新两种写法 → `auth-and-gateway.md` §3 §4
- 事件验签三种算法（倒序组合 HmacSHA256 / SHA256·SHA1 hex / demo 源码 HmacSHA256 Base64）；应答加密 `success` vs 明文 → `events.md` §3 §5
- 重复提交码 `10004`（码表）vs `100004`（幂等性页） → `errors-and-limits.md` §6
- 凭证保存示例 `billno` vs 参数 `billCode`、`externalSourceData*` 必填说明 vs 标记、`voucherStatus` 00 含义 → `gl-voucher.md` §2
- 销售订单详情示例 `http://api.diwork.com/yonsuite/…`；列表错误码数字 999 vs 字符串 → `purchase-sales-orders.md` §4 §8
- 客户 / 物料批量详情 body 是对象还是数组、客户保存必填项、供应商详情必填规则 → `master-data.md` §3 §4 §8 §12
- `orgtype`、`isEnd` 在不同组织接口里含义 / 类型不一；部门详情示例 `/yonsuite/…//` → `organization.md` §3 §5 §7
- 销售订单 / 物料 / 凭证事件的示例外壳与字段表不一致 → `events.md` §6

**文档未说明**
- 网关查询结果缓存多久、签名时间戳容忍窗口、签名二次编码容忍度、token 能否放 header、SDK 的生产 env 取值 → `auth-and-gateway.md`
- token 接口与网关查询接口的错误码表（探测到 `10018`、`"500"`） → `errors-and-limits.md` §4
- 凭证保存无 `data` 外壳时幂等键放哪、红字凭证写法、审核 / 记账接口（该分类公开接口里没有） → `gl-voucher.md` §1 §2
- 业务事件数据在外层 JSON 的位置、推送 Content-Type、自建应用解密源码 → `events.md` §2 §4 §6
- 限流窗口 / 配额、超出「免费调用次数」后是拒绝还是计费 → `errors-and-limits.md` §7
