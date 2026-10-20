---
name: fxiaoke
description: 接入纷享销客 CRM 开放平台（open.fxiaoke.com / developer.fxiaoke.com，Fxiaoke / ShareCRM OpenAPI）的 API 使用手册（文档版）——涵盖企业自建应用换 accessToken 与旧版 corpAccessToken、新旧两代公共参数（authorization Bearer + x-fs-ea + x-fs-userid 与 corpAccessToken / corpId / currentOpenUserId）、按所在云选域名、客户 / 联系人 / 线索 / 商机等预置对象与 __c 自定义对象的增删改查、公海与线索池、对象描述与字段值格式、search_query_info 查询条件与深翻页、通讯录（部门 / 人员 / 用户组 / 角色）、企信消息推送、错误码与限流。当用户提到"纷享销客""纷享""fxiaoke""ShareCRM""纷享 OpenAPI""corpAccessToken""AccountObj""LeadsObj""__c 自定义对象""x-fs-ea"，或要写代码同步纷享 CRM 数据、把 ERP / 数据仓库和纷享打通、给纷享员工发消息时，应主动使用本技能，不要凭记忆编造接口路径、对象 apiName、字段值格式，也不要套用 Salesforce、钉钉、企业微信的接口习惯。
---
# 纷享销客 CRM 开放平台接入指南

纷享销客（Fxiaoke / ShareCRM）的 OpenAPI：企业自建应用换 token 后，读写客户 / 联系人 / 线索 / 商机等预置对象和 `__c` 自定义对象、
查通讯录、给员工发企信消息。**本页只做分流与规则，字段表和示例在 `references/`。**

## ⚠ 验证状态

文档版：内容整理自 https://developer.fxiaoke.com/openapi_v2/ （新版文档站）和 https://open.fxiaoke.com/open/openindex/wiki.html
（旧版 wiki）（抓取于 2026-09-11），**未用真实凭证调用验证**。

- **无凭证探测（2026-09-11，共 10 次）**：两个换 token 入口；业务接口在「无鉴权 / 伪造新版 header / 伪造旧版 body」下的返回；
  `www.fxiaoke.com` 是否可当 API 域名；华为云域名。结论写在各 reference 里，明细见 `fxiaoke-workspace/probe-log.md`。
- 文档全部公开可读，**没有需要登录才能看的部分**；站点没有 llms.txt / sitemap / OpenAPI 规范，字段表来自渲染后的页面正文。
- 除标「无凭证探测」的条目外，所有报错、默认值、行为都是**文档原文，未实测**。对照实验待真实凭证到位后进行。
- 拿到凭证后按 `fxiaoke-workspace/verification-plan.md` 补测。

## 当前事实

| 项 | 值 |
| :--- | :--- |
| Base URL | 纷享云 `https://open.fxiaoke.com`；其他云 `open-<云登录域名>`（华为云 `open-hwcloud.fxiaoke.com` 等，见 `auth.md`）。**`www.fxiaoke.com` 不是 API 网关**（探测返回 302 HTML） |
| 换 token | `POST /oauth2.0/token?thirdTraceId=<uuid4>`，body `{"appId","appSecret","permanentCode","grantType":"app_secret"}` → `accessToken` + `ea` |
| 调用鉴权 | header `authorization: Bearer <accessToken>`（Bearer 后一个空格）+ `x-fs-ea: <ea>` + `x-fs-userid: <CRM 员工ID，如 1000>` |
| 每个请求 | URL 带 `?thirdTraceId=<RFC 4122 UUID v4>`，每次不同；一律 `POST` + `application/json` |
| token 有效期 | 7200 秒；0–6600 秒内重复获取返回同一个；换 token 接口每分钟 ≤10 次且**不能并发** → 必须缓存 |
| 最容易选错 | 对象路径：预置对象（`AccountObj` 等）走 `/cgi/crm/v2/data/*`；apiName 以 **`__c`** 结尾的自定义对象走 `/cgi/crm/custom/v2/data/*` |
| 响应 | 出错也是 **HTTP 200**（探测证实），判 `errorCode == 0`；不要用 `errorMessage` 判断 |

## 照通用经验写容易错的地方（来自文档，未实测）

1. **两代传参不能混用。** 新版：token 放 header `authorization: Bearer`，企业放 `x-fs-ea`，操作人放 `x-fs-userid`（CRM 员工 ID `1000`）。
   旧版：body 顶层放 `corpAccessToken` + `corpId` + `currentOpenUserId`（`FSUID_…`）。操作人决定数据权限，查不到 / 没权限先查它（`auth.md`）。
2. **预置对象和自定义对象是两套路径。** `__c` 对象用 `/cgi/crm/custom/v2/data/*`，批量作废还是没有 v2 的 `/cgi/crm/custom/data/invalid`。
   create / update 的 `dataObjectApiName` 放在 `data.object_data` **里面**，get / query 放在 `data` 下（`custom-objects.md`）。
3. **分页有三道硬限制。** `limit` ≤100；`offset` 必须是 limit 的整数倍（是偏移量不是页码）；`offset` ≤10000。
   超 1 万条改用 `_id` 升序 + `_id GT 上一页最后一条` + `offset 0` 的游标翻页（`query-and-paging.md`）。
4. **字段值类型和直觉不同。** 数字 / 金额传**字符串** `"100.01"`；日期传毫秒时间戳 Long；单选传 describe 里 `options.value` 不是 label；
   员工 / 部门字段即使单选也是**列表** `["1000"]`；过滤条件 `field_values` 必须是列表（`objects-and-fields.md`）。
5. **删除是两步，负责人不能 update。** 先 `invalid`（作废，单条 `object_data_id`），再 `delete`（`idList`）；改负责人只能 `changeOwner`（`data.Data[]`，大写 D）；
   公海 / 线索池里的数据先 `choose` 领取，否则谁都没权限（`crm-preset-objects.md`）。
6. **写入默认触发审批流和工作流。** `triggerApprovalFlow` / `triggerWorkFlow` 不传就是 true，批量导入会刷出一堆审批和通知，显式传 false。
7. **错误码表和实际返回对不上。** 探测：appSecret 错误实际回 `10006`（码表写的是「缺少参数scope」），缺鉴权实际回 `20017`（码表写 corpId 未找到）。
   只信 `0` 成功、`20016` token 失效；其余统一记 `errorCode` + `traceId` 处理（`errors-and-limits.md`）。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 拿 token、设置公共 header、选所在云域名、授权码 / 应用免登 | [`auth.md`](references/auth.md) | `POST /oauth2.0/token`、`GET /oauth2.0/authorize`、`POST /cgi/corpAccessToken/get/V2` |
| 查企业有哪些对象、字段 apiName 与类型、字段值怎么填、上传附件 / 图片 | [`objects-and-fields.md`](references/objects-and-fields.md) | `POST /cgi/crm/v2/object/list`、`/cgi/crm/v2/object/describe`、`/cgi/crm/v2/generatorFileUploadCredential` |
| 写查询条件、分页、深翻页、取总数、增量拉取 | [`query-and-paging.md`](references/query-and-paging.md) | `POST /cgi/crm/v2/data/query`、`/cgi/crm/custom/v2/data/findSimple` |
| 客户 / 联系人 / 线索 / 商机增删改查、改负责人、公海与线索池、相关团队、锁定 | [`crm-preset-objects.md`](references/crm-preset-objects.md) | `POST /cgi/crm/v2/data/create|get|update|invalid|delete|changeOwner|choose|return` |
| `__c` 自定义对象增删改查 | [`custom-objects.md`](references/custom-objects.md) | `POST /cgi/crm/custom/v2/data/*`、`/cgi/crm/custom/data/invalid` |
| 通讯录：部门、员工、用户组、角色 | [`org-directory.md`](references/org-directory.md) | `POST /cgi/user/list`、`/cgi/user/simpleList`、`/cgi/crm/v2/special/usergroupList` |
| 给员工发企信 / 服务号消息、ERP 数据推送、事件回调现状 | [`messaging.md`](references/messaging.md) | `POST /cgi/message/send`、`/cgi/app/message/revoke`、`/cgi/crm/erp/syncdata/objdata/push` |
| 错误码、限流与配额、权限类报错排查 | [`errors-and-limits.md`](references/errors-and-limits.md) | 全局（返回码表、100 次 / 20 秒） |

本 skill 不覆盖：审批流 / 业务流 / 阶段推进（`/cgi/crm/v2/special/*`、`/cgi/crm/approvalInstance/*`）、工单 / 库存 / 财务 / 订单等其余 40 多类预置对象
（读写方式同 `crm-preset-objects.md`，只换 apiName）、考勤外勤、BI、网盘文件、离线数据下载、客户端 JS API / UI 组件、纷享免登（SAML）。
文档在 https://developer.fxiaoke.com/openapi_v2/ 的「通用接口」「业务对象接口」。
**CRM 数据变更的事件回调 / 订阅：新旧公开文档都没有接口说明**，不要编造；替代方案是按 `last_modified_time` 增量轮询（`messaging.md` 第 6 节）。

## House rules

- 凭证只走环境变量：`FXK_APP_ID`、`FXK_APP_SECRET`、`FXK_PERMANENT_CODE`、`FXK_USER_ID`、`FXK_HOST`。不打印 token。
- **写代码前先调 `object/list` + `object/describe`**，拿准确的对象 / 字段 apiName 和 `type`，不要凭中文名或别家 CRM 的字段名猜。
- 官方文档没有提供 SDK；示例用 `requests`，统一封装一个客户端（`auth.md` 第 10 节的 `FxkClient`）：缓存 token、每次新 UUID、判 `errorCode`、20016 刷新重试一次。
- `x-fs-userid` 用有权限的员工（通常是 CRM 管理员）；人员对象（PersonnelObj）连管理员也要额外配共享规则（`org-directory.md`）。
- 限流：单接口 **100 次 / 20 秒**，每日总量按购买的资源包；`30002`（当日超限）/ `30003`（没买配额）重试没用，要找企业管理员。
- 写创建类代码前先问用户：应用是否已开启开发模式、服务器 IP 是否在白名单、企业是否购买了 OpenAPI 配额——这些不是参数错误，代码绕不过去。
- 文档自相矛盾的地方（下方汇总）写代码时做兜底（例如列表响应同时兼容 `data.dataList` 和单条 map），首次真实调用时打印原始响应核对。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

探测证实的文档错误在 reference 里用 `<!-- Gap: … -->` 标记（3 处，可 grep）：
- `www.fxiaoke.com/cgi/...`（文档示例域名）实际返回 302 HTML，不是 API 网关（`auth.md` 第 2 节）
- appSecret 缺失 / 非法实际返回 10006，码表不符（`errors-and-limits.md` 第 2 节）
- 缺鉴权实际返回 20017「corpAccessToken为必填项」，码表不符（`errors-and-limits.md` 第 2 节）

未实测的 ⚠（每份 reference 末尾都有本文件的清单）：
- 「是否返回总数」有三种参数名：`returnTotalNum` / `find_explicit_total_num` / `need_return_count_num`（`query-and-paging.md` 第 6 节）
- 列表查询响应是单条 map 还是 `data.dataList`；offset 超限错误码 10013 与码表冲突（`query-and-paging.md` 第 4、7 节）
- `convertUserId` / `convertMediaId` 默认值表述含混；员工字段填员工 ID 还是 FSUID（`auth.md` 第 3 节、`objects-and-fields.md` 第 4 节）
- changeOwner 的 `ownerId` 是 `"[1000]"` 还是 `["1000"]`；自定义对象 changeOwner 参数表 `idList` vs `Data[]`（`crm-preset-objects.md` 第 6 节、`custom-objects.md` 第 9 节）
- 自定义对象创建不返回 `dataId`（示例里没有）；多个页面的参数说明是从别的页面复制的（`custom-objects.md`）
- 客户对象的「查询」页实为公海对象、「删除」页实为费用明细对象（`crm-preset-objects.md` 第 5.2 节）
- 「服务号发消息」页参数是撤回接口的复制品；事件回调无文档（`messaging.md` 第 5、6 节）
- 云域名标签新旧版不一致；授权码 redirectUrl 对齐哪个配置项（`auth.md` 第 2、6 节）
