---
name: cross-platform-patterns
description: "Bridge code for Flutter MethodChannel and EventChannel, Kotlin Multiplatform expect/actual with Ktor and SQLDelight, React Native TurboModule specs, and platform detection. Use when sharing logic across iOS and Android or calling native APIs from a cross-platform app."
---

# Cross Platform Patterns

## Flutter MethodChannel

### Dart Side (caller)
```dart
import 'package:flutter/services.dart';

class BiometricService {
  static const _channel = MethodChannel('com.myapp/biometrics');

  Future<bool> authenticate(String reason) async {
    try {
      final bool result = await _channel.invokeMethod('authenticate', {
        'reason': reason,
      });
      return result;
    } on PlatformException catch (e) {
      if (e.code == 'NotAvailable') return false;
      rethrow;
    }
  }
}
```

### iOS Side (Swift)
```swift
// In AppDelegate or a FlutterPlugin
let channel = FlutterMethodChannel(
    name: "com.myapp/biometrics",
    binaryMessenger: controller.binaryMessenger
)

channel.setMethodCallHandler { call, result in
    switch call.method {
    case "authenticate":
        guard let args = call.arguments as? [String: Any],
              let reason = args["reason"] as? String else {
            result(FlutterError(code: "InvalidArgs", message: nil, details: nil))
            return
        }
        let context = LAContext()
        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, _ in
            DispatchQueue.main.async {
                result(success)
            }
        }
    default:
        result(FlutterMethodNotImplemented)
    }
}
```

### Android Side (Kotlin)
```kotlin
class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            "com.myapp/biometrics"
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "authenticate" -> {
                    val reason = call.argument<String>("reason") ?: ""
                    performBiometric(reason, result)
                }
                else -> result.notImplemented()
            }
        }
    }
}
```

---

## Flutter EventChannel (Streams from Native)

```dart
// Dart
class LocationService {
  static const _eventChannel = EventChannel('com.myapp/location');

  Stream<Map<String, double>> get locationStream {
    return _eventChannel.receiveBroadcastStream()
        .map((event) => Map<String, double>.from(event as Map));
  }
}
```

```swift
// iOS Swift
let eventChannel = FlutterEventChannel(
    name: "com.myapp/location",
    binaryMessenger: controller.binaryMessenger
)
eventChannel.setStreamHandler(LocationStreamHandler())

class LocationStreamHandler: NSObject, FlutterStreamHandler {
    var eventSink: FlutterEventSink?

    func onListen(withArguments arguments: Any?,
                  eventSink: @escaping FlutterEventSink) -> FlutterError? {
        self.eventSink = eventSink
        CLLocationManager().startUpdatingLocation()
        return nil
    }

    func onCancel(withArguments arguments: Any?) -> FlutterError? {
        eventSink = nil
        return nil
    }

    func sendLocation(_ location: CLLocation) {
        eventSink?(["lat": location.coordinate.latitude,
                    "lng": location.coordinate.longitude])
    }
}
```

---

## Kotlin Multiplatform Mobile (KMM)

### Shared expect/actual
```kotlin
// commonMain: expect declaration
expect class PlatformCrypto() {
    fun encrypt(data: ByteArray, key: ByteArray): ByteArray
    fun decrypt(data: ByteArray, key: ByteArray): ByteArray
}

// androidMain: actual implementation
actual class PlatformCrypto actual constructor() {
    actual fun encrypt(data: ByteArray, key: ByteArray): ByteArray {
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, SecretKeySpec(key, "AES"))
        return cipher.doFinal(data)
    }
    actual fun decrypt(data: ByteArray, key: ByteArray): ByteArray {
        // Android Keystore implementation
        TODO()
    }
}

// iosMain: actual implementation
actual class PlatformCrypto actual constructor() {
    actual fun encrypt(data: ByteArray, key: ByteArray): ByteArray {
        // Use CommonCrypto via cinterop
        TODO()
    }
    actual fun decrypt(data: ByteArray, key: ByteArray): ByteArray {
        TODO()
    }
}
```

### Shared Repository with Ktor + SQLDelight
```kotlin
// commonMain
class UserRepository(
    private val api: UserApi,      // Ktor HttpClient
    private val db: UserDatabase   // SQLDelight generated DB
) {
    suspend fun getUser(id: String): User {
        val cached = db.userQueries.selectById(id).executeAsOneOrNull()
        if (cached != null) return cached

        val user = api.fetchUser(id)
        db.userQueries.insert(user.id, user.name, user.email)
        return user
    }

    fun observeUser(id: String): Flow<User> =
        db.userQueries.selectById(id).asFlow().mapToOne()
}
```

---

## React Native: TurboModule (New Architecture)

### Spec File (TypeScript)
```typescript
// NativeMyModule.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  getDeviceId(): Promise<string>;
  setSecureValue(key: string, value: string): Promise<void>;
  getSecureValue(key: string): Promise<string | null>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('MyModule');
```

### Usage in React Native Component
```typescript
import NativeMyModule from './NativeMyModule';

async function storeToken(token: string) {
  try {
    await NativeMyModule.setSecureValue('auth_token', token);
  } catch (e) {
    console.error('Failed to store token:', e);
  }
}
```

---

## Platform Detection

### Flutter
```dart
import 'dart:io';
import 'package:flutter/foundation.dart';

// Simple platform check
if (Platform.isIOS) { /* iOS behavior */ }
if (Platform.isAndroid) { /* Android behavior */ }

// More precise (also works on web)
if (defaultTargetPlatform == TargetPlatform.iOS) { }

// Build widget conditionally
Widget get platformButton => Platform.isIOS
    ? CupertinoButton(onPressed: action, child: child)
    : ElevatedButton(onPressed: action, child: child);
```

### React Native
```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'ios'
      ? Platform.select({ ios: 44, default: 0 }) // Dynamic Island safe area
      : 0,
  },
});
```
