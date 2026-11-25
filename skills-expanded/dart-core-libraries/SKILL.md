---
name: dart-core-libraries
description: 熟练使用 Dart SDK 核心库（dart:core、dart:convert、dart:io、dart:math），避免重复造轮子。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T08:32:38.882053Z
---
# Working with Dart Core Libraries

## Contents
- [SDK Libraries](#sdk-libraries)
- [Working with `dart:core`](#working-with-dartcore)
- [Working with `dart:convert`](#working-with-dartconvert)
- [Working with `dart:io`](#working-with-dartio)
- [Working with `dart:math`](#working-with-dartmath)
- [Workflow: Building a Data Processing Pipeline](#workflow-building-a-data-processing-pipeline)
- [Examples](#examples)

Leverage Dart's built-in SDK libraries to perform common tasks: file I/O, JSON serialization, mathematical computations, string and URI manipulation. This skill covers `dart:core`, `dart:convert`, `dart:io`, and `dart:math`—with an end-to-end workflow that reads a JSON configuration file, applies math operations, and writes a result file.

## SDK Libraries

| Library | Role |
|---------|------|
| `dart:core` | Foundation: types, errors, collections, `DateTime`, `String`, `Uri`, `RegExp`. Auto-imported. |
| `dart:async` | Asynchronous programming: `Future`, `Stream`, `Zone`, `Timer`. |
| `dart:convert` | Encoders/decoders for JSON, UTF‑8, Base64, ASCII, Latin‑1. |
| `dart:io` | File, directory, process, socket, HTTP (native platforms only). |
| `dart:math` | Constants (`pi`, `e`), trig functions (`sin`, `cos`, `sqrt`), min/max, `Random`, geometry (`Point`, `Rectangle`). |

*Omitted: `dart:collection`, `dart:typed_data`, `dart:developer`, `dart:ffi`, `dart:isolate`, `dart:mirrors`, and web-specific libraries.*

---

## Working with `dart:core`

### String and RegExp operations
```dart
final phrase = 'Never odd or even';

// Searching
phrase.contains('odd');               // true
phrase.startsWith('Never');          // true
phrase.endsWith('even');             // true
phrase.indexOf('odd');               // 6

// Extraction
phrase.substring(6, 9);              // 'odd'
phrase.split(' ');                   // ['Never','odd','or','even']
phrase[0];                           // 'N'
phrase.codeUnits;                    // list of UTF‑16 code units

// Transformation
phrase.toUpperCase();                // 'NEVER ODD OR EVEN'
'  hello  '.trim();                  // 'hello'

// Building strings
final sb = StringBuffer()
  ..write('Dart ')
  ..writeAll(['is', 'fun'], ' ');
sb.toString();                       // 'Dart is fun'
```

For Unicode grapheme clusters prefer package `characters`.

**Regular expressions** – use `RegExp`:
```dart
final digits = RegExp(r'\d+');
'15 cats'.contains(digits);          // true
digits.hasMatch('abc');              // false
digits.allMatches('a1 b2')           // Iterable of Match objects
  .forEach((m) => print(m.group(0))); // prints '1', '2'

// Replacement
'I have 2 dogs'.replaceAll(digits, '*'); // 'I have * dogs'
```

### DateTime and Duration
```dart
final now = DateTime.now();
final y2k  = DateTime(2000);                         // Jan 1, 2000
final y2k2 = DateTime.utc(2000, 1, 2);               // Jan 2, 2000 UTC
final parsed = DateTime.parse('2000-01-01T00:00:00Z');
final copied = now.copyWith(year: now.year - 1);

// Milliseconds since Unix epoch
y2k.millisecondsSinceEpoch;           // 946684800000

// Arithmetic via Duration
final y2001 = y2k.add(const Duration(days: 366));
final dec2000 = y2001.subtract(const Duration(days: 30));
final diff = y2001.difference(y2k);  // Duration: 366 days
print(diff.inHours);                 // 8784
```
*Day‑based shifting may fail around DST transitions—prefer UTC for such calculations.*

### URI parsing and building
```dart
// Encoding full URIs vs. components
final uri = 'https://example.org/api?foo=some message';
Uri.encodeFull(uri);        // 'https://example.org/api?foo=some%20message'
Uri.encodeComponent(uri);   // 'https%3A%2F%2Fexample.org%2Fapi%3Ffoo%3Dsome%20message'

// Parsing
final parsed = Uri.parse('https://example.org:8080/foo/bar#frag');
parsed.scheme;   // 'https'
parsed.host;     // 'example.org'
parsed.path;     // '/foo/bar'
parsed.fragment; // 'frag'

// Building
final built = Uri(
  scheme: 'https',
  host: 'example.org', path: '/foo/bar',
  fragment: 'frag',
  queryParameters: {'lang': 'dart'},
);
print(built.toString()); // https://example.org/foo/bar?lang=dart#frag

// Shortcuts for http/https
final httpUri = Uri.http('example.org', '/foo/bar', {'lang': 'dart'});
final httpsUri = Uri.https('example.org', '/foo/bar', {'lang': 'dart'});
```

---

## Working with `dart:convert`

### JSON encoding/decoding
```dart
import 'dart:convert';

final jsonStr = '''[{"score": 40}, {"score": 80}]''';
final List<dynamic> scores = jsonDecode(jsonStr);
scores[0]['score']; // 40

final encoded = jsonEncode([
  {'score': 40},
  {'score': 80, 'overtime': true, 'guest': null},
]);
// '[{"score":40},{"score":80,"overtime":true,"guest":null}]'
```
Only `int`, `double`, `String`, `bool`, `null`, `List`, and `Map<String, …>` are directly encodable. Other objects must provide a `toJson()` method or you pass a custom replacer function to `jsonEncode`.

### UTF‑8 and Base64 conversion
```dart
// UTF‑8
final bytes = utf8.encode('hello');
final decoded = utf8.decode(bytes);  // 'hello'

// Stream of bytes to strings
Stream<List<int>> inputStream = ...;
inputStream
  .transform(utf8.decoder)
  .transform(const LineSplitter())
  .forEach(print);

// Base64
final base64 = base64Encode(utf8.encode('Dart'));
print(base64);                             // RGFydA==
final decodedBytes = base64Decode(base64);
print(utf8.decode(decodedBytes));          // Dart
```

---

## Working with `dart:io`

Import `dart:io` (native‑only). Most I/O operations return `Future` or `Stream`.

### Reading files
```dart
final file = File('config.json');

// Whole text or lines
final content = await file.readAsString();
final lines   = await file.readAsLines();

// Raw bytes
final bytes = await file.readAsBytes();

// Streaming (memory‑efficient for large files)
final stream = file.openRead()
  .transform(utf8.decoder)
  .transform(const LineSplitter());
await for (final line in stream) {
  print(line);
}
```

### Writing files
```dart
final sink = file.openWrite();       // overwrite mode (FileMode.write)
sink.write('${DateTime.now()}: done\n');
await sink.flush();
await sink.close();

// Append mode
final appendSink = file.openWrite(mode: FileMode.append);
```
Binary data: use `sink.add(List<int> data)`.

### Directory operations
```dart
final dir = Directory('data');
await dir.create(recursive: true);

// List contents
await for (final entity in dir.list()) {
  if (entity is File) {
    print('File: ${entity.path}');
  } else if (entity is Directory) {
    print('Dir:  ${entity.path}');
  }
}
// Delete recursively
await dir.delete(recursive: true);
```
Use `File` and `Directory` constructors for path handling: `File('$dirPath/$fileName')` or `File(path.join(dirPath, fileName))` with package `path`.

---

## Working with `dart:math`

### Random numbers and booleans
```dart
final rng = Random();
rng.nextDouble();          // [0.0, 1.0)
rng.nextInt(100);          // [0, 99]
rng.nextBool();            // true or false

// Repeatable seed
final seeded = Random(42);

// Cryptographically secure
final secureRng = Random.secure();
```

### Constants and trigonometric functions
```dart
import 'dart:math';

print(pi);                 // 3.141592653589793
print(e);                  // 2.718281828459045

final radians = 30 * (pi / 180);  // degrees → radians
sin(radians);              // ~0.5
cos(pi);                   // -1.0
sqrt(16);                  // 4.0

max(1, 1000);              // 1000
min(1, -1000);             // -1000
```

### Geometry (Point and Rectangle)
```dart
final p1 = Point(1, 2);
final p2 = Point(3, 4);
final rect = Rectangle(p1, p2);
print(rect.width);   // 2
print(rect.top);     // 2
```

---

## Workflow: Building a Data Processing Pipeline

Create (or edit) a Dart script that **reads a JSON configuration file, extracts numbers, performs a math operation, and writes the result**.

### Task Progress
- [ ] Determine if this is a new project or an existing one.
- [ ] Set up imports and async entry point.
- [ ] Read and parse the JSON configuration file.
- [ ] Validate configuration structure.
- [ ] Apply the requested mathematical operation.
- [ ] Write results as JSON to the output file.
- [ ] Run the script and inspect output.
- [ ] Add error handling and edge‑case handling.
- [ ] Re‑run until all cases pass.

### Step Details

#### 1. Project setup
- **NEW project:** `dart create -t console config_processor && cd config_processor`
- **EXISTING project:** Navigate to the project root.
- Open `bin/config_processor.dart` (or create a new Dart file).
- Ensure the entry point uses `async` main:
  ```dart
  Future<void> main() async {
    // pipeline here
  }
  ```

#### 2. Read and parse JSON
Use `dart:io` to read the file and `dart:convert` to decode.
```dart
import 'dart:convert';
import 'dart:io';

final configFile = File('config.json');
if (!await configFile.exists()) {
  // Condition: file missing → create a default config or fail gracefully
  print('Error: config.json not found');
  return;
}
final rawJson = await configFile.readAsString();
late Map<String, dynamic> config;
try {
  config = jsonDecode(rawJson) as Map<String, dynamic>;
} on FormatException {
  print('Invalid JSON format');
  return;
}
```

#### 3. Validate configuration
Expect a structure like:
```json
{
  "numbers": [2, 3, 5, 7],
  "operation": "sqrt",
  "output_file": "result.json"
}
```
Validation code:
```dart
if (!config.containsKey('numbers') || config['numbers'] is! List) {
  print('Config must contain a "numbers" list.');
  return;
}
final numbers = config['numbers'].cast<num>();
final operation = config['operation'] as String? ?? 'sqrt';
final outputFile = File(config['output_file'] as String? ?? 'result.json');
```

#### 4. Perform mathematical computation
Branch on `operation`:
```dart
import 'dart:math';

List<num> results;
switch (operation) {
  case 'sqrt':
    results = numbers.map((n) => sqrt(n.toDouble())).toList();
    break;
  case 'square':
    results = numbers.map((n) => n * n).toList();
    break;
  case 'random_int':
    // For demonstration: map each number to a random int up to that number
    final rng = Random();
    results = numbers.map((n) => rng.nextInt(n.toInt())).toList();
    break;
  default:
    print('Unknown operation "$operation". Valid: sqrt, square, random_int');
    return;
}
```

#### 5. Write results
```dart
final result = {
  'input': numbers,
  'operation': operation,
  'results': results,
};
final resultJson = jsonEncode(result);
await outputFile.writeAsString(resultJson);
print('Results written to ${outputFile.path}');
```

#### 6. Test with sample config
Create `config.json`:
```json
{"numbers": [4, 9, 16], "operation": "sqrt", "output_file": "result.json"}
```
Run `dart run`. Verify `result.json` contains `{"input":[4,9,16],"operation":"sqrt","results":[2.0,3.0,4.0]}`.

#### 7. Error handling and feedback loop
Wrap the entire pipeline in a `try`‑`catch` to handle I/O errors:
```dart
try {
  // entire process
} on FileSystemException catch (e) {
  print('File error: $e');
} catch (e) {
  print('Unexpected error: $e');
}
```
After each change: **Run → Inspect → Fix → Re‑run** until:
- Missing file prints a clear message.
- Invalid JSON reports `Invalid JSON format`.
- Unknown operation tells the user which operations are valid.
- Successful run produces the correct output file.

#### 8. Conditional Logic Patterns

Use conditional branching to handle different scenarios. Dart supports `if`‑`else` chains, `switch` statements, and null‑aware operators for concise control flow:

```dart
// If‑else chain for operation selection
if (operation == 'sqrt') {
  results = numbers.map((n) => sqrt(n.toDouble())).toList();
} else if (operation == 'square') {
  results = numbers.map((n) => n * n).toList();
} else if (operation == 'random_int') {
  final rng = Random();
  results = numbers.map((n) => rng.nextInt(n.toInt())).toList();
} else {
  print('Unknown operation "$operation". Valid: sqrt, square, random_int');
  return;
}
```

**Ternary operator** for concise inline conditionals:
```dart
final outputPath = config.containsKey('output_file')
    ? config['output_file'] as String
    : 'result.json';
```

**Null‑aware operators** (`??`, `??=`, `?.`) avoid explicit null checks:
```dart
final path = config['output_file'] as String? ?? 'result.json';   // 如果为 null 则使用默认值
final name = config['name']?.toUpperCase();                        // 如果为 null 则短路返回 null
config['counter'] ??= 0;                                           // 如果为 null 则赋值
```

### Feedback Loop
1. Execute `dart run`.
2. Examine the console output and the output file.
3. If an error occurs, identify the step and correct the code.
4. Re‑run. Repeat until all happy and error paths work as expected.

---

## Examples

`bin/config_processor.dart`:
```dart
import 'dart:convert';
import 'dart:io';
import 'dart:math';

Future<void> main() async {
  const configPath = 'config.json';

  // 1. Read file
  final configFile = File(configPath);
  if (!await configFile.exists()) {
    _fail('$configPath not found');
  }
  String rawJson;
  try {
    rawJson = await configFile.readAsString();
  } on FileSystemException {
    _fail('Cannot read $configPath');
    return;
  }

  // 2. Parse JSON
  Map<String, dynamic> config;
  try {
    config = jsonDecode(rawJson) as Map<String, dynamic>;
  } on FormatException {
    _fail('Invalid JSON');
    return;
  }

  // 3. Validate
  if (!config.containsKey('numbers') || config['numbers'] is! List) {
    _fail('"numbers" list required');
  }
  final numbers = (config['numbers'] as List)
      .map((e) => e is num ? e : num.parse(e.toString()))
      .toList();
  final operation = config['operation'] as String? ?? 'sqrt';
  final outputPath = config['output_file'] as String? ?? 'result.json';

  // 4. Compute
  List<num> results;
  switch (operation) {
    case 'sqrt':
      results = numbers.map((n) => sqrt(n.toDouble())).toList();
      break;
    case 'square':
      results = numbers.map((n) => n * n).toList();
      break;
    case 'random_int':
      final rng = Random(); // optionally seeded for reproducibility
      results = numbers.map((n) => rng.nextInt(n.toInt())).toList();
      break;
    default:
      _fail('Unknown operation "$operation". Valid: sqrt, square, random_int');
      return;
  }

  // 5. Write output
  final output = {
    'input': numbers,
    'operation': operation,
    'results': results,
  };
  try {
    await File(outputPath).writeAsString(jsonEncode(output));
    print('Successfully wrote $outputPath');
  } on FileSystemException {
    _fail('Cannot write to $outputPath');
  }
}

void _fail(String msg) {
  print('Error: $msg');
}
```

**Sample `config.json`:**
```json
{
  "numbers": [4, 9, 16],
  "operation": "sqrt",
  "output_file": "result.json"
}
```

**Expected `result.json`:**
```json
{"input":[4,9,16],"operation":"sqrt","results":[2.0,3.0,4.0]}
```

Use `dart run` to execute. Add more operation cases or a `seed` parameter for `random_int` as needed.
