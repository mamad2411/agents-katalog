---
name: laravel-performance
description: "Tối ưu hóa hiệu suất Laravel toàn diện theo chuẩn doanh nghiệp lớn (Enterprise)."
version: 1.0
impact-driven: true
priority-order: CRITICAL → HIGH → MEDIUM → LOW
stack: Laravel, PHP, Eloquent
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Laravel Performance Optimization

> Production-grade performance rules for Laravel, prioritized by real-world impact.

---

## 🎯 CORE PHILOSOPHY

### The Problem With Traditional Advice

Most Laravel performance advice is **not prioritized**:
- "Use cache"
- "Optimize queries"
- "Use queues"

**Result:** Developers waste time optimizing the wrong things.

### The Impact-Driven Approach

> **Fix N+1 queries (600ms → 100ms) BEFORE micro-optimizing array loops (2ms → 1ms)**

**Ordering matters:**

```
🔴 CRITICAL (5-20× improvement)     ← Fix FIRST
├── Eliminate N+1 Queries
├── Add Missing Database Indexes
└── Implement Query Result Caching

🟠 HIGH (Significant gains)         ← Fix SECOND
├── Optimize Eager Loading Strategy
├── Reduce Database Connection Overhead
└── Implement Response Caching

🟡 MEDIUM (Moderate gains)          ← Fix THIRD
├── Optimize Collection Operations
├── Reduce Memory Usage
└── Implement Job Queues

🟢 LOW (Incremental)                ← Fix LAST
├── Code-level micro-optimizations
└── Config tuning
```

---

## 📚 OPTIMIZATION CATEGORIES

### 1. Eliminating N+1 Queries (CRITICAL)

**Impact:** 5-20× improvement

#### Rule 1.1: Always Eager Load Relationships

**❌ Bad: N+1 Query Problem**
```php
// Fetches users: 1 query
$users = User::all();

// For EACH user, fetches posts: N queries
foreach ($users as $user) {
    echo $user->posts->count(); // N+1!
}
// Total: 1 + N queries (101 queries for 100 users)
```

**✅ Good: Eager Loading**
```php
// Single query with JOIN
$users = User::with('posts')->get();

foreach ($users as $user) {
    echo $user->posts->count(); // No additional query
}
// Total: 1-2 queries (depending on relationship type)
```

**Impact:** 600ms → 100ms (6× faster)

---

#### Rule 1.2: Use `withCount()` for Relationship Counts

**❌ Bad: Loading Full Relationships for Counting**
```php
$users = User::with('posts')->get();

foreach ($users as $user) {
    echo $user->posts->count(); // Loads all posts into memory!
}
```

**✅ Good: Only Count, Don't Load**
```php
$users = User::withCount('posts')->get();

foreach ($users as $user) {
    echo $user->posts_count; // No memory overhead
}
```

**Impact:** 80% less memory, 3× faster

---

#### Rule 1.3: Detect N+1 with Laravel Debugbar/Telescope

**Profiling First (MANDATORY):**
```bash
# Install Debugbar
composer require barryvdh/laravel-debugbar --dev

# Or use Telescope
php artisan telescope:install
```

**In Debugbar, look for:**
- Query count > 10-20 for simple pages → Likely N+1
- Duplicate query patterns → Definite N+1

**✅ Always profile before optimizing!**

---

### 2. Database Indexing (CRITICAL)

**Impact:** 10-100× improvement for large tables

#### Rule 2.1: Index Foreign Keys

**❌ Bad: Missing Index**
```php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id'); // ← NO INDEX!
    $table->string('title');
});

// Query: WHERE user_id = 123
// Performance: Table scan (SLOW on 1M+ rows)
```

**✅ Good: Indexed Foreign Keys**
```php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    // ↑ Auto-creates index + foreign key constraint
    $table->string('title');
});

// Or explicitly:
$table->index('user_id');
```

**Impact:** 5000ms → 50ms (100× faster) on large tables

---

#### Rule 2.2: Index WHERE Clause Columns

**❌ Bad: Unindexed Filter Columns**
```php
// Migration
$table->string('status'); // No index

// Query
Post::where('status', 'published')->get(); // Table scan!
```

**✅ Good: Indexed Filter Columns**
```php
// Migration
$table->string('status')->index();

// Or composite index for multiple filters
$table->index(['status', 'published_at']);
```

**Impact:** 2000ms → 20ms (100× faster)

---

#### Rule 2.3: Use `EXPLAIN` to Verify Indexes

**Check query performance:**
```php
DB::enableQueryLog();

Post::where('user_id', 123)->get();

dd(DB::getQueryLog());
```

**In database:**
```sql
EXPLAIN SELECT * FROM posts WHERE user_id = 123;

-- Look for "type: index" or "type: ref"
-- Avoid "type: ALL" (table scan)
```

---

### 3. Query Result Caching (CRITICAL)

**Impact:** 80-95% faster for repeated queries

#### Rule 3.1: Cache Expensive Queries

**❌ Bad: No Caching**
```php
public function index()
{
    // Runs query EVERY request
    $stats = DB::table('posts')
        ->selectRaw('COUNT(*) as total, AVG(views) as avg_views')
        ->first();
    
    return view('dashboard', compact('stats'));
}
```

**✅ Good: Cache Results**
```php
use Illuminate\Support\Facades\Cache;

public function index()
{
    $stats = Cache::remember('dashboard.stats', 3600, function () {
        return DB::table('posts')
            ->selectRaw('COUNT(*) as total, AVG(views) as avg_views')
            ->first();
    });
    
    return view('dashboard', compact('stats'));
}
```

**Impact:** 500ms → 5ms (100× faster)

---

#### Rule 3.2: Cache Tags for Granular Invalidation

**❌ Bad: Cache Everything or Nothing**
```php
// Option 1: Cache forever (stale data)
Cache::forever('users', User::all());

// Option 2: No cache (slow)
$users = User::all();
```

**✅ Good: Tagged Cache**
```php
// Cache with tags
Cache::tags(['users'])->remember('users.all', 3600, function () {
    return User::all();
});

// Invalidate when user changes
public function update(User $user)
{
    $user->update($request->all());
    Cache::tags(['users'])->flush(); // Clear only user caches
}
```

**Impact:** Fresh data + performance

---

### 4. Eager Loading Strategy (HIGH)

**Impact:** 40-70% faster

#### Rule 4.1: Nested Eager Loading

**❌ Bad: Multiple Levels Load Separately**
```php
$users = User::with('posts')->get();

// Later in view: Still causes N+1!
foreach ($users as $user) {
    foreach ($user->posts as $post) {
        echo $post->comments->count(); // N+1 on comments!
    }
}
```

**✅ Good: Nested Eager Loading**
```php
$users = User::with('posts.comments')->get();

// Or with counts
$users = User::with('posts')->withCount('posts.comments')->get();
```

---

#### Rule 4.2: Conditional Eager Loading

**❌ Bad: Always Load Everything**
```php
// Loads comments even when not needed
$posts = Post::with('comments')->get();
```

**✅ Good: Load Only When Needed**
```php
$posts = Post::query()
    ->when($request->has('include_comments'), function ($query) {
        $query->with('comments');
    })
    ->get();
```

---

### 5. Response Caching (HIGH)

**Impact:** 90-99% faster for static/semi-static pages

#### Rule 5.1: HTTP Cache Headers

**✅ Good: Set Cache Headers**
```php
return response()
    ->view('blog.post', compact('post'))
    ->header('Cache-Control', 'public, max-age=3600');
```

---

#### Rule 5.2: Full Page Caching

**✅ Use Laravel ResponseCache**
```bash
composer require spatie/laravel-responsecache
```

```php
// Automatically caches responses
Route::get('/blog', [BlogController::class, 'index'])
    ->middleware('cacheResponse:3600');
```

**Impact:** 500ms → 5ms (100× faster)

---

### 6. Collection Optimization (MEDIUM)

**Impact:** 30-50% faster

#### Rule 6.1: Use `chunk()` for Large Datasets

**❌ Bad: Load Everything into Memory**
```php
// Loads 1 million records into memory → OutOfMemoryException
$users = User::all();

foreach ($users as $user) {
    $user->notify(new NewsletterEmail());
}
```

**✅ Good: Process in Chunks**
```php
User::chunk(1000, function ($users) {
    foreach ($users as $user) {
        $user->notify(new NewsletterEmail());
    }
});
```

**Impact:** No memory errors, 40% faster

---

#### Rule 6.2: Use `lazy()` for Better Memory Efficiency

**✅ Best: Lazy Collection (Laravel 8+)**
```php
User::lazy()->each(function ($user) {
    $user->notify(new NewsletterEmail());
});
// Automatically chunks + lower memory overhead
```

---

### 7. Job Queues (MEDIUM)

**Impact:** Better UX, async processing

#### Rule 7.1: Queue Slow Operations

**❌ Bad: Blocking Request**
```php
public function store(Request $request)
{
    $user = User::create($request->all());
    
    // Blocks response for 2-5 seconds
    Mail::to($user)->send(new WelcomeEmail());
    
    return redirect()->route('dashboard');
}
```

**✅ Good: Queue Email**
```php
public function store(Request $request)
{
    $user = User::create($request->all());
    
    // Returns immediately
    Mail::to($user)->queue(new WelcomeEmail());
    
    return redirect()->route('dashboard');
}
```

**Impact:** 3000ms → 200ms perceived response time

---

## 🎯 USAGE GUIDELINES FOR AGENTS

### When to Apply This Skill

✅ **DO apply when:**
- Optimizing Laravel backend performance
- Code review for performance issues
- User reports slow API responses
- Building production features
- Refactoring existing controllers

❌ **DON'T apply when:**
- Prototyping/MVP stage
- Response time already <100ms
- No user complaints
- Over-optimizing prematurely

---

### Priority Decision Tree

```
User wants to optimize Laravel code
├── Profile first - DON'T guess!
│   └── Use Laravel Debugbar/Telescope
│
├── Identify bottleneck type
│   ├── Slow database queries? → Check CRITICAL (1-3)
│   │   ├── N+1 queries? → Rule 1.1-1.3
│   │   ├── Missing indexes? → Rule 2.1-2.3
│   │   └── Repeated queries? → Rule 3.1-3.2
│   │
│   ├── High database load? → Check HIGH (4-5)
│   │   ├── Eager loading → Rule 4.1-4.2
│   │   └── Response caching → Rule 5.1-5.2
│   │
│   └── Memory/slow operations? → Check MEDIUM (6-7)
│       ├── Large datasets → Rule 6.1-6.2
│       └── Blocking operations → Rule 7.1
│
└── Apply fix, measure improvement
    └── Document impact (e.g., "600ms → 100ms")
```

---

### Communication Template

When suggesting optimizations, use this format:

```
**Performance Issue Identified**

Category: [CRITICAL/HIGH/MEDIUM/LOW]
Rule: [Section].[Number] [Rule Name]
Impact: [Expected improvement]

Current Code:
[bad example]

Suggested Fix:
[good example]

Rationale:
[Why this matters, cite metric if possible]

Estimated Impact:
[e.g., "6x faster" or "Eliminates 100 queries per request"]
```

---

## 📋 QUICK REFERENCE: TOP RULES

### CRITICAL Priority

**1. Eliminate N+1 Queries**
- ✅ Use `with()` for eager loading
- ✅ Use `withCount()` for counts only
- ✅ Profile with Debugbar/Telescope
- ❌ Don't load relationships in loops

**2. Add Database Indexes**
- ✅ Index all foreign keys
- ✅ Index WHERE clause columns
- ✅ Use composite indexes for multiple filters
- ❌ Don't forget to index after adding columns

**3. Implement Query Caching**
- ✅ Use `Cache::remember()` for expensive queries
- ✅ Use cache tags for granular invalidation
- ❌ Don't cache forever without invalidation strategy

---

### HIGH Priority

**4. Optimize Eager Loading**
- ✅ Nested eager loading (`posts.comments`)
- ✅ Conditional loading (only when needed)
- ✅ Select only required columns

**5. Response Caching**
- ✅ Set HTTP cache headers
- ✅ Full page caching for static content
- ✅ Use Laravel ResponseCache package

---

### MEDIUM Priority

**6. Collection Optimization**
- ✅ Use `chunk()` or `lazy()` for large datasets
- ✅ Avoid loading everything into memory
- ✅ Process incrementally

**7. Job Queues**
- ✅ Queue emails, notifications, heavy processing
- ✅ Use `horizon` for queue monitoring
- ✅ Keep web requests fast (<200ms)

---

## 🔗 INTEGRATION WITH OTHER SKILLS

### Use With Laravel Conventions

- **Laravel conventions** (`.agent/rules/standards/frameworks/laravel-conventions.md`) → How to structure Laravel code (services, repositories)
- **laravel-performance** → How to optimize Laravel code (queries, caching)

**Example workflow:**
1. Use Laravel conventions to design architecture
2. Build feature
3. Use `laravel-performance` to optimize bottlenecks
4. Measure improvements

---

## 📊 METRICS TO TRACK

### Before Optimization

- [ ] Average response time (p95)
- [ ] Query count per request
- [ ] Total query time
- [ ] Memory usage
- [ ] Cache hit rate

### After Optimization

- [ ] Response time improvement (target: >50% faster)
- [ ] Query reduction (target: >70% fewer)
- [ ] Query time reduction (target: >80% faster)
- [ ] Memory reduction (target: >40% less)
- [ ] Cache hit rate (target: >80%)

---

## ✅ CHECKLIST FOR AGENTS

Before completing performance optimization work:

**CRITICAL Priority:**
- [ ] Checked for N+1 queries (Debugbar/Telescope)
- [ ] Verified all foreign keys have indexes
- [ ] Implemented query result caching for expensive queries
- [ ] Measured before/after query counts

**HIGH Priority:**
- [ ] Verified eager loading strategy
- [ ] Added response caching where appropriate
- [ ] Checked database connection pooling

**MEDIUM Priority:**
- [ ] Used `chunk()` or `lazy()` for large datasets
- [ ] Queued heavy operations (emails, processing)
- [ ] Optimized collection operations

**Documentation:**
- [ ] Measured before/after metrics
- [ ] Documented expected impact
- [ ] Added comments explaining optimizations
- [ ] Updated controller docs with performance notes

---

## 📖 REFERENCES

- [Laravel Performance Best Practices](https://laravel.com/docs/performance)
- [Laravel Query Builder](https://laravel.com/docs/queries)
- [Laravel Eloquent](https://laravel.com/docs/eloquent)
- [Laravel Caching](https://laravel.com/docs/cache)
- [Laravel Debugbar](https://github.com/barryvdh/laravel-debugbar)
- [Laravel Telescope](https://laravel.com/docs/telescope)

---

> **Remember:** Fix CRITICAL issues first (N+1, indexes, caching). Don't waste time on LOW optimizations if CRITICAL bottlenecks exist. Always profile before optimizing, and measure after to confirm improvements.

**Created:** 2026-01-19  
**Version:** 1.0  
**Framework:** Laravel  
**Inspired By:** Vercel React Best Practices (impact-driven prioritization)
