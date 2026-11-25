---
name: dart-fundamentals
description: 掌握 Dart 语言的基础要素（变量、操作符、控制流、函数、导库），用于编写符合规范的 Dart 代码。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T10:00:00Z
---
# 掌握 Dart 语言基础

## Contents
- [变量与类型推断](#变量与类型推断)
- [操作符](#操作符)
- [控制流](#控制流)
- [函数](#函数)
- [库与导入](#库与导入)
- [错误处理](#错误处理)
- [关键字速查](#关键字速查)
- [Workflow: 编写规范的 Dart 函数](#workflow-编写规范的-dart-函数)
- [Examples](#examples)

## 变量与类型推断

### 声明方式

```dart
var name = 'Dart';       // 类型推断为 String
final age = 10;          // 不可重新赋值，推断为 int
const pi = 3.14;         // 编译时常量，推断为 double
String greeting = 'Hi';  // 显式类型声明
int? nullableValue;      // 可空类型，默认为 null
late String lazyInit;    // 延迟初始化
```

### 选择指南

| 场景 | 推荐 |
|------|------|
| 局部变量，值会变 | `var` |
| 局部变量，值不变 | `final` |
| 编译时常量 | `const` |
| API 边界、字段 | 显式类型 |
| 可能为 null | 显式可空类型 `?` |

### final 与 const 的区别

```dart
final now = DateTime.now();  // OK，运行时确定
const time = DateTime.now(); // 错误！编译时常量不能是运行时值

const list = [1, 2, 3];      // 深度不可变
final mutList = [1, 2, 3];   // 不可重新赋值但内容可变
mutList.add(4);               // OK
```

## 操作符

### 算术与比较

```dart
// 算术
a + b   a - b   a * b   a / b    a ~/ b   a % b

// 比较
a == b   a != b   a > b   a < b   a >= b   a <= b

// 类型检查
a is String    a is! String    a as String
```

### 逻辑与空安全操作符

```dart
// 逻辑操作符
!a    a && b    a || b

// 空安全操作符
a ?? b         // 如果 a 为 null 则取 b
a?.b           // 安全访问：a 为 null 时短路返回 null
a ??= b        // 如果 a 为 null 则赋值 b
a!             // 断言非 null（运行时检查）
```

### 级联操作符

```dart
// 级联 (..) 对同一对象执行多个操作
var buffer = StringBuffer()
  ..write('Hello')
  ..write(' ')
  ..writeAll(['Dart', '!']);

// 空安全级联 (?..)
StringBuffer? buf;
buf?..write('safe');
```

### 集合操作符

```dart
// Spread (...)
var list = [1, 2, 3];
var combined = [0, ...list, 4];  // [0, 1, 2, 3, 4]

// 空安全 spread (...?)
List<int>? nullableList;
var safe = [0, ...?nullableList]; // [0]

// Collection if / for
var nav = ['Home', if (isAdmin) 'Admin', for (var i in items) '#$i'];
```

## 控制流

### 分支

```dart
// if-else
if (isRaining) {
  bringUmbrella();
} else if (isSunny) {
  wearSunglasses();
} else {
  stayHome();
}

// switch 表达式 (Dart 3+)
var status = switch (score) {
  >= 90 => '优秀',
  >= 60 => '及格',
  _     => '不及格',
};

// switch 语句 + 模式匹配
switch (pair) {
  case (int x, int y):
    print('坐标: ($x, $y)');
  case (String name, _):
    print('文本: $name');
}
```

### 循环

```dart
// for
for (var i = 0; i < 5; i++) { ... }

// for-in
for (final item in items) { ... }

// while / do-while
while (condition) { ... }
do { ... } while (condition);

// 可迭代方法链
items.where((e) => e > 0).map((e) => e * 2).forEach(print);
```

## 函数

### 函数定义

```dart
// 基本函数
int add(int a, int b) => a + b;

// 可选位置参数
String greet(String name, [String? title]) {
  return '${title ?? ''} $name';
}

// 可选命名参数（推荐）
String format({
  required String text,
  bool bold = false,
  Color? color,
}) {
  // ...
}

// 匿名函数（lambda）
var list = ['a', 'bb', 'ccc'];
list.where((e) => e.length > 1);
```

### 参数最佳实践

- 必要的参数使用 `required` 命名参数（Dart 3+ 不再推荐大量位置参数）
- 可选参数提供合理的默认值
- 函数体短于一行时使用 `=>` 箭头语法

### 函数作为一等公民

```dart
void Function(int) callback = (value) => print(value);

void execute(void Function(int) fn, int data) {
  fn(data);
}

// 级联传递
[1, 2, 3].map((e) => e * 2).where((e) => e > 2).toList();
```

## 库与导入

### 创建库

```dart
// lib/my_library.dart
library my_library;

// 导出公开 API
export 'src/internal.dart' show PublicClass;
```

### 导入方式

```dart
// 核心库
import 'dart:math';

// Package 库
import 'package:http/http.dart' as http;

// 相对路径导入
import '../utils/helpers.dart';

// show / hide（控制导入范围）
import 'package:lib/lib.dart' show VisibleFunction;
import 'package:lib/lib.dart' hide InternalClass;

// 延迟导入（懒加载）
import 'package:heavy_lib/heavy_lib.dart' deferred as heavy;
// 使用时:
await heavy.loadLibrary();
heavy.HeavyClass().doWork();
```

### 库可见性

- 以下划线 `_` 开头的标识符是库私有的
- 每个 Dart 文件是一个独立的库
- `part` 和 `part of` 用于将一个库拆分到多个文件中

```dart
// src/base.dart
part 'internal.dart';

class PublicClass {}     // 外部可见
class _PrivateClass {}   // 仅本库可见

// src/internal.dart
part of 'base.dart';

class _InternalHelper {}
```

## 错误处理

### try-catch-finally

```dart
try {
  var result = await riskyOperation();
  processResult(result);
} on FormatException catch (e) {
  print('格式错误: $e');
} on IOException {
  print('IO 错误');
} catch (e, stack) {
  print('未知错误: $e\n$stack');
} finally {
  await cleanup();
}
```

### 抛出自定义异常

```dart
class ValidationError extends Error {
  final String message;
  ValidationError(this.message);

  @override
  String toString() => 'ValidationError: $message';
}

void validate(String input) {
  if (input.isEmpty) {
    throw ValidationError('Input cannot be empty');
  }
}
```

## 关键字速查

### 常用关键字分类

| 类别 | 关键字 |
|------|--------|
| 声明 | `var`, `final`, `const`, `late` |
| 类型 | `class`, `enum`, `mixin`, `extension`, `typedef` |
| 函数 | `Function`, `return`, `void`, `async`, `await`, `yield` |
| 控制流 | `if`, `else`, `switch`, `case`, `for`, `while`, `do`, `break`, `continue` |
| 错误 | `try`, `catch`, `finally`, `throw`, `on`, `rethrow` |
| 库 | `import`, `export`, `part`, `library`, `deferred`, `show`, `hide` |
| 类成员 | `static`, `get`, `set`, `operator`, `this`, `super`, `new` |
| 修饰符 | `abstract`, `sealed`, `interface`, `base`, `final`（class） |
| 其他 | `is`, `as`, `in`, `with`, `implements`, `extends`, `required` |

## Workflow: 编写规范的 Dart 函数

### Task Progress

- [ ] **Step 1: 确定函数的输入输出。** 明确参数的数量、类型和可空性。使用命名参数（带 `required`）以增强可读性。
- [ ] **Step 2: 声明返回类型。** 如果可能返回 null 使用可空类型（`String?`），如果不会返回使用 `Never`，异步用 `Future<T>`。
- [ ] **Step 3: 处理边界情况。** 在函数开头处理 null、空集合、特殊情况，使用 `if (x == null) return` 提早返回。
- [ ] **Step 4: 实现主体逻辑。** 使用类型推断（`final`、`var`），保持函数短小（建议 < 30 行）。
- [ ] **Step 5: 添加文档注释。** 使用 `///` 注释说明函数功能、参数含义和返回值。
- [ ] **Step 6: 运行分析器。** 执行 `dart analyze` 确保无类型错误。
- [ ] **Step 7: 编写测试。** 覆盖边界情况和主要用况，验证函数行为正确。
- [ ] **Step 8: Feedback Loop。** 运行测试 → 分析失败用例 → 修正逻辑 → 重复直到全部通过。

### 条件逻辑

- **如果参数超过 3 个：** 使用命名参数或封装为对象。
- **如果函数内部创建 NEW 对象：** 使用 `final` 声明不可变性。
- **如果返回值可能为 null：** 返回 `T?` 而非抛异常，让调用方用 `??` 处理。
- **如果函数是纯计算（无副作用）：** 标记为 `const` 或考虑提取为静态方法。
- **如果使用 `switch` 判断多分支：** 使用 Dart 3 的 switch 表达式和模式匹配，确保处理所有情况。
- **如果导入产生名称冲突：** 使用 `as` 前缀重命名，或用 `show`/`hide` 控制导入范围。

## Examples

### 完整的用户输入验证

```dart
import 'dart:convert';

/// 用户注册请求的数据模型。
class RegistrationRequest {
  final String username;
  final String email;
  final String password;

  const RegistrationRequest({
    required this.username,
    required this.email,
    required this.password,
  });

  factory RegistrationRequest.fromJson(String jsonStr) {
    final map = jsonDecode(jsonStr) as Map<String, dynamic>;
    return RegistrationRequest(
      username: map['username'] as String,
      email: map['email'] as String,
      password: map['password'] as String,
    );
  }
}

/// 验证注册请求并返回错误信息列表。
/// 返回空列表表示验证通过。
List<String> validate(RegistrationRequest request) {
  final errors = <String>[];

  if (request.username.isEmpty) {
    errors.add('用户名不能为空');
  } else if (request.username.length < 3) {
    errors.add('用户名至少 3 个字符');
  }

  if (!request.email.contains('@')) {
    errors.add('邮箱格式不正确');
  }

  if (request.password.length < 8) {
    errors.add('密码至少 8 位');
  }

  return errors;
}

void main() {
  final valid = RegistrationRequest(
    username: 'alice',
    email: 'alice@example.com',
    password: 'secure123',
  );

  final errors = validate(valid);
  if (errors.isEmpty) {
    print('验证通过！');
  } else {
    for (final e in errors) {
      print('验证失败: $e');
    }
  }
}
```

### 使用集合操作符处理数据

```dart
List<int> filterAndTransform(List<int> numbers) {
  return [
    for (final n in numbers)
      if (n > 0)
        n * n
  ];
}

void main() {
  final input = [-2, -1, 0, 1, 2, 3];
  final squares = filterAndTransform(input);
  print(squares);  // [1, 4, 9]
}
```

### 使用 switch 表达式

```dart
String describeFruit(String fruit) => switch (fruit) {
  'apple' || 'pear'    => '仁果类水果',
  'banana' || 'mango'  => '热带水果',
  'grape' || 'berry'   => '浆果类',
  _                     => '其他水果',
};
```
