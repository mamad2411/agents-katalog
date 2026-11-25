---
name: "building-jaspr-web-apps"
description: "Builds SEO-friendly web applications with Dart using the Jaspr framework. Use when creating Dart-based websites, blogs, or landing pages requiring semantic HTML output; implementing server-side rendering (SSR) or static site generation (SSG); adding Tailwind CSS via jaspr_tailwind; routing with jaspr_router; testing components with jaspr_test; or building full-stack Dart web apps where Flutter Web's canvas rendering is unsuitable."
metadata:
  last_modified: "2026-04-27 17:41:00 (GMT+8)"
---

# Jaspr Web Architecture Guide (v0.23.x)

## Goal
[Jaspr](https://jaspr.site/) is a Dart web framework (current version: **0.22.x**).

Unlike Flutter Web (which draws pixels via Canvas and produces poor SEO), Jaspr compiles Dart to semantic HTML and CSS DOM elements. Use Jaspr for websites, blogs, landing pages, or any project requiring proper SEO.

## Instructions

### 1. Core Concept: Flutter-like Coding Experience
Jaspr mirrors Flutter’s component model. The `build` method returns a single `Component` (equivalent to a Flutter `Widget`).

| Flutter Concept | Jaspr Concept | Notes |
| :--- | :--- | :--- |
| `Widget` | `Component` | Every UI element in Jaspr is a Component |
| `StatelessWidget` | `StatelessComponent` | Pure declarative UI; receives `BuildContext context` |
| `StatefulWidget` | `StatefulComponent` | Manages lifecycle with `setState`, `initState`, `createState()` |
| `InheritedWidget` | `InheritedComponent` | Propagates state down the component tree |

#### 1.1 DOM Elements
Jaspr renders to DOM, so use its HTML tag helpers (`div`, `p`, `img`, etc.) from `jaspr/dom.dart`.

```dart
import 'package:jaspr/jaspr.dart';
import 'package:jaspr/dom.dart';

class ProfileCard extends StatelessComponent {
  final String name;

  const ProfileCard({required this.name, super.key});

  @override
  Component build(BuildContext context) {
    return div(
      classes: 'profile-card',
      styles: Styles(width: 300.px, backgroundColor: Colors.white),
      [
        h2([.text(name)]), // 🌟 .text() shorthand available since Dart 3.10 (Component.text)
        p([
          .text('Hello World!'),
        ]),
        button(
          onClick: () => print('Button successfully clicked!'),
          [.text('Contact Me')]
        )
      ]
    );
  }
}
```

### 2. Tailwind CSS Integration (`jaspr_tailwind`)
Jaspr provides official Tailwind CSS integration via `jaspr_tailwind`.

#### 2.1 Installation & Setup
```yaml
dev_dependencies:
  jaspr_tailwind: ^0.3.6  # does not resolve on Dart 3.13 (build_modules >=5 needs SDK <3.13); use Dart 3.12 or remove
```

Create `web/styles.tw.css` with the Tailwind v4 CSS-first syntax:
```css
/* web/styles.tw.css */
@import "tailwindcss";
```

#### 2.2 Loading Compiled CSS in the Root Component
In the root component, use `Document.head` to link the compiled stylesheet and consume Tailwind classes via the `classes` parameter:

```dart
import 'package:jaspr/jaspr.dart';
import 'package:jaspr/dom.dart';

class App extends StatelessComponent {
  @override
  Component build(BuildContext context) {
    return Component.fragment([
      // 🌟 jaspr_tailwind auto-compiles styles.tw.css → styles.css. Head content goes in Document.head.
      Document.head(children: [
        link(href: 'styles.css', rel: 'stylesheet'),
      ]),
      // Use Tailwind classes directly; jaspr_tailwind auto-refreshes during development
      div(
        classes: 'bg-gray-100 min-h-screen flex items-center justify-center',
        [
          h1(classes: 'text-4xl font-bold text-blue-600', [Component.text('Hello Tailwind!')]),
        ],
      ),
    ]);
  }
}
```

### 3. Routing (`jaspr_router`)
Jaspr’s routing mirrors `go_router` with a declarative API.

#### 3.1 Installation & Setup
```yaml
dependencies:
  jaspr_router: ^0.9.0
```

```dart
import 'package:jaspr/jaspr.dart';
import 'package:jaspr_router/jaspr_router.dart';

class MyApp extends StatelessComponent {
  @override
  Component build(BuildContext context) {
    return Router(
      routes: [
        Route(
          path: '/', 
          builder: (context, state) => const HomePage(),
        ),
        Route(
          path: '/about', 
          builder: (context, state) => const AboutPage(),
        ),
      ],
    );
  }
}
```

### 4. SSR: Asynchronous Backend Data Preloading

Jaspr’s key advantage over Flutter Web is server-side rendering (SSR). With Flutter Web, data is fetched in `initState`, causing a loading state on the client. With Jaspr SSR, data is fetched on the server before the HTML is sent to the browser.

#### 4.1 `AsyncStatelessComponent` (Server-only)
Import `jaspr/server.dart` to use `AsyncStatelessComponent`, which allows an `async` build method.

```dart
import 'package:jaspr/server.dart'; // 🌟 Server-only import
import 'package:jaspr/dom.dart';

class ArticlePage extends AsyncStatelessComponent {
  final String articleId;
  const ArticlePage(this.articleId);

  @override
  Future<Component> build(BuildContext context) async {
    // Runs server-side; freely use await for database/API calls
    final articleData = await Database.fetchArticle(articleId);

    // Browser receives fully-rendered HTML for instant, SEO-friendly content
    return div([
      h1([.text(articleData.title)]),
      p([.text(articleData.content)]),
    ]);
  }
}
```

#### 4.2 Stateful Preloading (`PreloadStateMixin`)
When state must be preserved, mix in `PreloadStateMixin`:

```dart
class MyState extends State<MyStatefulComponent> with PreloadStateMixin {
  
  @override
  Future<void> preloadState() async {
    // Runs server-side before initState(); prepares state for client-side hydration
    await loadInitialData();
  }
  
  // ...
}
```

### 5. Testing (`jaspr_test`)
`jaspr_test` covers component unit tests, SSR results, and browser interactions.

#### 5.1 Dependency Setup
```bash
dart pub add jaspr_test --dev
```
Since `jaspr_test` re-exports the native `package:test`, there is no need to import it separately.

#### 5.2 Three Major Testing Functions
Due to the complexities of the HTML/Web environment, Jaspr provides three scenario-specific testing functions:

**`testComponents` (Virtual Environment Component Testing)**
Unit test your Component logic in a Headless, pure Dart simulated environment. This is the fastest method. Usage is highly similar to Flutter's `testWidgets`.
```dart
import 'package:jaspr_test/jaspr_test.dart';

void main() {
  testComponents('Test clicking the button increments the count', (tester) async {
    tester.pumpComponent(MyComponent());
    expect(find.text('Count: 0'), findsOneComponent);
    await tester.click(find.tag('button'));
    expect(find.text('Count: 1'), findsOneComponent);
  });
}
```

**`testServer` (Server-Side Rendering Testing)**
Aimed at testing SSR applications. It directly starts a simulated local HTTP Server. You can send Requests and verify the HTML strings or state properties returned by the Server.
```dart
import 'package:jaspr_test/server_test.dart';

void main() {
  testServer('Verify Server-Side rendered HTML', (tester) async {
    final response = await tester.request('/');
    expect(response.document?.body?.text, contains('Welcome to SSR'));
  });
}
```

**`testClient` (Browser Hydration and State Syncing Tests)**
Runs in a headless browser environment, testing whether the client correctly takes over via hydration and handles DOM interactions after receiving `initialStateData` from the server.

### 6. State Management with BlocSignal (`bloc_signals_jaspr`)
Use `bloc_signals_jaspr` when a Jaspr app needs shared, event-driven state. It provides `BlocSignalProvider`, `BlocSignalBuilder`, `BlocSignalListener`, `BlocSignalSelector`, and `context.read/select`, all as Components. Verified with `jaspr` 0.23.5, `bloc_signals_jaspr` 1.3.0, and `bloc_signals` 1.7.0.
- **Reference**: [references/bloc-signals.md](references/bloc-signals.md)
- Keep bloc creation inside a provider in the page component. A top-level bloc is shared across SSR requests.

## Constraints
* Only use `AsyncStatelessComponent` on the server side (`jaspr/server.dart`). Never in client UI code.
* Do not nest Flutter `Widget`s inside Jaspr `Component`s.
* Choose the tester matching your render mode: SSR → `testServer`, CSR → `testComponents`, browser → `testClient`. Prefer DOM string matching over strict typing.
