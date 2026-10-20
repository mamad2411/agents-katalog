---
name: qiyuesuo
description: 接入契约锁电子签章开放平台（正式 openapi.qiyuesuo.com、测试 openapi.qiyuesuo.cn，文档 open.qiyuesuo.com）的 API 使用手册——涵盖 x-qys-open-* 请求头与 MD5(AppToken+AppSecret+timestamp+nonce) 签名、合同草稿与合同文档（本地文件 / 云平台模板）、业务分类、发起合同与签署位置、公章 / 法人章 / 审批静默签、签署页面链接、撤回删除与作废、印章管理、企业与个人认证、合同状态回调与加密回调、错误码与频次限制。当用户提到"契约锁""qiyuesuo""QYS""电子签章开放平台""x-qys-open-accesstoken""AppToken AppSecret""/v2/contract/draft""业务分类""companysign""pageurl"，或要写代码对接契约锁创建合同、盖章、获取签署链接、处理合同回调时，应主动使用本技能，不要凭记忆编造签名算法和接口路径，也不要套用法大大、e签宝、上上签、DocuSign 的接口习惯。
---
# 契约锁开放平台接入指南

契约锁（上海亘岩网络）电子签章的服务端 OpenAPI：静态 AppToken + AppSecret，每个请求带四个 `x-qys-open-*` 头，签名是四段拼接的 MD5；
核心对象是"合同"（草稿 → 合同文档 → 签署方 / 签署动作 → 发起 → 签署），大量默认行为由云平台上的"业务分类"决定。
**本页只做分流与规则，字段表和示例在 references/。**

## ⚠ 验证状态

文档版：内容整理自 https://open.qiyuesuo.com/document （经文档站自己的 `/api/doc/info`、`/api/doc/<nodeId>` JSON 接口抓取全部 133 个页面，抓取于 2026-09-11），
辅以下载中心 SDK 版本表和 GitHub `qiyuesuo/jssdk-server`、`qiyuesuo/sdk-python-sample` 源码，**未用真实凭证调用验证，也没有收到过真实回调**。
无凭证探测了 8 组请求（每组复跑两次）：测试 / 正式环境伪造 token、缺鉴权头、缺 nonce、过期时间戳、不存在的路径、示例里出现的第三个域名——结果见 auth-and-signing.md §8、errors-and-limits.md §2。
拿到凭证后按 `qiyuesuo-workspace/verification-plan.md` 补测；有 / 无 skill 的对照实验待真实凭证到位后进行。

## 当前事实

| 项 | 值 |
| --- | --- |
| Base URL | 测试 `https://openapi.qiyuesuo.cn`；正式 `https://openapi.qiyuesuo.com`（两者均探测到在线）。路径有 `/v2/…`、`/v3/…` 和无版本前缀的（`/companyauth/…`、`/company/…`），逐个照接口列表写 |
| 鉴权头 | `x-qys-open-accesstoken`（AppToken）、`x-qys-open-timestamp`（毫秒）、`x-qys-open-nonce`（UUID，10 分钟内不可重复）、`x-qys-open-signature` |
| 签名 | `md5_hex(AppToken + AppSecret + timestamp + nonce)`，直接拼接、不签 URL 和 body；没有换 token 接口，AppToken 不过期 |
| 请求体 | JSON 接口 `application/json`；上传文件接口（`/v2/document/addbyfile` 等）是 `multipart/form-data` |
| 成功判定 | 文档两种写法：`responseCode == "00000000"` / `code == 0`。探测：错误响应两个字段都有，且 HTTP 状态码 = code（441 缺头、442 token 无效） |
| 最容易选错的字段 | 签署位置绑定：公司位置填 `actionId`（签署节点 ID），个人位置填 `signatoryId`，都来自创建草稿的返回；坐标是 0–1 的相对值、原点在页面**左下角** |

## 照通用经验写容易错的地方（来自文档，未实测）

1. **签名不是 HMAC，也不覆盖请求内容。** 就是 `MD5(AppToken + AppSecret + timestamp + nonce)`；每个请求现生成 timestamp 和 nonce。文档接口示例大多漏了 `x-qys-open-nonce`（⚠ 与 API协议页矛盾），照协议页四个头都发。SDK 新版支持 HmacSha256，但文档站没写规则，手写请求别猜。
2. **合同要"草稿 → 加文档 → 发起"三步。** `POST /v2/contract/draft`（`send: false`）→ `/v2/document/addbyfile`（multipart）或 `/addbytemplate` → `/v2/contract/send`。只有草稿能加文档；`send: true` 一步发起要求业务分类里已有模板，否则 `1401`。
3. **业务分类会覆盖你的参数。** 分类"预设签署方"时，传入的签署方数量、类型、顺序必须与配置完全一致（`1301`）；不传 `category` 用默认分类。模板、印章只认云平台上的，开放平台控制台的旧模板会报"模板 Id 无效"。
4. **接口只能替自己公司签。** 发起方（及子公司）的公章、法人章、审批可用接口静默签；经办人签字节点和所有接收方都得打开签署页面（`/v2/contract/pageurl`，要传签署人 `user`，默认 30 分钟有效，可设到 90 天）。
5. **撤回、删除、作废是同一个接口。** `POST /v2/contract/invalid` 按状态决定：草稿删除、签署中撤回、已完成发起作废（所有方签完作废文件才生效，发起方没签过时要传 `sealId`）。不存在 `/cancel`、`/revoke`。
6. **回调是表单 POST，会反复推。** 合同回调失败后再推 7 次（5 分钟、2 小时 ×4、12 小时、24 小时），必须幂等；`callbackType` 的枚举、返回体、验签方式文档都没写（⚠），拿 `contractId` 回查 `/v2/contract/detail` 为准。
7. **下载有锁。** 同一文档 25 分钟内连续下载 10 次锁 12 小时（叠加）；`/v2/contract/download` 默认给 ZIP，要 PDF 用 `/v2/document/download?documentId=`。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| --- | --- | --- |
| 生成 x-qys-open-* 签名头、封装请求、选环境、查应用信息 | [auth-and-signing.md](references/auth-and-signing.md) | 所有接口的请求头 · `GET /company/token/get` |
| 建合同草稿、上传文件 / 用模板生成文档、发起、查详情、下载 | [contracts.md](references/contracts.md) | `POST /v2/contract/draft` · `POST /v2/document/addbyfile` · `POST /v2/document/addbytemplate` · `POST /v2/contract/send` · `GET /v2/contract/detail` |
| 签署位置、公章 / 法人章静默签、签署链接、催签、撤回与作废 | [signing.md](references/signing.md) | `POST /v2/contract/companysign` · `POST /v2/contract/pageurl` · `POST /v2/contract/invalid` |
| 印章查询与创建、帮客户做企业认证 / 个人认证 | [seals-and-company-auth.md](references/seals-and-company-auth.md) | `GET /v2/seal/list` · `POST /v2/seal/autocreate` · `POST /companyauth/pcpage` · `POST /v2/personalauth` |
| 接收合同状态回调、解密、认证 / 印章回调、改回调地址 | [callbacks.md](references/callbacks.md) | 契约锁 POST 表单到你的地址 · `POST /company/token/update/callback` |
| 错误码含义、鉴权报错、频次限制、有效期 | [errors-and-limits.md](references/errors-and-limits.md) | 全局码 `0/1001/1002/1005/1601`、`1101`–`1705`、8 位码 `11011101` 等 |

本 skill 不覆盖：组织架构（员工 / 角色 / 子公司邀请）、模板创建与编辑（`/v3/template/createbyword` 等）、存证与出证（`/v2/chain/notary`、`/chain/evidence/*`）、外部客户、授权管理（单点登录、个人签名授权页）、费用查询、信息校验与 OCR、单点登录集成、小程序插件、APP SDK、JS-SDK。
这些接口的鉴权方式相同，文档在 https://open.qiyuesuo.com/document/2725986623018775399 （接口列表）对应分组下。

## House rules

- 先在测试环境（`openapi.qiyuesuo.cn`）联调，上线换 `openapi.qiyuesuo.com`；两套环境的 AppToken、业务分类 ID、模板 ID、印章 ID 互不通用。私有化部署的地址文档未说明，别套公有云域名。
- AppToken / AppSecret 只从环境变量读，只放服务端；需要示例代码时复用 auth-and-signing.md §4 的 `qys_call`，不要每个接口重写一遍签名。
- 先解析 JSON，再看 HTTP 状态；成功判定 `code == 0 or responseCode == "00000000"`。
- 合同、文档、签署方、节点、印章 ID 都是 19 位长整数，在 JS / JSON 前端里当字符串处理。
- 每份合同传 `bizId` 作为你方业务键（草稿态重复 bizId 会覆盖原草稿）；以子公司身份发起的合同，用 bizId 定位时要带 `tenantName`。
- 签署进度以回调为主、`/v2/contract/detail` 兜底；签完落盘一次，别反复下载。
- 签署 / 认证链接只发给本人，别经聊天软件转发测试（认证链接只能打开一次）。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

| 位置 | 问题 |
| --- | --- |
| auth-and-signing.md §3 | API协议页要求四个头，接口示例只有三个（缺 nonce）；时间戳偏差窗口未说明 |
| auth-and-signing.md §7 | SDK 已支持 HmacSha256 鉴权，文档站无任何说明 |
| auth-and-signing.md §8 | 返回参数有的页只写 `responseCode`(String)、有的只写 `code`(Integer)；探测显示两者并存且 HTTP 状态 = code（Gap） |
| contracts.md §2 | Action 印章 / 操作人字段：参数表 `corpSealIds`/`corpOperators`，示例 `operators`/`sealId`；`send` 默认值未写 |
| contracts.md §3、§5 | multipart 下 `stampers` 编码方式未说明；`addbyfiles` 示例多出 `fileSuffix` |
| signing.md §6 | 签署链接有效期 30 分钟（接口页）vs 10 分钟（FAQ） |
| signing.md §8、§9 | add / edit 示例路径写成 `/modify`；`invalid` 对已撤回 / 已退回 / 已截止合同的行为两页说法不同 |
| seals-and-company-auth.md §6、§7 | 企业认证状态码三套口径；人脸模式 `FACE` vs `FACEID` |
| callbacks.md §2、§3、§6 | 合同回调 `callbackType` 枚举"见后方列表"但没有列表；返回体、验签、加密字段与 CBC IV 均未说明；个人签名授权回调的 secretKey 来源未说明 |
| errors-and-limits.md §2、§3 | 4 位码与 8 位码两套并存；鉴权错误 441/442 不在任何错误码表里（Gap）；QPS 限制未公布 |
