---
name: piying-view-developer
description: 皮影(Piying-view)表单开发文档 — 用于使用 Schema + Valibot 跨框架构建表单。当需要以下内容时使用：将自然语言需求自动转换为 piying Schema、注册自定义组件/控件、实现表单验证、处理动态行为（条件禁用/隐藏/值监听/字段联动）、布局控制（包装器组合/layout移动/分组容器）、值转换与输出控制（transformer/防抖/updateOn）。
---

# 皮影客户端表单开发技能

皮影是一个基于 Schema + Valibot 的跨框架表单解决方案。

## 一、入门

### [快速开始](./references/quick-start.md)

安装依赖、创建第一个表单组件（各框架示例）、包装器实现。包含完整代码示例。

---

## 组件渲染控制

### [setComponent — 指定字段使用的组件](references/set-component-api.md)

为 schema 中的字段指定渲染时使用的 Angular 组件（字符串映射或类引用）。

- **使用场景**
  - 通过自定义组件名注册映射表
  - 直接传入组件类避免配置查找

### [layout — 控制字段布局位置与顺序](references/layout-api.md)

精确控制字段在表单中的父容器归属、同级排序及跨层级重定位。

- **使用场景**
  - 将字段移动到其他分组或容器中
  - 调整同一层级内多个字段的显示先后
  - 实现复杂的非线性布局结构

### [asVirtualGroup / asControl / nonFieldControl — 控制渲染结构](references/asvirtualgroup-asc.control-nonfieldcontrol-api.md)

控制字段的分组行为和控件特性，影响字段树结构。

- **使用场景**
  - `v.intersect` 合并对象时避免产生逻辑分组
  - 将容器视为独立控件（不嵌套 FormControl）
  - 定义非表单控件（无原生表单绑定）

### [renderConfig — 控制字段渲染状态](references/render-config-api.md)

通过静态或动态方式控制字段是否渲染到页面。

- **使用场景**
  - 根据条件决定是否渲染某个字段

---

## 条件控制

### [condition — 按环境切换配置](references/condition-api.md)

为同一字段定义多套配置，在不同运行环境中自动应用不同行为。

- **使用场景**
  - 开发/测试/生产环境使用不同的组件或属性
  - A-B 实验通过环境参数切换不同 UI
  - 同 Schema 适配多套业务规则

### [hideWhen — 动态控制字段显示/隐藏](references/hide-when-api.md)

监听字段值变化，自动切换当前字段的 `hidden` 状态。

- **使用场景**
  - 联动隐藏：某选项改变时隐藏关联字段
  - 条件过滤：根据用户选择隐藏不相关输入
  - 隐藏时同时禁用其他依赖字段

### [disableWhen — 动态控制字段禁用状态](references/disable-when-api.md)

监听字段值变化，自动切换当前字段的 `disabled` 状态。

- **使用场景**
  - 联动禁用：某些条件满足时启动/禁止编辑
  - 表单只读模式切换
  - 根据其他字段的值决定当前字段是否可交互

---

## 值与事件监听

### [valueChange — 监听字段值变化](references/value-change-api.md)

订阅任意字段（包括跨字段）的值变化，通过 RxJS Observable 回调。

- **使用场景**
  - 实时汇总计算
  - 基于其他字段值做联动处理
  - 自定义数据持久化逻辑

### [outputChange — 监听字段 output 事件](references/output-change-api.md)

订阅字段或跨字段的 `output` 事件触发，非值变化类的事件监听。

- **使用场景**
  - 监听按钮点击等 UI 交互事件
  - 组件自定义事件响应
  - 跨字段事件流转

---

## 数据属性操作（Actions）

### [actions.inputs — 设置组件输入属性](references/actions-inputs-api.md)

同步或异步地设置、更新、移除组件的 `@Input` 属性。

- **使用场景**
  - 向子组件传递动态配置项
  - 增量更新部分输入属性而不影响其他
  - 通过 Signal/Observable 驱动输入值

### [actions.outputs — 设置组件输出事件](references/actions-outputs-api.md)

同步或异步地定义、更新、移除组件的 `@Output` 事件处理器。

- **使用场景**
  - 为子组件绑定自定义事件回调
  - 动态注册/注销事件监听
  - 多条件组合的事件处理策略

### [actions.events — 操作 DOM 事件](references/actions-events-api.md)

直接给组件或 Wrapper 的 DOM 元素添加事件监听器。

- **使用场景**
  - 添加 `click`、`mouseenter` 等原生 DOM 事件
  - 动态绑定/替换事件处理函数
  - 为复杂交互提供细粒度事件控制

### [actions.attributes — 操作 DOM 属性](references/attributes-actions-api.md)

同步或异步地设置、更新、移除组件和 Wrapper 的 DOM Attributes。

- **使用场景**
  - 动态添加 `data-*` 自定义属性用于测试或埋点
  - 设置 `id`、`title`、`placeholder` 等 HTML 属性
  - 根据状态切换 `readonly`、`required` 等布尔属性

### [actions.class — 动态设置 CSS Class](references/actions-class-api.md)

同步或异步地为组件自身或 Wrapper 元素设置 CSS class。

- **使用场景**
  - 条件添加高亮、错误提示等样式类
  - Wrapper 与组件分别应用不同 class
  - 通过 Signal/Observable 动态切换样式

### [actions.providers — 注入依赖（Provider）](references/actions-providers-api.md)

在 Schema 定义中注入自定义 Angular Provider，供组件或钩子函数使用。

- **使用场景**
  - 为组件提供 API Client、配置服务等外部依赖
  - 测试时替换 mock 实现
  - 运行时工厂函数动态创建实例

---

## 表单配置

### [formConfig — 表单运行时行为配置](references/formconfig-api.md)

通过 Valibot Pipe Action 配置字段的校验规则、值转换、默认值等表单属性。

- **使用场景**
  - 自定义同步/异步校验器
  - 实现 model/view 之间的值转换逻辑
  - 设置字段默认值和禁用策略
  - 控制表单更新触发时机（change/blur/submit）

---

## 路径与别名查询

### [field-query-path — Field 路径查询指南](references/field-query-path-guide.md)

`get(keyPath)` 方法的完整路径语法参考，支持根节点、父级、别名等导航方式。

- **使用场景**
  - 在任意位置查找表单树中的目标字段
  - 向上导航到父级或跳转到根节点
  - 通过 `@别名` 快速定位已注册的字段

### [setAlias — 为字段设置别名](references/setalias-api.md)

给字段注册一个易记的别名，后续通过 `@别名` 语法查询。

- **使用场景**
  - 为深层嵌套字段设置简短别名
  - 跨层级快速获取指定字段引用
  - 配合 `keyPath` 简化路径书写

## 高级

- [将自然语言需求转为 Schema](./references/natural-language-to-schema.md)
