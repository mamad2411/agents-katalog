---
name: kingdee
description: 接入金蝶云星空（Kingdee K/3 Cloud，开放平台 open.kingdee.com）WebAPI 的使用手册——覆盖第三方系统登录授权签名与会话登录、ExecuteBillQuery 单据查询与分页、单据保存/提交/审核/下推/状态操作、物料客户供应商等基础资料与多组织分配、总账凭证与应收应付、返回结构与报错排查。只覆盖金蝶云星空（公有云与私有部署，接口路径含 /k3cloud/ 与 .common.kdsvc），不覆盖金蝶云星瀚、苍穹、星空旗舰版、精斗云、KIS、K/3 WISE。当用户提到"金蝶""金蝶云星空""K3Cloud""K/3 Cloud""k3cloud_webapi_sdk""kingdee.cdp.webapi.sdk""ExecuteBillQuery""kdsvc""FormId""第三方系统登录授权""X-KDApi-AcctID"，或要写代码对接金蝶 ERP 的物料、客户、供应商、订单、入库出库、凭证、应收应付时，应主动使用本技能，不要凭记忆编造签名算法、接口名、FormId 或字段标识。
---

# 金蝶云星空 WebAPI 接入指南

金蝶云星空是部署在客户服务器（或金蝶公有云租户）上的 ERP，WebAPI 以「一个 URL 模式 + 表单 FormId」操作所有单据和基础资料。
**本 skill 覆盖金蝶云星空（K/3 Cloud）WebAPI；不覆盖金蝶云星瀚 / 苍穹 / 星空旗舰版（文档在 dev.kingdee.com）、精斗云、KIS、K/3 WISE——它们的接口完全不同，别套用。**
**本页只做分流与规则，字段表和示例在 `references/`。**

## ⚠ 验证状态

文档版：内容整理自 <https://open.kingdee.com/k3cloud/open/ApiCenterReportDetail.aspx> 及同站 API 文档服务
（API 版本 7.5.1800.6，发布 2020-10-15；抓取于 2026-09-11）和官方 Python SDK `kingdee.cdp.webapi.sdk` 8.2.0 源码，
**未用真实凭证调用验证**。新版 API 中心 `openapi.open.kingdee.com` 与金蝶云社区文章需要登录，未抓取，新版文档可能有更新。
无凭证探测：只对已被 SDK 弃用的旧公网网关 `api.kingdee.com/galaxyapi` 发了 5 次请求（结果见 `auth-and-connection.md` §9），
客户服务器没有公开地址，业务接口本身没有测。拿到凭证后按 `kingdee-workspace/verification-plan.md` 补测；对照实验待凭证到位后进行。

## 当前事实

| 项 | 值 |
| :--- | :--- |
| Base URL | **客户自己的星空站点** `http(s)://<host>/k3cloud/`；所有接口 `POST {ServerUrl}/{ServiceName}.common.kdsvc`，JSON body |
| ServiceName 形态 | `Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.<操作>`（登录类在 `...AuthService.`） |
| 鉴权（推荐） | 第三方系统登录授权：每个请求带 9 个签名头 `X-Api-ClientID`、`X-Api-Auth-Version: 2.0`、`x-api-timestamp`、`x-api-nonce`、`x-api-signheaders`、`X-Api-Signature`、`X-Kd-Appkey`、`X-Kd-Appdata`、`X-Kd-Signature`；HMAC-SHA256 → **小写 hex → 再 base64** |
| 凭证 | 账套 ID（= 数据中心 ID）+ 集成用户名 + AppID（`<clientId>_<32位>`）+ AppSecret；语系 `lcid` 默认 2052 |
| 有效期 | 签名按秒级时间戳每次重算；过期窗口文档未说明（探测：13 分钟前的时间戳被网关判过期） |
| 官方 SDK | Python `pip install kingdee.cdp.webapi.sdk`（import `k3cloud_webapi_sdk`，8.2.0 起 ServerUrl 必填）；.NET / Java 在官方资料包 |
| 最容易选错 | 请求体外层：查询类 `{"data":{FormId,…}}`，写操作 `{"formid":"…","data":{…}}`；FormId 与字段 key 大小写不统一，逐字照抄 |
| 前置条件 | 星空补丁 ≥ PT136657【7.3.1310.2】，管理员在「系统管理 → 第三方系统登录授权」新增授权 |

## 照通用经验写容易错的地方（来自文档 / SDK 源码，未实测）

1. **没有公共 API 域名。** ServerUrl 是客户的星空站点；SDK 8.2.0 注释「取消默认旧网关，要求必须输入url」，老博客里的 `api.kingdee.com/galaxyapi` 不要当默认值。
2. **签名不是常见的 base64(HMAC)。** `X-Api-Signature` = base64(hex(HMAC-SHA256(待签串)))，密钥是 AppID 第二段经固定种子异或解码后的值（不是 AppSecret）；
   待签路径要把 `/` 也编码成 `%2F`，路径后是两个 `\n`。`X-KDApi-*` 是配置文件键名，不是请求头。直接用 SDK 最稳。
3. **ExecuteBillQuery 返回裸二维数组。** 没有字段名、没有 total、没有 `Result` 外壳；`FieldKeys` 是逗号分隔字符串不是数组；
   分页只有 `StartRow` + `Limit`（≤2000），返回行数 < Limit 才算翻完。
4. **改单默认会删掉没传的分录。** Save 的 `IsDeleteEntry` 默认 true；只改部分分录要显式传 false，并在 `NeedUpDateFields` 里连单据体 key 一起列上。
5. **保存 ≠ 生效。** Save、Submit、Audit 是三个接口；`Numbers` 要数组、`Ids` 要逗号分隔字符串；禁用 / 作废 / 关闭走 `ExcuteOperation`（拼写就没有 e）+ `opNumber`。
6. **基础资料引用写对象、跨组织要分配。** 单据里写 `{"FNumber": "编码"}`（键名随表单还有 `FNUMBER`、`FNAME`）；物料建在 A 组织、B 组织要用时调 `Allocate`（内码），不是再 Save 一次。
7. **成败看 `Result.ResponseStatus.IsSuccess`，网关错误是 HTTP 519。** 业务失败在 body 里（模板里 IsSuccess 是字符串 `"false"`）；公有云网关失败返回非标准 519 + `errcode`。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 配置第三方授权、生成签名头、SDK 初始化、会话登录 | [`auth-and-connection.md`](references/auth-and-connection.md) | `AuthService.ValidateUser`、`AccountService.GetDataCenterList` |
| 按条件查单据 / 基础资料、分页拉全量、查元数据 | [`bill-query.md`](references/bill-query.md) | `ExecuteBillQuery`、`View`、`QueryBusinessInfo` |
| 保存 / 提交 / 审核 / 删除单据，下推，禁用作废等状态操作 | [`bill-operations.md`](references/bill-operations.md) | `Save`、`Submit`、`Audit`、`Push`、`ExcuteOperation` |
| 物料、客户、供应商的新建同步、多组织分配、分组 | [`master-data.md`](references/master-data.md) | `Save`（`BD_MATERIAL` 等）、`Allocate`、`GroupSave` |
| 生成总账凭证，应收单 / 应付单 / 收款单 | [`finance-vouchers.md`](references/finance-vouchers.md) | `Save`（`GL_VOUCHER`、`AR_receivable`、`AP_Payable`） |
| 看懂返回结构、批量部分失败、网关 519、SDK 异常 | [`errors-and-responses.md`](references/errors-and-responses.md) | `Result.ResponseStatus`、网关 `errcode` |

本 skill 不覆盖：生产制造、PLM、质量、CRM、电商分销等子系统的逐字段说明（942 个 FormId 清单来自官方 API 文档树，
各表单操作说明在 open.kingdee.com「API文档」与需登录的 openapi.open.kingdee.com/ApiDoc）；报表 `GetSysReportData`、附件上传下载、消息 `SendMsg`
（SDK 有方法名，文档未收录参数）；星空旗舰版 / 星瀚 / 苍穹（dev.kingdee.com）、精斗云、KIS。

## House rules

- **优先用官方 SDK**（Python `k3cloud_webapi_sdk`，或资料包里的 .NET / Java）；不用 SDK 时照 `auth-and-connection.md` §5 逐步实现签名。新对接不要用 ValidateUser 账号密码。
- 凭证只走环境变量：`KD_SERVER_URL`、`KD_ACCT_ID`、`KD_USERNAME`、`KD_APP_ID`、`KD_APP_SECRET`（可选 `KD_LCID`、`KD_ORG_NUM`）。
- SDK 返回的是字符串，自己 `json.loads`；SDK 未初始化时**返回**异常对象而不抛出，调用前检查 `sdk.initialize`。
- 每个写操作都检查 `Result.ResponseStatus.IsSuccess`（兼容字符串），失败把 `Errors[].FieldName / Message / DIndex` 原文写日志；没有错误码表，不要 `switch(ErrorCode)`。
- 组织、币别、单据类型、凭证字、计量单位、科目的**编码因账套而异**，先用 ExecuteBillQuery 查，不要把示例编码写死。
- 字段 key、FormId、opNumber 逐字照抄官方模板（大小写不统一）；客户二开字段用 `QueryBusinessInfo` 查。
- 同步顺序：先基础资料（Save→Submit→Audit→Allocate），再单据；上下游关联用 `Push`，不要用 Save 拼下游单。
- 批量写按 `DIndex` 处理部分失败，只重发失败项。
- SDK 关闭了 HTTPS 证书校验（`verify=False`），对安全有要求时自己发请求。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

**自相矛盾**
- 布尔参数说明写「布尔类型」，JSON 模板里是字符串 `"true"/"false"`（所有 Save 类接口）→ `bill-operations.md` §3
- `WorkflowAudit.Ids` 说明为字符串、模板为数组；`Allocate.PkIds` 说明为字符串、模板为数字；`PkEntryIds` 说明为字符串、模板为数组 → `bill-operations.md` §7 §9、`master-data.md` §2
- `View.CreateOrgId` 说明为字符串、模板为整数 → `bill-query.md` §5
- `GroupFieldKey` 同时写「必录」和「不填时取默认」→ `master-data.md` §7、`bill-query.md` §7
- Push 备注提到 `ConvertResponseStatus`，返回模板里没有 → `bill-operations.md` §8
- QueryBusinessInfo / WorkflowAudit 返回模板括号不配对 → `errors-and-responses.md` §5
- 物料字段说明标了 30 多个必填项，SDK 官方示例只传 4 个；SDK 示例写 `FUserOrgId`，模板写 `FUseOrgId` → `master-data.md` §3
- QueryGroupInfo 文档要外层 formid，SDK 不发 → `bill-query.md` §7
- 安装命令三处不一（PyPI 包名 / PyPI 描述 / SDK 介绍页）→ `auth-and-connection.md` §4

**文档未说明**
- ExecuteBillQuery：`FilterString` / `OrderString` 语法、`StartRow` 起点、`Limit` 默认值与超限行为、失败时返回结构、`.FNumber` 点号取值 → `bill-query.md` §3 §4
- Save：Id=0 是否即新建、同编码重复新建的行为、`FDocumentStatus` 枚举、日期时间格式、引用键名是否大小写敏感 → `bill-operations.md` §3 §4
- 凭证：`FVOUCHERGROUPNO` / `FDocumentStatus` 必填但取值规则未说明、`FDETAILID__FFLEXn` 与核算维度的映射、金额单位、无过账接口 → `finance-vouchers.md` §3–§5
- `ValidateUser` 的 HTTP body 形态与 `LoginResultType` 枚举；`GetDataCenterList` 返回结构 → `auth-and-connection.md` §7 §8
- 错误码 `ErrorCode` / `MsgCode` 取值表、限流规则、批量条数上限、业务失败时的 HTTP 状态码 → `errors-and-responses.md` §4 §8
- 网关时间戳容忍窗口；带伪造 `X-Api-ClientID` 仍报「应用ID为空」的原因 → `auth-and-connection.md` §9
- SDK 独有接口（BillQuery、QueryAsyncResult 异步轮询、FlexSave、SwitchOrg、附件等）不在 2020 版文档里 → `bill-query.md` §8、`bill-operations.md` §5 §11
