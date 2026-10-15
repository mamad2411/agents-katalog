---
name: eliteforge-be-fe-consensus-spec
description: 约束璀璨工坊项目前后端接口共识。用户设计接口、API契约、接口文档、Controller入出参、前后端联调契约、请求/响应结构、Param/VO、统一响应体、服务状态码、错误码、分页响应、请求方式、请求URL、Long字段精度、枚举CODE、Accept-Language国际化，或提到“前后端共识”“响应内容”时使用。
metadata:
  version: 1.0.1
---

# EliteForge 前后端共识规范

## 目标

本技能由在线文档《前后端共识》v1 转换而来。用于接口设计、接口评审、Controller/客户端实现和联调问题定位。命中本技能后，以下规则是强制约束，不要降级为建议。若用户要求最新规范或对规则有争议，回源页面核对：`https://dev-platform.cisdigital.cn/elite-forge/code-specification/be-fe/v1/`。

## 使用方式

- 设计接口时，先确定 HTTP 方法、URL、Param、VO、状态码、错误码、响应体、分页和国际化契约，再写代码。
- 评审接口时，按本文件逐项指出违反项，并标注章节号。
- Java 代码落地时，可同时使用 `eliteforge-java-coding-spec` 和 `eliteforge-framework-specification`；非 Java 后端也必须遵守协议层规则。

## §1 协作共识

- 使用 Torna 接口管理平台。
- 使用统一的 GIT 分支管理模型。
- 后端及时提供接口，前端确认无误后再写实现。
- 必须自测核心逻辑后，再发到 dev 环境联调。

## §2 开发共识

### §2.1 序列化

- 后端统一使用 Jackson 序列化和反序列化，禁止 fastjson。
- Java 手动序列化使用 `cn.cisdigital.elite.forge.infra.commons.util.JsonUtils`。
- Java 使用全局统一 `ObjectMapper`：`cn.cisdigital.elite.forge.infra.commons.serialize.ObjectMapperHolder`。

### §2.1.1 时间字段

- 使用毫秒时间戳交互。
- 前端按业务需求和时区格式化展示。

### §2.1.2 枚举字段

- 前后端交互、数据库存储、手动序列化和反序列化都使用枚举 CODE。
- 禁止使用枚举 name。示例：`FEMALE(0)`、`MALE(1)` 交互值用 `0`、`1`，不用 `FEMALE`、`MALE`。

### §2.1.3 Long 字段

- Long 类型使用字符串交互，防止 JS 精度丢失，例如雪花 ID。
- `/api/**` 和 `/inner-api/**` 的 ObjectMapper 统一将 Long 序列化为 String。
- `/open-api/**` 使用不同 ObjectMapper，开放接口不要处理 Long 转 String。

### §2.1.4 字段无数据

- JSON 不能忽略无数据字段。
- 后端用 `null` 表示“不存在”。
- 前端必须兼容 `null`。

### §2.2 请求方式

- 仅允许 GET 和 POST。
- 禁止 Restful 风格。

### §2.3 请求 URL

- URL 单词使用 kebab-case，例如 `/get-unique-data`。
- 禁止路径参数，例如 `/my/api/123/detail`。

### §2.4 请求内容

- 每个请求使用独立 Param 类，禁止跨接口复用。
- Param 类非必要不继承。
- Param 类禁止冗余或无用字段。
- GET 请求禁止传 List。
- 三个以上参数必须使用 POST Request Body。
- Request Body 必须控制大小，并同步关注 Spring、Tomcat、Nginx 等限制。
- 分页请求参数统一为 `current`、`size`。

### §2.5 响应内容

- 每个接口有独立 VO 类，不复用其他接口 VO。
- VO 类非必要不继承。
- VO 类禁止冗余或无用字段。
- 只有接口调用成功，HTTP 状态码才是 200。
- 服务成功和失败用不同错误码表示，错误码必须符合服务状态码规范。
- `0` 代表请求成功。
- `-1` 代表系统异常或未知异常。
- 其他情况返回 9 位错误码：1-3 位为产品唯一标识，4-6 位为服务唯一标识，7-9 位为项目自定义数值；项目自定义数值不能重复，从 1 开始递增，高位补 0。
- 统一响应体必须是 `code`、`message`、`data`。
- 列表响应的 `data` 是数组；单对象响应的 `data` 是对象；分页响应的 `data` 包含 `current`、`size`、`total`、`records`。

列表响应：

```json
{
  "code": "服务状态码",
  "message": "响应消息",
  "data": []
}
```

单对象响应：

```json
{
  "code": "服务状态码",
  "message": "响应消息",
  "data": {}
}
```

分页响应：

```json
{
  "code": "服务状态码",
  "message": "响应消息",
  "data": {
    "current": "当前页",
    "size": "显示条数",
    "total": "总数",
    "records": []
  }
}
```

### §2.6 国际化

- 使用标准 `Accept-Language` Header 切换语言。
- Header 值格式为 `<语言代码>-<国家或地区代码>`，使用短横线，例如 `zh-CN`、`en-US`。

## 输出约束

- 设计或评审接口时必须显式应用本规范，并标注章节号。
- 对“禁止”“必须”类条款给出明确结论，不使用“建议可以”这类弱化措辞。
- 不自行扩展统一响应体字段；业务扩展放入 `data`。
- 规范未覆盖的场景，标注“需用户补充或需外部确认”。
