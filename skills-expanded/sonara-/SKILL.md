# 个性化音乐推荐系统 - AI 开发严格规约 (DeepSeek 优化版)

## 1. 核心技术栈与环境锁定

- **后端环境**: 必须使用 .NET 9 (`TargetFramework: net9.0`)。禁止使用 .NET 10、Preview SDK 或任何预发布 NuGet 包。
- **数据库**: 统一使用单数据库 `MusicRecDb`（SQL Server 实例: `.\SQLEXPRESS`）。
- **数据持久化**: 业务层禁止手写 SQL；必须通过 EF Core 9 Migration (`dotnet ef migrations`) 自动生成表格。特殊性能优化或报表场景需明确批准。
- **前端栈**: Next.js, React, TypeScript, TailwindCSS, Framer Motion。
- **前端状态与请求**: 状态管理只允许使用 Zustand；异步请求与缓存只允许使用 TanStack Query (React Query)。

## 2. 模块化单体 (Modular Monolith) 架构守则

- **模块边界**: 严禁模块交叉引用。`Modules/X` 不允许直接引用 `Modules/Y`。
- **模块间通信**: 所有跨模块通信必须通过 `BuildingBlocks/Contracts` 或消息媒介（MediatR 内部事件）。
- **DbContext 规范**: 优先使用单主 DbContext 映射到同一数据库，并放置于 `BuildingBlocks/Infrastructure` 中。各模块可通过其隔离操作属于本模块的表，禁止跨模块直接操作他人的业务实体。

## 3. 后端代码规范 (C# 13 / .NET 9)

- **架构分层**: 严格遵守 CQRS 模式。Controller/Endpoint 只负责接收请求，业务逻辑必须封装在 MediatR 的 `IRequest` 和 `IRequestHandler` 中。

- **数据校验**: 使用 FluentValidation 进行输入验证；禁止在 Handler 内写大量 `if (string.IsNullOrEmpty)`。

- **对象映射**: 使用 Mapster 进行 Entity ↔ DTO 转换。

- **错误处理**: 业务异常必须抛出自定义异常，由全局异常处理中间件统一捕获并通过 Serilog 记录；禁止滥用 try-catch。

- **统一 API 返回格式**: 所有接口返回结构必须严格为：

  JSON

  ```
  {
    "success": boolean,
    "data": any,
    "message": string,
    "errors": string[]
  }
  ```

## 4. Spotify 集成与数据缓存

- **禁止直接调用 Spotify API**: 控制器或业务 Handler 不能直接发起 HTTP 请求。
- **适配器模式**: 所有 Spotify 请求必须通过 `Infrastructure/Spotify/` 下的 Service（如 `SpotifyAudioFeatureService`）。
- **数据缓存机制**: Spotify Metadata（歌曲、歌手、Audio Features）必须落库（SQL Server）。高频访问必须优先使用内存缓存 (`IMemoryCache`)；在 Phase 6 阶段可增加 Redis 缓存层。

## 5. 推荐系统算法 (最高优先级)

- **混合推荐公式**:

  $$\text{FinalScore} = 0.35 \times \text{AudioSimilarity} + 0.25 \times \text{BehaviorScore} + 0.15 \times \text{GenrePreference} + 0.10 \times \text{Freshness} + 0.10 \times \text{Diversity} + 0.05 \times \text{Popularity}$$

- **相似度计算**: 歌曲特征向量化包含 `[energy, danceability, valence, tempo, acousticness]`；计算相似歌曲时必须实现 **Cosine Similarity (余弦相似度)** 或 **Euclidean Distance (欧氏距离)**。

- **推荐解释**: 推荐接口返回的 DTO 必须包含 `Reason` 字段，例如 `"因为你最近喜欢高能量电子音乐"`，用于前端展示推荐原因。

## 6. 前端代码规范 (Next.js / TypeScript)

- **组件与样式**: 必须结合 Shadcn UI 与 TailwindCSS，实现响应式、Spotify 风格深色主题。
- **动画效果**: 页面切换、卡片悬浮、播放器展开等动态效果必须使用 Framer Motion。
- **类型安全**: 除非与第三方库交互或类型收敛阶段，否则禁止使用 `any`；优先使用 `unknown`、泛型和明确的 `interface`/`type`。

## 7. AI 开发行为守则

- **规则优先**: 若任务与规则冲突，先遵守本文件；若发现规则缺失，提出补充方案，不可擅自改架构。
- **小步开发**: 每次改动前必须先输出：修改目标、影响文件、风险点、验证方式；确认无误后再编码。
- **模块化开发**: 一次只生成或修改单个模块，不得一次生成整个项目。
- **架构稳定**: 严格遵守 Modular Monolith 架构，避免跨模块操作和循环依赖。