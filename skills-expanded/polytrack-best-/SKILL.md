# Polytrack.best 项目规则与模式

## 项目概览
这是一个基于HTML + TailwindCSS的静态游戏网站项目，为Polytrack赛车游戏提供优化的访问入口。项目采用移动端优先设计，重点关注SEO优化和性能表现。

## 核心技术栈
- **前端**: HTML5 + TailwindCSS + 原生JavaScript (最小化使用)
- **游戏集成**: iframe嵌入 (app-polytrack.kodub.com)
- **部署**: 静态文件托管
- **构建**: 计划从CDN迁移到本地TailwindCSS构建

## 关键设计原则

### 1. 移动端优先 (Mobile-First)
- 所有CSS使用TailwindCSS的响应式类名
- 断点策略: sm(640px) → md(768px) → lg(1024px)
- 移动端体验优先，桌面端增强

### 2. SEO优化优先
- 关键词"polytrack"密度控制在3.5-4%
- 完整的结构化数据 (JSON-LD)
- 语义化HTML结构
- 性能优化 (Core Web Vitals)

### 3. 性能至上
- 最小化JavaScript使用
- 预连接外部资源
- 固定比例容器防止CLS
- 关键CSS内联

### 4. 内容质量
- 基于真实游戏信息 (CrazyGames数据)
- 地道英文表达
- 用户价值导向

## 代码规范与模式

### HTML结构模式
```html
<!-- 统一的内容区块模式 -->
<section class="py-12 md:py-16">
  <div class="max-w-6xl mx-auto px-4 md:px-6">
    <h2 class="text-xl md:text-2xl font-semibold mb-6">标题</h2>
    <!-- 内容 -->
  </div>
</section>
```

### TailwindCSS使用模式
- **容器**: `max-w-6xl mx-auto px-4 md:px-6`
- **网格**: `grid md:grid-cols-2 lg:grid-cols-3 gap-6`
- **间距**: `py-12 md:py-16` (区块间距)
- **字体**: `text-xl md:text-2xl` (响应式字体)

### 游戏iframe集成模式
```html
<div class="game-aspect rounded-lg overflow-hidden border border-slate-200 skeleton" id="game-shell">
  <iframe
    title="Polytrack Online Racing Game"
    src="https://app-polytrack.kodub.com/0.5.1/?"
    loading="eager"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
    allowfullscreen
    referrerpolicy="strict-origin-when-cross-origin"
    onload="document.getElementById('game-shell')?.classList.remove('skeleton')"
  ></iframe>
</div>
```

### SEO配置模式
- **Meta标签**: 完整的title、description、canonical
- **Open Graph**: 社交分享优化
- **JSON-LD**: WebSite、WebPage、VideoGame、FAQPage
- **关键词分布**: 自然分布在H1、H2、内容中

## 文件组织规范

### 当前结构
```
polytrack.best/
├── index.html              # 主页面 (单文件应用)
├── project-requirements.md # 需求文档
├── seo-strategy.md        # SEO策略
├── memory-bank/           # 项目记忆库
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
└── .cursorrules           # 项目规则 (当前文件)
```

### 计划结构 (第二阶段)
```
polytrack.best/
├── index.html
├── assets/
│   ├── logo.svg           # 品牌logo
│   ├── og-cover.jpg       # 社交分享图
│   └── favicon.ico        # 网站图标
├── css/
│   └── styles.css         # 编译后的TailwindCSS
├── js/
│   └── main.js            # 最小化JavaScript
└── sw.js                  # Service Worker (可选)
```

## 开发工作流程

### 1. 任务开始前
- 阅读Memory Bank相关文档
- 确认当前项目状态 (activeContext.md)
- 了解技术约束 (techContext.md)

### 2. 开发过程中
- 遵循既定的设计模式
- 保持代码风格一致性
- 优先考虑SEO和性能影响

### 3. 任务完成后
- 更新相关Memory Bank文档
- 记录重要决策和变更
- 验证SEO和性能指标

## 重要约束与限制

### 技术约束
- **单页面应用**: 所有内容在index.html中
- **外部游戏**: 不能修改游戏本身，只能优化集成
- **静态部署**: 无服务器端处理能力
- **SEO优先**: 所有技术决策需考虑SEO影响

### 内容约束
- **英文内容**: 面向用户的内容必须使用地道英文
- **关键词密度**: "polytrack"保持在3.5-4%
- **真实信息**: 基于CrazyGames真实数据，不能虚构
- **用户价值**: 内容必须对用户有实际价值

### 性能约束
- **首屏加载**: 目标 < 3秒
- **Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1
- **移动端优先**: 移动端体验不能妥协
- **最小依赖**: 减少外部依赖和JavaScript使用

## 常见任务模式

### 添加新内容区块
1. 使用统一的section模式
2. 确保响应式设计
3. 检查关键词密度影响
4. 验证语义化HTML

### 性能优化
1. 检查资源加载优先级
2. 验证CLS影响
3. 测试移动端性能
4. 监控Core Web Vitals

### SEO优化
1. 验证结构化数据
2. 检查关键词分布
3. 确认meta标签完整性
4. 测试搜索引擎可见性

## 质量检查清单

### 代码质量
- [ ] HTML语义化和可访问性
- [ ] TailwindCSS类名规范使用
- [ ] 响应式设计实现
- [ ] JavaScript最小化原则

### SEO质量
- [ ] 关键词密度检查 (3.5-4%)
- [ ] 结构化数据验证
- [ ] Meta标签完整性
- [ ] 页面结构语义化

### 性能质量
- [ ] Core Web Vitals指标
- [ ] 资源加载优化
- [ ] 移动端性能
- [ ] 缓存策略实施

### 用户体验
- [ ] 跨设备兼容性
- [ ] 加载状态反馈
- [ ] 错误处理机制
- [ ] 可访问性支持

## 项目特定知识

### 游戏信息 (重要参考)
- **游戏名**: Polytrack (PolyTrack)
- **开发商**: Kodub
- **评分**: 8.2/10 (368,224票)
- **类型**: 赛车 + 赛道编辑器
- **特色**: TrackMania灵感，低多边形风格

### 关键词策略
- **主词**: polytrack (62.7K搜索量)
- **长尾**: polytrack unblocked (470), poly track (13.1K)
- **品牌**: kodub polytrack (220)
- **功能**: polytrack game, polytrack online

### 用户群体
- **休闲玩家**: 40% (快速娱乐)
- **创意玩家**: 35% (赛道编辑)
- **竞技玩家**: 25% (排行榜挑战)

## 常见问题解决

### TailwindCSS相关
- 使用响应式前缀: `md:`, `lg:`
- 容器模式: `max-w-6xl mx-auto px-4 md:px-6`
- 间距统一: `py-12 md:py-16`, `gap-6`

### iframe集成相关
- 固定比例: `padding-top: 75%` (4:3)
- 预连接: `preconnect` 和 `dns-prefetch`
- 加载反馈: 骨架屏动画

### SEO相关
- 关键词自然分布，避免堆砌
- 结构化数据完整性
- 移动端友好性优先

## 项目演进路径

### 当前阶段: 第二阶段优化
- Memory Bank建立 ✅
- TailwindCSS本地构建 ⏳
- 图像资源创建 ⏳
- 性能监控集成 ⏳

### 下一阶段: 功能扩展
- 赛道展示页面
- 社区功能集成
- 多语言支持
- PWA功能

---

**创建日期**: 2025年1月12日
**项目阶段**: 第二阶段 - 优化与完善
**技术栈**: HTML5 + TailwindCSS + 原生JS
**重点关注**: SEO优化 + 性能表现 + 用户体验