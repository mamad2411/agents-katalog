---
alwaysApply: true
---

# Logging Rules for Bible Study Finder Frontend

## Overview
All logging in the frontend MUST use the custom logger from `/lib/utils/logger.dart`. This ensures consistent, structured, and colored logging across the entire Flutter application.

## Core Principles

### 1. Logger Instantiation
- **ALWAYS** instantiate the logger as a static final field in classes that need logging
- **ALWAYS** use `getLogger('ClassName')` to get a logger instance
- **ALWAYS** store the logger as `static final _logger = getLogger('ClassName')`
- **ALWAYS** log successful initialization with `info` level (if applicable)

**Example:**
```dart
import '../../utils/logger.dart';

class MyService {
  static final _logger = getLogger('MyService');
  
  static Future<void> initialize() async {
    _logger.info('MyService initialized successfully');
  }
}
```

### 2. Log Levels and Usage

#### DEBUG Level
- **ALWAYS** use at the **start** of functions/methods to log:
  - Function name
  - Input parameters and their values (when safe to log)
  - Entry point information
- **ALWAYS** use at the **end** of functions/methods to log:
  - Function completion
  - Return values (when safe to log, excluding sensitive data)
- **ALWAYS** use in areas where errors could occur (before risky operations)
- **ALWAYS** include parameter values when logging function entries

**Example:**
```dart
static Future<bool> createUser(String firstName, String email, String password) async {
  _logger.debug('createUser called with firstName=$firstName, email=$email');
  
  try {
    // Risky operation - log before
    _logger.debug('Checking if user already exists');
    final existingUser = await _checkUserExists(email);
    
    if (existingUser != null) {
      _logger.warning('User with email $email already exists');
      return false;
    }
    
    // Create user
    final userId = await _createUserInDatabase(firstName, email, password);
    
    _logger.debug('createUser completed successfully, userId=$userId');
    return true;
    
  } catch (e, stackTrace) {
    _logger.error('Error in createUser: $e', error: e, stackTrace: stackTrace);
    return false;
  }
}
```

#### INFO Level
- **ALWAYS** use for general information and successful operations:
  - Successful initialization messages
  - Successful completion of business operations
  - Important state changes
  - General flow information (e.g., "Processing request", "Finishing function call")
- **ALWAYS** use when logging successful API operations
- **ALWAYS** use for successful API calls (via `logApiCall` helper)

**Example:**
```dart
_logger.info('UserService initialized successfully');
_logger.info('User created successfully: $userId');
_logger.info('Finishing createUser function call');
```

#### WARNING Level
- **ALWAYS** use for unexpected results that are NOT errors:
  - Validation failures
  - Not found scenarios (when expected)
  - Business logic warnings
  - Deprecated feature usage
  - Retry attempts
  - Non-critical failures

**Example:**
```dart
if (userData == null) {
  _logger.warning('User not found with email: $email');
  return false;
}

if (result.isEmpty) {
  _logger.warning('No groups found for user: $userId');
  return [];
}
```

#### ERROR Level
- **ALWAYS** use in `catch` blocks to log exceptions
- **ALWAYS** include the exception message
- **ALWAYS** use `error: e, stackTrace: stackTrace` for full stack traces in error logs
- **ALWAYS** log errors before returning error responses

**Example:**
```dart
try {
  final result = await _apiCall();
  return result;
} catch (e, stackTrace) {
  _logger.error('Error creating user: $e', error: e, stackTrace: stackTrace);
  return false;
}
```

#### CRITICAL Level
- **ONLY** use for system-critical failures:
  - API connection failures
  - Application initialization failures
  - Security breaches
  - Data corruption issues

**Example:**
```dart
if (apiBaseUrl == null || apiBaseUrl.isEmpty) {
  _logger.critical('API base URL not configured - application cannot continue');
  throw StateError('API base URL not configured');
}
```

### 3. Function Logging Pattern

**ALWAYS** follow this pattern for all functions:

```dart
static Future<bool> myFunction(String param1, int param2) async {
  // 1. DEBUG: Log function entry with parameters
  _logger.debug('myFunction called with param1=$param1, param2=$param2');
  
  try {
    // 2. DEBUG: Log before risky operations
    _logger.debug('Performing risky operation X');
    
    // 3. Perform operation
    final result = await _someOperation(param1, param2);
    
    // 4. INFO: Log successful completion
    _logger.info('Operation completed successfully: $result');
    
    // 5. DEBUG: Log function exit with return value (if safe)
    _logger.debug('myFunction completed, returning success=true');
    return true;
    
  } on SpecificException catch (e, stackTrace) {
    // 6. WARNING: Log expected exceptions
    _logger.warning('Expected error in myFunction: $e');
    return false;
    
  } catch (e, stackTrace) {
    // 7. ERROR: Log unexpected exceptions
    _logger.error('Unexpected error in myFunction: $e', error: e, stackTrace: stackTrace);
    return false;
  }
}
```

### 4. API Operations Logging

- **ALWAYS** log API operations:
  - Before making API calls (DEBUG)
  - After successful operations (INFO via `logApiCall`)
  - On failures (ERROR via `logApiCall`)
- **ALWAYS** include relevant IDs and operation details
- **ALWAYS** use the `logApiCall` helper method for structured API logging

**Example:**
```dart
static Future<List<Group>> getGroups() async {
  _logger.debug('getGroups called');
  
  try {
    final stopwatch = Stopwatch()..start();
    final url = _buildGetGroupsUrl();
    
    _logger.debug('Making API call: GET $url');
    final response = await http.get(url, headers: headers);
    stopwatch.stop();
    
    _logger.logApiCall(
      method: 'GET',
      url: url.toString(),
      statusCode: response.statusCode,
      responseTime: stopwatch.elapsedMilliseconds / 1000.0,
    );
    
    if (response.statusCode == 200) {
      final groups = _parseGroups(response.body);
      _logger.info('Successfully loaded ${groups.length} groups');
      return groups;
    } else {
      _logger.error('API returned status code: ${response.statusCode}');
      return [];
    }
    
  } catch (e, stackTrace) {
    _logger.logApiCall(
      method: 'GET',
      url: url.toString(),
      error: e.toString(),
    );
    _logger.error('Error fetching groups', error: e, stackTrace: stackTrace);
    rethrow;
  }
}
```

### 5. API Call Logging

- **ALWAYS** log API calls using the `logApiCall` helper method
- **ALWAYS** include method, URL, status code, response time, and errors
- **ALWAYS** log before making API calls (DEBUG)
- **ALWAYS** log after receiving responses (INFO for success, ERROR for failures)

**Example:**
```dart
_logger.debug('Making API call: GET $url');
try {
  final stopwatch = Stopwatch()..start();
  final response = await http.get(url, headers: headers);
  stopwatch.stop();
  
  _logger.logApiCall(
    method: 'GET',
    url: url.toString(),
    statusCode: response.statusCode,
    responseTime: stopwatch.elapsedMilliseconds / 1000.0,
  );
} catch (e, stackTrace) {
  _logger.logApiCall(
    method: 'GET',
    url: url.toString(),
    error: e.toString(),
  );
  _logger.error('API call failed', error: e, stackTrace: stackTrace);
}
```

### 6. Security and Sensitive Data

- **NEVER** log passwords, tokens, or other sensitive information
- **NEVER** log full credit card numbers or SSNs
- **ALWAYS** mask sensitive data (e.g., `password=***`, `token=***`)
- **ALWAYS** log security events using `logSecurityEvent` helper

**Example:**
```dart
// BAD
_logger.debug('User login: email=$email, password=$password');

// GOOD
_logger.debug('User login attempt: email=$email');

// For security events
_logger.logSecurityEvent(
  eventType: 'LOGIN_ATTEMPT',
  userId: userId,
  details: 'Failed login attempt',
);
```

### 7. Performance Logging

- **ALWAYS** log performance metrics for slow operations (>1 second)
- **ALWAYS** use the `logPerformance` helper for performance tracking
- **ALWAYS** log API response times
- **ALWAYS** log expensive UI operations

**Example:**
```dart
final stopwatch = Stopwatch()..start();
final result = await _complexOperation();
stopwatch.stop();

if (stopwatch.elapsedMilliseconds > 1000) {
  _logger.logPerformance(
    operation: 'complexOperation',
    duration: stopwatch.elapsedMilliseconds / 1000.0,
  );
}
```

### 8. Error Context

- **ALWAYS** provide context in error messages
- **ALWAYS** include relevant IDs, parameters, or state information
- **ALWAYS** use descriptive error messages
- **ALWAYS** log the full exception with `error: e, stackTrace: stackTrace` in error handlers

**Example:**
```dart
// BAD
_logger.error('Error occurred');

// GOOD
_logger.error('Error creating group with name=$name, leaderId=$leaderId: $e', 
    error: e, stackTrace: stackTrace);
```

### 9. Conditional Logging

- **ALWAYS** check conditions before logging to avoid unnecessary log noise
- **ALWAYS** use appropriate log levels to filter noise in production
- **ALWAYS** log important state changes even if they're expected

**Example:**
```dart
if (result.isNotEmpty) {
  _logger.info('Removed ${result.length} group role(s)');
} else {
  _logger.warning('No group roles found to remove');
}
```

### 10. Logging in Services

- **ALWAYS** log service entry points (DEBUG)
- **ALWAYS** log request parameters (DEBUG, excluding sensitive data)
- **ALWAYS** log response preparation (INFO)
- **ALWAYS** log service errors (ERROR)

**Example:**
```dart
class UserService {
  static final _logger = getLogger('UserService');
  
  static Future<bool> createUser(String email, String password) async {
    _logger.debug('createUser called with email=$email');
    
    try {
      final success = await UserApi.createUserApi(email, password);
      
      _logger.info('User creation completed: success=$success');
      return success;
      
    } catch (e, stackTrace) {
      _logger.error('Error in createUser: $e', error: e, stackTrace: stackTrace);
      return false;
    }
  }
}
```

### 11. Logging in API Layer

- **ALWAYS** log API operations
- **ALWAYS** log validation steps
- **ALWAYS** log data transformations
- **ALWAYS** use INFO for successful API operations
- **ALWAYS** use `logApiCall` for structured API logging

**Example:**
```dart
class GroupApi {
  static final _logger = getLogger('GroupApi');
  
  static Future<List<Group>> getGroupsApi() async {
    _logger.debug('getGroupsApi called');
    
    try {
      final stopwatch = Stopwatch()..start();
      final url = _buildGetGroupsUrl();
      final headers = await AuthStorage.getAuthHeaders();
      
      _logger.debug('Fetching groups from: $url');
      final response = await http.get(url, headers: headers);
      stopwatch.stop();
      
      _logger.logApiCall(
        method: 'GET',
        url: url.toString(),
        statusCode: response.statusCode,
        responseTime: stopwatch.elapsedMilliseconds / 1000.0,
      );
      
      return _handleGetGroupsResponse(response);
      
    } catch (e, stackTrace) {
      _logger.logApiCall(
        method: 'GET',
        url: url.toString(),
        error: e.toString(),
      );
      _logger.error('Error fetching groups', error: e, stackTrace: stackTrace);
      rethrow;
    }
  }
}
```

### 12. Logging in Pages/Widgets

- **ALWAYS** log important user interactions (DEBUG)
- **ALWAYS** log navigation events (DEBUG)
- **ALWAYS** log state changes (DEBUG)
- **ALWAYS** log errors in error handlers (ERROR)
- **ALWAYS** use `debugPrint` for UI-specific debugging (in addition to logger)

**Example:**
```dart
class MyGroupsPage extends StatefulWidget {
  @override
  State<MyGroupsPage> createState() => _MyGroupsPageState();
}

class _MyGroupsPageState extends State<MyGroupsPage> {
  static final _logger = getLogger('MyGroupsPage');
  
  @override
  void initState() {
    super.initState();
    _logger.debug('MyGroupsPage initialized');
    _loadGroups();
  }
  
  Future<void> _loadGroups() async {
    _logger.debug('Loading groups');
    try {
      final groups = await GroupService.getMyGroups();
      setState(() => _groups = groups);
      _logger.info('Loaded ${groups.length} groups');
    } catch (e, stackTrace) {
      _logger.error('Error loading groups', error: e, stackTrace: stackTrace);
    }
  }
  
  Future<void> _joinGroup(String groupId) async {
    _logger.debug('User joining group: $groupId');
    try {
      final success = await MembershipService.joinGroup(groupId);
      if (success) {
        _logger.info('Successfully joined group: $groupId');
      } else {
        _logger.warning('Failed to join group: $groupId');
      }
    } catch (e, stackTrace) {
      _logger.error('Error joining group: $groupId', error: e, stackTrace: stackTrace);
    }
  }
}
```

### 13. Logging in Utilities

- **ALWAYS** log utility function operations (DEBUG)
- **ALWAYS** log cache operations (DEBUG)
- **ALWAYS** log configuration loading (INFO)
- **ALWAYS** log errors in utilities (ERROR)

**Example:**
```dart
class Permissions {
  static final _logger = getLogger('Permissions');
  
  static Future<bool> hasPermission(String groupId, String permissionAction) async {
    _logger.debug('Checking permission: groupId=$groupId, action=$permissionAction');
    
    try {
      final userRoles = await _getUserRolesForGroup(groupId);
      _logger.debug('User roles for group $groupId: ${userRoles.map((r) => r.role).toList()}');
      
      // ... permission checking logic ...
      
      _logger.debug('Permission check result: $result');
      return result;
      
    } catch (e, stackTrace) {
      _logger.error('Error checking permission', error: e, stackTrace: stackTrace);
      return false;
    }
  }
}
```

## Summary Checklist

When writing code, ensure you:

- [ ] Import `getLogger` from `../../utils/logger.dart` (adjust path as needed)
- [ ] Instantiate logger as `static final _logger = getLogger('ClassName')`
- [ ] Log initialization success with `info` (if applicable)
- [ ] Add `debug` log at function start with parameters
- [ ] Add `debug` logs before risky operations
- [ ] Add `info` logs for successful operations
- [ ] Add `warning` logs for unexpected but non-error results
- [ ] Add `error` logs in all `catch` blocks with `error: e, stackTrace: stackTrace`
- [ ] Add `debug` log at function end (when appropriate)
- [ ] Never log sensitive data (passwords, tokens, etc.)
- [ ] Include context in error messages (IDs, parameters)
- [ ] Use helper methods for structured logging (`logApiCall`, `logPerformance`, etc.)
- [ ] Use `logApiCall` for all API operations

## Best Practices

1. **Be Descriptive**: Use clear, descriptive log messages that explain what happened
2. **Include Context**: Always include relevant IDs, parameters, or state information
3. **Use Appropriate Levels**: Don't use ERROR for warnings, don't use DEBUG for important info
4. **Log at Boundaries**: Log at service boundaries, API boundaries, and page boundaries
5. **Avoid Log Spam**: Don't log in tight loops or high-frequency operations without throttling
6. **Structured Logging**: Use the helper methods for structured logging when available
7. **Consistent Format**: Follow the established patterns for consistency
8. **Production Ready**: Ensure logs are useful in production debugging scenarios
9. **Flutter Specific**: Use `debugPrint` for UI-specific debugging in addition to logger
10. **Async Operations**: Always log async operations with proper error handling
