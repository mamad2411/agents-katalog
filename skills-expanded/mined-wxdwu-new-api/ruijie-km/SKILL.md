---
name: ruijie-km
description: 查询锐捷 KM 知识库文档、分类、标签、文档详情和资料下载记录。适用于查最新彩页、参数规格、产品资料、知识库分类和资料附件。
---

# 锐捷知识库

当用户要查锐捷 KM 资料、产品彩页、参数规格、文档详情、附件链接、分类或标签时使用本技能。

## 默认入口

优先使用 `km_search`，把用户问题当成知识库检索任务处理，而不是直接暴露 API 参数。

常见用法：

- “查一下 RG-S6921 最新产品彩页”
- “找交换机相关的参数规格资料”
- “查某个 docId 的详情和附件”
- “列出顶层分类，再展开市场资料库”

`km_search` 会做这些事：

- 用关键词、分类、标签、平台、时间范围检索文档
- 默认按发布时间倒序返回
- 对前几个结果补查详情，方便输出摘要、正文片段、KM 链接和附件
- 把 `makiting`、`marketing`、`市场资料平台` 统一按生产环境实际可用的 `marketing` 处理

## 工具选择

- `km_search`：面向用户的首选检索入口。
- `km_get_document`：已知 `docId` 时查正文、KM 链接和附件列表。
- `km_list_categories_by_parent`：展开分类；最顶层传 `parentId=0`。
- `km_list_categories`：读取完整分类树。
- `km_list_tags`：查标签，标签变化不频繁，查到后尽量在上下文里复用。
- `km_list_documents`：底层分页列表接口，只在需要精确控制 API 参数时使用。
- `km_list_downloads`：下载记录接口，只在用户明确要求“下载记录、下载人、审计、下载统计”时使用。
- `km_get_config`：排查连接环境和鉴权配置。

## 输出口径

检索结果优先给用户能直接判断的字段：

- 标题
- 更新时间或发布时间
- 作者
- 版本号
- 分类
- 标签
- 摘要或正文片段
- KM 文档链接
- 附件名称和附件链接

多结果时先列最相关或最新的 3-5 条，再说明还有多少条结果。不要把原始 JSON 大段倒给用户，除非用户明确要调试接口。

## 安全边界

下载记录可能包含下载者、部门、IP 和下载时间。除非用户明确要求查下载记录或审计信息，不要主动调用 `km_list_downloads`。

## 配置

默认使用生产 KM：

```bash
export RUIJIE_KM_ENV=prod
```

测试环境：

```bash
export RUIJIE_KM_ENV=test
```

或直接指定地址：

```bash
export RUIJIE_KM_BASE_URL="https://kmtest.ruijie.com.cn:1443"
```

如果 KM 网关需要登录态或额外请求头：

```bash
export RUIJIE_KM_COOKIE="your_cookie_string"
export RUIJIE_KM_AUTHORIZATION="Bearer your_token"
export RUIJIE_KM_EXTRA_HEADERS='{"X-Example":"value"}'
```

如果本机 Python 无法校验内部证书链，优先配置企业 CA：

```bash
export RUIJIE_KM_CA_FILE="/path/to/company-ca.pem"
```

内部临时联调可跳过 TLS 校验：

```bash
export RUIJIE_KM_INSECURE_TLS=1
```
