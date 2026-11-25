---
name: flutter-patterns
description: "Flutter app conventions: Freezed models, Riverpod providers, a Dio service layer, typed Failures, pagination, and routing. Apply when writing or reviewing Flutter/Dart code."
paths: ["**/*.dart"]
---

# Skill: Flutter Patterns

## Purpose
Guide Claude Code when implementing Flutter features in a Django-paired project. Follow these conventions unless the project's CLAUDE.md overrides them.

## Project Structure

```
lib/
├── main.dart
├── config/
│   ├── env.dart                    # Compile-time env (--dart-define)
│   └── constants.dart              # App-wide constants
├── core/
│   ├── api/                        # Dio client, interceptors
│   ├── error/                      # Sealed Failure hierarchy
│   ├── router/                     # GoRouter, auth guard
│   ├── theme/                      # Material 3 ThemeData
│   ├── providers/                  # App-level (session, auth state)
│   ├── utils/                      # Validation, formatting
│   └── widgets/                    # BaseScreen, shared dialogs
├── features/
│   └── {feature}/
│       ├── models/                 # Freezed data classes
│       ├── services/               # Interface + Django impl
│       ├── providers/              # Riverpod state
│       ├── screens/                # Full-page widgets
│       └── widgets/                # Feature-specific widgets
```

**Naming conventions:**
- Files: `snake_case.dart` (e.g. `book_service_django.dart`)
- Classes: `PascalCase` (e.g. `BookServiceDjango`)
- Features: singular noun (`profile`, `book`, `auth`)
- Screens: `{feature}_{action}_screen.dart` (`book_list_screen.dart`, `book_edit_screen.dart`)
- Generated files: co-located (`book.freezed.dart`, `book.g.dart`, `book_providers.g.dart`)

## Models

Use Freezed with `json_serializable`. Models mirror API response shapes.

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'book.freezed.dart';
part 'book.g.dart';

@freezed
abstract class Book with _$Book {
  const Book._();

  factory Book({
    @JsonKey(includeToJson: false) String? uuid,
    required String title,
    required String author,
    @JsonKey(name: 'published_date') required DateTime publishedDate,
    String? description,
    @JsonKey(name: 'cover_url') String? coverUrl,
  }) = _Book;

  factory Book.fromJson(Map<String, dynamic> json) => _$BookFromJson(json);

  factory Book.empty() => Book(
        title: '',
        author: '',
        publishedDate: DateTime.now(),
      );

  bool get exists => uuid != null;
}
```

**Conventions:**
- Freezed 3.x: annotate data classes `abstract` (unions use `sealed`); `@freezed` alone no longer generates the class body
- `const Book._()` private constructor enables custom getters/methods
- `@JsonKey(name: ...)` for snake_case API fields
- `@JsonKey(includeToJson: false)` for server-managed fields like `uuid` (the public identifier — never an integer `id`)
- `factory Book.empty()` for form initialization
- `bool get exists` for create-vs-update logic
- Keep models flat — no nested domain/data split

## Services

Abstract interface defines the contract. One concrete implementation per backend.

```dart
// book_service.dart
abstract class BookService {
  Future<PaginatedResponse<Book>> list({required int page, int pageSize = 20});
  Future<Book> retrieve(String uuid);
  Future<Book> save(Book book);
  Future<void> delete(String uuid);
}
```

```dart
// book_service_django.dart
class BookServiceDjango implements BookService {
  final DioClient client;

  BookServiceDjango(this.client);

  @override
  Future<PaginatedResponse<Book>> list({required int page, int pageSize = 20}) async {
    final response = await client.get(
      '/api/v1/books/',
      queryParameters: {'page': page, 'page_size': pageSize, 'ordering': '-created_at'},
    );
    final results = (response['results'] as List)
        .map((json) => Book.fromJson(json))
        .toList();
    return PaginatedResponse(
      page: response['page'],
      count: response['count'],
      numPages: response['num_pages'],
      results: results,
    );
  }

  @override
  Future<Book> retrieve(String uuid) async {
    final response = await client.get('/api/v1/books/$uuid/');
    return Book.fromJson(response);
  }

  @override
  Future<Book> save(Book book) async {
    if (book.exists) {
      final response = await client.patch('/api/v1/books/${book.uuid}/', data: book.toJson());
      return Book.fromJson(response);
    }
    final response = await client.post('/api/v1/books/', data: book.toJson());
    return Book.fromJson(response);
  }

  @override
  Future<void> delete(String uuid) async {
    await client.delete('/api/v1/books/$uuid/');
  }
}
```

**Conventions:**
- Services throw typed `Failure` exceptions (see Error Handling)
- `save()` combines create + update using `model.exists`
- No `Either`/`fpdart` — use `AsyncValue` for error handling at the provider level
- One service per feature, one implementation per backend

## Providers

Use `@riverpod` codegen everywhere. `AsyncNotifier` for stateful operations. Simple functional providers for reads.

### Service binding

```dart
// book_service_provider.dart
@riverpod
BookService bookService(Ref ref) {
  return BookServiceDjango(ref.watch(dioClientProvider));
}
```

### Detail provider (functional)

```dart
// book_detail_provider.dart
@riverpod
Future<Book> bookDetail(Ref ref, String uuid) async {
  return ref.watch(bookServiceProvider).retrieve(uuid);
}
```

### List provider (AsyncNotifier)

```dart
// book_list_provider.dart
@riverpod
class BookList extends _$BookList {
  int _page = 1;

  @override
  Future<PaginatedResponse<Book>> build() => _fetch();

  Future<PaginatedResponse<Book>> _fetch() {
    return ref.read(bookServiceProvider).list(page: _page);
  }

  Future<void> loadPage(int page) async {
    _page = page;
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => _fetch());
  }

  Future<void> refresh() async {
    _page = 1;
    ref.invalidateSelf();
  }
}
```

### Form provider (Notifier)

```dart
// book_form_provider.dart
@Riverpod(keepAlive: true)
class BookForm extends _$BookForm {
  @override
  Book build() => Book.empty();

  final formKey = GlobalKey<FormState>();
  final titleController = TextEditingController();
  final authorController = TextEditingController();

  void load(Book book) {
    state = book;
    titleController.text = book.title;
    authorController.text = book.author;
  }

  void reset() {
    state = Book.empty();
    titleController.clear();
    authorController.clear();
  }

  Future<bool> submit() async {
    if (!formKey.currentState!.validate()) return false;

    final book = state.copyWith(
      title: titleController.text,
      author: authorController.text,
    );

    try {
      final saved = await ref.read(bookServiceProvider).save(book);
      state = saved;
      reset();
      ref.invalidate(bookListProvider);
      if (saved.uuid != null) ref.invalidate(bookDetailProvider(saved.uuid!));
      return true;
    } on Failure catch (e) {
      // Surface error to UI via snackbar or dialog — don't swallow
      rethrow;
    }
  }

  Future<bool> delete() async {
    if (state.uuid == null) return false;
    await ref.read(bookServiceProvider).delete(state.uuid!);
    reset();
    ref.invalidate(bookListProvider);
    return true;
  }
}
```

**Conventions:**
- `@riverpod` (lowercase) for auto-dispose providers — most reads
- `@Riverpod(keepAlive: true)` for forms and auth state that survive navigation
- `AsyncValue.guard()` for wrapping async calls in list/detail providers
- Form providers own `TextEditingController`s and `GlobalKey<FormState>`
- After mutation, `ref.invalidate()` related list/detail providers

## Screens

Screens extend `BaseScreen`, which provides `Scaffold` with responsive breakpoint support.

```dart
class BookListScreen extends BaseScreen {
  static String route() => '/books';

  const BookListScreen({super.key});

  @override
  AppBar? appBar(BuildContext context, WidgetRef ref) {
    return AppBar(
      title: const Text('Books'),
      actions: [
        IconButton(
          onPressed: () {
            ref.read(bookFormProvider.notifier).reset();
            context.push(BookEditScreen.routeNew());
          },
          icon: const Icon(Icons.add),
        ),
      ],
    );
  }

  @override
  Widget body(BuildContext context, WidgetRef ref) {
    return const BookInfiniteListWidget();
  }
}
```

```dart
class BookDetailScreen extends BaseScreen {
  final String bookUuid;
  static String route([String? uuid]) => '/books/${uuid ?? ':uuid'}';

  const BookDetailScreen({super.key, required this.bookUuid});

  @override
  Widget body(BuildContext context, WidgetRef ref) {
    final data = ref.watch(bookDetailProvider(bookUuid));
    return data.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, _) => Center(child: Text(error.toString())),
      data: (book) => BookDetailWidget(book: book),
    );
  }
}
```

**Conventions:**
- Static `route()` method returns the path string
- Consume providers with `ref.watch()` in `body()`, `ref.read()` for actions
- Use `AsyncValue.when()` to handle loading/error/data states
- Override `bodyMd()` / `bodyLg()` only when layout differs at breakpoints

### BaseScreen

```dart
abstract class BaseScreen extends ConsumerWidget {
  final double horizontalPadding;
  final double verticalPadding;

  const BaseScreen({super.key, this.horizontalPadding = 16, this.verticalPadding = 8});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: appBar(context, ref),
      floatingActionButton: floatingActionButton(context, ref),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: verticalPadding),
        child: body(context, ref),
      ),
    );
  }

  AppBar? appBar(BuildContext context, WidgetRef ref) => null;
  FloatingActionButton? floatingActionButton(BuildContext context, WidgetRef ref) => null;
  Widget body(BuildContext context, WidgetRef ref) => const SizedBox.shrink();
}
```

## Widgets

### Extraction rules
- Extract when a widget exceeds ~40 lines or is reused
- One widget per file in `widgets/`
- Prefer `const` constructors — all fields `final`
- Compose widgets, never inherit (except `BaseScreen`)

### Consuming providers in widgets

```dart
class BookListTile extends ConsumerWidget {
  final Book book;
  const BookListTile({super.key, required this.book});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListTile(
      title: Text(book.title),
      subtitle: Text(book.author),
      onTap: () => context.push(BookDetailScreen.route(book.uuid)),
    );
  }
}
```

**Conventions:**
- Pass data down as constructor params when possible
- Use `ConsumerWidget` only when the widget needs `ref`
- Avoid deep nesting — extract sub-widgets at 3-4 levels

## API Client

Singleton Dio instance with interceptor chain: auth, token refresh, logging.

The canonical `DioClient` is defined in the **flutter-bootstrap** skill at `lib/core/api/dio_client.dart` — don't re-implement it here. It exposes `get`/`post`/`patch`/`delete`, injects the bearer token, refreshes an expired access token against `/api/v1/auth/refresh/` (reusing the stored refresh token, since the contract's refresh returns `{access}` only), and maps every `DioException` to a typed `Failure`.

**Conventions:**
- Single `Dio` instance — no per-request construction
- Timeouts configured at construction
- Token refresh in the auth interceptor, not scattered across services — and a failed refresh clears the session and rejects the request rather than sending it unauthenticated
- `LogInterceptor` gated behind `kDebugMode` — no raw `print()`
- `DioClient` maps `DioException` to a typed `Failure` via `mapDioException` (see Error Handling) — services and providers only ever see `Failure`s

## Auth

JWT session with secure storage, auth state provider, and router guard.

### Session provider

The canonical `secureStorage` provider and the keep-alive `Session` notifier live in the **flutter-bootstrap** skill at `lib/core/providers/session_provider.dart` — `Session` holds the `SessionToken`, persists it to `flutter_secure_storage`, and exposes `initialize`/`setToken`/`clearToken`. Reference it rather than re-declaring it.

### Auth notifier

```dart
@Riverpod(keepAlive: true)
class Auth extends _$Auth {
  @override
  FutureOr<User?> build() async {
    await ref.read(sessionProvider.notifier).initialize();
    if (ref.read(sessionProvider) == null) return null;
    return ref.read(authServiceProvider).currentUser();
  }

  Future<void> login({required String email, required String password}) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final user = await ref.read(authServiceProvider).login(email: email, password: password);
      return user;
    });
  }

  Future<void> logout() async {
    await ref.read(authServiceProvider).logout();
    ref.read(sessionProvider.notifier).clearToken();
    state = const AsyncData(null);
  }
}
```

### Route guard

```dart
@riverpod
GoRouter router(Ref ref) {
  final auth = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/books',
    redirect: (context, routerState) {
      final isLoggedIn = auth.valueOrNull != null;
      final isAuthRoute = routerState.matchedLocation.startsWith('/auth');

      if (!isLoggedIn && !isAuthRoute) return '/auth/login';
      if (isLoggedIn && isAuthRoute) return '/books';
      return null;
    },
    routes: [/* ... */],
  );
}
```

**Conventions:**
- Use `flutter_secure_storage` for token persistence
- Auth provider uses `AsyncValue<User?>` — null means logged out
- Router watches auth provider and rebuilds on auth state changes
- Session provider is keepAlive — survives navigation

## Error Handling

Sealed `Failure` class hierarchy. Services throw typed failures. Providers surface via `AsyncValue.error`.

The canonical `Failure` hierarchy — `sealed class Failure` with `ServerFailure`/`NetworkFailure`/`AuthFailure`/`ValidationFailure` — is defined in the **flutter-bootstrap** skill at `lib/core/error/failures.dart`. Reference it rather than re-declaring the classes; the conversion helper below is the DioException→Failure mapping the client layer applies.

### Converting DioException to Failure (in DioClient or a helper)

```dart
Failure mapDioException(DioException e) {
  if (e.type == DioExceptionType.connectionError ||
      e.type == DioExceptionType.connectionTimeout) {
    return const NetworkFailure();
  }
  final statusCode = e.response?.statusCode;
  if (statusCode == 401 || statusCode == 403) {
    return AuthFailure(e.response?.data?['detail'] ?? 'Authentication failed');
  }
  if (statusCode == 400) {
    return ValidationFailure(
      'Validation error',
      fieldErrors: _parseFieldErrors(e.response?.data),
    );
  }
  return ServerFailure(
    e.response?.data?['detail'] ?? 'Server error',
    statusCode: statusCode,
  );
}
```

### Surfacing errors in UI

```dart
// In a screen or widget:
ref.listen(bookListProvider, (prev, next) {
  if (next is AsyncError) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(next.error.toString())),
    );
  }
});
```

**Conventions:**
- Services catch `DioException` and throw typed `Failure`
- Providers use `AsyncValue.guard()` — failures surface as `AsyncError`
- UI uses `ref.listen()` or `AsyncValue.when()` to display errors
- No `Either`/`fpdart` — `AsyncValue` handles the loading/error/data tri-state

## Forms

`AsyncNotifier`-based form providers own controllers and validation. Submission returns `bool` for navigation.

### Form provider pattern (see Providers section for full example)

Key points:
- `TextEditingController` + `GlobalKey<FormState>` live on the notifier
- `load(Model)` populates controllers from existing data
- `reset()` clears everything for a fresh form
- `submit()` validates, calls service, invalidates related providers, returns success
- `keepAlive: true` so form state survives back-navigation during editing

### Form widget

```dart
class BookFormWidget extends ConsumerWidget {
  const BookFormWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifier = ref.read(bookFormProvider.notifier);
    final book = ref.watch(bookFormProvider);

    return Form(
      key: notifier.formKey,
      child: Column(
        children: [
          TextFormField(
            controller: notifier.titleController,
            validator: (v) => v == null || v.isEmpty ? 'Title required' : null,
            decoration: const InputDecoration(labelText: 'Title'),
          ),
          TextFormField(
            controller: notifier.authorController,
            decoration: const InputDecoration(labelText: 'Author'),
          ),
        ],
      ),
    );
  }
}
```

### Edit screen with submit

```dart
class BookEditScreen extends BaseScreen {
  final String? bookUuid;
  static String route([String? uuid]) => '/books/edit/${uuid ?? ':uuid'}';
  static String routeNew() => '/books/new';

  const BookEditScreen({super.key, this.bookUuid});

  @override
  AppBar? appBar(BuildContext context, WidgetRef ref) {
    return AppBar(
      title: Text(bookUuid != null ? 'Edit Book' : 'New Book'),
      actions: [
        IconButton(
          onPressed: () async {
            final success = await ref.read(bookFormProvider.notifier).submit();
            if (success && context.mounted) context.pop();
          },
          icon: const Icon(Icons.check),
        ),
      ],
    );
  }

  @override
  Widget body(BuildContext context, WidgetRef ref) {
    return const SingleChildScrollView(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: BookFormWidget(),
      ),
    );
  }
}
```

### Image upload

Use `image_picker` for selection. Upload to the backend's asset endpoint, receive a URL, store it on the model.

```dart
Future<void> pickAndUploadImage(WidgetRef ref) async {
  final picked = await ImagePicker().pickImage(source: ImageSource.gallery);
  if (picked == null) return;

  final bytes = await picked.readAsBytes();
  final url = await ref.read(assetServiceProvider).upload(
    filename: picked.name,
    bytes: bytes,
  );
  // Store url on the form model via the form provider
}
```

## Lists

Two patterns: paginated (page controls) and infinite scroll (load-more).

### Paginated list provider

See the `BookList` `AsyncNotifier` in the Providers section. UI consumes with:

```dart
final data = ref.watch(bookListProvider);
data.when(
  loading: () => const CircularProgressIndicator(),
  error: (e, _) => Text(e.toString()),
  data: (paginated) => Column(
    children: [
      ListView.builder(
        shrinkWrap: true,
        itemCount: paginated.results.length,
        itemBuilder: (context, i) => BookListTile(book: paginated.results[i]),
      ),
      // Page controls
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (paginated.page > 1)
            TextButton(
              onPressed: () => ref.read(bookListProvider.notifier).loadPage(paginated.page - 1),
              child: const Text('Previous'),
            ),
          Text('Page ${paginated.page} of ${paginated.numPages}'),
          if (paginated.page < paginated.numPages)
            TextButton(
              onPressed: () => ref.read(bookListProvider.notifier).loadPage(paginated.page + 1),
              child: const Text('Next'),
            ),
        ],
      ),
    ],
  ),
);
```

### Infinite scroll

Use the `infinite_scroll_pagination` package (v5) with a Riverpod provider exposing the `PagingController`. v5 drops `appendPage`/`appendLastPage`/`addPageRequestListener` — the controller is built from `getNextPageKey` + `fetchPage`, and the widget consumes a `PagingState` via `PagingListener`.

```dart
@Riverpod(keepAlive: true)
class BookInfiniteList extends _$BookInfiniteList {
  @override
  PagingController<int, Book> build() {
    final controller = PagingController<int, Book>(
      // Stop once a fetched page comes back empty; otherwise request page N+1.
      getNextPageKey: (state) =>
          state.lastPageIsEmpty ? null : state.nextIntPageKey,
      fetchPage: (page) async {
        final data = await ref.read(bookServiceProvider).list(page: page);
        return data.results;
      },
    );
    ref.onDispose(controller.dispose);
    return controller;
  }

  void refresh() => state.refresh();
}
```

Widget:

```dart
class BookInfiniteListWidget extends ConsumerWidget {
  const BookInfiniteListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.watch(bookInfiniteListProvider);

    return RefreshIndicator(
      onRefresh: () async => ref.read(bookInfiniteListProvider.notifier).refresh(),
      child: PagingListener(
        controller: controller,
        builder: (context, state, fetchNextPage) => PagedListView<int, Book>(
          state: state,
          fetchNextPage: fetchNextPage,
          builderDelegate: PagedChildBuilderDelegate<Book>(
            itemBuilder: (context, book, index) => BookListTile(book: book),
            noItemsFoundIndicatorBuilder: (_) => const Center(child: Text('No books found')),
          ),
        ),
      ),
    );
  }
}
```

### PaginatedResponse model

The canonical `PaginatedResponse<T>` — `page`, `count`, `numPages`, `results`, and `canLoadMore` — is defined in the **flutter-bootstrap** skill at `lib/core/models/paginated_response.dart`. It maps the contract's `{page, count, num_pages, results}` response shape (query params `page`/`page_size`). Reference it rather than re-declaring it.

### Filtering and ordering

Pass filter/order params through the service and into query parameters:

```dart
Future<PaginatedResponse<Book>> list({
  required int page,
  int pageSize = 20,
  String? search,
  String ordering = '-created_at',
}) async {
  final response = await client.get('/api/v1/books/', queryParameters: {
    'page': page,
    'page_size': pageSize,
    'ordering': ordering,
    if (search != null) 'search': search,
  });
  // ... parse response
}
```

## Testing

### Unit tests (services and providers)

```dart
// Mock the service
class MockBookService extends Mock implements BookService {}

void main() {
  late MockBookService mockService;

  setUp(() {
    mockService = MockBookService();
  });

  test('retrieve returns book', () async {
    final book = Book(uuid: 'book-uuid-1', title: 'Test', author: 'Author', publishedDate: DateTime.now());
    when(() => mockService.retrieve('book-uuid-1')).thenAnswer((_) async => book);

    final result = await mockService.retrieve('book-uuid-1');
    expect(result.title, 'Test');
  });
}
```

### Widget tests

```dart
void main() {
  testWidgets('BookListTile displays title and author', (tester) async {
    final book = Book(id: 1, title: 'My Book', author: 'Jane', publishedDate: DateTime.now());

    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(home: Scaffold(body: BookListTile(book: book))),
      ),
    );

    expect(find.text('My Book'), findsOneWidget);
    expect(find.text('Jane'), findsOneWidget);
  });
}
```

### Provider tests

```dart
void main() {
  test('bookDetail returns data', () async {
    final container = ProviderContainer(
      overrides: [
        bookServiceProvider.overrideWithValue(MockBookService()),
      ],
    );

    // Set up mock responses, then test provider output
  });
}
```

**Conventions:**
- Use `mocktail` for mocking (not `mockito`)
- Override service providers in tests — never mock Dio directly
- Widget tests wrap with `ProviderScope` + `MaterialApp`
- Test behavior, not implementation — assert what the user sees

## Working from Integration Summaries

When starting Flutter frontend work from a backend integration summary:
1. Generate Freezed model classes matching response shapes
2. Build the service interface + Django implementation
3. Wire up providers (service binding, list, detail, form)
4. Build screens and widgets
5. Verify against the real API before polishing UI
6. Flag any discrepancies between the summary and actual API behavior
