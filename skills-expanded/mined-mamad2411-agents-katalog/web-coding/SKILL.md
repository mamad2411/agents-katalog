---
name: web-coding
description: Triflow Web 前端开发规范。包括 Vue 3.5 + Element Plus + TypeScript 组件编写、API 类型定义、Pinia 状态管理、VXE Table、样式规范等项目约定。在编写或修改 triflow-web 代码时必须遵循。
---

# Triflow Web 前端开发规范

> 本 Skill 定义了 Triflow Web（管理后台）的代码编写规范，所有代码变更必须遵守。

## 1. 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.5 | UI 框架 |
| Element Plus | 最新 | UI 组件库 |
| Vite | 7.x | 构建工具 |
| TypeScript | 5.9 | 类型系统 |
| Pinia | 最新 | 状态管理 |
| pnpm | 10.0.0+ | 包管理器 |
| Turbo | 最新 | Monorepo 构建 |

## 2. 项目结构

### 路径别名

`#/` 是 `web-admin/src/` 的别名（tsconfig.json 中配置 `"#/*": ["./src/*"]"`），用于应用内导入：

```typescript
import { request } from '#/api/request';
import type { UserVO } from '#/api/modules/user';
import StatusTag from '#/components/status/StatusTag.vue';
```

### 目录结构

```
triflow-web/
├── apps/
│   ├── web-admin/           # 管理后台应用（#/ 指向 src/）
│   │   └── src/
│   │       ├── api/         # API 接口定义
│   │       ├── components/  # 业务组件
│   │       ├── router/      # 路由配置
│   │       ├── store/       # Pinia 状态
│   │       └── views/       # 页面视图
│   └── backend-mock/        # Mock 服务器
├── packages/                # 共享包（@core, effects, utils 等）
└── internal/                # 内部工具链
```

### Views 目录结构

```
views/{module}/{feature}/
├── index.vue              # 列表页
├── detail.vue             # 详情页（可选）
├── components/            # 页面私有组件
│   ├── user-form.vue
│   └── user-table.vue
└── composables/           # 页面私有 hooks
    └── use-user.ts
```

---

## 3. 组件规范

### 必须使用 `<script setup lang="ts">`

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { UserVO } from '#/api/types';

// ==================== Props ====================
interface Props {
  /** 用户ID */
  userId: number;
  /** 是否只读 */
  readonly?: boolean;
}
const props = withDefaults(defineProps<Props>(), {
  readonly: false,
});

// ==================== Emits ====================
const emit = defineEmits<{
  (e: 'update', user: UserVO): void;
}>();

// ==================== State ====================
const loading = ref(false);

// ==================== Computed ====================
const displayName = computed(() => userInfo.value?.nickname);

// ==================== Methods ====================
async function fetchUser() { ... }

// ==================== Lifecycle ====================
onMounted(() => { fetchUser(); });

// ==================== Expose ====================
defineExpose({ refresh: fetchUser });
</script>
```

**代码区域顺序**：Props → Emits → State → Computed → Methods → Lifecycle → Expose

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | `kebab-case.vue` | `user-list.vue` |
| 组件导出名 | `PascalCase` | `UserList` |
| 变量/函数 | `camelCase` | `getUserList` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_PAGE_SIZE` |
| 类型/接口 | `PascalCase` | `UserVO` |
| CSS 类名 | `kebab-case` | `.user-card` |

### 优先使用已封装组件

| 场景 | 推荐组件 | 位置 |
|------|----------|------|
| 状态标签 | `StatusTag` | `#/components/status/` |
| 状态选择 | `StatusSelect`, `StatusSwitch` | `#/components/status/` |
| 富文本编辑 | `RichTextEditor` | `#/components/editor/` |
| 枚举下拉 | `EnumSelect` | `#/components/enum-select/` |
| 图片上传 | `ImageUpload` | `#/components/image-upload/` |
| 文件选择 | `FileSelect` | `#/components/file-select/` |

> 详细组件模式、表格规范、Hooks 模板见 [COMPONENTS.md](./COMPONENTS.md)

---

## 4. TypeScript 规范

### 禁止使用 `any`

```typescript
// ❌ 禁止
const data: any = {}
function handle(params: any) {}

// ✅ 必须定义明确类型
interface UserVO {
  id: number
  username: string
  status: number
}
```

### API 类型定义

每个 API 模块文件必须定义请求参数和响应类型：

```typescript
// api/modules/user.ts
import { request } from '#/api/request';
import type { PageResult } from '#/api/types';

/** 用户查询参数 */
export interface UserQueryDTO {
  keyword?: string;
  status?: number;
  pageNum: number;
  pageSize: number;
}

/** 用户信息 */
export interface UserVO {
  id: number;
  username: string;
  status: number;
  createTime: string;
}

export function getUserPage(params: UserQueryDTO) {
  return request.post<PageResult<UserVO>>('/base/user/page', params);
}

export function getUserDetail(id: number) {
  return request.get<UserVO>('/base/user/detail', { params: { id } });
}

export function createUser(data: UserCreateDTO) {
  return request.post<void>('/base/user/create', data);
}
```

### 类型导入规范

```typescript
// ✅ 使用 type 关键字导入类型
import type { UserVO, UserQueryDTO } from '#/api/modules/user';

// ✅ 混合导入时分开
import { ref, computed } from 'vue';
import type { Ref, ComputedRef } from 'vue';
```

---

## 5. 状态管理规范

### Pinia Store 定义

使用 Setup Store 写法（`defineStore` + 箭头函数）：

```typescript
export const useUserStore = defineStore('user', () => {
  // State
  const userInfo = ref<UserVO | null>(null);
  const token = ref<string>('');

  // Getters
  const isLoggedIn = computed(() => !!token.value);

  // Actions
  async function login(params: LoginParams) { ... }
  function logout() { ... }
  function $reset() { ... }

  return { userInfo, token, isLoggedIn, login, logout, $reset };
});
```

### Store 使用规则

```typescript
// ❌ 禁止直接解构响应式数据（会丢失响应性）
const { userInfo } = useUserStore();

// ✅ 使用 storeToRefs
import { storeToRefs } from 'pinia';
const userStore = useUserStore();
const { userInfo, isLoggedIn } = storeToRefs(userStore);
const { login, logout } = userStore;  // actions 可以直接解构
```

---

## 6. 样式规范

### CSS 预处理器与工具类

- 使用 **SCSS**
- 优先使用 **Tailwind CSS** 工具类
- 自定义样式使用 **BEM 命名**

```scss
.user-card {
  &__header { }
  &__body { }
  &--active { }
  &--disabled { }
}
```

### 样式书写顺序

1. 定位（position, z-index）
2. 盒模型（display, width, padding, margin）
3. 排版（font-size, color）
4. 视觉（background, border, shadow）
5. 其他（cursor, transition）

### useNamespace Hook

```typescript
import { useNamespace } from '@vben/composables';
const ns = useNamespace('button');
// ns.b() → 'vben-button', ns.e('text') → 'vben-button__text'
```

---

## 7. 枚举下拉组件（EnumSelect）

前端通过 `EnumSelect` 组件自动加载后端枚举选项：

```vue
<EnumSelect v-model="form.status" enum-class="ArticleStatus" />
<EnumSelect v-model="form.type" enum-class="ConfigTypeEnum" clearable filterable />
<EnumSelect v-model="form.categories" enum-class="CategoryEnum" multiple />
```

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enumClass` | `string` | - | 枚举类简称（必填） |
| `clearable` | `boolean` | `true` | 是否可清除 |
| `multiple` | `boolean` | `false` | 是否多选 |
| `filterable` | `boolean` | `false` | 是否可过滤 |

手动调用 API：

```typescript
import { getEnumOptions, getEnumNameByCode } from '#/api/base/enum';
const options = await getEnumOptions('ArticleStatus');
const name = await getEnumNameByCode('ArticleStatus', '1');  // "已发布"
```

> 后端枚举定义规范见 server-coding skill 的枚举章节。`enumClass` 参数为后端枚举类的简称。

---

## 8. 表单与表格

### 表单规范

使用 Element Plus 原生表单校验：

```vue
<script setup lang="ts">
const formRef = ref<FormInstance>();
const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' },
  ],
};
async function handleSubmit() {
  const valid = await formRef.value?.validate();
  if (!valid) return;
  // 提交逻辑
}
</script>
```

### 表格规范

优先使用 **VXE Table**（`useVbenVxeGrid`）处理大数据量表格，支持虚拟滚动、代理分页。

> 完整 VXE Table 配置模板和表单校验示例见 [COMPONENTS.md](./COMPONENTS.md)

---

## 9. 国际化

所有用户可见文案**必须**使用 `t()` 国际化函数：

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>
<template>
  <el-button>{{ t('common.submit') }}</el-button>
</template>
```

---

## 10. 错误处理

```typescript
/** 业务错误类型（由全局拦截器抛出） */
interface BusinessError extends Error {
  code: number;
  message: string;
}

async function handleSubmit() {
  try {
    await createUser(form);
    ElMessage.success('创建成功');
  } catch (error: unknown) {
    // 全局拦截器已处理通用错误（Toast 提示）
    // 这里仅处理需要特殊 UI 响应的业务逻辑
    const bizError = error as BusinessError;
    if (bizError.code === 101001) {
      // 用户已存在的特殊处理
    }
  }
}
```

---

## 11. 性能优化

- **路由懒加载**：`const UserList = () => import('#/views/system/user/index.vue')`
- **组件异步导入**：`defineAsyncComponent(() => import(...))`
- **VXE Table 虚拟滚动**：`:scroll-y="{ enabled: true, gt: 100 }"`
- **图片**：WebP 格式 + CDN + `loading="lazy"`

---

## 12. 新增组件

新增组件后请更新 `CHARTER.md`，包含：组件用途、Props 定义、使用示例、导入方式。
