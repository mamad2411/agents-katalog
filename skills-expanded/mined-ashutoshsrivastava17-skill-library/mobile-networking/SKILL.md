---
name: mobile-networking
description: >
  Design and implement mobile networking layers — HTTP clients, interceptors,
  authentication token management, caching, offline queues, GraphQL, WebSockets,
  and response parsing across Flutter (Dio/http), Android (Retrofit/OkHttp/Ktor),
  and iOS (URLSession/Alamofire).
  TRIGGER when: user says /mobile-networking, asks about API integration in mobile,
  needs to set up networking, implement token refresh, or optimize API calls.
argument-hint: "[networking task or API integration need]"
user-invocable: true
---

# Mobile Networking

You are a senior mobile engineer. Help the user design, implement, or review mobile networking layers with platform-specific best practices.

## Process

### Step 1: Understand Requirements

| Question | Why It Matters |
|----------|---------------|
| What API protocol? (REST, GraphQL, gRPC, WebSocket) | Determines client library |
| What auth mechanism? (Bearer JWT, OAuth2, API key, session cookie) | Token management strategy |
| Does the app work offline? | Offline queue and cache strategy |
| What is the expected request volume? | Connection pooling, batching |
| Are there file uploads/downloads? | Multipart, streaming, progress tracking |
| What serialization format? (JSON, Protocol Buffers, MessagePack) | Parser selection |

### Step 2: Choose HTTP Client

#### Flutter

| Library | Best For | Features |
|---------|----------|----------|
| **Dio** | Most apps — recommended default | Interceptors, cancellation, multipart, FormData, transformers |
| **http** | Simple apps, minimal dependencies | Lightweight, built by Dart team |
| **Chopper** | Retrofit-style code generation | Type-safe, interceptors, converters |
| **graphql_flutter** | GraphQL APIs | Queries, mutations, subscriptions, cache |

```dart
// Dio — setup with interceptors
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com/v1',
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 15),
  headers: {'Content-Type': 'application/json'},
));

// Add interceptors
dio.interceptors.addAll([
  AuthInterceptor(tokenStorage),
  LogInterceptor(requestBody: true, responseBody: true),
  RetryInterceptor(dio: dio, retries: 3),
]);

// Type-safe API call
Future<List<Product>> getProducts() async {
  final response = await dio.get('/products');
  return (response.data as List)
      .map((json) => Product.fromJson(json))
      .toList();
}

// Multipart file upload
Future<void> uploadImage(File file) async {
  final formData = FormData.fromMap({
    'image': await MultipartFile.fromFile(file.path),
    'description': 'Product image',
  });
  await dio.post('/upload', data: formData);
}
```

#### Android (Kotlin)

| Library | Best For | Features |
|---------|----------|----------|
| **Retrofit + OkHttp** | Most apps — recommended default | Type-safe, interceptors, converters, widely adopted |
| **Ktor Client** | KMP / coroutines-first | Multiplatform, DSL-based, engine-agnostic |
| **Apollo Kotlin** | GraphQL APIs | Queries, mutations, subscriptions, normalized cache |
| **OkHttp (raw)** | Low-level control | Full HTTP control, WebSocket built-in |

```kotlin
// Retrofit + OkHttp — setup
interface ProductApi {
    @GET("products")
    suspend fun getProducts(): List<ProductDto>

    @GET("products/{id}")
    suspend fun getProduct(@Path("id") id: String): ProductDto

    @POST("products")
    suspend fun createProduct(@Body product: CreateProductRequest): ProductDto

    @Multipart
    @POST("upload")
    suspend fun uploadImage(@Part image: MultipartBody.Part): UploadResponse
}

// OkHttp client with interceptors
val okHttpClient = OkHttpClient.Builder()
    .addInterceptor(AuthInterceptor(tokenStorage))
    .addInterceptor(HttpLoggingInterceptor().apply {
        level = if (BuildConfig.DEBUG) Level.BODY else Level.NONE
    })
    .connectTimeout(10, TimeUnit.SECONDS)
    .readTimeout(15, TimeUnit.SECONDS)
    .retryOnConnectionFailure(true)
    .build()

// Retrofit instance
val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/v1/")
    .client(okHttpClient)
    .addConverterFactory(MoshiConverterFactory.create(moshi))
    // or: .addConverterFactory(KotlinxSerializationConverterFactory.create(json))
    .build()

val api = retrofit.create(ProductApi::class.java)
```

#### Android (Java)

```java
// Retrofit + OkHttp — Java
public interface ProductApi {
    @GET("products")
    Call<List<ProductDto>> getProducts();

    @GET("products/{id}")
    Call<ProductDto> getProduct(@Path("id") String id);

    @POST("products")
    Call<ProductDto> createProduct(@Body CreateProductRequest product);
}

// With RxJava
public interface ProductApi {
    @GET("products")
    Single<List<ProductDto>> getProducts();
}

// OkHttp client
OkHttpClient client = new OkHttpClient.Builder()
    .addInterceptor(new AuthInterceptor(tokenStorage))
    .addInterceptor(new HttpLoggingInterceptor().setLevel(Level.BODY))
    .connectTimeout(10, TimeUnit.SECONDS)
    .build();

Retrofit retrofit = new Retrofit.Builder()
    .baseUrl("https://api.example.com/v1/")
    .client(client)
    .addConverterFactory(GsonConverterFactory.create())
    .addCallAdapterFactory(RxJava3CallAdapterFactory.create()) // for RxJava
    .build();
```

#### iOS (Swift)

| Library | Best For | Features |
|---------|----------|----------|
| **URLSession + async/await** | Most apps — recommended default | Built-in, no dependencies, full control |
| **Alamofire** | Apps needing request chaining, interceptors, retry | Battle-tested, rich feature set |
| **Apollo iOS** | GraphQL APIs | Queries, mutations, subscriptions, code generation |
| **URLSession (Combine)** | Reactive chains | dataTaskPublisher, built-in |

```swift
// URLSession + async/await — modern approach
class APIClient {
    private let session: URLSession
    private let baseURL: URL
    private let decoder = JSONDecoder()

    func getProducts() async throws -> [Product] {
        let url = baseURL.appendingPathComponent("products")
        var request = URLRequest(url: url)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await session.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw APIError.invalidResponse
        }
        return try decoder.decode([Product].self, from: data)
    }

    // File upload
    func uploadImage(_ imageData: Data) async throws -> UploadResponse {
        var request = URLRequest(url: baseURL.appendingPathComponent("upload"))
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n")
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n")
        body.append("Content-Type: image/jpeg\r\n\r\n")
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n")

        let (data, _) = try await session.upload(for: request, from: body)
        return try decoder.decode(UploadResponse.self, from: data)
    }
}
```

```swift
// Alamofire — request chaining
AF.request("https://api.example.com/v1/products",
           headers: ["Authorization": "Bearer \(token)"])
    .validate()
    .responseDecodable(of: [Product].self) { response in
        switch response.result {
        case .success(let products): handleProducts(products)
        case .failure(let error): handleError(error)
        }
    }

// Alamofire interceptor
class AuthInterceptor: RequestInterceptor {
    func adapt(_ urlRequest: URLRequest, for session: Session,
               completion: @escaping (Result<URLRequest, Error>) -> Void) {
        var request = urlRequest
        request.setValue("Bearer \(getToken())", forHTTPHeaderField: "Authorization")
        completion(.success(request))
    }

    func retry(_ request: Request, for session: Session, dueTo error: Error,
               completion: @escaping (RetryResult) -> Void) {
        guard let statusCode = request.response?.statusCode, statusCode == 401 else {
            completion(.doNotRetry)
            return
        }
        refreshToken { success in
            completion(success ? .retry : .doNotRetry)
        }
    }
}
```

#### iOS (Objective-C)

```objc
// NSURLSession — legacy approach
NSURLSessionConfiguration *config = [NSURLSessionConfiguration defaultSessionConfiguration];
config.timeoutIntervalForRequest = 10;
config.HTTPAdditionalHeaders = @{@"Authorization": [NSString stringWithFormat:@"Bearer %@", token]};

NSURLSession *session = [NSURLSession sessionWithConfiguration:config];

NSURL *url = [NSURL URLWithString:@"https://api.example.com/v1/products"];
NSURLSessionDataTask *task = [session dataTaskWithURL:url
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if (error) { /* handle error */ return; }
        NSArray *products = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
        dispatch_async(dispatch_get_main_queue(), ^{
            [self updateUIWithProducts:products];
        });
    }];
[task resume];

// AFNetworking (legacy Alamofire equivalent)
AFHTTPSessionManager *manager = [[AFHTTPSessionManager alloc] initWithBaseURL:baseURL];
[manager GET:@"products" parameters:nil headers:@{@"Authorization": authHeader}
    progress:nil
    success:^(NSURLSessionDataTask *task, id responseObject) {
        // Handle success
    }
    failure:^(NSURLSessionDataTask *task, NSError *error) {
        // Handle failure
    }];
```

### Step 3: Implement Token Management

**Auth token refresh flow (all platforms):**

```
Request with token → 401 Unauthorized
  → Lock concurrent requests (prevent multiple refresh attempts)
  → Call refresh token endpoint
  → Success? → Update stored tokens → Retry original request + queued requests
  → Failure? → Clear tokens → Navigate to login
```

#### Flutter — Dio Token Refresh Interceptor
```dart
class AuthInterceptor extends QueuedInterceptor {
  final TokenStorage _tokenStorage;
  final Dio _refreshDio; // separate Dio instance to avoid recursion

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    final token = await _tokenStorage.getAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode != 401) {
      return handler.next(err);
    }

    try {
      final refreshToken = await _tokenStorage.getRefreshToken();
      final response = await _refreshDio.post('/auth/refresh', data: {
        'refresh_token': refreshToken,
      });
      await _tokenStorage.saveTokens(
        accessToken: response.data['access_token'],
        refreshToken: response.data['refresh_token'],
      );
      // Retry the failed request
      final retryResponse = await _refreshDio.fetch(err.requestOptions);
      handler.resolve(retryResponse);
    } catch (e) {
      await _tokenStorage.clearTokens();
      handler.next(err); // propagate to force logout
    }
  }
}
```

#### Android (Kotlin) — OkHttp Authenticator
```kotlin
class TokenAuthenticator(
    private val tokenStorage: TokenStorage,
    private val authApi: AuthApi
) : Authenticator {

    private val lock = Mutex()

    override fun authenticate(route: Route?, response: Response): Request? {
        // Max retry
        if (response.retryCount > 1) return null

        return runBlocking {
            lock.withLock {
                // Check if another thread already refreshed
                val currentToken = tokenStorage.getAccessToken()
                val requestToken = response.request.header("Authorization")?.removePrefix("Bearer ")

                if (currentToken != requestToken && currentToken != null) {
                    // Token was already refreshed by another thread
                    return@runBlocking response.request.newBuilder()
                        .header("Authorization", "Bearer $currentToken")
                        .build()
                }

                // Actually refresh
                try {
                    val refreshResponse = authApi.refresh(tokenStorage.getRefreshToken()!!)
                    tokenStorage.saveTokens(refreshResponse.accessToken, refreshResponse.refreshToken)
                    response.request.newBuilder()
                        .header("Authorization", "Bearer ${refreshResponse.accessToken}")
                        .build()
                } catch (e: Exception) {
                    tokenStorage.clearTokens()
                    null // give up, will trigger 401 handling in UI
                }
            }
        }
    }
}

private val Response.retryCount: Int
    get() = generateSequence(this) { it.priorResponse }.count() - 1
```

#### iOS (Swift) — URLSession Token Refresh
```swift
class AuthenticatedAPIClient {
    private let session: URLSession
    private let tokenStorage: TokenStorage
    private var isRefreshing = false
    private var pendingRequests: [(URLRequest, CheckedContinuation<(Data, URLResponse), Error>)] = []

    func authenticatedRequest(_ request: URLRequest) async throws -> (Data, URLResponse) {
        var authedRequest = request
        if let token = tokenStorage.accessToken {
            authedRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await session.data(for: authedRequest)

        guard let httpResponse = response as? HTTPURLResponse else {
            return (data, response)
        }

        if httpResponse.statusCode == 401 {
            let newToken = try await refreshTokenIfNeeded()
            var retryRequest = request
            retryRequest.setValue("Bearer \(newToken)", forHTTPHeaderField: "Authorization")
            return try await session.data(for: retryRequest)
        }

        return (data, response)
    }

    private func refreshTokenIfNeeded() async throws -> String {
        // Coalesce concurrent refresh attempts
        // ... refresh logic
    }
}
```

### Step 4: Implement Response Parsing

#### Serialization Libraries by Platform

| Platform | Recommended | Alternative | Legacy |
|----------|-------------|------------|--------|
| **Flutter** | `json_serializable` + `freezed` | `built_value`, manual `fromJson` | — |
| **Android (Kotlin)** | `kotlinx.serialization` | Moshi | Gson |
| **Android (Java)** | Gson | Moshi, Jackson | — |
| **iOS (Swift)** | `Codable` (built-in) | — | `NSJSONSerialization` |
| **iOS (ObjC)** | `NSJSONSerialization` + manual mapping | Mantle | — |

**Flutter — freezed + json_serializable:**
```dart
@freezed
class Product with _$Product {
  const factory Product({
    required String id,
    required String name,
    required double price,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    String? imageUrl,
  }) = _Product;

  factory Product.fromJson(Map<String, dynamic> json) =>
      _$ProductFromJson(json);
}
```

**Android (Kotlin) — kotlinx.serialization:**
```kotlin
@Serializable
data class Product(
    val id: String,
    val name: String,
    val price: Double,
    @SerialName("created_at") val createdAt: String,
    @SerialName("image_url") val imageUrl: String? = null,
)
```

**iOS (Swift) — Codable:**
```swift
struct Product: Codable {
    let id: String
    let name: String
    let price: Double
    let imageUrl: String?

    enum CodingKeys: String, CodingKey {
        case id, name, price
        case imageUrl = "image_url"
    }
}

// Custom date decoding
let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601
decoder.keyDecodingStrategy = .convertFromSnakeCase
```

### Step 5: Implement Caching & Offline Support

| Strategy | Implementation | When to Use |
|----------|---------------|-------------|
| **HTTP caching (ETag/Cache-Control)** | Handled by HTTP client + server headers | Read-heavy, data changes infrequently |
| **In-memory cache** | LRU cache in repository layer | Session-scoped, frequently accessed data |
| **Database cache** | Room / Core Data / Drift with TTL | Offline-capable, structured data |
| **Offline queue** | Queue writes, sync when online | Offline-first apps, unreliable networks |

**Repository pattern with cache:**
```
API Request
  → Check in-memory cache (instant)
  → Check database cache (fast, check TTL)
  → Fetch from network (slow)
  → Update database cache
  → Update in-memory cache
  → Return data
```

**Flutter — Cache-first with Dio:**
```dart
class ProductRepository {
  final ProductApi _api;
  final ProductDao _dao;
  final Duration _cacheTTL = const Duration(minutes: 15);

  Future<List<Product>> getProducts({bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = await _dao.getAll();
      if (cached.isNotEmpty && !_isStale(cached.first.cachedAt)) {
        return cached;
      }
    }

    try {
      final products = await _api.getProducts();
      await _dao.replaceAll(products);
      return products;
    } catch (e) {
      // Fallback to cache on network error
      final cached = await _dao.getAll();
      if (cached.isNotEmpty) return cached;
      rethrow;
    }
  }
}
```

### Step 6: Handle Errors Consistently

**Error model (all platforms):**
```
NetworkError
  ├── NoConnection          → show offline banner
  ├── Timeout               → retry with backoff
  ├── ServerError (5xx)     → retry with backoff, show generic error
  ├── ClientError (4xx)
  │   ├── Unauthorized (401) → refresh token or logout
  │   ├── Forbidden (403)    → show permission error
  │   ├── NotFound (404)     → show not found
  │   └── Validation (422)   → show field-level errors
  └── ParseError            → log, show generic error
```

**Flutter:**
```dart
sealed class NetworkError {
  const NetworkError();
}
class NoConnection extends NetworkError {}
class Timeout extends NetworkError {}
class ServerError extends NetworkError { final int code; const ServerError(this.code); }
class Unauthorized extends NetworkError {}
class ValidationError extends NetworkError { final Map<String, List<String>> fields; const ValidationError(this.fields); }
class Unknown extends NetworkError { final String message; const Unknown(this.message); }

NetworkError mapDioError(DioException e) => switch (e.type) {
  DioExceptionType.connectionTimeout => const Timeout(),
  DioExceptionType.connectionError => const NoConnection(),
  _ => switch (e.response?.statusCode) {
    401 => const Unauthorized(),
    422 => ValidationError(e.response?.data['errors']),
    >= 500 => ServerError(e.response!.statusCode!),
    _ => Unknown(e.message ?? 'Unknown error'),
  },
};
```

### Step 7: WebSocket / Real-Time Connections

| Platform | Library | Use Case |
|----------|---------|----------|
| **Flutter** | `web_socket_channel`, `socket_io_client` | Chat, live updates, notifications |
| **Android** | OkHttp WebSocket, Scarlet, Ktor WebSocket | Chat, live updates, notifications |
| **iOS** | URLSessionWebSocketTask, Starscream | Chat, live updates, notifications |

**Flutter — WebSocket:**
```dart
final channel = WebSocketChannel.connect(Uri.parse('wss://api.example.com/ws'));

channel.stream.listen(
  (message) { /* handle incoming message */ },
  onError: (error) { /* reconnect with backoff */ },
  onDone: () { /* connection closed, reconnect */ },
);

channel.sink.add(jsonEncode({'type': 'subscribe', 'topic': 'orders'}));
```

## Output Format

```markdown
## Networking Architecture
- **Platform:** [Flutter / Android / iOS]
- **HTTP Client:** [Dio / Retrofit+OkHttp / URLSession / Alamofire]
- **Auth:** [Bearer JWT / OAuth2 / API key]
- **Serialization:** [freezed / kotlinx.serialization / Codable]
- **Caching:** [HTTP cache / Database / In-memory / Offline queue]

## API Layer Structure
[Class diagram or module structure]

## Token Management
[Auth flow diagram]

## Error Handling
[Error type mapping and UI behavior]

## Caching Strategy
[What is cached, TTL, invalidation]
```

## Quality Checklist

- [ ] HTTP client is configured with timeouts (connect, read, write)
- [ ] Auth token refresh handles concurrent requests (no race conditions)
- [ ] Certificate pinning is configured (see `/mobile-security`)
- [ ] Error responses are mapped to domain error types (not raw HTTP errors in UI)
- [ ] Network calls are NOT on the main thread
- [ ] Logging is enabled in debug, disabled in release
- [ ] Retry logic uses exponential backoff with jitter
- [ ] Request cancellation is handled (screen dismissed, search debounced)
- [ ] File uploads show progress
- [ ] Offline fallback returns cached data when network fails

## Edge Cases

- Token refresh race condition: multiple concurrent 401s should coalesce into a single refresh, not multiple
- Large response bodies should be streamed, not loaded entirely into memory
- Untrusted server certificates in development: use a debug-only network config, never disable SSL in production
- GraphQL error responses return 200 with errors in the body — check `data.errors` even on 200
- WebSocket reconnection needs exponential backoff to avoid thundering herd on server recovery
- On Android, `Dispatchers.IO` is limited to 64 threads — for many concurrent requests, use a custom dispatcher
- On iOS, URLSession background sessions continue uploads/downloads when the app is suspended
