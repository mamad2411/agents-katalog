---
name: async-best-practices
description: Async/await patterns, ConfigureAwait, CancellationToken, no blocking calls
globs: ["**/*.cs", "**/*.ts"]
alwaysApply: false
---

# Async Best Practices

Use async/await properly. Never block on async. Propagate CancellationToken everywhere. ConfigureAwait(false) in libraries.

## C# Async Rules

**ALWAYS**:
- Use `async/await` — never `Task.Run()` as a general solution
- Add `CancellationToken` parameter to all async methods (except event handlers)
- Use `ConfigureAwait(false)` in libraries (frees UI thread)
- `Task<T>` for operations that return data
- `Task` or `ValueTask` for fire-and-forget only with proper error handling
- Propagate `CancellationToken` through the call chain
- Use `Task.Delay()` instead of `Thread.Sleep()` in async code
- Prefix async methods with `Async` suffix

**NEVER**:
- `.Result`, `.Wait()` — causes deadlocks and blocks threads
- `GetAwaiter().GetResult()` as a workaround
- `Task.Run()` for simple I/O-bound operations
- Mix synchronous and asynchronous code
- Catch `OperationCanceledException` without understanding it
- Call sync methods from async context
- Ignore cancellation tokens in long-running operations
- Fire-and-forget tasks without error handling

### ✅ GOOD Example
```csharp
// Proper async method with CancellationToken
public async Task<UserProfile> GetUserAsync(int userId, CancellationToken ct)
{
  // Propagate CT to database call
  var user = await _userRepository.GetUserAsync(userId, ct).ConfigureAwait(false);
  if (user == null)
    return null;
  
  // Propagate CT to dependent calls
  var profile = await _profileService.BuildProfileAsync(user, ct).ConfigureAwait(false);
  return profile;
}

// Service method accepting and using CT
public class UserRepository
{
  public async Task<User> GetUserAsync(int id, CancellationToken ct)
  {
    using var context = new UserDbContext();
    // Pass CT to database operation
    return await context.Users.FirstOrDefaultAsync(u => u.Id == id, ct);
  }
}

// Calling async method correctly
public async Task ProcessOrderAsync(Order order, CancellationToken ct)
{
  try
  {
    var profile = await GetUserAsync(order.UserId, ct); // Pass CT down
    // Use profile
  }
  catch (OperationCanceledException)
  {
    // Operation was cancelled - log and handle gracefully
    _logger.LogInformation("Order processing cancelled");
  }
}

// ConfigureAwait in libraries
public static class LibraryService
{
  public static async Task<Data> FetchDataAsync(CancellationToken ct)
  {
    // ConfigureAwait(false) so library doesn't capture UI context
    var result = await _httpClient.GetAsync("url", ct).ConfigureAwait(false);
    return await result.Content.ReadAsAsync<Data>(ct).ConfigureAwait(false);
  }
}
```

### ❌ BAD Example
```csharp
// Blocking on async - DEADLOCK RISK
public UserProfile GetUser(int userId)
{
  var user = _userRepository.GetUserAsync(userId).Result; // BLOCKS!
  return user;
}

// No CancellationToken
public async Task FetchUserAsync(int id)
{
  var user = await _userRepository.GetUserAsync(id);
  // No way to cancel this operation
}

// No ConfigureAwait in library
public static async Task<Data> FetchDataAsync()
{
  var result = await _httpClient.GetAsync("url"); // Captures UI context
  // Could deadlock in ASP.NET Core
}

// Fire-and-forget with no error handling
public void ProcessOrder(Order order)
{
  _ = ProcessOrderAsync(order); // No await, errors ignored!
}

// Mixing sync and async
public async Task ProcessAsync()
{
  var data = GetDataAsync().Result; // Anti-pattern
  await SaveAsync(data);
}

// Thread.Sleep in async code
public async Task CheckStatusAsync()
{
  while (true)
  {
    var status = await GetStatusAsync();
    Thread.Sleep(1000); // Blocks thread for no reason!
  }
}
```

---

## TypeScript Async Rules

**ALWAYS**:
- `async/await` for Promise-based operations
- `await` every Promise (or `.then()` chain properly)
- Handle rejection with `try/catch` or `.catch()`
- `takeUntilDestroyed()` to unsubscribe from observables (Angular)
- `subject.complete()` in ngOnDestroy if using Subject
- Pass `signal` or `computed` for reactive state (not Promises in UI)

**NEVER**:
- `.subscribe()` without unsubscribe
- Forget `await` on async operations
- Ignore Promise rejections
- Use `setTimeout` for async operations (use async/await instead)
- Mix Promises and Observables without converting
- Call `.toPromise()` then `.subscribe()` (pick one pattern)

### ✅ GOOD Example
```typescript
// Proper async/await with error handling
export class UserService {
  constructor(private http: HttpClient) {}
  
  async getUserAsync(id: number): Promise<User> {
    try {
      const response = await this.http.get<User>(`/api/users/${id}`).toPromise();
      return response;
    } catch (error) {
      console.error('Failed to fetch user:', error);
      throw error;
    }
  }
}

// Angular component with Observable
@Component({
  selector: 'app-user',
  template: `<div>{{ user$ | async }}</div>`
})
export class UserComponent implements OnInit {
  user$ = this.userService.getUser(id);
  
  constructor(private userService: UserService) {}
  
  ngOnInit() {
    // Observable handled by async pipe - no manual subscription
  }
  
  ngOnDestroy() {
    // No need to unsubscribe - async pipe handles it
  }
}

// New signal-based pattern (Angular 17+)
export class UserComponent {
  userId = input<number>();
  userService = inject(UserService);
  
  user = toSignal(
    this.userId.pipe(
      switchMap(id => this.userService.getUser(id)),
      takeUntilDestroyed()
    ),
    { initialValue: null }
  );
}
```

### ❌ BAD Example
```typescript
// Forgot await - Promise not resolved
async function processUser(id: number) {
  const user = getUserAsync(id); // Forgot await!
  console.log(user.name); // user is Promise, not User
}

// No unsubscribe - memory leak
export class UserComponent implements OnInit {
  ngOnInit() {
    this.userService.getUser(id).subscribe(user => {
      this.user = user;
      // No unsubscribe() in ngOnDestroy
    });
  }
}

// Unhandled rejection
async function load() {
  const user = await getUser(id); // If rejects, promise rejection goes uncaught
}

// Mix Promises and Observables poorly
const data = this.http.get('/api/users')
  .toPromise()
  .then(users => {
    // Process users
  })
  .subscribe(/* wrong - Promise doesn't have subscribe */);

// setTimeout instead of async/await
setTimeout(async () => {
  const result = await someAsync();
}, 1000); // Awkward - use async/await with delay instead
```

---

## CancellationToken Pattern (C#)

**ALWAYS**:
- Add `CancellationToken ct = default` to all async methods
- Pass token to child async calls
- Check token in loops: `ct.ThrowIfCancellationRequested()`
- Handle `OperationCanceledException` appropriately

**NEVER**:
- Catch and ignore OperationCanceledException (it's intentional)
- Create long-running loops without checking cancellation
- Ignore CancellationToken in business logic

### ✅ GOOD Example
```csharp
public async Task ProcessListAsync(List<Item> items, CancellationToken ct)
{
  foreach (var item in items)
  {
    // Check cancellation in loop
    ct.ThrowIfCancellationRequested();
    
    // Process item with CT
    await ProcessItemAsync(item, ct).ConfigureAwait(false);
  }
}

// In controller (ASP.NET Core provides CT automatically)
[HttpPost("process")]
public async Task<IActionResult> ProcessAsync([FromBody] ProcessRequest req, CancellationToken ct)
{
  await _service.ProcessAsync(req, ct);
  return Ok();
}

// Timeout with CancellationToken
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
try
{
  await LongRunningOperationAsync(cts.Token);
}
catch (OperationCanceledException)
{
  _logger.LogWarning("Operation timed out after 30 seconds");
}
```

---

## Async Checklist

- [ ] All async methods have `async` keyword
- [ ] All async method names end with `Async`
- [ ] `CancellationToken ct` parameter on all async methods
- [ ] CancellationToken propagated to child async calls
- [ ] `ConfigureAwait(false)` in libraries
- [ ] No `.Result` or `.Wait()` calls
- [ ] `try/catch` around `await` or `.catch()` on Promises
- [ ] No fire-and-forget tasks without error handling
- [ ] Observable subscriptions have unsubscribe
- [ ] `async/await` preferred over Task.Run()
- [ ] `Task.Delay()` instead of Thread.Sleep in async
