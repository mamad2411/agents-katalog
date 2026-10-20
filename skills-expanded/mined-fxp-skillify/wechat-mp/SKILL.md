---
name: wechat-mp
description: 接入微信公众平台服务端 API（developers.weixin.qq.com/doc/service/，域名 api.weixin.qq.com）的接入手册——涵盖 access_token 获取与稳定版接口、用户管理（关注者列表、用户信息、标签、黑名单）、被动回复消息与客服消息、模板消息与订阅通知、自定义菜单、网页授权（OAuth2.0）、服务器配置与消息加解密、全局错误码与调用限额。当用户提到"微信公众号""微信服务号""公众号开发""微信客服消息""模板消息""订阅通知""自定义菜单""网页授权""snsapi_base""snsapi_userinfo""access_token""api.weixin.qq.com""mp.weixin.qq.com"，或要写代码调用上述任意能力、接收微信服务器推送的消息与事件时，应主动使用本技能，不要凭记忆混淆模板消息与订阅通知、snsapi_base 与 snsapi_userinfo、或误用小程序/企业微信/微信支付的接口习惯。
---

# 微信公众平台 接入指南

微信公众平台（developers.weixin.qq.com/doc/service/）是运营者通过服务号/公众号为微信用户提供资讯和服务的平台，服务端 API 统一挂在 `api.weixin.qq.com`。
本 skill 覆盖运营与开发最常接的 8 块：鉴权、用户管理、消息与客服消息、模板消息与订阅通知、自定义菜单、网页授权、服务器配置与消息推送、错误码与限流。
**本页只做分流与规则，字段表和示例在 references/。**

## ⚠ 验证状态

文档版：内容整理自 https://developers.weixin.qq.com/doc/service/（服务号文档，抓取于 2026-09-17），页面为服务端渲染 HTML，用 `id="docContent"` 节点转换为 Markdown 得到，**未用真实凭证调用验证**。
无凭证探测（只用伪造的 `appid`/`secret`/`access_token`）做了 18 次：换 token 接口对伪造 appid/secret 的报错、10 余个只读与写接口对伪造 access_token 的报错格式、网页授权两个端点对伪造 appid/code/token 的报错（明细见 `references/errors-and-limits.md` 第 2 节与 `wechat-mp-workspace/probe-log.md`）。
消息推送签名与 AES 加解密流程未做离线校验（文档未附带可复现的测试向量，见 `references/events.md` 的 ⚠）。对照实验待真实凭证到位后进行；拿到凭证后按 `wechat-mp-workspace/verification-plan.md` 补测。

## 当前事实

| 项 | 值 |
| :--- | :--- |
| Base URL | `https://api.weixin.qq.com`；网页授权跳转页在 `https://open.weixin.qq.com`；管理后台与一次性订阅授权链接在 `https://mp.weixin.qq.com` |
| 鉴权 | 查询参数 **`?access_token=<token>`**，不是 Authorization 头（无凭证探测证实：不带该参数返回 `41001 access_token missing`，不是 401） |
| 换 token | `GET /cgi-bin/token?grant_type=client_credential&appid=&secret=`，7200 秒；官方现推荐 `POST /cgi-bin/stable_token`（JSON body），**与旧接口的 token 互相隔离**（文档原文，两者不共享缓存） |
| 成功判定 | **HTTP 200 + 响应体 `errcode`（数字）等于 0** 才算成功；出错也是 HTTP 200（无凭证探测：18 次伪造请求全部 HTTP 200，业务错误码在 JSON 里） |
| 最容易选错 | 网页授权 `scope` 只有 `snsapi_base`（静默、仅拿 openid）与 `snsapi_userinfo`（需用户手动同意、能拿昵称头像）两种；网页授权拿到的 `access_token` 与 `cgi-bin` 系列的全局 access_token 是**两套不同 token**，不能混用 |
| 文档站现状 | 旧版 `developers.weixin.qq.com/doc/offiaccount/...` 路径已下线重定向；文档拆分为「服务号」`/doc/service/`（本 skill 依据）与「公众号（原订阅号）」`/doc/subscription/`，两者共享同一套 `api.weixin.qq.com` 服务端接口，差异主要是账号认证/类型对功能的开通门槛，不是接口协议本身的差异（文档原文，`references/auth.md` 有说明） |

## 照通用经验写容易错的地方（来自文档，未实测；标 ⚠ 的另见 references 末节）

1. **token 只能放 URL 查询参数，绝不能放 Authorization 头或 JSON body。** 无凭证探测证实：缺 `access_token` 参数返回 `41001`；给一个格式正常但伪造的 token 返回 `40001 invalid credential`，报错文案里明确建议改用 `getStableAccessToken`——这是探测中发现的、文档本身没强调的实际行为提示。
2. **两套换 token 接口的 token 互相隔离，不能"一个刷新、两边用"。** `GET /cgi-bin/token`（旧）与 `POST /cgi-bin/stable_token`（新，推荐）各自维护自己的 access_token，混用刷新逻辑会导致某一边意外失效。二选一，不要都调。
3. **消息推送三选一（明文/兼容/安全模式）与三套下发消息的接口不是一回事，容易被一起搞混：** 被动回复（收到用户消息后 5 秒内同步回复，走 XML，见规则 6）、客服消息（异步，`POST /cgi-bin/message/custom/send`，见 4）、模板消息/订阅通知（主动推送营销/服务通知，见 `references/template-subscribe.md`）三者触发条件、时间窗口、消息格式完全不同，不能因为都叫"发消息给用户"就混用同一段代码。
4. **客服消息有时间窗口和条数限制，`errcode=0` 不代表用户在窗口内。** 用户主动发消息触发的窗口是 **48 小时内最多 5 条**；点击菜单/关注/扫码触发的窗口是 **1 分钟内最多 3 条**，且各场景配额独立、不叠加（点菜单不会顺带产生"用户发消息"场景的配额）。超窗口调用客服消息接口是否报错、报什么错，文档未明确说明，标 `⚠ 文档未说明`，见 `references/messaging.md`。
5. **模板消息与订阅通知不是一回事，也不是新旧替代关系那么简单：** 模板消息（`/cgi-bin/message/template/send`）面向已关注用户、按行业类目选模板；订阅通知（`/cgi-bin/message/subscribe/bizsend`）需用户在图文/网页里主动点击订阅组件，分"一次性订阅"和仅开放给政务民生/医疗类目的"长期订阅"；另外还有更早的、需要引导用户跳转 `mp.weixin.qq.com` 专属链接完成单次订阅的"一次性订阅消息"（`/cgi-bin/message/template/subscribe`，不同接口路径）。三者当前并存，文档写"服务号订阅通知功能开启灰度测试，模板消息能力可正常使用"，具体分界线未来会调整，写代码前先确认账号后台实际开放了哪个。
6. **被动回复必须在 5 秒内同步返回，超时或格式错误会让用户看到系统提示"该服务号暂时无法提供服务"。** 微信服务器 5 秒收不到响应会重试，最多重试 3 次；处理不完就直接回复字符串 `success` 或空串（不是 JSON），耗时逻辑改用客服消息异步下发。重试消息去重：普通消息用 `MsgId`，事件消息推荐 `FromUserName + CreateTime`。
7. **回调不校验来源就处理消息 = 安全洞。** 服务器配置（Token/EncodingAESKey）用于校验推送确实来自微信：GET 接入校验用 `signature`（sha1(sort(token,timestamp,nonce))），安全模式下消息体加解密的验签字段是 `msg_signature`（多算一个 `Encrypt` 参与排序），两者不可混用；AES 密钥固定用 `Base64Decode(EncodingAESKey + "=")`。细节见 `references/events.md`。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 换取 / 刷新 access_token，配置 IP 白名单，排查回调连通性 | [`auth.md`](references/auth.md) | `GET /cgi-bin/token`、`POST /cgi-bin/stable_token`、`GET /cgi-bin/getcallbackip`、`GET /cgi-bin/get_api_domain_ip` |
| 拉关注者列表、查用户信息、打标签、拉黑/取消拉黑、账号迁移转 openid | [`users.md`](references/users.md) | `GET /cgi-bin/user/get`、`GET /cgi-bin/user/info`、`POST /cgi-bin/tags/*`、`POST /cgi-bin/tags/members/*blacklist` |
| 接收用户消息与事件、5 秒内被动回复、发客服消息、管理客服账号与会话、群发图文 | [`messaging.md`](references/messaging.md) | 被动回复 XML、`POST /cgi-bin/message/custom/send`、`POST /cgi-bin/message/mass/sendall` |
| 发模板消息 / 订阅通知（一次性或长期）、选类目选模板 | [`template-subscribe.md`](references/template-subscribe.md) | `POST /cgi-bin/message/template/send`、`POST /cgi-bin/message/subscribe/bizsend`、`GET /wxaapi/newtmpl/gettemplate` |
| 创建 / 查询 / 删除自定义菜单与个性化菜单，处理菜单点击事件 | [`menu.md`](references/menu.md) | `POST /cgi-bin/menu/create`、`GET /cgi-bin/menu/get`、`POST /cgi-bin/menu/addconditional` |
| 网页静默/用户信息授权登录，snsapi_base 与 snsapi_userinfo 怎么选 | [`oauth.md`](references/oauth.md) | `GET https://open.weixin.qq.com/connect/oauth2/authorize`、`GET /sns/oauth2/access_token`、`GET /sns/userinfo` |
| 配置服务器 URL/Token/EncodingAESKey，接入校验，明文/兼容/安全模式，事件类型 | [`events.md`](references/events.md) | 接入校验 GET、消息推送 POST（XML/JSON）、AES-256-CBC 加解密 |
| 解读全局错误码，查/清零调用配额，处理限频 | [`errors-and-limits.md`](references/errors-and-limits.md) | 全局错误码表、`POST /cgi-bin/clear_quota`、`GET /cgi-bin/get_api_quota` |

本 skill 不覆盖：素材管理与草稿箱/发布能力（图文素材的 CRUD，域名相同但属于内容生产而非消息推送，文档在 `/doc/service/guide/product/asset.html`、`draft.html`、`publish.html`）、留言管理、数据统计接口、智能接口（NLP/OCR/图像处理）、微信发票与非税缴费、微信卡券与会员卡、微信门店/一物一码/长辈就医等垂直业务、JS-SDK 与开放标签的前端调用细节。这些的入口在服务号文档左侧导航，见 `wechat-mp-workspace/index.tsv`。

## House rules

- 凭证只走环境变量：`WECHAT_MP_APPID` / `WECHAT_MP_SECRET`，服务器配置用 `WECHAT_MP_TOKEN` / `WECHAT_MP_AES_KEY`。
- access_token 必须缓存并在有效期内复用（7200 秒），不要每次请求都换新 token；文档反复强调换 token 接口本身有独立的每日调用额度。
- 判断接口成功与否统一看响应体 `errcode == 0`，不要只看 HTTP 状态码——几乎所有业务错误都是 HTTP 200 + 非零 errcode（无凭证探测证实，见上）。
- 涉及用户 openid 的接口，openid 对"当前公众号"唯一；要跨公众号识别同一用户，需要 UnionID 机制（公众号绑定同一个微信开放平台账号后才有 `unionid` 字段）。
- 回调 / 主动下发消息前，先确认账号类型与认证状态：模板消息、网页授权 `snsapi_userinfo`、自定义菜单等能力大多要求"已认证服务号"，未认证账号调用会在业务错误码或后台权限集里体现，不是代码问题。
- 涉及 AES 消息加解密的代码，优先用官方 5 种语言示例代码校验过的库函数，不要自己重新实现 PKCS7 去填充逻辑（块大小是 32 字节，不是 AES 默认的 16）。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

**探测证实的发现**（`references/errors-and-limits.md` 与 `references/auth.md` 里用「无凭证探测（2026-09-17）」标注，未使用 `<!-- Gap: -->`，因为探测结果与文档描述一致，不是文档错误）：
- 换 token 接口对格式不合法的 appid 一律返回 `40013 invalid appid`，即使同时缺少 `grant_type` 参数也是先报 appid 错误——说明校验顺序是 appid 优先于 grant_type，文档未说明校验顺序。
- 伪造 access_token 调 `cgi-bin` 系列接口，报错文案里主动建议"could get access_token by getStableAccessToken"；同样伪造 `sns` 系列（网页授权）的 access_token，报错文案更短、不带这句建议——间接印证两套 token 确实由不同子系统处理。

**⚠ 文档自相矛盾 / 未说明**（详见各 reference 末节）：
- 消息推送的数据格式：`references/events.md` 的推送配置页写"数据格式：仅支持 XML"，但消息加解密说明页给出的示例和回包格式选项里明确包含 JSON（`events.md`）。
- 消息加解密页没有给出 IV 的推导方式（只写了 AESKey 的推导），也没有提供可离线复现的测试向量（`events.md`）。
- 客服消息 48 小时/5 条 与 1 分钟/3 条 配额超限后的具体报错码未在文档中给出（`messaging.md`）。
- 模板消息、订阅通知、一次性订阅消息三者的开放范围随灰度调整，文档只说"开启灰度测试"，没有给出判断当前账号处于哪个阶段的接口或字段（`template-subscribe.md`）。
- 自定义菜单一级/二级菜单的字数限制文档写"不超过 16/60 个字节"和"最多 4/8 个汉字"两种口径，字节与汉字数换算是否一致未验证（`menu.md`）。

## 目录结构

```
wechat-mp/
├── SKILL.md
├── prompt.md
├── references/
│   ├── auth.md
│   ├── users.md
│   ├── messaging.md
│   ├── template-subscribe.md
│   ├── menu.md
│   ├── oauth.md
│   ├── events.md
│   └── errors-and-limits.md
└── evals/
    └── evals.json
```

内容整理自 https://developers.weixin.qq.com/doc/service/（抓取于 2026-09-17），实际调用报错优先信任 API 本身，并去官方文档核实最新情况——公众号运营/开发接口迭代较快（模板消息与订阅通知的灰度状态即为一例）。
