---
name: dart-oss-dson
description: 学习 dart-league/dson 开源项目，通过 Dart 对象-JSON 序列化库理解 dart:core、dart:convert 的深度应用及代码生成技术。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-core-libraries
    - dart-type-system
  project:
    url: https://github.com/dart-league/dson
    stars: 65
    difficulty: intermediate
    category: library
---

# 学习 DSON 序列化库项目

## Contents

- [项目概览](#项目概览)
- [与 dart-core-libraries 的关联](#与-dart-core-libraries-的关联)
- [项目架构分析](#项目架构分析)
- [序列化实现详解](#序列化实现详解)
- [Workflow: 通过 DSON 学习序列化技术](#workflow-通过-dson-学习序列化技术)
- [Examples](#examples)

## 项目概览

**项目名称**: dson
**作者**: dart-league
**GitHub**: https://github.com/dart-league/dson
**Stars**: 65 | **难度**: 中等

一个纯 Dart 的对象-JSON 序列化库，支持循环引用、自定义转换器和代码生成。与 `json_serializable` 不同，dson 使用自己的注解和代码生成器，展示了 Dart 序列化机制的底层实现原理。

## 与 dart-core-libraries 的关联

该项目深入应用了 `dart-core-libraries` 技能：

| dart-core-libraries 主题 | 项目中的应用 |
|-------------------------|------------|
| dart:convert | JSON 编解码核心 |
| dart:mirrors / 反射 | 类型信息获取 |
| String 操作 | 代码生成模板 |
| Uri 解析 | 资源路径处理 |
| Dart 注解 | @Serializable 自定义注解 |
| 泛型 | 序列化器泛型抽象 |

## 项目架构分析

### 核心流程

```
@Serializable() 注解
    → code generator 扫描
    → 生成 .g.dart 文件
    → fromJson / toJson 方法
    → 支持循环引用解析
```

### 关键抽象

```dart
abstract class Serializable<T> {
  T fromJson(Map<String, dynamic> json);
  Map<String, dynamic> toJson();
}

class Serializer<T> {
  final Type type;
  final T Function(Map<String, dynamic>) fromJson;
  final Map<String, dynamic> Function(T) toJson;

  const Serializer({
    required this.type,
    required this.fromJson,
    required this.toJson,
  });
}
```

## 序列化实现详解

### 循环引用处理

DSON 的核心特性之一是支持循环引用的序列化：

```dart
class Node {
  String name;
  Node? parent;
  List<Node> children = [];
}

// DSL 自动处理父子循环引用
// {name: "root", parent: null, children: [
//   {name: "child", parent: "$ref:0", children: []}
// ]}
```

### 自定义转换器

```dart
class DateTimeConverter extends Converter<DateTime, int> {
  @override
  DateTime from(int milliseconds) =>
      DateTime.fromMillisecondsSinceEpoch(milliseconds);

  @override
  int to(DateTime date) => date.millisecondsSinceEpoch;
}
```

## Workflow: 通过 DSON 学习序列化技术

### Task Progress

- [ ] **Step 1: 阅读项目接口定义。** 从 `Serializable` 和 `Serializer` 抽象类理解核心设计。
- [ ] **Step 2: 理解注解机制。** 查看 `@Serializable()` 注解的定义，理解 Dart 元数据的存储方式。
- [ ] **Step 3: 跟踪序列化流程。** 从 `fromJson()` 调用开始，跟踪 JSON Map 如何转换为 Dart 对象。
- [ ] **Step 4: 研究循环引用处理。** 理解 DSON 如何用 `$ref` 标记解决循环引用。
- [ ] **Step 5: 运行测试。** 执行 `dart test` 观察循环引用、自定义转换器等测试用例。
- [ ] **Step 6: 自定义转换器。** 实现一个 `DurationConverter`，将 Duration 序列化为秒数。
- [ ] **Step 7: 对比 json_serializable。** 分析 DSON 与官方 json_serializable 的异同。
- [ ] **Step 8: Feedback Loop。** 添加转换器 → 写测试 → 跑分析 → 修正。

### 条件逻辑

- **如果对 Dart 注解机制不熟：** 查阅 `dart-type-system` 技能中关于元数据的说明。
- **如果需要处理复杂嵌套对象：** 参考 DSON 的递归序列化策略。
- **如果 JSON 解析性能是瓶颈：** 考虑使用 `dart:convert` 的 `JsonDecoder` 与自定义 `Converter` 组合。
- **如果遇到类型转换错误：** 检查 `fromJson` 中的 `as` 类型转换是否匹配 JSON 实际类型。

## Examples

### 从项目中学到的序列化模式

```dart
class User extends Serializable {
  String name;
  int age;
  List<String> tags;

  User({required this.name, required this.age, this.tags = const []});

  @override
  User fromJson(Map<String, dynamic> json) => User(
    name: json['name'] as String,
    age: json['age'] as int,
    tags: (json['tags'] as List).cast<String>(),
  );

  @override
  Map<String, dynamic> toJson() => {
    'name': name,
    'age': age,
    'tags': tags,
  };
}
```

### 结合 dart-core-libraries 的延伸练习：通用 JSON 工具

```dart
import 'dart:convert';

class JsonHelper {
  static String prettyPrint(Map<String, dynamic> json) {
    return const JsonEncoder.withIndent('  ').convert(json);
  }

  static T? safeGet<T>(Map<String, dynamic> json, String key) {
    if (!json.containsKey(key)) return null;
    final value = json[key];
    return value is T ? value : null;
  }

  static Map<String, dynamic> deepCopy(Map<String, dynamic> source) {
    return jsonDecode(jsonEncode(source)) as Map<String, dynamic>;
  }
}
```
