---
name: project-docs-api
description: Generate API documentation from Java Spring MVC, Feign, or Python FastAPI source, without IntelliJ IDEA. Use when asked for Markdown, Postman collections, or cURL examples from routes and request/response declarations.
---

# Project Docs API

Generate Markdown API documentation, Postman collections, and cURL examples from Spring MVC controllers, Feign clients, or FastAPI routes and their request/response declarations. Document fields and constraints from source evidence, and preserve unresolved types rather than guessing.

[中文文档 / Chinese documentation](.bundle/README.zh-CN.md)

若当前 Skill 目录下存在 `.bundle` 且其 `../../` 不是本集合的 Git 检出，先读取 `.bundle/skills/project-docs-api/GUIDE.md` 并以该目录为 Skill 真实目录；其中的共享脚本、资料和其他 Skill 均来自同一快照。通过 `npx skills update <已安装的本集合 Skill 名称>` 更新此类安装，按实际作用域加 `-g` 或 `-p`；不运行快照内依赖 Git 检出的更新命令。

按[读者与用途约定](.bundle/references/audience.md)提供必要解读；生成文档及用户要求的逐字接口片段仍保持下方契约，不能因读者不同改字段、必填、枚举或示例。读者提示放交付回复，独立解读按需提供，不重写生成原文。

Generate documentation with the API Savior RESTful Markdown contract from controller/Feign mapping annotations and real DTO declarations. Resolve this skill directory to its real path before using shared scripts or references, including when installed through a symlink. Use Python 3.11 or newer:

```bash
python3 <resolved-skill-directory>/../../scripts/generate_api_docs.py \
  --source <java-source-root> --output <output-directory> --base-url <optional-base-url>
```

It writes `api-docs.md`, `postman-collection.json`, and `curl.sh`.

- Pass one or more source roots with repeated `--source`.
- The generator is organized as `language adapter → API document IR → renderer`. `java_spring_adapter.py` and `python_fastapi_adapter.py` read source declarations; `api_document_renderers.py` consumes only the language-neutral IR. `generate_api_docs.py` preserves the CLI and existing Python imports. Use `--language python` for FastAPI source. See [the IR contract](.bundle/references/api-document-ir.md) before adding another language or framework.
- Require JDK 11 or newer for the current Java adapter. It uses the JDK AST API, not regular expressions, so it distinguishes DTO fields from local variables and supports `@RestController`, `@FeignClient(path = ...)`, class-level mappings, and source-defined composed Spring mappings.
- The FastAPI adapter handles `APIRouter` prefixes and `include_router`, `response_model`, package/relative imports, and request parameters declared by source-defined `Depends` functions, including route, router, include, and app dependencies. It preserves unresolved or ambiguous types rather than guessing.
- For Gradle projects, a selected Controller/Feign client automatically includes direct project-module `src/main/java` dependencies from either Groovy or Kotlin Gradle DSL. Pass additional `--source` roots for DTOs outside those modules; pass `--classpath <jar>` to supplement binary-only DTOs.
- The generator uses a code discovery engine automatically when one is available (codegraph index first, then the tree-sitter fallback), for Java and Python alike: `--endpoint` works without `--controller`, unresolved DTO types trigger automatic source-root discovery, and `--changed <file>` regenerates only the endpoints that change affects. `[codegraph]`/`[tree-sitter]` lines on stderr are informational, not errors. Pass `--no-codegraph` to disable all discovery; without an engine the generator scans the provided roots exactly as before. Engines only locate files and symbols — field, wire-name, and enum semantics always come from source parsing.
- For one endpoint, use `--controller <controller-java-file> --endpoint <method-name> --output-file <absolute-markdown-path>`. If that name has multiple routes or HTTP methods, use `--endpoint <name>@<METHOD>:<path>` (for example `find@POST:/items`); the CLI reports ambiguous names and available selectors. This fast path restricts the generated endpoint set before rendering.
- Preserve declared request fields, required flags, response-wrapper fields, DTO field descriptions, examples, notes, and JSON wire names such as `@JsonProperty` and `@RequestParam(name = ...)`. Respect source-declared Jackson field/getter annotations and class-level ignored properties, including inherited fields, in request and response directions. Java examples follow the plugin's field-meaning placeholders, typed explicit examples, numeric minimums, and millisecond timestamp convention. Never hard-code a project's wrapper or base-request models.
- For Java enum fields, resolve declared enum members and their API values from source. Handle direct enum types, fields linked to one enum through an annotation class literal (for example `@Schema(implementation = State.class)`), constructor-assigned values/descriptions, `@JsonValue`, `@JsonProperty`, and `@SerializedName`. Follow source-defined Controller helper calls that pass DTO parameters into enum methods to associate scalar fields with enums; keep these bindings local to each endpoint and parameter and leave conflicting matches unresolved. Keep enum choices in each field's “其他参考信息” and add a separate “枚举说明” table covering both request and response fields. Do not invent a wire value when source analysis cannot resolve it; use the ordinary typed placeholder in examples and label the field “取值未解析”. Supply the enum source root for this feature; binary-only JAR parsing does not expose enum metadata.
- RequestBody examples, Postman raw bodies, and cURL data use the same resolved DTO/enum values. Unresolved nested DTOs and non-JSON request bodies do not receive a fabricated JSON payload. Treat ordinary scalar examples as placeholders; replace them with valid environment values before sending requests. Without `--base-url`, cURL examples use localhost:8080 for Java or localhost:8000 for Python.
- The renderer follows the plugin's `restful/method.ftl` layout: 请求信息、入参、出参、JSON 示例、分层字段表、独立枚举表及源码声明的 Code 表格。GET 和表单接口生成 Postman Bulk Edit 入参示例。
- For a requested single endpoint, provide the corresponding generated section verbatim; do not create a rewritten substitute document.
- Parse package-private Controller methods as API methods; Spring MVC does not require `public` here.
- Only follow source-defined Controller/helper calls for the plugin's enum-field association. Do not inspect Controller, Service, Mapper, SQL, or runtime behavior to reinterpret other parameter semantics. Perform implementation/behavior audits only when explicitly requested, and present them separately from the plugin-style document.
- Resolve inheritance and generic substitutions from the supplied source roots and classpath JARs. The renderer keeps each generic instance separate, supports generic base classes and renders `Map` values as JSON objects. If stderr reports an unresolved DTO type, add that type's source root or JAR; unresolved request bodies and responses do not receive a fabricated `{}` example. A resolved DTO with no serialized fields can correctly produce `{}`. This parser intentionally does not load an IDEA project model.
- When the user requires exact parity with an installed IDEA plugin, compare both outputs for the same endpoint. This source-only adapter cannot infer library-only enum metadata or every PSI-resolved method call; report any unresolved fields explicitly instead of claiming byte-for-byte equivalence.
- Keep generated files outside the source tree unless the user explicitly wants them committed.
- Use the output as the API-doc generation equivalent of the documentation plugin. IDEA-only UI actions, navigation, and postfix code generation cannot run outside IDEA.
