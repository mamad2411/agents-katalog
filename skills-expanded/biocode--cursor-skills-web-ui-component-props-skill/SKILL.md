---
name: component-props
description: 在组件对应 Service 文件中定义 XxxProps 接口（仅 Props，不含 Emits/useXxx）。当需要"定义组件Props/组件属性/Props接口/透传属性/包装组件参数"时使用本 Skill，格式对齐 InputOrgTreeProps。
---

# 组件 Props 定义指南

> 本 Skill **只负责** `{组件名}Props` 的 `export interface` 定义。不编写 `Emits`、`useXxx`、业务逻辑。

## 1. 选型

| 业务诉求 | 方案 | 说明 |
| --- | --- | --- |
| 可复用公共组件（`views/**/public/`、`components/`） | 在 `{组件名}Service.ts` 定义 `export interface XxxProps` | 与 SFC 同名的 Service 文件顶部导出，SFC 用 `defineProps<XxxProps>()` |
| 页面私有、一次性弹窗 | 在 SFC 内 `interface Props` | 不单独建 Props 接口文件 |
| 列表/表格子组件数据契约 | 在 Api 文件定义 `XxxTableProps` | 见 WebUiApiMR，不走本 Skill |

统一规则：**公共组件 Props 必须放在 Service 文件**，禁止在 SFC 内重复声明同名 Props。

## 2. 快速接入

1. 确认组件 SFC 路径，得到组件名 `Xxx`（如 `InputOrgTree.vue` → `InputOrgTree`）
2. 在同级或 `service/` 目录创建/打开 `XxxService.ts`
3. 仅 `import type` 引入 Props 字段用到的 Api 类型（`GetXxxVo` 等）
4. 在文件最上方（`export default` 之前）按模板编写 `XxxProps` 块
5. SFC 中 `import type { XxxProps } from ".../XxxService"` 并 `defineProps<XxxProps>()` + `withDefaults`

## 3. 参数契约

### 命名与位置

| 项 | 约定 |
| --- | --- |
| 接口名 | `{组件名}Props`，与 SFC 文件名一致（不含 `.vue`） |
| 导出 | `export interface`，禁止 `type` 别名 |
| 文件 | `views/<域>/public/service/XxxService.ts` 或 `views/<域>/components/service/XxxService.ts` |
| 顺序 | Import → **JSDoc + XxxProps** →（本 Skill 不涉及 Emits / default） |

### JSDoc 块（interface 正上方，必填）

```ts
/**
 * {组件中文名}参数
 * 其他未声明 props 全量透传给{子组件名} 具体参考 @see {子组件}.vue
 *
 * 双向绑定 v-model 参数
 * v-model / v-model:xxx — {类型与含义，逐行列出}
 */
```

- `v-model` / `defineModel` **不得**写入 `XxxProps`，只在 JSDoc「双向绑定」段说明
- 透传子组件时写清 `@see` 目标 SFC 或第三方类型（如 `DialogProps`）

### 字段规则

| 规则 | 说明 |
| --- | --- |
| 注释 | 每个字段上方一行 `//中文说明`，与 `InputOrgTreeProps` 一致 |
| 可选性 | 业务 Props 默认全部 `?`；必填项由 SFC `defineModel({ required: true })` 承担 |
| 类型 | 优先 Api 层 `GetXxxVo` / `GetXxxListVo`；字面量联合用 `"a" \| "b"` |
| 回调 | 方法型 Props 注明语义，如「返回 `false` 则排除该节点」 |
| 禁止 | 不在 Props 中写 `modelValue`、`update:modelValue`、emit 事件名、ref/reactive |

## 4. 模板（Templates）

### 包装型输入组件（透传 Modal）

```ts
import type { GetOrgListVo, GetOrgTreeVo } from "@/views/core/api/OrgApi";

/**
 * 输入组织机构选择器参数
 * 其他参数全部透传给内部的 ModalOrgTree 组件 具体参考 ModalOrgTree 组件的属性说明 @see ModalOrgTree.vue
 *
 * 双向绑定 v-model 参数
 * v-model 已选组织机构 ID 数组
 * v-model:checked-org-names 已选组织机构名称
 */
export interface InputOrgTreeProps {
  //输入框占位符
  placeholder?: string;

  //是否只读
  readonly?: boolean;

  //排除节点方法 如果返回 false 则排除该节点
  excludeNodeMethod?: (node: GetOrgTreeVo) => boolean;

  //禁用节点方法 如果返回 false 则禁用该节点
  checkEnableMethod?: (node: GetOrgTreeVo) => boolean;

  //是否禁用
  disabled?: boolean;
}
```

### 模态框组件（透传 Dialog + 模式）

```ts
import type { GetOrgTreeVo } from "@/views/core/api/OrgApi";

/**
 * 模态组织机构选择器参数
 * 其他未声明 props 全量透传给底层的 OrgTree 组件 具体参考 OrgTree 组件的属性 @see OrgTree.vue
 *
 * 双向绑定 v-model 参数
 * v-model 模态框显隐控制
 * v-model:checked-org-ids 当前已勾选组织机构 ID 数组 不管单选多选都是数组
 */
export interface ModalOrgTreeProps {
  //模态框标题
  title?: string;

  //模态框宽度
  width?: string | number;

  //模式: 单选、多选
  mode?: "single" | "multiple";

  //是否只读
  readonly?: boolean;

  //限制选择组织机构数量
  max?: number | null;

  //组织树裁剪根 ID 将会以该 ID 为根节点进行裁剪 只显示该组织及下级组织
  cropOrgId?: string | null;

  //是否级联选择
  checkCascade?: boolean;

  //排除节点方法 如果返回 false 则排除该节点
  excludeNodeMethod?: (node: GetOrgTreeVo) => boolean;

  //禁用节点方法 如果返回 false 则禁用该节点
  checkEnableMethod?: (node: GetOrgTreeVo) => boolean;
}
```

### 极简 Props（仅展示类）

```ts
import type { GetCoreRootListVo } from "@/views/core/api/CoreRootApi";

/**
 * 租户菜单包绑定弹窗参数
 *
 * 双向绑定 v-model 参数
 * （无，显隐由父组件 props.visible 控制）
 */
export interface RootRpModalProps {
  visible: boolean;

  data?: GetCoreRootListVo | null;
}
```

### SFC 引用方式（仅 Props 相关片段）

```ts
import XxxService, { type XxxProps } from "@/views/<域>/public/service/XxxService";

const props = withDefaults(defineProps<XxxProps>(), {
  placeholder: "请选择",
  readonly: false,
});
```

`withDefaults` 的 key 必须与 `XxxProps` 字段名一致；默认值只写在 SFC，不写在 interface。

## 5. 陷阱（Traps）

```ts
// ❌ 把 v-model 写进 Props
export interface XxxProps {
  modelValue?: boolean;
  checkedOrgIds?: string[];
}
```

```ts
// ❌ 在 Props 文件里写 Emits / useXxx（本 Skill 范围外，且易混文件职责）
export interface XxxEmits { ... }
export default { useXxx() { ... } };
```

```ts
// ❌ 字段无 // 注释、用 type 别名
export type XxxProps = { title?: string };
```

```ts
// ❌ 在 Api 文件定义公共组件 Props（应放 Service）
// OrgApi.ts
export interface InputOrgTreeProps { ... }
```

```ts
// ✅ v-model 只在 JSDoc 说明，Props 只含业务透传字段
/**
 * 双向绑定 v-model 参数
 * v-model:checked-user-ids 当前已选用户 IDS
 */
export interface InputUserSelectorProps {
  placeholder?: string;
  readonly?: boolean;
}
```

## 6. 源码索引

- `src/main/resources/web-ui/src/views/core/public/service/InputOrgTreeService.ts` — `InputOrgTreeProps` 标准样例
- `src/main/resources/web-ui/src/views/core/public/service/ModalOrgTreeService.ts` — 模态框 + 透传 OrgTree
- `src/main/resources/web-ui/src/views/core/public/service/InputUserSelectorService.ts` — 极简 Props
- `src/main/resources/web-ui/src/views/core/public/InputOrgTree.vue` — `defineProps<InputOrgTreeProps>()` 用法
- `.cursor/rules/web-ui/module/WebUiServiceMR.mdc` — Service 层通用规范（列表页；组件 Props 为例外）
