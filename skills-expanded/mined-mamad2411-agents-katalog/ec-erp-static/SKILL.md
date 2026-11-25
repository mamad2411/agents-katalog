# EC-ERP 静态前端项目规范

## 项目概述
这是一个基于 TDesign 的 ERP 系统前端项目，使用 Vue 3 + TypeScript + Vite 2 + Pinia 构建。
项目包含供应链管理、仓库管理、销售统计等核心功能模块。

## 技术栈
- **框架**: Vue 3.2.45 (Composition API)
- **构建工具**: Vite 2.9.15
- **语言**: TypeScript 4.8.4
- **状态管理**: Pinia 2.0.11 + pinia-plugin-persistedstate
- **路由**: Vue Router 4.0.11
- **UI 组件库**: TDesign Vue Next 0.24.9
- **HTTP 客户端**: Axios 0.27.2
- **图表**: ECharts 5.4.0
- **工具库**: Lodash 4.17.21, Dayjs 1.11.6, Moment 2.29.4
- **代码规范**: ESLint + Prettier + Stylelint
- **样式**: Less 4.1.1

## 项目结构
```
src/
├── apis/              # API 接口层
│   ├── dto/          # 数据传输对象定义
│   └── *Apis.ts      # 各模块 API 接口
├── assets/           # 静态资源（图片、字体等）
├── components/       # 公共组件
├── config/           # 配置文件（代理、主题、全局配置）
├── constants/        # 常量定义
├── hooks/            # 可复用的组合式函数
├── layouts/          # 布局组件
├── pages/            # 页面组件
│   ├── dashboard/    # 数据看板
│   ├── supply/       # 供应链管理
│   ├── user/         # 用户相关
│   └── warehouse/    # 仓库管理
├── router/           # 路由配置
│   └── modules/      # 路由模块
├── store/            # Pinia 状态管理
│   └── modules/      # 状态模块
├── style/            # 全局样式
├── types/            # TypeScript 类型定义
├── utils/            # 工具函数
├── App.vue           # 根组件
├── main.ts           # 入口文件
└── permission.ts     # 权限控制

mock/                 # Mock 数据
├── api/              # Mock API
│   └── data/         # Mock 数据文件
└── index.ts          # Mock 入口
```

## 命名规范

### 文件和文件夹
1. **文件夹名**: 统一采用**下划线命名法** (snake_case)
   - 示例: `purchase_order/`, `sku_list/`, `data_analysis/`

2. **文件名**: 统一采用**小驼峰命名法** (camelCase)
   - 示例: `supplierList.vue`, `skuUtil.ts`, `warehouseApis.ts`

3. **Vue 组件文件**: 使用小驼峰，但组件名使用大驼峰 (PascalCase)
   - 文件: `selectPurchaseSkuDialog.vue`
   - 组件名: `SelectPurchaseSkuDialog`

### 代码命名
1. **类名**: 使用**大驼峰命名法** (PascalCase)
   - 示例: `UserService`, `OrderManager`, `DataProcessor`

2. **接口命名**: 以大写字母 **I** 开头，代表 `interface`
   - 示例: `IOption`, `IUserInfo`, `IReturnResult`

3. **变量和函数**: 使用**小驼峰命名法** (camelCase)
   - 示例: `getUserInfo()`, `orderList`, `totalAmount`

4. **常量**: 使用**全大写下划线命名法** (UPPER_SNAKE_CASE)
   - 示例: `API_BASE_URL`, `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`

5. **枚举**: 使用大驼峰，枚举值使用全大写下划线
   - 示例: `enum OrderStatus { PENDING = 'PENDING', COMPLETED = 'COMPLETED' }`

## 编码规范

### Vue 组件
1. **优先使用 Composition API** (`<script setup lang="ts">`)
2. **组件导入顺序**:
   ```typescript
   // 1. Vue 核心
   import { ref, computed, onMounted } from 'vue';
   // 2. 第三方库
   import { MessagePlugin } from 'tdesign-vue-next';
   // 3. 项目内部导入
   import { getUserList } from '@/apis/userApis';
   import type { IUserInfo } from '@/types/interface';
   ```

3. **组件结构顺序**:
   ```vue
   <script setup lang="ts">
   // 1. 导入
   // 2. Props 定义
   // 3. Emits 定义
   // 4. 响应式数据
   // 5. 计算属性
   // 6. 生命周期钩子
   // 7. 方法
   </script>

   <template>
     <!-- 模板内容 -->
   </template>

   <style scoped lang="less">
   /* 样式 */
   </style>
   ```

4. **Props 和 Emits 明确定义类型**:
   ```typescript
   interface Props {
     orderId: string;
     visible: boolean;
   }
   const props = defineProps<Props>();
   
   interface Emits {
     (e: 'update:visible', value: boolean): void;
     (e: 'confirm', data: any): void;
   }
   const emit = defineEmits<Emits>();
   ```

### TypeScript
1. **严格类型检查**: 避免使用 `any`，使用具体类型或泛型
2. **接口优于类型别名**: 定义对象结构时优先使用 `interface`
3. **类型定义集中管理**: 放在 `src/types/` 或 `src/apis/dto/` 目录
4. **导出类型**: 使用 `export type` 或 `export interface`

### API 调用
1. **统一使用 `src/utils/request.ts` 的 axios 实例**
2. **API 按模块组织**: 如 `supplierApis.ts`, `warehouseApis.ts`
3. **请求格式** (POST 请求自动包装):
   ```typescript
   {
     timestamp: Date.now(),
     serviceName: 'ec_erp_static',
     apiUrl: '/erp_api/xxx',
     traceId: 'xxxxx',
     body: { /* 实际数据 */ }
   }
   ```
4. **响应格式**:
   ```typescript
   interface IReturnResult<T = any> {
     result: number;        // 0 表示成功
     resultMsg: string;
     traceId: string;
     data: T;
   }
   ```

### 状态管理 (Pinia)
1. **模块化组织**: 按业务模块拆分 store
2. **持久化配置**: 使用 `pinia-plugin-persistedstate`
3. **Store 结构**:
   ```typescript
   import { defineStore } from 'pinia';
   
   export const useUserStore = defineStore('user', {
     state: () => ({
       userInfo: null,
     }),
     getters: {
       isLoggedIn: (state) => !!state.userInfo,
     },
     actions: {
       async fetchUserInfo() {
         // 异步逻辑
       },
     },
   });
   ```

### 路由
1. **路由懒加载**: 使用动态导入
   ```typescript
   component: () => import('@/pages/supply/supplierList.vue')
   ```
2. **路由 meta 信息**: 包含标题、图标、权限等
3. **嵌套路由**: 使用 `children` 配置
4. **路由守卫**: 在 `permission.ts` 中统一处理

### 样式
1. **使用 Less 预处理器**
2. **组件样式使用 scoped**: `<style scoped lang="less">`
3. **全局样式**: 放在 `src/style/` 目录
4. **自动注入全局变量**: `@import "@/style/global.less";` (已在 vite.config.ts 配置)
5. **遵循 BEM 命名规范** (可选但推荐)

### 错误处理
1. **统一在 axios 拦截器中处理**
2. **使用 TDesign 的 MessagePlugin 提示错误**
3. **敏感操作使用 try-catch 包裹**
4. **提供友好的错误提示信息**

## 开发流程

### 开发命令
```bash
# 开发环境（连接后端）
npm run dev

# Mock 环境（使用本地 Mock 数据）
npm run dev:mock

# 构建测试环境
npm run build:test

# 构建生产环境
npm run build

# 代码检查
npm run lint

# 代码自动修复
npm run lint:fix

# 样式检查
npm run stylelint

# 样式自动修复
npm run stylelint:fix
```

### Git 提交规范
遵循 [Angular Convention](https://github.com/conventional-changelog/conventional-changelog/tree/master/packages/conventional-changelog-angular)

提交类型：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档变更
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（既不是新增功能，也不是修复 bug）
- `perf`: 性能优化
- `test`: 增加测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: 添加供应商管理模块
fix: 修复订单列表分页问题
docs: 更新 README 文档
```

### 分支管理
- `main`: 主分支，保护分支
- `develop`: 开发分支
- `feature/xxx`: 功能分支
- `fix/xxx`: 修复分支

## 特殊功能说明

### Mock 数据
- Mock 数据文件位于 `mock/api/data/` 目录
- 使用 `vite-plugin-mock` 插件
- 启动 Mock 模式: `npm run dev:mock`

### 主题配置
- 支持明亮/暗黑主题切换
- 自定义主题颜色配置
- 配置文件: `src/config/color.ts`, `src/config/style.ts`

### 导出功能
- 使用 `xlsx` 库导出 Excel
- 工具函数: `src/utils/excel.ts`, `src/utils/exportUtil.ts`

### 打印功能
- 使用 `vue3-print-nb` 和 `html2canvas`
- 打印相关页面: `src/pages/warehouse/printOrder.vue`

### 图表可视化
- 使用 ECharts 5.4.0
- 图表工具函数: `src/utils/charts.ts`
- 网络图: 使用 `v-network-graph` 和 `gojs`

## 业务模块说明

### 供应链管理 (supply)
- **采购订单列表** (`purchaseOrderList.vue`): 采购订单管理
- **SKU 列表** (`skuList.vue`): SKU（库存单位）管理
- **SKU 采购价格表** (`skuPurchasePriceList.vue`): 采购价格管理
- **供应商列表** (`supplierList.vue`): 供应商信息管理

### 仓库管理 (warehouse)
- **打印订单** (`printOrder.vue`): 订单打印功能
- **SKU 拣货单** (`skuPickingNote.vue`): 拣货单管理
- **盘点** (`stocktaking.vue`): 库存盘点功能

### 数据看板 (dashboard)
- **店铺销售** (`shopSale.vue`): 店铺销售数据统计
- **SKU 销售** (`skuSale.vue`): SKU 销售数据统计

## 注意事项

1. **路径别名**: 使用 `@/` 代替 `src/`
   ```typescript
   import { request } from '@/utils/request';
   ```

2. **环境变量**: 在 `.env` 文件中配置，使用 `import.meta.env` 访问
   ```typescript
   const baseUrl = import.meta.env.VITE_BASE_URL;
   ```

3. **代理配置**: 后端 API 代理到 `http://localhost:15002`
   ```typescript
   // vite.config.ts
   proxy: {
     '^/erp_api/.*': {
       target: 'http://localhost:15002',
       changeOrigin: true,
     },
   }
   ```

4. **自动保存格式化**: 建议配合 WebStorm 的 `save action` 插件

5. **兼容性**: 
   - Chrome >= 84
   - Firefox >= 83
   - Safari >= 14.1
   - Edge >= 84

6. **组件库**: 优先使用 TDesign 组件，保持 UI 一致性
   - [TDesign Vue Next 文档](https://tdesign.tencent.com/vue-next/overview)
   - 常用组件: Table, Form, Dialog, Message, DatePicker, Select 等

## 最佳实践

1. **组件拆分**: 单个组件不超过 500 行，合理拆分子组件
2. **复用逻辑**: 抽取为 hooks 或工具函数
3. **类型安全**: 充分利用 TypeScript 的类型系统
4. **性能优化**: 
   - 使用 `computed` 缓存计算结果
   - 列表使用 `v-for` 时添加 `key`
   - 大列表使用虚拟滚动
5. **代码注释**: 复杂逻辑添加注释说明
6. **单元测试**: 核心业务逻辑编写单元测试（待完善）
7. **代码审查**: 提交前进行 self-review

## 开发工具推荐
- **IDE**: WebStorm / VSCode
- **浏览器插件**: Vue DevTools
- **VSCode 插件**: 
  - Vue Language Features (Volar)
  - TypeScript Vue Plugin (Volar)
  - ESLint
  - Prettier
  - EditorConfig

## 参考资源
- [Vue 3 文档](https://v3.vuejs.org/)
- [Vue 3 风格指南](https://v3.vuejs.org/style-guide/)
- [TypeScript 文档](https://www.typescriptlang.org/)
- [TDesign Vue Next](https://tdesign.tencent.com/vue-next/overview)
- [Vite 文档](https://vitejs.dev/)
- [Pinia 文档](https://pinia.vuejs.org/)

