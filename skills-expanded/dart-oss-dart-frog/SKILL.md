---
name: dart-oss-dart-frog
description: 学习 dart-frog-dev/dart_frog 开源项目，通过纯 Dart 后端框架理解服务端架构、异步请求处理和 Dart 全栈开发模式。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-async-concurrency
    - dart-core-libraries
  project:
    url: https://github.com/dart-frog-dev/dart_frog
    stars: 2200
    difficulty: advanced
    category: framework
---

# 学习 Dart Frog 后端框架项目

## Contents

- [项目概览](#项目概览)
- [与 dart-async-concurrency 的关联](#与-dart-async-concurrency-的关联)
- [项目架构分析](#项目架构分析)
- [后端架构模式详解](#后端架构模式详解)
- [Workflow: 通过 Dart Frog 学习 Dart 后端开发](#workflow-通过-dart-frog-学习-dart-后端开发)
- [Examples](#examples)

## 项目概览

**项目名称**: dart_frog
**作者**: dart-frog-dev
**GitHub**: https://github.com/dart-frog-dev/dart_frog
**Stars**: 2.2k | **难度**: 进阶

一个快速、极简的纯 Dart 后端框架，支持热重载、路由系统、中间件链和 WebSocket。基于 `shelf` HTTP 服务器构建，是学习 Dart 服务端架构、异步并发处理和全栈开发的最佳范例。

## 与 dart-async-concurrency 的关联

该项目是 `dart-async-concurrency` 技能在服务端的高级应用：

| dart-async-concurrency 主题 | 项目中的应用 |
|--------------------------|------------|
| Future / async/await | 请求处理管道 |
| Stream | WebSocket 连接、请求体流读取 |
| 并发处理 | Isolate 级别请求分发 |
| 错误处理 | 全局异常捕获与响应 |
| 中间件链 | 异步中间件管道 |

## 项目架构分析

### 核心架构

```
dart_frog/
├── packages/
│   └── dart_frog/
│       ├── lib/
│       │   ├── dart_frog.dart        # 公共 API
│       │   └── src/
│       │       ├── router.dart       # 路由系统
│       │       ├── middleware.dart    # 中间件
│       │       ├── request_context.dart
│       │       ├── response.dart     # 响应构造
│       │       └── hot_reload.dart   # 热重载
│       └── pubspec.yaml
├── bricks/                           # Mason 模板
└── pubspec.yaml
```

### 请求处理管道

```
HTTP Request
    → Router (路径匹配)
    → Middleware Chain (认证/日志/CORS)
    → Route Handler (业务逻辑)
    → Response
```

### 路由文件约定

```
routes/
├── index.dart              # GET /
├── users/
│   ├── index.dart          # GET /users
│   ├── [id].dart          # GET /users/:id
│   └── [id]/
│       └── posts.dart      # GET /users/:id/posts
```

## 后端架构模式详解

### 路由处理

```dart
import 'package:dart_frog/dart_frog.dart';

Response onRequest(RequestContext context) {
  final method = context.request.method;
  return switch (method) {
    HttpMethod.get => _onGet(context),
    HttpMethod.post => _onPost(context),
    _ => Response(statusCode: 405),
  };
}

Future<Response> _onGet(RequestContext context) async {
  return Response.json(body: {'message': 'Hello, Dart Frog!'});
}
```

### 中间件模式

```dart
Handler middleware(Handler handler) {
  return (context) async {
    final startTime = DateTime.now();
    print('[${startTime}] ${context.request.method} ${context.request.url}');

    final response = await handler(context);

    final elapsed = DateTime.now().difference(startTime);
    print('Responded in ${elapsed.inMilliseconds}ms');
    return response;
  };
}
```

### WebSocket 处理

```dart
Future<Response> onRequest(RequestContext context) async {
  if (context.request.headers['upgrade'] == 'websocket') {
    final handler = context.read<WebSocketHandler>();
    return handler((channel, protocol) {
      channel.stream.listen((message) {
        channel.sink.add('Echo: $message');
      });
    });
  }
  return Response(statusCode: 400);
}
```

## Workflow: 通过 Dart Frog 学习 Dart 后端开发

### Task Progress

- [ ] **Step 1: 安装 Dart Frog CLI。** `dart pub global activate dart_frog_cli`。
- [ ] **Step 2: 创建新项目。** `dart_frog create my_api` 生成脚手架。
- [ ] **Step 3: 启动开发服务器。** `dart_frog dev` 体验热重载。
- [ ] **Step 4: 创建第一个路由。** 在 `routes/` 下创建文件，实现 GET/POST 处理。
- [ ] **Step 5: 添加中间件。** 实现日志记录、认证检查中间件。
- [ ] **Step 6: 集成依赖注入。** 使用 `context.read<T>()` 获取服务实例。
- [ ] **Step 7: 实现 WebSocket。** 添加实时通信功能。
- [ ] **Step 8: Feedback Loop。** 修改路由 → 热重载立即生效 → 发送 HTTP 请求验证 → 重复。

### 条件逻辑

- **如果需要了解 HTTP 服务器原理：** 使用 `dart-async-concurrency` 技能中的 Future/Stream 章节理解异步 I/O。
- **如果项目结构过于复杂：** 从单个路由文件开始，参考 routes 文件约定逐步添加文件。
- **如果需要部署到生产环境：** 使用 `dart compile exe` 编译为独立可执行文件。
- **如果需要处理大文件上传：** 使用 Stream 读取请求体，避免将全部内容加载到内存。

## Examples

### 从项目中学到的 REST API 模式

```dart
// routes/users/[id].dart
Future<Response> onRequest(RequestContext context, String id) async {
  final userService = context.read<UserService>();
  final user = await userService.findById(id);

  if (user == null) {
    return Response.json(
      body: {'error': 'User not found'},
      statusCode: 404,
    );
  }

  return Response.json(body: {'id': user.id, 'name': user.name});
}
```

### 结合 dart-async-concurrency 的延伸练习：流式响应

```dart
import 'dart:async';

Future<Response> onRequest(RequestContext context) async {
  final controller = StreamController<String>();

  Timer.periodic(const Duration(seconds: 1), (timer) {
    if (timer.tick > 5) {
      controller.close();
      timer.cancel();
    } else {
      controller.add('Event ${timer.tick}\n');
    }
  });

  return Response(
    body: controller.stream.transform(utf8.encoder),
    headers: {'Content-Type': 'text/event-stream'},
  );
}
```
