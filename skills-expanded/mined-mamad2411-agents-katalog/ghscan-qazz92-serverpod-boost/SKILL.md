# ServerPod Endpoints

{{#has_endpoints}}
## Existing Endpoints

This project has **{{endpoint_count}} endpoint(s)**:

{{#endpoints}}
### {{name}}
- **File:** `{{file}}`
- **Methods:** {{method_count}}

{{#methods}}
- `{{signature}}`
{{/methods}}

{{/endpoints}}

Follow these existing patterns when adding new endpoints.

---

## Adding New Endpoints

{{/has_endpoints}}
{{^has_endpoints}}
## Creating Your First Endpoint

This project doesn't have any endpoints yet. Let's create one:

---

{{/has_endpoints}}

### Step 1: Define the Endpoint

Create a new file in `{{project_name}}_server/lib/src/endpoints/`:

```dart
// {{project_name}}_server/lib/src/endpoints/user_endpoint.dart
import 'package:serverpod/serverpod.dart';

class UserEndpoint extends Endpoint {
  /// Creates a new user and returns the user ID
  Future<int?> createUser(
    Session session,
    String email,
    String password,
  ) async {
    // Check if user already exists
    final existing = await User.find(
      session,
      where: (u) => u.email.equals(email),
    );

    if (existing.isNotEmpty) {
      throw InvalidInputException('Email already registered');
    }

    // Hash password
    final hashed = await session.auth.signUp(email, password);

    // Create user
    final user = User(
      email: email,
      passwordHash: hashed,
      createdAt: DateTime.now(),
    );

    await user.insert(session);
    return user.id;
  }

  /// Gets user information by ID
  Future<UserData?> getUser(Session session, int userId) async {
    final user = await User.findById(session, userId);

    if (user == null) {
      throw InvalidInputException('User not found: $userId');
    }

    return UserData(
      id: user.id!,
      email: user.email,
      createdAt: user.createdAt,
    );
  }

  /// Lists users with pagination
  Future<List<UserData>> listUsers(
    Session session,
    int limit,
    int offset,
  ) async {
    final users = await User.find(
      session,
      limit: limit,
      offset: offset,
      orderBy: User.createdAt,
      orderDescending: true,
    );

    return users.map((u) => UserData(
      id: u.id!,
      email: u.email,
      createdAt: u.createdAt,
    )).toList();
  }
}
```

### Step 2: Generate Protocol

Run the protocol generator:

```bash
serverpod generate
```

This creates the client-side code automatically.

### Step 3: Use in Client

```dart
// In your Flutter app or client
final userId = await session.user.createUser(
  email: 'user@example.com',
  password: 'secure_password',
);

final user = await session.user.getUser(userId);
print('Created user: ${user.email}');
```

## Method Signature Best Practices

### Do's ✓

- **Always return `Future<T>`** for async operations
- **Use `Session session`** as the first parameter
- **Use typed parameters** with concrete types
- **Document complex types** with comments
- **Return nullable types** only when appropriate

```dart
// ✓ Good
Future<UserData?> getUser(Session session, int userId) async {
  final user = await User.findById(session, userId);
  return user?.toData();
}

// ✓ Good with documentation
Future<List<UserData>> searchUsers(
  Session session,
  String query, // Case-insensitive email search
  int limit, // Maximum 100
) async {
  // Implementation
}
```

### Don'ts ✗

```dart
// ✗ Bad - untyped return
Future<dynamic> getUser(Session session, int userId) async {}

// ✗ Bad - missing Session parameter
Future<User> getUser(int userId) async {}

// ✗ Bad - using dynamic
Future<void> updateUser(Session session, dynamic data) async {}
```

## Advanced Patterns

### Streaming Responses

For long-running operations, use streaming to send progress updates:

```dart
Stream<String> processLargeFile(
  Session session,
  String fileId,
) async* {
  yield 'Starting process...';

  final file = await UploadedFile.findById(session, fileId);

  yield 'Processing ${file.name}...';

  // Process file in chunks
  final chunks = file.data.chunked(1000);
  for (final (i, chunk) in chunks.indexed) {
    await processChunk(session, chunk);
    yield 'Processed chunk ${i + 1}/${chunks.length}';
  }

  yield 'Process complete!';
}
```

### Authentication

Check if a user is authenticated:

```dart
Future<UserData> getProfile(Session session) async {
  final userId = session.userId;

  if (userId == null) {
    throw UnauthorizedException('Not authenticated');
  }

  final user = await User.findById(session, userId);

  if (user == null) {
    throw UnauthorizedException('User not found');
  }

  return user.toData();
}
```

### Input Validation

Validate all inputs before using them:

```dart
Future<void> changePassword(
  Session session,
  String oldPassword,
  String newPassword,
) async {
  final userId = session.userId;
  if (userId == null) {
    throw UnauthorizedException('Not authenticated');
  }

  // Validate password strength
  if (newPassword.length < 8) {
    throw InvalidInputException('Password must be at least 8 characters');
  }

  if (!RegExp(r'[A-Z]').hasMatch(newPassword)) {
    throw InvalidInputException('Password must contain uppercase letters');
  }

  // Implementation
}
```

### Error Handling

Return descriptive error messages:

```dart
Future<int> createUser(Session session, String email, String password) async {
  // Check if email is valid
  if (!email.contains('@')) {
    throw InvalidInputException('Invalid email format');
  }

  // Check for duplicates
  final existing = await User.find(
    session,
    where: (u) => u.email.equals(email),
  );

  if (existing.isNotEmpty) {
    throw InvalidInputException('Email already registered');
  }

  // Check password strength
  if (password.length < 8) {
    throw InvalidInputException('Password too weak (min 8 characters)');
  }

  // Create user
  final user = User(email: email, password: password);
  await user.insert(session);

  return user.id!;
}
```

## Endpoint Organization

### Group Related Methods

Keep related methods together in one endpoint:

```dart
class ProductEndpoint extends Endpoint {
  // CRUD operations
  Future<int?> create(Session session, ProductData data) async {}
  Future<ProductData?> get(Session session, int id) async {}
  Future<List<ProductData>> list(Session session) async {}
  Future<void> update(Session session, int id, ProductData data) async {}
  Future<void> delete(Session session, int id) async {}

  // Search
  Future<List<ProductData>> search(Session session, String query) async {}

  // Categories
  Future<List<ProductData>> byCategory(Session session, int categoryId) async {}
}
```

### Keep Endpoints Focused

One endpoint per domain, max 10-15 methods:

```dart
// ✓ Good - focused endpoints
UserEndpoint      // User management
ProductEndpoint   // Product catalog
OrderEndpoint     // Order processing
PaymentEndpoint   // Payment handling

// ✗ Bad - too broad
ApiEndpoint       // Everything (100+ methods)
```

## Testing Endpoints

Write tests for business logic:

```dart
// test/endpoints/user_endpoint_test.dart
import 'package:test/test.dart';
import 'package:serverpod_test_serverpod/serverpod_test_serverpod.dart';

void main() {
  group('UserEndpoint', () {
    testWithServerpod('create user', (session, endpoints) async {
      final userId = await endpoints.user.createUser(
        session,
        email: 'test@example.com',
        password: 'password123',
      );

      expect(userId, isNotNull);
      expect(userId, isPositive);
    });

    testWithServerpod('rejects duplicate email', (session, endpoints) async {
      await endpoints.user.createUser(
        session,
        email: 'test@example.com',
        password: 'password123',
      );

      expect(
        () => endpoints.user.createUser(
          session,
          email: 'test@example.com',
          password: 'password456',
        ),
        throwsA(isA<InvalidInputException>()),
      );
    });
  });
}
```

---

For information about models and database operations, see the **models** skill.
