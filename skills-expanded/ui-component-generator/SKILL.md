# UI 组件生成器

## 描述
专业的 UI 组件自动生成工具，可以根据设计需求快速生成 React、Vue、Angular 等现代前端框架的组件代码。

## 类别
设计

## 标签
UI组件, 前端开发, React, Vue, Angular, 设计系统

## 使用场景
- 快速创建基础 UI 组件
- 生成复杂交互组件
- 创建设计系统组件
- 生成响应式布局
- 创建主题化组件

## 前置要求
- Claude Desktop 版本 1.0+
- 了解前端开发基础
- 熟悉至少一种前端框架

## 使用方法

### 基础用法
```
请帮我生成一个 [框架类型] 的 [组件类型] 组件，具有以下特性：
- [特性1]
- [特性2]
- [样式要求]
```

### 高级用法
```
我需要创建一个专业的 [组件类型] 组件，请生成：

组件要求：
- 框架：[React/Vue/Angular]
- 类型：[函数组件/类组件]
- 样式：[CSS Modules/Styled Components/Tailwind CSS]
- 功能：[详细功能描述]

设计规范：
- 主题色：[颜色配置]
- 字体：[字体配置]
- 间距：[间距系统]
- 动画：[动画要求]

交互需求：
- [交互1]
- [交互2]
- [交互3]

可访问性：
- 需要支持键盘导航
- 包含 ARIA 标签
- 支持屏幕阅读器

响应式要求：
- 桌面端：[桌面端布局]
- 平板端：[平板端布局]
- 移动端：[移动端布局]

请提供：
1. 完整的组件代码
2. 样式文件
3. 使用示例
4. 测试代码
```

## 配置选项

### 支持的框架
- React (函数组件 & 类组件)
- Vue 3 (Composition API)
- Angular (Components & Services)
- Svelte
- Vanilla JavaScript

### 样式解决方案
- CSS Modules
- Styled Components
- Emotion
- Tailwind CSS
- SCSS/SASS
- CSS-in-JS

### 组件类型
- 表单组件 (Input, Select, Checkbox 等)
- 导航组件 (Menu, Breadcrumb, Tabs 等)
- 布局组件 (Grid, Card, Panel 等)
- 反馈组件 (Modal, Toast, Loading 等)
- 数据展示组件 (Table, Chart, List 等)
- 交互组件 (Slider, Carousel, Tree 等)

## 输出格式

生成的组件包含：
1. 组件主文件 (.jsx/.vue/.ts)
2. 样式文件 (.css/.scss/.module.css)
3. 类型定义文件 (.d.ts)
4. 使用示例文件
5. 测试文件
6. Storybook 故事 (可选)

## 限制和注意事项
- 生成的组件需要根据项目的设计系统进行调整
- 复杂的业务逻辑可能需要额外的状态管理
- 建议结合项目的组件库使用
- 某些特殊效果可能需要额外的依赖

## 版本历史
- v1.0.0: 初始版本，支持基础组件生成
- v1.1.0: 添加更多框架支持
- v1.2.0: 增强样式和动画支持
- v1.3.0: 添加可访问性支持

## 许可证
MIT License

## 贡献者
Claude Skills Hub Team
