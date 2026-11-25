---
name: swift-networking
description: Builds a protocol-based async/await networking layer with URLSession, testable abstractions, error handling, and mock support for Swift projects. Use when user says "add networking", "create an API layer", "fetch data from API", "build a network service", "add URLSession", "implement HTTP requests", "create a REST client", or "set up API calls".
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# Swift Networking Layer

## Instructions

### Step 1: Clarify Requirements

Ask if not already provided:
- Base URL (can be a placeholder constant)
- Authentication method: Bearer token, API key in header, OAuth, none
- Endpoints to implement upfront (or start with the pattern only)
- Response format: JSON (assumed), XML, or other
- Error handling needs: retry logic, token refresh, offline support

### Step 2: Generate the Core Layer

Generate in `Services/Networking/`:

**HTTPClientProtocol — the testability key:**
```swift
// Services/Networking/HTTPClientProtocol.swift
import Foundation

protocol HTTPClientProtocol {
    func data(for request: URLRequest) async throws -> (Data, URLResponse)
}

// URLSession conforms for free — no wrapper needed
extension URLSession: HTTPClientProtocol {}
```

**APIError:**
```swift
// Services/Networking/APIError.swift
import Foundation

enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse(statusCode: Int)
    case decodingError(Error)
    case unauthorized
    case noInternetConnection
    case unknown(Error)

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL."
        case .invalidResponse(let code): return "Server error (\(code))."
        case .decodingError: return "Failed to parse server response."
        case .unauthorized: return "You are not authorized. Please log in again."
        case .noInternetConnection: return "No internet connection."
        case .unknown(let error): return error.localizedDescription
        }
    }
}
```

**Endpoint — type-safe request building:**
```swift
// Services/Networking/Endpoint.swift
import Foundation

struct Endpoint {
    let path: String
    let method: HTTPMethod
    let queryItems: [URLQueryItem]?
    let body: Encodable?
    let headers: [String: String]

    init(
        path: String,
        method: HTTPMethod = .get,
        queryItems: [URLQueryItem]? = nil,
        body: Encodable? = nil,
        headers: [String: String] = [:]
    ) {
        self.path = path
        self.method = method
        self.queryItems = queryItems
        self.body = body
        self.headers = headers
    }

    func urlRequest(baseURL: URL, authToken: String? = nil) throws -> URLRequest {
        var components = URLComponents(url: baseURL.appendingPathComponent(path), resolvingAgainstBaseURL: true)
        components?.queryItems = queryItems

        guard let url = components?.url else { throw APIError.invalidURL }

        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if let token = authToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        headers.forEach { request.setValue($1, forHTTPHeaderField: $0) }

        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }

        return request
    }
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
}
```

**APIClient:**
```swift
// Services/Networking/APIClient.swift
import Foundation

final class APIClient {
    private let httpClient: HTTPClientProtocol
    private let baseURL: URL
    private let decoder: JSONDecoder

    init(
        httpClient: HTTPClientProtocol = URLSession.shared,
        baseURL: URL
    ) {
        self.httpClient = httpClient
        self.baseURL = baseURL
        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder.dateDecodingStrategy = .iso8601
    }

    func fetch<T: Decodable>(_ endpoint: Endpoint, authToken: String? = nil) async throws -> T {
        let request = try endpoint.urlRequest(baseURL: baseURL, authToken: authToken)
        let (data, response) = try await httpClient.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse(statusCode: -1)
        }

        switch httpResponse.statusCode {
        case 200...299:
            do {
                return try decoder.decode(T.self, from: data)
            } catch {
                throw APIError.decodingError(error)
            }
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.invalidResponse(statusCode: httpResponse.statusCode)
        }
    }

    func send(_ endpoint: Endpoint, authToken: String? = nil) async throws {
        let request = try endpoint.urlRequest(baseURL: baseURL, authToken: authToken)
        let (_, response) = try await httpClient.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse(statusCode: (response as? HTTPURLResponse)?.statusCode ?? -1)
        }
    }
}
```

### Step 3: Generate a Repository (Service Layer)

ViewModels should never call `APIClient` directly — wrap it in a repository:

```swift
// Services/Networking/UserRepository.swift
import Foundation

protocol UserRepositoryProtocol {
    func fetchUsers() async throws -> [User]
    func fetchUser(id: String) async throws -> User
}

final class UserRepository: UserRepositoryProtocol {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func fetchUsers() async throws -> [User] {
        try await apiClient.fetch(Endpoint(path: "/users"))
    }

    func fetchUser(id: String) async throws -> User {
        try await apiClient.fetch(Endpoint(path: "/users/\(id)"))
    }
}
```

### Step 4: Generate Mock for Testing

```swift
// Always generate alongside the real implementation
final class MockHTTPClient: HTTPClientProtocol {
    var stubbedData: Data = Data()
    var stubbedResponse: URLResponse = HTTPURLResponse(
        url: URL(string: "https://example.com")!,
        statusCode: 200,
        httpVersion: nil,
        headerFields: nil
    )!
    var stubbedError: Error?
    private(set) var requestsMade: [URLRequest] = []

    func data(for request: URLRequest) async throws -> (Data, URLResponse) {
        requestsMade.append(request)
        if let error = stubbedError { throw error }
        return (stubbedData, stubbedResponse)
    }
}

final class MockUserRepository: UserRepositoryProtocol {
    var stubbedUsers: [User] = []
    var stubbedError: Error?

    func fetchUsers() async throws -> [User] {
        if let error = stubbedError { throw error }
        return stubbedUsers
    }

    func fetchUser(id: String) async throws -> User {
        if let error = stubbedError { throw error }
        return stubbedUsers.first { $0.id == id } ?? stubbedUsers[0]
    }
}
```

### Step 5: Quality Checklist

- [ ] `URLSession` is hidden behind `HTTPClientProtocol` — never used directly in business code
- [ ] ViewModels depend on repository protocols, not on `APIClient` directly
- [ ] `APIError` is exhaustive and has user-readable descriptions
- [ ] JSON decoding uses `convertFromSnakeCase` (or explicit `CodingKeys`)
- [ ] Base URL is a constant — not hardcoded as a string literal in call sites
- [ ] `MockHTTPClient` and `Mock[X]Repository` are generated alongside the real types
- [ ] No network calls anywhere in the View layer

## Examples

### Example 1: REST API with auth

User says: "Add networking to fetch a list of products from our REST API at api.myapp.com"

Files generated:
- `HTTPClientProtocol.swift`
- `APIError.swift`
- `Endpoint.swift`
- `APIClient.swift`
- `ProductRepository.swift` + `ProductRepositoryProtocol`
- `MockHTTPClient.swift`
- `MockProductRepository.swift`

### Example 2: Adding a new endpoint

User says: "Add an endpoint to POST a new order"

Actions:
1. Add `createOrder(body: OrderRequest)` to the endpoint enum or repository
2. Add the method to `OrderRepositoryProtocol` and `OrderRepository`
3. Update `MockOrderRepository`

## Troubleshooting

**Decoding fails silently**: Add error logging in the `catch` block of `fetch()`. Print the raw JSON string for debugging: `String(data: data, encoding: .utf8)`.

**401 errors in tests**: `MockHTTPClient` is returning the wrong status code. Set `stubbedResponse` with `statusCode: 200` explicitly.

**Tests are hitting real network**: `URLSession.shared` is still used directly somewhere. Verify the `APIClient` is initialized with `MockHTTPClient` in tests.
