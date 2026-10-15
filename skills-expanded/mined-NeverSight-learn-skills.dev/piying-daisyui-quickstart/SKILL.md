---
name: piying-daisyui-quickstart
description: 快速初始化 @piying-lib/angular-daisyui 项目。验证前提条件并指导完成所有安装配置步骤。
---

# @piying-lib/angular-daisyui 快速初始化流程

## 核心流程

### 步骤 1: 前提条件验证

**目标**: 确认用户有一个现有的 Angular 项目

**检查项**:

- 项目中存在 `angular.json` 文件
- 项目中存在 `package.json` 文件
- 项目使用 TypeScript

**如果验证失败**:

- 提示用户需要先创建 Angular 项目: `ng new my-app`
- 或者提供一个现有的 Angular 项目路径

---

### 步骤 2: 安装主包及对等依赖

**目标**: 安装 `@piying-lib/angular-daisyui` 及其必要的对等依赖

**执行命令**:

```bash
npm i @piying-lib/angular-daisyui
npm i @piying/view-angular@^2.7.1
npm i daisyui@^5.5.19
npm i @angular/cdk@>=20.0.0
npm i @angular/material@>=20.0.0
npm i @cyia/ngx-common@>=20.0.4
```

**验证**:

- 检查 `package.json` 中是否已添加上述包
- 检查 `node_modules` 中是否成功安装

---

### 步骤 3: 安装 Tailwind CSS（如果不存在）

**目标**: 确保项目中已安装 Tailwind CSS

**检查项**:

- 检查 `package.json` 中是否存在 `tailwindcss`
- 检查 `.postcssrc.json` 文件是否存在

**如果不存在，执行**:

```bash
npm install tailwindcss @tailwindcss/postcss postcss --force
```

**配置 `.postcssrc.json`**:

```json
{
  "plugins": {
    "@tailwindcss/postcss": {}
  }
}
```

**验证**:

- `.postcssrc.json` 文件存在且配置正确
- `tailwindcss` 已添加到 `package.json`

---

### 步骤 4: 安装 DaisyUI（如果不存在）

**目标**: 确保项目中已安装 DaisyUI

**检查项**:

- 检查 `package.json` 中是否存在 `daisyui`

**如果不存在，执行**:

```bash
npm i -D daisyui@latest
```

**验证**:

- `daisyui` 已添加到 `package.json` 的 `devDependencies`

---

### 步骤 5: 配置 CSS

**目标**: 在主 CSS 文件中添加必要的配置

**需配置的文件**:

- `src/styles.css` 或 `src/styles.scss`

**添加内容**:

```css
@import 'tailwindcss';

@plugin "daisyui" {
  themes:
    light --default,
    dark --prefersdark;
}

@source '../node_modules/@piying-lib/angular-daisyui/fesm2022';
@source '../node_modules/@piying-lib/angular-daisyui/preset-css/ts';
```

**验证**:

- CSS 文件中已添加上述代码
- 路径与项目结构匹配

---

### 步骤 6: 配置应用

**目标**: 在 `src/app/app.config.ts` 中添加必要的配置

**需修改的文件**:

- `src/app/app.config.ts`

**添加内容**:

```typescript
import { ThemeService } from '@piying-lib/angular-daisyui/service';

export const appConfig: ApplicationConfig = {
  providers: [
    // ... 其他 providers
    ThemeService,
  ],
};
```

**验证**:

- `ThemeService` 已添加到 providers 数组
- 导入语句正确

---

### 步骤 7: 导入预定义组件

**目标**: 导入并配置 piying-view 的预定义组件

**需修改的文件**:

- `src/app/app.ts` 或其他组件文件

**添加内容**:

```typescript
import { typedComponent } from '@piying/view-angular';
import { PresetDefine } from '@piying-lib/angular-daisyui/preset';

const safeDefine = typedComponent(PresetDefine);
export const FieldGlobalConfig = safeDefine.define;
```

**验证**:

- `typedComponent` 和 `PresetDefine` 正确导入
- `FieldGlobalConfig` 已导出供后续使用

---

### 步骤 8: 快速开始验证

**目标**: 确认安装和配置正确

**验证方式**:

1. 检查 `src/index.html` 是否存在
2. 检查 `src/main.ts` 是否正确引导应用
3. 尝试运行项目: `npm start`

**预期结果**:

- 项目成功启动
- 没有编译错误
- DaisyUI 主题正常加载

---

## 错误处理

### 常见问题 1: 对等依赖版本冲突

**症状**: 安装时出现 peer dependency 警告或错误

**解决方法**:

- 使用 `--legacy-peer-deps` 或 `--force` 标志
- 或手动指定对等依赖的兼容版本

### 常见问题 2: Tailwind CSS 配置错误

**症状**: 启动时出现 Tailwind 相关错误

**解决方法**:

- 确认 `.postcssrc.json` 配置正确
- 确认 `tailwindcss` 版本兼容

### 常见问题 3: DaisyUI 主题未加载

**症状**: 应用运行但 DaisyUI 样式未生效

**解决方法**:

- 检查 CSS 配置中的 `@source` 路径
- 确认 `daisyui` 已正确安装

---

## 完成标准

当以下所有条件满足时，初始化完成:

1. ✅ 所有包已成功安装
2. ✅ Tailwind CSS 配置正确
3. ✅ DaisyUI 配置正确
4. ✅ CSS 配置已添加
5. ✅ `app.config.ts` 已更新
6. ✅ 预定义组件已导入
7. ✅ 项目可以成功编译和运行
8. ✅ 没有明显的警告或错误
