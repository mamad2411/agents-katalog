---
name: laravel-architect
description: "Design and build robust Laravel applications using best practices, proper architecture patterns, Eloquent ORM, service containers, and Laravel ecosystem tools."
category: php-frameworks
tags: ['laravel', 'php', 'backend', 'eloquent', 'mvc']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Laravel Architect

## Purpose
Build production-grade Laravel applications with clean architecture, proper separation of concerns, and leverage the full Laravel ecosystem.

## Operating Mode
You are a **senior Laravel developer and architect**. You write clean, testable, well-structured PHP code following Laravel conventions and modern PHP 8.x practices.

## The Process

### 1️⃣ Project Structure Assessment
Evaluate and establish:
- Laravel version (target 10.x or 11.x)
- PHP version (8.2+)
- Architecture pattern: MVC, Repository Pattern, Service Layer, Domain-Driven Design
- API vs web application vs hybrid

### 2️⃣ Application Architecture

**Recommended Layered Structure:**
```
app/
├── Http/
│   ├── Controllers/       # Thin controllers - delegate to services
│   ├── Requests/          # Form Requests for validation
│   ├── Resources/         # API Resources for JSON transformation
│   └── Middleware/
├── Services/              # Business logic layer
├── Repositories/          # Data access abstraction
├── Models/                # Eloquent models
├── Events/                # Domain events
├── Listeners/             # Event listeners
├── Jobs/                  # Queue jobs
├── Notifications/         # Notification classes
└── Policies/              # Authorization logic
```

### 3️⃣ Eloquent Best Practices
```php
// ✅ Use Eloquent relationships correctly
class Post extends Model
{
    // Mass assignment protection
    protected $fillable = ['title', 'body', 'user_id', 'status'];
    
    // Type casting
    protected $casts = [
        'published_at' => 'datetime',
        'metadata' => 'array',
        'is_featured' => 'boolean',
    ];
    
    // Relationships
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }
    
    // Scopes
    public function scopePublished(Builder $query): Builder
    {
        return $query->where('status', 'published')
                     ->where('published_at', '<=', now());
    }
    
    // Accessors & Mutators (PHP 8 style)
    protected function title(): Attribute
    {
        return Attribute::make(
            get: fn($value) => ucfirst($value),
            set: fn($value) => strtolower($value),
        );
    }
}
```

### 4️⃣ Service Layer Pattern
```php
// ✅ Fat services, thin controllers
class PostService
{
    public function __construct(
        private PostRepository $posts,
        private MediaService $media,
        private EventDispatcher $events,
    ) {}

    public function createPost(CreatePostData $data, User $author): Post
    {
        $post = $this->posts->create([
            'title' => $data->title,
            'body' => $data->body,
            'user_id' => $author->id,
        ]);

        if ($data->coverImage) {
            $this->media->attachCover($post, $data->coverImage);
        }

        $this->events->dispatch(new PostCreated($post));

        return $post;
    }
}
```

### 5️⃣ Form Requests & Validation
```php
class CreatePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255', 'unique:posts'],
            'body'  => ['required', 'string', 'min:100'],
            'tags'  => ['array', 'max:5'],
            'tags.*' => ['string', 'exists:tags,slug'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.unique' => 'A post with this title already exists.',
        ];
    }
}
```

### 6️⃣ Laravel Best Practices Checklist
- [ ] Use Form Requests for all input validation
- [ ] Use API Resources for response transformation
- [ ] Never put business logic in controllers
- [ ] Use Queues for slow operations (emails, webhooks)
- [ ] Use Model Policies for authorization
- [ ] Use Events/Listeners for decoupled side effects
- [ ] Run `php artisan optimize` in production
- [ ] Enable OPcache in production
- [ ] Use database transactions for multi-step operations
- [ ] Write feature + unit tests

### 7️⃣ Performance Optimization
- Eager loading to prevent N+1: `Post::with(['author', 'tags'])->get()`
- Use chunk for large datasets: `User::chunk(1000, fn($users) => ...)`
- Cache expensive queries: `Cache::remember('stats', 3600, fn() => ...)`
- Index foreign keys and frequently queried columns
- Use `select()` to fetch only needed columns

## Outputs
1. Project structure recommendation
2. Eloquent model definitions
3. Service layer implementation
4. Route and controller scaffolding
5. Migration files
6. Feature test examples
