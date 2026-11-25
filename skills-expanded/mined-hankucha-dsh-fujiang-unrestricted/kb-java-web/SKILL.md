---
name: kb-java-web
description: CVE/PoC 知识库 · Java Web / CI / 中间件：Confluence OGNL(2022-26134)/pre-auth(2021-26084)/SSTI(2023-22527)/restore(2023-22518)/管理员接管(2023-22515)、Jenkins(2024-23897)、TeamCity(2023-42793/2024-27198)、Solr(2019-17558)、Tomcat AJP(2020-1938)/PUT(2017-12615)、Struts2 S2-066(2023-50164)、ActiveMQ(2023-46604)、WebLogic console(2020-14882)/async(2019-2725)。每条都有对应 PoC；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# Java Web / CMS / CI（22 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

若依(RuoYi) 二开 / Spring Boot 那类部署残留（默认口令、Druid、Actuator）与业务逻辑面一起在 `kb-gray-market`；这一栏是**有 CVE 的 Java Web / CI 组件**。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `cve-2017-12615-tomcat-put.md` | Tomcat PUT 任意文件写入（JSP 落地） | critical | PUT /x.jsp/ 写 webshell |
| `cve-2019-17558-solr-velocity.md` | Apache Solr Velocity 模板注入 RCE | high | - |
| `cve-2019-2725-weblogic-async.md` | WebLogic wls9_async_response 未授权 RCE（2019 在野） | critical | /wls9_async_response/on/asyncResponseService |
| `cve-2020-14882-weblogic-console.md` | WebLogic 控制台未授权 RCE（console.portal 路径穿越） | critical | /console/css/%252e%252e%252fconsole.portal |
| `cve-2020-1938-tomcat-ajp-ghostcat.md` | Tomcat AJP 文件读取 / 包含（Ghostcat） | critical | AJP 8009 读 WEB-INF/web.xml |
| `cve-2021-25646-druid-rce.md` | Apache Druid 未授权 RCE（CVE-2021-25646） | critical | POST /druid/indexer/v1/sampler 的 filter 里塞 JS |
| `cve-2021-26084-confluence-ognl-preauth.md` | Confluence 未授权 OGNL 注入（pre-auth，ENCODED_TOKEN） | critical | /pages/doenterpagevariables.action 的 queryString |
| `cve-2022-22947-gateway-spel.md` | Spring Cloud Gateway Actuator SpEL 注入 RCE（CVE-2022-22947） | critical | /actuator/gateway/routes 添加 SpEL 过滤器后 refresh |
| `cve-2022-22963-spring-cloud-function.md` | Spring Cloud Function SpEL 注入 RCE（CVE-2022-22963） | critical | 请求头 spring.cloud.function.routing-expression |
| `cve-2022-26134-confluence-ognl.md` | Confluence 未授权 OGNL 注入（Confluence OGNL RCE） | critical | - |
| `cve-2023-22515-confluence-admin.md` | Confluence 未授权管理员接管（setup 流程未关） | critical | 打开 setup 流程重建管理员 |
| `cve-2023-22518-confluence-setup-restore.md` | Confluence 未授权恢复导致管理员接管 | critical | /json/setup-restore.action 上传自有导出 |
| `cve-2023-22527-confluence-ssti.md` | Confluence 模板注入 RCE（text-inline.vm） | critical | - |
| `cve-2023-27350-papercut-setup-bypass.md` | PaperCut NG/MF 认证绕过 → RCE（CVE-2023-27350） | critical | /app?service=page/SetupCompleted 未授权 → 打印脚本执行 |
| `cve-2023-42793-teamcity-auth-bypass.md` | TeamCity 认证绕过 → 管理员令牌 → RCE | critical | - |
| `cve-2023-46604-activemq-openwire.md` | Apache ActiveMQ OpenWire 反序列化 RCE | critical | OpenWire 发 ClassInfo 加载远程 XML |
| `cve-2023-50164-struts2-s2-066.md` | Struts2 文件上传路径穿越（S2-066） | critical | 篡改上传文件名的目录穿越 |
| `cve-2023-7028-gitlab-takeover.md` | GitLab 任意账号接管（CVE-2023-7028） | critical | POST /users/password 的 user[email][] 传两个地址 |
| `cve-2024-23897-jenkins-file-read.md` | Jenkins CLI 任意文件读取 | high | - |
| `cve-2024-27198-teamcity-bypass.md` | TeamCity 鉴权绕过（;.jsp 路径参数） | critical | /app/rest/server;.jsp 越权后建管理员 |
| `cve-2024-38856-ofbiz-unauth-rce.md` | Apache OFBiz 未授权 RCE（CVE-2024-38856） | critical | /webtools/control/ProgramExport 未授权执行 Groovy |
| `cve-2024-53677-struts2-s2-067.md` | Struts2 文件上传路径穿越 → RCE（S2-067，CVE-2024-53677） | critical | multipart 里 UploadFileName 用 ../ 穿越到 web 根 |

## 用这一页的方法

- 先看 `/prod-api/`、`/druid/`、`/actuator`、`/swagger-ui.html` 这四个"开发残留"，比找 CVE 快得多。
- Actuator/heapdump 里能直接捞到 DB/Redis 口令与 JWT secret —— 拿到就回落 `kb-triage` 的资产分层。
- 若依系后台的"定时任务"与"代码生成器"是现成 RCE 入口，比链式反序列化稳。
