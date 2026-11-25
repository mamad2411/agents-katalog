---
name: dart-oss-google-translator
description: 学习 gabrielpacheco23/google-translator 开源项目，通过一个简洁的 Google 翻译 Dart 库，掌握 Dart 基础语法、HTTP 请求和 JSON 处理。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-fundamentals
    - dart-core-libraries
  project:
    url: https://github.com/gabrielpacheco23/google-translator
    stars: 191
    difficulty: beginner
    category: library
---

# 学习 Google 翻译 Dart 库项目

## Contents

- [项目概览](#项目概览)
- [与 dart-fundamentals 的关联](#与-dart-fundamentals-的关联)
- [项目结构导读](#项目结构导读)
- [核心实现分析](#核心实现分析)
- [Workflow: 通过小型库项目学习 Dart](#workflow-通过小型库项目学习-dart)
- [Examples](#examples)

## 项目概览

**项目名称**: google-translator
**作者**: gabrielpacheco23
**GitHub**: https://github.com/gabrielpacheco23/google-translator
**Stars**: 191 | **难度**: 入门级

一个极简的 Dart 翻译库，通过 HTTP 请求调用 Google 翻译 API。代码量小（约 70 行核心代码），结构清晰，是学习 Dart HTTP 客户端开发、JSON 处理、Future 的绝佳入门项目。

## 与 dart-fundamentals 的关联

该项目直接应用于 `dart-fundamentals` 和 `dart-core-libraries` 技能：

| Dart 基础主题 | 项目中的应用 |
|-------------|------------|
| 函数定义 | translate() 异步函数 |
| Future / async / await | HTTP 请求与响应处理 |
| 类型推断 | var / final 使用 |
| 字符串模板 | URL 拼接、错误信息 |
| dart:convert | JSON 解码 |
| HTTP 客户端 | HTTP GET 请求 |

## 项目结构导读

```
google-translator/
├── lib/
│   ├── translator.dart          # 主入口，对外暴露 API
│   └── src/
│       ├── translator_base.dart # 翻译核心逻辑
│       └── language.dart        # 语言代码常量
├── test/
│   └── translator_test.dart     # 单元测试
└── pubspec.yaml                 # 依赖（http package）
```

## 核心实现分析

### 关键代码模式

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class GoogleTranslator {
  final http.Client _client;

  GoogleTranslator({http.Client? client})
      : _client = client ?? http.Client();

  Future<String> translate(
    String text, {
    String from = 'auto',
    String to = 'en',
  }) async {
    final uri = Uri.parse(
      'https://translate.googleapis.com/translate_a/single'
      '?client=gtx&sl=$from&tl=$to&dt=t&q=${Uri.encodeComponent(text)}',
    );

    final response = await _client.get(uri);
    if (response.statusCode == 200) {
      final json = jsonDecode(response.body) as List;
      final translations = json[0] as List;
      return translations.map((t) => t[0] as String).join();
    }
    throw Exception('翻译失败: ${response.statusCode}');
  }
}
```

### 设计亮点

| 特性 | 说明 |
|------|------|
| 依赖注入 | `http.Client` 通过构造方法注入，便于测试 |
| 异步处理 | 所有网络请求使用 `async/await` |
| 错误处理 | HTTP 非 200 状态抛出异常 |
| JSON 解析 | 使用 `dart:convert` 解析 Google 返回格式 |

## Workflow: 通过小型库项目学习 Dart

### Task Progress

- [ ] **Step 1: 克隆并安装。** `git clone` 后运行 `dart pub get` 安装依赖。
- [ ] **Step 2: 阅读测试文件。** 先从 `test/` 目录入手，理解库的预期行为。
- [ ] **Step 3: 阅读核心源码。** 逐行理解 `translator.dart` 和 `translator_base.dart`。
- [ ] **Step 4: 运行测试。** 执行 `dart test` 验证功能正确。
- [ ] **Step 5: 添加新功能。** 尝试添加批量翻译、源语言检测等功能。
- [ ] **Step 6: 编写新测试。** 为新增功能编写单元测试。
- [ ] **Step 7: 代码质量检查。** `dart analyze` 确保无类型错误和警告。
- [ ] **Step 8: Feedback Loop。** 添加功能 → 写测试 → 验证 → 优化 → 重复。

### 条件逻辑

- **如果遇到 HTTP 相关概念不理解：** 查阅 `dart-fundamentals` 技能中关于 `Future` 和 `async/await` 的部分。
- **如果需要扩展功能：** 先阅读 Google Translate API 文档，理解返回数据格式。
- **如果测试运行失败：** 检查网络连接，部分测试可能需要代理或 VPN。
- **如果代码量增长过快：** 考虑拆分文件，将不同语言的逻辑分离到独立模块。

## Examples

### 扩展：添加批量翻译

```dart
Future<List<String>> translateBatch(
  List<String> texts, {
  String from = 'auto',
  String to = 'en',
}) async {
  final results = <String>[];
  for (final text in texts) {
    final translated = await translate(text, from: from, to: to);
    results.add(translated);
  }
  return results;
}
```

### 扩展：添加语言检测

```dart
Future<String> detectLanguage(String text) async {
  final uri = Uri.parse(
    'https://translate.googleapis.com/translate_a/single'
    '?client=gtx&sl=auto&tl=en&dt=t&q=${Uri.encodeComponent(text)}',
  );
  final response = await _client.get(uri);
  if (response.statusCode == 200) {
    final json = jsonDecode(response.body) as List;
    return json[2] as String; // 检测到的源语言代码
  }
  throw Exception('语言检测失败');
}
```
