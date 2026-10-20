---
name: performance-audit
description: Detect performance issues, N+1 queries, allocations in loops, blocking calls
globs: ["**/*.cs", "**/*.ts", "**/*.sql"]
alwaysApply: false
---

# Performance Audit

Identify and prevent performance bottlenecks. Profile before optimizing. Favor set-based operations, async patterns, and efficient algorithms.

## SQL Performance

**ALWAYS**:
- Use parameterised queries (prepared statements)
- SELECT specific columns, never SELECT *
- Add indexes on foreign keys and WHERE clause columns
- Use WITH (NOLOCK) on read-heavy SELECT statements
- Replace cursors with set-based operations (INSERT...SELECT, UPDATE...FROM)
- Replace CTEs with temp tables for queries processing > 10k rows
- Make WHERE clauses SARGable (no functions wrapping columns)

**NEVER**:
- N+1 queries (loop that queries in each iteration)
- String concatenation for SQL (always parameterised)
- Cursors for data processing
- SELECT * in production queries
- Subqueries without understanding execution plan
- Missing indexes on frequently-searched columns

### ✅ GOOD Example
```sql
-- Efficient: specific columns, indexed WHERE, set-based JOIN
SELECT u.Id, u.Name, COUNT(o.Id) AS OrderCount
FROM Users u
LEFT JOIN Orders o ON u.Id = o.UserId
WHERE u.Status = 'Active'
  AND u.CreatedDate > DATEADD(MONTH, -6, GETDATE())
GROUP BY u.Id, u.Name
ORDER BY OrderCount DESC

-- Create covering index for this query
CREATE INDEX IX_Users_Status_CreatedDate 
  ON Users(Status, CreatedDate) 
  INCLUDE (Id, Name)
```

### ❌ BAD Example
```sql
-- Inefficient: N+1, SELECT *, no indexes
FOR @userId IN (SELECT Id FROM Users)
BEGIN
  SELECT * FROM Orders WHERE UserId = @userId
  DECLARE @total = SELECT SUM(Amount) FROM Orders WHERE UserId = @userId
  -- Processing logic here (N+1 problem)
END
```

---

## C# Performance

**ALWAYS**:
- Async/await with ConfigureAwait(false) in libraries
- Use Span<T> for performance-critical buffer operations
- Pre-allocate collections when size is known (new List<T>(capacity))
- Use StringBuilder for string concatenation in loops
- Cache Regex objects (static readonly)
- Minimize allocations in tight loops
- Use object pooling for frequently-allocated objects

**NEVER**:
- Thread.Sleep in async code (use Task.Delay)
- Blocking on async (.Result, .Wait())
- LINQ in tight loops (use foreach)
- Repeated string concatenation (use StringBuilder)
- Large array allocations in loops
- Unnecessary LINQ chains (single-pass when possible)

### ✅ GOOD Example
```csharp
// Efficient: pre-allocated, StringBuilder, async
public async Task<string> ProcessLargeDataAsync(IEnumerable<string> items, CancellationToken ct)
{
  var sb = new StringBuilder(capacity: 1000);
  foreach (var item in items)
  {
    sb.Append(item);
    sb.Append(',');
    // Do NOT allocate in loop
  }
  
  // Single async call, not per-item
  var result = await _repository.SaveAsync(sb.ToString(), ct).ConfigureAwait(false);
  return result;
}

// Cache the compiled Regex
private static readonly Regex EmailPattern = new Regex(@"^[^@\s]+@[^@\s]+\.[^@\s]+$", RegexOptions.Compiled);
```

### ❌ BAD Example
```csharp
// Inefficient: allocations in loop, blocking async
public string ProcessLargeData(IEnumerable<string> items)
{
  var result = "";
  foreach (var item in items)
  {
    result += item + ","; // String allocation per iteration
  }
  
  // N+1: one SaveAsync per item
  foreach (var item in items)
  {
    _repository.SaveAsync(item).Wait(); // Blocking! Dead-lock risk
  }
  
  return result;
}
```

---

## TypeScript Performance

**ALWAYS**:
- Lazy-load modules using dynamic imports
- Use ChangeDetectionStrategy.OnPush (Angular)
- Prefer signals over BehaviorSubject for local state
- Memoize expensive computations (@computed in signals)
- Use trackBy in *ngFor
- Unsubscribe or use takeUntilDestroyed()
- Code-split at route boundaries

**NEVER**:
- Subscribe to multiple observables without merging (use combineLatest, merge, concat)
- Forget unsubscribe (memory leak + performance)
- Change detection strategy.Default with frequent updates
- Large bundle size without code-splitting
- Global state mutation without memoization
- Synchronous heavy computations in templates

### ✅ GOOD Example
```typescript
// Efficient: lazy load, OnPush, signals, tracked iteration
import { Component, ChangeDetectionStrategy, input, signal, computed } from '@angular/core';

@Component({
  selector: 'app-orders',
  template: `
    <div *ngFor="let order of filteredOrders(); trackBy: trackById">
      {{ order.id }} - {{ order.total }}
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrdersComponent {
  orders = input<Order[]>([]);
  filter = signal('');
  
  // Memoized computation
  filteredOrders = computed(() =>
    this.orders().filter(o => o.status.includes(this.filter()))
  );
  
  trackById(index: number, item: Order) { return item.id; }
}

// Lazy-load heavy modules
const adminModule = () => import('./admin/admin.module').then(m => m.AdminModule);
```

### ❌ BAD Example
```typescript
// Inefficient: no lazy load, Default detection, BehaviorSubject, no trackBy
@Component({
  selector: 'app-orders',
  template: `
    <div *ngFor="let order of orders$ | async">
      {{ order.id }} - {{ getTotal(order) }}  <!-- Recalculated on every render -->
    </div>
  `
})
export class OrdersComponent {
  orders$ = new BehaviorSubject<Order[]>([]);
  
  ngOnInit() {
    this.orders$.subscribe(/* handling */); // No takeUntilDestroyed
  }
  
  getTotal(order: Order) {
    return order.items.reduce((sum, i) => sum + i.price, 0); // Heavy computation in template
  }
}

// No lazy-load
import { AdminModule } from './admin/admin.module';
```

---

## General Performance

**Profile Before Optimizing**:
- Use browser DevTools, dotnet-trace, SQL Profiler
- Measure actual bottlenecks
- Don't optimize guesses
- Benchmark before/after with realistic data

**Cache Strategically**:
- In-memory cache for frequently-accessed, rarely-changing data
- Redis for distributed caching
- HTTP caching headers for API responses
- Never cache security-sensitive data

**Rate Limit & Throttle**:
- API rate limiting (per user, per IP)
- Database connection pooling
- Request throttling for UI updates (debounce, throttle)

---

## Performance Checklist

- [ ] No N+1 queries in application code
- [ ] Indexes on foreign keys and WHERE columns
- [ ] Parameterised queries (no string concatenation)
- [ ] No blocking .Result / .Wait() in async code
- [ ] Allocations outside of tight loops
- [ ] Async/await with ConfigureAwait(false)
- [ ] Lazy-loaded modules and code-splitting
- [ ] ChangeDetectionStrategy.OnPush (Angular)
- [ ] trackBy in loops
- [ ] Profile before optimizing (measure actual bottlenecks)
