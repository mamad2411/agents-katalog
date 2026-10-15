---
name: "fastadmin-addon-dev"
description: "FastAdmin插件开发引导工具。当用户要创建FastAdmin插件、开发插件功能、生成插件骨架代码时调用。通过多轮对话确认需求后自动生成符合规范的插件代码。"
---

# fastadmin-addon-dev

当用户要开发 FastAdmin 插件时调用本 skill。AI 通过多轮对话，按 Phase 0→4 顺序逐项确认需求（插件标识、数据库、菜单、配置、前台），每个关键节点用 GATE 阻塞，确认通过后才进入下一步，最终一次性生成符合 FastAdmin 规范的全部插件代码。

本 skill 只负责"什么时候问什么、什么时候停、什么时候生成"的流程编排，具体代码规范统一遵循 `references/addon-spec.md`。

## Behavior

- 默认进入多轮对话模式，从 Phase 0 开始顺序推进
- 每次只问当前步骤的问题（一个步骤内可展示多个关联项作为一个确认单元，但整体只等一次回复）
- 不跳过任何 GATE 确认门，必须等用户显式确认后才能继续
- 生成代码时严格遵循 `references/addon-spec.md` 中的全部规范
- 用户回答"跳过"或"你看着办"时，该模块使用 AI 的默认建议，但仍需展示默认值并等用户确认

## Primitives

### 生成插件文件

根据多轮对话收集的配置，在 Phase 4 一次性生成以下文件（直接写入工作目录的 `addons/插件标识/` 路径下）：

| 文件 | 必需 | 说明 |
|------|------|------|
| `info.ini` | 是 | 插件基础信息（name/title/intro/author/version 等） |
| `Mydemo.php` | 是 | 核心：`$menu` 菜单数组 + install/uninstall/enable/disable/upgrade |
| `install.sql` | 视情况 | 数据库建表语句（有数据表时必需） |
| `config.php` | 视情况 | 插件配置项（无配置则不显示配置按钮） |
| 后台控制器 | 是 | `addons/插件标识/application/admin/controller/插件标识/` 下 |
| 后台模型 | 是 | `addons/插件标识/application/admin/model/插件标识/` 下 |
| 验证器 | 是 | `addons/插件标识/application/admin/validate/` 下 |
| 后台视图 | 是 | `addons/插件标识/application/admin/view/插件标识/` 下（index/add/edit，有 deletetime 时含 recyclebin） |
| 后台 JS | 是 | `addons/插件标识/public/assets/js/backend/插件标识/` 下 |
| 语言包 | 是 | `addons/插件标识/application/admin/lang/zh-cn/插件标识/` 下 |
| 前台控制器 | 视情况 | `addons/插件标识/controller/` 下（需要前台页面时） |
| `bootstrap.js` | 视情况 | 全局 JS（需要注册外部 JS 或 configInit 时） |
| `testdata.sql` | 视情况 | 测试数据 |

> CRUD 文件（控制器/模型/验证器/视图/JS/语言包）的字段映射规则严格遵循 `references/addon-spec.md` 第 17 节。代码生成时**直接读取 `references/stubs/` 下的 `.stub` 模板文件**，按 `{%占位符%}` 替换为实际值，确保与 `php think crud` 输出一致。

## 对话流程

按以下 Phase 0→4 顺序推进。每个 Phase 内按编号步骤逐步询问，遇到 GATE 必须停下等用户确认。

### Phase 0 — 需求理解

**目标**：理解用户要做什么插件，确定插件标识。

1. **理解功能描述**
   - 问："这个插件要实现什么功能？请描述核心场景和目标用户。"
   - 等待用户描述，不要急着提方案。

2. **提炼插件标识**
   - 根据描述提出 2-3 个标识建议（全小写英文单词或拼音首字母，≥3 字符，仅 `a-z`）。
   - 展示建议列表，让用户选一个或自定义。

3. **确认标题和简介**
   - 生成中文标题和一句话简介，展示给用户确认。

🚧 **GATE 1**：插件标识、标题、简介全部确认后，才能进入 Phase 1。必须等用户回复"确认"或等价表述。

### Phase 1 — 数据库设计

**目标**：确认数据表结构并生成 install.sql。

1. **提出表结构建议**
   - 根据功能需求提出需要哪些表，逐表展示字段清单（字段名、类型、说明）。

2. **确认字段规范**
   - 自动检查字段命名是否符合规范：时间字段以 `time` 结尾且 `bigint(16)`；关联字段以 `_id` 结尾；状态字段用 `enum`；可数名词加 `s`。
   - 如有违规，主动修正并说明原因，再展示修正后的版本。

3. **确认特殊字段**
   - 逐一询问是否需要：`user_id`（关联会员）、`category_id`（关联分类）、`weigh`（排序）、`deletetime`（回收站）、`status`（TAB 选项卡）。

4. **生成 install.sql**
   - 根据确认的表结构生成完整 install.sql，表名以插件标识开头并使用 `__PREFIX__` 前缀，`CREATE TABLE` 前无空格，无 `DROP/DELETE`。
   - 展示完整 SQL，等用户确认。

🚧 **GATE 2**：install.sql 确认后才能进入 Phase 2。

### Phase 2 — 菜单与控制器

**目标**：确认后台菜单层级、控制器列表和 `$menu` 配置。

1. **提出菜单结构**
   - 根据数据表提出后台菜单层级，用缩进列表展示，例如：
     ```
     文章管理 (mydemo)
     ├── 文章列表 (mydemo/article)
     │   ├── 查看 (mydemo/article/index)
     │   ├── 添加 (mydemo/article/add)
     │   ├── 编辑 (mydemo/article/edit)
     │   ├── 删除 (mydemo/article/del)
     │   └── 批量更新 (mydemo/article/multi)
     └── 分类管理 (mydemo/category)
         └── ...
     ```

2. **确认控制器列表**
   - 每个菜单层级对应哪个后台控制器，确认 CRUD 方法列表（`index/add/edit/del/multi`，无需的功能用空方法阻止继承）。

3. **展示 $menu 配置**
   - 生成 `$menu` 数组（PHP 代码）：首个 `name` 必须与插件标识相同，子菜单 `name` 必须以 `插件标识/` 开始。等用户确认。

4. **展示 Mydemo.php 核心结构**
   - 展示 `install/uninstall/enable/disable/upgrade` 方法（调用 `Menu::create/delete/enable/disable/upgrade`），确认菜单注册逻辑。

🚧 **GATE 3**：菜单结构、控制器列表、`$menu` 配置全部确认后才能进入 Phase 3。

### Phase 3 — 配置与前台

**目标**：确认插件配置、前台功能、行为事件和 JS 模块。

1. **确认配置项**
   - 建议需要的 `config.php` 配置项，逐项展示 name、title、type、默认值。用户选择保留/删除/新增。

2. **确认前台功能**
   - 询问是否需要前台页面（`controller/` 下）、是否需要会员中心菜单（`userSidenavAfter`）、是否需要 API 接口。
   - 如果用户需要 API 接口，自动应用以下默认规则并告知用户：
     - **鉴权方式**：Header 中使用 `Authorization: Bearer {密钥}`
     - **密钥配置**：自动在 `config.php` 中增加 `apikey` 配置项（`type: string`），供用户在后台设置密钥
     - **入参格式**：默认 `body JSON` 格式
     - **返回格式**：统一返回 JSON 格式结果
     - **返回结构**：`{"code": 1, "msg": "success", "data": {...}}`（code=1 成功，code=0 失败）

3. **确认行为事件**
   - 询问是否需要注册行为（列出可用标签位：`config_init`、`upload_after`、`login_init` 等）。如需要，确认方法名（必须驼峰式，如 `uploadAfter`）。

4. **确认 JS 模块**
   - 询问是否需要 `bootstrap.js` 全局 JS。如需要，确认引入的外部 JS 和 RequireJS 配置，以及是否需要 `configInit` 渲染配置到前台。

🚧 **GATE 4**：所有配置项、前台功能、行为事件、JS 模块全部确认后，进入最终生成。

### Phase 4 — 代码生成

**目标**：汇总确认后，一次性生成全部插件文件。

1. **汇总确认**
   - 展示一份完整的配置摘要（插件标识、标题、数据表、后台菜单、配置项、前台功能、行为事件、JS 模块），最后确认一次。

2. **生成代码**
   - 🚧 **GATE 5（FINAL）**：用户确认汇总后，使用 `Write` 工具将全部文件**实际写入到工作目录**的 `addons/插件标识/` 路径下，按以下顺序生成：
     1. `info.ini`
     2. `Mydemo.php`（`$menu` + install/uninstall/enable/disable/upgrade）
     3. `install.sql`
     4. `config.php`（如有配置）
     5. 后台控制器（`addons/插件标识/application/admin/controller/插件标识/`）
     6. 后台模型（`addons/插件标识/application/admin/model/插件标识/`）
     7. 验证器（`addons/插件标识/application/admin/validate/`）
     8. 后台视图（`addons/插件标识/application/admin/view/插件标识/`，含 index/add/edit，有 deletetime 时含 recyclebin）
     9. 后台 JS（`addons/插件标识/public/assets/js/backend/插件标识/`）
     10. 语言包（`addons/插件标识/application/admin/lang/zh-cn/插件标识/`）
     11. 前台控制器（`addons/插件标识/controller/`）（如有）
     12. `bootstrap.js`（如有）
     13. `testdata.sql`（如有）
   - **CRUD 文件（5-13）的生成规则**：先根据 install.sql 生成 `fields.json`（字段定义），再调用 `generate_crud.py fields.json` 脚本生成等价于 `php think crud` 的代码，或由 AI 按 `references/addon-spec.md` 第 17 节映射规则手动生成。生成后用 `Write` 工具写入对应路径。
   - 生成完成后，在对话中输出**已生成文件清单**（文件路径 + 行数），供用户核对。
   - 生成时严格遵循 `references/addon-spec.md` 中的命名规则、目录结构、控制器模板、数据库规范等全部章节。

3. **输出检查清单**
   - 展示开发检查清单（参照 `references/addon-spec.md` 第 18 节的 12 项），提醒用户按清单验证生成结果。

## General rules

- **Never skip** 任何 GATE，即使用户说"你看着办"或"全部用默认"，也必须展示默认值并等用户确认。
- **Never skip** Phase 1 的字段规范自动检查，发现违规必须主动修正并说明原因。
- **Never skip** Phase 4 的汇总确认（GATE 5），汇总通过后才能开始生成代码。
- 用户说"跳过"时，该模块使用 AI 默认建议，但仍需展示默认值让用户确认后才算通过 GATE。
- 每个 Phase 的问题一次只问一个步骤，不要一次性抛出多个步骤的问题。
- 如果用户中途修改了前面的决定，需要重新确认受影响的后续步骤，不要直接沿用旧决定。
- 生成 `install.sql` 时，表名必须以插件标识开头，使用 `__PREFIX__` 前缀，禁止 `DROP TABLE`、`DELETE FROM`。
- 后台控制器的 `index/add/edit/del/multi` 等方法必须注册到菜单规则中，禁止配置到 `$noNeedLogin` 或 `$noNeedRight`。
- 行为方法名必须使用驼峰式（如 `uploadAfter` 而非 `upload_after`），缓存必须使用 `tag('插件标识')`。

## 响应格式

采用纯 Markdown 文本，不使用 `ui` JSON 块。需要用户选择时，用编号列表或表格展示选项，请用户在普通聊天文本中回复。关键确认点统一用"请回复 **确认** 继续，或说明需要修改的地方"句式。

### 示例：Phase 1 提问模板（字段表格）

```md
### 数据库设计

根据你的功能需求，我建议创建以下数据表：

**1. 文章表 `__PREFIX__mydemo_article`**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int(10) | 主键 |
| title | varchar(255) | 标题 |
| content | text | 正文 |
| user_id | int(10) | 作者ID |
| createtime | bigint(16) | 创建时间 |
| updatetime | bigint(16) | 更新时间 |
| deletetime | bigint(16) | 删除时间 |
| status | enum('normal','hidden') | 状态 |

请确认：
1. 表名和字段是否正确？
2. 是否需要调整或添加字段？

请回复 **确认** 继续，或说明需要修改的地方。
```

### 示例：GATE 确认模板

```md
---

以上是数据库设计部分。请确认后回复 **确认** 进入菜单设计，
或说明需要调整的地方。
```
