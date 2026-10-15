---
name: apifox-sync
description: 与 Apifox 双向同步接口文档和数据模型。支持：1）从 Apifox 导出 OpenAPI 规范并生成 Java Spring Boot 代码（Controller、DTO、Entity）；2）解析本地 Java 代码（注解或手动描述）并导入到 Apifox 更新接口/数据模型；3）批量扫描目录同步多个 Controller；4）增量同步只更新变更的接口。当用户提到"从 Apifox 获取接口"、"生成接口代码"、"同步到 Apifox"、"上传接口到 Apifox"、"更新 Apifox 文档"、"批量同步"时使用此 skill。
---

# Apifox 双向同步

## 脚本路径配置

**首次使用前，确认脚本安装路径（以下用 `{SKILL_PATH}` 表示）：**

| IDE/平台 | 默认路径 |
|---------|---------|
| Qoder | `.qoder/skills/apifox-sync` |
| Cursor | `.cursor/skills/apifox-sync` |
| 手动安装 | 用户自定义位置 |

**AI Agent 自动检测规则：**
1. 优先检查 `.qoder/skills/apifox-sync/scripts/apifox-api.py` 是否存在
2. 若不存在，检查 `.cursor/skills/apifox-sync/scripts/apifox-api.py`
3. 若都不存在，询问用户脚本安装位置

**后续所有命令中的 `{SKILL_PATH}` 需替换为实际检测到的路径。**

---

## 第 0 步：读取配置（每次操作前必做）

**按以下优先级获取 `ACCESS_TOKEN` 和 `PROJECT_ID`，不得直接向用户索要：**

### 优先级 1：读取项目根目录的 `apifox.config.json`

使用文件读取工具查找工作区根目录下的 `apifox.config.json`，格式如下：

```json
{
  "accessToken": "your-token-here",
  "projectId": "12345678"
}
```

**可选的高级配置项（支持自定义包装类和模型目录）：**

```json
{
  "accessToken": "your-token-here",
  "projectId": "12345678",
  "responseWrapperTypes": {
    "MyResult": {
      "success": {"type": "boolean"},
      "errorCode": {"type": "string"},
      "data": "$T"
    }
  },
  "modelDirs": ["domain", "dto", "vo", "entity", "model", "bean", "pojo"]
}
```

- `responseWrapperTypes`：自定义响应包装类结构。`"$T"` 表示泛型参数展开位置。默认已支持 `Result`、`R`、`CommonResult`、`BaseResult`、`ApiResult`、`ResponseEntity`。
- `modelDirs`：自定义数据模型搜索的子目录名。默认搜索 `domain`、`dto`、`vo`、`entity`、`model`、`bean`、`pojo`、`request`、`response`。

若文件存在，直接读取 `accessToken` 和 `projectId` 字段，跳过后续询问。

### 优先级 2：文件不存在时，引导用户初始化

告知用户可在项目根目录终端运行以下命令（**一次性操作，后续无需重复**，支持 Windows / macOS / Linux）：

```bash
python {SKILL_PATH}/scripts/init-config.py
```

或者让用户直接提供 Token 和 Project ID，AI 自动在项目根目录创建 `apifox.config.json`。

> **安全提示：** 建议将 `apifox.config.json` 加入 `.gitignore`，防止 Token 泄露到代码仓库。

获取 ACCESS_TOKEN 路径：`Apifox → 头像 → 账号设置 → API 访问令牌 → 新建令牌`

---

## 工作流 1：从 Apifox 拉取并生成代码

### 步骤 1：运行导出脚本获取 OpenAPI 数据

在项目根目录执行以下命令：

```bash
python {SKILL_PATH}/scripts/apifox-api.py export
```

脚本会自动读取 `apifox.config.json` 中的配置，输出完整的 OpenAPI JSON 到终端。

如需保存到文件：

```bash
python {SKILL_PATH}/scripts/apifox-api.py export openapi.json
```

> 完整 API 参数说明参见 [api-reference.md](references/api-reference.md)

### 步骤 2：解析 OpenAPI 数据

从响应 JSON 中提取：
- `paths`：接口路径、方法、参数、请求体、响应
- `components.schemas`：数据模型（生成 DTO/Entity）
- `tags`：接口分组（生成 Controller 类名）

### 步骤 3：生成 Java Spring Boot 代码

详细模板参见 [code-gen-guide.md](references/code-gen-guide.md)。

| 目标 | 规则 |
|------|------|
| Controller | 每个 `tag` → 一个 `@RestController`，每个路径方法 → 一个方法 |
| DTO | 每个 schema → 一个 DTO 类，`required` 字段加 `@NotNull`/`@NotBlank` |
| 命名 | 类名 PascalCase，方法名 camelCase |

---

## 工作流 2：将本地代码上传到 Apifox

### 方式 A：智能解析 Java 代码（推荐）

运行代码解析脚本，自动扫描并提取接口信息：

```bash
# 解析单个文件
python {SKILL_PATH}/scripts/code-parser.py parse src/main/java/com/example/controller/UserController.java

# 批量解析目录
python {SKILL_PATH}/scripts/code-parser.py parse-dir src/main/java/com/example/controller/

# 输出 OpenAPI JSON
python {SKILL_PATH}/scripts/code-parser.py parse-dir src/main/java/com/example/controller/ --output openapi.json
```

**智能解析特性：**

脚本自动识别以下注解并转换：

| Java 注解 | OpenAPI 字段 |
|----------|-------------|
| `@RestController` + `@RequestMapping` | 基础路径 |
| `@GetMapping` / `@PostMapping` / `@PutMapping` / `@DeleteMapping` | 路径和方法 |
| `@PathVariable` / `@RequestParam` / `@RequestBody` | 参数 |
| `@Operation` / `@Parameter` / `@Schema` | 描述信息 |
| `@NotNull` / `@NotBlank` / `@NotEmpty` | required 字段 |
| `@Api` / `@ApiOperation`（Swagger 2） | 描述信息 |

**数据模型自动追踪：**

解析器会智能识别并处理以下场景：

1. **复杂类型参数**：`@RequestParam UserDTO user` → 自动转换为 requestBody，并生成 UserDTO schema
2. **泛型返回类型**：`Result<DemoVO>` → 自动展开为 `{ code, msg, data: DemoVO }` 结构
3. **多种包装类**：内置支持 `Result<T>`、`R<T>`、`CommonResult<T>`、`BaseResult<T>`、`ApiResult<T>`、`ResponseEntity<T>` 等包装类，也可通过 `apifox.config.json` 自定义
4. **分页类型**：内置支持 `Page<T>`（Spring Data）、`IPage<T>`（MyBatis-Plus）、`PageResult<T>`、`PageInfo<T>` 等分页包装
5. **Map 类型**：`Map<String, UserDTO>` → 正确生成 `additionalProperties` 结构
6. **引用类型解析**：自动扫描 `domain/`, `dto/`, `vo/`, `entity/`, `model/`, `bean/`, `pojo/`, `request/`, `response/` 目录（可通过配置自定义），生成所有引用的数据模型
7. **嵌套泛型**：`List<UserDTO>`、`Map<String, List<UserDTO>>` → 正确生成嵌套类型
8. **数组类型**：`String[]`、`int[]` → 正确生成 array 类型

> **注意**：确保 Controller 文件和其引用的 DTO/VO 文件在同一项目结构中，解析器会自动从 `src/main/java` 根目录搜索数据模型定义。

### 方式 B：用户手动描述

按以下格式整理后构建 OpenAPI JSON：

```
接口名称：xxx
路径：GET /api/xxx
描述：xxx
请求参数：
  - id: integer, 必填, 用户ID
请求体：{ 字段列表 }
响应：{ code: integer, data: 对象 }
```

### 步骤：运行导入脚本上传到 Apifox

**方式 A：从 JSON 文件导入**

```bash
python {SKILL_PATH}/scripts/apifox-api.py import openapi.json
```

**方式 B：直接传入 JSON 字符串**

```bash
python {SKILL_PATH}/scripts/apifox-api.py import-raw '{"openapi":"3.0.1","info":{"title":"项目名","version":"1.0.0"},"paths":{...}}'
```

**方式 C：一键同步（解析 + 上传）**

```bash
# 同步单个文件
python {SKILL_PATH}/scripts/apifox-api.py sync-file src/main/java/com/example/controller/UserController.java

# 批量同步目录
python {SKILL_PATH}/scripts/apifox-api.py sync-dir src/main/java/com/example/controller/
```

> 完整 API 参数说明参见 [api-reference.md](references/api-reference.md)

**同步策略说明：**

| 策略 | 场景 |
|------|------|
| `OVERWRITE_EXISTING`（默认） | 覆盖已存在，推荐日常更新 |
| `AUTO_MERGE` | 自动合并更改 |
| `KEEP_EXISTING` | 保留已存在，仅新增 |
| `CREATE_NEW` | 保留已存在，另创建新的 |

> 如需使用其他策略，在命令中添加 `--strategy AUTO_MERGE` 参数。

---

## 工作流 3：批量操作

### 批量导出并生成代码

```bash
# 导出全部接口并生成代码
python {SKILL_PATH}/scripts/apifox-api.py export --generate

# 指定输出目录
python {SKILL_PATH}/scripts/apifox-api.py export --generate --output src/main/java/com/example/
```

### 批量同步本地代码到 Apifox

```bash
# 扫描整个 controller 目录并同步
python {SKILL_PATH}/scripts/apifox-api.py sync-dir src/main/java/com/example/controller/ --strategy OVERWRITE_EXISTING

# 只同步变更的文件（增量同步）
python {SKILL_PATH}/scripts/apifox-api.py sync-dir src/main/java/com/example/controller/ --incremental
```

### 查看同步状态

```bash
# 查看本地代码与 Apifox 的差异
python {SKILL_PATH}/scripts/apifox-api.py diff src/main/java/com/example/controller/

# 预览将要同步的内容（不实际执行）
python {SKILL_PATH}/scripts/apifox-api.py sync-dir src/main/java/com/example/controller/ --dry-run
```

---

## 错误处理

| HTTP 状态 | 含义 | 处理 |
|-----------|------|------|
| 401 | Token 无效或过期 | 重新生成 Token，更新 `apifox.config.json` |
| 403 | 无项目权限 | 确认 Token 对应账号有该项目权限 |
| 404 | projectId 不存在 | 确认 PROJECT_ID，更新 `apifox.config.json` |
| 422 | 数据格式错误 / 缺少版本 Header | 检查 `X-Apifox-Api-Version` 是否携带；OpenAPI JSON 格式是否合法 |

---

## 快速示例

**场景：导出 Apifox 全量接口并生成 UserController**
1. 运行 `python {SKILL_PATH}/scripts/apifox-api.py export` 获取 OpenAPI JSON
2. 解析 JSON，筛选含 `/user` 的路径
3. 生成 `UserController.java`（参见 [code-gen-guide.md](references/code-gen-guide.md)）

**场景：把本地新写的接口同步到 Apifox**
1. 读取指定 Controller 文件，解析注解，构建 OpenAPI JSON
2. 将 OpenAPI JSON 保存到临时文件 `temp-openapi.json`
3. 运行 `python {SKILL_PATH}/scripts/apifox-api.py import temp-openapi.json`
4. 脚本返回导入结果（创建/更新/失败数量）

**场景：批量同步整个 controller 目录**
1. 运行 `python {SKILL_PATH}/scripts/apifox-api.py sync-dir src/main/java/com/example/controller/`
2. 脚本自动扫描所有 Controller 文件，解析并上传
3. 返回汇总结果
