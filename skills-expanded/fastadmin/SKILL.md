---
name: fastadmin
description: 用于 FastAdmin 后台二次开发、原生目录新增功能、CRUD 生成、数据库字段设计、字段命名规则、关联模型、关联字段显示、菜单权限、控制器、模型、验证器、JS、视图、语言包、SQL、已有源文件修改和插件源文件修改。用户提到 FastAdmin、后台模块、CRUD、php think crud、字段命名、关联表显示、菜单节点、权限节点、后台 JS、插件源文件修改或相关排错时应使用此 skill。
---

# FastAdmin 开发

## 执行边界

- 先定位 FastAdmin 项目根目录：必须包含 `think`、`application/`、`addons/`、`public/`。
- 所有框架路径均相对于当前项目根目录；不得写入本机模板绝对路径。
- 默认使用简体中文输出分析、执行结果和验证结论；代码、命令、路径、配置 key、错误信息保持原文。
- 新增功能默认落到 FastAdmin 原生目录；插件目录只允许明确修改原插件已有源文件或在原文件加方法。
- 不在 `addons/<plugin>` 下新增独立功能板块。

## 必读规则

按任务触发读取，不一次性加载所有 `references/`：

1. 任何任务先读 `references/01-ownership.md`，确定原生新增、已有源文件修改或插件源文件修改。
2. 涉及新表、新字段、新索引、状态值、外键或 SQL，读 `references/02-database-design.md`。
3. 新增标准后台数据管理模块，读 `references/03-native-crud.md`。
4. 新增原生页面或修改后台视图/JS，读 `references/04-native-frontend.md`。
5. 修改已有控制器、模型、服务、验证器、JS、视图或插件源文件，读 `references/05-existing-source-change.md`。

## 固定流程

1. 判定归属：新增一律原生；已有文件修改按当前文件；明确插件源文件修改才进入插件规则。
2. 判定项目根和当前项目实际命令：先检查 `php think`、`application/admin/command/Crud.php`、`application/admin/command/Menu.php`。
3. 涉及数据库时先完成字段设计，再决定是否执行 `php think crud`。
4. CRUD 前判断控制器层级、关联模型显示、字段识别、菜单路径；再构造最小必要命令。
5. CRUD 后生成菜单权限；菜单必须使用最终控制器路径。
6. 生成后复核 SQL、控制器、模型、验证器、视图、后台 JS、语言包、菜单权限、字段组件、关联显示。

## 硬性约束

- `php think crud` 是生成标准原生管理模块的方式，不决定任务归属。
- CRUD 默认命令优先，特殊参数后置；`--controller` 只用于项目层级归属，不用于解决字段组件、`pid`、selectpage 或减少页面改造。
- 数据库字段设计必须参考当前项目 `application/admin/command/Crud.php` 的字段识别规则。
- 列表需要显示关联表字段时，CRUD 命令必须加入 `--relation`、`--relationmode`、`--relationforeignkey`、`--relationprimarykey`、`--relationfields`。
- 树形父级字段默认使用 `pid`，不改成本表名 `_id`。
- 菜单权限优先用 `--menu=1` 或 `php think menu --controller=<controller>`；多个控制器可重复传入 `--controller`。

## 输出契约

- 实现前说明：任务归属、目标目录、是否需要数据库、是否适合 CRUD、是否需要关联模型、最终控制器路径、菜单生成方式。
- 实现后说明：实际执行命令、生成/修改的关键文件、菜单节点、验证结果、未验证项。
