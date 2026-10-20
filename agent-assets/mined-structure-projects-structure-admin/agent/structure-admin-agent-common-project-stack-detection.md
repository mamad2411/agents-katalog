---
name: common-project-stack-detection
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 project-stack-detection Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/project-stack-detection.md`（完整规范）。以下为操作要点：


# 项目栈识别与规则优先级

> 本规则 MUST 在任何工作开始前最先读。
> 目的：确保 AI 使用**正确的栈级规则**，而不是泛化的 _common 规则。

## 第 1 步：识别项目栈（MUST 最先执行）

开始任何工作前 MUST 先识别当前项目的技术栈：

### 通过依赖文件识别

```bash
# Java / Spring Boot 系
cat pom.xml | grep -o "cn\.structured\|spring-boot" | head -5

# 前端系
cat package.json | grep -o "@structure-projects\|vue\|react\|next" | head -5

# 通过 wiki/ 目录识别（最直接）
ls wiki/  # 看有哪些栈级 wiki 目录
```

### 通过项目根目录文件识别

| 标识文件 | 推断栈 |
|---|---|
| `pom.xml` 含 `cn.structured` | `structure-boot` |
| `pom.xml` 含 `spring-boot-starter` 但无 `cn.structured` | `spring-boot` |
| `package.json` 含 `vue` | `vue3` |
| `package.json` 含 `react` | `react` |
| `package.json` 含 `next` | `nextjs` |
| `build.gradle` / `build.gradle.kts` | 按 `plugins`/`dependencies` 识别 |
| `Cargo.toml` | Rust 栈（按 dependencies 识别 axum/actix） |
| `go.mod` | Go 栈（按依赖识别 gin/echo） |
| `requirements.txt` / `pyproject.toml` | Python 栈（按依赖识别 django/fastapi/flask） |
| `pubspec.yaml` | `flutter` |
| `*.xcodeproj` / `Podfile` | `ios` |
| `build.gradle` (Android) | `android` |

## 第 2 步：确定规则加载优先级（MUST 遵守）

识别出栈后 MUST 按以下顺序加载规则：

```
1. 栈级规则（<stack>-*.mdc）          ← 优先级最高
2. 栈级 Wiki（wiki/<stack>/*.md）     ← 必细参考
3. 栈级技能（<stack>-<action>）       ← 栈级动作
4. _common 规则（common-*.mdc）       ← 通用兜底
5. _common Wiki（wiki/_common/*.md）  ← 通用参考
6. _common 技能（git-commit 等）       ← 通用动作
```

**核心原则**：**栈级优先，_common 兜底**。

## 第 3 步：必读栈级 Wiki（MUST）

识别出栈后 MUST Read：

```
wiki/<stack>/developer.md         # 开发约束
wiki/<stack>/components.md        # 生态组件清单（必选组件）
wiki/<stack>/architect.md         # 架构约束（如涉及设计）
wiki/<stack>/project-scaffolding.md  # 项目结构（如涉及初始化）
```

## 第 4 步：常见错误（MUST NOT）

- ❌ **MUST NOT** 只看 _common 规则就开始工作
- ❌ **MUST NOT** 凭 LLM 自带知识选技术栈版本（必须看 `wiki/<stack>/components.md` 里的版本约束）
- ❌ **MUST NOT** 忽略栈级规则里的"必选组件"（如 structure-boot 项目 MUST 用 structure-security）
- ❌ **MUST NOT** 把 A 栈的规则应用到 B 栈项目

## 栈级规则覆盖范围（举例）

### structure-boot 项目 MUST 遵守

- **Spring Boot 版本**：MUST `4.0.6`（不是 3.x）
- **JDK**：MUST 17+
- **包名**：MUST `cn.structured.*`（含 d），除了 `structure-common` / `structure-infra` 用 `cn.structure.*`（无 d）
- **安全框架**：MUST 用 `structure-security`（含 JWT）
- **JSON**：MUST FastJSON（禁止 Jackson/Gson）
- **服务间调用**：MUST `@FeignClient` + fallback
- **持久化**：MUST `RepositoryFacade + Delegate` 模式
- **异常**：MUST `CommonException` + `{X}ExceptionEnum`
- **响应**：MUST `ResResultVO<T>` + `ResultUtilSimpleImpl`

### vue3 项目 MUST 遵守

- **技术栈**：Vue 3 + Vite + TS + Pinia + Vue Router + Element Plus + UnoCSS
- **微前端**：MUST 用 `wujie` + `@structure-projects/wujie-subapp`
- **组件库**：MUST 用 `@structure-projects/components`（按需命名导入）
- **HTTP**：MUST 用 `@structure-projects/gateway-client`
- **npm scope**：MUST `@structure-projects`

## 识别失败的处理

如果无法识别项目栈：
1. **MUST 问用户**："请确认当前项目使用的技术栈"
2. **MUST NOT** 默认按通用规则开始工作
3. **MUST NOT** 凭印象猜测栈

完整规则以 `wiki/_common/project-stack-detection.md` 为准。
