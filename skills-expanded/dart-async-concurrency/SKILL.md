---
name: dart-async-concurrency
description: 掌握 Dart 异步与并发编程（Future、async/await、Stream、Isolate），编写高性能无阻塞的应用。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T08:39:45.107950Z
---
# Mastering Dart Asynchronous Programming and Concurrency

## Contents

- [Event Loop and Microtask Queue](#event-loop-and-microtask-queue)
- [Creating and Chaining Futures](#creating-and-chaining-futures)
- [Using async/await](#using-async-await)
- [Working with Streams](#working-with-streams)
- [Transforming Streams](#transforming-streams)
- [Running Code in Isolates](#running-code-in-isolates)
- [Sequential vs Concurrent Execution](#sequential-vs-concurrent-execution)
- [Workflow: Building an Asynchronous Data Pipeline](#workflow-building-an-asynchronous-data-pipeline)
- [Examples](#examples)

## Event Loop and Microtask Queue

Dart uses a single-threaded event loop with two queues: the **event queue** and the **microtask queue**. All Dart code runs inside an isolate, each with its own event loop. The loop processes events one at a time in the order they arrive.

```dart
// Conceptual event loop
while (eventQueue.isNotEmpty) {
  eventQueue.processNextEvent();
}
```

Microtasks are scheduled via `scheduleMicrotask()` and are executed before the next event. `Future.then()`, `catchError()`, and `whenComplete()` callbacks always run as microtasks. Direct `Future()` constructor callbacks run synchronously but the completion of a future is propagated via microtask.

**Rule**: Use `scheduleMicrotask` sparingly—prefer `Future` for most asynchronous work. Use microtasks only for internal housekeeping that must run before any other event.

## Creating and Chaining Futures

### Creating Futures

```dart
Future<String>.value('Hello');          // completes immediately with value
Future<String>.error(Exception('Oh'));  // completes with error
Future.delayed(Duration(seconds: 1), () => 'Later'); // completes after delay
Future(() => computeSomething());       // runs callback asynchronously
```

### Chaining with then/catchError/whenComplete

Use `then()` to transform a future’s value, `catchError()` to handle errors, and `whenComplete()` for cleanup (like `finally`).

```dart
fetchData()
  .then((data) => parse(data))
  .catchError((e) => handleError(e), test: (e) => e is FormatException)
  .whenComplete(() => cleanUp());
```

**Error propagation**: If a `then()` callback throws, the returned future completes with that error — `catchError()` will catch it regardless of whether the error originated in the original future or in a `then()`.

**Cautious**: Register error handlers early. If you delay attaching `catchError()`, the error might become unhandled.

**Mixing sync/async errors**: Wrap function bodies with `Future.sync()` to catch synchronous errors in the future chain.

```dart
Future<int> safeParse(String data) {
  return Future.sync(() {
    // If this throws synchronously, the returned future captures it.
    return int.parse(data);
  });
}
```

## Using async/await

Mark a function with `async` to make it return a `Future<T>`. Inside, `await` pauses execution until the awaited future completes.

```dart
Future<String> fetchUserOrder() async {
  final data = await fetchData();        // Suspends here, other code can run
  return 'Order: $data';
}
```

**Error handling**: Use `try/catch` around `await` expressions.

```dart
try {
  final data = await fetchData();
} catch (e) {
  print('Failed: $e');
}
```

**Execution flow**: The function runs synchronously until the first `await`. After that, it returns an uncompleted future and resumes when the awaited value is ready.

**Linting**: Enable `discarded_futures` and `unawaited_futures` to catch mistakes.

## Working with Streams

Streams provide a sequence of asynchronous events. They can be **single-subscription** (one listener) or **broadcast** (many listeners).

### Creating Streams

- **Existing stream**: `map()`, `where()`, `take()` etc. return a new stream.
- **async* generator**: Use `yield` to emit values.

```dart
Stream<int> countStream(int max) async* {
  for (var i = 1; i <= max; i++) {
    yield i;
  }
}
```

- **StreamController**: Manually push events.

```dart
final controller = StreamController<int>();
controller.add(1);
controller.addError('something wrong');
controller.close();
final stream = controller.stream;
```

For broadcast: `StreamController<int>.broadcast()`.

**Pausing/resuming**: Use the controller’s `onListen`, `onPause`, `onResume`, `onCancel` callbacks to start/stop event production and avoid memory leaks.

### Consuming Streams

- **await for**: Process each event sequentially.

```dart
await for (final value in stream) {
  print(value);
}
```

- **listen()**: Low-level control.

```dart
stream.listen(
  (data) => print(data),
  onError: (e) => print('Error: $e'),
  onDone: () => print('Done'),
  cancelOnError: true,
);
```

## Transforming Streams

Chain transformation methods to build a data pipeline.

```dart
stream
  .where((item) => item.isValid)          // filter
  .map((item) => item.transform())        // one-to-one
  .take(10)                               // limit
  .expand((item) => [item, item+1])       // one-to-many
  .asyncExpand((id) => fetchDetails(id))  // async one-to-many
  .transform(StreamTransformer.fromHandlers( // custom transformer
    handleData: (data, sink) => sink.add(data.toUpperCase()),
  ))
  .handleError((e) => log(e))             // error filtering
  .timeout(Duration(seconds: 2));         // protect against idle streams
```

**Key methods**:
- `asyncMap`: like `map` but callback returns a `Future`.
- `distinct`: skips consecutive duplicates.
- `transform`: uses a `StreamTransformer`. Common transformers: `utf8.decoder`, `LineSplitter`.

## Running Code in Isolates

Isolates enable true parallelism. Each isolate has its own memory and communicates exclusively via message passing (`SendPort`/`ReceivePort`).

### Simple one-shot computation

Use `Isolate.run()`:

```dart
int heavyComputation(int n) => n <= 1 ? 1 : heavyComputation(n-1) + heavyComputation(n-2);

void main() async {
  final result = await Isolate.run(() => heavyComputation(40));
  print(result);
}
```

For Flutter, use `compute(heavyComputation, 40)` – it wraps `Isolate.run`.

### Long-lived isolates with message passing

- **Spawn**: `Isolate.spawn(entryPoint, initialMessage)`
- **Setup**: Main isolate creates a `ReceivePort` and sends its `sendPort` to the spawned isolate. The spawned isolate creates its own `ReceivePort` and sends its `sendPort` back.
- **Communicate**: Use `sendPort.send(message)` on either side.

See the robust ports example in the appendix for a complete, production-ready pattern including message IDs, completers, error forwarding, and port closing.

**Limitations**: Isolates do not share state. Objects containing native resources (e.g., `Socket`) cannot be sent between isolates. Use only objects that can be copied or transferred (primitives, simple objects, typed data).

## Sequential vs Concurrent Execution

### Sequential

```dart
// Fetch three URLs one after another
final result1 = await fetchUrl(url1);
final result2 = await fetchUrl(url2);
final result3 = await fetchUrl(url3);
```

### Concurrent with Future.wait

```dart
// Start all fetches at once, wait for all to complete
final results = await Future.wait([
  fetchUrl(url1),
  fetchUrl(url2),
  fetchUrl(url3),
]);
```

`Future.wait` returns a list of results in the same order as the input futures. If any future fails, the returned future completes with that error (unless `eagerError` is set to false).

### Stream concurrency

Streams are inherently sequential. To process events concurrently, use a `StreamController` and fire off asynchronous tasks per event, then emit results when they complete:

```dart
Stream<Result> concurrentMap<T, Result>(
  Stream<T> source, Future<Result> Function(T) mapper,
) {
  final controller = StreamController<Result>();
  var pending = 0;
  controller.onListen = () {
    final subscription = source.listen((event) {
      pending++;
      mapper(event).then((result) {
        controller.add(result);
        pending--;
        if (pending == 0 && subscription.isPaused) controller.close();
      });
    }, onDone: () {
      // Wait for all pending operations
    });
  };
  return controller.stream;
}
```

General rule: Use `Future.wait` when you have a fixed set of independent futures. Use a stream with controlled concurrency when the number of tasks is large or unbounded.

---

## Workflow: Building an Asynchronous Data Pipeline

### Task Progress

- [ ] **1. Define requirements** — Identify the data sources (APIs, files) and desired output.
- [ ] **2. Set up project** — Create a Dart console app or Flutter widget.
- [ ] **3. Implement individual data fetching** using `async/await` and error handling.
- [ ] **4. Add concurrent requests** using `Future.wait` where appropriate.
- [ ] **5. Introduce Stream-based file processing** if large files are involved.
- [ ] **6. Apply stream transformations** for filtering, mapping, and error recovery.
- [ ] **7. Offload heavy parsing/decoding** to an isolate using `Isolate.run` or `compute`.
- [ ] **8. Combine results** and produce final output.
- [ ] **9. Write unit tests** — mock HTTP/file I/O, verify error paths.
- [ ] **10. Run tests → Review output → Fix failures → Re-run**

### Conditional Logic

- **If the task is a single HTTP request** → Use `await` with `try/catch`.
- **If multiple independent requests** → Use `Future.wait`.
- **If the data source is a continuous stream (e.g., WebSocket)** → Use a `Stream` listener or `await for`.
- **If data needs massaging** → Add `.map()`, `.where()`, `.transform()`.
- **If a computation takes > 16ms (UI frame budget)** → Use `Isolate.run` (or `compute` in Flutter).
- **If you need ongoing communication with a worker** → Set up `ReceivePort`/`SendPort` via `Isolate.spawn`.

### Feedback Loop

1. Write code according to the selected pattern.
2. Run `dart analyze` to catch static issues.
3. Execute tests or the main entry point.
4. Inspect console output for unhandled errors or wrong order.
5. Add logging (`print`, `debugPrint`) to trace async execution.
6. Use `unawaited_futures` lint to catch missing `await`.
7. Profile with Dart DevTools if UI jank persists.
8. Iterate until the pipeline meets latency and correctness goals.

---

## Examples

### 1. Future with Chain and Error Handling

```dart
import 'dart:async';

Future<String> fetchUser(String id) =>
    Future.delayed(Duration(seconds: 1), () => 'User $id');

void main() {
  fetchUser('1')
      .then((user) => print(user))
      .catchError((e) => print('Error: $e'))
      .whenComplete(() => print('Done'));
}
```

### 2. async/await with try/catch

```dart
Future<void> main() async {
  try {
    final user = await fetchUser('2');
    print(user);
  } catch (e) {
    print('Caught: $e');
  }
}
```

### 3. Stream with Transformer Pipeline

```dart
import 'dart:async';

Stream<String> uppercaseLines(Stream<String> source) {
  return source
      .transform(const LineSplitter())
      .map((line) => line.toUpperCase())
      .where((line) => line.isNotEmpty)
      .handleError((e) => print('Error: $e'));
}
```

### 4. Isolate for JSON Parsing

```dart
import 'dart:convert';
import 'dart:isolate';

Future<Map<String, dynamic>> parseJsonInIsolate(String jsonString) =>
    Isolate.run(() => jsonDecode(jsonString) as Map<String, dynamic>);

void main() async {
  final result = await parseJsonInIsolate('{"key": "value"}');
  print(result);
}
```

### 5. Sequential vs Concurrent Fetch

```dart
// Sequential
final page1 = await fetchPage(url1);
final page2 = await fetchPage(url2);

// Concurrent
final pages = await Future.wait([fetchPage(url1), fetchPage(url2)]);
```

### 6. Robust Long-Lived Isolate (Abbreviated)

<details>
<summary>Expand to see a robust worker isolate pattern</summary>

```dart
import 'dart:async';
import 'dart:convert';
import 'dart:isolate';

class Worker {
  final SendPort _commands;
  final ReceivePort _responses;
  final Map<int, Completer<Object?>> _activeRequests = {};
  int _idCounter = 0;
  bool _closed = false;

  Future<Object?> parseJson(String message) async {
    if (_closed) throw StateError('Closed');
    final completer = Completer<Object?>.sync();
    final id = _idCounter++;
    _activeRequests[id] = completer;
    _commands.send((id, message));
    return await completer.future;
  }

  static Future<Worker> spawn() async {
    final initPort = RawReceivePort();
    final connection = Completer<(ReceivePort, SendPort)>.sync();
    initPort.handler = (initialMessage) {
      final commandPort = initialMessage as SendPort;
      connection.complete((
        ReceivePort.fromRawReceivePort(initPort),
        commandPort,
      ));
    };
    try {
      await Isolate.spawn(_startRemoteIsolate, (initPort.sendPort));
    } on Object {
      initPort.close();
      rethrow;
    }
    final (ReceivePort receivePort, SendPort sendPort) =
        await connection.future;
    return Worker._(receivePort, sendPort);
  }

  Worker._(this._responses, this._commands) {
    _responses.listen(_handleResponsesFromIsolate);
  }

  void _handleResponsesFromIsolate(dynamic message) {
    final (int id, Object? response) = message as (int, Object?);
    final completer = _activeRequests.remove(id)!;
    if (response is RemoteError) {
      completer.completeError(response);
    } else {
      completer.complete(response);
    }
    if (_closed && _activeRequests.isEmpty) _responses.close();
  }

  static void _startRemoteIsolate(SendPort sendPort) {
    final receivePort = ReceivePort();
    sendPort.send(receivePort.sendPort);
    _handleCommandsToIsolate(receivePort, sendPort);
  }

  static void _handleCommandsToIsolate(
    ReceivePort receivePort,
    SendPort sendPort,
  ) {
    receivePort.listen((message) {
      if (message == 'shutdown') {
        receivePort.close();
        return;
      }
      final (int id, String jsonText) = message as (int, String);
      try {
        final jsonData = jsonDecode(jsonText);
        sendPort.send((id, jsonData));
      } catch (e) {
        sendPort.send((id, RemoteError(e.toString(), '')));
      }
    });
  }

  void close() {
    if (!_closed) {
      _closed = true;
      _commands.send('shutdown');
      if (_activeRequests.isEmpty) _responses.close();
    }
  }
}
```

</details>
