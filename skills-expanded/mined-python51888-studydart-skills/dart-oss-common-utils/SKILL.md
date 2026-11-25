---
name: dart-oss-common-utils
description: 学习 Sky24n/common_utils 开源项目，通过实用工具类库掌握 Dart SDK 核心库（dart:core、dart:io、dart:convert）的实战应用，避免重复造轮子。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-core-libraries
    - dart-fundamentals
  project:
    url: https://github.com/Sky24n/common_utils
    stars: 1452
    difficulty: beginner
    category: library
---

# 学习 Common Utils 工具库项目

## Contents

- [项目概览](#项目概览)
- [与 dart-core-libraries 的关联](#与-dart-core-libraries-的关联)
- [项目结构导读](#项目结构导读)
- [工具类详解](#工具类详解)
- [Workflow: 通过工具库学习核心库 API](#workflow-通过工具库学习核心库-api)
- [Examples](#examples)

## 项目概览

**项目名称**: common_utils
**作者**: Sky24n
**GitHub**: https://github.com/Sky24n/common_utils
**Stars**: 1.5k | **难度**: 入门级

一个纯 Dart 通用工具类库，包含日期处理、加密、JSON、日志、金额格式化、正则、文本、时间轴、计时器等十余种工具类。该项目展示了 `dart:core`、`dart:io`、`dart:convert`、`dart:math` 等核心库的综合实战用法。

## 与 dart-core-libraries 的关联

该项目是 `dart-core-libraries` 技能的直接应用集合：

| dart-core-libraries 主题 | 项目工具类 |
|-------------------------|----------|
| String / RegExp 操作 | RegexUtil, TextUtil |
| DateTime / Duration | DateUtil, TimelineUtil, TimerUtil |
| JSON 编解码 | JsonUtil |
| 数学运算 | NumUtil, MoneyUtil |
| 类型判断 | ObjectUtil |
| 加密相关 | EncryptUtil |

## 项目结构导读

```
common_utils/
├── lib/
│   ├── common_utils.dart          # 导出所有工具类
│   └── src/
│       ├── date_util.dart         # 日期格式化、时间差计算
│       ├── encrypt_util.dart      # MD5、Base64、SHA
│       ├── json_util.dart         # JSON 深拷贝、对象转 JSON
│       ├── log_util.dart          # 分级日志输出
│       ├── money_util.dart        # 金额格式化（分→元）
│       ├── num_util.dart          # 数值保留小数、千分位
│       ├── object_util.dart       # 类型判断与转换
│       ├── regex_util.dart        # 手机号、邮箱、身份证正则
│       ├── text_util.dart         # 字符串判空、截取
│       ├── timeline_util.dart     # 时间轴格式化（刚刚、N分钟前）
│       └── timer_util.dart        # 倒计时、轮询定时器
├── test/                          # 单元测试
└── pubspec.yaml
```

## 工具类详解

### DateUtil — 日期格式化

```dart
class DateUtil {
  static String format(DateTime date, {String fmt = 'yyyy-MM-dd HH:mm:ss'}) {
    // 核心逻辑：使用 intl 或手动格式化
    // 本质是对 dart:core DateTime API 的封装
  }

  static int daysBetween(DateTime from, DateTime to) {
    // Duration 计算
    return to.difference(from).inDays;
  }
}
```

### RegexUtil — 正则校验

```dart
class RegexUtil {
  static bool isMobile(String input) =>
      RegExp(r'^1[3-9]\d{9}$').hasMatch(input);

  static bool isEmail(String input) =>
      RegExp(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$').hasMatch(input);
}
```

### EncryptUtil — 加密工具

```dart
import 'dart:convert';
import 'package:crypto/crypto.dart';

class EncryptUtil {
  static String md5(String input) =>
      md5.convert(utf8.encode(input)).toString();

  static String base64Encode(String input) =>
      base64.encode(utf8.encode(input));
}
```

## Workflow: 通过工具库学习核心库 API

### Task Progress

- [ ] **Step 1: 浏览工具类列表。** 打开 `lib/common_utils.dart` 查看所有导出的工具类。
- [ ] **Step 2: 选择一个感兴趣的工具类。** 比如从 `DateUtil` 开始，学习 DateTime API。
- [ ] **Step 3: 阅读测试代码。** 打开对应 test 文件，理解每个方法的输入输出。
- [ ] **Step 4: 对照 dart.cn 文档。** 查阅 `dart-core-libraries` 技能中对应的核心库 API。
- [ ] **Step 5: 手写练习。** 不看书，自己实现一个类似的工具方法。
- [ ] **Step 6: 对比优劣。** 将你的实现与项目代码对比，理解项目的设计考量。
- [ ] **Step 7: 扩展工具。** 为项目添加一个新的工具类（如 FileUtil、ColorUtil）。
- [ ] **Step 8: Feedback Loop。** 运行 `dart analyze` → `dart test` → 修正问题 → 提交。

### 条件逻辑

- **如果对某个 Dart 核心 API 不熟悉：** 使用 `dart-core-libraries` 技能查阅完整说明。
- **如果需要新增工具类：** 先确认 dart:core 是否已有类似功能，避免重复造轮子。
- **如果测试覆盖不足：** 为现有工具方法补充边界情况测试。
- **如果需要性能优化：** 使用 `Stopwatch` 测量工具方法的执行时间。

## Examples

### 从项目中学到的工具方法模式

```dart
String numToMoneyString(double amount) {
  final parts = amount.toStringAsFixed(2).split('.');
  final intPart = parts[0];
  final buffer = StringBuffer();
  for (var i = 0; i < intPart.length; i++) {
    if (i > 0 && (intPart.length - i) % 3 == 0) {
      buffer.write(',');
    }
    buffer.write(intPart[i]);
  }
  return '\$${buffer.toString()}.${parts[1]}';
}

void main() {
  print(numToMoneyString(1234567.89)); // $1,234,567.89
}
```

### 结合 dart-core-libraries 的延伸

```dart
import 'dart:io';
import 'dart:convert';
import 'dart:math';

class FileUtil {
  static Future<Map<String, dynamic>> readJson(String path) async {
    final file = File(path);
    final content = await file.readAsString();
    return jsonDecode(content) as Map<String, dynamic>;
  }

  static Future<void> writeJson(
    String path,
    Map<String, dynamic> data,
  ) async {
    final file = File(path);
    await file.writeAsString(jsonEncode(data));
  }

  static int randomInt(int max) =>
      Random().nextInt(max);
}
```
