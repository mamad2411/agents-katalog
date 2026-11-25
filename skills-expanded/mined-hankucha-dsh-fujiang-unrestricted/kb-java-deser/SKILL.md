---
name: kb-java-deser
description: CVE/PoC 知识库 · Java 反序列化与表达式注入：Log4Shell(2021-44228)、Spring4Shell(2022-22965)、Struts2 S2-045(2017-5638)、WebLogic T3(2015-4852)/wls-wsat(2017-10271)、Fastjson autoType(2022-25845)、Java ECDSA 空签名(2022-21449)。每条都有对应 PoC 与利用步骤；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# Java 反序列化 / 表达式注入（9 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

命中特征：响应头或报错里出现 Java 技术栈（Tomcat/Jetty/WebLogic/Resin），参数被记录进日志，JSON 请求体，`Set-Cookie: rememberMe=deleteMe`，`Content-Type` 被服务端解析。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `cve-2015-4852-weblogic-t3.md` | WebLogic T3 反序列化（CommonsCollections） | critical | T3 握手 + ysoserial 序列化对象 |
| `cve-2016-4437-shiro-rememberme.md` | Shiro rememberMe 默认密钥反序列化 RCE（CVE-2016-4437） | critical | Cookie: rememberMe=<AES 加密的 gadget 链> |
| `cve-2017-10271-weblogic-wls-wsat.md` | WebLogic wls-wsat XMLDecoder 反序列化 RCE | critical | - |
| `cve-2017-5638-struts2-s2-045.md` | Struts2 S2-045 Content-Type OGNL 注入 | critical | - |
| `cve-2021-44228-log4shell.md` | Apache Log4j2 JNDI 注入（Log4Shell） | critical | - |
| `cve-2022-1471-snakeyaml.md` | SnakeYAML 反序列化 RCE（CVE-2022-1471） | critical | 任意 YAML 输入（上传/配置/接口） |
| `cve-2022-21449-psychic-signatures.md` | Java ECDSA 空签名绕过（Psychic Signatures） | high | r=0,s=0 的空签名被接受 |
| `cve-2022-22965-spring4shell.md` | Spring Framework 数据绑定 RCE（Spring4Shell） | critical | - |
| `cve-2022-25845-fastjson-autotype.md` | Fastjson autoType 反序列化 RCE | high | - |

## 用这一页的方法

1. 先按「指纹」确认组件与版本区间（版本不在区间内的，别把 PoC 打出去当结论）。
2. 每条 PoC 都给了**探测形态**与**利用形态**两段；先打探测，用 dnslog / 回显头 / 现象确认命中，再打利用。
3. 需要外连的（JNDI、反序列化回连）先确认目标出网；不出网的目标改走本地 gadget + 回显，或干脆只提交"可利用性证据"。
4. 修复建议按条目里的一行落地，报告里写清"实测版本 + 命中证据 + 建议版本"。
