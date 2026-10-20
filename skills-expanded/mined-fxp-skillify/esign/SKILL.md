---
name: esign
description: 接入 e签宝电子签名开放平台（SaaS API V3，文档 open.esign.cn，接口域名 openapi.esign.cn，沙箱 smlopenapi.esign.cn）的 API 使用手册——涵盖 X-Tsign-Open-* 请求头与 HmacSHA256 请求签名（Content-MD5、待签名字符串）、本地文件上传（fileUploadUrl、PUT 文件流、状态轮询）与合同模板填充、签署流程（create-by-file 发起、签署方与签署区、签署链接、查询、撤销、完结、下载）、个人与机构实名认证和用户授权、回调通知接收与验签、错误码与限制。当用户提到"e签宝""esign""tsign""e签宝开放平台""SaaS API V3""签署流程""signFlowId""create-by-file""X-Tsign-Open-Ca-Signature""电子签名 API""电子合同接口"，或要写代码对接 e签宝发起合同签署、生成签署链接、处理签署完成回调时，应主动使用本技能，不要凭记忆编造签名算法和接口路径，也不要套用法大大、上上签、DocuSign 的接口习惯。
---
# e签宝（SaaS API V3）接入指南

e签宝开放平台的服务端 RESTful API：每个请求带 `X-Tsign-Open-*` 头和一个对"7 行待签名字符串"的 HmacSHA256 签名，
body 是 JSON；核心业务对象是"签署流程"（signFlowId），文件要先上传到 OSS 拿 fileId。
**本页只做分流与规则，字段表和示例在 references/。**

## ⚠ 验证状态

文档版：内容整理自 https://open.esign.cn/doc/opendoc/dev-guide3/el34xh 起的 SaaS API V3 文档（页面 SSR 状态里的正文，
共抓取 110 页，清单见 `esign-workspace/index.tsv`，抓取于 2026-09-11），**未用真实凭证调用验证**。
无凭证探测了 9 类请求（伪造 appId 的签名请求、缺鉴权头、过期时间戳、不存在路径、OAuth 换 token、伪造 token），
每条复跑两次一致，结果见 auth-and-signing.md §11 与 `esign-workspace/probe-log.md`。
签名 / Content-MD5 / 回调验签函数只用本地测试向量校验过拼接逻辑，从未被网关接受过。
拿到凭证后按 `esign-workspace/verification-plan.md` 补测；有 / 无 skill 的对照实验待真实凭证到位后进行。

## 当前事实

| 项 | 值 |
| --- | --- |
| Base URL | 正式 `https://openapi.esign.cn`；沙箱 `https://smlopenapi.esign.cn`（两者均探测到在线）。AppId / Secret / IP 白名单 / 模板两套环境各自独立 |
| 鉴权头 | `X-Tsign-Open-App-Id`、`X-Tsign-Open-Auth-Mode: Signature`、`X-Tsign-Open-Ca-Timestamp`（毫秒，15 分钟）、`X-Tsign-Open-Ca-Signature`、`Accept: */*`、`Content-Type: application/json; charset=UTF-8`、`Content-MD5` |
| 签名 | `Base64(HmacSHA256(AppSecret, "METHOD\nAccept\nContent-MD5\nContent-Type\nDate\n" + PathAndParameters))`；Date 为空也留空行；无自选 Headers 时不加那一行；query 按 key 升序且不编码 |
| Content-MD5 | `Base64(MD5 原始 16 字节(body))`，不是 hex；GET/DELETE 无 body 时为空串 |
| 成功判定 | `code == 0`（int）。网关鉴权失败是 HTTP 401 + `{"success":false,"code":401,"message":…}`（探测证实） |
| 前置条件 | 调用方公网出口 IP 必须在应用白名单里（2026-07-31 起不能填 `*`） |
| 最容易选错的字段 | `signFlowConfig.autoFinish` 默认 **false**（签完不自动完结、不能下载）；`autoStart` 默认 **true** |

## 照通用经验写容易错的地方（来自文档，未实测）

1. **签名串是 7 行换行拼接，不是参数排序拼接。** HTTP 方法、Accept、Content-MD5、Content-Type、Date、[Headers]、Path+Query，
   输出 Base64；漏传 `X-Tsign-Open-Auth-Mode: Signature` 会被当成 token 模式，报 `TOKEN_CANT_BE_NULL`（这一点无凭证探测证实）。
2. **body 只序列化一次。** 算 Content-MD5 的字节必须就是发出去的字节；用 `requests(json=...)` 这类会二次序列化的写法容易 `INVALID_SIGNATURE`。
3. **沙箱和正式是两套世界。** 域名、AppId、Secret、IP 白名单、模板、数据都不通用；401 `无效的应用` 常是 appId 与域名环境不匹配。
4. **上传文件是"拿地址 → PUT 到 OSS → 轮询状态"。** PUT 的 Content-MD5 / Content-Type 必须与第一步 body 一致，且不带 e签宝签名头；
   PUT 返回 `errCode:0` 不代表可用，要轮询到 `fileStatus` 为 2 或 5 再发起，否则 `1437513 文档未成功转换成pdf`。
5. **签完不会自动"完成"。** `autoFinish` 默认 false：流程停在"签署中"，不推 `SIGN_FLOW_COMPLETE`，下载报 `1437518`；
   要么发起时设 true，要么签完调 `POST /v3/sign-flow/{id}/finish`。
6. **默认不发任何通知。** `noticeTypes` 默认空串；要 e签宝发短信就传 `"1"`，否则自己用 sign-url 取链接发给签署人。
7. **回调验签和请求签名是两套算法。** 回调是 `hex(HmacSHA256(AppSecret, TIMESTAMP + query值 + 原始body))`；
   流程结束事件里 `signFlowStatus` 是字符串 `"2"`，撤销 / 拒签 / 过期也会推同一个 `SIGN_FLOW_COMPLETE`。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| --- | --- | --- |
| 算请求签名、Content-MD5，封装 Python / curl 客户端，沙箱与正式环境配置 | [auth-and-signing.md](references/auth-and-signing.md) | 公共请求头 · `GET /v1/oauth2/access_token`（不推荐） |
| 上传本地文件拿 fileId、轮询状态、关键字定位、合同模板填充生成文件 | [files-and-templates.md](references/files-and-templates.md) | `POST /v3/files/file-upload-url` · `GET /v3/files/{fileId}` · `POST /v3/files/create-by-doc-template` |
| 发起签署、设置签署方与签署区、取签署链接、查询、撤销、完结、下载 | [sign-flows.md](references/sign-flows.md) | `POST /v3/sign-flow/create-by-file` · `POST /v3/sign-flow/{id}/sign-url` · `GET /v3/sign-flow/{id}/detail` · `POST /v3/sign-flow/{id}/revoke` · `POST /v3/sign-flow/{id}/file-download-url` |
| 个人 / 机构实名认证、用户授权，查 psnId / orgId | [identity-authorization.md](references/identity-authorization.md) | `POST /v3/psn-auth-url` · `POST /v3/org-auth-url` · `GET /v3/persons/identity-info` · `GET /v3/organizations/identity-info` |
| 接收回调、验签、重试与幂等、事件对照 | [callbacks.md](references/callbacks.md) | e签宝 POST 到你的 Webhook / notifyUrl（头 `X-Tsign-Open-SIGNATURE`） |
| 错误码含义、各类限制、重试策略 | [errors-and-limits.md](references/errors-and-limits.md) | 网关 401 · 业务码 `1435xxx` / `1437xxx` / `1430xxx` / `1450xxx` |

本 skill 不覆盖：印章服务、企业机构成员、企业控制台、合同管理（数据推送）、账号管理、e签宝官网功能开放 API、流程模板的控件管理、
合同解约与出证、核验已签文件、审批、扫码签、身份核验认证服务、存证、OCR、合同比对、电子签名 SDK 3.0、混合云 / 医签宝。
这些文档在 https://open.esign.cn/doc/opendoc 首页"API文档"目录下（同一套签名规则）。

## House rules

- 先在沙箱联调；上线前在正式环境重建应用、白名单、模板，并按文档提前 2–3 天向 e签宝报备。
- 凭证只走环境变量（示例用 `ESIGN_APP_ID` / `ESIGN_APP_SECRET` / `ESIGN_HOST`）；OAuth 方式会把 secret 放进 URL，别用。
- 所有示例复用 auth-and-signing.md §5 的 `esign_request()`，不要每个接口重写签名。
- 先解析 JSON 再判断，按 `code` 分支，不按 `message` 文案；反序列化容忍新增字段。
- 时间字段一律毫秒时间戳；服务器做 NTP 校时。
- 签署进度以回调为主、`/detail` 兜底；回调接收端 5 秒内回 2xx，业务异步做，按事件去重（Webhook 与 notifyUrl 同时配置会推两次）。
- 签署链接、认证链接、下载链接都可能免登录访问，只发给对应的人，不写进日志。
- 创建类接口失败重试前先查是否已创建，避免重复发起签署。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

| 位置 | 问题 |
| --- | --- |
| sign-flows.md §15 | `signerType` 字段表 0/1/2/3，错误码表"只支持0或1"；文档示例 `signFlowExpireTime` 是无效时间戳；sign-url 的 `operator` 标必选却说可不传 |
| sign-flows.md §7 / callbacks.md §7 | `signFlowStatus` 详情接口是 int、回调是 string；`signFieldStatus` 字段表是 string |
| auth-and-signing.md §12 | POST 省略 Content-MD5 是否可行、业务失败的 HTTP 状态码未说明；公共响应表没写网关 401 的 `success` 字段 |
| auth-and-signing.md §11 | 换 token 失败的 `72000032` 不在任何错误码页（探测得到） |
| identity-authorization.md §10 | 错误码页把机构授权信息路径写成 `/v3/persons/{psnId}/authorized-info`；`redirectDelayTime` 类型两处不一致 |
| callbacks.md §10 | 回调时间戳有效窗口、重试间隔（只有图片）未说明；文档验签示例密钥已脱敏无法复现 |
| files-and-templates.md §9 | 字段 `docTemplateName` 与报错 `templateName不能为空` 不一致；关键字坐标与签章坐标的换算未抓取 |
| errors-and-limits.md §8 | 没有 QPS 数值；`SIMPLE_MODE_CANT_PASS` 含义未说明 |
