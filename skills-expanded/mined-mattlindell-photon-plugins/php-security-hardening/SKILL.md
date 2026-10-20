---
name: php-security-hardening
description: PHP security patterns organized by framework — universal PHP, WordPress (nonces, capabilities, escaping), Laravel (Form Requests, guards, Sanctum), and CI3 legacy hardening. Use when implementing authentication, authorization, input validation, output escaping, or any security-sensitive code.
---

# PHP Security Hardening

Security patterns organized by framework, covering the most common vulnerabilities in PHP applications. Every pattern shows the vulnerable approach and the secure alternative so you can recognize and prevent security flaws at the code level.

## When to Use This Skill

- Implementing authentication or authorization logic
- Handling user input (forms, query strings, file uploads, API requests)
- Writing database queries that include any external data
- Rendering user-supplied content in HTML, attributes, or URLs
- Building REST API endpoints
- Storing or verifying passwords and secrets
- Configuring sessions, CSRF protection, or security headers
- Auditing existing code for security weaknesses
- Hardening legacy CI3 applications

## Core Concepts

**Defense in depth:** Never rely on a single security control. Validate input, escape output, use prepared statements, enforce authorization, and set security headers -- all together.

**Principle of least privilege:** Grant only the minimum permissions required. Use allowlists (`$fillable`, `current_user_can()`, `permission_callback`) rather than denylists.

**Input validation vs output escaping:** Validate and sanitize data when it enters your application. Escape data when it leaves (into HTML, SQL, URLs, etc.). These are complementary, not interchangeable.

**Framework-first security:** Always prefer your framework's built-in security mechanisms over hand-rolled solutions.

## Quick Start

The single most impactful security improvement for any PHP codebase:

```php
// 1. Never concatenate user input into SQL
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => $email]);

// 2. Never echo user input without escaping
echo htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

// 3. Never store passwords in plaintext
$hash = password_hash($password, PASSWORD_DEFAULT);
```

---

## Universal PHP Security

These patterns apply to all PHP applications regardless of framework.

### Pattern 1: SQL Injection Prevention

**Vulnerable (DO NOT DO THIS):**

```php
$username = $_GET['username'];
$result = $pdo->query("SELECT * FROM users WHERE username = '$username'");
// Attacker sends: ' OR '1'='1' --  => returns ALL users
```

**Secure (DO THIS):**

```php
// Prepared statement with parameter binding
$stmt = $pdo->prepare('SELECT * FROM users WHERE username = :username');
$stmt->execute(['username' => $_GET['username']]);
$result = $stmt->fetchAll();

// For IN clauses, generate placeholders dynamically
$ids = [1, 2, 3];
$placeholders = implode(',', array_fill(0, count($ids), '?'));
$stmt = $pdo->prepare("SELECT * FROM users WHERE id IN ($placeholders)");
$stmt->execute($ids);

// Configure PDO securely
$pdo = new PDO($dsn, $user, $pass, [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_EMULATE_PREPARES   => false,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);
```

**Why:** Prepared statements separate query structure from data, making injection impossible. Disabling emulated prepares ensures native parameterization.

### Pattern 2: Password Storage

**Vulnerable (DO NOT DO THIS):**

```php
// Plaintext, MD5, SHA1, or salted MD5 -- all inadequate
$hash = md5($_POST['password']);
// Timing-attack-vulnerable comparison
if ($storedHash == md5($inputPassword)) { /* login */ }
```

**Secure (DO THIS):**

```php
// Hash with password_hash() -- bcrypt by default, auto-generates salt
$hash = password_hash($_POST['password'], PASSWORD_DEFAULT);

// Verify with password_verify() -- timing-safe comparison
$storedHash = $db->fetchColumn('SELECT password FROM users WHERE email = ?', [$email]);
if ($storedHash && password_verify($_POST['password'], $storedHash)) {
    // Rehash if algorithm has been upgraded
    if (password_needs_rehash($storedHash, PASSWORD_DEFAULT)) {
        $newHash = password_hash($_POST['password'], PASSWORD_DEFAULT);
        $db->execute('UPDATE users SET password = ? WHERE email = ?', [$newHash, $email]);
    }
} else {
    throw new AuthenticationException('Invalid email or password.');
}
```

**Why:** `password_hash()` uses intentionally slow algorithms with unique salts. `password_verify()` uses constant-time comparison to prevent timing attacks. `password_needs_rehash()` enables transparent algorithm upgrades.

### Pattern 3: CSRF Protection

**Vulnerable (DO NOT DO THIS):**

```php
// No CSRF token -- any external site can forge this request
if ($_POST['confirm'] === 'yes') {
    deleteAccount($_SESSION['user_id']);
}
```

**Secure (DO THIS):**

```php
// Generate and store a CSRF token in the session
function generateCsrfToken(): string {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

// Verify on submission using hash_equals() (timing-safe)
function verifyCsrfToken(string $token): bool {
    return isset($_SESSION['csrf_token'])
        && hash_equals($_SESSION['csrf_token'], $token);
}

// In handler: verify before processing
if (!verifyCsrfToken($_POST['csrf_token'] ?? '')) {
    http_response_code(403);
    die('Invalid CSRF token.');
}
// Regenerate after sensitive actions
unset($_SESSION['csrf_token']);
```

**Why:** CSRF tokens prove the request originated from your form. `hash_equals()` prevents timing attacks. Regenerating after sensitive actions prevents replay.

### Pattern 4: File Upload Validation

**Vulnerable (DO NOT DO THIS):**

```php
// No type validation, original filename, no size limit, web-accessible directory
$destination = '/var/www/uploads/' . $_FILES['avatar']['name'];
move_uploaded_file($_FILES['avatar']['tmp_name'], $destination);
```

**Secure (DO THIS):**

```php
function handleFileUpload(array $file, string $uploadDir): string {
    if ($file['error'] !== UPLOAD_ERR_OK) {
        throw new RuntimeException('Upload failed: ' . $file['error']);
    }
    if ($file['size'] > 2 * 1024 * 1024) {
        throw new RuntimeException('File exceeds 2 MB limit.');
    }
    // Validate MIME via finfo (not client-supplied type)
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $allowedTypes = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/gif' => 'gif', 'image/webp' => 'webp'];
    $detected = $finfo->file($file['tmp_name']);
    if (!isset($allowedTypes[$detected])) {
        throw new RuntimeException('File type not allowed.');
    }
    // Random filename prevents path traversal and overwrites
    $newFilename = bin2hex(random_bytes(16)) . '.' . $allowedTypes[$detected];
    move_uploaded_file($file['tmp_name'], rtrim($uploadDir, '/') . '/' . $newFilename);
    return $newFilename;
}
// Store uploads OUTSIDE the web root
$filename = handleFileUpload($_FILES['avatar'], '/var/www/storage/uploads/');
```

**Why:** Validate MIME type via `finfo`, generate random filenames, and store outside the web root to prevent attackers from uploading and executing PHP shells.

### Pattern 5: Cross-Site Scripting (XSS) Prevention

**Vulnerable (DO NOT DO THIS):**

```php
echo "<h1>Welcome, " . $_GET['name'] . "</h1>";
echo '<input type="text" value="' . $userInput . '">';
echo '<a href="' . $userUrl . '">Click here</a>';
```

**Secure (DO THIS):**

```php
// HTML body context
echo '<h1>Welcome, ' . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . '</h1>';

// HTML attribute context
echo '<input type="text" value="' . htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8') . '">';

// URL context -- validate scheme first
function safeUrl(string $url): string {
    $parsed = parse_url($url);
    if (!$parsed || !in_array($parsed['scheme'] ?? '', ['http', 'https'], true)) {
        return '#';
    }
    return htmlspecialchars($url, ENT_QUOTES, 'UTF-8');
}

// JavaScript context
echo '<script>var userData = ' . json_encode($userData, JSON_HEX_TAG | JSON_HEX_AMP) . ';</script>';

// Helper to reduce boilerplate
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}
```

**Why:** XSS lets attackers execute JavaScript in other users' browsers. The fix is context-aware output escaping at the point of output, not at input.

### Pattern 6: Security Headers

**Vulnerable (DO NOT DO THIS):**

```php
// No security headers -- browser defaults leave users exposed to
// clickjacking, MIME sniffing, downgrade attacks, and inline script injection
```

**Secure (DO THIS):**

```php
function setSecurityHeaders(): void {
    header('X-Frame-Options: SAMEORIGIN');
    header('X-Content-Type-Options: nosniff');
    header('Strict-Transport-Security: max-age=31536000; includeSubDomains; preload');
    header("Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; frame-ancestors 'self'");
}
setSecurityHeaders();
```

**Why:** Security headers are a zero-cost defense-in-depth measure. CSP prevents inline script injection, HSTS prevents protocol downgrade, and X-Frame-Options prevents clickjacking.

---

## WordPress Security

WordPress-specific patterns using the functions and APIs provided by WordPress core.

### Pattern 7: Nonce Verification

**Vulnerable (DO NOT DO THIS):**

```php
// No nonce -- any external site can forge this request
add_action('admin_post_delete_item', function () {
    wp_delete_post($_POST['item_id'], true);
    wp_redirect(admin_url('admin.php?page=my-plugin'));
    exit;
});
```

**Secure (DO THIS):**

```php
// In the form
function render_delete_form(int $item_id): void { ?>
    <form method="POST" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
        <?php wp_nonce_field('delete_item_' . $item_id, '_delete_nonce'); ?>
        <input type="hidden" name="action" value="delete_item">
        <input type="hidden" name="item_id" value="<?php echo absint($item_id); ?>">
        <button type="submit">Delete</button>
    </form>
<?php }

// In the handler
add_action('admin_post_delete_item', function () {
    $item_id = absint($_POST['item_id'] ?? 0);
    if (!wp_verify_nonce($_POST['_delete_nonce'] ?? '', 'delete_item_' . $item_id)) {
        wp_die('Security check failed.', 'Forbidden', ['response' => 403]);
    }
    if (!current_user_can('delete_post', $item_id)) {
        wp_die('Permission denied.', 'Forbidden', ['response' => 403]);
    }
    wp_delete_post($item_id, true);
    wp_safe_redirect(admin_url('admin.php?page=my-plugin&deleted=1'));
    exit;
});

// For AJAX: use check_ajax_referer()
add_action('wp_ajax_my_ajax_action', function () {
    check_ajax_referer('my_ajax_nonce', 'security');
    wp_send_json_success(['message' => 'Done']);
});
```

**Why:** Nonces are time-limited tokens tied to a specific action and user, proving the request is legitimate. Always pair nonce verification with capability checks.

### Pattern 8: Capability Checks

**Vulnerable (DO NOT DO THIS):**

```php
// 'read' capability -- any logged-in user can access admin settings
add_menu_page('Settings', 'My Plugin', 'read', 'my-plugin-settings', 'render_settings_page');
add_action('admin_post_save_settings', function () {
    update_option('my_plugin_api_key', $_POST['api_key']);
});
```

**Secure (DO THIS):**

```php
// Require 'manage_options' capability for the menu
add_action('admin_menu', function () {
    add_menu_page('My Plugin Settings', 'My Plugin', 'manage_options', 'my-plugin-settings', 'render_settings_page');
});

// Verify capability + nonce in the handler (defense in depth)
add_action('admin_post_save_settings', function () {
    check_admin_referer('my_plugin_save_settings', '_settings_nonce');
    if (!current_user_can('manage_options')) {
        wp_die('Permission denied.', 'Forbidden', ['response' => 403]);
    }
    update_option('my_plugin_api_key', sanitize_text_field($_POST['api_key'] ?? ''));
    wp_safe_redirect(admin_url('admin.php?page=my-plugin-settings&saved=1'));
    exit;
});

// Post-specific capability with meta-capability mapping
if (!current_user_can('edit_post', $post_id)) {
    wp_die('You cannot edit this post.');
}
```

**Why:** The menu page capability only hides the menu item; it does not protect the handler. Check capabilities in both places. Use WordPress's role/capability system rather than `is_admin()` (which only checks if you are on an admin page).

### Pattern 9: Output Escaping

**Vulnerable (DO NOT DO THIS):**

```php
echo '<h2>' . $post_title . '</h2>';
echo '<a href="' . $url . '">Visit site</a>';
echo '<input type="text" value="' . $option_value . '">';
```

**Secure (DO THIS):**

```php
// HTML body -- esc_html()
echo '<h2>' . esc_html($post_title) . '</h2>';

// HTML attributes -- esc_attr()
echo '<input type="text" value="' . esc_attr($option_value) . '">';

// URLs -- esc_url()
echo '<a href="' . esc_url($url) . '">Visit site</a>';

// Rich HTML -- wp_kses_post() allows safe post-level tags
echo wp_kses_post($content_with_html);

// Custom allowed HTML -- wp_kses() with explicit allowlist
$allowed = ['a' => ['href' => [], 'title' => []], 'strong' => [], 'em' => []];
echo wp_kses($user_bio, $allowed);

// Textarea -- esc_textarea()
echo '<textarea>' . esc_textarea($saved_content) . '</textarea>';
```

**Why:** Each escaping function is designed for a specific output context. Escape at the point of output (late escaping) -- the WordPress security standard.

### Pattern 10: Database Query Safety

**Vulnerable (DO NOT DO THIS):**

```php
global $wpdb;
$results = $wpdb->get_results("SELECT * FROM {$wpdb->prefix}orders WHERE user_id = " . $_GET['user_id']);
$wpdb->query("DELETE FROM {$wpdb->prefix}logs WHERE id = " . $_POST['log_id']);
```

**Secure (DO THIS):**

```php
global $wpdb;

// Use $wpdb->prepare() with format placeholders
$results = $wpdb->get_results(
    $wpdb->prepare("SELECT * FROM {$wpdb->prefix}orders WHERE user_id = %d", absint($_GET['user_id']))
);

// LIKE queries -- esc_like() then prepare()
$like = '%' . $wpdb->esc_like(sanitize_text_field($_GET['s'])) . '%';
$results = $wpdb->get_results(
    $wpdb->prepare("SELECT * FROM {$wpdb->prefix}posts WHERE post_title LIKE %s", $like)
);

// IN clause with multiple values
$ids = array_map('absint', $_GET['ids'] ?? []);
if (!empty($ids)) {
    $placeholders = implode(',', array_fill(0, count($ids), '%d'));
    $results = $wpdb->get_results(
        $wpdb->prepare("SELECT * FROM {$wpdb->prefix}posts WHERE ID IN ($placeholders)", ...$ids)
    );
}

// INSERT/UPDATE -- prefer $wpdb->insert() and $wpdb->update()
$wpdb->insert(
    $wpdb->prefix . 'orders',
    ['user_id' => $user_id, 'total' => $total, 'status' => 'pending'],
    ['%d', '%f', '%s']
);
```

**Why:** `$wpdb->prepare()` uses `%s`, `%d`, `%f` placeholders that are properly escaped. For LIKE queries, `$wpdb->esc_like()` escapes `%` and `_` within the search term. Always sanitize input in addition to using prepared statements.

### Pattern 11: REST Endpoint Security

**Vulnerable (DO NOT DO THIS):**

```php
// No permission_callback -- accessible to anyone, triggers _doing_it_wrong in WP 5.5+
register_rest_route('my-plugin/v1', '/users/(?P<id>\d+)', [
    'methods'  => 'DELETE',
    'callback' => function (WP_REST_Request $request) {
        wp_delete_user($request['id']);
        return new WP_REST_Response(['deleted' => true]);
    },
]);
```

**Secure (DO THIS):**

```php
register_rest_route('my-plugin/v1', '/users/(?P<id>\d+)', [
    'methods'             => 'DELETE',
    'callback'            => 'my_plugin_delete_user',
    'permission_callback' => fn(WP_REST_Request $r) => current_user_can('delete_users'),
    'args' => [
        'id' => [
            'required'          => true,
            'validate_callback' => fn($v) => is_numeric($v) && $v > 0,
            'sanitize_callback' => 'absint',
        ],
    ],
]);

function my_plugin_delete_user(WP_REST_Request $request): WP_REST_Response {
    $user_id = $request->get_param('id');
    if (get_current_user_id() === $user_id) {
        return new WP_REST_Response(['message' => 'Cannot delete yourself.'], 400);
    }
    require_once ABSPATH . 'wp-admin/includes/user.php';
    wp_delete_user($user_id);
    return new WP_REST_Response(['deleted' => true, 'user_id' => $user_id]);
}

// For intentionally public endpoints, declare it explicitly
register_rest_route('my-plugin/v1', '/posts', [
    'methods'             => 'GET',
    'callback'            => 'my_plugin_get_posts',
    'permission_callback' => '__return_true',
]);
```

**Why:** `permission_callback` is the authorization gate for REST endpoints. Even public endpoints should set it to `'__return_true'` to show it was deliberate. Use `validate_callback` and `sanitize_callback` for type safety at the API boundary.

---

## Laravel Security

Laravel-specific security patterns using the framework's built-in tools.

### Pattern 12: Mass Assignment Protection

**Vulnerable (DO NOT DO THIS):**

```php
class User extends Model { }  // No $fillable -- all attributes mass-assignable

public function store(Request $request) {
    $user = User::create($request->all()); // Attacker can send is_admin=true
}
```

**Secure (DO THIS):**

```php
class User extends Model {
    protected $fillable = ['name', 'email', 'password'];
    protected $hidden = ['password', 'remember_token'];
    protected $casts = [
        'email_verified_at' => 'datetime',
        'is_admin'          => 'boolean',
        'password'          => 'hashed', // Laravel 10+
    ];
}

public function store(StoreUserRequest $request) {
    $user = User::create($request->validated()); // Only validated fields
}

// Protected fields must be set explicitly
public function promoteToAdmin(User $user): void {
    $user->is_admin = true;
    $user->save();
}
```

**Why:** `$fillable` whitelists mass-assignable attributes. Prefer `$fillable` over `$guarded` because forgetting to guard a new column is a vulnerability, while forgetting to fill one is just a bug. Always use `$request->validated()` instead of `$request->all()`.

### Pattern 13: Authentication Middleware

**Vulnerable (DO NOT DO THIS):**

```php
// No middleware -- anyone can access; or manual auth()->check() in every method
Route::get('/dashboard', [DashboardController::class, 'index']);
Route::get('/admin/users', [AdminController::class, 'users']);
```

**Secure (DO THIS):**

```php
// Authenticated routes
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::post('/settings', [SettingsController::class, 'update']);
});

// Admin routes with role middleware
Route::middleware(['auth', 'verified', 'admin'])->prefix('admin')->group(function () {
    Route::get('/users', [AdminController::class, 'users']);
});

// Custom admin middleware
class EnsureUserIsAdmin {
    public function handle(Request $request, Closure $next): Response {
        if (!$request->user()?->is_admin) {
            abort(403, 'Unauthorized.');
        }
        return $next($request);
    }
}

// API routes with Sanctum
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('posts', PostController::class);
});
```

**Why:** Middleware enforces auth at the routing layer before controller code runs. A missing route in a middleware group is immediately obvious; a forgotten `auth()->check()` in a controller is a silent vulnerability.

### Pattern 14: Form Request Validation

**Vulnerable (DO NOT DO THIS):**

```php
public function store(Request $request) {
    $post = Post::create([
        'title'   => $request->input('title'),
        'body'    => $request->input('body'),
        'user_id' => $request->input('user_id'), // User can set any author!
    ]);
}
```

**Secure (DO THIS):**

```php
class StorePostRequest extends FormRequest {
    public function authorize(): bool {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array {
        return [
            'title'       => ['required', 'string', 'max:255'],
            'body'        => ['required', 'string', 'max:50000'],
            'category_id' => ['required', 'integer', 'exists:categories,id'],
            'tags'        => ['sometimes', 'array', 'max:10'],
            'tags.*'      => ['integer', 'exists:tags,id'],
        ];
    }
}

// Clean controller
public function store(StorePostRequest $request) {
    $post = Post::create([
        ...$request->validated(),
        'user_id' => $request->user()->id, // Set from auth, not input
    ]);
    return redirect()->route('posts.show', $post);
}
```

**Why:** Form Requests move validation and authorization into a dedicated, reusable class. `$request->validated()` returns only fields that passed validation. Setting `user_id` from auth prevents impersonation.

### Pattern 15: Rate Limiting

**Vulnerable (DO NOT DO THIS):**

```php
// No rate limiting on login, API, or password reset endpoints
Route::post('/login', [AuthController::class, 'login']);
Route::post('/api/search', [SearchController::class, 'query']);
```

**Secure (DO THIS):**

```php
// Define rate limiters in AppServiceProvider boot()
RateLimiter::for('login', function (Request $request) {
    $key = Str::lower($request->string('email')) . '|' . $request->ip();
    return Limit::perMinute(5)->by($key)->response(fn() =>
        back()->withErrors(['email' => 'Too many attempts. Try again in a minute.'])
    );
});

RateLimiter::for('api', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(60)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});

// Apply to routes
Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:login');
Route::middleware(['auth:sanctum', 'throttle:api'])->group(function () {
    Route::apiResource('posts', PostController::class);
});
Route::post('/forgot-password', [PasswordController::class, 'sendResetLink'])
    ->middleware('throttle:sensitive');
```

**Why:** Without rate limiting, attackers can brute-force credentials or exhaust resources. Key by email+IP on login to prevent credential stuffing while allowing different users from the same IP.

---

## CI3 Legacy Security

Patterns for hardening CodeIgniter 3 applications that are still in production.

### Pattern 16: Query Safety

**Vulnerable (DO NOT DO THIS):**

```php
class User_model extends CI_Model {
    public function get_user($username) {
        $query = $this->db->query(
            "SELECT * FROM users WHERE username = '" . $username . "'"
        );
        return $query->row();
    }

    public function search($term) {
        $this->db->where("name LIKE '%" . $term . "%'");
        return $this->db->get('products')->result();
    }
}
```

**Secure (DO THIS):**

```php
class User_model extends CI_Model {
    // Query bindings -- CI3's parameterized query mechanism
    public function get_user(string $username) {
        return $this->db->query('SELECT * FROM users WHERE username = ?', [$username])->row();
    }

    // Active Record -- auto-escapes values
    public function get_user_ar(string $username) {
        return $this->db->where('username', $username)->get('users')->row();
    }

    // LIKE queries with Active Record
    public function search(string $term) {
        return $this->db->like('name', $term)->get('products')->result();
    }

    // Multiple conditions with explicit type casting
    public function get_orders(int $user_id, string $status) {
        return $this->db
            ->where('user_id', (int) $user_id)
            ->where('status', $status)
            ->order_by('created_at', 'DESC')
            ->get('orders')
            ->result();
    }
}
```

**Why:** CI3's `?` bindings and Active Record methods auto-escape values. Cast to `(int)` for integer parameters as an extra safety layer. Never concatenate user input into raw SQL.

### Pattern 17: Session Hardening

**Vulnerable (DO NOT DO THIS):**

```php
// application/config/config.php -- insecure defaults
$config['sess_save_path']       = NULL;    // Shared /tmp
$config['sess_expiration']      = 0;       // Never expires
$config['cookie_httponly']      = FALSE;   // JS can read cookie
$config['cookie_secure']        = FALSE;   // Sent over HTTP
$config['cookie_samesite']      = '';      // No SameSite
```

**Secure (DO THIS):**

```php
// application/config/config.php -- hardened
$config['sess_driver']          = 'database';
$config['sess_save_path']       = 'ci_sessions';
$config['sess_cookie_name']     = '__Host-session';
$config['sess_expiration']      = 7200;        // 2 hours
$config['sess_match_ip']        = TRUE;
$config['sess_time_to_update']  = 300;         // Regenerate ID every 5 min
$config['cookie_secure']        = TRUE;
$config['cookie_httponly']       = TRUE;
$config['cookie_samesite']      = 'Lax';

// Regenerate session ID on privilege changes
class Auth extends CI_Controller {
    public function login() {
        // ... validate credentials ...
        if ($authenticated) {
            $this->session->sess_regenerate(TRUE); // Destroy old session
            $this->session->set_userdata([
                'user_id'   => $user->id,
                'logged_in' => TRUE,
            ]);
        }
    }

    public function logout() {
        $this->session->sess_destroy();
        redirect('login');
    }
}
```

**Why:** Default CI3 session config is insecure. File-based sessions in `/tmp` can be read by other apps on shared hosting. Cookies without `httponly` can be stolen via XSS. Regenerating session IDs after login prevents session fixation. The `__Host-` cookie prefix enforces secure + path=/.

---

## Best Practices Summary

### Input Handling

- Validate and sanitize all input at the application boundary
- Use framework sanitization: `sanitize_text_field()` (WP), `$request->validated()` (Laravel), `$this->input->post()` (CI3)
- Never trust client-supplied data: form fields, query params, headers, cookies, files, API bodies

### Output Escaping

- Escape at the point of output, not input
- WP: `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses()`
- Laravel: Blade `{{ }}` auto-escapes; `{!! !!}` only for trusted HTML
- CI3: `html_escape()` or `htmlspecialchars()`

### Database Queries

- Never concatenate user input into SQL
- PHP: PDO prepared statements; WP: `$wpdb->prepare()`; Laravel: Eloquent/Query Builder; CI3: query bindings or Active Record

### Authentication and Authorization

- Check both identity and permission on every request
- WP: `wp_verify_nonce()` + `current_user_can()`; Laravel: `auth` middleware + Policies; CI3: session auth + role checks

### CSRF and Session Security

- Use framework CSRF on all state-changing requests
- WP: `wp_nonce_field()`/`wp_verify_nonce()`; Laravel: `@csrf`; CI3: `$config['csrf_protection'] = TRUE`
- Regenerate session IDs after login

### Security Headers

- Set CSP, HSTS, X-Frame-Options, X-Content-Type-Options on every response

### Dependency Management

- Run `composer audit` regularly
- Keep frameworks updated; pin versions in production via `composer.lock`
