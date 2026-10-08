# MyTestApp Flutter项目 - Cursor AI代码生成规则

## 项目概述
这是一个基于Flutter的端到端加密群聊应用，采用去中心化P2P架构。使用Provider进行状态管理，支持跨平台运行。

## 代码风格要求

### 命名规范
- 文件：小写+下划线 `user_setup_screen.dart`
- 类：PascalCase `User`, `GroupService`, `ChatScreen`
- 变量/函数：camelCase `currentUser`, `sendMessage()`
- 私有成员：下划线前缀 `_currentUser`, `_handleMessage()`
- 常量：小写+下划线 `_algorithm`, `_key_length`

### 导入顺序
```dart
// 1. Dart标准库
import 'dart:convert';
import 'dart:io';

// 2. Flutter框架
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// 3. 第三方包
import 'package:json_annotation/json_annotation.dart';

// 4. 项目内部
import '../models/user.dart';
import '../services/encryption_service.dart';
```

### 类结构
```dart
class ExampleClass {
  // 1. 静态常量
  static const String _constant = 'value';
  
  // 2. 实例变量
  final String id;
  String? _privateVariable;
  
  // 3. 构造函数
  ExampleClass({required this.id});
  
  // 4. 工厂构造函数
  factory ExampleClass.fromJson(Map<String, dynamic> json) => ...;
  
  // 5. Getter/Setter
  String get displayName => _privateVariable ?? 'default';
  
  // 6. 公共方法
  Future<void> publicMethod() async { ... }
  
  // 7. 私有方法
  void _privateMethod() { ... }
}
```

## 架构模式

### 模型层 (models/)
- 使用`@JsonSerializable()`注解
- 包含`fromJson`和`toJson`方法
- 使用枚举定义状态

### 服务层 (services/)
- 单例模式：`static final _instance = Service._internal()`
- 异步方法使用`async/await`
- 错误处理使用try-catch

### 状态管理 (providers/)
- 继承`ChangeNotifier`
- 使用`notifyListeners()`通知UI更新
- 私有变量存储状态

### UI层 (screens/)
- StatefulWidget用于有状态界面
- 使用`Consumer<AppProvider>`监听状态变化
- 私有方法构建UI组件

## 编码规范

### 异步编程
```dart
Future<void> exampleAsync() async {
  try {
    final data = await fetchData();
    final processed = await processData(data);
    await saveData(processed);
  } catch (e) {
    print('操作失败: $e');
  }
}
```

### 错误处理
```dart
try {
  final result = await riskyOperation();
  return result;
} catch (e) {
  print('操作失败: $e');
  throw CustomException('操作失败: $e');
}
```

### 空安全
```dart
String? nullableString;
final displayName = nullableString ?? 'Unknown';
final length = nullableString?.length;
```

## 安全要求

### 加密相关
- 使用AES-256-GCM加密消息
- 密钥使用安全的随机生成器
- 避免在日志中输出敏感信息

### 数据验证
```dart
void validateInput(String input) {
  if (input.isEmpty) {
    throw ValidationException('输入不能为空');
  }
}
```

## UI组件规范

### 界面结构
```dart
class ExampleScreen extends StatefulWidget {
  final String title;
  const ExampleScreen({super.key, required this.title});
  
  @override
  State<ExampleScreen> createState() => _ExampleScreenState();
}

class _ExampleScreenState extends State<ExampleScreen> {
  final _controller = TextEditingController();
  
  @override
  void initState() {
    super.initState();
  }
  
  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: _buildBody(),
    );
  }
  
  Widget _buildBody() {
    return Consumer<AppProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        return _buildContent(provider);
      },
    );
  }
}
```

### 状态管理使用
```dart
// 监听状态变化
Consumer<AppProvider>(
  builder: (context, provider, child) {
    return Text(provider.currentUser?.name ?? 'Unknown');
  },
)

// 一次性读取
context.read<AppProvider>().performAction();
```

## 注释规范

### 文档注释
```dart
/// 类的文档注释
class ExampleClass {
  /// 字段的文档注释
  final String exampleField;
  
  /// 方法的文档注释
  /// 
  /// [param1] 参数1的描述
  /// 返回值的描述
  Future<String> exampleMethod(String param1) async {
    // 行内注释用于解释复杂逻辑
    final result = await _processData(param1);
    return result;
  }
}
```

## 性能优化

### 内存管理
- 及时释放控制器和监听器
- 使用`const`构造函数
- 避免内存泄漏

### 异步操作
- 避免阻塞主线程
- 合理使用Future和Stream

## 测试要求

### 单元测试
```dart
void main() {
  group('ExampleService Tests', () {
    late ExampleService service;
    
    setUp(() {
      service = ExampleService();
    });
    
    test('should perform operation successfully', () async {
      final result = await service.performOperation();
      expect(result.isSuccess, isTrue);
    });
  });
}
```

## 注意事项

1. 所有代码必须通过Flutter分析器检查
2. 遵循Flutter官方最佳实践
3. 保持代码简洁和可读性
4. 优先使用Flutter内置组件
5. 注意跨平台兼容性
6. 重视用户体验和性能优化
7. 使用中文注释和错误信息
8. 确保P2P通信的稳定性
9. 实现端到端加密的安全性
10. 支持二维码扫码功能 