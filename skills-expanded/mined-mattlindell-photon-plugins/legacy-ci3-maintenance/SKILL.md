---
name: legacy-ci3-maintenance
description: Safe maintenance patterns for CodeIgniter 3 legacy applications — MVC conventions, avoiding regressions, incremental improvements, and security patching. Intentionally lean for codebases in maintenance mode. Use when working in CI3 code, patching CI3 security issues, or making safe changes to legacy PHP.
---

# Legacy CI3 Maintenance

Safe, boring, and correct. This skill covers the minimum you need to maintain a CodeIgniter 3 application without breaking it. CI3 codebases are headed for retirement (eventual rebuild into Python/FastAPI microservices), so the goal is not to modernize aggressively — it is to keep things running, patch security issues, and extract logic incrementally so migration gets easier over time.

Do not overinvest. Every change should either fix a bug, close a security hole, or make the eventual migration cheaper.

## When to Use This Skill

- Making bug fixes or feature patches in a CI3 application
- Patching security vulnerabilities in CI3 code
- Adding tests to untested legacy CI3 code before modifying it
- Extracting business logic into framework-agnostic services
- Adding Composer to a CI3 project for the first time
- Preparing CI3 code for eventual migration to a new stack

## Core Concepts

CodeIgniter 3 follows a straightforward MVC pattern. Controllers handle HTTP, models handle data, views handle output. CI3 uses a "superobject" — `$this` inside controllers/models gives access to all loaded libraries, helpers, and the database via a shared instance. There is no dependency injection container; everything hangs off `$this`.

Key directories:

- `application/controllers/` — request handlers
- `application/models/` — database interaction
- `application/views/` — output templates
- `application/config/` — configuration files
- `application/helpers/` — procedural utility functions
- `application/libraries/` — class-based utilities
- `application/services/` — framework-agnostic business logic (you create this)

## Quick Start

Before touching any CI3 code:

1. **Write a characterization test** that captures current behavior (see Avoiding Regressions below)
2. **Make the smallest possible change** that solves the problem
3. **Test manually in the environment** — CI3 projects rarely have CI pipelines
4. **If extracting logic**, put it in `application/services/` as a plain PHP class

## Fundamental Patterns

### CI3 MVC Refresher

#### Controller Structure

Controllers extend `CI_Controller` and load dependencies in the constructor or per-method. Public methods map to URI segments.

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Orders extends CI_Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->load->model('Order_model');
        $this->load->helper('url');
        $this->load->library('session');
    }

    public function index(): void
    {
        $data['orders'] = $this->Order_model->get_active_orders();
        $data['title'] = 'Active Orders';

        $this->load->view('templates/header', $data);
        $this->load->view('orders/list', $data);
        $this->load->view('templates/footer');
    }

    public function show(int $id): void
    {
        $order = $this->Order_model->get_by_id($id);

        if ($order === null) {
            show_404();
        }

        $data['order'] = $order;
        $this->load->view('templates/header', $data);
        $this->load->view('orders/detail', $data);
        $this->load->view('templates/footer');
    }
}
```

#### Model Structure

Models extend `CI_Model` and use `$this->db` (the Query Builder) for all database interaction. Never concatenate user input into queries.

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Order_model extends CI_Model
{
    protected string $table = 'orders';

    public function get_active_orders(): array
    {
        return $this->db
            ->where('status', 'active')
            ->order_by('created_at', 'DESC')
            ->get($this->table)
            ->result_array();
    }

    public function get_by_id(int $id): ?array
    {
        $row = $this->db
            ->where('id', $id)
            ->get($this->table)
            ->row_array();

        return $row ?: null;
    }

    public function update_status(int $id, string $status): bool
    {
        return $this->db
            ->where('id', $id)
            ->update($this->table, ['status' => $status]);
    }
}
```

#### Routing

Routes are defined in `application/config/routes.php`. CI3 maps URI segments to controller/method by default, but explicit routes give you control.

```php
<?php
// application/config/routes.php

// Default controller when visiting /
$route['default_controller'] = 'dashboard';

// 404 handler
$route['404_override'] = '';

// Explicit routes — left side is URI pattern, right side is controller/method
$route['orders'] = 'orders/index';
$route['orders/(:num)'] = 'orders/show/$1';
$route['api/orders/(:num)/status'] = 'api/orders/update_status/$1';

// Regex route for slugs
$route['blog/(:any)'] = 'blog/post/$1';
```

Wildcards: `(:num)` matches digits, `(:any)` matches any character. For more control, use regex directly: `$route['products/([a-z]+)/(\d+)'] = 'catalog/product/$1/$2';`

### Avoiding Regressions

#### Characterization Test

Before changing any existing code, write a test that locks in the current behavior. This is your safety net — if the test passes before your change, it must still pass after.

```php
<?php
// tests/models/Order_model_test.php

use PHPUnit\Framework\TestCase;

class Order_model_test extends TestCase
{
    private static $CI;
    private Order_model $model;

    public static function setUpBeforeClass(): void
    {
        // Boot CI3 test instance
        self::$CI =& get_instance();
        self::$CI->load->database('testing');
    }

    protected function setUp(): void
    {
        self::$CI->load->model('Order_model');
        $this->model = self::$CI->Order_model;

        // Start transaction — rollback after each test
        self::$CI->db->trans_start();
    }

    protected function tearDown(): void
    {
        self::$CI->db->trans_rollback();
    }

    /**
     * Characterization test: captures what get_active_orders currently returns.
     * Written BEFORE making changes. Do not modify this test — it documents
     * existing behavior. If it breaks, your change introduced a regression.
     */
    public function test_get_active_orders_returns_array_with_expected_keys(): void
    {
        // Insert known data
        self::$CI->db->insert('orders', [
            'status' => 'active',
            'customer_name' => 'Test Customer',
            'total' => 99.99,
            'created_at' => '2025-01-15 10:00:00',
        ]);

        $result = $this->model->get_active_orders();

        $this->assertIsArray($result);
        $this->assertNotEmpty($result);
        $this->assertArrayHasKey('status', $result[0]);
        $this->assertArrayHasKey('customer_name', $result[0]);
        $this->assertEquals('active', $result[0]['status']);
    }

    public function test_get_by_id_returns_null_for_nonexistent(): void
    {
        $result = $this->model->get_by_id(999999);
        $this->assertNull($result);
    }
}
```

The point is not to write perfect tests. The point is to have _something_ that catches regressions before you refactor.

#### Safe Refactoring: Extract Method, Then Extract Class

When you need to modify complex controller logic, do it in two steps. First, extract the logic into a private method without changing behavior. Run your characterization test. Then extract that method into its own service class.

Step 1 — Extract method (keep in same file):

```php
<?php
// BEFORE: logic tangled in controller method
class Reports extends CI_Controller
{
    public function monthly(): void
    {
        // 40 lines of calculation logic mixed with HTTP concerns...
    }
}

// AFTER: extract method — same behavior, easier to test
class Reports extends CI_Controller
{
    public function monthly(): void
    {
        $start = $this->input->get('start_date');
        $end = $this->input->get('end_date');

        $report = $this->build_monthly_report($start, $end);

        $this->load->view('reports/monthly', ['report' => $report]);
    }

    private function build_monthly_report(string $start, string $end): array
    {
        $this->load->model('Sales_model');
        $sales = $this->Sales_model->get_range($start, $end);

        $totals = [];
        foreach ($sales as $sale) {
            $month = date('Y-m', strtotime($sale['created_at']));
            $totals[$month] = ($totals[$month] ?? 0) + (float) $sale['amount'];
        }

        return [
            'period' => "$start to $end",
            'totals' => $totals,
            'grand_total' => array_sum($totals),
        ];
    }
}
```

Step 2 — Extract to service class (see Incremental Improvements below).

#### Feature Flag via Config

When you need to change behavior but want a rollback path, use a config toggle. This is especially useful for CI3 where deployments may not have feature flag infrastructure.

```php
<?php
// application/config/feature_flags.php
$config['use_new_tax_calculation'] = false;  // flip to true after validation

// In the controller or service:
$use_new = $this->config->item('use_new_tax_calculation');

if ($use_new) {
    $tax = $this->Tax_service->calculate_v2($order);
} else {
    $tax = $this->Tax_service->calculate($order);
}
```

Run both code paths side-by-side during testing. Once the new path is validated in production, remove the old path and the flag. Do not let feature flags accumulate.

### Incremental Improvements

#### Adding Composer

Most CI3 projects do not use Composer. Adding it lets you pull in modern PHP libraries (Monolog, Carbon, PHPUnit) and sets up PSR-4 autoloading for your new service classes.

Minimal `composer.json` at project root:

```json
{
    "name": "company/legacy-app",
    "description": "Legacy CI3 application",
    "type": "project",
    "require": {
        "php": ">=7.4"
    },
    "require-dev": {
        "phpunit/phpunit": "^9.6"
    },
    "autoload": {
        "psr-4": {
            "App\\Services\\": "application/services/"
        }
    }
}
```

Then require the Composer autoloader in `index.php`, before CI3 boots:

```php
<?php
// index.php — add near the top, before CI3 bootstrap
if (file_exists(__DIR__ . '/vendor/autoload.php')) {
    require_once __DIR__ . '/vendor/autoload.php';
}

// ... rest of CI3 index.php unchanged
```

Run `composer install` and commit both `composer.json` and `composer.lock`.

#### Extracting Business Logic into Services

This is the single most valuable thing you can do for eventual migration. Pull business logic out of controllers and models into plain PHP classes that have zero CI3 dependencies.

```php
<?php
// application/services/MonthlyReportBuilder.php

declare(strict_types=1);

namespace App\Services;

class MonthlyReportBuilder
{
    /**
     * Build a monthly totals report from raw sales data.
     *
     * @param array<int, array{created_at: string, amount: string|float}> $sales
     * @return array{period: string, totals: array<string, float>, grand_total: float}
     */
    public function build(string $startDate, string $endDate, array $sales): array
    {
        $totals = [];

        foreach ($sales as $sale) {
            $month = date('Y-m', strtotime($sale['created_at']));
            $totals[$month] = ($totals[$month] ?? 0.0) + (float) $sale['amount'];
        }

        ksort($totals);

        return [
            'period' => "{$startDate} to {$endDate}",
            'totals' => $totals,
            'grand_total' => array_sum($totals),
        ];
    }
}
```

Then use it from the controller:

```php
<?php
use App\Services\MonthlyReportBuilder;

class Reports extends CI_Controller
{
    public function monthly(): void
    {
        $start = $this->input->get('start_date');
        $end = $this->input->get('end_date');

        $this->load->model('Sales_model');
        $sales = $this->Sales_model->get_range($start, $end);

        $builder = new MonthlyReportBuilder();
        $report = $builder->build($start, $end, $sales);

        $this->load->view('reports/monthly', ['report' => $report]);
    }
}
```

The service class is pure PHP. When you migrate to FastAPI, translate `MonthlyReportBuilder` directly — the logic is already isolated from the framework.

#### Adding Type Hints Gradually

Do not rewrite entire files. Add type hints to methods as you touch them. Start with new code, then annotate existing methods when you modify them.

```php
<?php
// BEFORE — no types, implicit mixed everywhere
class Order_model extends CI_Model
{
    public function get_by_status($status)
    {
        return $this->db->where('status', $status)->get('orders')->result_array();
    }

    public function update_total($id, $total)
    {
        return $this->db->where('id', $id)->update('orders', ['total' => $total]);
    }
}

// AFTER — types added on methods you touched
class Order_model extends CI_Model
{
    /**
     * @return array<int, array<string, mixed>>
     */
    public function get_by_status(string $status): array
    {
        return $this->db->where('status', $status)->get('orders')->result_array();
    }

    public function update_total(int $id, float $total): bool
    {
        return $this->db->where('id', $id)->update('orders', ['total' => $total]);
    }
}
```

Add `declare(strict_types=1);` only to new files you create (like service classes). Adding it to existing CI3 files risks breaking code that relies on PHP's type coercion.

### Security

#### Query Bindings vs String Concatenation

This is the most common CI3 security issue. Never build queries with string concatenation. Use query bindings or the Query Builder.

```php
<?php
// DANGEROUS — SQL injection via $status
$query = $this->db->query("SELECT * FROM orders WHERE status = '$status'");

// DANGEROUS — SQL injection via $name
$query = $this->db->query(
    "SELECT * FROM users WHERE name = '" . $this->input->post('name') . "'"
);

// SAFE — query bindings with ? placeholders
$query = $this->db->query(
    'SELECT * FROM orders WHERE status = ? AND customer_id = ?',
    [$status, $customer_id]
);

// SAFE — Query Builder handles escaping
$result = $this->db
    ->where('status', $status)
    ->where('customer_id', $customer_id)
    ->get('orders')
    ->result_array();

// SAFE — LIKE with Query Builder
$result = $this->db
    ->like('name', $search_term)
    ->get('users')
    ->result_array();
```

When auditing CI3 code, search for `->query(` with string concatenation or variable interpolation. Every instance is a potential SQL injection.

#### Session Hardening Configuration

CI3 sessions default to cookie-based storage, which is insecure for anything beyond trivial data. Switch to database-backed sessions and harden the cookie settings.

```php
<?php
// application/config/config.php

// Use database driver instead of cookie/file
$config['sess_driver'] = 'database';
$config['sess_save_path'] = 'ci_sessions';  // table name

// Cookie security
$config['sess_cookie_name'] = 'ci_session';
$config['sess_expiration'] = 7200;          // 2 hours
$config['sess_match_ip'] = true;            // bind session to IP
$config['sess_time_to_update'] = 300;       // regenerate ID every 5 min
$config['sess_regenerate_destroy'] = true;  // destroy old session on regenerate

// Cookie hardening (applies to session cookie)
$config['cookie_httponly'] = true;           // no JavaScript access
$config['cookie_secure'] = true;            // HTTPS only
$config['cookie_samesite'] = 'Lax';         // CSRF protection (CI3.1.9+)
```

Create the sessions table:

```sql
CREATE TABLE IF NOT EXISTS `ci_sessions` (
    `id` varchar(128) NOT NULL,
    `ip_address` varchar(45) NOT NULL,
    `timestamp` int(10) unsigned DEFAULT 0 NOT NULL,
    `data` blob NOT NULL,
    KEY `ci_sessions_timestamp` (`timestamp`)
);
```

## Best Practices Summary

1. **Write a characterization test before changing anything.** No exceptions. If you cannot test it, at least document the current behavior in a comment before modifying it.
2. **Use query bindings for every database query.** Search the codebase for raw string concatenation in SQL — fix those first.
3. **Extract business logic into `application/services/` as plain PHP.** These classes survive the migration to the new stack.
4. **Add type hints only to code you are actively modifying.** Do not go on typing crusades through files you are not changing.
5. **Use feature flags for behavioral changes.** One config value, one if/else, clean removal when validated.
6. **Add Composer early.** It unlocks PSR-4 autoloading for services and gives you PHPUnit for characterization tests.
7. **Do not add `declare(strict_types=1)` to existing CI3 files.** Only use it in new service classes you create.
8. **Harden sessions immediately** if they are still cookie-based. This is the lowest-effort, highest-impact security fix.
9. **Keep changes small and reversible.** This codebase is in maintenance mode. Grand rewrites belong in the new stack.
10. **Every service you extract is one less thing to rewrite later.** Prioritize extracting the business logic that will be needed in the Python/FastAPI migration.
