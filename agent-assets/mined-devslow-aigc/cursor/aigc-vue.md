---
description: 
globs: 
alwaysApply: false
---
# Vue2 文章AIGC优化网页项目规范

## 1. 项目结构
```
project-root/
├── public/                # 静态资源文件
│   ├── index.html         # HTML 模板
│   └── favicon.ico        # 网站图标
├── src/                   # 源代码
│   ├── assets/            # 静态资源（会被webpack处理）
│   ├── components/        # 公共组件
│   │   ├── common/        # 通用组件
│   │   └── business/      # 业务组件
│   ├── views/             # 视图组件
│   ├── api/               # API请求模块
│   │   ├── index.js       # API入口
│   │   └── services/      # 服务模块（按功能分类）
│   ├── utils/             # 工具函数
│   │   ├── request.js     # 请求封装
│   │   ├── auth.js        # 授权相关
│   │   └── tools.js       # 通用工具
│   ├── store/             # Vuex状态管理
│   │   ├── index.js       # Store入口
│   │   └── modules/       # 模块化Store
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── styles/            # 全局样式
│   │   ├── variables.scss # 样式变量
│   │   └── global.scss    # 全局样式定义
│   ├── constants/         # 常量定义
│   │   └── openai.js      # OpenAI相关常量
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── .eslintrc.js           # ESLint配置
├── .prettierrc.js         # Prettier配置
├── babel.config.js        # Babel配置
├── vue.config.js          # Vue CLI配置
├── package.json           # 项目依赖管理
└── README.md              # 项目说明
```

## 2. 命名规范

### 文件命名
- 组件文件：使用PascalCase，如`ArticleEditor.vue`
- JS/TS文件：使用camelCase，如`apiService.js`
- 样式文件：使用kebab-case，如`main-style.scss`

### 变量命名
- 变量与函数：使用camelCase，如`articleContent`
- 常量：使用大写下划线，如`API_KEY`
- 组件名：使用PascalCase，如`ArticleOptimizer`
- CSS类名：使用BEM命名法，如`.article-card__title`

## 3. 编码规范

### Vue组件规范
- 使用组件选项顺序：name, components, props, data, computed, watch, methods, 生命周期钩子
- 组件props必须定义类型和默认值
- 组件事件名使用kebab-case，如`@content-change`
- 每个组件应该只有一个职责


### API调用规范
- 使用统一的请求封装，处理异常和加载状态
- API密钥不直接写在代码中，使用环境变量或安全存储
- 实现请求防抖和节流，避免过度调用API


## 4. 安全规范
- OpenAI API密钥存储在环境变量中，不提交到代码仓库
- 实现服务端代理转发API请求，避免前端暴露密钥
- 敏感数据传输时进行加密处理
- 输入内容防注入处理

## 6. 性能优化规范
- 路由懒加载
- 长文本渲染使用虚拟滚动
- 优化API请求，避免频繁调用


## 7. 文档与注释规范
- 关键业务逻辑添加详细注释
- 复杂组件提供使用示例
- 提供项目README和开发指南
- API模块添加接口文档

















4/