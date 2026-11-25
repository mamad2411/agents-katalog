---
description: Dart/Flutter development rules - naming conventions, widget patterns, state management
globs: frontend/**/*.dart,**/*.yaml,**/*.yml
---

# Dart/Flutter Development Rules

**Naming conventions, widget patterns, and state management** guidelines for Dart/Flutter development.

## 🔧 Naming Conventions

### **Class Names: PascalCase**
```dart
// ✅ DO: Descriptive class names
class AuthService { }
class RegisterResponse { }
class UserProfileCard { }
class DatabaseConnection { }

// ❌ DON'T: Ambiguous class names
class Service { }
class Data { }
class Helper { }
```

### **Variables/Functions: camelCase**
```dart
// ✅ DO: Descriptive variable names
String userEmail = 'user@example.com';
bool isUserActive = true;
bool hasAdminPermission = false;
double learningRate = 0.001;

Future<void> handleUserRegistration() async { }
Future<bool> validateEmailFormat() async { }

// ❌ DON'T: Ambiguous variable names
String email = 'user@example.com';
bool flag = true;
bool perm = false;
double lr = 0.001;

Future<void> handle() async { }
```

### **Constants: UPPER_SNAKE_CASE**
```dart
// ✅ DO: Constant naming
const String API_BASE_URL = 'https://api.example.com';
const int MAX_RETRY_COUNT = 3;
const Duration DEFAULT_TIMEOUT = Duration(seconds: 30);

// ❌ DON'T: Naming like regular variables
const String apiBaseUrl = 'https://api.example.com';
const int maxRetryCount = 3;
```

### **Private Members: Start with _**
```dart
// ✅ DO: Mark private members
class AuthService {
  String _email = '';
  String _password = '';
  
  Future<void> _validateInput() async { }
  Future<void> _sendNotification() async { }
}
```

### **File Names: snake_case**
```dart
// ✅ DO: File naming
auth_service.dart
register_screen.dart
user_models.dart
database_connection.dart

// ❌ DON'T: PascalCase file names
AuthService.dart
RegisterScreen.dart
```

## 🎨 Flutter Widget Patterns

### **Widget Structure**
```dart
// ✅ DO: Clear widget structure
class UserProfileCard extends StatelessWidget {
  final UserModel user;
  final VoidCallback onTap;
  
  const UserProfileCard({
    Key? key,
    required this.user,
    required this.onTap,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(user.name),
        subtitle: Text(user.email),
        onTap: onTap,
      ),
    );
  }
}

// ❌ DON'T: Complex and long widgets
class ComplexWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 200+ lines of complex UI
  }
}
```

### **StatefulWidget Pattern**
```dart
// ✅ DO: StatefulWidget structure
class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  // 1. Controller declarations
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  
  // 2. State variables
  bool _isLoading = false;
  bool _obscurePassword = true;
  
  // 3. Lifecycle methods
  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
  
  // 4. Business logic methods
  Future<void> _handleRegister() async {
    // Implementation...
  }
  
  // 5. Validation methods
  String? _validateEmail(String? value) {
    // Implementation...
  }
  
  // 6. UI build method
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // UI implementation...
    );
  }
}
```

## 🔄 State Management

### **State Management Pattern**
```dart
// ✅ DO: Appropriate state management
class _RegisterScreenState extends State<RegisterScreen> {
  bool _isLoading = false;
  String? _errorMessage;
  
  Future<void> _handleRegister() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });
    
    try {
      final response = await ApiService.register(
        _emailController.text.trim(),
        _passwordController.text,
      );
      
      if (response != null) {
        // Success handling
        if (mounted) {
          Navigator.pop(context);
        }
      } else {
        // Failure handling
        if (mounted) {
          setState(() {
            _errorMessage = 'Registration failed.';
          });
        }
      }
    } catch (e) {
      // Error handling
      if (mounted) {
        setState(() {
          _errorMessage = 'Network error occurred.';
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }
}
```

## 🎯 UI/UX Principles

### **Responsive Design**
```dart
// ✅ DO: Responsive layout
class ResponsiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 800) {
          return DesktopLayout();  // Desktop layout
        } else if (constraints.maxWidth > 400) {
          return TabletLayout();   // Tablet layout
        } else {
          return MobileLayout();   // Mobile layout
        }
      },
    );
  }
}
```

### **const Constructor Usage**
```dart
// ✅ DO: Use const constructors
class AppTitle extends StatelessWidget {
  const AppTitle({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return const Text(
      'App Title',
      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
    );
  }
}
```

## 📝 Form Validation Patterns

### **Input Validation**
```dart
// ✅ DO: Form validation pattern
String? _validateEmail(String? value) {
  if (value == null || value.isEmpty) {
    return 'Please enter an email.';
  }
  
  final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
  if (!emailRegex.hasMatch(value)) {
    return 'Please enter a valid email format.';
  }
  
  return null;
}

String? _validatePassword(String? value) {
  if (value == null || value.isEmpty) {
    return 'Please enter a password.';
  }
  
  if (value.length < 6) {
    return 'Password must be at least 6 characters.';
  }
  
  return null;
}
```

## 🧪 Test Patterns

### **Widget Testing**
```dart
// ✅ DO: Widget test writing
testWidgets('User profile card displays correctly', (WidgetTester tester) async {
  final user = UserModel(name: 'John Doe', email: 'john@example.com');
  
  await tester.pumpWidget(
    MaterialApp(
      home: UserProfileCard(
        user: user,
        onTap: () {},
      ),
    ),
  );
  
  expect(find.text('John Doe'), findsOneWidget);
  expect(find.text('john@example.com'), findsOneWidget);
});
```

## 🔍 Error Handling Patterns

### **UI Error Handling**
```dart
// ✅ DO: UI error handling
if (response != null) {
  // Success handling
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(response.message),
      backgroundColor: Colors.green,
    ),
  );
} else {
  // Failure handling
  ScaffoldMessenger.of(context).showSnackBar(
    const SnackBar(
      content: Text('Operation failed.'),
      backgroundColor: Colors.red,
    ),
  );
}
```

## 🔧 Logging Patterns

### **developer.log Usage**
```dart
import 'dart:developer' as developer;

// ✅ DO: Logging pattern
developer.log('Registration successful: ${user.email}', name: 'AuthService');
developer.log('Supabase registration failed: ${e.message}', name: 'AuthService');
developer.log('Registration error: $e', name: 'AuthService');

// ❌ DON'T: Log sensitive information
developer.log('Password: $password', name: 'AuthService');
```

## ✅ Dart/Flutter Development Checklist

### **Code Quality**
- [ ] **Naming**: Follow camelCase, PascalCase rules
- [ ] **Widget Separation**: Separate into reusable widgets
- [ ] **const Constructors**: Use actively
- [ ] **Lifecycle**: Clean up resources in dispose() method

### **UI/UX**
- [ ] **Responsive Design**: Support various screen sizes
- [ ] **Form Validation**: Appropriate validation for user input
- [ ] **UI Feedback**: Display loading states, error messages
- [ ] **Accessibility**: Use Semantics widgets

### **State Management**
- [ ] **Appropriate Widgets**: Proper use of StatefulWidget/StatelessWidget
- [ ] **State Separation**: Unidirectional data flow
- [ ] **mounted Check**: Check state before UI updates

### **Testing**
- [ ] **Widget Tests**: Verify UI components
- [ ] **Unit Tests**: Verify business logic
- [ ] **Integration Tests**: Verify complete flows