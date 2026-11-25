---
name: dart-null-safety
description: 运用 Dart 健全空安全机制（Sound Null Safety），消除空引用异常并编写类型安全的代码。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T10:00:00Z
---
# 掌握 Dart 空安全

## Contents
- [核心原则](#核心原则)
- [类型系统中的可空性](#类型系统中的可空性)
- [空安全的语法与操作符](#空安全的语法与操作符)
- [流程分析与类型提升](#流程分析与类型提升)
- [Late 变量与延迟初始化](#late-变量与延迟初始化)
- [核心库的空安全变更](#核心库的空安全变更)
- [Dart 3 空安全迁移](#dart-3-空安全迁移)
- [Workflow: 实现空安全的 Dart 代码](#workflow-实现空安全的-dart-代码)
- [Examples](#examples)

## 核心原则

Dart 的空安全基于两条核心原则：

**默认不可空** — 除非将变量显式声明为可空，否则它一定是非空的类型。`String` 类型的变量必须包含一个字符串，不能为 `null`。

**完全可靠** — Dart 的类型系统保证：如果一个表达式有不可空的静态类型，那么它在运行时永远不会为 `null`。类型检查器会在编译时捕获所有潜在的空引用错误。

## 类型系统中的可空性

空安全从根本上改变了 Dart 的类型层级：

- `Null` 类型不再是所有类型的子类。`null` 只能赋值给 `Null` 或可空类型（如 `String?`）。
- 所有类型默认为非空。`int`、`String`、`List<int>` 等不能包含 `null`。
- 可空类型通过在类型后加 `?` 声明：`String?` 等价于 `String | Null`。
- `Object` 不再是最顶层类型，改用 `Object?` 表示可以接受任何值的类型。
- 新的底层类型 `Never` 表示永远不会成功返回的表达式（如 `throw`）。

```dart
int a = 42;           // 非空，不能赋值为 null
int? b = null;         // 可空，可以赋值为 null
String? name;          // 默认为 null

// 可空类型只能访问 Null 类也定义的方法
// 即 toString()、==、hashCode
```

## 空安全的语法与操作符

### Null-aware 操作符

| 操作符 | 用法 | 说明 |
|--------|------|------|
| `?.` | `obj?.method()` | 如果 `obj` 为 null 则短路返回 null |
| `??` | `a ?? b` | 如果 `a` 为 null 则使用 `b` |
| `??=` | `a ??= b` | 如果 `a` 为 null 则赋值 `b` |
| `!` | `obj!.method()` | 断言 `obj` 不为 null（运行时检查） |

```dart
String? name;
print(name?.length);       // null（不会崩溃）
print(name?.length ?? 0);  // 0

List<int>? list;
list?.add(1);              // 安全调用

// 空值断言：确信值不为 null 时使用
String? input = 'hello';
print(input!.length);      // 5
```

### 空值断言操作符 `!`

使用 `!` 将可空类型强制转换为非空类型。仅在确信值不为 null 时使用，否则运行时抛出 `TypeError`：

```dart
String? nullable = getValue();
String nonNullable = nullable!;  // 运行时检查
```

## 流程分析与类型提升

Dart 的流程分析可以在判断 `null` 检查后自动将可空类型提升为非空类型：

```dart
String? name;

if (name != null) {
  print(name.length);  // 类型提升：name 现在是 String
}

// 提前返回模式也支持类型提升
int getLength(String? value) {
  if (value == null) return 0;
  return value.length;  // 这里 value 已提升为 String
}
```

### 赋值分析

编译器跟踪变量的赋值状态，确保非空变量在使用前已被初始化：

```dart
int result;                    // OK，不需要立即初始化
if (condition) {
  result = 1;
} else {
  result = 2;
}
print(result);                 // OK，所有路径都已赋值
```

### Never 类型

`Never` 类型用于永远不会返回的函数，帮助流程分析：

```dart
Never throwError(String msg) {
  throw ArgumentError(msg);
}

int parse(String? value) {
  if (value == null) throwError('Cannot be null');
  return int.parse(value);     // value 已提升为 String
}
```

## Late 变量与延迟初始化

`late` 关键字用于延迟初始化非空变量：

```dart
class Database {
  late final Connection connection;  // 延迟初始化
  
  void init() {
    connection = Connection.open();  // 运行时检查
  }
}

// Late 变量在首次访问时初始化
late String greeting = _computeGreeting();  // 懒加载
```

**使用场景**：
- 在构造函数体中初始化 `final` 字段
- 懒加载开销大的计算
- 依赖注入模式

## 核心库的空安全变更

Dart 3 对核心库做了以下重要变更：

| 变更 | 说明 |
|------|------|
| `Map.[]` 返回可空 | `map[key]` 返回 `V?`，因为 key 可能不存在 |
| 移除 `List()` 构造 | 使用 `[]` 字面量或 `List.filled()` |
| `Iterator.current` 可空 | 迭代前后访问返回 `null` |
| `num.parse()` 移除 `onError` | 使用 `tryParse()` 代替 |
| 移除隐式转换 | 不再自动将 `dynamic` 转为具体类型 |

```dart
var map = {'a': 1, 'b': 2};
int? value = map['c'];           // null，而不是异常
print(map['c'] ?? 0);            // 0

// int.parse 替代方案
int? parsed = int.tryParse('abc'); // null
```

## Dart 3 空安全迁移

从 Dart 3 开始，空安全是强制性的，不再需要选择启用。

**迁移步骤**：

1. 更新 `pubspec.yaml` 的 SDK 约束：
```yaml
environment:
  sdk: '>=3.0.0 <4.0.0'
```

2. 确保所有依赖已支持空安全（SDK 下限 >= 2.12.0）。

3. 运行分析检查：
```bash
dart analyze
```

4. 修复常见问题：
   - 可选参数的默认值使用 `=` 而非 `:`。
   - `class` 用作 mixin 时必须标记为 `mixin class`。
   - `switch` 语句的 `continue` 只能指向循环标签。

## Workflow: 实现空安全的 Dart 代码

### Task Progress

- [ ] **Step 1: 确定类型的可空性。** 分析变量是否可能为 null。默认使用非空类型。
- [ ] **Step 2: 声明可空类型。** 对可能为 null 的变量添加 `?`（如 `String?`、`int?`）。
- [ ] **Step 3: 处理可空值。** 使用 `??` 提供默认值，使用 `?.` 安全调用，使用 `if (x != null)` 进行类型提升。
- [ ] **Step 4: 使用 late 延迟初始化。** 对需要延迟赋值的非空字段使用 `late`。
- [ ] **Step 5: 使用 ! 断言非空。** 仅当你确信值不为 null 时使用 `!`。
- [ ] **Step 6: 运行分析器。** 执行 `dart analyze` 检查空安全错误。
- [ ] **Step 7: 运行测试。** 确保所有测试通过，没有空引用异常。
- [ ] **Step 8: Feedback Loop。** 审查分析器输出 → 修复空安全警告 → 重新运行测试 → 重复直到全部通过。

### 条件逻辑

- **如果创建 NEW 代码：** 所有变量默认非空，只在需要时加 `?`。优先使用 `final`。
- **如果编辑 EXISTING 代码：** 逐步迁移，从叶子类开始向上。先修复非空字段的初始化。
- **如果一个字段总是非空但构造函数中不能初始化：** 使用 `late final`。
- **如果一个函数可能无返回值：** 返回可空类型或用 `Never` 表示不返回。
- **如果与旧版库交互：** 使用 `!` 断言或 `??` 提供默认值处理可能的 null。

## Examples

### 完整示例：空安全的数据模型

```dart
class User {
  final String name;           // 非空
  final String? email;         // 可空
  final int? age;              // 可空
  late final DateTime createdAt;  // 延迟赋值
  
  User({required this.name, this.email, this.age}) {
    createdAt = DateTime.now();
  }
  
  String get displayName => name;
  
  String get emailOrFallback => email ?? 'No email provided';
  
  // 工厂方法：从 JSON 安全解析
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      name: json['name'] as String,
      email: json['email'] as String?,   // 可能为 null
      age: json['age'] as int?,
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'name': name,
      if (email != null) 'email': email,
      if (age != null) 'age': age,
    };
  }
}

void main() {
  var user = User.fromJson({
    'name': 'Alice',
    'email': null,
  });
  
  print(user.emailOrFallback);   // "No email provided"
  print(user.name.length);       // 5（安全）
}
```

### 空安全与集合操作

```dart
List<String?> items = ['a', null, 'b', null];

// 过滤 null 值
List<String> nonNull = items.whereType<String>().toList();
print(nonNull);  // ['a', 'b']

// 或使用 where
var filtered = items.where((e) => e != null).toList();

// Map 访问
Map<String, int?> scores = {'Alice': 10, 'Bob': null};
int? bobScore = scores['Bob'];
int aliceScore = scores['Alice'] ?? 0;  // 10
int charlieScore = scores['Charlie'] ?? 0;  // 0（key 不存在）
```

### 类型提升的高级用法

```dart
String? fetchData() => DateTime.now().second % 2 == 0 ? 'data' : null;

void processData() {
  final data = fetchData();
  
  // 模式1: if-null 后返回
  if (data == null) {
    print('No data available');
    return;
  }
  // data 在这里已提升为 String
  print(data.toUpperCase());
}

// 使用 Never 辅助函数
Never fail(String msg) => throw StateError(msg);

int? tryParse(String value) {
  if (int.tryParse(value) case final parsed?) {
    return parsed;
  }
  return null;
}
```
