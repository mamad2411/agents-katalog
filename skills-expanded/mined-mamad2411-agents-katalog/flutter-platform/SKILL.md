---
name: flutter-platform
description: "When to activate: Flutter platform channels, method channels, FFI, platform-specific code, plugins, MethodChannel, EventChannel, native code"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: dart
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Flutter Platform Integration Patterns

## MethodChannel (Dart → Native call)

```dart
// Dart side
class BatteryService {
  static const _channel = MethodChannel('com.example.app/battery');

  Future<int> getBatteryLevel() async {
    try {
      final level = await _channel.invokeMethod<int>('getBatteryLevel');
      return level ?? -1;
    } on PlatformException catch (e) {
      throw BatteryException('Failed: ${e.message}');
    }
  }
}

// Android (Kotlin) — MainActivity.kt
private val CHANNEL = "com.example.app/battery"

override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
  super.configureFlutterEngine(flutterEngine)
  MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
    when (call.method) {
      "getBatteryLevel" -> {
        val level = getBatteryLevel()
        if (level != -1) result.success(level) else result.error("UNAVAILABLE", "Battery unavailable", null)
      }
      else -> result.notImplemented()
    }
  }
}

// iOS (Swift) — AppDelegate.swift
let controller = window?.rootViewController as! FlutterViewController
let batteryChannel = FlutterMethodChannel(name: "com.example.app/battery",
                                          binaryMessenger: controller.binaryMessenger)
batteryChannel.setMethodCallHandler { call, result in
  guard call.method == "getBatteryLevel" else { result(FlutterMethodNotImplemented); return }
  result(UIDevice.current.batteryLevel * 100)
}
```

## EventChannel (Native → Dart stream)

```dart
// Dart side
class SensorService {
  static const _channel = EventChannel('com.example.app/sensors');

  Stream<double> get accelerometerStream =>
    _channel.receiveBroadcastStream().map((e) => e as double);
}

// Android (Kotlin)
EventChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example.app/sensors")
  .setStreamHandler(object : EventChannel.StreamHandler {
    override fun onListen(arguments: Any?, events: EventChannel.EventSink) {
      sensorManager.registerListener(/* emit via events.success(value) */)
    }
    override fun onCancel(arguments: Any?) {
      sensorManager.unregisterListener(listener)
    }
  })
```

## dart:ffi (Direct C interop)

```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

// Bind to native function
typedef NativeAdd = Int32 Function(Int32 a, Int32 b);
typedef DartAdd = int Function(int a, int b);

final dylib = DynamicLibrary.open('libnative.so'); // Android
final add = dylib.lookupFunction<NativeAdd, DartAdd>('add');

// Use
final result = add(3, 4); // 7

// Strings with FFI
final ptr = 'Hello'.toNativeUtf8();
nativeFunc(ptr);
calloc.free(ptr);
```

## Platform-Specific UI

```dart
import 'dart:io' show Platform;

Widget buildButton() {
  if (Platform.isIOS) {
    return CupertinoButton(child: const Text('OK'), onPressed: () {});
  }
  return ElevatedButton(onPressed: () {}, child: const Text('OK'));
}

// Or use Theme.of(context).platform
Widget buildSwitch(BuildContext context) =>
  Theme.of(context).platform == TargetPlatform.iOS
    ? CupertinoSwitch(value: true, onChanged: (_) {})
    : Switch(value: true, onChanged: (_) {});
```

## Plugin Architecture

```dart
// Platform interface (shared)
abstract class CameraPluginPlatform extends PlatformInterface {
  CameraPluginPlatform() : super(token: _token);
  static final _token = Object();
  static CameraPluginPlatform _instance = MethodChannelCamera();
  static CameraPluginPlatform get instance => _instance;

  Future<String?> pickImage() => throw UnimplementedError();
}

// Method channel implementation
class MethodChannelCamera extends CameraPluginPlatform {
  final _channel = const MethodChannel('camera_plugin');

  @override
  Future<String?> pickImage() => _channel.invokeMethod<String>('pickImage');
}

// Public API (federated plugin)
class CameraPlugin {
  static Future<String?> pickImage() =>
    CameraPluginPlatform.instance.pickImage();
}
```

## Checking Platform Capabilities

```dart
// Using device_info_plus
final deviceInfo = DeviceInfoPlugin();
if (Platform.isAndroid) {
  final androidInfo = await deviceInfo.androidInfo;
  if (androidInfo.version.sdkInt >= 33) { /* Android 13+ */ }
}

// Using package_info_plus
final packageInfo = await PackageInfo.fromPlatform();
print('${packageInfo.appName} v${packageInfo.version}+${packageInfo.buildNumber}');
```

## Background Isolates

```dart
// Heavy computation in background isolate
Future<List<int>> sortLargeList(List<int> data) async {
  return await Isolate.run(() {
    final copy = List<int>.from(data);
    copy.sort();
    return copy;
  });
}

// Send port for bidirectional communication
void spawnWorker() async {
  final receivePort = ReceivePort();
  await Isolate.spawn(_workerEntry, receivePort.sendPort);
  final sendPort = await receivePort.first as SendPort;
  sendPort.send({'task': 'compute', 'data': largeData});
}
