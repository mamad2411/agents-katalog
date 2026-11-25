---
name: piying-create-route-page
description: 将 piying-view 的表单定义通过路由直接显示。指导用户配置路由并使用 SchemaViewPage 组件展示表单。
---

# piying-view 路由显示流程

## 核心流程

### 1.实现要求

**目标** 根据要求实现schema定义

**实现**

- 根据`any-to-piying`技能实现schema定义
- 写入到src/define文件夹中

### 2.配置路由

**目标**: 在路由配置中添加 SchemaViewPage 组件和引入上一步的schema

**需编辑的文件**:

- `src/app/app.routes.ts`或指定项目中的路由数组

**配置代码**:

```typescript
import { SchemaViewPage } from '@piying-lib/angular-core';
import { typedComponent } from '@piying/view-angular';
import { PresetDefine } from '@piying-lib/angular-daisyui/preset';
import * as v from 'valibot';

const safeDefine = typedComponent(PresetDefine);

export const routes: Routes = [
  {
    path: 'hello',
    component: SchemaViewPage,
    data: {
      // Valibot schema 定义
      schema: () =>
        //上一步的定义
        ,
      // 相关配置
      options: () => ({
        fieldGlobalConfig: safeDefine.define,
      }),
      // 默认值,如果需要
      // model: () => undefined,
    },
  },
];
```

**验证**:

- 路由配置语法正确

---
