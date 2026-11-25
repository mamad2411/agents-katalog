---
name: "generating-flutter-ui"
description: "Generative UI (GenUI) for Flutter with the genui 0.10 package (SurfaceController, A2uiTransportAdapter, Conversation, Surface) and an LLM backend such as Firebase AI Logic (firebase_ai). Use when the layout must come from model output, for chat-based UI generation, prompt-to-UI systems, or AI-driven dashboards. Do not use for static screens."
metadata:
  last_modified: "2026-11-10"
  package_versions: "genui 0.10.4, firebase_ai 5.1.0, firebase_core 5.1.0 (verified with flutter analyze on Flutter 3.47.9)"
---

# Flutter Generative UI (GenUI)

## Goal
Render UI that an AI model generates at runtime, using `genui` 0.10. Use it only for features whose structure depends on model output. Static screens should use normal widgets.

## Instructions

### 1. Setup
```bash
flutter pub add genui firebase_ai firebase_core
```
- macOS and iOS: allow outbound network access in `{ios,macos}/Runner/*.entitlements` with `com.apple.security.network.client` set to `true`.
- Initialize Firebase and configure GenUI logging before `runApp`. `DefaultFirebaseOptions` comes from the FlutterFire CLI.
```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  configureLogging(logCallback: (level, msg) => debugPrint('GenUI $level: $msg'));
  runApp(const MaterialApp(home: GenUiPage()));
}
```

### 2. Core objects

| Object | Role |
|---|---|
| `SurfaceController(catalogs: [...])` | Holds the widget catalog and the state of each surface. |
| `A2uiTransportAdapter(onSend: ...)` | Sends user messages to the model. Feed model output back with `addChunk(text)`. |
| `Conversation(controller:, transport:)` | Runs the loop. Exposes `events` and `sendRequest(ChatMessage)`. |
| `Surface(surfaceContext: controller.contextFor(id))` | Renders one surface. |

### 3. Example: Firebase AI Logic backend
This file compiles with `flutter analyze` against the pinned versions.
```dart
import 'package:firebase_ai/firebase_ai.dart';
import 'package:flutter/material.dart';
import 'package:genui/genui.dart' hide TextPart;
import 'package:genui/genui.dart' as genui;

class GenUiPage extends StatefulWidget {
  const GenUiPage({super.key});

  @override
  State<GenUiPage> createState() => _GenUiPageState();
}

class _GenUiPageState extends State<GenUiPage> {
  late final SurfaceController _controller;
  late final A2uiTransportAdapter _transport;
  late final Conversation _conversation;
  late final ChatSession _chatSession;
  final List<String> _surfaceIds = [];

  @override
  void initState() {
    super.initState();
    final catalog = BasicCatalogItems.asCatalog();
    _controller = SurfaceController(catalogs: [catalog]);
    _transport = A2uiTransportAdapter(onSend: _sendAndReceive);
    _conversation = Conversation(controller: _controller, transport: _transport);
    final model = FirebaseAI.googleAI().generativeModel(model: 'gemini-3-flash-preview');
    _chatSession = model.startChat();

    _conversation.events.listen((event) {
      switch (event) {
        case ConversationSurfaceAdded added:
          setState(() => _surfaceIds.add(added.surfaceId));
        case ConversationSurfaceRemoved removed:
          setState(() => _surfaceIds.remove(removed.surfaceId));
        case ConversationContentReceived content:
          debugPrint(content.text);
        case ConversationError error:
          debugPrint('${error.error}');
        default:
      }
    });

    final promptBuilder = PromptBuilder.chat(
      catalog: catalog,
      systemPromptFragments: ['You are a helpful assistant.'],
    );
    _conversation.sendRequest(ChatMessage.system(promptBuilder.systemPromptJoined()));
  }

  Future<void> _sendAndReceive(ChatMessage msg) async {
    final buffer = StringBuffer();
    for (final part in msg.parts) {
      if (part.isUiInteractionPart) {
        buffer.write(part.asUiInteractionPart!.interaction);
      } else if (part is genui.TextPart) {
        buffer.write(part.text);
      }
    }
    if (buffer.isEmpty) return;
    final response = await _chatSession.sendMessage(Content.text(buffer.toString()));
    if (response.text?.isNotEmpty ?? false) {
      _transport.addChunk(response.text!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      for (final id in _surfaceIds) Surface(surfaceContext: _controller.contextFor(id)),
    ]);
  }

  @override
  void dispose() {
    _conversation.dispose();
    super.dispose();
  }
}
```

### 4. Events
Handle `ConversationSurfaceAdded` and `ConversationSurfaceRemoved` by updating the list of surface IDs, then build one `Surface` per ID. Handle `ConversationContentReceived` for plain text and `ConversationError` for failures.

### 5. System prompt
Build the prompt with `PromptBuilder.chat(catalog:, systemPromptFragments:)`, then send `ChatMessage.system(promptBuilder.systemPromptJoined())` once. `systemPrompt()` is a method that returns an `Iterable<String>`, not a `String`.

### 6. Ask about input widgets
Before you write user-input UI, ask which widgets the app should use. The official guide treats this as a question for the user, not a default.

### 7. Official reference
The `genui` package ships an official integration guide at `skills/integrate-genui-firebase/SKILL.md` inside the installed package. Read it when you need the full Firebase setup steps.

## Constraints
- Do not add `genui_firebase_ai`. It is discontinued. Call `firebase_ai` directly from `onSend`.
- Do not use the 0.7-era names `ContentGenerator`, `GenUiConversation`, `A2uiMessageProcessor`, or the manual `DataModel` wiring. They do not match genui 0.10.4.
- Dispose the `Conversation` in `dispose()`.
- Use GenUI only for AI-driven structure. Do not use it for static screens or ordinary layouts.
