---
name: keyblade-pro-code-rules
description: >
  当用户要求生成、修改或审查 Vue3 + TypeScript + Arco Design 子项目代码时触发。
  覆盖 kb-pro-table / useTable / useForm 使用规范、arco design + unocss 样式规则。
  模块组织与命名规范、枚举与类型约束、ref 优先的响应式规范等。
  无论用户是否明确提到"规范"或"规则"，只要涉及 Vue3 + TypeScript + Arco Design 子项目的代码编写就应使用此 skill。
---

# 项目编码规范

## 适用范围

本项目是 **pnpm monorepo**，包含多个子项目。本规范**仅适用于使用以下技术栈的子项目**：

- vue3 + TypeScript + vite + arco design + unocss

**判断方式**：查看目标目录下是否有 `vite.config.ts` 且 `package.json` 中包含上述依赖。

如果用户操作的是 Vue2、React、Node.js 等其他技术栈的子项目，**不适用**本规范中的 Vue3 专属规则（如表格页规范、组件规范、样式规范、响应式规范、自动导入等），但通用规则（如文件命名规范、注释规范）仍然建议遵循。

## 技术栈

vue3 + TypeScript + vite + arco design + unocss

## 表格页规范【Vue3 专属】

常规列表页必须遵循以下模式，参考 `web/src/views/components-document/query-table/index.vue`：

1. **必须使用 `kb-pro-table`** 作为表格组件
2. **表格逻辑尽量使用 `useTable`** hooks，从 `@/hooks` 导入
3. **弹窗式编辑优先**：新增、编辑操作建议使用弹窗式实现（`save.modalComponent` 配置）
4. **表单尽量使用 `useForm`**，从 `@/hooks` 导入
5. 多表格页面必须拆分为多个独立组件

### useTable 配置要点

- query.fn：请求函数，严禁在组件内做复杂数据处理，建议放到 request.ts 中
- remove.beforeFn：删除前确认逻辑
- save.modalComponent：弹窗编辑组件

### 表格列定义

- 使用 `IProTableColumn` 类型
- 字段名使用字符串，方便编辑器可以点击跳转到定义处
- 通过 `setColumnAlign(columns, 'center')` 设置默认居中

## 组件规范【Vue3 专属】

- 使用 arco design 组件库，文档参考 https://arco.design/vue/component
- 自定义组件需类型完备，props 必须声明类型和必要的注释

## 样式规范【Vue3 专属】

- **优先使用 unocss**，避免在 `<style>` 标签中定义 class
- arco design 组件上使用 unocss 时，若出现样式覆盖冲突，加 `!` 前缀强制生效
- 示例：`<a-button class="!bg-red-500">`

## 模块组织规范【通用】

`modules/` 下按业务模块创建以下文件：

| 文件 | 用途 |
|------|------|
| `index.ts` | 统一导出 |
| `request.ts` | API 请求 + mock 数据 |
| `type.ts` | 类型定义 |
| `enum.ts` | 枚举定义 |

**每个字段必须有完整注释。**

### request.ts 规范

参考 `web/src/modules/example/request.ts`：

1. **namespace 组织**：使用 `namespace 模块名Request` 包裹所有接口函数
2. **HTTP 方法对应**：从 `@keyblade/http` 导入 `getRequest` / `postRequest` / `putRequest` / `deleteRequest`
3. **URL 前缀**：使用 `AppConfig.apiPrefix` 拼接路径
4. **try/catch 包裹**：每个请求函数必须 try/catch，错误处理在 request 层完成
5. **错误码判断**：成功/失败必须使用 `EResponseCode` 枚举值，如 `res?.code === EResponseCode.success`
6. **类型声明**：已知返回值类型时必须显式声明到 `getRequest<T>` / `postRequest<T>` 中，优先让 TypeScript 自动推导
7. **数据处理**：格式转换、错误处理等逻辑尽量放到 request 层，减少渲染层代码量

**示例：**
```ts
import { getRequest, postRequest, putRequest, deleteRequest } from '@keyblade/http'
import { AppConfig } from '@/configs/app'
import { EResponseCode } from '@/enums'
import type { IExample } from './type'

const { apiPrefix } = AppConfig

export namespace ExampleRequest {
  export async function listPage(params: { pageNum: number; pageSize: number }) {
    try {
      const res = await getRequest<{ data: { list: IExample[]; total: number } }>(
        apiPrefix.main + '/',
        params
      )
      if (res?.data) {
        return res.data
      }
    } catch {}
  }

  export async function add(params: object) {
    try {
      const res = await postRequest(apiPrefix.main + '/', params)
      return res?.code === EResponseCode.success
    } catch {}
    return false
  }
}
```

### type.ts 要求

1. type/interface 变量名前缀：`I + 父级完整模块名 + 子模块名首字母简写`

**示例：**
```ts
export type IUserManagementUM = {
  /** 用户ID */
  id: string
  /** 用户名称 */
  name: string
}
```

### enum.ts 要求

1. enum 变量名前缀：`E + 父级完整模块名 + 子模块名首字母简写`

**示例：**
```ts
export enum EUserManagementUM {
  /** 正常 */
  Normal = 1,
  /** 冻结 */
  Frozen = 2,
}
```

## 类型规范【通用】

- 状态切换、选项值等**禁止使用字符串字面量**，必须定义枚举
- 下拉选项使用 `ValueMap` 或 `Dict` 结构，配合 `tag-enum` 组件展示

**错误示例：**
```ts
const status = 'all' // 禁止
```

**正确示例：**
```ts
const status = EStatus.All
```

## 响应式规范【Vue3 专属】

- **优先使用 `ref`**，只在特殊场景下使用 `reactive`
- ref 访问值时必须 `.value`，模板中自动解包

## 自动导入【Vue3 专属】

项目已配置 `unplugin-auto-import` 插件，Vite 会自动注入以下 API，**代码中禁止显式导入**：

- `vue`：`ref`、`reactive`、`computed`、`watch`、`watchEffect`、`onMounted`、`onUnmounted`、`defineProps`、`defineEmits`、`defineExpose` 等
- `pinia`：`defineStore`、`storeToRefs` 等
- `vue-router`：`useRoute`、`useRouter` 等

**错误示例：**
```ts
import { ref, computed } from 'vue'        // 禁止
import { defineStore } from 'pinia'        // 禁止
import { useRoute } from 'vue-router'      // 禁止
```

**正确示例：**
```ts
const count = ref(0)                       // 直接可用
const double = computed(() => count.value * 2)
```

## 表单规范【Vue3 专属】

- 使用 `a-form` + `useForm` 组合
- 校验规则必须写 `message` 提示
- 弹窗表单需暴露 `submit` 和 `beforeCancel` 方法

## 文件命名规范【通用】

- **禁止使用驼峰命名（camelCase）**
- 文件名使用短横线分隔（kebab-case）
- 示例：`user-management` ✓，`userManagement` ✗

## ESLint 规范【通用】

- 生成的代码必须符合目标项目的 ESLint 配置
- 使用项目根目录下的 `.eslintrc` 或 `.eslintrc.*` 或 `eslint.config.*` 文件定义的规则
- 避免产生任何 ESLint 警告或错误
- 代码格式需通过项目的 lint 命令校验

## 注释规范【通用】

- 所有类型字段必须有完整注释
- 复杂逻辑必须加行注释说明原因
- props 必须注释说明用途

