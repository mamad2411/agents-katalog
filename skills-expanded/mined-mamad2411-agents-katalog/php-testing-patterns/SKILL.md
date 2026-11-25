---
name: php-testing-patterns
description: PHP testing patterns with PHPUnit, Pest, WordPress test framework (WP_UnitTestCase), Laravel test helpers, Sage testing, and CI3 legacy testing. Use when writing tests, setting up test infrastructure, or choosing a testing strategy.
---

# PHP Testing Patterns

Framework-aware testing patterns across the PHP stack: PHPUnit fundamentals, Pest's expressive syntax, WordPress integration tests with `WP_UnitTestCase`, Laravel's HTTP and database test helpers, Sage/Roots component testing, and adding tests to legacy CodeIgniter 3 codebases.

## When to Use This Skill

- Writing unit, integration, or feature tests for any PHP project
- Setting up a test suite for the first time (PHPUnit, Pest, WP test scaffold)
- Choosing between Pest and PHPUnit for a new project
- Testing WordPress plugins or themes (hooks, REST endpoints, factories)
- Testing Laravel controllers, Form Requests, jobs, events, or notifications
- Testing Sage Blade components or view composers
- Adding tests to untested legacy CI3 code

## Core Concepts

1. **Test isolation** -- each test must be independent. Use `setUp`/`tearDown` (PHPUnit) or `beforeEach`/`afterEach` (Pest) to guarantee a clean slate.
2. **Arrange-Act-Assert** -- set up preconditions, execute the behavior, verify the outcome.
3. **Test doubles** -- mocks verify interactions, stubs provide canned answers, spies record calls. Use the lightest double that proves the behavior.
4. **Framework test helpers exist for a reason** -- prefer `assertDatabaseHas`, factory methods, and `expect()` over raw PHPUnit equivalents.
5. **Test the behavior, not the implementation** -- assert on outcomes (HTTP status, database state, return values) rather than internal method calls.

## Quick Start

```php
<?php
namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

final class SmokeTest extends TestCase
{
    public function test_php_is_running(): void
    {
        $this->assertTrue(PHP_VERSION_ID >= 80100, 'PHP 8.1+ is required');
    }
}
```

Run with: `./vendor/bin/phpunit tests/Unit/SmokeTest.php`

---

## Fundamental Patterns

### Pattern 1: PHPUnit Test Class with setUp/tearDown

```php
<?php
namespace Tests\Unit;

use App\Services\InvoiceCalculator;
use App\ValueObjects\Money;
use App\ValueObjects\TaxRate;
use PHPUnit\Framework\TestCase;

final class InvoiceCalculatorTest extends TestCase
{
    private InvoiceCalculator $calculator;

    protected function setUp(): void
    {
        parent::setUp();
        $this->calculator = new InvoiceCalculator();
    }

    public function test_calculates_subtotal_from_line_items(): void
    {
        $lineItems = [
            ['description' => 'Widget A', 'quantity' => 3, 'unit_price' => 1000],
            ['description' => 'Widget B', 'quantity' => 1, 'unit_price' => 2500],
        ];

        $this->assertSame(5500, $this->calculator->subtotal($lineItems));
    }

    public function test_total_equals_subtotal_plus_tax(): void
    {
        $lineItems = [['description' => 'Service', 'quantity' => 1, 'unit_price' => 20000]];
        $taxRate = TaxRate::fromPercentage(10.0);

        $invoice = $this->calculator->calculate($lineItems, $taxRate);

        $this->assertSame(20000, $invoice->subtotal);
        $this->assertSame(2000, $invoice->tax);
        $this->assertSame(22000, $invoice->total);
    }
}
```

### Pattern 2: Data Providers for Parameterized Tests

Data providers run the same test logic against multiple input/output pairs.

```php
<?php
namespace Tests\Unit;

use App\Validators\EmailValidator;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class EmailValidatorTest extends TestCase
{
    private EmailValidator $validator;

    protected function setUp(): void
    {
        parent::setUp();
        $this->validator = new EmailValidator();
    }

    public static function emailProvider(): array
    {
        return [
            'standard email'       => ['user@example.com', true],
            'plus addressing'      => ['user+tag@example.com', true],
            'missing at sign'      => ['userexample.com', false],
            'missing domain'       => ['user@', false],
            'double dot in domain' => ['user@example..com', false],
            'empty string'         => ['', false],
        ];
    }

    #[DataProvider('emailProvider')]
    public function test_validates_email_addresses(string $email, bool $expected): void
    {
        $this->assertSame($expected, $this->validator->isValid($email));
    }
}
```

### Pattern 3: Test Doubles with Mockery

Mock an external dependency to test a service in isolation.

```php
<?php
namespace Tests\Unit;

use App\Contracts\PaymentGatewayInterface;
use App\DTOs\ChargeResult;
use App\Services\OrderService;
use Mockery;
use Mockery\Adapter\Phpunit\MockeryPHPUnitIntegration;
use PHPUnit\Framework\TestCase;

final class OrderServiceTest extends TestCase
{
    use MockeryPHPUnitIntegration;

    private OrderService $orderService;
    private PaymentGatewayInterface|Mockery\MockInterface $gateway;

    protected function setUp(): void
    {
        parent::setUp();
        $this->gateway = Mockery::mock(PaymentGatewayInterface::class);
        $this->orderService = new OrderService($this->gateway);
    }

    public function test_processes_order_when_payment_succeeds(): void
    {
        $this->gateway
            ->shouldReceive('charge')->once()
            ->with('tok_visa_123', 5000, 'usd')
            ->andReturn(new ChargeResult(success: true, transactionId: 'txn_abc', amount: 5000));

        $order = $this->orderService->placeOrder(token: 'tok_visa_123', amountCents: 5000, currency: 'usd');

        $this->assertSame('confirmed', $order->status);
        $this->assertSame('txn_abc', $order->transactionId);
    }

    public function test_spy_verifies_gateway_was_never_called_for_zero_amount(): void
    {
        $this->gateway->shouldNotReceive('charge');

        $order = $this->orderService->placeOrder(token: 'tok_visa_123', amountCents: 0, currency: 'usd');

        $this->assertSame('invalid', $order->status);
    }
}
```

### Pattern 4: Exception Testing

```php
<?php
namespace Tests\Unit;

use App\Exceptions\InsufficientFundsException;
use App\Exceptions\InvalidAccountException;
use App\Services\BankAccount;
use PHPUnit\Framework\TestCase;

final class BankAccountTest extends TestCase
{
    public function test_withdraw_throws_exception_when_insufficient_funds(): void
    {
        $account = new BankAccount(balance: 100_00);

        $this->expectException(InsufficientFundsException::class);
        $this->expectExceptionMessage('Cannot withdraw 15000 cents: only 10000 available');

        $account->withdraw(150_00);
    }

    public function test_transfer_throws_for_invalid_recipient(): void
    {
        $sender = new BankAccount(balance: 500_00);

        try {
            $sender->transferTo(accountId: 'nonexistent', amount: 100_00);
            $this->fail('Expected InvalidAccountException was not thrown');
        } catch (InvalidAccountException $e) {
            $this->assertSame('nonexistent', $e->getAccountId());
            $this->assertSame(500_00, $sender->getBalance());
        }
    }
}
```

### Pattern 5: Pest -- test()/it() Syntax with expect() API

```php
<?php
// tests/Unit/StringHelperTest.php
use App\Helpers\StringHelper;

test('slugifies a string correctly', function () {
    expect(StringHelper::slugify('Hello World! This is a Test.'))->toBe('hello-world-this-is-a-test');
});

test('truncates long strings with ellipsis', function () {
    expect(StringHelper::truncate('The quick brown fox jumps over the lazy dog', 20))
        ->toBeString()
        ->toHaveLength(20)
        ->toEndWith('...');
});

// Chained assertions on complex objects
test('user DTO has correct properties', function () {
    $user = new App\DTOs\UserDTO(name: 'Jane Doe', email: 'jane@example.com', role: 'admin');

    expect($user)
        ->name->toBe('Jane Doe')
        ->email->toContain('@')
        ->role->toBeIn(['admin', 'editor', 'viewer']);
});

// Collections with each()
test('all prices are positive integers', function () {
    expect([100, 250, 999, 50, 1200])
        ->each->toBeInt()
        ->each->toBeGreaterThan(0);
});
```

### Pattern 6: Pest -- beforeEach/afterEach Hooks

```php
<?php
// tests/Unit/CartTest.php
use App\Services\Cart;
use App\Models\Product;

beforeEach(function () {
    $this->cart = new Cart();
    $this->productA = new Product(id: 1, name: 'Widget', priceCents: 1500);
    $this->productB = new Product(id: 2, name: 'Gadget', priceCents: 3000);
});

test('adds a product to the cart', function () {
    $this->cart->add($this->productA, quantity: 2);

    expect($this->cart)
        ->itemCount()->toBe(2)
        ->totalCents()->toBe(3000);
});

test('calculates total with multiple products', function () {
    $this->cart->add($this->productA, quantity: 2); // 3000
    $this->cart->add($this->productB, quantity: 1); // 3000

    expect($this->cart->totalCents())->toBe(6000);
});
```

### Pattern 7: Pest -- Arch Testing

Enforce project architecture conventions without testing runtime behavior.

```php
<?php
// tests/Arch/ArchitectureTest.php

arch('models extend Eloquent base model')
    ->expect('App\Models')
    ->toExtend('Illuminate\Database\Eloquent\Model');

arch('controllers have Controller suffix')
    ->expect('App\Http\Controllers')
    ->toHaveSuffix('Controller');

arch('no debugging statements left in source code')
    ->expect(['dd', 'dump', 'ray', 'var_dump', 'print_r'])
    ->not->toBeUsed();

arch('value objects are readonly and final')
    ->expect('App\ValueObjects')
    ->toBeFinal()
    ->toBeReadonly();

arch('contracts directory contains only interfaces')
    ->expect('App\Contracts')
    ->toBeInterfaces();

arch('domain layer does not depend on infrastructure')
    ->expect('App\Domain')
    ->not->toUse(['Illuminate\Http', 'Illuminate\Routing']);
```

### Pattern 8: Decision Guide -- Pest vs PHPUnit

| Factor               | PHPUnit                         | Pest                                     |
| -------------------- | ------------------------------- | ---------------------------------------- |
| Team experience      | Team knows PHPUnit              | Open to new tools                        |
| Project type         | Library/framework (open source) | Application code (Laravel, WP, internal) |
| Existing suite       | Large existing PHPUnit suite    | Greenfield or small suite                |
| IDE support          | Full class-based refactoring    | Closure-based files                      |
| Architecture testing | Not built-in                    | Built-in `arch()`                        |
| Assertion style      | Explicit `$this->assert*()`     | Fluent `expect()->` chains               |

**Rule of thumb:** Default to Pest for Laravel/Sage. Use PHPUnit directly for WP plugins extending `WP_UnitTestCase` and for open-source PHP libraries. Pest wraps PHPUnit, so both can coexist.

---

## Advanced Patterns

### Pattern 9: WordPress -- WP_UnitTestCase with Factory Methods

Factory methods create real database records that are rolled back after each test.

```php
<?php
namespace Tests\Integration;

use WP_UnitTestCase;

final class CustomPostTypeQueryTest extends WP_UnitTestCase
{
    private int $authorId;

    public function set_up(): void
    {
        parent::set_up();
        $this->authorId = self::factory()->user->create(['role' => 'editor']);
    }

    public function test_factory_creates_posts_and_queries_them(): void
    {
        $postIds = self::factory()->post->create_many(3, [
            'post_type'   => 'post',
            'post_status' => 'publish',
            'post_author' => $this->authorId,
        ]);
        // Draft should NOT appear
        self::factory()->post->create(['post_type' => 'post', 'post_status' => 'draft', 'post_author' => $this->authorId]);

        $query = new \WP_Query([
            'post_type' => 'post', 'post_status' => 'publish', 'author' => $this->authorId,
        ]);

        $this->assertSame(3, $query->found_posts);
    }

    public function test_factory_creates_posts_with_meta(): void
    {
        $postId = self::factory()->post->create([
            'post_status' => 'publish',
            'meta_input'  => ['price' => '29.99', 'currency' => 'USD'],
        ]);

        $this->assertSame('29.99', get_post_meta($postId, 'price', true));
        $this->assertSame('USD', get_post_meta($postId, 'currency', true));
    }
}
```

### Pattern 10: WordPress -- Testing Hook Registrations

Verify that your plugin registers the correct actions and filters.

```php
<?php
namespace Tests\Integration;

use App\Plugin\MyPlugin;
use WP_UnitTestCase;

final class HookRegistrationTest extends WP_UnitTestCase
{
    private MyPlugin $plugin;

    public function set_up(): void
    {
        parent::set_up();
        $this->plugin = new MyPlugin();
        $this->plugin->register();
    }

    public function test_registers_init_action(): void
    {
        $priority = has_action('init', [$this->plugin, 'registerPostTypes']);
        $this->assertNotFalse($priority);
        $this->assertSame(10, $priority);
    }

    public function test_filter_modifies_content(): void
    {
        $postId = self::factory()->post->create(['post_content' => 'Original.', 'post_status' => 'publish']);
        $this->go_to(get_permalink($postId));

        $filtered = apply_filters('the_content', 'Original.');

        $this->assertStringContainsString('Original.', $filtered);
        $this->assertStringContainsString('Disclaimer:', $filtered);
    }
}
```

### Pattern 11: WordPress -- Testing REST Endpoints

Test custom REST API routes end-to-end within the WordPress test framework.

```php
<?php
namespace Tests\Integration;

use WP_REST_Request;
use WP_REST_Server;
use WP_UnitTestCase;

final class EventsRestControllerTest extends WP_UnitTestCase
{
    private WP_REST_Server $server;

    public function set_up(): void
    {
        parent::set_up();
        global $wp_rest_server;
        $this->server = $wp_rest_server = new WP_REST_Server();
        do_action('rest_api_init');
    }

    public function tear_down(): void
    {
        global $wp_rest_server;
        $wp_rest_server = null;
        parent::tear_down();
    }

    public function test_get_events_returns_published_events(): void
    {
        self::factory()->post->create_many(3, ['post_type' => 'event', 'post_status' => 'publish']);

        $response = $this->server->dispatch(new WP_REST_Request('GET', '/myplugin/v1/events'));

        $this->assertSame(200, $response->get_status());
        $this->assertCount(3, $response->get_data());
    }

    public function test_create_event_requires_authentication(): void
    {
        $request = new WP_REST_Request('POST', '/myplugin/v1/events');
        $request->set_body_params(['title' => 'New Event', 'date' => '2026-06-15']);

        $this->assertSame(401, $this->server->dispatch($request)->get_status());
    }

    public function test_create_event_succeeds_for_editors(): void
    {
        wp_set_current_user(self::factory()->user->create(['role' => 'editor']));

        $request = new WP_REST_Request('POST', '/myplugin/v1/events');
        $request->set_body_params(['title' => 'Annual Conference', 'date' => '2026-09-20']);

        $response = $this->server->dispatch($request);
        $this->assertSame(201, $response->get_status());
        $this->assertSame('Annual Conference', $response->get_data()['title']);
    }
}
```

### Pattern 12: WordPress -- Mocking with Brain Monkey

Unit-test WordPress-dependent code without loading WordPress.

```php
<?php
namespace Tests\Unit;

use App\Services\SettingsManager;
use Brain\Monkey;
use Brain\Monkey\Functions;
use Mockery\Adapter\Phpunit\MockeryPHPUnitIntegration;
use PHPUnit\Framework\TestCase;

final class SettingsManagerTest extends TestCase
{
    use MockeryPHPUnitIntegration;

    protected function setUp(): void
    {
        parent::setUp();
        Monkey\setUp();
    }

    protected function tearDown(): void
    {
        Monkey\tearDown();
        parent::tearDown();
    }

    public function test_get_setting_reads_from_wp_options(): void
    {
        Functions\expect('get_option')
            ->once()->with('myplugin_api_key', '')->andReturn('sk_live_abc123');

        $this->assertSame('sk_live_abc123', (new SettingsManager())->get('api_key'));
    }

    public function test_save_setting_calls_update_option(): void
    {
        Functions\expect('update_option')
            ->once()->with('myplugin_api_key', 'sk_live_new456')->andReturn(true);
        Functions\expect('sanitize_text_field')
            ->once()->with('sk_live_new456')->andReturnFirstArg();

        $this->assertTrue((new SettingsManager())->save('api_key', 'sk_live_new456'));
    }
}
```

### Pattern 13: Laravel -- Feature Test with HTTP Assertions

Send real HTTP requests through the application stack.

```php
<?php
namespace Tests\Feature;

use App\Models\Article;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class ArticleControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_index_returns_published_articles(): void
    {
        Article::factory()->published()->count(3)->create();
        Article::factory()->draft()->count(2)->create();

        $this->getJson('/api/articles')
            ->assertOk()
            ->assertJsonCount(3, 'data')
            ->assertJsonStructure([
                'data' => [['id', 'title', 'slug', 'excerpt', 'published_at']],
                'meta' => ['current_page', 'last_page', 'total'],
            ]);
    }

    public function test_store_requires_authentication(): void
    {
        $this->postJson('/api/articles', ['title' => 'Test', 'body' => 'Content'])
            ->assertUnauthorized();
    }

    public function test_store_creates_article_for_authenticated_user(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)->postJson('/api/articles', [
            'title' => 'My New Article',
            'body'  => 'Article body content here.',
            'tags'  => ['php', 'testing'],
        ])
            ->assertCreated()
            ->assertJsonPath('data.title', 'My New Article')
            ->assertJsonPath('data.author.id', $user->id);
    }
}
```

### Pattern 14: Laravel -- Database Assertions

Assert on database state after operations.

```php
<?php
namespace Tests\Feature;

use App\Models\Subscription;
use App\Models\User;
use App\Services\SubscriptionService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class SubscriptionServiceTest extends TestCase
{
    use RefreshDatabase;

    private SubscriptionService $service;

    protected function setUp(): void
    {
        parent::setUp();
        $this->service = app(SubscriptionService::class);
    }

    public function test_subscribe_creates_database_record(): void
    {
        $user = User::factory()->create();
        $this->service->subscribe($user, plan: 'pro', interval: 'monthly');

        $this->assertDatabaseHas('subscriptions', [
            'user_id' => $user->id, 'plan' => 'pro', 'status' => 'active',
        ]);
    }

    public function test_cancel_soft_deletes_subscription(): void
    {
        $user = User::factory()->create();
        $sub = Subscription::factory()->active()->create(['user_id' => $user->id, 'plan' => 'pro']);

        $this->service->cancel($sub);

        $this->assertSoftDeleted('subscriptions', ['id' => $sub->id, 'status' => 'cancelled']);
        $this->assertDatabaseMissing('subscriptions', [
            'user_id' => $user->id, 'status' => 'active', 'deleted_at' => null,
        ]);
    }
}
```

### Pattern 15: Laravel -- Faking Queues, Events, and Notifications

Assert jobs were dispatched, events fired, or notifications sent -- without executing side effects.

```php
<?php
namespace Tests\Feature;

use App\Events\OrderPlaced;
use App\Jobs\SendOrderConfirmation;
use App\Jobs\UpdateInventory;
use App\Models\Order;
use App\Models\User;
use App\Notifications\OrderShippedNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\{Event, Notification, Queue};
use Tests\TestCase;

final class OrderWorkflowTest extends TestCase
{
    use RefreshDatabase;

    public function test_placing_order_dispatches_jobs(): void
    {
        Queue::fake();
        $user = User::factory()->create();

        $this->actingAs($user)->postJson('/api/orders', [
            'items' => [['product_id' => 1, 'quantity' => 2]],
        ])->assertCreated();

        Queue::assertPushed(SendOrderConfirmation::class, fn ($job) => $job->userId === $user->id);
        Queue::assertPushed(UpdateInventory::class);
    }

    public function test_placing_order_fires_event(): void
    {
        Event::fake([OrderPlaced::class]);
        $user = User::factory()->create();

        $this->actingAs($user)->postJson('/api/orders', [
            'items' => [['product_id' => 1, 'quantity' => 1]],
        ]);

        Event::assertDispatched(OrderPlaced::class, fn ($e) => $e->order->user_id === $user->id);
    }

    public function test_shipping_order_sends_notification(): void
    {
        Notification::fake();
        $user  = User::factory()->create();
        $order = Order::factory()->for($user)->create(['status' => 'processing']);

        $this->actingAs($user)->postJson("/api/orders/{$order->id}/ship");

        Notification::assertSentTo($user, OrderShippedNotification::class);
    }
}
```

### Pattern 16: Laravel -- Testing Form Requests

Test validation rules in isolation.

```php
<?php
namespace Tests\Unit;

use App\Http\Requests\StoreProductRequest;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

final class StoreProductRequestTest extends TestCase
{
    private function validate(array $data): \Illuminate\Validation\Validator
    {
        return Validator::make($data, (new StoreProductRequest())->rules());
    }

    public function test_valid_product_data_passes(): void
    {
        $this->assertTrue($this->validate([
            'name' => 'Premium Widget', 'slug' => 'premium-widget',
            'price' => 29.99, 'category_id' => 1, 'sku' => 'WDG-PREM-001',
        ])->passes());
    }

    public function test_name_is_required(): void
    {
        $v = $this->validate(['name' => '', 'price' => 10.00]);
        $this->assertTrue($v->fails());
        $this->assertArrayHasKey('name', $v->errors()->toArray());
    }

    public function test_price_must_be_positive(): void
    {
        $v = $this->validate(['name' => 'Widget', 'price' => -5.00]);
        $this->assertTrue($v->fails());
        $this->assertArrayHasKey('price', $v->errors()->toArray());
    }
}
```

### Pattern 17: Sage -- Testing Blade Components and View Composers

Test Sage view composers that pass WordPress data to Blade templates.

```php
<?php
namespace Tests\Feature;

use App\View\Composers\NavigationComposer;
use Tests\TestCase;

final class NavigationComposerTest extends TestCase
{
    public function test_composer_provides_primary_menu_data(): void
    {
        register_nav_menus(['primary_navigation' => 'Primary Navigation']);
        $menuId = wp_create_nav_menu('Test Primary');
        wp_update_nav_menu_item($menuId, 0, [
            'menu-item-title' => 'Home', 'menu-item-url' => home_url('/'), 'menu-item-status' => 'publish',
        ]);

        $locations = get_theme_mod('nav_menu_locations', []);
        $locations['primary_navigation'] = $menuId;
        set_theme_mod('nav_menu_locations', $locations);

        $data = (new NavigationComposer())->with();

        $this->assertArrayHasKey('primaryMenu', $data);
        $this->assertSame('Home', $data['primaryMenu'][0]->title);
    }
}

final class AlertComponentTest extends TestCase
{
    public function test_renders_with_default_info_type(): void
    {
        $this->blade('<x-alert message="Heads up!" />')
            ->assertSee('Heads up!')
            ->assertSee('bg-blue-100');
    }

    public function test_renders_error_alert_with_dismiss_button(): void
    {
        $this->blade('<x-alert type="error" message="Something failed." :dismissible="true" />')
            ->assertSee('bg-red-100')
            ->assertSee('button');
    }
}
```

### Pattern 18: CI3 -- Adding PHPUnit and Characterization Tests

Add tests to a legacy CodeIgniter 3 project. Characterization tests capture existing behavior before refactoring.

**Bootstrap setup** (`tests/bootstrap.php`):

```php
<?php
define('ENVIRONMENT', 'testing');
define('BASEPATH', __DIR__ . '/../system/');
define('APPPATH', __DIR__ . '/../application/');
define('VIEWPATH', APPPATH . 'views/');
define('FCPATH', __DIR__ . '/../');
define('SYSDIR', 'system');

require_once __DIR__ . '/../vendor/autoload.php';
require_once BASEPATH . 'core/Common.php';
require_once BASEPATH . 'core/Controller.php';

function &get_instance()
{
    return CI_Controller::get_instance();
}
```

**Characterization test for an existing CI3 model:**

```php
<?php
namespace Tests;

use PHPUnit\Framework\TestCase;
use Mockery;

final class ProductModelCharacterizationTest extends TestCase
{
    public function test_calculate_discount_applies_percentage(): void
    {
        $model = $this->createPartialModel();

        $this->assertSame(80.0, $model->calculate_discount(100, 20));
        $this->assertSame(0.0, $model->calculate_discount(100, 150)); // capped at 100%
    }

    public function test_get_active_products_queries_database(): void
    {
        $dbMock = Mockery::mock('CI_DB_query_builder');
        $dbMock->shouldReceive('where')->once()->with('status', 'active')->andReturnSelf();
        $dbMock->shouldReceive('order_by')->once()->with('name', 'asc')->andReturnSelf();
        $dbMock->shouldReceive('get')->once()->with('products')->andReturnSelf();
        $dbMock->shouldReceive('result')->once()->andReturn([
            (object) ['id' => 1, 'name' => 'Alpha', 'status' => 'active'],
        ]);

        $model = $this->createPartialModel();
        $model->db = $dbMock;

        $this->assertCount(1, $model->get_active_products());
    }

    private function createPartialModel(): \Product_model
    {
        require_once APPPATH . 'models/Product_model.php';
        return (new \ReflectionClass(\Product_model::class))->newInstanceWithoutConstructor();
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }
}
```

---

## Best Practices Summary

1. **One assertion concept per test.** Multiple `assert*` calls for the same logical outcome are fine; avoid testing unrelated behaviors in a single method.
2. **Name tests after the behavior.** Use `test_rejects_expired_coupon` not `test_validate_coupon_method`.
3. **Use data providers for input variations.** Eliminates duplication when 5+ cases differ only by input/output.
4. **Mock at the boundary, not everywhere.** Mock external services, not the class under test or its value objects.
5. **Use framework test helpers.** `assertDatabaseHas`, factory methods, `expect()` reduce boilerplate.
6. **Keep the test database fast.** Use `RefreshDatabase` or WP's transaction rollback. Avoid seeding large datasets.
7. **Run tests in CI on every push.** A suite that only runs locally rots.
8. **For legacy code, start with characterization tests.** Document what the code actually does before refactoring.
