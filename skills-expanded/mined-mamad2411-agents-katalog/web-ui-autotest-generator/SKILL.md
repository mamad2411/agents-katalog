---
name: web-ui-autotest-generator
description: 从前端和后端源码中生成可维护的 Web UI 自动化测试。适用于分析页面、路由、组件、接口、用户流程，生成 Playwright UI 测试，运行测试，生成中文报告，并自检页面功能和跨页面逻辑是否被独立测试资产覆盖。 Generate maintainable Web UI automated tests from frontend and backend source code. Use for analyzing pages, routes, components, APIs, and user flows; generating and running Playwright UI tests; producing Chinese test reports; and checking whether page features and cross-page logic are covered by independent test assets.
---

# Web UI 自动化测试生成器

使用本 skill 可以把一个 Web 项目整理成可执行、可复查、可持续维护的 UI 自动化测试套件。

目标不是只写几条临时脚本，而是先分析前端页面、后端接口、用户流程和 UI 状态，再生成 Playwright 测试、覆盖率清单、执行命令和中文报告。生成后的测试资产应能脱离本 skill 独立运行。

## 默认技术栈

除非目标仓库已经明确使用其他 UI 测试框架，否则默认使用 Playwright + TypeScript。

默认输出结构：

```text
tests/e2e/
  pages/                 # Page Object 模型
  specs/                 # 按页面或路由组织的测试用例
  fixtures/              # 登录状态、测试数据、接口 mock
  utils/                 # 通用辅助函数
  reports/               # 测试报告和中文总结
playwright.config.ts
ui-test-manifest.json
ui-test-coverage.json
```

内置资源：

```text
scripts/generate_manifest.py       # 源码扫描，生成 ui-test-manifest.json
scripts/audit_selectors.py         # 选择器稳定性审计，生成 ui-selector-audit.json
scripts/check_coverage.py          # 清单和用例覆盖率检查，生成 ui-test-coverage.json
scripts/analyze_failures.py        # Playwright JSON 报告分析，生成 ui-test-repair-plan.json
assets/templates/                  # Playwright 起始模板
assets/templates/summary.zh-CN.md.template # 中文最终测试报告模板
```

## 工作流程

1. 检查项目结构和已有测试工具。
2. 分析前端路由、页面、组件、UI 控件、状态管理和接口调用。
3. 如存在后端代码、OpenAPI、Swagger 或 Apifox 文档，补充分析接口契约。
4. 生成页面、功能、接口和流程清单。
5. 审计选择器稳定性，并记录 `data-testid` 等改造建议。
6. 生成 Playwright Page Object、fixture、spec 和 CI 脚本。
7. 条件允许时在本地运行测试。
8. 如果测试失败，分析失败原因并修复生成的测试。
9. 按覆盖率规则自检生成结果并输出评分。
10. 生成中文测试报告，说明执行结果、覆盖缺口、选择器风险和后续动作。

生成或评审测试时，按需读取 `references/coverage-rubric.md`。

编写清单、覆盖率或报告时，按需读取 `references/output-contract.md`。

## 脚本化初筛

先使用内置脚本得到稳定的基础扫描结果，再结合项目代码进行人工判断和修正。

生成初始清单：

```bash
python3 path/to/web-ui-autotest-generator/scripts/generate_manifest.py --root . --out ui-test-manifest.json --pretty
```

审计选择器稳定性：

```bash
python3 path/to/web-ui-autotest-generator/scripts/audit_selectors.py --root . --out ui-selector-audit.json --pretty
```

生成测试后检查覆盖率：

```bash
python3 path/to/web-ui-autotest-generator/scripts/check_coverage.py --root . --manifest ui-test-manifest.json --selector-audit ui-selector-audit.json --tests-dir tests/e2e --out ui-test-coverage.json --pretty
```

如果 Playwright 执行失败且已有 JSON 报告，生成修复计划：

```bash
python3 path/to/web-ui-autotest-generator/scripts/analyze_failures.py --report tests/e2e/reports/results.json --out ui-test-repair-plan.json --pretty
```

脚本输出是草稿，需要复核：

- 生成大量测试前，先修正错误的路由、页面和文件映射。
- 如果源码高度动态，补充业务名称、权限信息和接口映射。
- 使用 `ui-selector-audit.json` 选择更稳定的定位方式，并给出 `data-testid` 建议。
- 不要静默忽略覆盖缺口；应在 `ui-test-coverage.json` 中写明原因。

## 发现规则

从快速本地检查开始：

```bash
rg --files
```

重点识别：

- 包管理器：`package.json`、lockfile、workspace 文件。
- 前端框架：React、Next.js、Vue、Nuxt、Angular、Svelte、Vite、Umi、qiankun、微前端。
- 路由定义：router 文件、文件路由约定、路由配置、菜单配置。
- 页面根目录：`src/pages`、`src/views`、`app`、`pages`、`routes`。
- 复用 UI 组件：弹窗、抽屉、表格、表单、上传器、选择器、标签页、步骤条。
- 接口层：`src/api`、`src/services`、请求客户端、生成式客户端、GraphQL 文档。
- 状态与鉴权：store、context、cookie、localStorage、路由守卫、权限校验。
- 现有测试约定：命名方式、fixture、测试 id、mock 风格、CI 脚本。

优先沿用仓库已有风格。如果已有 Playwright，直接扩展现有体系。如果项目已经稳定使用 Cypress，且用户没有指定 Playwright，则跟随 Cypress。

## 前端分析

建立页面清单。每个页面都应尽量识别：

- 路由路径和路由参数。
- 页面标题或业务名称。
- 访问权限和登录要求。
- 主组件和子组件。
- 可见控件：按钮、链接、标签页、菜单、筛选项、输入框、下拉框、日期选择器。
- 表单字段、校验规则、必填项、禁用态。
- 表格或列表列、行操作、分页、排序、批量操作。
- 弹窗、抽屉、浮层及其提交、取消流程。
- 空态、加载态、错误态、成功态和无权限状态。
- 页面跳转和跨页面流转。
- 页面加载或用户操作触发的接口调用。

优先基于源码和稳定选择器生成测试。如果 UI 元素缺少稳定选择器，使用 `getByRole`、`getByLabel`、`getByText` 等可访问定位方式，并在报告中说明哪些位置适合补充 `data-testid`。

选择器优先级：

1. `data-testid` 或项目已有测试 id 约定。
2. 可访问角色和名称。
3. 表单字段 label。
4. 稳定可见文本。
5. 稳定组件属性。
6. 只有没有更好方式时才使用 CSS 选择器。

生成 spec 前先运行 `scripts/audit_selectors.py`。根据审计结果决定：

- 使用已有稳定选择器生成测试。
- 当可访问信息足够时，优先使用 role、label、text 定位。
- 对缺少稳定选择器的关键元素写入 `missingStableSelectors` 建议。
- 只有用户同意修改产品代码时，才补充 `data-testid`。

核心流程不要悄悄使用脆弱选择器。无法避免时，必须在最终中文报告中说明。

## 后端与接口分析

使用后端代码、OpenAPI、Swagger 或 Apifox 文档增强 UI 测试。

提取：

- 接口方法和路径。
- 请求参数、body 结构和必填字段。
- 响应字段和业务状态。
- 错误码和校验信息。
- 鉴权方式和角色要求。
- 数据生命周期约束，例如创建 -> 列表 -> 详情 -> 更新 -> 删除。

把接口映射回 UI 行为：

```text
页面加载 -> 列表/详情接口
搜索/筛选 -> 查询接口
新增/编辑表单 -> 创建/更新接口
删除/批量操作 -> 变更接口
下载/导出 -> 文件接口
路由跳转 -> 详情页或子页面接口
```

如果没有后端代码，从前端接口客户端推断契约，并在必要时使用 route mock。

## 清单优先

生成大量测试前，先创建或更新 `ui-test-manifest.json`。

清单应描述：

- 页面和路由。
- 每个页面的功能项。
- UI 元素和操作。
- 接口依赖。
- 跨页面流程。
- 建议测试场景。
- 已覆盖和缺失项。

把清单作为生成和评审的事实来源。清单错误时，先修正清单，再扩展测试。

## 测试生成规则

按页面和用户流程生成测试。

创建新的 Playwright 文件时，使用 `assets/templates/` 作为起点：

- `page-object.ts.template`：Page Object 类。
- `page-spec.ts.template`：页面级测试。
- `playwright.config.ts.template`：项目没有 Playwright 配置时使用。
- `auth-fixture.ts.template`：需要鉴权但项目登录方式不明确时使用。
- `package-scripts.json.template`：补充 npm scripts 时使用。
- `github-actions-e2e.yml.template`：补充 GitHub Actions CI 时使用。
- `summary.zh-CN.md.template`：编写最终中文测试报告时使用。

每个业务页面通常应覆盖：

- 页面可以正常加载。
- 核心可见控件渲染。
- 主列表、表格或主要内容渲染。
- 搜索、筛选、重置流程。
- 支持新增时覆盖新增流程。
- 支持编辑时覆盖编辑流程。
- 支持删除或危险操作时覆盖确认与结果。
- 支持详情或跳转时覆盖导航流程。
- 必填字段和表单校验错误。
- 接口失败或空态。
- 相关的无权限或未登录状态。

跨页面流程应生成场景 spec，不要在单页面测试中重复堆叠：

```text
登录 -> 新建实体 -> 搜索实体 -> 打开详情 -> 编辑实体 -> 回到列表验证 -> 删除实体
```

避免脆弱测试：

- 不断言用户看不到的实现细节。
- 不依赖任意固定等待。
- 除非 fixture 明确创建数据，否则不依赖顺序敏感的数据。
- 不绑定生成式 CSS 类名。
- 如果应用支持 i18n，不假设固定中英文文本，应检查语言文件。

使用确定性测试数据：

- 优先使用 API 做 setup 和 teardown。
- 测试数据名称使用时间戳或生成 ID 保持唯一。
- 创建的数据要隔离并清理。
- 如果清理有风险，危险场景优先使用 mock。

## Page Object 规则

重复交互和稳定页面语义应放入 Page Object。

好的 Page Object 暴露用户语义动作：

```ts
await userListPage.search({ name: 'Alice' })
await userListPage.createUser(data)
await userListPage.deleteUser('Alice')
```

不要把底层选择器作为主要接口，除非确实需要。

Page Object 应包含：

- `goto`
- 核心 locator
- 常用用户动作
- 页面 ready 断言
- 表格、表单、弹窗的小型辅助方法

场景特有断言保留在 spec 中，可复用的页面就绪断言放在 Page Object 中。

## 鉴权策略

如果页面需要登录：

1. 优先复用项目已有鉴权 helper。
2. 优先使用 Playwright `storageState` fixture。
3. 如果后端支持测试登录接口，用接口完成登录准备。
4. 如果没有稳定测试账号，生成带占位说明的测试，并在报告中标记为需要人工补充。

不要写入真实生产账号或密钥。

## 执行

新增或复用脚本：

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

条件允许时运行：

```bash
npx playwright test
```

如果应用需要开发服务器，使用仓库标准 dev 命令启动，并按需配置 Playwright `webServer`。

如果依赖缺失且网络不可用，仍然生成测试套件，并在中文报告中明确写明未执行原因。

## 失败修复循环

测试失败时，先做短循环修复，避免只留下原始失败。

1. 使用 JSON reporter 运行 Playwright。
2. 用 `scripts/analyze_failures.py` 生成 `ui-test-repair-plan.json`。
3. 将失败归类为：选择器、超时、断言、鉴权、导航、接口、测试数据或未知。
4. 优先修复出现最多的失败类型。
5. 重跑受影响 spec 或完整测试套件。
6. 重新生成 `ui-test-coverage.json`。

修复建议：

- 选择器失败：改进 Page Object locator，补充稳定选择器建议，只有获得许可时才改产品代码的 `data-testid`。
- 超时失败：等待用户可见的页面就绪、接口响应或加载态消失。
- 断言失败：断言稳定的用户可见结果，不断言实现细节。
- 鉴权失败：补充 storage state、测试登录 fixture 或账号需求说明。
- 接口/数据失败：补充确定性 setup、route mock 或 cleanup helper。

当测试通过，或遇到必须由用户提供账号、环境、业务规则的明确阻塞时，停止修复循环。

## CI/CD 产物

生成后的测试应能脱离本 skill 独立运行。

如果项目使用 npm scripts，新增或合并：

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ci": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

如果项目使用 GitHub Actions，复制并调整 `assets/templates/github-actions-e2e.yml.template` 到 `.github/workflows/e2e.yml`。

其他 CI 系统也应保持同一契约：

- 安装依赖。
- 安装 Playwright 浏览器。
- 提供 `E2E_BASE_URL` 和鉴权密钥。
- 运行 `npm run test:e2e:ci`。
- 上传 HTML、JSON、JUnit、trace 等报告产物。

## 自检

生成后必须先自检，再交付。

首次生成测试后运行 `scripts/check_coverage.py`，修复后再次运行。

检查：

- 每个发现到的路由是否至少有一个加载或渲染测试。
- 每个主要按钮或动作是否有测试场景，或有明确排除原因。
- 每个表单是否覆盖必填校验和至少一个成功路径。
- 列表页是否覆盖搜索、重置、分页和空态。
- 危险操作是否覆盖确认、取消和结果验证。
- 是否覆盖接口失败或后端错误状态。
- 重要跨页面流程是否覆盖。
- 测试套件是否能独立运行。
- 选择器是否可维护。
- 测试数据 setup 和 cleanup 是否清晰。

写入 `ui-test-coverage.json`，包含已覆盖项和缺失项。缺失项可以存在，但必须写明原因。

覆盖率报告应包含：

- 总体评分。
- 页面覆盖率。
- 功能覆盖率。
- API 覆盖率。
- 跨页面流程覆盖率。
- 存在 `ui-selector-audit.json` 时，包含选择器稳定性评分。

## 中文报告

最终面向人阅读的测试报告必须使用中文。写入 `tests/e2e/reports/summary.md` 时，使用 `assets/templates/summary.zh-CN.md.template`。

报告必须包含：

- 生成了哪些文件。
- 覆盖了哪些页面和路由。
- 生成的测试数量。
- 重新执行命令。
- 如果执行过测试，写明测试结果。
- 覆盖缺口。
- 总体评分和各维度评分。
- 选择器稳定性评分和主要选择器建议。
- 如果测试失败，写明失败修复摘要。
- 仍需人工提供的测试账号、环境变量或业务规则。

机器可读产物包括：

- Playwright HTML report。
- CI 需要时生成 JUnit XML。
- `ui-selector-audit.json`。
- `ui-test-coverage.json`。
- 失败时生成 `ui-test-repair-plan.json`。
- 中文 Markdown 总结：`tests/e2e/reports/summary.md`。

## 完成标准

任务只有在以下条件满足时才算完成：

- 测试套件文件已经生成。
- 清单、选择器审计和覆盖率报告已经存在。
- 测试已执行并修复，或报告了明确阻塞原因。
- 已提供可独立运行的本地或 CI 命令。
- 用户可以根据中文报告中的命令重新运行测试。
