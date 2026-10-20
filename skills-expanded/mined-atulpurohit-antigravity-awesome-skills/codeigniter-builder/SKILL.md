---
name: codeigniter-builder
description: "Build clean, efficient CodeIgniter 4 applications. Covers MVC structure, database queries, validation, services, and RESTful API development."
category: php-frameworks
tags: ['codeigniter', 'php', 'mvc', 'backend']
complexity: intermediate
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# CodeIgniter Builder

## Purpose
Build well-structured CodeIgniter 4 applications using modern PHP practices, proper MVC separation, and CI4's powerful features.

## Operating Mode
You are a **CodeIgniter 4 expert**. You write clean, testable CI4 code following the framework's conventions and PHP 8 features.

## The Process

### 1️⃣ CI4 Project Structure
```
app/
├── Controllers/
│   ├── BaseController.php
│   └── Api/
│       └── PostController.php
├── Models/
│   └── PostModel.php
├── Libraries/          # Custom libraries
├── Filters/            # Middleware-like filters
├── Services/           # Service classes (business logic)
└── Validation/
    └── PostRules.php
```

### 2️⃣ Model with Query Builder
```php
// app/Models/PostModel.php
class PostModel extends Model
{
    protected $table         = 'posts';
    protected $primaryKey    = 'id';
    protected $allowedFields = ['title', 'body', 'user_id', 'status', 'published_at'];
    protected $useTimestamps = true;
    protected $useSoftDeletes = true;
    
    protected $validationRules = [
        'title' => 'required|min_length[3]|max_length[255]|is_unique[posts.title]',
        'body'  => 'required|min_length[100]',
    ];

    public function getPublished(int $perPage = 10): array
    {
        return $this->where('status', 'published')
                    ->where('published_at <=', date('Y-m-d H:i:s'))
                    ->orderBy('published_at', 'DESC')
                    ->paginate($perPage);
    }

    public function search(string $term): array
    {
        return $this->groupStart()
                        ->like('title', $term)
                        ->orLike('body', $term)
                    ->groupEnd()
                    ->where('status', 'published')
                    ->findAll();
    }
}
```

### 3️⃣ Controller (Thin)
```php
class PostController extends BaseController
{
    protected PostModel $postModel;
    protected PostService $postService;

    public function __construct()
    {
        $this->postModel   = new PostModel();
        $this->postService = new PostService();
    }

    public function index(): string
    {
        return view('posts/index', [
            'posts'  => $this->postModel->getPublished(),
            'pager'  => $this->postModel->pager,
        ]);
    }

    public function store(): RedirectResponse
    {
        $data = $this->request->getPost(['title', 'body']);

        if (!$this->postModel->validate($data)) {
            return redirect()->back()->withInput()->with('errors', $this->postModel->errors());
        }

        $this->postService->createPost($data, auth()->id());

        return redirect()->to('/posts')->with('success', 'Post created!');
    }
}
```

### 4️⃣ Filters (Middleware)
```php
// app/Filters/AuthFilter.php
class AuthFilter implements FilterInterface
{
    public function before(RequestInterface $request, $arguments = null): ?ResponseInterface
    {
        if (!auth()->check()) {
            return redirect()->to('/login');
        }
        return null;
    }
}

// Register in app/Config/Filters.php
'aliases' => [
    'auth'       => AuthFilter::class,
    'throttle'   => ThrottleFilter::class,
],
'filters' => [
    'auth' => ['before' => ['dashboard/*', 'posts/create', 'posts/edit/*']],
],
```

### 5️⃣ Services
```php
// app/Services/PostService.php
class PostService
{
    private PostModel $posts;

    public function __construct()
    {
        $this->posts = new PostModel();
    }

    public function createPost(array $data, int $userId): Post|false
    {
        $db = db_connect();
        $db->transStart();

        $postId = $this->posts->insert(array_merge($data, ['user_id' => $userId]));
        // Additional operations...
        
        $db->transComplete();
        return $db->transStatus() ? $this->posts->find($postId) : false;
    }
}
```

## Outputs
1. MVC structure template
2. Model with validation and query builder
3. Controller with proper separation
4. Filter/middleware implementation
5. Service layer pattern
6. RESTful routing configuration
