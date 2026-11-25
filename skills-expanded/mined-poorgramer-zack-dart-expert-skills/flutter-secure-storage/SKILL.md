---
name: "managing-secure-storage"
description: "FlutterSecureStorage (v10.x) for encrypted key-value storage of sensitive data using platform-native secure enclaves with biometric authentication support. Use this skill when storing OAuth tokens (access tokens, refresh tokens, ID tokens), API keys and secrets, user passwords or PINs, session tokens, encryption keys, private keys for cryptography, certificate data, biometric enrollment data, banking credentials, health data, or any sensitive information requiring platform-level encryption (iOS Keychain with Secure Enclave, Android Keystore with Hardware-backed keys). Supports Touch ID, Face ID, and Android biometric prompt integration. Handles biometric change invalidation (resetOnError), data migration from SharedPreferences/EncryptedSharedPreferences, Google Drive backup exclusion, automatic key rotation, configurable encryption algorithms (AES), and prevents data extraction even on rooted/jailbroken devices. Essential for authentication flows, secure credential management, or compliance requirements (PCI DSS, HIPAA, GDPR data protection)."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# SecureStorage Encrypted Storage Guide (v10.x)

## Goal
Implement encrypted key-value storage for sensitive data using flutter_secure_storage. Leverages platform-native secure storage (iOS Keychain, Android Keystore) for maximum security.

## Process

### Phase 1: Install Dependencies

```yaml
dependencies:
  flutter_secure_storage: ^11.2.0  # v11: Android minSdk 24; the encryptedSharedPreferences option was removed
```

### Phase 2: Platform Configuration

**Android (android/app/build.gradle)**:
```gradle
// android/app/build.gradle (Groovy). v11 requires minSdk 24.
android {
    defaultConfig {
        minSdk 24
    }
}
```

**Android Backup Exclusion (AndroidManifest.xml)**:
```xml
<application
  android:fullBackupContent="@xml/backup_rules"
  android:allowBackup="true">
```

**Android Backup Rules (res/xml/backup_rules.xml)**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
  <!-- Exclude secure storage from Google Drive backups -->
  <exclude domain="sharedpref" path="FlutterSecureStorage.xml"/>
</full-backup-content>
```

**iOS**: No additional configuration required (uses Keychain by default).

### Phase 3: Create Secure Storage Wrapper

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorage {
  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(
      resetOnError: true, // Auto-reset on biometric change invalidation
    ),
    iOptions: IOSOptions(
      accessibility: KeychainAccessibility.first_unlock,
      accountName: AppleOptions.defaultAccountName,
    ),
  );
  
  // Access Token
  static Future<String?> getAccessToken() => _storage.read(key: _Keys.accessToken);
  static Future<void> setAccessToken(String value) => _storage.write(key: _Keys.accessToken, value: value);
  static Future<void> deleteAccessToken() => _storage.delete(key: _Keys.accessToken);
  
  // Refresh Token
  static Future<String?> getRefreshToken() => _storage.read(key: _Keys.refreshToken);
  static Future<void> setRefreshToken(String value) => _storage.write(key: _Keys.refreshToken, value: value);
  
  // API Key
  static Future<String?> getApiKey() => _storage.read(key: _Keys.apiKey);
  static Future<void> setApiKey(String value) => _storage.write(key: _Keys.apiKey, value: value);
  
  // User Credentials (for biometric unlock)
  static Future<String?> getStoredPassword() => _storage.read(key: _Keys.password);
  static Future<void> setStoredPassword(String value) => _storage.write(key: _Keys.password, value: value);
  
  // Clear all secure data (logout)
  static Future<void> clearAll() => _storage.deleteAll();
  
  // Check if key exists
  static Future<bool> hasAccessToken() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }
}

class _Keys {
  static const String accessToken = 'access_token';
  static const String refreshToken = 'refresh_token';
  static const String apiKey = 'api_key';
  static const String password = 'stored_password';
}
```

### Phase 4: Usage Examples

**Authentication Flow**:
```dart
// Login - store tokens
Future<void> login(String username, String password) async {
  final response = await authApi.login(username, password);
  await SecureStorage.setAccessToken(response.accessToken);
  await SecureStorage.setRefreshToken(response.refreshToken);
}

// Check authentication status
Future<bool> isAuthenticated() async {
  return await SecureStorage.hasAccessToken();
}

// Logout - clear tokens
Future<void> logout() async {
  await SecureStorage.clearAll();
}

// Refresh token
Future<String> refreshAccessToken() async {
  final refreshToken = await SecureStorage.getRefreshToken();
  if (refreshToken == null) throw Exception('No refresh token');
  
  final response = await authApi.refresh(refreshToken);
  await SecureStorage.setAccessToken(response.accessToken);
  return response.accessToken;
}
```

**API Client Integration**:
```dart
class ApiClient {
  Future<Response> get(String path) async {
    final token = await SecureStorage.getAccessToken();
    
    return http.get(
      Uri.parse('$baseUrl$path'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );
  }
}
```

### Phase 5: Integration with State Management

**With Riverpod**:
```dart
final authStateProvider = NotifierProvider<AuthNotifier, AuthState>(AuthNotifier.new);

class AuthNotifier extends Notifier<AuthState> {
  @override
  AuthState build() {
    _checkAuthStatus();
    return AuthState.loading();
  }
  
  Future<void> _checkAuthStatus() async {
    final hasToken = await SecureStorage.hasAccessToken();
    state = hasToken ? AuthState.authenticated() : AuthState.unauthenticated();
  }
  
  Future<void> login(String username, String password) async {
    state = AuthState.loading();
    try {
      final response = await authApi.login(username, password);
      await SecureStorage.setAccessToken(response.accessToken);
      await SecureStorage.setRefreshToken(response.refreshToken);
      state = AuthState.authenticated();
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }
  
  Future<void> logout() async {
    await SecureStorage.clearAll();
    state = AuthState.unauthenticated();
  }
}
```

---

## Production Issues & Best Practices

### Biometric Change Invalidation

**Problem:** User adds/removes fingerprint → Android Keystore keys become invalid  
**Solution:** Enable `resetOnError: true` in AndroidOptions

```dart
const storage = FlutterSecureStorage(
  aOptions: AndroidOptions(
    resetOnError: true, // Auto-reset on key invalidation
  ),
);
```

**User Communication:**
```dart
try {
  final token = await SecureStorage.getAccessToken();
} catch (e) {
  if (e.toString().contains('KeyPermanentlyInvalidatedException')) {
    // Show user-friendly message
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Security Settings Changed'),
        content: Text('Your device security settings have changed. Please log in again.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pushReplacementNamed(context, '/login'),
            child: Text('Re-login'),
          ),
        ],
      ),
    );
  }
}
```

### Data Migration Best Practice

**Android Migration Path:**
1. **Old app:** SharedPreferences/EncryptedSharedPreferences
2. **Migration v1:** Read old data, write to Keystore
3. **Migration v2+:** Keystore only

**Migration Example:**
```dart
class SecureStorageMigration {
  static Future<void> migrateFromSharedPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    
    // Migrate access token
    final oldAccessToken = prefs.getString('access_token');
    if (oldAccessToken != null) {
      await SecureStorage.setAccessToken(oldAccessToken);
      await prefs.remove('access_token');
    }
    
    // Migrate refresh token
    final oldRefreshToken = prefs.getString('refresh_token');
    if (oldRefreshToken != null) {
      await SecureStorage.setRefreshToken(oldRefreshToken);
      await prefs.remove('refresh_token');
    }
    
    // Mark migration complete
    await prefs.setBool('migrated_to_secure_storage', true);
  }
  
  static Future<bool> needsMigration() async {
    final prefs = await SharedPreferences.getInstance();
    return !(prefs.getBool('migrated_to_secure_storage') ?? false);
  }
}

// In main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  if (await SecureStorageMigration.needsMigration()) {
    await SecureStorageMigration.migrateFromSharedPreferences();
  }
  
  runApp(MyApp());
}
```

**CRITICAL:** Test upgrade from ALL previous app versions.

### Google Drive Backup Issue

**Problem:** Keystore keys don't restore from Google Drive backups → app crashes on new device  
**Solution:** Exclude FlutterSecureStorage from backups (see Phase 2 configuration)

**Verification:**
```bash
# Check if backup exclusion is working
adb shell bmgr list transports
adb shell bmgr backupnow --all
```

### iOS Keychain Best Practices

**Accessibility Options:**
```dart
const storage = FlutterSecureStorage(
  iOptions: IOSOptions(
    accessibility: KeychainAccessibility.first_unlock, // Recommended
    // Other options:
    // - unlocked: Accessible only when device unlocked
    // - first_unlock_this_device: Never migrates to new device
    // - unlocked_this_device: Most restrictive
  ),
);
```

**Common Issues:**
- ❌ Missing Keychain entitlements in Xcode → Add "Keychain Sharing" capability
- ❌ Incorrect `accessControlFlags` for biometric gating → Use `biometryAny` or `biometryCurrentSet`

**Biometric Gating Example:**
```dart
// iOS only - require biometric for read
const storage = FlutterSecureStorage(
  iOptions: IOSOptions(
    accessibility: KeychainAccessibility.unlocked,
    // Requires biometric authentication
    accessControl: AccessControlOptions(
      biometryCurrentSet: true,
      userPresence: true,
    ),
  ),
);
```

---

## Constraints

* **Never in SharedPreferences**: NEVER store sensitive data in SharedPreferences. Always use SecureStorage.
* **Async Only**: All operations are async. Cannot be accessed synchronously.
* **Platform Dependency**: Requires platform-native secure storage. May fail on emulators without proper setup.
* **No Complex Objects**: Stores strings only. Serialize complex objects to JSON first.
* **Key Management**: Use const string keys via wrapper class to prevent typos.
* **Logout Cleanup**: Always call `clearAll()` on logout to prevent token leakage.
* **Backup Exclusion**: Always exclude FlutterSecureStorage from cloud backups (Android/iOS).
* **Migration Testing**: Test app upgrades from all previous versions to catch migration issues.
* **Biometric Invalidation**: Handle `resetOnError` scenario with user-friendly re-authentication flow.
