---
name: performance-budget
description: Performance budgets — response time targets, bundle size limits, database query budgets, caching strategy
globs: ["**/*.cs", "**/*.ts", "**/*.sql"]
alwaysApply: false
---

# Performance Budget

Every application has a performance budget. Define and monitor: API response time, bundle size, database query time, and concurrent connection limits.

## Performance Targets (Baseline)

### API Response Times

| Scenario | Target | Percentile | Action |
|----------|--------|-----------|--------|
| **Fast endpoint** (GET status, cache hit) | < 50ms | P95 | Immediate response |
| **Normal endpoint** (GET data, single DB query) | < 200ms | P95 | 1 query, cached |
| **Complex endpoint** (multiple queries, external API) | < 500ms | P95 | Max 5 DB calls, timeout fallback |
| **Batch endpoint** (POST 100+ items) | < 2s | P95 | Async processing, queue |

**P95**: 95th percentile. 95% of requests must be faster than target. 5% slower is acceptable for outliers.

### Web Bundle Size

| Type | Target | Notes |
|------|--------|-------|
| **Initial HTML** | < 50KB | Gzipped |
| **JavaScript (main)** | < 250KB | Gzipped, code-split |
| **JavaScript (vendor)** | < 200KB | Gzipped, node_modules |
| **CSS (critical)** | < 30KB | Inline critical, defer rest |
| **Images** | < 1MB | Total for page, compressed |
| **Total Page Load** | < 1.5MB | All assets, gzipped |

**Rule of thumb**: Each 1MB delay = 7% abandonment increase (mobile especially).

### Database Query Budget

| Scenario | Budget | Notes |
|----------|--------|-------|
| **Single record fetch** | < 10ms | Should hit index or cache |
| **List query** (0-100 items) | < 100ms | Pagination required, no SELECT * |
| **Aggregation** (COUNT, SUM, GROUP BY) | < 200ms | On indexed columns only |
| **Join query** (2-3 tables) | < 100ms | Should use indexes on FK |
| **N+1 queries** | **NOT ALLOWED** | Batch load or JOINs required |
| **Max DB calls per request** | **≤ 5** | Reduce with caching, batching |

---

## Bundle Size Targets (TypeScript/Angular)

**ALWAYS**:
- Measure gzipped bundle size (what users download)
- Set bundle budgets in `angular.json` or `webpack.config.js`
- Code-split lazy routes (separate chunks for feature modules)
- Tree-shake unused code (use ES6 imports, not CommonJS)
- Defer non-critical CSS and scripts
- Lazy-load images (use `loading="lazy"` or Intersection Observer)
- Compress images (WebP, AVIF with fallback)

**NEVER**:
- Bundle all libraries eagerly
- Include `console.log()` in production (dead code)
- Ship unminified code to production
- Load jQuery or lodash when native alternatives exist
- Use `*ngIf` for routes instead of lazy-loading modules
- Import entire libraries when using 1-2 functions

### ✅ GOOD Bundle Strategy (Angular)
```json
{
  "projects": {
    "app": {
      "architect": {
        "build": {
          "options": {
            "budgets": [
              {
                "type": "bundle",
                "name": "main",
                "baseline": "250kb",
                "maximumWarning": "270kb",
                "maximumError": "300kb"
              },
              {
                "type": "bundle",
                "name": "polyfills",
                "baseline": "50kb",
                "maximumWarning": "60kb",
                "maximumError": "75kb"
              },
              {
                "type": "initial",
                "maximumWarning": "500kb",
                "maximumError": "750kb"
              }
            ],
            "aot": true,
            "optimization": true,
            "sourceMap": false,
            "namedChunks": false
          }
        }
      }
    }
  }
}
```

### ✅ GOOD Code Splitting (Angular Router)
```typescript
// Lazy-load feature modules
const routes: Routes = [
  {
    path: 'dashboard',
    loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule)
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule)
  },
  // Dynamic imports create separate chunks
];
```

### ✅ GOOD Image Optimization (HTML)
```html
<!-- Modern image formats with fallback -->
<picture>
  <source srcset="hero.webp" type="image/webp">
  <source srcset="hero.jpg" type="image/jpeg">
  <img src="hero.jpg" alt="Hero image" loading="lazy" width="800" height="400">
</picture>

<!-- Lazy-load offscreen images -->
<img 
  src="image.jpg" 
  alt="Product" 
  loading="lazy"
  width="300"
  height="300"
>
```

### ❌ BAD Bundle
```typescript
// Bundling everything eagerly
import * as lodash from 'lodash';  // 70KB unused library

// All routes loaded upfront
const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'admin', component: AdminComponent },
  // No lazy loading = single 1MB bundle
];

// Unminified code in production
// console.log() calls left in code
// jQuery included but not used
```

---

## Database Query Budget (C#/SQL)

**ALWAYS**:
- Use `SELECT col1, col2` not `SELECT *`
- Use indexes on WHERE, JOIN, and ORDER BY columns
- Batch queries: `GetUsersByIds(new[] { 1, 2, 3 })` not loop with N+1
- Use `LIMIT` / `OFFSET` for pagination
- Profile slow queries (> 100ms) with SQL Server Profiler or `EXPLAIN ANALYZE`
- Cache frequently accessed data (user profiles, settings)
- Set query timeout: 30s default, 5s for critical endpoints

**NEVER**:
- `SELECT *` (specify columns)
- N+1 queries (loop fetching 1 by 1)
- Queries without indexes on filtered columns
- Unbounded result sets (no LIMIT/OFFSET)
- Left outer joins on lookup tables (use INNER for lookups)
- Queries without a query plan analysis

### ✅ GOOD Query Design (C#)
```csharp
// ❌ BAD: N+1 queries
public async Task<List<OrderWithItems>> GetOrders()
{
    var orders = await db.Orders.ToListAsync();  // Query 1
    foreach (var order in orders)
    {
        order.Items = await db.OrderItems
            .Where(i => i.OrderId == order.Id)
            .ToListAsync();  // Query N
    }
    return orders;
}

// ✅ GOOD: Batch load with Include
public async Task<List<OrderWithItems>> GetOrders()
{
    return await db.Orders
        .Include(o => o.Items)  // Single query with JOIN
        .ToListAsync();
}

// ✅ GOOD: Batch load by IDs
public async Task<List<User>> GetUsersByIds(int[] userIds)
{
    return await db.Users
        .Where(u => userIds.Contains(u.Id))
        .ToListAsync();  // WHERE id IN (...) — indexed
}

// ✅ GOOD: Paginated query
public async Task<PaginatedResult<User>> GetUsers(int page, int pageSize = 20)
{
    var skip = (page - 1) * pageSize;
    var total = await db.Users.CountAsync();
    var users = await db.Users
        .OrderBy(u => u.Name)
        .Skip(skip)
        .Take(pageSize)
        .ToListAsync();
    return new PaginatedResult<User> { Items = users, Total = total };
}

// ✅ GOOD: Cached query
public async Task<User?> GetUserCached(int userId, IMemoryCache cache)
{
    var cacheKey = $"user_{userId}";
    if (cache.TryGetValue(cacheKey, out User? cachedUser))
    {
        return cachedUser;
    }

    var user = await db.Users.FirstOrDefaultAsync(u => u.Id == userId);
    cache.Set(cacheKey, user, TimeSpan.FromMinutes(15));
    return user;
}
```

### ✅ GOOD Query with Index (SQL)
```sql
-- Create indexes on frequently filtered columns
CREATE INDEX idx_users_email ON Users(Email);
CREATE INDEX idx_orders_user_id ON Orders(UserId);
CREATE INDEX idx_order_items_order_id ON OrderItems(OrderId);

-- Good query: uses indexes
SELECT u.Id, u.Name, COUNT(o.Id) as OrderCount
FROM Users u
LEFT JOIN Orders o ON u.Id = o.UserId
WHERE u.Email = 'alice@example.com'  -- Indexed
GROUP BY u.Id, u.Name;

-- Bad query: no index on Age
SELECT * FROM Users WHERE Age > 25;  -- Slow, full table scan

-- Bad query: SELECT *
SELECT * FROM Orders WHERE UserId = 123;  -- Might return 100 columns you don't need
```

---

## Caching Strategy

**Cache Layer 1: Application (Memory)**
- Hot data (user settings, feature flags)
- TTL: 5-15 minutes
- Size limit: Monitor memory usage
- Invalidation: On-demand (settings change)

**Cache Layer 2: Distributed (Redis)**
- Session data, API responses
- TTL: 15-60 minutes
- Shared across server instances
- Invalidation: Pattern-based or TTL

**Cache Layer 3: HTTP Cache**
- Static assets (CSS, JS, images)
- TTL: 24 hours to 1 year
- Browser caches locally
- Set `Cache-Control` and `ETag` headers

**Cache Layer 4: Database Query Cache**
- Don't cache everything (only read-heavy queries)
- Use materialized views for aggregations
- Periodic refresh (async job)

### ✅ GOOD Caching (C# ASP.NET Core)
```csharp
// Memory cache for hot data
public class UserService
{
    private readonly IMemoryCache _cache;
    private const string UserCacheKeyFormat = "user_{0}";

    public UserService(IMemoryCache cache)
    {
        _cache = cache;
    }

    public async Task<User?> GetUserAsync(int userId)
    {
        var cacheKey = string.Format(UserCacheKeyFormat, userId);

        if (_cache.TryGetValue(cacheKey, out User? cachedUser))
        {
            return cachedUser;
        }

        var user = await db.Users.FirstOrDefaultAsync(u => u.Id == userId);
        if (user != null)
        {
            _cache.Set(cacheKey, user, TimeSpan.FromMinutes(15));
        }

        return user;
    }
}

// HTTP cache headers
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet("{id}")]
    [ResponseCache(Duration = 300, Location = ResponseCacheLocation.Any)]  // Cache 5 minutes
    public async Task<Product> GetProduct(int id)
    {
        return await db.Products.FirstAsync(p => p.Id == id);
    }

    [HttpGet]
    public async Task<List<Product>> GetProducts()
    {
        // Don't cache mutable data
        return await db.Products.ToListAsync();
    }
}
```

---

## Performance Monitoring

**Monitor these metrics**:
- API response time (P50, P95, P99)
- Error rate (5xx, timeouts)
- Database query time
- Cache hit rate
- Memory usage
- CPU usage
- Concurrent users/requests

**Tools**:
- Application Insights (Azure)
- Datadog
- New Relic
- Prometheus + Grafana (self-hosted)
- ELK Stack (Elasticsearch, Logstash, Kibana)

### ✅ GOOD Instrumentation (C#)
```csharp
// Structured logging with timing
public async Task<User?> GetUserAsync(int userId, ILogger<UserService> logger)
{
    var stopwatch = Stopwatch.StartNew();
    try
    {
        var user = await db.Users.FirstOrDefaultAsync(u => u.Id == userId);
        stopwatch.Stop();

        logger.LogInformation(
            "GetUser completed in {ElapsedMs}ms. UserId={UserId}. Found={Found}",
            stopwatch.ElapsedMilliseconds,
            userId,
            user != null
        );

        return user;
    }
    catch (Exception ex)
    {
        stopwatch.Stop();
        logger.LogError(
            ex,
            "GetUser failed after {ElapsedMs}ms. UserId={UserId}",
            stopwatch.ElapsedMilliseconds,
            userId
        );
        throw;
    }
}
```

---

## Performance Budget Checklist

- [ ] API response time targets defined (< 200ms P95)
- [ ] Bundle size budget set (main < 250KB gzipped)
- [ ] Database query budget defined (max 5 queries per request)
- [ ] No N+1 queries in critical paths
- [ ] Slow queries identified and optimized (> 100ms logged)
- [ ] Indexes created on WHERE, JOIN, ORDER BY columns
- [ ] Caching strategy implemented (memory + distributed)
- [ ] Images optimized (WebP/AVIF, lazy-loaded)
- [ ] Code-splitting enabled for large bundles
- [ ] Performance metrics monitored (APM tool)
- [ ] Slow requests alarmed (> 1s for normal endpoints)
- [ ] Bundle size monitored on every build
